"""Replay the already-converted CD210 artifact on its matching Q8B OpenCL GPU."""
import ctypes as C
import hashlib
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / 'models/q8b_cd210.thneed'
MODEL_SHA256 = 'eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068'
MODEL_BYTES = 99641029
LEGACY_SPECS = {
  'img': ((1, 12, 128, 256), np.uint8),
  'big_img': ((1, 12, 128, 256), np.uint8),
  'features_buffer': ((1, 24, 512), np.float32),
  'desire_pulse': ((1, 25, 8), np.float32),
  'traffic_convention': ((1, 2), np.float32),
  'action_t': ((1, 2), np.float32),
}
CURRENT_SPECS = {
  'new_img': ((2, 6, 128, 256), np.uint8),
  'desire': ((8,), np.float32),
  'traffic_convention': ((1, 2), np.float32),
  'action_t': ((1, 2), np.float32),
  'state_img_q': ((2, 5, 6, 128, 256), np.uint8),
  'state_desire_q': ((100, 1, 8), np.float32),
  'state_feat_q': ((96, 1, 512), np.float32),
}


def verify_file(path: Path, sha256: str, size: int | None = None) -> None:
  if size is not None and path.stat().st_size != size:
    raise ValueError(f'{path.name}: size mismatch')
  with path.open('rb') as stream:
    actual = hashlib.file_digest(stream, 'sha256').hexdigest()
  if actual != sha256:
    raise ValueError(f'{path.name}: SHA256 mismatch')


def validate_inputs(inputs: dict[str, np.ndarray], specs: dict) -> None:
  if inputs.keys() != specs.keys():
    raise ValueError(f'input names differ: expected {tuple(specs)}')
  for name, (shape, dtype) in specs.items():
    value = inputs[name]
    if not isinstance(value, np.ndarray) or value.shape != shape or value.dtype != np.dtype(dtype):
      raise ValueError(f'{name}: expected {shape}/{np.dtype(dtype)}')
    if not value.flags.c_contiguous or not np.isfinite(value).all():
      raise ValueError(f'{name}: contiguous finite data required')


