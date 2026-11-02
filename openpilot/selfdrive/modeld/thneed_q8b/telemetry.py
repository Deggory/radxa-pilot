"""Versioned Q8B timing diagnostics on an existing reserved debug service.

All timestamps are host monotonic nanoseconds. This is diagnostic data, never
an input to driving decisions. Camera/UI timing is first-draw host submission.
"""
from collections import deque
import json
import math
from statistics import median

SERVICE = 'customReservedRawData0'


def encode_timing(producer, sequence, frame_id, capture_ns, output_ns, model_ms, inference_ms):
  return json.dumps({'type': 'q8b.modelTiming', 'version': 1, 'producer': producer, 'sequence': sequence, 'frame_id': frame_id,
                     'capture_ns': capture_ns, 'output_ns': output_ns, 'model_ms': model_ms, 'inference_ms': inference_ms},
                    allow_nan=False, separators=(',', ':')).encode()


class TimingWindow:
  """Bounded two-second medians; old samples become unavailable after one second."""
  def __init__(self):
    self.model = deque(maxlen=120)
    self.ui = deque(maxlen=120)

  def receive(self, payload, now_ns):
    try:
      if len(payload) > 4096:
        return False
      sample = json.loads(payload)
      if (not isinstance(sample, dict) or sample.get('type') != 'q8b.modelTiming' or
          type(sample.get('version')) is not int or sample['version'] != 1):
        return False
      for key in ('producer', 'sequence', 'frame_id', 'capture_ns', 'output_ns'):
        if type(sample[key]) is not int or sample[key] < (0 if key == 'frame_id' else 1):
          return False
      for key in ('model_ms', 'inference_ms'):
        if type(sample[key]) not in (float, int) or not math.isfinite(sample[key]) or not 0 <= sample[key] <= 1000:
          return False
      if not 0 < sample['capture_ns'] <= sample['output_ns'] <= now_ns or now_ns - sample['output_ns'] > 1_000_000_000:
        return False
      if sample['output_ns'] - sample['capture_ns'] > 1_000_000_000:
        return False
      if self.model:
        previous = self.model[-1]
        if sample['output_ns'] <= previous['output_ns']:
          return False
        if sample['producer'] != previous['producer']:
          self.model.clear()
        elif sample['sequence'] <= previous['sequence']:
          return False
      sample['camera_model_ms'] = (sample['output_ns'] - sample['capture_ns']) / 1e6
      self.model.append(sample)
      return True
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError):
      return False

  def camera_draw(self, frame_id, capture_ns, draw_ns):
    if not 0 < capture_ns <= draw_ns or draw_ns - capture_ns > 1_000_000_000:
      return False
    if self.ui:
      previous = self.ui[-1]
      if frame_id == previous['frame_id'] or capture_ns <= previous['capture_ns']:
        return False
    self.ui.append({'frame_id': frame_id, 'capture_ns': capture_ns, 'draw_ns': draw_ns, 'camera_ui_ms': (draw_ns - capture_ns) / 1e6})
    return True

  def snapshot(self, now_ns):
    for samples, timestamp in ((self.model, 'output_ns'), (self.ui, 'draw_ns')):
      while samples and samples[0][timestamp] < now_ns - 2_000_000_000:
        samples.popleft()
    result = {'inference_ms': None, 'model_ms': None, 'camera_model_ms': None, 'model_hz': None, 'camera_ui_ms': None}
    if self.model and 0 <= now_ns - self.model[-1]['output_ns'] <= 1_000_000_000:
      result.update({key: median(row[key] for row in self.model) for key in ('inference_ms', 'model_ms', 'camera_model_ms')})
      if len(self.model) > 1:
        first, last = self.model[0], self.model[-1]
        result['model_hz'] = (last['sequence'] - first['sequence']) * 1e9 / (last['output_ns'] - first['output_ns'])
    if self.ui and 0 <= now_ns - self.ui[-1]['draw_ns'] <= 1_000_000_000:
      result['camera_ui_ms'] = median(row['camera_ui_ms'] for row in self.ui)
    return result
