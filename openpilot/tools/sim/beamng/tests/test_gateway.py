import math
import unittest

from openpilot.tools.sim.beamng.pc.gateway import Encoder, SourceGate, Sample, encode_serial, adapter_config
from opendbc.car.retropilot.simulation import SimulationReceiver


def sample(sequence=1, sim_time=1.0, **changes):
  values = {'session': 1234, 'sequence': sequence, 'sim_time': sim_time, 'wall_time': 100.0,
                'speed': 10.0, 'angle': -12.3, 'rate': -5.0, 'rpm': 1200.0, 'ignition': 1.0,
                'throttle': 0.25, 'brake_input': 0.1, 'brake': 0.3, 'gear': 3.0,
                'accel_x': 1.2, 'accel_y': -2.3, 'accel_z': 0.0,
                'gyro_x': 0.1, 'gyro_y': -0.2, 'gyro_z': 0.3,
                'wheel_fl': 10.0, 'wheel_fr': 10.5, 'wheel_rl': 9.5, 'wheel_rr': 11.0,
                'cruise_available': 1.0, 'cruise_enabled': 0.0, 'cruise_speed': 20.0,
                'buttons': 0, 'valid': 0x3fff}
  values.update(changes)
  return Sample(**values)


class TestTelemetry(unittest.TestCase):
  def setUp(self):
    self.encoder = Encoder(session=77)
    self.receiver = SimulationReceiver()

  def receive(self, frames, now=1_000_000_000):
    for address, data, bus in frames:
      self.receiver.feed(address, data, bus, now)
    return self.receiver.current(now)

  def test_independent_dbc_encoder_to_opendbc_decoder(self):
    result = self.receive(self.encoder.encode(sample()))
    self.assertIsNotNone(result)
    self.assertAlmostEqual(result['speed_mps'], 10.0)
    self.assertEqual(result['rpm'], 1200)
    self.assertAlmostEqual(result['steering_angle_deg'], -12.3)
    self.assertEqual(result['acceleration_mps2'], [1.2, -2.3, 0.0])
    self.assertEqual(result['angular_velocity_rps'], [0.1, -0.2, 0.3])
    self.assertEqual(result['wheel_speeds_mps'], [10.0, 10.5, 9.5, 11.0])
    self.assertAlmostEqual(result['brake_input'], 0.1, delta=1/255)
    self.assertAlmostEqual(result['brake_applied'], 0.3, delta=1/255)
    self.assertTrue(result['cruise']['available'])
    self.assertFalse(result['cruise']['enabled'])
    self.assertAlmostEqual(result['cruise']['set_speed_mps'], 20.0)

  def test_explicit_beamng_platform_consumes_data_and_remains_no_output(self):
    from opendbc.car import gen_empty_fingerprint, structs
    from opendbc.car.retropilot.interface import CarInterface
    from opendbc.car.retropilot.values import CAR
    cp = CarInterface.get_params(CAR.RETROPILOT_BEAMNG, gen_empty_fingerprint(), [], False, False, False)
    ci = CarInterface(cp, CarInterface.get_non_essential_params_sp(cp, CAR.RETROPILOT_BEAMNG))
    state, _ = ci.update([(1_000_000_000, self.encoder.encode(sample()))])
    self.assertAlmostEqual(state.vEgoRaw, 10.0)
    self.assertAlmostEqual(state.steeringAngleDeg, -12.3, places=4)
    self.assertAlmostEqual(state.wheelSpeeds.fr, 10.5)
    self.assertTrue(state.brakePressed)
    self.assertFalse(state.vehicleSensorsInvalid)
    self.assertTrue(state.carNotReady)
    self.assertEqual(cp.safetyConfigs[0].safetyModel, structs.CarParams.SafetyModel.noOutput)
    self.assertTrue(cp.dashcamOnly)
    state, _ = ci.update([(1_200_000_000, [])])
    self.assertTrue(state.vehicleSensorsInvalid)

  def test_only_telemetry_never_actuator_commands(self):
    addresses = {a for a, _, _ in self.encoder.encode(sample())}
    self.assertEqual(addresses, {0x50, 0x75, 0x76, 0x100, *range(0x700, 0x708)})
    self.assertFalse(addresses & {0x10e, 0x12e, 0x200, 0x20e, 0x22e, 0x300, 0x400, 0x600})

  def test_counter_wrap_session_reset_and_old_session_rejection(self):
    for index in (65534, 65535, 65536):
      result = self.receive(self.encoder.encode(sample(sequence=index, sim_time=1+(index-65534)*0.02)))
      self.assertIsNotNone(result)
      self.assertEqual(result['sequence'], index & 65535)
    old = self.encoder.encode(sample(sequence=65537, sim_time=1.06))
    self.encoder.session = 78
    self.assertIsNotNone(self.receive(self.encoder.encode(sample(sequence=1, sim_time=0.02))))
    self.assertIsNone(self.receive(old, 1_200_000_000))

  def test_command_message_cannot_enter_the_telemetry_encoder(self):
    with self.assertRaises(ValueError):
      self.encoder.message('ACTUATOR_STEERING_COMMAND', 0, {'STEER_MODE': 2})

  def test_missing_fields_remain_unavailable(self):
    result = self.receive(self.encoder.encode(sample(valid=0x3fff & ~(1 << 8 | 1 << 10 | 1 << 11))))
    self.assertIsNone(result['acceleration_mps2'])
    self.assertIsNone(result['wheel_speeds_mps'])
    self.assertIsNone(result['cruise'])
    self.assertIsNotNone(result['angular_velocity_rps'])

  def test_corrupted_truncated_and_wrong_bus_do_not_complete(self):
    for kind in ('crc', 'dlc', 'bus', 'missing'):
      receiver = SimulationReceiver()
      frames = self.encoder.encode(sample())
      for address, data, bus in frames:
        if address == 0x702:
          if kind == 'missing':
            continue
          if kind == 'crc':
            data = data[:2] + bytes([data[2] ^ 1]) + data[3:]
          if kind == 'dlc':
            data = data[:-1]
          if kind == 'bus':
            bus = 0
        receiver.feed(address, data, bus, 1_000_000_000)
      self.assertIsNone(receiver.current(1_000_000_000), kind)

  def test_bundle_timeout_duplicate_and_nonprogressing_time(self):
    frames = self.encoder.encode(sample())
    self.assertIsNotNone(self.receive(frames))
    self.assertIsNone(self.receiver.current(1_200_000_000))
    self.assertIsNone(self.receive(frames, 1_210_000_000))
    self.assertIsNone(self.receive(self.encoder.encode(sample(sequence=2)), 1_220_000_000))
    self.assertIsNotNone(self.receive(self.encoder.encode(sample(sequence=3, sim_time=1.04)), 1_240_000_000))

  def test_partial_and_mixed_cycles_not_fresh(self):
    frames1 = self.encoder.encode(sample())
    frames2 = self.encoder.encode(sample(sequence=2, sim_time=1.02))
    self.assertIsNone(self.receive(frames1[:-1]))
    self.assertIsNone(self.receive(frames2[:3] + frames1[3:]))

  def test_bad_values_are_not_clamped_or_sent(self):
    for changes in ({'speed': math.nan}, {'angle': math.inf}, {'brake': 1.1}, {'speed': -1.0}, {'angle': 4000.0}):
      with self.assertRaises(ValueError, msg=str(changes)):
        self.encoder.encode(sample(**changes))

  def test_source_gate_stale_pause_order_and_reset(self):
    gate = SourceGate()
    self.assertTrue(gate.accept(sample(), 100.0))
    self.assertFalse(gate.accept(sample(), 100.02))
    self.assertFalse(gate.accept(sample(sequence=2), 100.04))  # paused sim
    self.assertFalse(gate.accept(sample(sequence=3, sim_time=1.1), 101.0))
    self.assertTrue(gate.accept(sample(session=4321, sequence=1, sim_time=0.02), 100.0))
    self.assertFalse(gate.accept(sample(sequence=4, sim_time=1.2), 100.0))  # retired session

  def test_serial_wire_bytes_and_config(self):
    self.assertEqual(encode_serial(0x123, bytes.fromhex('112255')), bytes.fromhex('aac3230111225555'))
    with self.assertRaises(ValueError):
      encode_serial(0x200, bytes(9))
    config = adapter_config(500000)
    self.assertEqual(config[:5], bytes.fromhex('aa55120301'))
    self.assertEqual(config[13:15], bytes([0, 1]))
    self.assertEqual(config[-1], sum(config[2:-1]) & 255)


if __name__ == '__main__':
  unittest.main()
