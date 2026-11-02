"""Opt-in Thneed implementation of stock modeld's ModelState interface."""
import atexit
from functools import lru_cache
import json
import os
import time
from pathlib import Path

import numpy as np

from openpilot.common.hardware.radxa.performance import MaxPerformanceLease
from openpilot.selfdrive.modeld.parse_model_outputs import Parser
from openpilot.selfdrive.modeld.thneed_q8b.runtime import HERE, CURRENT_SPECS, ThneedModel, validate_inputs
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


def exact_gather_map(matrices, width=1280, height=720):
  """Encode source byte addresses through the pinned warp once per geometry.

  Three byte passes preserve its exact FP32/round-half-even decisions. Per-frame
  GPU gathering then needs no CPU warp or intermediate image readback.
  """
  matrices = np.asarray(matrices, dtype=np.float32)
  if matrices.shape != (2, 3, 3) or not np.isfinite(matrices).all():
    raise ValueError('Two finite 3x3 camera transforms required')
  stride, yh, uvh, _ = get_nv12_info(width, height)
  addresses = np.arange(stride * (yh + uvh), dtype=np.uint32)
  result = np.zeros((2, 6, 128, 256), dtype=np.uint32)
  for shift in (0, 8, 16):
    encoded = ((addresses >> shift) & 255).astype(np.uint8)
    for view, matrix in enumerate(matrices):
      result[view] |= prepare_nv12(encoded, matrix, width, height).astype(np.uint32) << shift
  return result


def provisional_transforms():
  """Explicit bench assumption only; this does not mark calibration valid."""
  from openpilot.common.transformations.camera import get_device_camera_config
  from openpilot.common.transformations.model import get_warp_matrix
  intrinsics = get_device_camera_config('radxaQ8b', 'unknown').narrow_road.intrinsics
  return tuple(get_warp_matrix(np.zeros(3), intrinsics, wide).astype(np.float32) for wide in (False, True))


