import unittest

from opendbc.can import CANPacker, CANParser


def reference_crc(data):
  # Independent bitwise SAE-J1850, payload bytes 1..DLC-1.
  crc = 0xFF
  for byte in data[1:]:
    crc ^= byte
    for _ in range(8):
      crc = ((crc << 1) ^ (0x1D if crc & 0x80 else 0)) & 0xFF
  return crc ^ 0xFF


class TestOcelot(unittest.TestCase):
  def test_all_canonical_messages_and_counters(self):
    packer = CANPacker('ocelot_controls')
    for msg in packer.dbc.addr_to_msg.values():
      with self.subTest(message=msg.name):
        parser = CANParser('ocelot_controls', [(msg.name, 20)], 2)
        for index in range(33):
          address, data, bus = packer.make_can_msg(msg.name, 2, {})
          self.assertEqual(len(data), msg.size)
          self.assertEqual(data[0], reference_crc(data))
          parser.update([(1_000_000_000 + index * 50_000_000, [(address, data, bus)])])
          self.assertEqual(parser.vl[msg.name]['COUNTER'], index % 16)
          self.assertTrue(parser.can_valid)

  def test_crc_covers_full_interceptor_status(self):
    packer = CANPacker('ocelot_controls')
    parser = CANParser('ocelot_controls', [('INTERCEPTOR_STEERING_SENSOR', 20)], 2)
    address, data, bus = packer.make_can_msg('INTERCEPTOR_STEERING_SENSOR', 2, {'TRQ_1': 100, 'COUNTER': 1})
    parser.update([(1_000_000_000, [(address, data, bus)])])
    before = dict(parser.vl[address])
    for offset in range(8):
      for bit in range(8):
        damaged = bytearray(data)
        damaged[offset] ^= 1 << bit
        updated = parser.update([(1_010_000_000, [(address, bytes(damaged), bus)])])
        self.assertNotIn(address, updated)
        self.assertEqual(parser.vl[address], before)

  def test_repeated_counter_becomes_invalid(self):
    packer = CANPacker('ocelot_controls')
    parser = CANParser('ocelot_controls', [('SPEED', 20)], 2)
    msg = packer.make_can_msg('SPEED', 2, {'COUNTER': 1})
    for i in range(7):
      parser.update([(1_000_000_000 + i * 10_000_000, [msg])])
    self.assertFalse(parser.can_valid)


if __name__ == '__main__':
  unittest.main()
