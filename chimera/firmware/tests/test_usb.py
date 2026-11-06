# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UsbTests(unittest.TestCase):
  def test_clock_detached_core_and_ep0_with_sanitizers(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "usb_test"
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-I", str(ROOT), str(ROOT / "usb_hw.c"),
                               str(ROOT / "usb_ep0.c"), str(ROOT / "protocol.c"), str(ROOT / "tests/usb_test.c"),
                               "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())


if __name__ == "__main__":
  unittest.main()
