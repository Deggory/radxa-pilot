import unittest
from unittest.mock import patch

from opendbc.can import CANPacker
from opendbc.car import Bus, CanData, gen_empty_fingerprint, structs
from opendbc.car.car_helpers import get_car, interfaces
from opendbc.car.fingerprints import all_legacy_fingerprint_cars
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.values import CAN_BUS, CAR, RetroPilotFlags


def make_interface(fingerprint=None, speed_factor=0.0):
  cp = CarInterface.get_params(CAR.RETROPILOT_RETROFIT, fingerprint or gen_empty_fingerprint(), [], False, False, False)
  cp.wheelSpeedFactor = speed_factor
  cp_sp = CarInterface.get_non_essential_params_sp(cp, CAR.RETROPILOT_RETROFIT)
  return CarInterface(cp, cp_sp)


class TestRetroPilot(unittest.TestCase):
  def setUp(self):
    self.packer = CANPacker('ocelot_controls')
    self.ci = make_interface(speed_factor=1.0)
    self.t = 1_000_000_000

  def update(self, changes=None, bus=CAN_BUS, omit=()):
    values = {'STEER_ANGLE_SENSOR': {'STEER_ANGLE': -12.3, 'STEER_RATE': 4},
              'SPEED': {'CAN_SPEED': 36}, 'ENGINE': {'IGNITION_ON': 1}, 'CRUISE': {}}
    for name, signals in (changes or {}).items():
      values.setdefault(name, {}).update(signals)
    frames = [self.packer.make_can_msg(name, bus, signals) for name, signals in values.items() if name not in omit]
    self.t += 50_000_000
    return self.ci.update([(self.t, frames)])[0]

  def test_registered_explicit_passive_platform(self):
    self.assertIs(interfaces[CAR.RETROPILOT_RETROFIT], CarInterface)
    cp = self.ci.CP
    self.assertEqual(cp.brand, 'retropilot')
    self.assertTrue(cp.dashcamOnly)
    self.assertFalse(cp.openpilotLongitudinalControl)
    self.assertFalse(cp.pcmCruise)
    self.assertEqual(cp.safetyConfigs[0].safetyModel, structs.CarParams.SafetyModel.noOutput)
    self.assertEqual(cp.flags, 0)
    self.assertNotIn(CAR.RETROPILOT_RETROFIT, all_legacy_fingerprint_cars())

  def test_normal_selection_does_not_send_diagnostic_queries(self):
    frame = CanData(*self.packer.make_can_msg('STEER_ANGLE_SENSOR', CAN_BUS, {}))
    transmissions = []

    def receive(wait_for_one=False):
      return [[frame]]

    def send(frames):
      transmissions.extend(frames)
      # Existing query code catches transport errors; assert the calls afterwards.
      raise RuntimeError('No CAN transmitter in this test')

    with patch.dict('os.environ', {'SKIP_FW_QUERY': ''}):
      ci = get_car(receive, send, lambda enabled: None, False, False, fixed_fingerprint=str(CAR.RETROPILOT_RETROFIT))
    self.assertIsInstance(ci, CarInterface)
    self.assertEqual(ci.CP.fingerprintSource, structs.CarParams.FingerprintSource.fixed)
    self.assertEqual(transmissions, [])

  def test_real_state_and_no_invented_wheels_or_gear(self):
    state = self.update({'ENGINE': {'BRAKE_PRESSED': 1}})
    self.assertTrue(state.canValid)
    self.assertAlmostEqual(state.vEgoRaw, 10.0)
    self.assertAlmostEqual(state.steeringAngleDeg, -12.3, delta=1e-5)  # Cereal Float32
    # Canonical rate is unsigned magnitude; it cannot populate signed rate.
    self.assertEqual(state.steeringRateDeg, 0)
    self.assertEqual(self.ci.can_parsers[Bus.main].vl['STEER_ANGLE_SENSOR']['STEER_RATE'], 4)
    self.assertTrue(state.brakePressed)
    self.assertEqual(state.gearShifter, structs.CarState.GearShifter.unknown)
    self.assertEqual(sum(state.wheelSpeeds.to_dict().values()), 0)
    self.assertTrue(state.carNotReady)

  def test_speed_scale_is_explicit(self):
    self.ci = make_interface()
    state = self.update()
    self.assertTrue(state.canValid)
    self.assertTrue(state.vehicleSensorsInvalid)
    self.assertEqual(state.vEgoRaw, 0)
    self.ci = make_interface(speed_factor=0.01)
    self.assertAlmostEqual(self.update({'SPEED': {'CAN_SPEED': 3600}}).vEgoRaw, 10.0)

  def test_wrong_bus_and_missing_message_do_not_become_valid(self):
    self.assertFalse(self.update(bus=(CAN_BUS + 1) % 3).canValid)
    self.assertFalse(self.update(omit=('ENGINE',)).canValid)

  def test_stale_state_and_pause_disarm(self):
    self.update()
    self.assertTrue(self.update({'CRUISE': {'ON_OFF': 1}}).cruiseState.available)
    for _ in range(6):
      self.t += 1_000_000_000
      state, _ = self.ci.update([(self.t, [])])
    self.assertFalse(state.canValid)
    self.assertTrue(state.canTimeout)
    self.assertFalse(state.cruiseState.available)
    self.assertFalse(self.update({'CRUISE': {'ON_OFF': 1}}).cruiseState.available)

  def test_buttons_are_edges_and_cruise_is_not_fake_enabled(self):
    self.update()
    state = self.update({'CRUISE': {'ON_OFF': 1}})
    self.assertTrue(state.cruiseState.available)
    self.assertEqual(len(state.buttonEvents), 1)
    self.assertTrue(state.buttonEvents[0].pressed)
    self.assertEqual(len(self.update({'CRUISE': {'ON_OFF': 1}}).buttonEvents), 0)
    state = self.update({'CRUISE': {'SET_DOWN': 1}})
    self.assertFalse(state.cruiseState.enabled)
    self.assertEqual(state.cruiseState.speed, 0)
    self.assertFalse(self.update({'CRUISE': {'CANCEL': 1}}).cruiseState.available)

  def test_brake_and_ignition_drop_disarm(self):
    for engine in ({'BRAKE_PRESSED': 1}, {'IGNITION_ON': 0}):
      self.update()
      self.update({'CRUISE': {'ON_OFF': 1}})
      self.assertFalse(self.update({'ENGINE': engine}).cruiseState.available)

  def test_malformed_dlc_is_not_decoded(self):
    self.update()
    before = self.ci.can_parsers[Bus.main].ts_nanos['SPEED']['CAN_SPEED']
    msg = self.packer.make_can_msg('SPEED', CAN_BUS, {'CAN_SPEED': 90})
    for data in (msg[1][:-1], msg[1] + b'\x00'):
      self.t += 10_000_000
      self.ci.update([(self.t, [(msg[0], data, msg[2])])])
      self.assertEqual(self.ci.can_parsers[Bus.main].ts_nanos['SPEED']['CAN_SPEED'], before)

  def test_module_detection_is_per_instance_bus_and_dlc(self):
    finger = gen_empty_fingerprint()
    finger[CAN_BUS] = {0x301: 8, 0x201: 6, 0x20F: 5}
    ci = make_interface(finger)
    self.assertTrue(ci.CP.flags & RetroPilotFlags.STEER_INTERCEPTOR)
    self.assertTrue(ci.CP.flags & RetroPilotFlags.GAS_INTERCEPTOR)
    self.assertTrue(ci.CP.flags & RetroPilotFlags.IBOOSTER)
    self.assertFalse(make_interface().CP.flags)
    finger[CAN_BUS][0x301] = 6
    self.assertFalse(make_interface(finger).CP.flags & RetroPilotFlags.STEER_INTERCEPTOR)
    finger[(CAN_BUS + 1) % 3] = {0x12F: 7}
    self.assertFalse(make_interface(finger).CP.flags & RetroPilotFlags.STEER_ACTUATOR)

  def test_apply_cannot_transmit_even_with_active_requests(self):
    for value in (0.0, 1.0, float('nan'), float('inf')):
      control = structs.CarControl(enabled=True, latActive=True, longActive=True)
      control.actuators.torque = value
      control.actuators.accel = value
      actuators, sends = self.ci.apply(control.as_reader(), structs.CarControlSP(), self.t)
      self.assertEqual(sends, [])
      self.assertEqual(actuators.torque, 0)
      self.assertEqual(actuators.accel, 0)

  def test_interceptor_override_and_fault_without_fake_torque_calibration(self):
    finger = gen_empty_fingerprint()
    finger[CAN_BUS] = {0x301: 8}
    self.ci = make_interface(finger, speed_factor=1.0)
    state = self.update({'INTERCEPTOR_STEERING_SENSOR': {'OVERRIDE': 1, 'STATE': 2, 'TRQ_1': 100}})
    self.assertTrue(state.canValid)
    self.assertTrue(state.steeringPressed)
    self.assertTrue(state.steerFaultTemporary)
    self.assertEqual(state.steeringTorque, 0)
    self.assertFalse(state.cruiseState.available)

  def test_driver_override_clears_local_armed_indicator(self):
    finger = gen_empty_fingerprint()
    finger[CAN_BUS] = {0x301: 8}
    self.ci = make_interface(finger, speed_factor=1.0)
    self.update({'INTERCEPTOR_STEERING_SENSOR': {}})
    state = self.update({'INTERCEPTOR_STEERING_SENSOR': {}, 'CRUISE': {'ON_OFF': 1}})
    self.assertTrue(state.cruiseState.available)
    state = self.update({'INTERCEPTOR_STEERING_SENSOR': {'OVERRIDE': 1}})
    self.assertFalse(state.cruiseState.available)

  def test_actuator_status_uses_canonical_physical_units(self):
    finger = gen_empty_fingerprint()
    finger[CAN_BUS] = {0x12F: 7}
    self.ci = make_interface(finger, speed_factor=1.0)
    state = self.update({'ACTUATOR_STEERING_STATUS': {'STEERING_OK': 1, 'STEERING_TORQUE_DRIVER': -8,
                                                    'STEERING_TORQUE_EPS': 16}})
    self.assertEqual(state.steeringTorque, -8)
    self.assertEqual(state.steeringTorqueEps, 16)
    self.assertFalse(state.steerFaultTemporary)

  def test_brake_status_driver_override_and_fault(self):
    for name, address in (('IBOOSTER_BRAKE_STATUS', 0x20F), ('ACTUATOR_BRAKE_STATUS', 0x10F)):
      with self.subTest(endpoint=name):
        finger = gen_empty_fingerprint()
        finger[CAN_BUS] = {address: 5}
        self.ci = make_interface(finger, speed_factor=1.0)
        state = self.update({name: {'DRIVER_BRAKE_APPLIED': 1, 'BRAKE_OK': 1}})
        self.assertTrue(state.brakePressed)
        self.assertFalse(state.accFaulted)
        state = self.update({name: {'BRAKE_OK': 0}})
        self.assertTrue(state.accFaulted)


if __name__ == '__main__':
  unittest.main()
