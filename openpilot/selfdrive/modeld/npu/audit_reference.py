"""Preserve complete-data provenance and both precision diagnostics after a failed run."""
import argparse
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort

from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, validate_road_manifest, verify_graphs
from openpilot.selfdrive.modeld.npu.diagnose_case import compare_saved
from openpilot.selfdrive.modeld.npu.prepare_graph import SOURCE_SHA
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.reference_dataset import initial_states, options


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('work', type=Path)
  parser.add_argument('--report-name', default='reference-report.json')
  args = parser.parse_args()
  work = args.work.resolve()
  graph, dataset, road = work / 'artifacts/graph-v1', work / 'data/calibration500-v2', work / 'data/road700-v2'
  report_path = dataset / args.report_name
  if report_path.parent != dataset or report_path.exists():
    raise ValueError('requires a fresh report name inside the dataset')
  verify_graphs(graph / 'reference_fp16.onnx', graph / 'quantization_source_fp32.onnx')
  manifest = json.loads((road / 'manifest.json').read_text())
  records = validate_road_manifest(manifest, 500)
  if len(records) != 500:
    raise ValueError('requires all 500 prepared road frames')
  fp32_path = work / 'artifacts/semantic_reference_fp32.onnx'
  semantic_receipt = json.loads(fp32_path.with_suffix('.json').read_text())
  if semantic_receipt['original_sha256'] != SOURCE_SHA or digest(fp32_path) != semantic_receipt['semantic_reference_sha256']:
    raise ValueError('wrong independent semantic reference')
  derivative = ort.InferenceSession(str(graph / 'quantization_source_fp32.onnx'), sess_options=options(), providers=['CPUExecutionProvider'])
  reference = ort.InferenceSession(str(graph / 'reference_fp16.onnx'), sess_options=options(), providers=['CPUExecutionProvider'])
  semantic = ort.InferenceSession(str(fp32_path), sess_options=options(), providers=['CPUExecutionProvider'])
  lines, files = (dataset / 'input_list.txt').read_text().splitlines(), []
  if len(lines) != 500:
    raise ValueError('native list incomplete')
  previous_image = np.zeros((2, 5, 6, 128, 256), dtype=np.uint8)
  states = initial_states(reference)
  for index, record in enumerate(records):
    road_path = (road / record['file']).resolve()
    if not road_path.is_relative_to(road) or digest(road_path) != record['sha256']:
      raise ValueError('changed road file')
    with np.load(road_path) as raw:
      controls = {name: raw[name] for name in raw.files}
    listed = dict(value.split(':=', 1) for value in lines[index].split())
    if set(listed) != {item.name for item in derivative.get_inputs()}:
      raise ValueError('wrong native input names')
    for item in derivative.get_inputs():
      path = dataset / f'{index:06d}' / (item.name + '.raw')
      if Path(listed[item.name]).resolve() != path.resolve():
        raise ValueError('native list references wrong path')
      value = np.fromfile(path, dtype=np.float32).reshape(item.shape)
      if not np.isfinite(value).all():
        raise ValueError('invalid native input')
      if item.name in controls and not np.array_equal(value, controls[item.name]):
        raise ValueError('wrong native control input')
      if item.name in states and not np.array_equal(value, states[item.name]):
        raise ValueError(f'wrong fresh-reference recurrence at frame {index}: {item.name}')
      if item.name == 'updated_state_img_q':
        expected = np.concatenate([previous_image[:, 1:], controls['new_img'][:, None]], axis=1)
        if not np.array_equal(expected, value):
          raise ValueError('image FIFO mismatch')
      files.append({'file': str(path.relative_to(dataset)), 'sha256': digest(path)})
    previous_image = expected
    output_names = [item.name for item in reference.get_outputs()]
    result = dict(zip(output_names, reference.run(output_names, controls | states), strict=True))
    if not all(np.isfinite(value).all() for value in result.values()):
      raise ValueError('nonfinite replayed reference')
    states = {name: result['next_' + name] for name in states}
    if index % 25 == 0:
      print(f'recurrent provenance {index + 1}/500', flush=True)
  indices = np.linspace(0, 499, 10, dtype=int)
  comparisons, same_precision = [], []
  for index in indices:
    comparisons.append(compare_saved(work, int(index), reference, derivative))
    same_precision.append(compare_saved(work, int(index), semantic, derivative))
    print(index, 'FP16:', comparisons[-1]['packed'], 'FP32:', same_precision[-1]['packed'], flush=True)
  failures = sum(row['packed']['outside_atol_0p01_rtol_0p01'] for row in comparisons)
  report = {'reference_sha256': REFERENCE_SHA, 'derivative_sha256': DERIVATIVE_SHA,
            'semantic_reference_sha256': semantic_receipt['semantic_reference_sha256'],
            'road_manifest_sha256': digest(road / 'manifest.json'), 'frames': 500, 'native_inputs': files,
            'input_list_sha256': digest(dataset / 'input_list.txt'), 'comparisons': comparisons,
            'same_precision_comparisons': same_precision, 'strict_fp16_gate': 'fail' if failures else 'pass',
            'reference_recurrence_verified_frames': 500,
            'outside_fp16_tolerance': failures, 'generator': 'completed calibration500-v2 followed by independent post-failure audit',
            'limits': 'Same-precision equivalence does not erase FP16 precision failures or qualify INT8. No threshold is changed.'}
  report_path.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
  main()
