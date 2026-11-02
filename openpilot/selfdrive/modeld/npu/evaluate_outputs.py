"""Measure held-out QNN outputs against this release's independently reset FP16 reference."""
import argparse
import json
from pathlib import Path

import numpy as np

from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, verify_native_inputs
from openpilot.selfdrive.modeld.npu.contracts import HEADS, SIZES
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.metrics import errors

INPUT_SHAPES = {'desire': [8], 'traffic_convention': [1, 2], 'action_t': [1, 2],
                'state_desire_q': [132, 1, 8], 'state_feat_q': [128, 1, 16384], 'updated_state_img_q': [2, 5, 6, 128, 256]}


IO_MODE = 'float_files_host_quantize_dequantize'


def tensor_contract(tensor, shape, encodings):
  if tensor['dimensions'] != shape:
    raise ValueError('compiled tensor shape changed')
  if encodings is None:
    if tensor['dataType'] != 'QNN_DATATYPE_FLOAT_32':
      raise ValueError('compiled tensor dtype changed')
    return
  expected = encodings[tensor['name']]
  quantization = tensor['quantizeParams']
  if (tensor['dataType'] != 'QNN_DATATYPE_UFIXED_POINT_8' or expected['bitwidth'] != 8 or
      quantization['definition'] != 'QNN_DEFINITION_DEFINED' or
      quantization['quantizationEncoding'] != 'QNN_QUANTIZATION_ENCODING_SCALE_OFFSET' or
      quantization['scaleOffset'] != {'scale': expected['scale'], 'offset': expected['offset']} or
      not np.isfinite(expected['scale']) or expected['scale'] <= 0 or not -255 <= expected['offset'] <= 0):
    raise ValueError('compiled integer IO encoding differs from calibrated boundary')


def output_contract(metadata, io_encodings=None):
  info = metadata['info']
  if (info['numGraphs'] != 1 or info['socModel'] != 37 or info['contextMetadata']['info']['dspArch'] != 68 or
      not info['buildId'].startswith('v2.37.1.250807')):
    raise ValueError('requires one inspected SDK2.37 v68/SoC37 QNN graph')
  graph = info['graphs'][0]['info']
  inputs = {item['info']['name']: item['info'] for item in graph['graphInputs']}
  if set(inputs) != set(INPUT_SHAPES) or len(inputs) != len(graph['graphInputs']):
    raise ValueError('compiled input names do not match this model')
  for name, shape in INPUT_SHAPES.items():
    tensor_contract(inputs[name], shape, io_encodings)
  actual = {item['info']['name']: item['info'] for item in graph['graphOutputs']}
  if len(actual) != len(graph['graphOutputs']):
    raise ValueError('duplicate compiled output names')
  expected = {'q8b_' + head: size for head, size in zip(HEADS, SIZES, strict=True) if head != 'pad'}
  if set(actual) not in (set(expected), set(expected) | {'q8b_pad'}):
    raise ValueError('compiled output names do not match this model')
  for name, size in expected.items():
    tensor_contract(actual[name], [1, size], io_encodings)
  if io_encodings is not None and set(io_encodings) != set(inputs) | set(actual):
    raise ValueError('calibrated IO encoding coverage changed')
  if 'q8b_pad' in actual and (actual['q8b_pad']['dimensions'] != [1, 2] or
                            actual['q8b_pad']['dataType'] != 'QNN_DATATYPE_FLOAT_32'):
    raise ValueError('compiled padding contract changed')
  return actual


def read_outputs(folder, contract):
  pieces = []
  for head, size in zip(HEADS, SIZES, strict=True):
    name = 'q8b_' + head
    value = np.fromfile(folder / (name + '.raw'), dtype=np.float32) if name in contract else np.zeros(size, np.float32)
    if value.size != size or not np.isfinite(value).all():
      raise ValueError(f'invalid QNN output: {name}')
    if head == 'pad' and np.any(value):
      raise ValueError('expected zero padding')
    pieces.append(value)
  return np.concatenate(pieces).reshape(1, -1)


