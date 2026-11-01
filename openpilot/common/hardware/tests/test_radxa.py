"""Q8B identity contracts, using real schemas and read-only hardware classes."""
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openpilot.cereal import log


class TestRadxaDetection(unittest.TestCase):
  def setUp(self):
    self.platform = importlib.import_module('openpilot.common.platform')
    self.temp = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp.cleanup)
    self.path = Path(self.temp.name) / 'compatible'
    self.linux = patch.object(self.platform.platform, 'system', return_value='Linux')
    self.arm = patch.object(self.platform.platform, 'machine', return_value='aarch64')
    self.linux.start()
    self.arm.start()
    self.addCleanup(self.linux.stop)
    self.addCleanup(self.arm.stop)

  def test_exact_compatible_token_first_or_later(self):
    for contents in (b'radxa,dragon-q8b\0qcom,sc8280xp\0', b'qcom,sc8280xp\0radxa,dragon-q8b\0'):
      with self.subTest(contents=contents):
        self.path.write_bytes(contents)
        self.assertTrue(self.platform.is_radxa_q8b(self.path))

  def test_other_boards_and_substrings_are_not_q8b(self):
    for contents in (b'', b'qcom,sc8280xp\0', b'radxa,rock-5b\0',
                     b'radxa,dragon-q8b-pro\0', b'prefix-radxa,dragon-q8b\0'):
      with self.subTest(contents=contents):
        self.path.write_bytes(contents)
        self.assertFalse(self.platform.is_radxa_q8b(self.path))

  def test_missing_or_unreadable_tree_is_generic(self):
    self.assertFalse(self.platform.is_radxa_q8b(self.path))
    with patch.object(Path, 'read_bytes', side_effect=PermissionError):
      self.assertFalse(self.platform.is_radxa_q8b(self.path))

  def test_other_os_or_architecture_is_generic(self):
    self.path.write_bytes(b'radxa,dragon-q8b\0')
    with patch.object(self.platform.platform, 'system', return_value='Darwin'):
      self.assertFalse(self.platform.is_radxa_q8b(self.path))
    with patch.object(self.platform.platform, 'machine', return_value='x86_64'):
      self.assertFalse(self.platform.is_radxa_q8b(self.path))

  def test_existing_agnos_marker_keeps_comma_precedence(self):
    try:
      with patch.object(self.platform.os.path, 'isfile', return_value=True):
        selected = importlib.reload(self.platform)
        self.assertTrue(selected.AGNOS)
        self.assertTrue(selected.COMMA_HARDWARE)
        self.assertFalse(selected.PC)
        self.assertFalse(selected.RADXA_Q8B)
    finally:
      importlib.reload(self.platform)


class TestRadxaIdentity(unittest.TestCase):
  def test_schema_preserves_old_ordinals_and_round_trips_q8b(self):
    expected = {'unknown': 0, 'neo': 1, 'chffrAndroid': 2, 'chffrIos': 3,
                'tici': 4, 'pc': 5, 'tizi': 6, 'mici': 7, 'radxaQ8b': 8}
    self.assertEqual(log.InitData.DeviceType.schema.enumerants, expected)
    for field in ('deviceState', 'initData'):
      event = log.Event.new_message()
      event.init(field).deviceType = 'radxaQ8b'
      with log.Event.from_bytes(event.to_bytes()) as decoded:
        self.assertEqual(str(getattr(decoded, field).deviceType), 'radxaQ8b')

  def test_radxa_backend_keeps_generic_hardware_operations(self):
    module = importlib.import_module('openpilot.common.hardware.radxa.hardware')
    hardware = module.HardwareRadxa()
    self.assertEqual(hardware.get_device_type(), 'radxaQ8b')
    self.assertEqual(hardware.get_name(), 'Radxa Dragon Q8B')
    with patch.object(module.platform, 'freedesktop_os_release', return_value={'PRETTY_NAME': 'Ubuntu fixture'}):
      self.assertEqual(hardware.get_os_version(), 'Ubuntu fixture')
    self.assertEqual(hardware.get_current_power_draw(), 0)
    self.assertEqual(hardware.get_thermal_config().get_msg(), {})
    self.assertIsNone(hardware.initialize_hardware())

  def test_os_description_falls_back_without_os_release(self):
    module = importlib.import_module('openpilot.common.hardware.radxa.hardware')
    with patch.object(module.platform, 'freedesktop_os_release', side_effect=OSError), \
         patch.object(module.platform, 'system', return_value='Linux'):
      self.assertEqual(module.HardwareRadxa().get_os_version(), 'Linux')

  def test_factory_selects_radxa_without_changing_pc_policy(self):
    platform = importlib.import_module('openpilot.common.platform')
    hardware = importlib.import_module('openpilot.common.hardware')
    try:
      with patch.object(platform, 'RADXA_Q8B', True), patch.object(platform, 'COMMA_HARDWARE', False), patch.object(platform, 'PC', True):
        hardware = importlib.reload(hardware)
        self.assertEqual(hardware.HARDWARE.get_device_type(), 'radxaQ8b')
        self.assertTrue(hardware.PC)
        self.assertFalse(hardware.COMMA_HARDWARE)
      with patch.object(platform, 'RADXA_Q8B', False), patch.object(platform, 'COMMA_HARDWARE', False), patch.object(platform, 'PC', True):
        hardware = importlib.reload(hardware)
        self.assertEqual(hardware.HARDWARE.get_device_type(), 'pc')
    finally:
      importlib.reload(hardware)

  def test_unknown_camera_is_explicitly_unconfigured(self):
    camera = importlib.import_module('openpilot.common.transformations.camera')
    config = camera.DEVICE_CAMERAS['radxaQ8b', 'unknown']
    self.assertEqual(list(config.all_cams()), [])
    for sensor in ('unknown', 'ox03c10', 'os04c10'):
      with self.subTest(sensor=sensor), self.assertRaisesRegex(ValueError, 'Radxa Dragon Q8B.*calibration'):
        camera.get_device_camera_config('radxaQ8b', sensor)
    self.assertIs(camera.get_device_camera_config('pc', 'unknown'), camera.DEVICE_CAMERAS['pc', 'unknown'])
    self.assertIs(camera.get_device_camera_config('mici', 'os04c10'), camera.DEVICE_CAMERAS['mici', 'os04c10'])

  def test_explicit_camera_configuration_can_be_registered_later(self):
    camera = importlib.import_module('openpilot.common.transformations.camera')
    # A test-only fixture, not a claimed calibration for a physical Q8B camera.
    config = camera.DeviceCameraConfig(camera.CameraConfig(2, 2, 1), camera._NoneCameraConfig(), camera._NoneCameraConfig())
    with patch.dict(camera.DEVICE_CAMERAS, {('radxaQ8b', 'fixture'): config}):
      self.assertIs(camera.get_device_camera_config('radxaQ8b', 'fixture'), config)


if __name__ == '__main__':
  unittest.main()
