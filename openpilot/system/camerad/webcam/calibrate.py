"""Printable target, guided image collection and offline lens-calibration candidate.

No result is installed into DEVICE_CAMERAS. Intrinsics/distortion and mounted
camera orientation are separate measurements. See CALIBRATION.md.
"""
import argparse
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import signal
import subprocess

import cv2 as cv
import numpy as np

from openpilot.system.camerad.webcam.config import ROAD_WIDTH, ROAD_HEIGHT, RADXA_Q8B, road_camera_device, rotate_180

PATTERN = (9, 6)
MIN_VIEWS = 12


def write_target(directory: Path) -> tuple[Path, Path]:
  """A4 landscape, 10x7 squares of25mm =9x6 internal corners; vector PDF/SVG."""
  directory.mkdir(parents=True, exist_ok=True)
  svg, pdf = directory / 'ak-checkerboard-a4.svg', directory / 'ak-checkerboard-a4.pdf'
  if svg.exists() or pdf.exists():
    raise FileExistsError('Target exists; refusing to overwrite')
  rects = [(23.5 + x * 25, 15 + y * 25) for y in range(7) for x in range(10) if (x + y) % 2 == 0]
  label = 'AK-Camera: 9 x 6 inner corners; 25 mm squares; print at 100% / actual size'
  body = ''.join(f'<rect class="square" x="{x}" y="{y}" width="25" height="25"/>' for x, y in rects)
  svg.write_text(''.join(('<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210">',
                         '<rect width="297" height="210" fill="white"/>',
                         f'<text x="148.5" y="9" text-anchor="middle" font-size="3.2">{label}</text>',
                         f'<g fill="black">{body}</g>',
                         '<text x="148.5" y="198" text-anchor="middle" font-size="3">Measure square =25mm; ruler below =100mm</text>',
                         '<path d="M98.5 203v4m0-2h100m0-2v4" fill="none" stroke="black" stroke-width="0.3"/></svg>\n')))
  mm = 72 / 25.4
  drawing = ['1 1 1 rg 0 0 842 596 re f', '0 0 0 rg']
  drawing += [f'{x * mm:.6f} {(210 - y - 25) * mm:.6f} {25 * mm:.6f} {25 * mm:.6f} re f' for x, y in rects]
  drawing += [f'BT /F1 9 Tf 68 {201 * mm:.6f} Td ({label}) Tj ET',
              'BT /F1 9 Tf 170 34 Td (Measure square =25mm; ruler below =100mm) Tj ET',
              f'0 G 0.8 w {98.5 * mm:.6f} {5 * mm:.6f} m {198.5 * mm:.6f} {5 * mm:.6f} l S']
  stream = '\n'.join(drawing).encode('ascii')
  objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
             f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {297 * mm:.6f} {210 * mm:.6f}] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>'.encode(),
             f'<< /Length {len(stream)} >>\nstream\n'.encode() + stream + b'\nendstream',
             b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
  data = bytearray(b'%PDF-1.4\n')
  offsets = [0]
  for i, obj in enumerate(objects, 1):
    offsets.append(len(data))
    data.extend(f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n')
  xref = len(data)
  data.extend(b'xref\n0 6\n0000000000 65535 f \n')
  for offset in offsets[1:]:
    data.extend(f'{offset:010d} 00000 n \n'.encode())
  data.extend(f'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
  pdf.write_bytes(data)
  return svg, pdf


def object_points(square_mm: float) -> np.ndarray:
  if not np.isfinite(square_mm) or square_mm <= 0:
    raise ValueError('Square size must be a positive measured millimetre value')
  points = np.zeros((PATTERN[0] * PATTERN[1], 3), dtype=np.float32)
  points[:, :2] = np.mgrid[:PATTERN[0], :PATTERN[1]].T.reshape(-1, 2) * square_mm
  return points


def detect(image):
  found, corners = cv.findChessboardCornersSB(cv.cvtColor(image, cv.COLOR_BGR2GRAY), PATTERN, cv.CALIB_CB_NORMALIZE_IMAGE)
  return corners if found else None


def solve(views: list[np.ndarray], image_size: tuple[int, int], square_mm: float) -> dict:
  obj = object_points(square_mm)
  if image_size != (ROAD_WIDTH, ROAD_HEIGHT) or len(views) < MIN_VIEWS:
    raise ValueError('Need at least 12 full 720p views for the AK capture mode')
  if any(v.shape != (54, 1, 2) or not np.isfinite(v).all() for v in views):
    raise ValueError('Each view must contain 54 finite internal corners')
  centers = np.array([v.mean(axis=(0, 1)) for v in views])
  spread = np.ptp(centers, axis=0) / image_size
  if np.any(spread < .15):
    raise ValueError('Insufficient view diversity: move target across both image axes and tilt it')
  rms, k, distortion, _rvecs, _tvecs, stddev, _extrinsic_stddev, errors = cv.calibrateCameraExtended(
    [obj.copy() for _ in views], views, image_size, None, None)
  if not np.isfinite(rms) or not np.isfinite(k).all() or not np.isfinite(distortion).all() or not np.isfinite(errors).all() or not np.isfinite(stddev).all():
    raise ValueError('Calibration produced non-finite parameters')
  if k[0, 0] <= 0 or k[1, 1] <= 0 or not 0 < k[0, 2] < image_size[0] or not 0 < k[1, 2] < image_size[1]:
    raise ValueError('Calibration produced implausible focal length/principal point')
  if rms > 1.0 or errors.max() > 1.5:
    raise ValueError(f'Reprojection error too high: RMS={rms:.3f}px, worst={errors.max():.3f}px; recollect images')
  return {'version': 1, 'status': 'candidate_not_installed', 'lens_model': 'opencv_pinhole_5_coefficients',
          'image_size': list(image_size), 'pattern_inner_corners': list(PATTERN), 'square_mm': square_mm,
          'views': len(views), 'camera_matrix': k.tolist(), 'distortion_coefficients': distortion.ravel().tolist(),
          'rms_px': rms, 'per_view_rms_px': errors.ravel().tolist(), 'intrinsics_stddev': stddev.ravel().tolist(),
          'center_coverage_fraction': spread.tolist(), 'optical_state_review_required': True,
          'mounted_orientation_calibrated': False}


def solve_directory(directory: Path, output: Path, square_mm: float):
  if output.exists():
    raise FileExistsError(output)
  manifest = json.loads((directory / 'manifest.json').read_text())
  if manifest.get('error'):
    raise ValueError('Capture ended with an error; review/recollect before solving')
  profile = manifest['profile']
  if (profile.get('width'), profile.get('height'), profile.get('format'), profile.get('capture_fps')) != (1280, 720, 'MJPG', 60):
    raise ValueError('Capture manifest does not describe the expected 720p MJPG 60 profile')
  views, inputs = [], []
  for record in manifest['images']:
    if Path(record['file']).name != record['file']:
      raise ValueError('Image path must stay inside the capture directory')
    path = directory / record['file']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != record['sha256']:
      raise ValueError(f'Image hash changed: {path.name}')
    image = cv.imread(str(path))
    if image is None or image.shape != (ROAD_HEIGHT, ROAD_WIDTH, 3):
      raise ValueError(f'Image is not full720p: {path}')
    corners = detect(image)
    if corners is None:
      raise ValueError(f'Checkerboard not detected: {path}')
    views.append(corners)
    inputs.append({'file': path.name, 'sha256': digest})
  result = solve(views, (ROAD_WIDTH, ROAD_HEIGHT), square_mm)
  result.update(capture_profile=manifest['profile'], input_images=inputs,
                created_utc=datetime.now(UTC).isoformat())
  with output.open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
  return result


def capture(directory: Path, samples: int):
  # Standard Tk works with headless OpenCV wheels; Pillow is a preview dependency.
  import tkinter as tk
  from PIL import Image, ImageTk
  from openpilot.system.camerad.webcam.native_capture import LatestCapture, NativeCapture
  if not RADXA_Q8B:
    raise ValueError('Live collection requires the detected Q8B board')
  if not MIN_VIEWS <= samples <= 100:
    raise ValueError('Choose 12..100 samples (24 recommended)')
  directory.mkdir(parents=True, exist_ok=False)
  device, rotation = road_camera_device(), rotate_180()
  controls = subprocess.check_output(['v4l2-ctl', '-d', device,
                                     '--get-ctrl=focus_automatic_continuous,focus_absolute,exposure_dynamic_framerate'], text=True)
  root = tk.Tk()
  root.title('AK-Camera lens calibration — Space saves; Escape finishes')
  if 'focus_automatic_continuous: 1' in controls:
    tk.Label(root, text='Autofocus is ON: results stay provisional; fixed-focus operation needs review', fg='darkred').pack()
  status = tk.StringVar(value='Show whole target, move and tilt it; Space saves a distinct view')
  tk.Label(root, textvariable=status).pack()
  panel = tk.Label(root)
  panel.pack()
  tk.Button(root, text='Save view (Space)', command=lambda: save()).pack(side='left')
  tk.Button(root, text='Finish (Escape)', command=root.destroy).pack(side='right')
  collected, corners_saved, failed = [], [], []
  current = {}
  source = None

  def save_frame():
    if current.get('corners') is None:
      status.set('No complete 9x6 grid found; show the whole target')
      return
    corners = current['corners']
    if any(np.sqrt(np.mean((corners - old) ** 2)) < 10 for old in corners_saved):
      status.set('View too similar; move/tilt target before saving')
      return
    name = f'frame-{len(collected):03d}.jpg'
    encoded = current['raw'].payload if not rotation else cv.imencode('.jpg', current['image'], [cv.IMWRITE_JPEG_QUALITY, 98])[1].tobytes()
    (directory / name).write_bytes(encoded)
    collected.append({'file': name, 'sha256': hashlib.sha256(encoded).hexdigest(),
                      'timestamp_ns': current['raw'].timestamp_ns, 'source_sequence': current['raw'].sequence})
    corners_saved.append(corners.copy())
    status.set(f'Saved {len(collected)}/{samples}; vary position/distance/tilt, keep whole board visible')
    if len(collected) >= samples:
      root.destroy()

  def save():
    try:
      save_frame()
    except Exception as error:
      failed.append(error)
      root.destroy()

  def tick():
    try:
      raw = source.read()
      image = cv.imdecode(np.frombuffer(raw.payload, dtype=np.uint8), cv.IMREAD_COLOR)
      if image is None or image.shape != (ROAD_HEIGHT, ROAD_WIDTH, 3):
        raise ValueError('Invalid 720p JPEG from camera')
      if rotation:
        image = cv.flip(image, -1)
      corners = detect(image)
      current.update(raw=raw, image=image, corners=corners)
      annotated = image.copy()
      if corners is not None:
        cv.drawChessboardCorners(annotated, PATTERN, corners, True)
      preview = cv.resize(cv.cvtColor(annotated, cv.COLOR_BGR2RGB), (960, 540))
      panel.image = ImageTk.PhotoImage(Image.fromarray(preview))
      panel.configure(image=panel.image)
      root.after(100, tick)
    except Exception as error:
      failed.append(error)
      root.destroy()

  root.bind('<space>', lambda _event: save())
  root.bind('<Escape>', lambda _event: root.destroy())
  previous_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}
  def interrupt(_signum, _frame):
    root.after_idle(root.destroy)
  for sig in previous_handlers:
    signal.signal(sig, interrupt)
  try:
    source = LatestCapture(NativeCapture(device))
    root.after(0, tick)
    root.mainloop()
  finally:
    for sig, handler in previous_handlers.items():
      signal.signal(sig, handler)
    try:
      root.destroy()
    except tk.TclError:
      pass  # Window already closed by Finish/Escape/signal.
    try:
      if source is not None:
        source.close()
    finally:
      profile = {'device': device, 'width': ROAD_WIDTH, 'height': ROAD_HEIGHT, 'format': 'MJPG',
                 'capture_fps': 60, 'rotate_180': rotation, 'controls_before': controls}
      manifest = {'profile': profile, 'images': collected, 'requested_samples': samples,
                  'created_utc': datetime.now(UTC).isoformat(), 'error': str(failed[0]) if failed else None}
      (directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
  if failed:
    raise RuntimeError('Camera collection stopped; partial images/manifest preserved') from failed[0]
  print(f'Saved {len(collected)} view(s) in {directory}; solve separately after checking print scale and focus state')


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  commands = parser.add_subparsers(dest='command', required=True)
  target = commands.add_parser('target')
  target.add_argument('--directory', type=Path, required=True)
  collect = commands.add_parser('capture')
  collect.add_argument('--directory', type=Path, required=True)
  collect.add_argument('--samples', type=int, default=24)
  solver = commands.add_parser('solve')
  solver.add_argument('--directory', type=Path, required=True)
  solver.add_argument('--output', type=Path, required=True)
  solver.add_argument('--square-mm', type=float, required=True, help='Measured printed square side, millimetres')
  args = parser.parse_args()
  if args.command == 'target':
    print(*write_target(args.directory), sep='\n')
  elif args.command == 'capture':
    capture(args.directory, args.samples)
  else:
    result = solve_directory(args.directory, args.output, args.square_mm)
    print(f'Candidate saved to {args.output}; RMS={result["rms_px"]:.3f}px; not installed')


if __name__ == '__main__':
  main()
