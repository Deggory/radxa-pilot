import ast
import os
from pathlib import Path
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import cv2 as cv
import numpy as np

from openpilot.system.camerad.webcam import config
from openpilot.system.camerad.webcam.camera import RoadCamera, bgr_to_nv12
from openpilot.system.camerad.webcam.native_capture import LatestCapture, NativeCapture, RawFrame
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info


class TestRoadConfiguration(unittest.TestCase):
  def test_model_build_includes_720p_warp_only_for_q8b(self):
    path = Path(__file__).resolve().parents[3] / 'selfdrive/modeld/SConscript'
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if (isinstance(n, ast.Assign) and
             any(isinstance(t, ast.Name) and t.id == 'camera_configs' for t in n.targets)) or
             (isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == 'RADXA_Q8B')]
    self.assertEqual(len(nodes), 2)
    for board in (False, True):
      scope = {'RADXA_Q8B': board, 'ROAD_WIDTH': 1280, 'ROAD_HEIGHT': 720,
               '_ar_ox_fisheye': SimpleNamespace(width=1928, height=1208),
               '_os_fisheye': SimpleNamespace(width=1344, height=760)}
      exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
      self.assertEqual((1280, 720) in scope['camera_configs'], board)

  def test_explicit_board_and_webcam_scope(self):
    for board, env, expected in [
      (True, {}, False),
      (False, {'USE_WEBCAM': '1'}, False),
      (True, {'USE_WEBCAM': '1', 'Q8B_ROAD_ONLY': '1'}, True),
    ]:
      with self.subTest(board=board, env=env), patch.dict(os.environ, env, clear=True), patch.object(config, 'RADXA_Q8B', board):
        self.assertEqual(config.road_only_enabled(), expected)
    for env in [{'Q8B_ROAD_ONLY': '1'}, {'USE_WEBCAM': '1', 'Q8B_ROAD_ONLY': 'yes'}]:
      with patch.dict(os.environ, env, clear=True), self.assertRaises(ValueError):
        config.road_only_enabled()
    with patch.dict(os.environ, {'USE_WEBCAM': '1', 'Q8B_ROAD_ONLY': '1'}, clear=True), patch.object(config, 'RADXA_Q8B', False):
      with self.assertRaises(ValueError):
        config.road_only_enabled()

  def test_stable_device_and_explicit_rotation(self):
    with patch.dict(os.environ, {}, clear=True):
      self.assertIn('SunplusIT_Inc_AK-Camera_JV-video-index0', config.road_camera_device())
      self.assertFalse(config.rotate_180())
    with patch.dict(os.environ, {'ROAD_CAM': '2', 'ROAD_CAM_ROTATE_180': '1'}, clear=True):
      self.assertEqual(config.road_camera_device(), '/dev/video2')
      self.assertTrue(config.rotate_180())
    with patch.dict(os.environ, {'ROAD_CAM': '/dev/v4l/by-id/custom'}, clear=True):
      self.assertEqual(config.road_camera_device(), '/dev/v4l/by-id/custom')
    with patch.dict(os.environ, {'DRIVER_CAM': '3'}, clear=True), self.assertRaises(ValueError):
      config.road_camera_device()

  def test_real_registry_disables_only_driver_camera_processes_in_road_mode(self):
    path = Path(__file__).resolve().parents[2] / 'manager/process_config.py'
    tree = ast.parse(path.read_text())
    calls = next(n.value.elts for n in tree.body if isinstance(n, ast.Assign) and
                 any(isinstance(t, ast.Name) and t.id == 'procs' for t in n.targets))
    names = {'camerad', 'webcamerad', 'dmonitoringmodeld', 'dmonitoringd', 'hardwared'}
    for road_only in (False, True):
      actual = {}
      def process(name, *_args, result=actual, **kwargs):
        result[name] = kwargs.get('enabled', True)
      scope = {'PythonProcess': process, 'NativeProcess': process, 'driverview': None,
               'livestream': None, 'always_run': None, 'or_': lambda *_: None,
               'WEBCAM': True, 'PC': True, 'Q8B_ROAD_ONLY': road_only}
      for call in calls:
        if isinstance(call, ast.Call) and isinstance(call.args[0], ast.Constant) and call.args[0].value in names:
          eval(compile(ast.Expression(call), str(path), 'eval'), scope)
      self.assertFalse(actual['camerad'])
      self.assertTrue(actual['webcamerad'])
      self.assertTrue(actual['hardwared'])
      self.assertEqual(actual['dmonitoringmodeld'], not road_only)
      self.assertEqual(actual['dmonitoringd'], not road_only)


