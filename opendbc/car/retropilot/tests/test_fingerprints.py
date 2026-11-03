import unittest
from unittest.mock import patch

from opendbc.can import CANPacker
from opendbc.car import CanData, structs
from opendbc.car.car_helpers import can_fingerprint, get_car
from opendbc.car.fingerprints import MIGRATION, all_legacy_fingerprint_cars
from opendbc.car.fw_versions import VERSIONS
from opendbc.car.retropilot import fingerprints
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.values import CAN_BUS, CAR


class TestRetroPilotIdentification(unittest.TestCase):
  def test_c2_name_is_mapped_in_shared_migration_registry(self):
    self.assertEqual(MIGRATION['RETROPILOT RETROFIT'], CAR.RETROPILOT_RETROFIT)
    self.assertEqual(fingerprints.MIGRATION['RETROPILOT RETROFIT'], CAR.RETROPILOT_RETROFIT)

  def test_no_placeholder_can_or_firmware_identification(self):
    self.assertEqual(fingerprints.FINGERPRINTS, {})
    self.assertFalse(hasattr(fingerprints, 'FW_VERSIONS'))
    self.assertNotIn(CAR.RETROPILOT_RETROFIT, all_legacy_fingerprint_cars())
    self.assertNotIn('retropilot', VERSIONS)

  def test_c2_and_modern_explicit_names_select_same_passive_interface(self):
    frame = CanData(*CANPacker('ocelot_controls').make_can_msg('STEER_ANGLE_SENSOR', CAN_BUS, {}))
    transmissions = []

    def send(frames):
      transmissions.extend(frames)
      raise RuntimeError('No transmitter in this offline test')

    for name in ('RETROPILOT RETROFIT', str(CAR.RETROPILOT_RETROFIT)):
      for use_environment in (False, True):
        with self.subTest(name=name, environment=use_environment):
          transmissions.clear()

          with patch.dict('os.environ', {'FINGERPRINT': name if use_environment else '', 'SKIP_FW_QUERY': ''}):
            ci = get_car(lambda **kwargs: [[frame]], send, lambda enabled: None, False, False,
                         fixed_fingerprint=None if use_environment else name)
          self.assertIsInstance(ci, CarInterface)
          self.assertEqual(ci.CP.carFingerprint, CAR.RETROPILOT_RETROFIT)
          self.assertEqual(ci.CP.fingerprintSource, structs.CarParams.FingerprintSource.fixed)
          self.assertTrue(ci.CP.dashcamOnly)
          self.assertEqual(ci.CP.safetyConfigs[0].safetyModel, structs.CarParams.SafetyModel.noOutput)
          self.assertEqual(ci.CP.wheelSpeedFactor, 0)
          self.assertEqual(transmissions, [])

  def test_no_global_retropilot_override(self):
    frame = CanData(*CANPacker('ocelot_controls').make_can_msg('SPEED', CAN_BUS, {}))
    with patch.dict('os.environ', {'FINGERPRINT': '', 'SKIP_FW_QUERY': '1'}):
      ci = get_car(lambda **kwargs: [[frame]], lambda frames: self.fail('Unexpected TX'),
                   lambda enabled: None, False, False, fixed_fingerprint='MOCK')
    self.assertEqual(ci.CP.carFingerprint, 'MOCK')

  def test_protocol_frames_alone_do_not_claim_automatic_identity(self):
    packer = CANPacker('ocelot_controls')
    frames = [CanData(*packer.make_can_msg(name, CAN_BUS, {}))
              for name in ('STEER_ANGLE_SENSOR', 'ENGINE', 'SPEED', 'CRUISE')]
    candidate, observed = can_fingerprint(lambda **kwargs: [frames])
    self.assertIsNone(candidate)
    self.assertEqual(observed[CAN_BUS], {0x50: 6, 0x75: 8, 0x76: 8, 0x100: 8})


if __name__ == '__main__':
  unittest.main()
