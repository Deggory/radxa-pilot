"""Optional bench timer at model completion, independent of UI polling/drawing."""
import atexit
import json
import math
import os
from pathlib import Path


class ModelTimingRecorder:
  def __init__(self, path):
    if not os.getenv('OPENPILOT_PREFIX', '').startswith('q8b_preview_'):
      raise ValueError('Model timing capture requires an isolated Q8B preview namespace')
    self.stream = Path(path).open('x')
    atexit.register(self.close)

  def record(self, frame_id, capture_ns, output_ns, full_model_call_ms, stages):
    if capture_ns <= 0 or output_ns < capture_ns or not math.isfinite(full_model_call_ms) or full_model_call_ms < 0:
      raise ValueError('Invalid model benchmark timestamps/duration')
    self.stream.write(json.dumps({'frame_id': frame_id, 'capture_ns': capture_ns, 'output_ns': output_ns,
                                  'camera_to_output_ms': (output_ns - capture_ns) / 1e6,
                                  'full_model_call_ms': full_model_call_ms, 'stages': stages}, allow_nan=False) + '\n')

  def close(self):
    self.stream.close()
    atexit.unregister(self.close)
