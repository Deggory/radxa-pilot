import tempfile
from pathlib import Path
import unittest

from openpilot.common.hardware.radxa.telemetry import read_health, HealthSampler


class TestQ8bTelemetry(unittest.TestCase):
  def test_named_sensors_and_pwm_are_read_only_and_distinguish_missing(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      files = {'class/thermal/thermal_zone9/type': 'cpu7-1-thermal', 'class/thermal/thermal_zone9/temp': '45200',
               'class/thermal/thermal_zone2/type': 'cpu0-0-thermal', 'class/thermal/thermal_zone2/temp': '48800',
               'class/thermal/thermal_zone3/type': 'gpuss-2-thermal', 'class/thermal/thermal_zone3/temp': '39100',
               'class/thermal/thermal_zone4/type': 'pmic-thermal', 'class/thermal/thermal_zone4/temp': '99000',
               'class/hwmon/hwmon73/name': 'radxa_svc_glink', 'class/hwmon/hwmon73/pwm1': '96',
               'class/hwmon/hwmon73/pwm1_enable': '2'}
      for name, value in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
      sample = read_health(root)
      self.assertEqual((sample['cpu_c'], sample['gpu_c'], sample['pwm'], sample['fan_mode']), (48.8, 39.1, 96, 2))
      self.assertAlmostEqual(sample['pwm_percent'], 96 / 255 * 100)
      self.assertIsNone(sample['fan_rpm'])
      for name, value in files.items():
        self.assertEqual((root / name).read_text(), value)
      (root / 'class/hwmon/hwmon73/pwm1').write_text('999')
      (root / 'class/thermal/thermal_zone3/temp').write_text('invalid')
      sample = read_health(root)
      self.assertIsNone(sample['pwm'])
      self.assertIsNone(sample['gpu_c'])

  def test_missing_is_not_zero_and_stale_samples_expire(self):
    with tempfile.TemporaryDirectory() as directory:
      sample = read_health(Path(directory))
      self.assertIsNone(sample['cpu_c'])
      self.assertIsNone(sample['pwm'])
      sampler = HealthSampler(Path(directory))
      sampler.close()
      try:
        sampler.latest = {**sample, 'sample_ns': 1_000_000_000, 'cpu_c': 42.0}
        self.assertEqual(sampler.snapshot(2_000_000_000)['cpu_c'], 42.0)
        self.assertIsNone(sampler.snapshot(5_000_000_000)['cpu_c'])
      finally:
        sampler.close()
      self.assertFalse(sampler.thread.is_alive())
