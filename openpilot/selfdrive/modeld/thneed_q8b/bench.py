"""Private camera/model-only baseline; no display, manager or vehicle processes."""
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid

import numpy as np

from openpilot.system.camerad.webcam.preview import preview_environment, stop_children


def summarize(rows, warmup_seconds):
  if not rows:
    raise RuntimeError('No model timing records')
  if any(b['frame_id'] <= a['frame_id'] or b['capture_ns'] <= a['capture_ns'] or b['output_ns'] <= a['output_ns']
         for a, b in zip(rows, rows[1:], strict=False)):
    raise RuntimeError('Model frame/timestamp order is invalid')
  steady = [r for r in rows if r['output_ns'] >= rows[0]['output_ns'] + warmup_seconds * 1e9]
  if len(steady) < 20:
    raise RuntimeError('Insufficient steady camera/model samples')
  def stats(values):
    return dict(zip(('median', 'p95', 'p99', 'max'), [*np.percentile(values, [50, 95, 99]).tolist(), max(values)], strict=True))
  rate = (len(steady) - 1) * 1e9 / (steady[-1]['output_ns'] - steady[0]['output_ns'])
  clocks = {r['stages']['performance']['received_ns']: r['stages']['performance'] for r in steady}
  return {'samples': len(steady), 'output_hz': rate,
          'camera_to_output_ms': stats([r['camera_to_output_ms'] for r in steady]),
          'full_model_call_ms': stats([r['full_model_call_ms'] for r in steady]),
          'stages_ms': {key: stats([r['stages'][key] for r in steady])
                        for key in ('cpu_prepare_ms', 'input_validation_ms', 'upload_ms', 'inference_readback_ms')},
          'clock_samples': list(clocks.values()),
          'all_clock_samples_at_tested_max': all(c['gpu_hz'] == 690000000 and
                                                  sorted(c['cpu_khz'].values()) == [2438400, 2995200] for c in clocks.values()),
          'timestamp_endpoint': 'V4L2 monotonic source timestamp to model.run return; excludes UI receipt and drawing'}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--log-dir', type=Path, required=True)
  parser.add_argument('--seconds', type=float, default=65)
  parser.add_argument('--warmup-seconds', type=float, default=5)
  args = parser.parse_args()
  if not 0 <= args.warmup_seconds < args.seconds or args.seconds < 10:
    parser.error('Require at least 10 seconds and a shorter nonnegative warmup')
  args.log_dir.mkdir(parents=True, exist_ok=False)
  prefix = 'q8b_preview_' + uuid.uuid4().hex[:12]
  children = []
  stopped = False
  def interrupted(_signum, _frame):
    nonlocal stopped
    stopped = True
  signal.signal(signal.SIGTERM, interrupted)
  signal.signal(signal.SIGINT, interrupted)
  with tempfile.TemporaryDirectory(prefix=prefix) as state, ExitStack() as stack:
    env = preview_environment(Path(state), prefix, model=True)
    env.pop('Q8B_THNEED_SNAPSHOT_DIR', None)
    env['Q8B_MODEL_TIMINGS'] = str(args.log_dir.resolve() / 'model-timings.jsonl')
    shm = Path('/dev/shm') / ('msgq_' + prefix)
    shm.mkdir()
    try:
      for name, module in [('camera', 'openpilot.system.camerad.webcam.camerad'), ('model', 'openpilot.selfdrive.modeld.modeld')]:
        log = stack.enter_context((args.log_dir / f'{name}.log').open('w'))
        command = [sys.executable, '-m', module] + (['--demo'] if name == 'model' else [])
        children.append(subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT))
      (args.log_dir / 'processes.json').write_text(json.dumps({'prefix': prefix, 'pids': [p.pid for p in children],
                                                            'names': ['camera', 'model']}, indent=2) + '\n')
      start = time.monotonic()
      while time.monotonic() - start < args.seconds and not stopped:
        for p in children:
          if p.poll() is not None:
            raise RuntimeError('Camera/model child stopped early; inspect logs')
        time.sleep(.05)
    finally:
      stop_children(children)
      shutil.rmtree(shm)
      (Path('/tmp') / (prefix + '_visionipc_camerad')).unlink(missing_ok=True)
      (args.log_dir / 'session-result.json').write_text(json.dumps({'prefix': prefix,
        'child_exit_codes': [p.returncode for p in children], 'interrupted': stopped}, indent=2) + '\n')
  if stopped or any(p.returncode for p in children):
    raise RuntimeError('Incomplete camera/model benchmark')
  rows = [json.loads(line) for line in (args.log_dir / 'model-timings.jsonl').read_text().splitlines()]
  result = summarize(rows, args.warmup_seconds)
  result['baseline_targets_met'] = (result['camera_to_output_ms']['median'] < 38 and
                                    result['stages_ms']['inference_readback_ms']['median'] <= 12 and
                                    19.5 <= result['output_hz'] <= 20.5 and result['all_clock_samples_at_tested_max'])
  (args.log_dir / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
  print(json.dumps({k: v for k, v in result.items() if k != 'clock_samples'}, indent=2))


if __name__ == '__main__':
  main()