def to_legacy_inputs(inputs: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
  """Match the pinned 65a08adc ONNX wrapper's exact Slice/Concat/ReduceMax order."""
  validate_inputs(inputs, CURRENT_SPECS)
  image = np.concatenate((inputs['state_img_q'][:, 1:], inputs['new_img'][:, None]), axis=1)
  desire = np.concatenate((inputs['state_desire_q'][1:], inputs['desire'][None, None]), axis=0)
  return {
    'img': np.ascontiguousarray(image[0, ::4].reshape(1, 12, 128, 256)),
    'big_img': np.ascontiguousarray(image[1, ::4].reshape(1, 12, 128, 256)),
    'features_buffer': np.ascontiguousarray(inputs['state_feat_q'][::4].transpose(1, 0, 2)),
    'desire_pulse': np.ascontiguousarray(desire.reshape(25, 4, 1, 8).max(axis=1).transpose(1, 0, 2)),
    'traffic_convention': inputs['traffic_convention'],
    'action_t': inputs['action_t'],
  }


def next_states(inputs: dict[str, np.ndarray], outputs: np.ndarray) -> dict[str, np.ndarray]:
  return {
    'outputs': outputs,
    'next_state_img_q': np.concatenate((inputs['state_img_q'][:, 1:], inputs['new_img'][:, None]), axis=1),
    'next_state_desire_q': np.concatenate((inputs['state_desire_q'][1:], inputs['desire'][None, None]), axis=0),
    'next_state_feat_q': np.concatenate((inputs['state_feat_q'][1:], outputs[:, 1064:1576][None]), axis=0),
  }


def check(status: int) -> None:
  if status != 0:
    raise RuntimeError(f'OpenCL error {status}')


class OpenCLContext:
  """Own a GPU context/queue without importing or patching Tinygrad."""
  def __init__(self, expected: dict):
    self.context = self.queue = None
    self.lib = C.CDLL('libOpenCL.so.1')
    signatures = {
      'clGetPlatformIDs': ([C.c_uint, C.c_void_p, C.c_void_p], C.c_int),
      'clGetDeviceIDs': ([C.c_void_p, C.c_uint64, C.c_uint, C.c_void_p, C.c_void_p], C.c_int),
      'clGetDeviceInfo': ([C.c_void_p, C.c_uint, C.c_size_t, C.c_void_p, C.c_void_p], C.c_int),
      'clCreateContext': ([C.c_void_p, C.c_uint, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p], C.c_void_p),
      'clCreateCommandQueueWithProperties': ([C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p], C.c_void_p),
      'clReleaseCommandQueue': ([C.c_void_p], C.c_int),
      'clReleaseContext': ([C.c_void_p], C.c_int),
    }
    for name, (args, result) in signatures.items():
      function = getattr(self.lib, name)
      function.argtypes, function.restype = args, result
    count = C.c_uint()
    check(self.lib.clGetPlatformIDs(0, None, C.byref(count)))
    platforms = (C.c_void_p * count.value)()
    check(self.lib.clGetPlatformIDs(count, platforms, None))
    self.device = None
    for platform in platforms:
      count = C.c_uint()
      status = self.lib.clGetDeviceIDs(platform, 4, 0, None, C.byref(count))  # CL_DEVICE_TYPE_GPU only
      if status == -1:
        continue
      check(status)
      devices = (C.c_void_p * count.value)()
      check(self.lib.clGetDeviceIDs(platform, 4, count, devices, None))
      for device in devices:
        self.info = {'name': self.device_string(device, 0x102B), 'driver': self.device_string(device, 0x102D)}
        if all(self.info[k] == expected[k] for k in ('name', 'driver')):
          self.device = device
          break
      if self.device:
        break
    if not self.device:
      raise RuntimeError('No GPU matches the saved Thneed device/driver; no CPU fallback')
    error = C.c_int()
    device_array = (C.c_void_p * 1)(self.device)
    try:
      self.context = self.lib.clCreateContext(None, 1, device_array, None, None, C.byref(error))
      check(error.value)
      if not self.context:
        raise RuntimeError('OpenCL context creation returned null')
      self.queue = self.lib.clCreateCommandQueueWithProperties(self.context, self.device, None, C.byref(error))
      check(error.value)
      if not self.queue:
        raise RuntimeError('OpenCL queue creation returned null')
    except BaseException:
      self.close()
      raise

  def device_string(self, device, key: int) -> str:
    size = C.c_size_t()
    check(self.lib.clGetDeviceInfo(device, key, 0, None, C.byref(size)))
    buffer = C.create_string_buffer(size.value)
    check(self.lib.clGetDeviceInfo(device, key, size, buffer, None))
    return buffer.value.decode()

  def close(self) -> None:
    if self.queue:
      self.lib.clReleaseCommandQueue(self.queue)
      self.queue = None
    if self.context:
      self.lib.clReleaseContext(self.context)
      self.context = None


class ThneedModel:
  """Single-owner synchronous replay. Only the pinned, trusted artifact is accepted."""
  def __init__(self, artifact: Path = MODEL):
    verify_file(artifact, MODEL_SHA256, MODEL_BYTES)
    self.handle = None
    self.device = None
    manifest = json.loads((HERE / 'provenance.json').read_text())
    metadata_path = artifact.with_suffix('.metadata.json')
    pin = manifest['files']['models/q8b_cd210.metadata.json']
    verify_file(metadata_path, pin['sha256'], pin['bytes'])
    self.metadata = json.loads(metadata_path.read_text())
    if self.metadata['input_names'] != list(LEGACY_SPECS):
      raise ValueError('saved model input order mismatch')
    self.lib = C.CDLL(str(HERE / 'build/libq8b_thneed.so'))
    self.lib.q8b_thneed_error.restype = C.c_char_p
    self.lib.q8b_thneed_load.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.c_char_p, C.c_size_t]
    self.lib.q8b_thneed_load.restype = C.c_void_p
    self.lib.q8b_thneed_upload.argtypes = [C.c_void_p, C.c_uint, C.c_void_p, C.c_size_t]
    self.lib.q8b_thneed_upload.restype = C.c_int
    self.lib.q8b_thneed_run.argtypes = [C.c_void_p, C.c_void_p]
    self.lib.q8b_thneed_run.restype = C.c_int
    self.lib.q8b_thneed_destroy.argtypes = [C.c_void_p]
    self.lib.q8b_thneed_destroy.restype = None
    try:
      self.device = OpenCLContext(self.metadata['device'])
      self.handle = self.lib.q8b_thneed_load(self.device.context, self.device.device, self.device.queue,
                                          str(artifact).encode(), self.metadata['output_bytes'])
      if not self.handle:
        raise RuntimeError(self.lib.q8b_thneed_error().decode())
    except BaseException:
      self.close()
      raise

  def native_check(self, status: int) -> None:
    if status != 0:
      raise RuntimeError(self.lib.q8b_thneed_error().decode())

  def run(self, inputs: dict[str, np.ndarray]) -> np.ndarray:
    started = time.monotonic_ns()
    validate_inputs(inputs, LEGACY_SPECS)
    validated = time.monotonic_ns()
    if not self.handle:
      raise RuntimeError('Thneed model is closed')
    for index, name in enumerate(LEGACY_SPECS):
      value = inputs[name]
      self.native_check(self.lib.q8b_thneed_upload(self.handle, index, value.ctypes.data, value.nbytes))
    output = np.empty((1, 2576), dtype=np.float16)
    uploaded = time.monotonic_ns()
    self.native_check(self.lib.q8b_thneed_run(self.handle, output.ctypes.data))
    finished = time.monotonic_ns()
    self.last_timing = {
      'input_validation_ms': (validated - started) / 1e6,
      'upload_ms': (uploaded - validated) / 1e6,
      'inference_readback_ms': (finished - uploaded) / 1e6,
    }
    if not np.isfinite(output).all():
      raise RuntimeError('nonfinite Thneed output')
    return output.astype(np.float32)

  def run_current(self, inputs: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    return next_states(inputs, self.run(to_legacy_inputs(inputs)))

  def close(self) -> None:
    if self.handle:
      self.lib.q8b_thneed_destroy(self.handle)
      self.handle = None
    if self.device:
      self.device.close()
      self.device = None

  def __enter__(self):
    return self

  def __exit__(self, *_):
    self.close()
