"""Generate fresh model states and a native-input calibration list on the x86 host."""
import argparse
import json
import hashlib
from pathlib import Path
import time

import numpy as np
import onnxruntime as ort

from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, validate_road_manifest, verify_graphs
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.prepare_graph import HEADS


def options():
  config = ort.SessionOptions()
  config.intra_op_num_threads = 6
  config.inter_op_num_threads = 1
  return config


def initial_states(session):
  types = {'tensor(float)': np.float32, 'tensor(uint8)': np.uint8}
  return {item.name: np.zeros(item.shape, types[item.type]) for item in session.get_inputs() if item.name.startswith('state_')}


def errors(reference, actual):
  if reference.shape != actual.shape or not np.isfinite(reference).all() or not np.isfinite(actual).all():
    raise ValueError('nonfinite or mismatched output')
  difference = actual.astype(np.float64) - reference.astype(np.float64)
  scale = float(np.sqrt(np.mean(reference.astype(np.float64) ** 2)))
  return {'mae': float(np.mean(np.abs(difference))), 'max_abs': float(np.max(np.abs(difference))),
          'relative_rms': float(np.sqrt(np.mean(difference ** 2)) / scale) if scale > 1e-12 else None,
          'outside_atol_0p01_rtol_0p01': int(np.sum(np.abs(difference) > .01 + .01 * np.abs(reference)))}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--reference', type=Path, required=True)
  parser.add_argument('--derivative', type=Path, required=True)
  parser.add_argument('--road', type=Path, required=True)
  parser.add_argument('--output', type=Path, required=True)
  parser.add_argument('--frames', type=int, default=500)
  parser.add_argument('--compare-frames', type=int, default=10)
  args = parser.parse_args()
  if args.output.exists():
    parser.error('choose a fresh output directory')
  manifest = json.loads((args.road / 'manifest.json').read_text())
  if not 1 <= args.frames <= len(manifest['records']):
    parser.error('insufficient unique road inputs')
  if not min(10, args.frames) <= args.compare_frames <= args.frames:
    parser.error('compare-frames must cover at least min(10, frames) and no greater than frames')
  validate_road_manifest(manifest, args.frames)
  verify_graphs(args.reference, args.derivative)
  reference = ort.InferenceSession(str(args.reference), sess_options=options(), providers=['CPUExecutionProvider'])
  derivative = ort.InferenceSession(str(args.derivative), sess_options=options(), providers=['CPUExecutionProvider'])
  states = initial_states(reference)
  args.output.mkdir(parents=True)
  expected_outputs = ['q8b_' + name for name in HEADS]
  if [item.name for item in derivative.get_outputs()] != expected_outputs:
    raise ValueError('derivative head order changed')
  compare_indices = set(np.linspace(0, args.frames - 1, args.compare_frames, dtype=int))
  lines, comparisons, native_inputs = [], [], []
  started = time.monotonic()
  for index, record in enumerate(manifest['records'][:args.frames]):
    road_path = (args.road / record['file']).resolve()
    if not road_path.is_relative_to(args.road.resolve()) or digest(road_path) != record['sha256']:
      raise ValueError('road input file changed or outside dataset')
    with np.load(road_path) as raw:
      inputs = {name: raw[name].copy() for name in raw.files}
    if hashlib.sha256(inputs['new_img'].tobytes()).hexdigest() != record['image_sha256']:
      raise ValueError('image digest disagrees with road manifest')
    feeds = inputs | states
    names = [item.name for item in reference.get_outputs()]
    result = dict(zip(names, reference.run(names, feeds), strict=True))
    if not all(np.isfinite(v).all() for v in result.values()):
      raise ValueError(f'nonfinite floating reference frame {index}')
    dfeeds = {item.name: feeds[item.name] if item.name != 'updated_state_img_q'
              else result['next_state_img_q'].astype(np.float32) for item in derivative.get_inputs()}
    if index in compare_indices:
      outputs = derivative.run(None, dfeeds)
      packed = np.concatenate(outputs, axis=1)
      head_stats, offset = {}, 0
      for item, output in zip(derivative.get_outputs(), outputs, strict=True):
        size = output.shape[1]
        head_stats[item.name] = errors(result['outputs'][:, offset:offset + size], output)
        offset += size
      comparisons.append({'index': index, 'packed': errors(result['outputs'], packed), 'heads': head_stats})
      print(f'compatibility frame {index}: {comparisons[-1]["packed"]}', flush=True)
    folder = args.output / f'{index:06d}'
    folder.mkdir()
    entries = []
    for name, value in dfeeds.items():
      target = folder / (name + '.raw')
      np.ascontiguousarray(value).tofile(target)
      native_inputs.append({'file': str(target.relative_to(args.output)), 'sha256': digest(target)})
      entries.append(f'{name}:={target.resolve()}')
    lines.append(' '.join(entries))
    states = {name: result['next_' + name] for name in states}
    if index % 25 == 0:
      print(f'fresh reference {index + 1}/{args.frames}', flush=True)
  (args.output / 'input_list.txt').write_text('\n'.join(lines) + '\n')
  if any(row['packed']['outside_atol_0p01_rtol_0p01'] for row in comparisons):
    raise ValueError('FP32 derivative compatibility diagnostic failed; quantization blocked')
  (args.output / 'reference-report.json').write_text(json.dumps({'reference_sha256': REFERENCE_SHA, 'derivative_sha256': DERIVATIVE_SHA,
    'input_list_sha256': digest(args.output / 'input_list.txt'), 'native_inputs': native_inputs,
    'frames': args.frames, 'elapsed_s': time.monotonic() - started,
    'road_manifest': str(args.road / 'manifest.json'), 'state_policy': ('Fresh zero initialization once, then this FP16 release own state outputs; ' +
                     'no historical model states.'),
    'comparisons': comparisons, 'limits': ('FP32 derivative comparison diagnostics, not INT8 accuracy or driving quality. ' +
               'Calibration only; held-out evaluation must reset independently and use disjoint frames.')}, indent=2) + '\n')


if __name__ == '__main__':
  main()
