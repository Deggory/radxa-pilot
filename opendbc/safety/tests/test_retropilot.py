"""Compiled disabled-command policy tests; no device or vehicle access."""
import os
import random
import unittest

from opendbc.car import gen_empty_fingerprint
from opendbc.car.retropilot import commands
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.values import CAN_BUS, CAR
from opendbc.car.structs import CarParams
from opendbc.safety.tests import common
from opendbc.safety.tests.libsafety import libsafety_py


# Literal canonical wire payloads before CRC and counter insertion. Brake zero
# is offset encoded: relative=0x7e00 and position=0x0140, not all-zero bytes.
DISABLED = {
  0x10E: b'\x00\x00\x00\x7e\x40\x01',
  0x12E: bytes(6),
  0x200: bytes(6),
  0x20E: b'\x00\x00\x00\x7e\x40\x01',
  0x22E: bytes(5),
  0x300: bytes(6),
  0x400: bytes(6),
}


def checksum(payload):
  """Bitwise reference, independent of the host CRC lookup table."""
  crc = 0xFF
  for byte in payload[1:]:
    crc ^= byte
    for _ in range(8):
      crc = ((crc << 1) ^ (0x1D if crc & 0x80 else 0)) & 0xFF
  return crc ^ 0xFF


def packet(addr, data, bus=CAN_BUS):
  payload = bytearray(data)
  payload[0] = checksum(payload)
  return common.make_msg(bus, addr, dat=payload)


