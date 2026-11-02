import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from openpilot.selfdrive.modeld.npu.reference_dataset import errors, save_report


class TestDiagnostics(unittest.TestCase):
  def test_failed_gate_keeps_its_report(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'report.json'
      report = {'comparisons': [{'packed': {'outside_atol_0p01_rtol_0p01': 1}}]}
      with self.assertRaises(ValueError):
        save_report(path, report)
      self.assertEqual(json.loads(path.read_text()), report)

  def test_passing_report_is_saved(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'report.json'
      report = {'comparisons': [{'packed': {'outside_atol_0p01_rtol_0p01': 0}}]}
      save_report(path, report)
      self.assertEqual(json.loads(path.read_text()), report)

  def test_nonfinite_output_is_rejected(self):
    with self.assertRaises(ValueError):
      errors(np.zeros(2), np.array([0., np.nan]))

  def test_zero_reference_has_no_relative_rms(self):
    self.assertIsNone(errors(np.zeros(2), np.ones(2))['relative_rms'])
