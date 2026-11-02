import json
import unittest
from unittest.mock import Mock, patch

from openpilot.selfdrive.modeld.thneed_q8b.telemetry import encode_timing, TimingWindow


class TestTimingTelemetry(unittest.TestCase):
  def packet(self, sequence=1, frame=7, capture=1_000_000_000, output=1_035_000_000, producer=123):
    return encode_timing(producer, sequence, frame, capture, output, 14., 11.)

  def test_source_endpoints_sequence_rate_and_staleness(self):
    window = TimingWindow()
    self.assertTrue(window.receive(self.packet(), 1_040_000_000))
    # Publication IDs can jump; rate must use actual inference sequence, not camera frame gaps.
    self.assertTrue(window.receive(self.packet(sequence=2, frame=10, capture=1_050_000_000, output=1_085_000_000), 1_090_000_000))
    stats = window.snapshot(1_090_000_000)
    self.assertEqual((stats['inference_ms'], stats['model_ms'], stats['camera_model_ms'], stats['model_hz']), (11., 14., 35., 20.))
    self.assertIsNone(window.snapshot(3_000_000_000)['inference_ms'])
    self.assertFalse(window.receive(self.packet(), 3_000_000_000))

  def test_first_draw_ignores_redraws_and_matches_frame_metadata(self):
    window = TimingWindow()
    self.assertTrue(window.camera_draw(1, 1_000_000_000, 1_040_000_000))
    self.assertFalse(window.camera_draw(1, 1_000_000_000, 1_080_000_000))
    self.assertEqual(window.snapshot(1_080_000_000)['camera_ui_ms'], 40.)
    self.assertFalse(window.camera_draw(2, 2_000_000_000, 1_090_000_000))
    self.assertIsNone(window.snapshot(3_000_000_000)['camera_ui_ms'])

  def test_publisher_counts_actual_inferences_and_diagnostic_failure_is_isolated(self):
    from openpilot.selfdrive.modeld.thneed_q8b.telemetry import ModelTimingPublisher, SERVICE
    pm = Mock()
    with patch('openpilot.cereal.messaging.PubMaster', return_value=pm):
      publisher = ModelTimingPublisher()
    publisher.record(10, 1_000_000_000, 1_035_000_000, 14., {'inference_readback_ms': 11.})
    publisher.record(99, 1_050_000_000, 1_085_000_000, 14., {'inference_readback_ms': 11.})
    channel, message = pm.send.call_args.args
    self.assertEqual(channel, SERVICE)
    packet = json.loads(bytes(message.customReservedRawData0))
    self.assertEqual((packet['sequence'], packet['frame_id']), (2, 99))
    pm.send.side_effect = RuntimeError('debug channel failed')
    with patch('openpilot.common.swaglog.cloudlog.exception'):
      publisher.record(100, 1_100_000_000, 1_135_000_000, 14., {'inference_readback_ms': 11.})
    self.assertIsNone(publisher.pm)
    publisher.record(101, 1_150_000_000, 1_185_000_000, 14., {})
    self.assertEqual(pm.send.call_count, 3)

  def test_bad_packets_and_restart_do_not_leave_false_live_values(self):
    window = TimingWindow()
    for payload in (b'bad json', b'[]', b'x' * 4097, b'[' * 2000, b'{"type":"unrelated"}'):
      self.assertFalse(window.receive(payload, 1_040_000_000))
    packet = json.loads(self.packet())
    for update in ({'inference_ms': float('nan')}, {'capture_ns': -1}, {'sequence': True}, {'sequence': 10**300}, {'version': 2}):
      self.assertFalse(window.receive(json.dumps({**packet, **update}).encode(), 1_040_000_000))
    window.receive(self.packet(), 1_040_000_000)
    self.assertTrue(window.receive(self.packet(producer=124, output=1_085_000_000, capture=1_050_000_000), 1_090_000_000))
    self.assertIsNone(window.snapshot(1_090_000_000)['model_hz'])


if __name__ == '__main__':
  unittest.main()
