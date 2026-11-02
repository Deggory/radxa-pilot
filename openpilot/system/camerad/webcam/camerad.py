#!/usr/bin/env python3
import threading
import os
import platform
import signal
from collections import namedtuple

from openpilot.cereal.visionipc import VisionStreamType
from msgq.visionipc import VisionIpcServer
from openpilot.cereal import messaging

from openpilot.system.camerad.webcam.camera import Camera, RoadCamera
from openpilot.system.camerad.webcam.config import PUBLISH_FPS, road_only_enabled, road_camera_device
from openpilot.common.realtime import Ratekeeper
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info

NARROW_ROAD_CAM = os.getenv("NARROW_ROAD_CAM", os.getenv("ROAD_CAM", "0"))
WIDE_CAM = os.getenv("WIDE_CAM")
DRIVER_CAM = os.getenv("DRIVER_CAM")

CameraType = namedtuple("CameraType", ["msg_name", "stream_type", "cam_id"])

CAMERAS = [
  CameraType("narrowRoadCameraState", VisionStreamType.VISION_STREAM_NARROW_ROAD, NARROW_ROAD_CAM)
]
if WIDE_CAM:
  CAMERAS.append(CameraType("wideRoadCameraState", VisionStreamType.VISION_STREAM_WIDE_ROAD, WIDE_CAM))
if DRIVER_CAM:
  CAMERAS.append(CameraType("cabinCameraState", VisionStreamType.VISION_STREAM_CABIN, DRIVER_CAM))

class Camerad:
  def __init__(self):
    self.road_only = road_only_enabled()
    selected = CAMERAS
    if self.road_only:
      selected = [CameraType('narrowRoadCameraState', VisionStreamType.VISION_STREAM_NARROW_ROAD, road_camera_device())]
    self.pm = messaging.PubMaster([c.msg_name for c in selected])
    self.vipc_server = VisionIpcServer("camerad")
    self.cameras = []
    try:
      for c in selected:
        if self.road_only:
          cam = RoadCamera(c.msg_name, c.stream_type, c.cam_id)
        else:
          cam_device = f"/dev/video{c.cam_id}" if platform.system() != "Darwin" else c.cam_id
          cam = Camera(c.msg_name, c.stream_type, cam_device)
        self.cameras.append(cam)
        if self.road_only:
          stride, y_height, _uv_height, size = get_nv12_info(cam.W, cam.H)
          self.vipc_server.create_buffers_with_sizes(c.stream_type, 20, cam.W, cam.H, size, stride, stride * y_height)
        else:
          self.vipc_server.create_buffers(c.stream_type, 20, int(cam.W), int(cam.H))
      self.vipc_server.start_listener()
    except BaseException:
      if self.road_only:
        for cam in self.cameras:
          cam.close()
      raise

  def _send_yuv(self, yuv, frame_id, pub_type, yuv_type, *, timestamp_ns=None, source_sequence=None):
    eof = timestamp_ns if timestamp_ns is not None else int(frame_id * 0.05 * 1e9)
    self.vipc_server.send(yuv_type, yuv, frame_id, eof, eof)
    dat = messaging.new_message(pub_type, valid=True)
    msg = {
      "frameId": frame_id,
      "transform": [1.0, 0.0, 0.0,
                    0.0, 1.0, 0.0,
                    0.0, 0.0, 1.0]
    }
    if timestamp_ns is not None:
      # UVC provides one driver timestamp, not independently measured SOF/EOF.
      # Keep it paired with the frame in both IPC and the camera-state message.
      msg.update(timestampSof=eof, timestampEof=eof, frameIdSensor=source_sequence)
    setattr(dat, pub_type, msg)
    self.pm.send(pub_type, dat)

  def camera_runner(self, cam):
    rk = Ratekeeper(PUBLISH_FPS, None)
    for frame in cam.read_frames():
      if self.road_only:
        self._send_yuv(frame.yuv, cam.cur_frame_id, cam.cam_type_state, cam.stream_type,
                       timestamp_ns=frame.timestamp_ns, source_sequence=frame.source_sequence)
      else:
        self._send_yuv(frame, cam.cur_frame_id, cam.cam_type_state, cam.stream_type)
      cam.cur_frame_id += 1
      rk.keep_time()

  def run(self):
    if self.road_only:
      # A capture/decode failure reaches the process manager; do not leave a
      # healthy-looking publisher alive after a worker thread has died.
      try:
        self.camera_runner(self.cameras[0])
      finally:
        self.cameras[0].close()
      return
    threads = []
    for cam in self.cameras:
      cam_thread = threading.Thread(target=self.camera_runner, args=(cam,))
      cam_thread.start()
      threads.append(cam_thread)

    for t in threads:
      t.join()


def main():
  if road_only_enabled():
    def shutdown(_signum, _frame):
      raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, shutdown)
  camerad = Camerad()
  try:
    camerad.run()
  except KeyboardInterrupt:
    if not camerad.road_only:
      raise


if __name__ == "__main__":
  main()
