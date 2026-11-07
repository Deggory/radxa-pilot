# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MainStartupTests(unittest.TestCase):
  def test_actual_main_preparation_with_read_only_register_backend(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "main_test"
      result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                               "-fsanitize=address,undefined", "-DCHIMERA_MAIN_NATIVE_TEST", "-I", str(ROOT),
                               str(ROOT / "main.c"), str(ROOT / "boot_facts.c"),
                               str(ROOT / "tests/main_test.c"), "-o", str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      print(result.stdout.strip())
