import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.q8b.performance_guard import Profile


class TestPerformanceProfile(unittest.TestCase):
  def make_profile(self, root):
    files = {
      'proc/device-tree/compatible': 'radxa,dragon-q8b\0qcom,sc8280xp\0',
      'sys/class/devfreq/3d00000.gpu/available_frequencies': '270000000 690000000',
      'sys/class/devfreq/3d00000.gpu/available_governors': 'userspace simple_ondemand',
      'sys/class/devfreq/3d00000.gpu/governor': 'simple_ondemand',
      'sys/class/devfreq/3d00000.gpu/min_freq': '270000000',
      'sys/class/devfreq/3d00000.gpu/max_freq': '690000000',
      'sys/class/devfreq/3d00000.gpu/cur_freq': '690000000',
      'sys/class/thermal/thermal_zone0/temp': '45000',
    }
    for number, maximum in [(0, '2438400'), (4, '2995200')]:
      for name, value in {'scaling_governor': 'schedutil', 'scaling_available_governors': 'performance schedutil',
                          'cpuinfo_max_freq': maximum, 'scaling_max_freq': maximum, 'scaling_cur_freq': maximum}.items():
        files[f'sys/devices/system/cpu/cpufreq/policy{number}/{name}'] = value
    for name, value in files.items():
      path = root / name
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text(value)
    return Profile(root)

  def test_apply_readback_restore_and_temperature_trip(self):
    with tempfile.TemporaryDirectory() as directory:
      profile = self.make_profile(Path(directory))
      original = profile.original.copy()
      profile.apply()
      self.assertEqual(profile.telemetry()['gpu_hz'], 690000000)
      (profile.root / 'sys/class/thermal/thermal_zone0/temp').write_text('85000')
      with self.assertRaisesRegex(RuntimeError, 'Temperature limit'):
        profile.telemetry()
      profile.restore()
      self.assertTrue(all(p.read_text().strip() == v for p, v in original.items()))

  def test_refuse_changed_board_or_reduced_limits_without_writes(self):
    for name, value in [('proc/device-tree/compatible', 'other-board'),
                        ('sys/class/devfreq/3d00000.gpu/max_freq', '500000000'),
                        ('sys/devices/system/cpu/cpufreq/policy4/scaling_max_freq', '2000000')]:
      with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        profile = self.make_profile(root)
        (root / name).write_text(value)
        with self.assertRaises(RuntimeError):
          Profile(root)
        self.assertEqual((profile.gpu / 'governor').read_text(), 'simple_ondemand')

  def test_policy_change_and_missing_thermals_refuse_continuation(self):
    with tempfile.TemporaryDirectory() as directory:
      profile = self.make_profile(Path(directory))
      profile.apply()
      (profile.gpu / 'min_freq').write_text('270000000')
      with self.assertRaisesRegex(RuntimeError, 'mismatch'):
        profile.telemetry()
      profile.restore()
      (profile.root / 'sys/class/thermal/thermal_zone0/temp').unlink()
      with self.assertRaisesRegex(RuntimeError, 'No thermal'):
        profile.temperatures()

  def test_restore_attempts_remaining_paths_after_failure(self):
    with tempfile.TemporaryDirectory() as directory:
      profile = self.make_profile(Path(directory))
      profile.apply()
      write = Path.write_text
      def failing_write(path, value, *args, **kwargs):
        if path == profile.gpu / 'min_freq':
          raise OSError('test failure')
        return write(path, value, *args, **kwargs)
      with patch.object(Path, 'write_text', failing_write), self.assertRaisesRegex(RuntimeError, 'retained'):
        profile.restore()
      self.assertEqual((profile.policies[0] / 'scaling_governor').read_text().strip(), 'schedutil')

class TestPerformancePrivilegeBoundary(unittest.TestCase):
  def test_full_status_pipe_does_not_block_guard(self):
    from tools.q8b.performance_guard import emit
    with patch('tools.q8b.performance_guard.os.write', side_effect=BlockingIOError):
      emit({'telemetry': {}})
      with self.assertRaisesRegex(RuntimeError, 'pipe is full'):
        emit({'ready': True}, required=True)

  def test_installer_rejects_untrusted_ancestors_before_creation(self):
    from tools.q8b import install_performance as installer
    import os
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      with patch.dict(os.environ, {'SUDO_USER': 'radxa'}), patch.object(installer.os, 'geteuid', return_value=0), \
           patch.object(installer.os, 'umask', return_value=0o022), \
           patch.object(installer, 'DESTINATION', root / 'libexec/helper'), \
           patch.object(installer, 'RULE', root / 'rules/rule'), patch.object(Path, 'mkdir') as mkdir:
        with self.assertRaises((RuntimeError, FileNotFoundError)):
          installer.install()
        mkdir.assert_not_called()

  def test_missing_installed_helper_does_not_attempt_sudo_or_load_model(self):
    from openpilot.common.hardware.radxa.performance import MaxPerformanceLease
    with patch('openpilot.common.hardware.radxa.performance.Path.is_file', return_value=False), \
         patch('openpilot.common.hardware.radxa.performance.subprocess.Popen') as process:
      with self.assertRaisesRegex(RuntimeError, 'One-time local setup'):
        MaxPerformanceLease()
      process.assert_not_called()


if __name__ == '__main__':
  unittest.main()
