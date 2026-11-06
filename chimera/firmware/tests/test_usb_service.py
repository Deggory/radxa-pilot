# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UsbServiceTests(unittest.TestCase):
  def test_real_component_pipeline_with_register_faults(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "usb_service_test"
      sources = ["usb_service.c", "boot_facts.c", "usb_time.c", "usb_hw.c", "usb_driver.c", "usb_ep0.c", "protocol.c"]
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-I", str(ROOT), *(str(ROOT / s) for s in sources),
                               str(ROOT / "tests/usb_service_test.c"), "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())
