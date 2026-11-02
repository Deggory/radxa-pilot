from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.run_qnn import bounded_run, verify_files


class TestBoundedReplay(unittest.TestCase):
  def test_runtime_change_and_outside_path_rejected(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      library = root / 'lib.so'
      library.write_bytes(b'pinned SDK library')
      files = {'lib.so': {'sha256': digest(library)}}
      verify_files(root, files)
      library.write_bytes(b'different release')
      with self.assertRaises(ValueError):
        verify_files(root, files)
      with self.assertRaises(ValueError):
        verify_files(root, {'../lib.so': files['lib.so']})

  def test_lease_failure_terminates_only_owned_child(self):
    process, lease = Mock(), Mock()
    process.poll.return_value = None
    lease.check.side_effect = RuntimeError('guard died')
    with patch('openpilot.selfdrive.modeld.npu.run_qnn.subprocess.Popen', return_value=process):
      with self.assertRaisesRegex(RuntimeError, 'guard died'):
        bounded_run(['private-qnn'], {}, None, lease, 0)
    process.terminate.assert_called_once()
    process.wait.assert_called_once_with(timeout=5)

  def test_timeout_kills_child_that_ignores_termination(self):
    process, lease = Mock(), Mock()
    process.poll.return_value = None
    process.wait.side_effect = [subprocess.TimeoutExpired('private-qnn', 5), 0]
    with patch('openpilot.selfdrive.modeld.npu.run_qnn.subprocess.Popen', return_value=process), \
         patch('openpilot.selfdrive.modeld.npu.run_qnn.time.monotonic', return_value=121):
      with self.assertRaises(TimeoutError):
        bounded_run(['private-qnn'], {}, None, lease, 0)
    process.terminate.assert_called_once()
    process.kill.assert_called_once()
