"""Offline native/Python mailbox16 and health43 interoperability vectors."""
from pathlib import Path
import subprocess
import unittest

from openpilot.common.basedir import BASEDIR
from openpilot.selfdrive.pandad.chimera_protocol import decode_health, decode_mailboxes


class TestNativeChimeraParity(unittest.TestCase):
  def test_native_vectors_match_python(self):
    binary = Path(BASEDIR) / 'openpilot/selfdrive/pandad/tests/test_chimera_usb'
    output = subprocess.check_output([str(binary), '--vectors'], text=True)
    mailboxes = health_reports = 0
    for line in output.splitlines():
      kind, raw_hex, native = line.split('|')
      raw = bytes.fromhex(raw_hex)
      if kind == 'M':
        frames = [f for f in decode_mailboxes(raw) if not f.returned and not f.remote]
        expected = '' if not frames else f'{frames[0].address},{frames[0].bus},{int(frames[0].extended)},{frames[0].data.hex()}'
        self.assertEqual(native, expected, raw_hex)
        mailboxes += 1
      else:
        self.assertEqual(kind, 'H')
        self.assertEqual([int(v) for v in native.split(',')], list(decode_health(raw).values()))
        health_reports += 1
    self.assertEqual(mailboxes, 432)
    self.assertEqual(health_reports, 5)


if __name__ == '__main__':
  unittest.main()
