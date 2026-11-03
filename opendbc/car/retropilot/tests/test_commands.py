import unittest

from opendbc.can import CANPacker
from opendbc.car.retropilot import commands


class TestCommands(unittest.TestCase):
  def setUp(self):
    self.packer = CANPacker('ocelot_controls')

  def test_interceptor_exact_layout_and_disabled_neutral(self):
    address, data, bus = commands.steering_interceptor(self.packer, 2, True, 1600, 1420, 5)
    self.assertEqual((address, bus), (0x300, 2))
    self.assertEqual(data[1:].hex(), '40068c0585')
    self.assertEqual(commands.steering_interceptor(self.packer, 2, False, 1600, 1420, 5)[1][1:].hex(), '0000000005')

  def test_actuator_torque_and_angle_have_canonical_scales(self):
    address, data, bus = commands.steering_actuator(self.packer, 2, 1, 7.5, -12.3, 7)
    self.assertEqual((address, bus), (0x12E, 2))
    self.assertEqual(data[1:].hex(), '1785ff0f00')
    self.assertEqual(commands.steering_actuator(self.packer, 2, 0, 7.5, -12.3, 7)[1][1:].hex(), '0700000000')

  def test_gas_endpoint_families_are_explicit(self):
    for actuator, address in ((False, 0x200), (True, 0x400)):
      msg = commands.gas(self.packer, 2, True, 500, 700, 15, actuator=actuator)
      self.assertEqual(msg[0], address)
      self.assertEqual(msg[1][1:].hex(), 'f401bc028f')
      self.assertEqual(commands.gas(self.packer, 2, False, 500, 700, 15, actuator=actuator)[1][1:].hex(), '000000000f')

  def test_ssc_is_a_distinct_command_family(self):
    msg = commands.steering_ssc(self.packer, 2, 2, 2.0, -8.0, 4)
    self.assertEqual(msg[0], 0x22E)
    self.assertEqual(len(msg[1]), 5)
    self.assertEqual(msg[1][1:].hex(), '24c0ff10')
    self.assertEqual(commands.steering_ssc(self.packer, 2, 0, 2.0, -8.0, 4)[1][1:].hex(), '04000000')

  def test_brake_offsets_and_family(self):
    for ibooster, address in ((False, 0x10E), (True, 0x20E)):
      msg = commands.brake(self.packer, 2, 2, 2.5, 0, 8, ibooster=ibooster)
      self.assertEqual(msg[0], address)
      self.assertEqual(msg[1][1:].hex(), '28007ee001')

  def test_relay_layout(self):
    msg = commands.relay(self.packer, 2, True, 0x1234, 0)
    self.assertEqual(msg[0], 0x600)
    self.assertEqual(msg[1][1:].hex(), '341280')

  def test_invalid_inputs_cannot_wrap_or_encode(self):
    for enabled in (float('nan'), 1, 'false'):
      with self.assertRaises(ValueError):
        commands.steering_interceptor(self.packer, 2, enabled, 1500, 1500, 0)
    for value in (float('nan'), float('inf'), 32768, -32769):
      with self.subTest(value=value), self.assertRaises(ValueError):
        commands.steering_interceptor(self.packer, 2, True, value, 1500, 0)
    for counter in (-1, 16, 1.5):
      with self.assertRaises(ValueError):
        commands.steering_interceptor(self.packer, 2, True, 1500, 1500, counter)
    for bus in (-1, 4, 1.5):
      with self.assertRaises(ValueError):
        commands.steering_interceptor(self.packer, bus, True, 1500, 1500, 0)
    with self.assertRaises(ValueError):
      commands.brake(self.packer, 2, 3, 2.5, 0, 0)


if __name__ == '__main__':
  unittest.main()
