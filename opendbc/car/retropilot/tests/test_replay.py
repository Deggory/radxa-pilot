import io
import json
import unittest

from opendbc.can import CANPacker
from opendbc.car.retropilot.profiles import C2_REFERENCE
from opendbc.car.retropilot.replay import replay
from opendbc.car.retropilot.values import CAN_BUS


class TestReplay(unittest.TestCase):
  def rows(self, count=14, live_count=1):
    packer = CANPacker('ocelot_controls')
    signals = {'STEER_ANGLE_SENSOR': {'STATE': 1}, 'ENGINE': {'IGNITION_ON': 1}, 'SPEED': {'CAN_SPEED': 36}, 'CRUISE': {},
               'INTERCEPTOR_STEERING_SENSOR': {}, 'ACTUATOR_GAS_SENSOR': {}, 'IBOOSTER_BRAKE_STATUS': {'BRAKE_OK': 1}}
    rows = []
    for i in range(count):
      frames = [packer.make_can_msg(name, CAN_BUS, values) for name, values in signals.items()] if i < live_count else []
      rows.append({'timestamp_nanos': 1_000_000_000 + i * 10_000_000,
                   'can': [(address, data.hex(), bus) for address, data, bus in frames],
                   'control': {'enabled': True, 'latActive': True, 'longActive': True, 'actuators': {'torque': 1, 'accel': 0.5}}})
    return rows

  def evaluate(self, rows):
    destination = io.StringIO()
    replay((json.dumps(row) for row in rows), destination, C2_REFERENCE, 1.0)
    return [json.loads(line) for line in destination.getvalue().splitlines()]

  def test_real_parser_to_modern_controller_with_stale_cutoff(self):
    results = self.evaluate(self.rows())
    self.assertTrue(results[0]['lateral_active'])
    self.assertTrue(results[0]['longitudinal_active'])
    self.assertEqual(results[0]['candidate_actuators']['torqueOutputCan'], 5)
    self.assertEqual(results[0]['candidate_actuators']['gas'], 0.5)
    self.assertEqual([frame[0] for frame in results[0]['candidate_can']], [0x300, 0x400, 0x20E])
    self.assertEqual(results[11]['block_reason'], 'state_unavailable')
    self.assertEqual(results[11]['candidate_actuators']['gas'], 0)
    self.assertFalse(results[11]['longitudinal_active'])
    for result in results:
      self.assertEqual(result['actual_actuators']['torque'], 0)
      self.assertEqual(result['actual_actuators']['gas'], 0)
      self.assertEqual(result['transmitted_can'], [])

  def test_bad_crc_cannot_refresh_controller_state(self):
    rows = self.rows(live_count=14)
    for row in rows[1:]:
      for frame in row['can']:
        if frame[0] == 0x76:
          data = bytearray.fromhex(frame[1])
          data[0] ^= 1
          frame_index = row['can'].index(frame)
          row['can'][frame_index] = (frame[0], data.hex(), frame[2])
    self.assertEqual(self.evaluate(rows)[11]['block_reason'], 'state_unavailable')

  def test_bad_timestamp_reports_input_line(self):
    rows = self.rows(count=1)
    rows[0]['timestamp_nanos'] = -1
    with self.assertRaisesRegex(ValueError, 'input line 1'):
      self.evaluate(rows)


if __name__ == '__main__':
  unittest.main()