class TestRetroPilot(common.SafetyTest):
  SAFETY_MODEL = CarParams.SafetyModel.retropilot
  TX_MSGS = [[addr, CAN_BUS] for addr in DISABLED]
  FWD_BUS_LOOKUP = {}

  def test_mode_registration_and_schema(self):
    self.assertEqual(self.SAFETY_MODEL, 39)
    self.assertEqual(CarParams.SafetyModel.hongqi, 26)
    self.assertEqual(self.safety.set_safety_hooks(self.SAFETY_MODEL, 0), 0)
    self.assertEqual(self.safety.get_current_safety_mode(), self.SAFETY_MODEL)

  def test_car_interface_remains_passive(self):
    cp = CarInterface.get_params(CAR.RETROPILOT_RETROFIT, gen_empty_fingerprint(), [], False, False, False)
    self.assertTrue(cp.dashcamOnly)
    self.assertEqual(cp.safetyConfigs[0].safetyModel, CarParams.SafetyModel.noOutput)

  def test_disabled_commands_all_counters(self):
    for addr, data in DISABLED.items():
      counter_byte = 5 if addr in (0x200, 0x300, 0x400) else 1
      for counter in range(16):
        payload = bytearray(data)
        payload[counter_byte] |= counter
        for controls_allowed in (False, True):
          self.safety.set_controls_allowed(controls_allowed)
          self.assertTrue(self._tx(packet(addr, payload)), (addr, counter, controls_allowed))

  def test_host_disabled_encoders_match_literal_contract(self):
    packer = common.CANPackerSafety('ocelot_controls')
    frames = [commands.brake(packer, CAN_BUS, 0, 0, 0, 0),
              commands.steering_actuator(packer, CAN_BUS, 0, 0, 0, 0),
              commands.gas(packer, CAN_BUS, False, 0, 0, 0),
              commands.brake(packer, CAN_BUS, 0, 0, 0, 0, ibooster=True),
              commands.steering_ssc(packer, CAN_BUS, 0, 0, 0, 0),
              commands.steering_interceptor(packer, CAN_BUS, False, 0, 0, 0),
              commands.gas(packer, CAN_BUS, False, 0, 0, 0, actuator=True)]
    for addr, data, bus in frames:
      self.assertEqual(data[1:], DISABLED[addr][1:])
      self.assertEqual(data[0], checksum(data))
      self.assertTrue(self._tx(common.make_msg(bus, addr, dat=data)))

  def test_every_non_counter_payload_bit_is_blocked(self):
    # Includes ENABLE/mode bits, active targets and reserved bits. Recompute
    # CRC so the policy must reject the content, not merely its checksum.
    for addr, data in DISABLED.items():
      counter_byte = 5 if addr in (0x200, 0x300, 0x400) else 1
      for index in range(1, len(data)):
        for bit in range(8):
          if index == counter_byte and bit < 4:
            continue
          payload = bytearray(data)
          payload[index] ^= 1 << bit
          for controls_allowed in (False, True):
            self.safety.set_controls_allowed(controls_allowed)
            self.assertFalse(self._tx(packet(addr, payload)), (addr, index, bit))

  def test_bad_checksum(self):
    for addr, data in DISABLED.items():
      for bit in range(8):
        msg = packet(addr, data)
        msg[0].data[0] ^= 1 << bit
        self.assertFalse(self._tx(msg))

  def test_wrong_bus_and_length(self):
    for addr, data in DISABLED.items():
      for bus in range(8):
        if bus != CAN_BUS:
          self.assertFalse(self._tx(packet(addr, data, bus)))
      for length in (*range(9), 12, 16, 20, 24, 32, 48, 64):
        if length != len(data):
          # Keep otherwise canonical data and a valid CRC: payload validation
          # must not conceal a regression in dispatcher DLC enforcement.
          payload = (data + bytes(64))[:length]
          msg = packet(addr, payload) if length else common.make_msg(CAN_BUS, addr, length=0)
          self.assertFalse(self._tx(msg), (addr, length))

  def test_fd_extended_and_returned_metadata_are_blocked(self):
    for addr, data in DISABLED.items():
      for flag in ('fd', 'extended', 'returned', 'rejected'):
        msg = packet(addr, data)
        setattr(msg[0], flag, 1)
        self.assertFalse(self._tx(msg), (addr, flag))

  def test_relays_and_other_ids_are_blocked(self):
    self.safety.set_controls_allowed(True)
    for addr in (0x600, 0x601, 0x50, 0x75, 0x76, 0x100, 0x301, 0x7DF, 0x18DB33F1):
      for length in (4, 5, 6, 8):
        self.assertFalse(self._tx(packet(addr, bytes(length))))

  def test_unknown_parameters_block_all_commands(self):
    for param in (1, 2, 4, 8, 16, 32, 64, 128, 255, 256, 0x8000, 0xFFFF):
      self.assertEqual(self.safety.set_safety_hooks(self.SAFETY_MODEL, param), 0)
      self.safety.set_controls_allowed(True)
      for addr, data in DISABLED.items():
        self.assertFalse(self._tx(packet(addr, data)))
    self.safety.set_safety_hooks(self.SAFETY_MODEL, 0)
    self.assertTrue(self._tx(packet(0x300, DISABLED[0x300])))

  def test_receive_never_enables_control(self):
    for bus in range(4):
      for addr in (*DISABLED, 0x301, 0x401, 0x10F, 0x20F, 0x100, 0x600, 0x7DF):
        self.assertTrue(self._rx(common.make_msg(bus, addr)))
        self.assertFalse(self.safety.get_controls_allowed())

  def test_board_fault_blocks_even_disabled_commands(self):
    self.safety.set_relay_malfunction(True)
    for addr, data in DISABLED.items():
      self.assertFalse(self._tx(packet(addr, data)))

  def test_switching_back_to_nooutput_blocks_disabled_commands(self):
    self.safety.set_safety_hooks(CarParams.SafetyModel.noOutput, 0)
    for addr, data in DISABLED.items():
      self.assertFalse(self._tx(packet(addr, data)))

  def test_random_valid_crc_payloads_cannot_actuate(self):
    rng = random.Random(0)
    self.safety.set_controls_allowed(True)
    for addr, data in DISABLED.items():
      for _ in range(200):
        payload = bytes(rng.getrandbits(8) for _ in data)
        self.assertFalse(self._tx(packet(addr, payload)))

  def test_release_build_registers_same_restricted_policy(self):
    path = libsafety_py._build_libsafety(release=True)
    try:
      release = libsafety_py.ffi.dlopen(path)
      self.assertEqual(release.set_safety_hooks(self.SAFETY_MODEL, 0), 0)
      self.assertTrue(release.safety_tx_hook(packet(0x300, DISABLED[0x300])))
      active = bytearray(DISABLED[0x300])
      active[5] = 0x80
      self.assertFalse(release.safety_tx_hook(packet(0x300, active)))
      self.assertFalse(release.get_controls_allowed())
    finally:
      os.unlink(path)


if __name__ == '__main__':
  unittest.main()
