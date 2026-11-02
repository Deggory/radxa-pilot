"""Bounded GPU replay/accuracy check of the copied artifact; no model conversion."""
import argparse
import json
from pathlib import Path
import time

import numpy as np

from openpilot.selfdrive.modeld.thneed_q8b.runtime import HERE, MODEL, MODEL_SHA256, ThneedModel, verify_file


def current_inputs(legacy: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
  """Independently embed saved host histories into the newer interface's queues."""
  images = np.concatenate((legacy['img'][0, 6:], legacy['big_img'][0, 6:])).reshape(2, 6, 128, 256)
  image_queue = np.zeros((2, 5, 6, 128, 256), dtype=np.uint8)
  image_queue[0, 1], image_queue[1, 1] = legacy['img'][0, :6], legacy['big_img'][0, :6]
  desire_grouped = np.repeat(legacy['desire_pulse'][0], 4, axis=0)[:, None, :]
  return {
    'new_img': images, 'state_img_q': image_queue,
    'desire': desire_grouped[-1, 0],
    'state_desire_q': np.concatenate((np.zeros((1, 1, 8), dtype=np.float32), desire_grouped[:-1])),
    'state_feat_q': np.repeat(legacy['features_buffer'].transpose(1, 0, 2), 4, axis=0),
    'traffic_convention': legacy['traffic_convention'], 'action_t': legacy['action_t'],
  }


def policy_snapshot() -> dict[str, str]:
  paths = list(Path('/sys/devices/system/cpu/cpufreq').glob('policy*/scaling_governor'))
  gpu = Path('/sys/class/devfreq/3d00000.gpu')
  paths += [gpu / name for name in ('governor', 'min_freq', 'max_freq')]
  return {str(path): path.read_text().strip() for path in paths if path.is_file()}


def verify(frames: int, warmup: int) -> dict:
  if not 1 <= frames <= 2000 or not 0 <= warmup <= 200:
    raise ValueError('frames must be 1..2000 and warmup 0..200')
  metadata = json.loads(MODEL.with_suffix('.metadata.json').read_text())
  fixtures_path = MODEL.with_suffix('.fixtures.npz')
  provenance = json.loads((HERE / 'provenance.json').read_text())
  pin = provenance['files']['models/q8b_cd210.fixtures.npz']
  verify_file(fixtures_path, pin['sha256'], pin['bytes'])
  before = policy_snapshot()
  rows = []
  with np.load(fixtures_path, allow_pickle=False) as fixtures, ThneedModel() as model:
    for repeat in range(2):
      for case in range(metadata['cases']):
        inputs = {name: fixtures[f'case_{case}_{name}'] for name in metadata['input_names']}
        output = model.run(inputs)
        np.testing.assert_array_equal(output, fixtures[f'case_{case}_cl'])
        np.testing.assert_allclose(output, fixtures[f'case_{case}_ort'], rtol=.001, atol=.005)
        queued = current_inputs(inputs)
        adapted = model.run_current(queued)
        np.testing.assert_array_equal(adapted['outputs'], output)
        np.testing.assert_array_equal(adapted['next_state_img_q'][:, -1], queued['new_img'])
        np.testing.assert_array_equal(adapted['next_state_desire_q'][-1, 0], queued['desire'])
        np.testing.assert_array_equal(adapted['next_state_feat_q'][-1], output[:, 1064:1576])
        rows.append({'repeat': repeat, 'case': case, 'outputs': output.size, 'exact_saved_cl': True,
                     'saved_cpu_reference_pass': True, 'current_queue_adapter_pass': True})
    inputs = {name: fixtures[f'case_0_{name}'] for name in metadata['input_names']}
    for _ in range(warmup):
      model.run(inputs)
    samples = []
    for _ in range(frames):
      start = time.perf_counter_ns()
      output = model.run(inputs)
      samples.append((time.perf_counter_ns() - start) / 1e6)
    np.testing.assert_array_equal(output, fixtures['case_0_cl'])
    device = model.device.info
  after = policy_snapshot()
  if before != after:
    raise RuntimeError('CPU/GPU policy changed during verification')
  return {
    'status': 'pass', 'artifact_sha256': MODEL_SHA256, 'new_conversion': False,
    'device': device, 'accuracy': rows, 'rtol': .001, 'atol': .005,
    'timing_scope': 'input uploads + synchronized replay/readback + Python validation; no camera/UI',
    'warmup': warmup, 'frames': frames, 'samples_ms': samples,
    'median_ms': float(np.median(samples)), 'p95_ms': float(np.percentile(samples, 95)),
    'policy_before': before, 'policy_after': after,
    'limits': 'Short same-input benchmark; not a new 20Hz camera run or full manager/recurrent qualification.',
  }


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--frames', type=int, default=40)
  parser.add_argument('--warmup', type=int, default=10)
  parser.add_argument('--output', type=Path, required=True)
  args = parser.parse_args()
  if args.output.exists():
    parser.error('Refusing to overwrite an existing report')
  # Reserve the receipt before device access so concurrent checks cannot overwrite it.
  with args.output.open('x') as receipt:
    try:
      result = verify(args.frames, args.warmup)
    except BaseException as error:
      json.dump({'status': 'fail', 'error': repr(error)}, receipt, indent=2)
      receipt.write('\n')
      raise
    json.dump(result, receipt, indent=2)
    receipt.write('\n')
  print(json.dumps({k: result[k] for k in ('status', 'frames', 'median_ms', 'p95_ms', 'new_conversion')}))


if __name__ == '__main__':
  main()
