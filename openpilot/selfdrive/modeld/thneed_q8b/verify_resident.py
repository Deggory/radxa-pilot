"""Exact image/history and model checks for resident NV12 inputs, not a latency benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from openpilot.common.hardware.radxa.performance import MaxPerformanceLease
from openpilot.selfdrive.modeld.thneed_q8b.runtime import ThneedModel, CURRENT_SPECS, to_legacy_inputs, next_states, MODEL_SHA256
from openpilot.selfdrive.modeld.thneed_q8b.state import exact_gather_map, prepare_nv12, provisional_transforms
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--output-dir', type=Path, required=True)
  parser.add_argument('--frames', type=int, default=12)
  args = parser.parse_args()
  if args.frames < 12:
    parser.error('At least 12 changing steps are required')
  args.output_dir.mkdir(parents=True, exist_ok=False)
  matrices = provisional_transforms()
  maps = exact_gather_map(matrices)
  size = get_nv12_info(1280, 720)[3]
  queues = {k: np.zeros(shape, dtype=dtype) for k, (shape, dtype) in CURRENT_SPECS.items() if k.startswith('state_')}
  generator = np.random.default_rng(1931)
  rows = []
  with MaxPerformanceLease() as performance, ThneedModel() as model:
    model.configure_images(maps)
    for index in range(args.frames):
      if index == 6:
        matrices = (np.array([[1.01, .02, 3.25], [-.02, .97, 8.5], [.00001, -.00001, 1]], dtype=np.float32),
                    np.eye(3, dtype=np.float32))
        model.configure_images(exact_gather_map(matrices))
      if index == 8:
        model.reset_images()
        for value in queues.values():
          value.fill(0)
      # Distinct source bytes cover Y, both chroma channels and padded boundaries.
      camera = generator.integers(0, 256, size, dtype=np.uint8)
      views = np.stack([prepare_nv12(camera, matrix, 1280, 720) for matrix in matrices])
      desire = np.eye(8, dtype=np.float32)[index % 8]
      inputs = {'new_img': views, 'desire': desire, 'traffic_convention': np.array([[1, 0]], dtype=np.float32),
                'action_t': np.array([[.2, .3]], dtype=np.float32), **queues}
      legacy = to_legacy_inputs(inputs)
      start = time.monotonic_ns()
      model.prepare_images(camera)
      elapsed = (time.monotonic_ns() - start) / 1e6
      inspected = model.inspect_images_for_verification()  # Explicit qualification-only readback.
      np.testing.assert_array_equal(inspected[0], legacy['img'][0])
      np.testing.assert_array_equal(inspected[1], legacy['big_img'][0])
      resident = model.run_resident({k: v for k, v in inputs.items() if k not in ('new_img', 'state_img_q')})
      actual = resident['outputs'].copy()
      expected = model.run(legacy)
      np.testing.assert_array_equal(actual, expected)
      next_queues = next_states(inputs, actual)
      for key in ('state_desire_q', 'state_feat_q'):
        np.testing.assert_array_equal(resident['next_' + key], next_queues['next_' + key])
      if index in (0, 2, 4, 6, 8, 11):
        np.savez_compressed(args.output_dir / f'frame-{index:03d}.npz', raw=actual[0], **inputs)
      queues = {key: next_queues['next_' + key] for key in queues}
      rows.append({'frame': index, 'image_bytes_exact': True, 'model_outputs_exact': 2576,
                   'geometry_changed_before_step': index == 6,
                   'reset_before_step': index == 8, 'gpu_prepare_host_ms': elapsed})
      performance.check()
    device = model.device.info
  result = {'status': 'pass', 'rows': rows, 'artifact_sha256': MODEL_SHA256, 'device': device,
            'initial_gather_map_sha256': hashlib.sha256(maps.tobytes()).hexdigest(),
            'production_image_readbacks': 0, 'history_lag_frames': 4,
            'limits': 'Qualification uses explicit image readbacks and CPU warps; these are absent from the production resident path.'}
  (args.output_dir / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
  print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
  main()
