# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LegacySessionTests(unittest.TestCase):
  def test_explicit_legacy_session_with_real_components_and_register_faults(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "legacy_session_test"
      sources = ["main.c", "main_runtime.c", "usb_service.c", "boot_facts.c", "usb_time.c", "usb_hw.c",
                 "usb_driver.c", "usb_ep0.c", "protocol.c"]
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-DCHIMERA_MAIN_NATIVE_TEST", "-I", str(ROOT),
                               *(str(ROOT / s) for s in sources), str(ROOT / "tests/legacy_session_test.c"),
                               "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())
