"""Live Q8B camera in Sunnypilot's onroad UI, without vehicle/model processes."""
import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import uuid


def preview_environment(state_dir: Path, prefix: str) -> dict[str, str]:
  env = os.environ.copy()
  env.update(OPENPILOT_PREFIX=prefix, PARAMS_ROOT=str(state_dir / 'params'),
             USE_WEBCAM='1', Q8B_ROAD_ONLY='1', BIG='1', SUNNYPILOT_UI='1', FPS='30', RECORD='0')
  return env


def stop_children(children):
  for child in reversed(children):
    if child.poll() is None:
      child.terminate()
  for child in reversed(children):
    try:
      child.wait(timeout=8)
    except subprocess.TimeoutExpired:
      child.kill()
      child.wait()


def run_ui(args):
  if not os.getenv('OPENPILOT_PREFIX', '').startswith('q8b_preview_') or not os.getenv('PARAMS_ROOT'):
    raise ValueError('UI preview requires isolated messaging and parameters')

  import pyray as rl
  from opendbc.car.structs import car
  from openpilot.cereal import messaging
  from openpilot.common.hardware import HARDWARE
  from openpilot.common.params import Params
  from openpilot.system.ui.lib.application import gui_app
  from openpilot.selfdrive.ui.onroad.augmented_road_view import AugmentedRoadView
  from openpilot.selfdrive.ui.ui_state import ui_state

  # UI demonstration state only, in an isolated namespace. No car interface runs.
  cp = car.CarParams(brand='mock', passive=True, wheelbase=1, steerRatio=10)
  Params().put('CarParams', cp.to_bytes(), block=True)
  pm = messaging.PubMaster(['deviceState', 'pandaStates'])
  device = messaging.new_message('deviceState')
  device.deviceState.started = True
  device.deviceState.deviceType = HARDWARE.get_device_type()
  panda = messaging.new_message('pandaStates', 1)
  panda.pandaStates[0].pandaType = 'uno'
  panda.pandaStates[0].ignitionLine = True

  gui_app.init_window('Sunnypilot — Q8B camera preview')
  signal.signal(signal.SIGTERM, lambda _sig, _frame: gui_app.request_close())
  signal.signal(signal.SIGINT, lambda _sig, _frame: gui_app.request_close())
  view = AugmentedRoadView()
  gui_app.push_widget(view)
  start = time.monotonic()
  last_publish = 0.0
  frame_count = 0
  first_frame = last_frame = None
  screenshot_saved = False
  benchmark = None
  original_end_drawing = rl.end_drawing
  benchmark_result = None
  if args.benchmark:
    from openpilot.system.camerad.webcam.benchmark import CameraUiBenchmark, graphics_metadata, timed_end_drawing
    metadata = {**graphics_metadata(rl), 'ui_target_fps': gui_app.target_fps, 'capture_fps': 60, 'publication_fps': 20}
    benchmark = CameraUiBenchmark(time.monotonic_ns(), args.warmup_seconds)
    rl.end_drawing = timed_end_drawing(original_end_drawing, view, benchmark)
  try:
    for should_render, _frame_time, _cpu_time in gui_app.render():
      now = time.monotonic()
      if now - last_publish >= .1:
        pm.send('deviceState', device)
        pm.send('pandaStates', panda)
        device.clear_write_flag()
        panda.clear_write_flag()
        last_publish = now
      ui_state.update()
      if should_render and view.frame is not None:
        frame_id = view.client.frame_id
        if frame_id != last_frame:
          frame_count += 1
          if first_frame is None:
            first_frame = frame_id
          last_frame = frame_id
        if args.screenshot and frame_count >= 40 and not screenshot_saved:
          target = Path(args.screenshot).resolve()
          target.parent.mkdir(parents=True, exist_ok=True)
          rl.take_screenshot(os.path.relpath(target))
          screenshot_saved = target.is_file()
          if not screenshot_saved:
            raise RuntimeError(f'Failed to save screenshot to {target}')
      if args.seconds and now - start >= args.seconds:
        gui_app.request_close()
  finally:
    rl.end_drawing = original_end_drawing
    if benchmark is not None:
      benchmark_result = benchmark.write(args.log_dir, time.monotonic() - start, args.seconds, metadata)
    result = {'unique_camera_frames': frame_count, 'first_frame': first_frame,
              'last_frame': last_frame, 'screenshot_saved': screenshot_saved,
              'seconds': time.monotonic() - start, 'model_processes_started': False, 'vehicle_processes_started': False}
    (args.log_dir / 'ui-result.json').write_text(json.dumps(result, indent=2) + '\n')
    view.close()
  if not frame_count:
    raise RuntimeError('No camera frames were rendered; inspect camera.log and ui.log')
  if benchmark_result is not None and benchmark_result['status'] != 'complete':
    raise RuntimeError('Camera-to-UI benchmark ended before sufficient steady measurements')


