import unittest
from types import SimpleNamespace

import numpy as np

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import desire_pulse, presentation_indices


class TestDesirePulse(unittest.TestCase):
  def test_desire_is_rising_edge_only(self):
    previous = np.zeros(8, dtype=np.float32)
    pulse, previous = desire_pulse('laneChangeStarting', 'left', previous)
    np.testing.assert_array_equal(np.flatnonzero(pulse), [3])
    pulse, previous = desire_pulse('laneChangeStarting', 'left', previous)
    assert not pulse.any()
    pulse, previous = desire_pulse('laneChangeFinishing', 'left', previous)
    assert not pulse.any()
    pulse, _ = desire_pulse('laneChangeStarting', 'left', previous)
    np.testing.assert_array_equal(np.flatnonzero(pulse), [3])


  def test_none_and_invalid_direction_never_pulse(self):
    previous = np.zeros(8, dtype=np.float32)
    for state, direction in [('off', 'left'), ('laneChangeStarting', 'none'), ('preLaneChange', 'right')]:
      pulse, previous = desire_pulse(state, direction, previous)
      assert not pulse.any()
    pulse, _ = desire_pulse('laneChangeStarting', 'right', previous)
    np.testing.assert_array_equal(np.flatnonzero(pulse), [4])


class TestPresentationIndex(unittest.TestCase):
  def test_video_offset_is_not_camera_ordinal(self):
    entries = [SimpleNamespace(frameId=5912 + i, segmentId=i, segmentNum=4, type='fullHEVC') for i in range(4)]
    mapping = presentation_indices(entries, 4)
    self.assertEqual(mapping[5913], 1)
    self.assertEqual(mapping[5915], 3)

  def test_duplicate_and_wrong_segment(self):
    entry = SimpleNamespace(frameId=5913, segmentId=1, segmentNum=4, type='fullHEVC')
    with self.assertRaises(ValueError):
      presentation_indices([entry, entry], 4)
    self.assertEqual(presentation_indices([entry], 5), {})
