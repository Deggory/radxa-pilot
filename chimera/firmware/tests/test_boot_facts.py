# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BootFactsTests(unittest.TestCase):
  def test_read_only_identity_and_reset_snapshot(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "boot_facts_test"
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-I", str(ROOT), str(ROOT / "boot_facts.c"),
                               str(ROOT / "usb_ep0.c"), str(ROOT / "protocol.c"),
                               str(ROOT / "tests/boot_facts_test.c"), "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())
