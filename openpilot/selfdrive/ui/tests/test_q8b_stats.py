import os
import unittest
from unittest.mock import patch

from openpilot.selfdrive.ui.onroad.q8b_stats import display_number, fan_text
from openpilot.system.camerad.webcam.config import stats_enabled


class TestQ8bStats(unittest.TestCase):
  def test_zero_is_a_measurement_and_unknown_is_unavailable(self):
    self.assertEqual(display_number(0., 'ms'), '0.0 ms')
    self.assertEqual(display_number(None, 'ms'), '--')
    self.assertEqual(fan_text({'pwm': 0, 'pwm_percent': 0., 'fan_mode': 1}), ('0% MANUAL', '0/255 | RPM unavailable'))
    self.assertEqual(fan_text({'pwm': None, 'pwm_percent': None, 'fan_mode': 2}), ('--', 'PWM duty | RPM unavailable'))

  def test_scoped_opt_out_and_invalid_setting(self):
    with patch('openpilot.system.camerad.webcam.config.road_only_enabled', return_value=True), patch.dict(os.environ, {}, clear=True):
      self.assertTrue(stats_enabled())
      os.environ['Q8B_SHOW_STATS'] = '0'
      self.assertFalse(stats_enabled())
      os.environ['Q8B_SHOW_STATS'] = 'yes'
      with self.assertRaises(ValueError):
        stats_enabled()
    with patch('openpilot.system.camerad.webcam.config.road_only_enabled', return_value=False), patch.dict(os.environ, {}, clear=True):
      self.assertFalse(stats_enabled())
