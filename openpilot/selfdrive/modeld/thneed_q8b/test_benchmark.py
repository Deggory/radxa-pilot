import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openpilot.selfdrive.modeld.thneed_q8b.benchmark import ModelTimingRecorder


class TestModelTimings(unittest.TestCase):
  def test_records_source_to_output_endpoint_and_distinct_stages(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'timings.jsonl'
      with patch.dict(os.environ, {'OPENPILOT_PREFIX': 'q8b_preview_test'}):
        recorder = ModelTimingRecorder(path)
      recorder.record(4, 1_000_000_000, 1_035_000_000, 15, {'inference_readback_ms': 12})
      recorder.close()
      row = json.loads(path.read_text())
      self.assertEqual(row['camera_to_output_ms'], 35)
      self.assertEqual(row['full_model_call_ms'], 15)
      self.assertEqual(row['stages']['inference_readback_ms'], 12)
      self.assertEqual(row['frame_id'], 4)
      with patch.dict(os.environ, {'OPENPILOT_PREFIX': 'q8b_preview_test'}), self.assertRaises(FileExistsError):
        ModelTimingRecorder(path)

  def test_summary_checks_frame_identity_clock_samples_and_timing_scope(self):
    from openpilot.selfdrive.modeld.thneed_q8b.bench import summarize
    rows = [{'frame_id': i, 'capture_ns': 1_000_000_000 + i * 50_000_000,
             'output_ns': 1_035_000_000 + i * 50_000_000, 'camera_to_output_ms': 35, 'full_model_call_ms': 15,
             'stages': {'cpu_prepare_ms': 2, 'input_validation_ms': .1, 'upload_ms': .1, 'inference_readback_ms': 12,
                        'performance': {'received_ns': 1, 'gpu_hz': 690000000,
                                        'cpu_khz': {'policy0': 2438400, 'policy4': 2995200}}}}
            for i in range(30)]
    result = summarize(rows, 0)
    self.assertEqual(result['output_hz'], 20)
    self.assertEqual(result['camera_to_output_ms']['median'], 35)
    self.assertTrue(result['all_clock_samples_at_tested_max'])
    self.assertEqual(len(result['clock_samples']), 1)
    rows[10]['frame_id'] = 9
    with self.assertRaisesRegex(RuntimeError, 'order'):
      summarize(rows, 0)

  def test_refuses_normal_namespace_and_invalid_timestamp(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / 'timings.jsonl'
      with patch.dict(os.environ, {'OPENPILOT_PREFIX': 'normal'}), self.assertRaises(ValueError):
        ModelTimingRecorder(path)
      self.assertFalse(path.exists())
      with patch.dict(os.environ, {'OPENPILOT_PREFIX': 'q8b_preview_test'}):
        recorder = ModelTimingRecorder(path)
      try:
        with self.assertRaises(ValueError):
          recorder.record(0, 0, 1, 0, {})
      finally:
        recorder.close()


if __name__ == '__main__':
  unittest.main()
