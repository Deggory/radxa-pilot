"""Owned UVC MJPEG frames with V4L2 timestamps; no external workspace imports.

Adapted from the previously tested Q8B capture.py/capture.c and latest_camera.py.
The C helper restores the prior camera format/rate when its owner closes it.
"""
import ctypes as C
from dataclasses import dataclass
import errno
from pathlib import Path
import threading
import time

from openpilot.system.camerad.webcam.config import ROAD_WIDTH, ROAD_HEIGHT, CAPTURE_FPS


@dataclass(frozen=True)
class RawFrame:
  payload: bytes
  timestamp_ns: int
  sequence: int
  discarded: int


class NativeCapture:
  def __init__(self, path: str):
    library = Path(__file__).with_name('libuvc_capture.so')
    if not library.is_file():
      raise RuntimeError('Build the Q8B camera helper first; see webcam/README.md')
    self.lib = C.CDLL(str(library), use_errno=True)
    self.lib.camera_open.argtypes = [C.c_char_p, C.c_uint, C.c_uint, C.c_uint]
    self.lib.camera_open.restype = C.c_void_p
    self.lib.camera_get_info.argtypes = [C.c_void_p, C.POINTER(C.c_uint32)]
    self.lib.camera_get_info.restype = C.c_int
    self.lib.camera_read.argtypes = [C.c_void_p, C.c_void_p, C.c_uint, C.POINTER(C.c_uint64)]
    self.lib.camera_read.restype = C.c_int
    self.lib.camera_close.argtypes = [C.c_void_p]
    self.lib.camera_close.restype = None
    self.handle = self.lib.camera_open(path.encode(), ROAD_WIDTH, ROAD_HEIGHT, CAPTURE_FPS)
    if not self.handle:
      raise OSError(C.get_errno(), 'Unable to open Q8B MJPEG camera', path)
    try:
      info = (C.c_uint32 * 7)()
      if self.lib.camera_get_info(self.handle, info) < 0:
        raise OSError(C.get_errno(), 'Unable to read negotiated camera mode')
      fourcc = int.from_bytes(b'MJPG', 'little')
      if (info[0], info[1], info[2]) != (ROAD_WIDTH, ROAD_HEIGHT, fourcc) or not info[4] or abs(info[3] / info[4] - CAPTURE_FPS) > 0.1:
        raise ValueError(f'Camera did not negotiate 1280x720 MJPG/60 FPS: {list(info)}')
      self.info = {'width': info[0], 'height': info[1], 'fourcc': 'MJPG', 'fps': info[3] / info[4], 'buffers': info[5]}
      self.buffer = C.create_string_buffer(max(info[6], ROAD_WIDTH * ROAD_HEIGHT * 3))
      self.meta = (C.c_uint64 * 4)()
      self.last_timestamp = 0
      self.recoverable_errors = 0
    except BaseException:
      self.close()
      raise

  def read(self) -> RawFrame:
    for _ in range(3):
      size = self.lib.camera_read(self.handle, self.buffer, len(self.buffer), self.meta)
      if size >= 0:
        timestamp, sequence, _flags, discarded = self.meta
        if timestamp <= self.last_timestamp or timestamp > time.monotonic_ns():
          raise ValueError('Camera timestamp is not strictly increasing monotonic time')
        self.last_timestamp = timestamp
        return RawFrame(C.string_at(self.buffer, size), timestamp, sequence, discarded)
      error = C.get_errno()
      if error not in (errno.EIO, errno.EAGAIN):
        raise OSError(error, 'Q8B camera capture failed')
      self.recoverable_errors += 1
    raise OSError(error, 'Camera failed after three consecutive recoverable reads')

  def close(self):
    if self.handle:
      self.lib.camera_close(self.handle)
      self.handle = None


class LatestCapture:
  """Drain 60 Hz capture continuously; expose one owned latest JPEG, never a FIFO."""
  def __init__(self, source):
    self.source = source
    self.condition = threading.Condition()
    self.stop = threading.Event()
    self.latest = None
    self.consumed = None
    self.error = None
    self.captured = self.overwritten = self.discarded = 0
    self.thread = threading.Thread(target=self._capture, name='q8b-road-capture', daemon=True)
    self.thread.start()

  def _capture(self):
    try:
      while not self.stop.is_set():
        frame = self.source.read()
        with self.condition:
          if self.latest is not None and self.latest.sequence != self.consumed:
            self.overwritten += 1
          self.latest = frame
          self.captured += 1
          self.discarded += frame.discarded
          self.condition.notify_all()
    except Exception as error:
      with self.condition:
        self.error = error
        self.condition.notify_all()
    finally:
      self.source.close()

  def read(self) -> RawFrame:
    with self.condition:
      ready = self.condition.wait_for(lambda: self.error is not None or
                                     (self.latest is not None and self.latest.sequence != self.consumed), timeout=3.5)
      if self.error is not None:
        raise RuntimeError('Q8B camera capture stopped') from self.error
      if not ready:
        raise TimeoutError('No fresh Q8B camera frame within 3.5 seconds')
      self.consumed = self.latest.sequence
      return self.latest

  def close(self):
    self.stop.set()
    self.thread.join(timeout=4)
    if self.thread.is_alive():
      raise TimeoutError('Q8B capture thread did not stop')
