import unittest
from dataclasses import replace
from types import SimpleNamespace

from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.retropilot.carcontroller import CarController
from opendbc.car.retropilot.profiles import C2_REFERENCE, ControllerProfile
from opendbc.car.retropilot.tests.test_retropilot import make_interface
from opendbc.car.retropilot.values import CAN_BUS, RetroPilotFlags as F


class TestController(unittest.TestCase):
  def setUp(self):
    self.ci = make_interface(speed_factor=1.0)
    self.ci.CP.flags = int(C2_REFERENCE.modules)
    self.controller = CarController({Bus.main: 'ocelot_controls'}, self.ci.CP, self.ci.CP_SP, profile=C2_REFERENCE)
    self.cc = structs.CarControl(enabled=True, latActive=True, longActive=True)
    self.cc.actuators.torque = 1
    self.cc.actuators.accel = 0.5
    self.t = 1_000_000_000
    self.cs = SimpleNamespace(out=structs.CarState(canValid=True), control_ready=True, control_state_nanos=self.t)
    self.parser = CANParser('ocelot_controls', [('INTERCEPTOR_STEERING_COMMAND', 100), ('ACTUATOR_GAS_COMMAND', 50),
                                             ('IBOOSTER_BRAKE_COMMAND', 100)], CAN_BUS)

  def step(self, advance=10_000_000, refresh=True):
    self.t += advance
    if refresh:
      self.cs.control_state_nanos = self.t
    result = self.controller.preview(self.cc, self.cs, self.t)
    self.parser.update([(self.t, result.can_messages)])
    return result

  def test_c2_steering_migrates_to_modern_torque_and_slew(self):
    result = self.step()
    self.assertTrue(result.lateral_active)
    self.assertEqual(result.actuators.torqueOutputCan, 5)
    self.assertAlmostEqual(result.actuators.torque, 5 / 350)
    self.assertEqual(self.parser.vl['INTERCEPTOR_STEERING_COMMAND']['TORQUE_COMMAND1'], 1515)
    self.assertEqual(self.parser.vl['INTERCEPTOR_STEERING_COMMAND']['TORQUE_COMMAND2'], 1505)
    self.assertEqual(self.step().actuators.torqueOutputCan, 10)

  def test_disabled_and_lat_inactive_reset_request_and_slew(self):
    self.step()
    self.cc.latActive = False
    result = self.step()
    self.assertFalse(result.lateral_active)
    self.assertEqual(result.actuators.torque, 0)
    self.assertEqual(self.parser.vl['INTERCEPTOR_STEERING_COMMAND']['ENABLE'], 0)
    self.assertEqual(self.parser.vl['INTERCEPTOR_STEERING_COMMAND']['TORQUE_COMMAND1'], 0)
    self.cc.latActive = True
    self.assertEqual(self.step().actuators.torqueOutputCan, 5)
    self.cc.enabled = False
    self.assertEqual(self.step().actuators.torqueOutputCan, 0)

  def test_speed_taper_never_reverses_torque_above_90_ms(self):
    for speed in (90, 100):
      self.cs.out.vEgo = speed
      self.assertEqual(self.step().actuators.torqueOutputCan, 0)

  def test_missing_profile_does_not_assume_c2_calibration(self):
    self.controller = CarController({Bus.main: 'ocelot_controls'}, self.ci.CP, self.ci.CP_SP)
    result = self.step()
    self.assertEqual(result.can_messages, [])
    self.assertEqual(result.block_reason, 'calibration_missing')

  def test_profile_validation_and_endpoint_selection(self):
    self.assertIsInstance(C2_REFERENCE, ControllerProfile)
    for change in ({'steer_max': float('nan')}, {'steer_delta_up': 0}, {'gas_accel_full': 0},
                   {'steer_centers': (32767, 0)}, {'gas_gains': (70000, 0)},
                   {'modules': F.GAS_INTERCEPTOR | F.GAS_ACTUATOR}, {'modules': F.STEER_SSC}):
      with self.subTest(change=change), self.assertRaises(ValueError):
        replace(C2_REFERENCE, **change)

  def test_preview_never_becomes_live_output(self):
    # Even mutating CP cannot promote unqualified C2 calibration to CAN TX.
    self.ci.CP.dashcamOnly = False
    actual, sends = self.controller.update(self.cc, structs.CarControlSP(), self.cs, self.t)
    self.assertTrue(self.controller.last_preview.can_messages)
    self.assertEqual(actual.torque, 0)
    self.assertEqual(actual.accel, 0)
    self.assertEqual(sends, [])

  def test_pedals_have_independent_activation_and_c2_scaling(self):
    result = self.step()
    self.assertTrue(result.longitudinal_active)
    self.assertEqual(result.actuators.gas, 0.5)
    self.assertEqual(self.parser.vl['ACTUATOR_GAS_COMMAND']['THROTTLE_REQ'], 750)
    self.assertEqual(self.parser.vl['IBOOSTER_BRAKE_COMMAND']['BRAKE_POSITION_COMMAND'], 0)
    self.cc.latActive = False
    self.cc.actuators.accel = -0.5
    result = self.step()
    self.assertEqual(result.actuators.gas, 0)
    self.assertEqual(result.actuators.brake, 0.5)
    self.assertEqual(self.parser.vl['ACTUATOR_GAS_COMMAND']['ENABLE'], 0)
    self.assertEqual(self.parser.vl['IBOOSTER_BRAKE_COMMAND']['BRAKE_POSITION_COMMAND'], 3.5)
    self.cc.longActive = False
    result = self.step()
    self.assertEqual(result.actuators.brake, 0)
    self.assertEqual(self.parser.vl['IBOOSTER_BRAKE_COMMAND']['BRAKE_MODE'], 0)

  def test_schedule_counters_bus_crc_and_actual_held_pedal(self):
    seen = {}
    for i in range(40):
      result = self.step()
      self.assertEqual(len(result.can_messages), 3 if i % 2 == 0 else 2)
      for address, data, bus in result.can_messages:
        self.assertEqual(bus, CAN_BUS)
        count = (data[1] if address == 0x20E else data[5]) & 15
        self.assertEqual(count, seen.get(address, 0) % 16)
        seen[address] = seen.get(address, 0) + 1
      self.assertTrue(self.parser.can_valid)
    self.assertEqual(seen, {0x300: 40, 0x400: 20, 0x20E: 40})
    self.cc.actuators.accel = 0.75
    self.step()  # 50Hz send
    self.cc.actuators.accel = 0.25
    self.assertEqual(self.step().actuators.gas, 0.75)  # held between sends

  def test_disengage_flushes_50hz_gas_immediately(self):
    self.step()
    self.cc.enabled = False  # odd tick, normally no gas command
    result = self.step()
    self.assertIn(0x400, [msg[0] for msg in result.can_messages])
    self.assertEqual(self.parser.vl['ACTUATOR_GAS_COMMAND']['ENABLE'], 0)
    self.assertEqual(self.parser.vl['ACTUATOR_GAS_COMMAND']['THROTTLE_REQ'], 0)
    self.assertEqual(result.actuators.accel, 0)

  def test_invalid_state_request_and_timing_emit_disabled_commands(self):
    cases = [lambda: setattr(self.cs, 'control_ready', False), lambda: setattr(self.cs.out, 'canValid', False),
             lambda: setattr(self.cs.out, 'vehicleSensorsInvalid', True), lambda: setattr(self.cs.out, 'brakePressed', True),
             lambda: setattr(self.cc.actuators, 'torque', float('nan')), lambda: setattr(self.cc.actuators, 'accel', float('inf')),
             lambda: setattr(self.cc.cruiseControl, 'cancel', True), lambda: setattr(self.ci.CP, 'flags', 0)]
    for change in cases:
      self.setUp()
      self.step()
      change()
      result = self.step()
      self.assertTrue(result.block_reason)
      self.assertFalse(result.lateral_active)
      self.assertFalse(result.longitudinal_active)
      self.assertEqual(result.actuators.torqueOutputCan, 0)
      self.assertEqual(result.actuators.gas, 0)
      self.assertEqual(self.parser.vl['INTERCEPTOR_STEERING_COMMAND']['ENABLE'], 0)
    for advance in (0, -10_000_000, 60_000_000):
      self.setUp()
      self.step()
      self.assertEqual(self.step(advance).block_reason, 'control_timing')
    self.setUp()
    self.step()
    for _ in range(11):
      result = self.step(refresh=False)
    self.assertEqual(result.block_reason, 'state_unavailable')

  def test_driver_overrides_and_faults_are_per_axis(self):
    self.cs.out.steeringPressed = True
    self.assertFalse(self.step().lateral_active)
    self.assertTrue(self.step().longitudinal_active)
    self.cs.out.steeringPressed = False
    self.cs.out.gasPressed = True
    self.assertTrue(self.step().lateral_active)
    self.assertFalse(self.step().longitudinal_active)
    self.cs.out.gasPressed = False
    self.cs.out.accFaulted = True
    self.assertFalse(self.step().longitudinal_active)

  def test_alternative_c2_gas_brake_and_relay_encoders(self):
    profile = replace(C2_REFERENCE, modules=F.STEER_INTERCEPTOR | F.GAS_INTERCEPTOR | F.BRAKE_ACTUATOR | F.RELAY,
                      gas_offsets=(850, 480), gas_gains=(2400, 2000))
    self.ci.CP.flags = int(profile.modules)
    self.controller = CarController({Bus.main: 'ocelot_controls'}, self.ci.CP, self.ci.CP_SP, profile=profile)
    self.t += 10_000_000
    self.cs.control_state_nanos = self.t
    result = self.controller.preview(self.cc, self.cs, self.t, relay_bits=3)
    parser = CANParser('ocelot_controls', [('PEDAL_GAS_COMMAND', 50), ('ACTUATOR_BRAKE_COMMAND', 100), ('RELAY_CORE_COMMAND', 50)], CAN_BUS)
    parser.update([(self.t, result.can_messages)])
    self.assertEqual(parser.vl['PEDAL_GAS_COMMAND']['GAS_COMMAND'], 2050)
    self.assertEqual(parser.vl['PEDAL_GAS_COMMAND']['GAS_COMMAND2'], 1480)
    self.assertEqual(parser.vl['RELAY_CORE_COMMAND']['RELAY_COMMAND'], 3)
    self.assertEqual(parser.vl['ACTUATOR_BRAKE_COMMAND']['BRAKE_MODE'], 2)

  def test_asymmetric_slew_and_direction_change(self):
    self.controller.profile = replace(C2_REFERENCE, steer_delta_up=10, steer_delta_down=3)
    self.assertEqual(self.step().actuators.torqueOutputCan, 10)
    self.cc.actuators.torque = -1
    for expected in (7, 4, 1, 0, -10):
      self.assertEqual(self.step().actuators.torqueOutputCan, expected)


if __name__ == '__main__':
  unittest.main()
