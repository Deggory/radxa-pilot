import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import MagicMock, patch

from openpilot.system.camerad.webcam.preview import preview_environment, stop_children


class TestPreviewIsolation(unittest.TestCase):
  def test_uses_private_messages_and_params_without_modifying_parent_environment(self):
    with patch.dict(os.environ, {'OPENPILOT_PREFIX': 'existing', 'PARAMS_ROOT': '/existing', 'DISPLAY': ':7'}):
      env = preview_environment(Path('/tmp/private-preview'), 'q8b_preview_test')
      self.assertEqual(env['OPENPILOT_PREFIX'], 'q8b_preview_test')
      self.assertEqual(env['PARAMS_ROOT'], '/tmp/private-preview/params')
      self.assertEqual(env['DISPLAY'], ':7')
      self.assertEqual(env['Q8B_ROAD_ONLY'], '1')
      self.assertEqual(env['RECORD'], '0')
      self.assertEqual(os.environ['OPENPILOT_PREFIX'], 'existing')
      self.assertEqual(os.environ['PARAMS_ROOT'], '/existing')

  def test_stops_owned_children_and_reaps_even_when_one_requires_kill(self):
    camera, ui = MagicMock(), MagicMock()
    camera.poll.return_value = None
    ui.poll.return_value = 0
    camera.wait.side_effect = [subprocess.TimeoutExpired('camera', 8), 0]
    stop_children([camera, ui])
    camera.terminate.assert_called_once()
    camera.kill.assert_called_once()
    self.assertEqual(camera.wait.call_count, 2)
    ui.terminate.assert_not_called()
    ui.kill.assert_not_called()
    ui.wait.assert_called_once()


if __name__ == '__main__':
  unittest.main()
