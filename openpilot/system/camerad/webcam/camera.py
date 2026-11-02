from dataclasses import dataclass
import os
import time

import cv2 as cv
import numpy as np

from openpilot.system.camerad.webcam.config import ROAD_WIDTH, ROAD_HEIGHT, rotate_180
from openpilot.system.camerad.webcam.native_capture import LatestCapture, NativeCapture
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info


def bgr_to_nv12(bgr: np.ndarray) -> bytes:
  """Use the same padded NV12 layout as current modeld/compile_warp."""
  height, width = bgr.shape[:2]
  i420 = cv.cvtColor(bgr, cv.COLOR_BGR2YUV_I420).ravel()
  y_size = height * width
  uv_size = y_size // 4
  stride, y_height, uv_height, size = get_nv12_info(width, height)
  nv12 = np.zeros(size, dtype=np.uint8)
  y = nv12[:stride * y_height].reshape(y_height, stride)
  uv = nv12[stride * y_height:stride * (y_height + uv_height)].reshape(uv_height, stride)
  y[:] = 16
  uv[:] = 128
  y[:height, :width] = i420[:y_size].reshape(height, width)
  uv[:height // 2, :width:2] = i420[y_size:y_size + uv_size].reshape(height // 2, width // 2)
  uv[:height // 2, 1:width:2] = i420[y_size + uv_size:].reshape(height // 2, width // 2)
  return nv12.tobytes()


@dataclass(frozen=True)
class RoadFrame:
  yuv: bytes
  timestamp_ns: int
  source_sequence: int


class RoadCamera:
  W, H = ROAD_WIDTH, ROAD_HEIGHT

  def __init__(self, cam_type_state, stream_type, camera_id):
    self.cam_type_state, self.stream_type = cam_type_state, stream_type
    self.cur_frame_id = 0
    self.rotation = rotate_180()
    fresh = os.getenv('Q8B_FRESH_CAPTURE', '1')
    if fresh not in ('0', '1'):
      raise ValueError('Q8B_FRESH_CAPTURE must be 0 or 1')
    self.fresh_capture = fresh == '1'
    self.source = NativeCapture(camera_id)
    try:
      self.capture = LatestCapture(self.source)
    except BaseException:
      self.source.close()
      raise
    print(f'Q8B road camera: {camera_id}, {self.source.info}, rotate_180={self.rotation}', flush=True)

  def read_frames(self):
    while True:
      raw = self.capture.read(fresh=self.fresh_capture)
      # Bound age independently of queue depth; never relabel an old frame as new.
      if not 0 <= time.monotonic_ns() - raw.timestamp_ns <= 250_000_000:
        raise ValueError('Q8B camera frame is stale (over 250 ms) or from the future')
      bgr = cv.imdecode(np.frombuffer(raw.payload, dtype=np.uint8), cv.IMREAD_COLOR)
      if bgr is None or bgr.shape != (self.H, self.W, 3):
        raise ValueError('Q8B camera returned an invalid JPEG or unexpected image size')
      if self.rotation:
        bgr = cv.flip(bgr, -1)
      yuv = bgr_to_nv12(bgr)
      if time.monotonic_ns() - raw.timestamp_ns > 250_000_000:
        raise ValueError('Q8B frame became stale during decode/conversion')
      yield RoadFrame(yuv, raw.timestamp_ns, raw.sequence)

  def close(self):
    self.capture.close()

class Camera:
  def __init__(self, cam_type_state, stream_type, camera_id):
    try:
      camera_id = int(camera_id)
    except ValueError: # allow strings, ex: /dev/video0
      pass
    self.cam_type_state = cam_type_state
    self.stream_type = stream_type
    self.cur_frame_id = 0

    print(f"Opening {cam_type_state} at {camera_id}")

    self.cap = cv.VideoCapture(camera_id)

    self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280.0)
    self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720.0)
    self.cap.set(cv.CAP_PROP_FPS, 25.0)

    self.W = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
    self.H = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

  @classmethod
  def bgr2nv12(self, bgr):
    import av
    frame = av.VideoFrame.from_ndarray(bgr, format='bgr24')
    return frame.reformat(format='nv12').to_ndarray()

  def read_frames(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      # Rotate the frame 180 degrees (flip both axes)
      frame = cv.flip(frame, -1)
      yuv = Camera.bgr2nv12(frame)
      yield yuv.data.tobytes()
    self.cap.release()
