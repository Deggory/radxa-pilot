"""Opt-in Thneed implementation of stock modeld's ModelState interface."""
import atexit
from functools import lru_cache
import json
import os
from pathlib import Path

import numpy as np

from openpilot.selfdrive.modeld.parse_model_outputs import Parser
from openpilot.selfdrive.modeld.thneed_q8b.runtime import HERE, CURRENT_SPECS, ThneedModel
from openpilot.sunnypilot.modeld_v2.modeld_base import ModelStateBase
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info
from openpilot.system.camerad.webcam.config import ROAD_WIDTH, ROAD_HEIGHT, road_only_enabled


def thneed_enabled() -> bool:
  value = os.getenv('Q8B_THNEED', '0')
  if value not in ('0', '1'):
    raise ValueError('Q8B_THNEED must be 0 or 1')
  if value == '1' and not road_only_enabled():
    raise ValueError('Q8B_THNEED=1 requires Q8B road-only webcam mode')
  return value == '1'


def select_small_model(width, height, stock_factory):
  return ThneedModelState(width, height) if thneed_enabled() else stock_factory(width, height, False)


@lru_cache(maxsize=1)
def pinned_warp(width, height):
  from tinygrad import Tensor, TinyJit
  from examples.openpilot.compile_warp import make_frame_prepare, NV12Frame
  stride, yh, uvh, _ = get_nv12_info(width, height)
  warp = make_frame_prepare(NV12Frame(width, height, stride, yh, uvh, stride * (yh + uvh)), 512, 256)

  @TinyJit
  def run(frame: Tensor, matrix: Tensor):
    return warp(frame, matrix).contiguous().realize()

  return run


def prepare_nv12(data, matrix: np.ndarray, width: int, height: int) -> np.ndarray:
  """Use current pinned CPU:LLVM warp, including its floating-point rounding."""
  if (width, height) != (ROAD_WIDTH, ROAD_HEIGHT):
    raise ValueError('Q8B Thneed currently requires the accepted 1280x720 camera profile')
  if matrix.shape != (3, 3) or not np.isfinite(matrix).all():
    raise ValueError('finite 3x3 transform required')
  matrix = np.asarray(matrix, dtype=np.float32)
  stride, y_height, uv_height, _ = get_nv12_info(width, height)
  size = stride * (y_height + uv_height)
  frame = np.frombuffer(data, dtype=np.uint8)
  if frame.size < size:
    raise ValueError(f'NV12 buffer needs at least {size} bytes')
  # Denominator is affine over the rectangle: reject any zero crossing before sampling.
  w = matrix[2] @ np.array([[0, 511, 0, 511], [0, 0, 255, 255], [1, 1, 1, 1]], dtype=np.float32)
  if not np.isfinite(matrix).all() or not np.isfinite(w).all() or not (np.all(w > 1e-9) or np.all(w < -1e-9)):
    raise ValueError('invalid perspective denominator')
  from tinygrad import Tensor, Context
  with Context(DEV='CPU:LLVM'):
    return pinned_warp(width, height)(Tensor(frame[:size].copy(), device='CPU'), Tensor(matrix, device='CPU')).numpy().copy()


def provisional_transforms():
  """Explicit bench assumption only; this does not mark calibration valid."""
  from openpilot.common.transformations.camera import get_device_camera_config
  from openpilot.common.transformations.model import get_warp_matrix
  intrinsics = get_device_camera_config('radxaQ8b', 'unknown').narrow_road.intrinsics
  return tuple(get_warp_matrix(np.zeros(3), intrinsics, wide).astype(np.float32) for wide in (False, True))


class ThneedModelState(ModelStateBase):
  vision_input_names = ('img', 'big_img')
  chestnut = False

  def __init__(self, cam_w, cam_h, *, backend_factory=ThneedModel):
    if not thneed_enabled():
      raise ValueError('Thneed ModelState requires explicit Q8B_THNEED=1')
    if (cam_w, cam_h) != (ROAD_WIDTH, ROAD_HEIGHT):
      raise ValueError('Q8B Thneed requires 1280x720 frames')
    super().__init__()
    self.sample_directory = os.getenv('Q8B_THNEED_SNAPSHOT_DIR')
    if self.sample_directory:
      if not os.getenv('OPENPILOT_PREFIX', '').startswith('q8b_preview_'):
        raise ValueError('Model input snapshots require the isolated preview namespace')
      self.sample_directory = Path(self.sample_directory)
      self.sample_directory.mkdir(parents=True, exist_ok=True)
    self.width, self.height = cam_w, cam_h
    self.output_slices = {k: slice(*v) for k, v in json.loads((HERE / 'output_slices.json').read_text()).items()}
    self.parser = Parser()
    self.backend = backend_factory()
    self.reset()
    atexit.register(self.close)

  def reset(self):
    self.queues = {k: np.zeros(shape, dtype=dtype) for k, (shape, dtype) in CURRENT_SPECS.items() if k.startswith('state_')}
    self.prev_desire = np.zeros(8, dtype=np.float32)
    self.last_inputs = None
    self.last_raw = None
    self.run_count = 0

  def run(self, bufs, transforms, inputs, after_enqueue=None):
    views = np.stack([prepare_nv12(getattr(bufs[k], 'data', bufs[k]), transforms[k], self.width, self.height)
                      for k in self.vision_input_names])
    desire = np.asarray(inputs['desire_pulse'], dtype=np.float32).copy()
    desire[0] = 0
    current = {
      'new_img': views,
      'desire': np.where(desire - self.prev_desire > .99, desire, 0).astype(np.float32),
      'traffic_convention': np.ascontiguousarray(inputs['traffic_convention'], dtype=np.float32).reshape(1, 2),
      'action_t': np.ascontiguousarray(inputs['action_t'], dtype=np.float32).reshape(1, 2),
      **self.queues,
    }
    result = self.backend.run_current(current)
    if after_enqueue is not None:
      after_enqueue()
    raw = result['outputs'][0].copy()
    parsed = self.parser.parse_outputs({k: raw[None, v].copy() for k, v in self.output_slices.items()})
    self.queues = {k: result[f'next_{k}'] for k in self.queues}
    self.prev_desire = desire
    self.last_inputs, self.last_raw = current, raw
    self.run_count += 1
    if self.sample_directory and self.run_count in (20, 200, 400, 600, 800, 1000):
      with (self.sample_directory / f'frame-{self.run_count:06d}.npz').open('xb') as sample:
        np.savez_compressed(sample, raw=raw, **current)
    if os.getenv('SEND_RAW_PRED'):
      parsed['raw_pred'] = raw.copy()
    return parsed

  def warmup(self):
    size = get_nv12_info(self.width, self.height)[3]
    frame = np.zeros(size, dtype=np.uint8)
    self.run(dict.fromkeys(self.vision_input_names, frame), dict.fromkeys(self.vision_input_names, np.eye(3, dtype=np.float32)),
             {'desire_pulse': np.zeros(8, dtype=np.float32), 'traffic_convention': np.array([1, 0]), 'action_t': np.zeros(2)})
    self.reset()

  def close(self):
    if self.backend is not None:
      self.backend.close()
      self.backend = None
    atexit.unregister(self.close)
