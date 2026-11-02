"""Inspect an individual pre-quantization mismatch using saved reference state."""
import argparse
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort

from openpilot.selfdrive.modeld.npu.contracts import verify_graphs
from openpilot.selfdrive.modeld.npu.prepare_graph import HEADS, SOURCE_SHA
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.reference_dataset import errors, options


def compare_saved(work, index, reference, derivative, dataset=None, road_offset=0):
  dataset = dataset or work / 'data/calibration500-v2'
  with np.load(work / 'data/road700-v2' / f'{road_offset + index:06d}.npz') as raw:
    controls = {name: raw[name] for name in raw.files}
  feeds = {item.name: np.fromfile(dataset / f'{index:06d}' / (item.name + '.raw'), dtype=np.float32).reshape(item.shape)
           for item in derivative.get_inputs()}
  if index:
    previous_image = np.fromfile(dataset / f'{index - 1:06d}/updated_state_img_q.raw', dtype=np.float32).astype(np.uint8)
    previous_image = previous_image.reshape(2, 5, 6, 128, 256)
  else:
    previous_image = np.zeros((2, 5, 6, 128, 256), dtype=np.uint8)
  rfeeds = controls | {'state_img_q': previous_image, 'state_desire_q': feeds['state_desire_q'], 'state_feat_q': feeds['state_feat_q']}
  expected = reference.run(['outputs'], rfeeds)[0]
  outputs = derivative.run(None, feeds)
  packed, offset, detail = np.concatenate(outputs, axis=1), 0, {}
  for head, output in zip(HEADS, outputs, strict=True):
    ref = expected[:, offset:offset + output.shape[1]]
    bad = np.flatnonzero(np.abs(output - ref) > .01 + .01 * np.abs(ref))
    detail[head] = errors(ref, output) | {'failures': [{'index': int(i), 'reference': float(ref.flat[i]),
                                                     'actual': float(output.flat[i]), 'fp16_rounded_actual': float(np.float16(output.flat[i]))}
                                                    for i in bad]}
    offset += output.shape[1]
  result = {'index': index, 'road_index': road_offset + index, 'dataset': str(dataset), 'packed': errors(expected, packed), 'heads': detail}
  return result


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('work', type=Path)
  parser.add_argument('--index', type=int, required=True)
  parser.add_argument('--same-precision', action='store_true')
  parser.add_argument('--dataset', type=Path)
  parser.add_argument('--road-offset', type=int, default=0)
  args = parser.parse_args()
  work, index = args.work, args.index
  graph = work / 'artifacts/graph-v1'
  reference_path, derivative_path = graph / 'reference_fp16.onnx', graph / 'quantization_source_fp32.onnx'
  verify_graphs(reference_path, derivative_path)
  if args.same_precision:
    reference_path = work / 'artifacts/semantic_reference_fp32.onnx'
    receipt = json.loads(reference_path.with_suffix('.json').read_text())
    if receipt['original_sha256'] != SOURCE_SHA or digest(reference_path) != receipt['semantic_reference_sha256']:
      raise ValueError('wrong same-precision semantic reference')
  reference = ort.InferenceSession(str(reference_path), sess_options=options(), providers=['CPUExecutionProvider'])
  derivative = ort.InferenceSession(str(derivative_path), sess_options=options(), providers=['CPUExecutionProvider'])
  result = compare_saved(work, index, reference, derivative, dataset=args.dataset, road_offset=args.road_offset)
  result['precision'] = 'fp32' if args.same_precision else 'fp16'
  destination = work / 'artifacts' / f'diagnostic-{index}{"-fp32" if args.same_precision else ""}.json'
  destination.write_text(json.dumps(result, indent=2) + '\n')
  print(json.dumps(result, indent=2))


if __name__ == '__main__':
  main()