def run_preview(args):
  prefix = 'q8b_preview_' + uuid.uuid4().hex[:12]
  args.log_dir.mkdir(parents=True, exist_ok=True)
  children = []
  stop_requested = False

  def interrupted(_sig, _frame):
    nonlocal stop_requested
    stop_requested = True

  signal.signal(signal.SIGINT, interrupted)
  signal.signal(signal.SIGTERM, interrupted)
  with tempfile.TemporaryDirectory(prefix=prefix + '_') as state:
    env = preview_environment(Path(state), prefix)
    shm = Path('/dev/shm') / ('msgq_' + prefix)
    shm.mkdir()
    try:
      with (args.log_dir / 'camera.log').open('w') as camera_log, (args.log_dir / 'ui.log').open('w') as ui_log:
        commands = [[sys.executable, '-m', 'openpilot.system.camerad.webcam.camerad'],
                    [sys.executable, '-m', __spec__.name, '--ui-child', '--log-dir', str(args.log_dir), '--seconds', str(args.seconds)]]
        if args.screenshot:
          commands[1] += ['--screenshot', args.screenshot]
        if args.benchmark:
          commands[1] += ['--benchmark', '--warmup-seconds', str(args.warmup_seconds)]
        for command, log in zip(commands, [camera_log, ui_log], strict=True):
          children.append(subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT))
        (args.log_dir / 'processes.json').write_text(json.dumps({'prefix': prefix, 'pids': [c.pid for c in children],
                                                               'commands': commands}, indent=2) + '\n')
        print(f'Starting Sunnypilot camera preview. Close its window or press Ctrl+C. Logs: {args.log_dir}', flush=True)
        while not stop_requested and children[1].poll() is None:
          if children[0].poll() is not None:
            raise RuntimeError(f'Camera stopped; inspect {args.log_dir / "camera.log"}')
          time.sleep(.1)
        if children[1].returncode:
          raise RuntimeError(f'UI stopped with exit {children[1].returncode}; inspect {args.log_dir / "ui.log"}')
    except KeyboardInterrupt:
      pass
    finally:
      stop_children(children)
      (args.log_dir / 'session-result.json').write_text(json.dumps(
        {'prefix': prefix, 'child_exit_codes': [child.returncode for child in children]}, indent=2) + '\n')
      # Only remove this session's files, after its processes release them.
      import shutil
      shutil.rmtree(shm)
      socket = Path('/tmp') / (prefix + '_visionipc_camerad')
      if socket.exists():
        socket.unlink()


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--log-dir', type=Path, default=Path('/tmp') / ('q8b-camera-view-' + time.strftime('%Y%m%d-%H%M%S')))
  parser.add_argument('--seconds', type=float, default=0, help='Close automatically after this many seconds; zero keeps window open')
  parser.add_argument('--screenshot', help='Save a screenshot after 40 distinct camera frames')
  parser.add_argument('--benchmark', action='store_true', help='Record per-frame capture-to-UI timing; default run is 65 seconds')
  parser.add_argument('--warmup-seconds', type=float, default=5, help='Exclude this initial interval from benchmark statistics')
  parser.add_argument('--ui-child', action='store_true', help=argparse.SUPPRESS)
  args = parser.parse_args()
  if not math.isfinite(args.seconds) or args.seconds < 0 or not math.isfinite(args.warmup_seconds) or args.warmup_seconds < 0:
    parser.error('Duration and warmup must be finite and nonnegative')
  if args.benchmark:
    if args.seconds == 0:
      args.seconds = 65
    if args.seconds <= args.warmup_seconds:
      parser.error('Benchmark duration must exceed warmup')
  from openpilot.common.platform import RADXA_Q8B
  if not RADXA_Q8B:
    parser.error('This preview is for the Radxa Dragon Q8B')
  if args.ui_child:
    run_ui(args)
  else:
    run_preview(args)


if __name__ == '__main__':
  main()