def verify_run(run, context, metadata, input_list, output_files):
  if (not run.get('command') or any(arg.split('=', 1)[0] in ['--use_native_input_files', '--use_native_output_files']
                                   for arg in run['command'])):
    raise ValueError('execution did not use the reviewed host float-file IO mode')
  expected = {'context_sha256': digest(context), 'context_info_sha256': digest(metadata),
              'input_list_sha256': digest(input_list), 'qnn_output_files': output_files, 'exit_code': 0, 'io_mode': IO_MODE}
  if any(run.get(key) != value for key, value in expected.items()):
    raise ValueError('execution receipt does not bind the context, inputs and outputs')


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--context', type=Path, required=True)
  parser.add_argument('--context-info', type=Path, required=True)
  parser.add_argument('--reference-data', type=Path, required=True)
  parser.add_argument('--qnn-outputs', type=Path, required=True)
  parser.add_argument('--run-receipt', type=Path, required=True, help='Recorded by the executor after successful QNN execution')
  parser.add_argument('--report', type=Path, required=True)
  args = parser.parse_args()
  if args.report.exists():
    parser.error('existing report preserved')
  root = args.reference_data.resolve()
  receipt = root / 'reference-report.json'
  reference = json.loads(receipt.read_text())
  if (reference['reference_sha256'] != REFERENCE_SHA or reference['derivative_sha256'] != DERIVATIVE_SHA or
      reference['start_frame'] != 500 or reference['frames'] != 200):
    raise ValueError('requires independently reset disjoint held-out inputs and 132-frame warmup')
  input_list = root / 'input_list.txt'
  verify_native_inputs(input_list, reference)
  files = reference['reference_outputs']
  if len(files) != reference['frames']:
    raise ValueError('incomplete floating output receipt')
  run = json.loads(args.run_receipt.read_text())
  contract = output_contract(json.loads(args.context_info.read_text()), run.get('io_encodings'))
  expected, actual, outputs = [], [], []
  for index, entry in enumerate(files):
    path = (root / entry['file']).resolve()
    if not path.is_relative_to(root) or digest(path) != entry['sha256']:
      raise ValueError('floating output provenance changed')
    candidate_folder = args.qnn_outputs / f'Result_{index}'
    candidate = read_outputs(candidate_folder, contract)
    golden = np.load(path, allow_pickle=False)
    if golden.shape != candidate.shape or not np.isfinite(golden).all():
      raise ValueError('invalid floating output')
    outputs.extend({'file': str(p.relative_to(args.qnn_outputs)), 'sha256': digest(p)}
                   for p in sorted(candidate_folder.glob('*.raw')))
    if index >= 132:
      expected.append(golden)
      actual.append(candidate)
  verify_run(run, args.context, args.context_info, input_list, outputs)
  expected, actual = np.concatenate(expected), np.concatenate(actual)
  offset, heads = 0, {}
  for head, size in zip(HEADS, SIZES, strict=True):
    heads[head] = errors(expected[:, offset:offset + size], actual[:, offset:offset + size])
    offset += size
  report = {'context_sha256': digest(args.context), 'context_info_sha256': digest(args.context_info),
            'reference_receipt_sha256': digest(receipt), 'qnn_output_files': outputs,
            'run_receipt_sha256': digest(args.run_receipt), 'source_start_frame': 500, 'source_end_frame': 699,
            'warmup_frames': 132, 'evaluated_frames': len(expected), 'packed': errors(expected, actual), 'heads': heads,
            'qualification': 'unqualified tensor diagnostics; no driving-accuracy percentage',
            'state_policy': 'teacher-forced current FP16 reference states; candidate closed-loop recurrence not measured'}
  args.report.write_text(json.dumps(report, indent=2) + '\n')
  print(json.dumps({key: value for key, value in report.items() if key != 'qnn_output_files'}, indent=2))


if __name__ == '__main__':
  main()
