# SPDX-License-Identifier: MIT
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
# Load the pure module without pandad package startup/cereal runtime dependencies.
decode_bootstrap_identity = runpy.run_path(str(ROOT.parents[1] / 'openpilot/selfdrive/pandad/chimera_identity.py'))['decode_bootstrap_identity']
MANIFEST = b'CHMR\x01\x20\x01\x00' + bytes(12) + b'\x03\x08\x00\x00\xff\x01' + bytes(6)
VERSION = b'chimera-f413-bootstrap-v1'


class BootstrapIdentityTests(unittest.TestCase):
  def test_decodes_topology_without_operational_status(self):
    identity = decode_bootstrap_identity(MANIFEST, VERSION)
    self.assertEqual(identity.firmware_version, VERSION.decode('ascii'))
    self.assertEqual(identity.physical_bus_count, 3)
    self.assertEqual(identity.classical_payload_max, 8)
    self.assertEqual(identity.physical_interfaces, ('IGN', 'VSS', 'CPS', 'BRAKE', 'ADC1', 'ADC2', 'RELAY', 'OBDC_REQUEST', 'OBDC_IGNITION'))
    self.assertEqual(identity.operational_capabilities, 0)
    self.assertEqual(identity.active_can_layout_hash, 0)
    self.assertEqual(identity.active_health_layout_hash, 0)

  def test_every_single_byte_manifest_change_is_rejected(self):
    for offset, original in enumerate(MANIFEST):
      for value in range(256):
        if value != original:
          damaged = bytearray(MANIFEST)
          damaged[offset] = value
          with self.subTest(offset=offset, value=value), self.assertRaises(ValueError):
            decode_bootstrap_identity(bytes(damaged), VERSION)

  def test_unknown_versions_and_incomplete_or_padded_responses_rejected(self):
    for length in range(129):
      for raw, other, is_manifest in ((MANIFEST, VERSION, True), (VERSION, MANIFEST, False)):
        if length == len(raw):
          continue
        damaged = (raw + bytes(129))[:length]
        with self.subTest(length=length, manifest=is_manifest), self.assertRaises(ValueError):
          decode_bootstrap_identity(damaged, other) if is_manifest else decode_bootstrap_identity(other, damaged)
    for offset, original in enumerate(VERSION):
      for value in range(256):
        if value != original:
          damaged = bytearray(VERSION)
          damaged[offset] = value
          with self.subTest(offset=offset, value=value), self.assertRaises(ValueError):
            decode_bootstrap_identity(MANIFEST, bytes(damaged))

  def test_actual_firmware_control_replies_decode_and_health_stays_unavailable(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / 'identity_reply_test'
      result = subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined',
                               '-I', str(ROOT), str(ROOT / 'protocol.c'), str(ROOT / 'tests/identity_reply_test.c'),
                               '-o', str(executable)], capture_output=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      self.assertEqual(result.stdout, MANIFEST + VERSION)
      identity = decode_bootstrap_identity(result.stdout[:32], result.stdout[32:])
      self.assertEqual(identity.operational_capabilities, 0)

  def test_non_wire_types_rejected(self):
    for invalid in (None, 32, '', list(MANIFEST), bytearray(MANIFEST), memoryview(MANIFEST)):
      with self.subTest(type=type(invalid).__name__):
        with self.assertRaises(TypeError):
          decode_bootstrap_identity(invalid, VERSION)
        with self.assertRaises(TypeError):
          decode_bootstrap_identity(MANIFEST, invalid)


if __name__ == '__main__':
  unittest.main()
