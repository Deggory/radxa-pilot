import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock

import numpy as np

from openpilot.selfdrive.modeld.thneed_q8b.state import prepare_nv12, thneed_enabled, select_small_model, ThneedModelState
from openpilot.selfdrive.modeld.thneed_q8b.runtime import next_states
from openpilot.system.camerad.cameras.nv12_info import get_nv12_info


class TestStateBoundary(unittest.TestCase):
  def test_opt_in_requires_q8b_road_only_and_webcam(self):
    with patch.dict(os.environ, {}, clear=True):
      self.assertFalse(thneed_enabled())
      os.environ['Q8B_THNEED'] = 'yes'
      with self.assertRaises(ValueError):
        thneed_enabled()
      os.environ['Q8B_THNEED'] = '1'
      with self.assertRaises(ValueError):
        thneed_enabled()
      os.environ.update(Q8B_ROAD_ONLY='1', USE_WEBCAM='1')
      with patch('openpilot.system.camerad.webcam.config.RADXA_Q8B', False):
        with self.assertRaises(ValueError):
          thneed_enabled()
      with patch('openpilot.system.camerad.webcam.config.RADXA_Q8B', True):
        self.assertTrue(thneed_enabled())

  def test_selection_preserves_stock_by_default(self):
    stock = Mock(return_value='stock')
    with patch.dict(os.environ, {}, clear=True):
      self.assertEqual(select_small_model(1280, 720, stock), 'stock')
      stock.assert_called_once_with(1280, 720, False)
    stock.reset_mock()
    with patch('openpilot.selfdrive.modeld.thneed_q8b.state.thneed_enabled', return_value=True):
      with patch('openpilot.selfdrive.modeld.thneed_q8b.state.ThneedModelState', return_value='thneed'):
        self.assertEqual(select_small_model(1280, 720, stock), 'thneed')
        stock.assert_not_called()

  def test_padded_nv12_warp_respects_uv_offset_and_view_translation(self):
    stride, y_height, uv_height, size = get_nv12_info(1280, 720)
    frame = np.full(size, 255, dtype=np.uint8)
    yy, xx = np.indices((720, 1280))
    y = (yy + xx * 3).astype(np.uint8)
    uv = frame[stride*y_height:stride*(y_height+uv_height)].reshape(uv_height, stride)
    frame[:stride*y_height].reshape(y_height, stride)[:720, :1280] = y
    uv[:360, :1280:2] = 31
    uv[:360, 1:1280:2] = 97
    matrix = np.array([[1, 0, 256], [0, 1, 128], [0, 0, 1]], dtype=np.float32)
    actual = prepare_nv12(frame, matrix, 1280, 720)
    crop = y[128:384, 256:768]
    np.testing.assert_array_equal(actual[:4], np.stack((crop[::2, ::2], crop[1::2, ::2], crop[::2, 1::2], crop[1::2, 1::2])))
    np.testing.assert_array_equal(actual[4], 31)
    np.testing.assert_array_equal(actual[5], 97)

  def test_bad_warp_and_short_buffer_rejected(self):
    data = np.zeros(get_nv12_info(1280, 720)[3], dtype=np.uint8)
    for matrix in (np.zeros((3, 3), dtype=np.float32), np.full((3, 3), np.nan, dtype=np.float32)):
      with self.assertRaises(ValueError):
        prepare_nv12(data, matrix, 1280, 720)
    with self.assertRaises(ValueError):
      prepare_nv12(data[:100], np.eye(3, dtype=np.float32), 1280, 720)

  def test_perspective_rounding_matches_pinned_unbatched_warp(self):
    from tinygrad import Tensor, Context
    from examples.openpilot.compile_warp import make_frame_prepare, NV12Frame
    from openpilot.system.camerad.webcam.camera import bgr_to_nv12
    y, x = np.indices((720, 1280))
    frame = bgr_to_nv12(np.stack((x % 256, y % 256, (x+y) % 256), axis=-1).astype(np.uint8))
    matrix = np.array([[1.01, .02, 3.25], [-.02, .97, 8.5], [.00001, -.00001, 1]], dtype=np.float32)
    actual = prepare_nv12(frame, matrix, 1280, 720)
    stride, yh, uvh, _ = get_nv12_info(1280, 720)
    reference = make_frame_prepare(NV12Frame(1280, 720, stride, yh, uvh, stride * (yh+uvh)), 512, 256)
    with Context(DEV='CPU:LLVM'):
      expected = reference(Tensor(np.frombuffer(frame, dtype=np.uint8).copy(), device='CPU'), Tensor(matrix, device='CPU')).numpy()
    # A NumPy rewrite differed at a rounding boundary for this actual perspective transform.
    np.testing.assert_array_equal(actual, expected)

  def test_model_state_owns_recurrence_and_warmup_resets_it(self):
    class Backend:
      calls = 0
      closed = False

      def run_current(self, inputs):
        self.calls += 1
        output = np.zeros((1, 2576), dtype=np.float32)
        output[:, 1064:1576] = self.calls
        return next_states(inputs, output)

      def close(self):
        self.closed = True

    with patch.dict(os.environ, {'Q8B_THNEED': '1', 'Q8B_ROAD_ONLY': '1', 'USE_WEBCAM': '1'}):
      with patch('openpilot.system.camerad.webcam.config.RADXA_Q8B', True):
        with patch('openpilot.sunnypilot.modeld_v2.modeld_base.ModelStateBase.__init__', return_value=None):
          state = ThneedModelState(1280, 720, backend_factory=Backend)
    backend = state.backend
    try:
      data = np.zeros(get_nv12_info(1280, 720)[3], dtype=np.uint8)
      bufs = dict.fromkeys(state.vision_input_names, data)
      transforms = dict.fromkeys(state.vision_input_names, np.eye(3, dtype=np.float32))
      inputs = {'desire_pulse': np.array([1, 1, 0, 0, 0, 0, 0, 0], dtype=np.float32),
                'traffic_convention': np.array([1, 0]), 'action_t': np.zeros(2)}
      original_desire = inputs['desire_pulse'].copy()
      callback = Mock()
      result = state.run(bufs, transforms, inputs, callback)
      callback.assert_called_once()
      self.assertEqual(result['plan'].shape, (1, 33, 15))
      self.assertEqual(state.last_inputs['desire'][1], 1)
      np.testing.assert_array_equal(state.queues['state_feat_q'][-1], 1)
      state.run(bufs, transforms, inputs)
      self.assertEqual(state.last_inputs['desire'][1], 0)
      np.testing.assert_array_equal(state.last_inputs['state_feat_q'][-1], 1)
      np.testing.assert_array_equal(state.queues['state_feat_q'][-1], 2)
      np.testing.assert_array_equal(inputs['desire_pulse'], original_desire)
      state.warmup()
      self.assertTrue(all(not np.any(v) for v in state.queues.values()))
      self.assertFalse(np.any(state.prev_desire))
    finally:
      state.close()
      state.close()
    self.assertTrue(backend.closed)

  def test_manager_routes_only_stock_runner_and_defers_other_compiler(self):
    from openpilot.system.manager import process_config as config
    from openpilot.cereal import custom
    with patch.object(config, 'Q8B_THNEED', True):
      with patch.object(config, 'get_active_model_runner', side_effect=AssertionError('must not inspect alternate model')):
        self.assertTrue(config.is_stock_model(True, None, None))
        self.assertFalse(config.is_tinygrad_model(True, None, None))
    with patch.object(config, 'Q8B_THNEED', False):
      with patch.object(config, 'get_active_model_runner', return_value=custom.ModelManagerSP.Runner.tinygrad):
        self.assertFalse(config.is_stock_model(True, None, None))
        self.assertTrue(config.is_tinygrad_model(True, None, None))

  def test_snapshots_require_private_namespace_before_creating_backend(self):
    with tempfile.TemporaryDirectory() as directory:
      target = Path(directory) / 'samples'
      with patch.dict(os.environ, {'Q8B_THNEED': '1', 'Q8B_ROAD_ONLY': '1', 'USE_WEBCAM': '1',
                                   'OPENPILOT_PREFIX': 'normal', 'Q8B_THNEED_SNAPSHOT_DIR': str(target)}):
        with patch('openpilot.system.camerad.webcam.config.RADXA_Q8B', True):
          with patch('openpilot.sunnypilot.modeld_v2.modeld_base.ModelStateBase.__init__', return_value=None):
            backend = Mock()
            with self.assertRaisesRegex(ValueError, 'isolated preview'):
              ThneedModelState(1280, 720, backend_factory=backend)
            backend.assert_not_called()
            self.assertFalse(target.exists())


if __name__ == '__main__':
  unittest.main()
