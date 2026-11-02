from types import SimpleNamespace
import unittest

from openpilot.system.camerad.webcam.benchmark import CameraUiBenchmark, timed_end_drawing


class TestCameraUiBenchmark(unittest.TestCase):
  def test_preserves_warmup_and_measures_first_completion_per_frame(self):
    bench = CameraUiBenchmark(start_ns=1_000_000_000, warmup_seconds=1)
    bench.record(1, 1_100_000_000, 1_110_000_000, 1_120_000_000)
    bench.record(2, 2_100_000_000, 2_110_000_000, 2_120_000_000)
    bench.record(2, 2_100_000_000, 2_130_000_000, 2_140_000_000)
    bench.record(4, 2_150_000_000, 2_170_000_000, 2_180_000_000)
    result = bench.summary(elapsed_seconds=2, requested_seconds=2)
    self.assertEqual(len(bench.rows), 3)
    self.assertEqual(result['status'], 'complete')
    self.assertEqual(result['samples'], 2)
    self.assertEqual(result['warmup_samples'], 1)
    self.assertEqual(result['repeated_ui_frames'], 1)
    self.assertEqual(result['skipped_publication_ids'], 1)
    self.assertEqual(result['capture_to_frame_complete_ms']['median'], 25)
    self.assertEqual(result['capture_to_frame_complete_ms']['p95'], 29.5)
    self.assertEqual(result['capture_to_frame_complete_ms']['max'], 30)
    self.assertAlmostEqual(result['displayed_unique_fps'], 1e9 / 60_000_000)

  def test_rejects_invalid_pairing_or_clock_order(self):
    for values in [(1, 0, 10, 20), (1, 30, 10, 20), (1, 5, 20, 10)]:
      with self.subTest(values=values), self.assertRaises(ValueError):
        CameraUiBenchmark(0, 0).record(*values)
    bench = CameraUiBenchmark(0, 0)
    bench.record(2, 100, 110, 120)
    for values in [(1, 130, 140, 150), (3, 99, 140, 150), (2, 101, 140, 150)]:
      with self.subTest(values=values), self.assertRaises(ValueError):
        bench.record(*values)

  def test_incomplete_run_and_missing_steady_samples_are_explicit(self):
    bench = CameraUiBenchmark(0, 5)
    bench.record(1, 100, 110, 120)
    result = bench.summary(elapsed_seconds=1, requested_seconds=65)
    self.assertEqual(result['status'], 'incomplete')
    self.assertEqual(result['samples'], 0)
    self.assertIsNone(result['capture_to_frame_complete_ms'])

  def test_hook_keeps_original_frame_metadata_across_end_drawing(self):
    bench = CameraUiBenchmark(0, 0)
    view = SimpleNamespace(frame=SimpleNamespace(frame_id=7),
                           client=SimpleNamespace(frame_id=7, timestamp_sof=100))
    calls = []

    def original():
      calls.append('end_drawing')
      view.client.frame_id = 99
      view.client.timestamp_sof = 999

    clock = iter([110, 130]).__next__
    timed_end_drawing(original, view, bench, clock)()
    self.assertEqual(calls, ['end_drawing'])
    self.assertEqual(bench.rows[0]['frame_id'], 7)
    self.assertEqual(bench.rows[0]['capture_ns'], 100)
    self.assertEqual(bench.rows[0]['frame_complete_ns'], 130)

  def test_hook_rejects_buffer_metadata_mismatch(self):
    bench = CameraUiBenchmark(0, 0)
    view = SimpleNamespace(frame=SimpleNamespace(frame_id=8),
                           client=SimpleNamespace(frame_id=7, timestamp_sof=100))
    with self.assertRaisesRegex(ValueError, 'frame'):
      timed_end_drawing(lambda: None, view, bench, lambda: 130)()


if __name__ == '__main__':
  unittest.main()
