from dataclasses import dataclass
import time

import cv2 as cv
import numpy as np

from openpilot.system.camerad.webcam.config import ROAD_WIDTH, ROAD_HEIGHT, rotate_180
from openpilot.system.camerad.webcam.native_capture import LatestCapture, NativeCapture


def bgr_to_nv12(bgr: np.ndarray) -> bytes:
  height, width = bgr.shape[:2]
  i420 = cv.cvtColor(bgr, cv.COLOR_BGR2YUV_I420).ravel()
  y_size = height * width
  uv_size = y_size // 4
  nv12 = np.empty_like(i420)
  nv12[:y_size] = i420[:y_size]
  nv12[y_size::2] = i420[y_size:y_size + uv_size]
  nv12[y_size + 1::2] = i420[y_size + uv_size:]
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
    self.source = NativeCapture(camera_id)
    try:
      self.capture = LatestCapture(self.source)
    except BaseException:
      self.source.close()
      raise
    print(f'Q8B road camera: {camera_id}, {self.source.info}, rotate_180={self.rotation}', flush=True)

  def read_frames(self):
    while True:
      raw = self.capture.read()
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
