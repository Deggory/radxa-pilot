"""Isolated Q8B camera UI, with optional Thneed predictions and no vehicle processes."""
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
from contextlib import ExitStack


def preview_environment(state_dir: Path, prefix: str, *, model: bool = False) -> dict[str, str]:
  env = os.environ.copy()
  env.update(OPENPILOT_PREFIX=prefix, PARAMS_ROOT=str(state_dir / 'params'),
             USE_WEBCAM='1', Q8B_ROAD_ONLY='1', BIG='1', SUNNYPILOT_UI='1', FPS='30', RECORD='0')
  env.pop('Q8B_THNEED', None)
  if model:
    env.update(Q8B_THNEED='1', DEBUG='0', DEV='CPU:LLVM')
  return env


def preview_commands(args):
  ui = [sys.executable, '-m', __spec__.name, '--ui-child', '--log-dir', str(args.log_dir), '--seconds', str(args.seconds)]
  commands = [[sys.executable, '-m', 'openpilot.system.camerad.webcam.camerad']]
  names = ['camera']
  if args.model:
    commands.append([sys.executable, '-m', 'openpilot.selfdrive.modeld.modeld', '--demo'])
    names.append('model')
    ui += ['--model']
  if args.screenshot:
    ui += ['--screenshot', args.screenshot]
  if args.benchmark:
    ui += ['--benchmark', '--warmup-seconds', str(args.warmup_seconds)]
  return commands + [ui], names + ['ui']


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
  pm = messaging.PubMaster(['deviceState', 'pandaStates'] + (['extrinsicsCalibration'] if args.model else []))
  device = messaging.new_message('deviceState')
  device.deviceState.started = True
  device.deviceState.deviceType = HARDWARE.get_device_type()
  panda = messaging.new_message('pandaStates', 1)
  panda.pandaStates[0].pandaType = 'uno'
  panda.pandaStates[0].ignitionLine = True
  calibration = None
  if args.model:
    calibration = messaging.new_message('extrinsicsCalibration')
    calibration.valid = False
    calibration.extrinsicsCalibration.calStatus = 'uncalibrated'
    calibration.extrinsicsCalibration.rpyCalib = [0., 0., 0.]

  gui_app.init_window('Sunnypilot — Q8B Thneed preview (uncalibrated)' if args.model else 'Sunnypilot — Q8B camera preview')
  signal.signal(signal.SIGTERM, lambda _sig, _frame: gui_app.request_close())
  signal.signal(signal.SIGINT, lambda _sig, _frame: gui_app.request_close())
  view = AugmentedRoadView()
  gui_app.push_widget(view)
  start = time.monotonic()
  last_publish = 0.0
  frame_count = 0
  first_frame = last_frame = None
  model_rows = []
  last_model_frame = None
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
        if calibration is not None:
          pm.send('extrinsicsCalibration', calibration)
          calibration.clear_write_flag()
        last_publish = now
      ui_state.update()
      if args.model and ui_state.sm.updated['modelV2']:
        md = ui_state.sm['modelV2']
        if md.frameId != last_model_frame:
          points = list(md.position.x) + list(md.position.y) + list(md.position.z)
          if len(points) != 99 or not all(math.isfinite(value) for value in points):
            raise RuntimeError('Model published an invalid path')
          model_rows.append({'frame_id': md.frameId, 'timestamp_eof': md.timestampEof,
                             'receipt_ns': time.monotonic_ns(), 'execution_ms': md.modelExecutionTime * 1000,
                             'valid': ui_state.sm.valid['modelV2'], 'path_points': len(md.position.x),
                             'path_render_points': len(view.model_renderer._path.raw_points)})
          last_model_frame = md.frameId
      if should_render and view.frame is not None:
        frame_id = view.client.frame_id
        if frame_id != last_frame:
          frame_count += 1
          if first_frame is None:
            first_frame = frame_id
          last_frame = frame_id
        model_ready = not args.model or (len(model_rows) >= 20 and len(view.model_renderer._path.raw_points) > 0)
        if args.screenshot and frame_count >= 40 and model_ready and not screenshot_saved:
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
              'seconds': time.monotonic() - start, 'model_processes_started': args.model, 'vehicle_processes_started': False,
              'model_messages': len(model_rows), 'model_path_render_points': len(view.model_renderer._path.raw_points)}
    if view.q8b_stats is not None:
      result['q8b_stats'] = view.q8b_stats.diagnostics()
    if args.model:
      (args.log_dir / 'model-received.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in model_rows))
    (args.log_dir / 'ui-result.json').write_text(json.dumps(result, indent=2) + '\n')
    view.close()
  if not frame_count:
    raise RuntimeError('No camera frames were rendered; inspect camera.log and ui.log')
  if args.model and (len(model_rows) < 20 or result['model_path_render_points'] == 0):
    raise RuntimeError('Insufficient model predictions/overlay; inspect model.log and ui.log')
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
    env = preview_environment(Path(state), prefix, model=args.model)
    env.pop('Q8B_THNEED_SNAPSHOT_DIR', None)
    env.pop('Q8B_MODEL_TIMINGS', None)
    if args.model and args.benchmark:
      env['Q8B_MODEL_TIMINGS'] = str(args.log_dir.resolve() / 'model-timings.jsonl')
    if args.model_checks:
      env['Q8B_GPU_PREP'] = '0'
      env['Q8B_THNEED_SNAPSHOT_DIR'] = str(args.log_dir.resolve() / 'model-inputs')
      print('Model snapshots use the CPU-preparation reference path; this is not a production latency test.', flush=True)
    shm = Path('/dev/shm') / ('msgq_' + prefix)
    shm.mkdir()
    try:
      with ExitStack() as stack:
        commands, names = preview_commands(args)
        logs = [stack.enter_context((args.log_dir / f'{name}.log').open('w')) for name in names]
        for command, log in zip(commands, logs, strict=True):
          children.append(subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT))
        (args.log_dir / 'processes.json').write_text(json.dumps({'prefix': prefix, 'pids': [c.pid for c in children],
                                                               'commands': commands, 'names': names}, indent=2) + '\n')
        print(f'Starting Sunnypilot camera preview. Close its window or press Ctrl+C. Logs: {args.log_dir}', flush=True)
        while not stop_requested and children[-1].poll() is None:
          for child, name in zip(children[:-1], names[:-1], strict=True):
            if child.poll() is not None:
              raise RuntimeError(f'{name} stopped; inspect {args.log_dir / (name + ".log")}')
          time.sleep(.1)
        if children[-1].returncode:
          raise RuntimeError(f'UI stopped with exit {children[-1].returncode}; inspect {args.log_dir / "ui.log"}')
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
  parser.add_argument('--model', action='store_true', help='Add isolated stock modeld using the existing Q8B Thneed model; no vehicle controls')
  parser.add_argument('--model-checks', action='store_true',
                      help='Use CPU preparation and save six reference samples; requires --model, excludes latency qualification')
  parser.add_argument('--warmup-seconds', type=float, default=5, help='Exclude this initial interval from benchmark statistics')
  parser.add_argument('--ui-child', action='store_true', help=argparse.SUPPRESS)
  args = parser.parse_args()
  if args.model_checks and not args.model:
    parser.error('--model-checks requires --model')
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