class ThneedModelState(ModelStateBase):
  vision_input_names = ('img', 'big_img')
  chestnut = False

  def __init__(self, cam_w, cam_h, *, backend_factory=ThneedModel, performance_factory=MaxPerformanceLease):
    if not thneed_enabled():
      raise ValueError('Thneed ModelState requires explicit Q8B_THNEED=1')
    if (cam_w, cam_h) != (ROAD_WIDTH, ROAD_HEIGHT):
      raise ValueError('Q8B Thneed requires 1280x720 frames')
    super().__init__()
    gpu_prepare = os.getenv('Q8B_GPU_PREP', '1')
    if gpu_prepare not in ('0', '1'):
      raise ValueError('Q8B_GPU_PREP must be 0 or 1')
    self.gpu_prepare = gpu_prepare == '1'
    self.map_key = None
    self.sample_directory = os.getenv('Q8B_THNEED_SNAPSHOT_DIR')
    if self.sample_directory:
      if not os.getenv('OPENPILOT_PREFIX', '').startswith('q8b_preview_'):
        raise ValueError('Model input snapshots require the isolated preview namespace')
      self.sample_directory = Path(self.sample_directory)
      self.sample_directory.mkdir(parents=True, exist_ok=True)
    if self.gpu_prepare and self.sample_directory:
      raise ValueError('Resident input validation uses explicit GPU verification, not CPU-image snapshots')
    self.width, self.height = cam_w, cam_h
    self.output_slices = {k: slice(*v) for k, v in json.loads((HERE / 'output_slices.json').read_text()).items()}
    self.parser = Parser()
    self.backend = self.performance = None
    try:
      self.performance = performance_factory()
      self.backend = backend_factory()
      self.reset()
    except BaseException as e:
      try:
        self.close()
      except Exception as close_error:
        e.add_note(str(close_error))
      raise
    atexit.register(self.close)

  def reset(self):
    self.queues = {k: np.zeros(shape, dtype=dtype) for k, (shape, dtype) in CURRENT_SPECS.items()
                   if k.startswith('state_') and (not self.gpu_prepare or k != 'state_img_q')}
    if self.gpu_prepare:
      self.backend.reset_images()
    self.prev_desire = np.zeros(8, dtype=np.float32)
    self.last_inputs = None
    self.last_raw = None
    self.run_count = 0
    self.needs_reset = False

  def run(self, bufs, transforms, inputs, after_enqueue=None):
    if self.needs_reset:
      raise RuntimeError('A failed resident frame requires reset before another prediction')
    self.performance.check()
    started = time.monotonic_ns()
    desire = np.asarray(inputs['desire_pulse'], dtype=np.float32).copy()
    desire[0] = 0
    current = {
      'desire': np.where(desire - self.prev_desire > .99, desire, 0).astype(np.float32),
      'traffic_convention': np.ascontiguousarray(inputs['traffic_convention'], dtype=np.float32).reshape(1, 2),
      'action_t': np.ascontiguousarray(inputs['action_t'], dtype=np.float32).reshape(1, 2),
      **self.queues,
    }
    if self.gpu_prepare:
      if bufs['img'] is not bufs['big_img']:
        raise ValueError('Resident Q8B path requires the same single road camera for both model views')
      validate_inputs(current, {k: v for k, v in CURRENT_SPECS.items() if k not in ('new_img', 'state_img_q')})
      # Any failure after this point requires reset: image and feature history must advance together.
      self.needs_reset = True
      matrices = np.stack([transforms[k] for k in self.vision_input_names]).astype(np.float32)
      key = matrices.tobytes()
      if key != self.map_key:
        self.backend.configure_images(exact_gather_map(matrices, self.width, self.height))
        self.map_key = key
      configured = time.monotonic_ns()
      self.backend.prepare_images(getattr(bufs['img'], 'data', bufs['img']))
      views = None
    else:
      configured = started
      views = np.stack([prepare_nv12(getattr(bufs[k], 'data', bufs[k]), transforms[k], self.width, self.height)
                        for k in self.vision_input_names])
    prepared = time.monotonic_ns()
    if self.gpu_prepare:
      result = self.backend.run_resident(current)
    else:
      current['new_img'] = views
      result = self.backend.run_current(current)
    if after_enqueue is not None:
      after_enqueue()
    raw = result['outputs'][0].copy()
    parsed = self.parser.parse_outputs({k: raw[None, v].copy() for k, v in self.output_slices.items()})
    self.queues = {k: result[f'next_{k}'] for k in self.queues}
    self.prev_desire = desire
    self.last_timing = {'cpu_prepare_ms': 0.0 if self.gpu_prepare else (prepared - started) / 1e6,
                        'gpu_prepare_ms': (prepared - configured) / 1e6 if self.gpu_prepare else 0.0,
                        'map_configuration_ms': (configured - started) / 1e6 if self.gpu_prepare else 0.0,
                        **getattr(self.backend, 'last_timing', {}), 'resident_images': self.gpu_prepare,
                        'performance': self.performance.last_telemetry}
    self.last_inputs, self.last_raw = current, raw
    self.run_count += 1
    if self.sample_directory and self.run_count in (20, 200, 400, 600, 800, 1000):
      with (self.sample_directory / f'frame-{self.run_count:06d}.npz').open('xb') as sample:
        np.savez_compressed(sample, raw=raw, **current)
    if os.getenv('SEND_RAW_PRED'):
      parsed['raw_pred'] = raw.copy()
    self.needs_reset = False
    return parsed

  def warmup(self):
    size = get_nv12_info(self.width, self.height)[3]
    frame = np.zeros(size, dtype=np.uint8)
    self.run(dict.fromkeys(self.vision_input_names, frame), dict.fromkeys(self.vision_input_names, np.eye(3, dtype=np.float32)),
             {'desire_pulse': np.zeros(8, dtype=np.float32), 'traffic_convention': np.array([1, 0]), 'action_t': np.zeros(2)})
    self.reset()

  def close(self):
    try:
      if self.backend is not None:
        backend, self.backend = self.backend, None
        backend.close()
    finally:
      if self.performance is not None:
        performance, self.performance = self.performance, None
        performance.close()
      atexit.unregister(self.close)
