# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UsbDriverTests(unittest.TestCase):
  def test_bounded_cycle_counter_backend(self):
    self.compile_run("usb_time_test", ["usb_time.c"])

  def test_polling_ep0_packet_driver(self):
    self.compile_run("usb_driver_test", ["usb_driver.c", "usb_ep0.c", "protocol.c"])

  def compile_run(self, name, sources):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / name
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-I", str(ROOT),
                               *(str(ROOT / source) for source in sources),
                               str(ROOT / "tests" / (name + ".c")), "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())
