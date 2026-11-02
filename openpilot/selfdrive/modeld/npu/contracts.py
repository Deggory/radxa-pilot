"""Pinned conversion provenance and continuous road-sequence checks."""
import json
from pathlib import Path

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest

REFERENCE_SHA = 'da9506a64143b0bfd535db8901671170e385451c9f68790f29ebf1114f457b38'
DERIVATIVE_SHA = 'eceadb809ada5462481cb343e643850e45c72cc4fdf55db0deb74b5718b9411d'
SEMANTIC_SHA = '135d27f95df49447a8509dc0cd422e7bbf4359149a71d07c342f426fee88be3d'
HEADS = ['lane_lines', 'lane_line_probs', 'road_edges', 'meta', 'desire_pred', 'pose', 'wide_from_device_euler',
         'road_transform', 'plan', 'lead', 'lead_prob', 'desire_state', 'action', 'hidden_state', 'pad']
SIZES = [528, 8, 264, 55, 32, 12, 6, 12, 990, 144, 3, 8, 4, 16384, 2]


def validate_road_metadata(records):
  if not records or len({r['image_sha256'] for r in records}) != len(records):
    raise ValueError('road images must be nonempty and unique')
  for previous, current in zip(records[:-1], records[1:], strict=True):
    elapsed = current['capture_ns'] - previous['capture_ns']
    if current['frame_id'] != previous['frame_id'] + 1 or not 40_000_000 <= elapsed <= 60_000_000:
      raise ValueError('non-contiguous 20 Hz camera sequence; explicit reset needed')


def validate_road_manifest(manifest, frames):
  if manifest.get('format_version') != 2 or not manifest.get('video_alignment', '').startswith('frameId mapped through fullHEVC'):
    raise ValueError('requires corrected encode-index road-preparation format 2')
  records = manifest['records'][:frames]
  validate_road_metadata(records)
  for record in records:
    if not all(name in record for name in ['narrow_video_index', 'wide_video_index']):
      raise ValueError('missing encoded presentation positions')
  return records


def verify_graphs(reference, derivative):
  for path, expected in [(reference, REFERENCE_SHA), (derivative, DERIVATIVE_SHA)]:
    if digest(path) != expected:
      raise ValueError(f'wrong pinned conversion graph: {path}')


def float_receipt(work, create=False):
  work = Path(work)
  source = work / 'artifacts/graph-v1/quantization_source_fp32.onnx'
  dlc = work / 'artifacts/dlc-v1/float.dlc'
  receipt = work / 'artifacts/dlc-v1/float-receipt.json'
  actual = {'source_sha256': digest(source), 'dlc_sha256': digest(dlc), 'dlc_bytes': dlc.stat().st_size,
            'sdk': '2.37.1.250807'}
  if actual['source_sha256'] != DERIVATIVE_SHA:
    raise ValueError('wrong source for floating DLC')
  if create:
    receipt.write_text(json.dumps(actual, indent=2) + '\n')
  elif json.loads(receipt.read_text()) != actual:
    raise ValueError('floating DLC provenance changed')


def verify_calibration(input_list, research=False):
  input_list = Path(input_list).resolve()
  report = json.loads((input_list.parent / 'reference-report.json').read_text())
  if report.get('reference_sha256') != REFERENCE_SHA or report.get('derivative_sha256') != DERIVATIVE_SHA:
    raise ValueError('calibration model identity is unverified')
  comparisons = report.get('comparisons', [])
  if (len(comparisons) < min(10, report['frames']) or
      (report['frames'] > 128 and not any(r['index'] >= 128 for r in comparisons))):
    raise ValueError('floating compatibility diagnostics missing')
  failures = sum(r['packed']['outside_atol_0p01_rtol_0p01'] for r in comparisons)
  if failures and not research:
    raise ValueError('floating compatibility diagnostics failed')
  if research:
    semantic = report.get('same_precision_comparisons', [])
    if (report.get('semantic_reference_sha256') != SEMANTIC_SHA or
        report.get('reference_recurrence_verified_frames') != report['frames'] or
        [r['index'] for r in semantic] != [r['index'] for r in comparisons] or
        any(r['packed']['max_abs'] != 0 or not r['packed'].get('bitwise_equal') for r in semantic)):
      raise ValueError('research requires exact same-precision graph comparisons')
    print(f'RESEARCH ONLY: retaining {failures} failed FP16 diagnostic values; no accuracy acceptance')
  verify_native_inputs(input_list, report)


def verify_native_inputs(input_list, report):
  input_list = Path(input_list).resolve()
  if digest(input_list) != report.get('input_list_sha256'):
    raise ValueError('calibration input list changed')
  if len(input_list.read_text().splitlines()) != report['frames']:
    raise ValueError('calibration frame count changed')
  listed_paths = [Path(field.split(':=', 1)[1]).resolve() for line in input_list.read_text().splitlines() for field in line.split()]
  recorded_paths = [(input_list.parent / entry['file']).resolve() for entry in report['native_inputs']]
  if len(set(recorded_paths)) != len(recorded_paths) or set(listed_paths) != set(recorded_paths):
    raise ValueError('native calibration receipt coverage changed')
  for entry in report['native_inputs']:
    path = (input_list.parent / entry['file']).resolve()
    if not path.is_relative_to(input_list.parent) or digest(path) != entry['sha256']:
      raise ValueError('native calibration file changed or outside dataset')


def research_receipt(work, input_list, create=False):
  work, input_list = Path(work), Path(input_list)
  float_receipt(work)
  verify_calibration(input_list, research=True)
  calibration = input_list.parent / 'reference-report.json'
  report = json.loads(calibration.read_text())
  dlc = work / 'artifacts/dlc-v1/w8a8-research.dlc'
  actual = {'sdk': '2.37.1.250807', 'precision': 'W8A8/bias32', 'backend': 'generic HTP; target-specific context pending',
            'source_sha256': DERIVATIVE_SHA, 'float_receipt_sha256': digest(work / 'artifacts/dlc-v1/float-receipt.json'),
            'dlc_sha256': digest(dlc), 'dlc_bytes': dlc.stat().st_size, 'calibration_receipt_sha256': digest(calibration),
            'input_list_sha256': digest(input_list), 'frames': report['frames'],
            'retained_fp16_failure_count': sum(r['packed']['outside_atol_0p01_rtol_0p01'] for r in report['comparisons']),
            'qualification': 'unqualified research; owner permits retained FP16 diagnostic failure'}
  receipt = dlc.with_suffix('.json')
  if create:
    if receipt.exists():
      raise ValueError('existing research receipt preserved')
    receipt.write_text(json.dumps(actual, indent=2) + '\n')
  elif json.loads(receipt.read_text()) != actual:
    raise ValueError('research quantization provenance changed')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('mode', choices=['record-float', 'verify-float', 'verify-calibration', 'verify-calibration-research',
                                      'record-research', 'verify-research'])
  parser.add_argument('path', type=Path)
  parser.add_argument('--input-list', type=Path)
  args = parser.parse_args()
  if args.mode in ('record-research', 'verify-research'):
    if args.input_list is None:
      parser.error('--input-list is required for research provenance')
    research_receipt(args.path, args.input_list, create=args.mode == 'record-research')
  elif args.mode.startswith('verify-calibration'):
    verify_calibration(args.path, research=args.mode.endswith('-research'))
  else:
    float_receipt(args.path, create=args.mode == 'record-float')
