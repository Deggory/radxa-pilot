import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from openpilot.selfdrive.modeld.thneed_q8b.runtime import (
  CURRENT_SPECS, LEGACY_SPECS, ThneedModel, next_states, to_legacy_inputs, validate_inputs, verify_file,
)


class TestContract(unittest.TestCase):
  def inputs(self):
    return {k: np.zeros(shape, dtype=dtype) for k, (shape, dtype) in CURRENT_SPECS.items()}

  def test_hash_and_size_reject_corruption(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'model'
      path.write_bytes(b'good')
      verify_file(path, hashlib.sha256(b'good').hexdigest(), 4)
      path.write_bytes(b'evil')
      with self.assertRaises(ValueError):
        verify_file(path, hashlib.sha256(b'good').hexdigest(), 4)
      with self.assertRaises(ValueError):
        verify_file(path, hashlib.sha256(b'evil').hexdigest(), 5)

  def test_exact_input_boundary(self):
    inputs = self.inputs()
    validate_inputs(inputs, CURRENT_SPECS)
    for mutation in ('missing', 'extra', 'dtype', 'shape', 'nan', 'noncontiguous'):
      bad = inputs.copy()
      if mutation == 'missing':
        del bad['action_t']
      elif mutation == 'extra':
        bad['unknown'] = np.zeros(1)
      elif mutation == 'dtype':
        bad['action_t'] = bad['action_t'].astype(np.float16)
      elif mutation == 'shape':
        bad['action_t'] = np.zeros(2, dtype=np.float32)
      elif mutation == 'nan':
        bad['action_t'] = np.full((1, 2), np.nan, dtype=np.float32)
      else:
        bad['state_feat_q'] = bad['state_feat_q'][::-1]
      with self.subTest(mutation=mutation), self.assertRaises(ValueError):
        validate_inputs(bad, CURRENT_SPECS)

  def test_bad_artifact_refused_before_gpu_or_native_loading(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'bad.thneed'
      path.write_bytes(b'bad')
      with patch('openpilot.selfdrive.modeld.thneed_q8b.runtime.OpenCLContext') as device:
        with patch('openpilot.selfdrive.modeld.thneed_q8b.runtime.C.CDLL') as library:
          with self.assertRaises(ValueError):
            ThneedModel(path)
          device.assert_not_called()
          library.assert_not_called()

  def test_wrapper_samples_exact_history_slots(self):
    inputs = self.inputs()
    for view in range(2):
      inputs['new_img'][view] = 90 + view
      for frame in range(5):
        inputs['state_img_q'][view, frame] = view * 10 + frame
    inputs['state_feat_q'][:] = np.arange(96, dtype=np.float32)[:, None, None]
    inputs['state_desire_q'][1, 0, 2] = .75
    inputs['desire'][4] = 1
    original = {k: v.copy() for k, v in inputs.items()}
    legacy = to_legacy_inputs(inputs)
    validate_inputs(legacy, LEGACY_SPECS)
    np.testing.assert_array_equal(legacy['img'][0, :6], 1)
    np.testing.assert_array_equal(legacy['img'][0, 6:], 90)
    np.testing.assert_array_equal(legacy['big_img'][0, :6], 11)
    np.testing.assert_array_equal(legacy['big_img'][0, 6:], 91)
    np.testing.assert_array_equal(legacy['features_buffer'][0, :, 0], np.arange(0, 96, 4))
    self.assertEqual(legacy['desire_pulse'][0, 0, 2], .75)
    self.assertEqual(legacy['desire_pulse'][0, -1, 4], 1)
    for k in inputs:
      np.testing.assert_array_equal(inputs[k], original[k])

  def test_next_states_append_features_and_do_not_alias(self):
    inputs = self.inputs()
    outputs = np.arange(2576, dtype=np.float32).reshape(1, -1)
    inputs['new_img'][:] = 73
    inputs['desire'][3] = 1
    result = next_states(inputs, outputs)
    np.testing.assert_array_equal(result['next_state_img_q'][:, -1], inputs['new_img'])
    np.testing.assert_array_equal(result['next_state_desire_q'][-1, 0], inputs['desire'])
    np.testing.assert_array_equal(result['next_state_feat_q'][-1], outputs[:, 1064:1576])
    for k in ('img', 'desire', 'feat'):
      self.assertFalse(np.shares_memory(result[f'next_state_{k}_q'], inputs[f'state_{k}_q']))


if __name__ == '__main__':
  unittest.main()
