"""Pinned conversion provenance and continuous road-sequence checks."""
import json
from pathlib import Path

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest

REFERENCE_SHA = 'da9506a64143b0bfd535db8901671170e385451c9f68790f29ebf1114f457b38'
DERIVATIVE_SHA = 'eceadb809ada5462481cb343e643850e45c72cc4fdf55db0deb74b5718b9411d'


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


def verify_calibration(input_list):
  input_list = Path(input_list).resolve()
  report = json.loads((input_list.parent / 'reference-report.json').read_text())
  if report.get('reference_sha256') != REFERENCE_SHA or report.get('derivative_sha256') != DERIVATIVE_SHA:
    raise ValueError('calibration model identity is unverified')
  comparisons = report.get('comparisons', [])
  if (len(comparisons) < min(10, report['frames']) or
      (report['frames'] > 128 and not any(r['index'] >= 128 for r in comparisons)) or
      any(r['packed']['outside_atol_0p01_rtol_0p01'] for r in comparisons)):
    raise ValueError('floating compatibility diagnostics missing or failed')
  if digest(input_list) != report.get('input_list_sha256'):
    raise ValueError('calibration input list changed')
  if len(input_list.read_text().splitlines()) != report['frames']:
    raise ValueError('calibration frame count changed')
  for entry in report['native_inputs']:
    path = (input_list.parent / entry['file']).resolve()
    if not path.is_relative_to(input_list.parent) or digest(path) != entry['sha256']:
      raise ValueError('native calibration file changed or outside dataset')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('mode', choices=['record-float', 'verify-float', 'verify-calibration'])
  parser.add_argument('path', type=Path)
  args = parser.parse_args()
  if args.mode == 'verify-calibration':
    verify_calibration(args.path)
  else:
    float_receipt(args.path, create=args.mode == 'record-float')