class TestFrames(unittest.TestCase):
  def test_current_model_can_copy_the_full_720p_frame(self):
    data = bgr_to_nv12(np.zeros((720, 1280, 3), dtype=np.uint8))
    stride, y_height, uv_height, allocation = get_nv12_info(1280, 720)
    copied = np.frombuffer(data, dtype=np.uint8, count=stride * (y_height + uv_height))
    self.assertEqual(copied.size, 1_413_120)
    self.assertEqual(len(data), allocation)
    self.assertEqual(allocation, 2_220_032)

  def test_negotiated_mode_rejection_closes_native_handle(self):
    for mode in [(1280, 720, int.from_bytes(b'MJPG', 'little'), 30, 1, 4, 4_147_200),
                 (1280, 720, int.from_bytes(b'MJPG', 'little'), 60, 0, 4, 4_147_200)]:
      dll = MagicMock()
      dll.camera_open.return_value = 123
      def fill_info(_handle, info, result=mode):
        info[:] = result
        return 0
      dll.camera_get_info.side_effect = fill_info
      with patch('ctypes.CDLL', return_value=dll), self.assertRaises(ValueError):
        NativeCapture('/unused-camera')
      dll.camera_close.assert_called_once_with(123)

  def test_road_decode_orientation_and_timestamp_are_preserved(self):
    bgr = np.zeros((720, 1280, 3), dtype=np.uint8)
    bgr[:360] = (0, 0, 255)
    ok, jpeg = cv.imencode('.jpg', bgr)
    self.assertTrue(ok)
    timestamp = time.monotonic_ns()
    camera = RoadCamera.__new__(RoadCamera)
    camera.rotation = False
    camera.fresh_capture = False
    camera.capture = MagicMock()
    camera.capture.read.return_value = RawFrame(jpeg.tobytes(), timestamp, 51, 0)
    frame = next(camera.read_frames())
    self.assertEqual(frame.timestamp_ns, timestamp)
    self.assertEqual(frame.source_sequence, 51)
    self.assertEqual(frame.yuv, bgr_to_nv12(cv.imdecode(jpeg, cv.IMREAD_COLOR)))
    camera.rotation = True
    rotated = next(camera.read_frames())
    self.assertEqual(rotated.yuv, bgr_to_nv12(cv.flip(cv.imdecode(jpeg, cv.IMREAD_COLOR), -1)))

  def test_bad_and_stale_frames_are_not_published(self):
    camera = RoadCamera.__new__(RoadCamera)
    camera.rotation = False
    camera.fresh_capture = False
    camera.capture = MagicMock()
    for payload, timestamp in [(b'not a JPEG', time.monotonic_ns()), (b'', 1), (b'', time.monotonic_ns() + 10**12)]:
      camera.capture.read.return_value = RawFrame(payload, timestamp, 3, 0)
      with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
        next(camera.read_frames())

  def test_nv12_keeps_luma_and_interleaves_u_v(self):
    bgr = np.zeros((4, 4, 3), dtype=np.uint8)
    bgr[:2] = (0, 0, 255)
    bgr[2:] = (255, 0, 0)
    i420 = cv.cvtColor(bgr, cv.COLOR_BGR2YUV_I420).ravel()
    data = np.frombuffer(bgr_to_nv12(bgr), dtype=np.uint8)
    stride, y_height, uv_height, size = get_nv12_info(4, 4)
    self.assertEqual(len(data), size)
    y = data[:stride * y_height].reshape(y_height, stride)
    uv = data[stride * y_height:stride * (y_height + uv_height)].reshape(uv_height, stride)
    np.testing.assert_array_equal(y[:4, :4].ravel(), i420[:16])
    np.testing.assert_array_equal(uv[:2, :4:2].ravel(), i420[16:20])
    np.testing.assert_array_equal(uv[:2, 1:4:2].ravel(), i420[20:24])
    self.assertTrue(np.all(y[4:] == 16))
    self.assertTrue(np.all(uv[2:] == 128))

  def test_latest_slot_owns_bytes_and_does_not_repeat_frames(self):
    released = threading.Event()
    class Source:
      info = {'fps': 60}
      def __init__(self):
        self.counter = 0
        self.closed = False
      def read(self):
        self.counter += 1
        if self.counter > 2:
          released.wait(1)
          raise OSError('disconnected')
        return RawFrame(bytes([self.counter]), time.monotonic_ns(), self.counter, 0)
      def close(self):
        self.closed = True
    source = Source()
    capture = LatestCapture(source)
    try:
      with capture.condition:
        self.assertTrue(capture.condition.wait_for(lambda: capture.captured >= 2, timeout=1))
      frame = capture.read()
      self.assertEqual(frame.payload, b'\x02')
      self.assertEqual(frame.sequence, 2)
      released.set()
      with self.assertRaisesRegex(RuntimeError, 'capture stopped'):
        capture.read()
    finally:
      released.set()
      capture.close()
    self.assertTrue(source.closed)

  def test_fresh_deadline_discards_cached_frame_and_waits_for_next_arrival(self):
    capture = LatestCapture.__new__(LatestCapture)
    capture.condition = MagicMock()
    capture.latest = RawFrame(b'old', 100, 4, 0)
    capture.consumed, capture.error = 1, None
    def wait_for(predicate, timeout):
      self.assertFalse(predicate())
      capture.latest = RawFrame(b'new', 200, 5, 0)
      self.assertTrue(predicate())
      return True
    capture.condition.wait_for.side_effect = wait_for
    frame = capture.read(fresh=True)
    self.assertEqual((frame.sequence, frame.timestamp_ns, frame.payload), (5, 200, b'new'))
    self.assertEqual(capture.consumed, 5)

  def test_publication_pairs_real_timestamp_sequence_and_payload(self):
    from openpilot.system.camerad.webcam.camerad import Camerad
    from openpilot.cereal.visionipc import VisionStreamType
    class IPC:
      def send(self, *args):
        self.args = args
    class Publisher:
      def send(self, topic, msg):
        self.topic, self.msg = topic, msg
    service = Camerad.__new__(Camerad)
    service.vipc_server, service.pm = IPC(), Publisher()
    timestamp = time.monotonic_ns()
    service._send_yuv(b'payload', 7, 'narrowRoadCameraState', VisionStreamType.VISION_STREAM_NARROW_ROAD,
                      timestamp_ns=timestamp, source_sequence=23)
    self.assertEqual(service.vipc_server.args[1:4], (b'payload', 7, timestamp))
    msg = service.pm.msg.narrowRoadCameraState
    self.assertEqual(msg.frameId, 7)
    self.assertEqual(msg.frameIdSensor, 23)
    self.assertEqual(msg.timestampSof, timestamp)
    self.assertEqual(msg.timestampEof, timestamp)

  def test_capture_failure_closes_camera_and_reaches_manager(self):
    from openpilot.system.camerad.webcam.camerad import Camerad
    service = Camerad.__new__(Camerad)
    service.road_only = True
    service.cameras = [MagicMock()]
    service.camera_runner = MagicMock(side_effect=RuntimeError('camera disconnected'))
    with self.assertRaisesRegex(RuntimeError, 'camera disconnected'):
      service.run()
    service.cameras[0].close.assert_called_once()


if __name__ == '__main__':
  unittest.main()
