import struct
import unittest

from opendbc.can import CANPacker
from opendbc.car import gen_empty_fingerprint
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.values import CAR
from openpilot.selfdrive.pandad import can_capnp_to_list
from openpilot.selfdrive.pandad.chimera_protocol import decode_health, decode_mailboxes, can_event_bytes


def mailbox(address, data, bus=2, *, extended=False, remote=False, returned=False, bus_time=0):
  rir = (address << (3 if extended else 21)) | (4 if extended else 0) | (2 if remote else 0)
  rdtr = len(data) | ((bus | (128 if returned else 0)) << 4) | (bus_time << 16)
  return struct.pack('<II8s', rir, rdtr, data)


class TestChimeraProtocol(unittest.TestCase):
  def test_standard_extended_zero_length_and_metadata(self):
    raw = mailbox(0x301, b'\x01\x02', bus_time=0x1234) + mailbox(0x18ff0101, b'', 0, extended=True)
    frames = decode_mailboxes(raw)
    self.assertEqual((frames[0].address, frames[0].data, frames[0].bus, frames[0].bus_time), (0x301, b'\x01\x02', 2, 0x1234))
    self.assertTrue(frames[1].extended)
    self.assertEqual(frames[1].address, 0x18ff0101)
    self.assertEqual(frames[1].data, b'')

  def test_literal_mailbox_and_historical_board_health_vectors(self):
    # STM32 register layout, independent of the test mailbox constructor.
    frame = decode_mailboxes(bytes.fromhex('00002060260000000102030405060000'))[0]
    self.assertEqual((frame.address, frame.bus, frame.data), (0x301, 2, bytes.fromhex('010203040506')))
    # Actual receive-only Chimera probe, 2026-10-17. Historical observation only.
    raw = bytes.fromhex('f96f0000000000000000000000000000000000000000000000000000000000000000000000001100000000')
    health = decode_health(raw)
    self.assertEqual(health['uptime'], 28665)
    self.assertEqual(health['safety_model_raw'], 17)
    self.assertEqual(health['controls_allowed'], 0)

  def test_malformed_batch_is_rejected_as_a_whole(self):
    valid = mailbox(0x50, b'123456')
    bad = [valid[:-1], valid + b'\x00', mailbox(1, b'123456789'), mailbox(1, b'', bus=4),
           struct.pack('<II8s', (0x50 << 21) | 8, 0, b''), struct.pack('<II8s', 0, 0x1000, b'')]
    for raw in bad:
      with self.subTest(raw=raw.hex()), self.assertRaises(ValueError):
        decode_mailboxes(raw)

  def test_returned_and_remote_records_cannot_be_vehicle_reception(self):
    raw = mailbox(0x50, b'123456', returned=True) + mailbox(0x50, b'123456', remote=True)
    frames = decode_mailboxes(raw)
    self.assertTrue(frames[0].returned)
    self.assertTrue(frames[1].remote)
    packets = can_capnp_to_list([can_event_bytes(frames, 1_000_000_000)])
    self.assertEqual(packets, [(1_000_000_000, [])])

  def test_health_is_exact_legacy_layout_and_raw_safety(self):
    raw = struct.pack('<8I7Bh2B', *range(8), 1, 0, 1, 0, 2, 3, 17, -3, 4, 1)
    health = decode_health(raw)
    self.assertEqual(len(raw), 43)
    self.assertEqual(health['ignition_line'], 1)
    self.assertEqual(health['controls_allowed'], 1)
    self.assertEqual(health['safety_model_raw'], 17)
    self.assertEqual(health['safety_param_raw'], -3)
    for size in (0, 42, 44, 49, 50):
      with self.assertRaises(ValueError):
        decode_health(bytes(size))

  def test_real_cereal_to_carstate_keeps_bus_and_enabled_angle(self):
    packer = CANPacker('ocelot_controls')
    signals = {'STEER_ANGLE_SENSOR': {'STATE': 1, 'STEER_ANGLE': -12.3}, 'ENGINE': {'IGNITION_ON': 1},
               'SPEED': {'CAN_SPEED': 36}, 'CRUISE': {}}
    raw = b''.join(mailbox(address, data, bus) for address, data, bus in
                   (packer.make_can_msg(name, 2, values) for name, values in signals.items()))
    packets = can_capnp_to_list([can_event_bytes(decode_mailboxes(raw), 1_000_000_000)])
    cp = CarInterface.get_params(CAR.RETROPILOT_RETROFIT, gen_empty_fingerprint(), [], False, False, False)
    cp.wheelSpeedFactor = 1
    ci = CarInterface(cp, CarInterface.get_non_essential_params_sp(cp, CAR.RETROPILOT_RETROFIT))
    state, _ = ci.update(packets)
    self.assertTrue(state.canValid)
    self.assertFalse(state.vehicleSensorsInvalid)
    self.assertAlmostEqual(state.vEgoRaw, 10)
    self.assertAlmostEqual(state.steeringAngleDeg, -12.3, places=4)
    self.assertTrue(state.carNotReady)


if __name__ == '__main__':
  unittest.main()
