"""First-display camera timing for the isolated preview; no GPU synchronization."""
import json
import math
import time

import numpy as np


class CameraUiBenchmark:
  def __init__(self, start_ns: int, warmup_seconds: float):
    if not math.isfinite(warmup_seconds) or warmup_seconds < 0:
      raise ValueError('Warmup must be finite and nonnegative')
    self.start_ns = start_ns
    self.warmup_ns = int(warmup_seconds * 1e9)
    self.rows = []
    self.repeated_ui_frames = 0

  def record(self, frame_id: int, capture_ns: int, draw_ready_ns: int, frame_complete_ns: int):
    if not 0 < capture_ns <= draw_ready_ns <= frame_complete_ns:
      raise ValueError('Invalid camera/render timestamp order')
    if self.rows:
      previous = self.rows[-1]
      if frame_id == previous['frame_id']:
        if capture_ns != previous['capture_ns']:
          raise ValueError('Repeated frame has different capture metadata')
        self.repeated_ui_frames += 1
        return
      if (frame_id < previous['frame_id'] or capture_ns <= previous['capture_ns'] or
          frame_complete_ns <= previous['frame_complete_ns']):
        raise ValueError('Camera frame or timestamps went backwards')
    self.rows.append({'frame_id': frame_id, 'capture_ns': capture_ns, 'draw_ready_ns': draw_ready_ns,
                      'frame_complete_ns': frame_complete_ns,
                      'warmup': frame_complete_ns < self.start_ns + self.warmup_ns})

  def summary(self, elapsed_seconds: float, requested_seconds: float):
    rows = [r for r in self.rows if not r['warmup']]

    def stats(end, start):
      if not rows:
        return None
      values = np.array([(r[end] - r[start]) / 1e6 for r in rows])
      return {**dict(zip(['median', 'p95', 'p99'], np.percentile(values, [50, 95, 99]).tolist(), strict=True)),
              'mean': float(values.mean()), 'min': float(values.min()), 'max': float(values.max())}

    return {'status': 'complete' if elapsed_seconds >= requested_seconds and len(rows) >= 2 else 'incomplete',
            'samples': len(rows), 'warmup_samples': len(self.rows) - len(rows),
            'warmup_seconds': self.warmup_ns / 1e9, 'elapsed_seconds': elapsed_seconds,
            'requested_seconds': requested_seconds, 'repeated_ui_frames': self.repeated_ui_frames,
            'skipped_publication_ids': rows[-1]['frame_id'] - rows[0]['frame_id'] + 1 - len(rows) if rows else 0,
            'displayed_unique_fps': (len(rows) - 1) * 1e9 / (rows[-1]['frame_complete_ns'] - rows[0]['frame_complete_ns'])
              if len(rows) >= 2 else None,
            'capture_to_draw_ready_ms': stats('draw_ready_ns', 'capture_ns'),
            'capture_to_frame_complete_ms': stats('frame_complete_ns', 'capture_ns'),
            'end_drawing_ms': stats('frame_complete_ns', 'draw_ready_ns'),
            'quantile_method': 'numpy percentile linear',
            'endpoint': 'host Raylib EndDrawing return, including its normal frame pacing; not optical presentation',
            'capture_clock': 'V4L2 driver monotonic timestamp carried by VisionIPC'}

  def write(self, directory, elapsed_seconds, requested_seconds, metadata):
    with (directory / 'timings.jsonl').open('w') as stream:
      for row in self.rows:
        stream.write(json.dumps(row) + '\n')
    result = {**self.summary(elapsed_seconds, requested_seconds), 'environment': metadata}
    (directory / 'benchmark.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def timed_end_drawing(original, view, benchmark, clock=time.monotonic_ns):
  def measured():
    sample = None
    if view.frame is not None:
      if view.frame.frame_id != view.client.frame_id:
        raise ValueError('Displayed buffer and capture metadata have different frame IDs')
      sample = (view.client.frame_id, view.client.timestamp_sof)
    draw_ready = clock()
    original()
    completed = clock()
    if sample is not None:
      benchmark.record(*sample, draw_ready, completed)
  return measured


def graphics_metadata(rl):
  import ctypes
  import ctypes.util
  gl = ctypes.CDLL(ctypes.util.find_library('GL'))
  gl.glGetString.argtypes = [ctypes.c_uint]
  gl.glGetString.restype = ctypes.c_char_p
  result = {}
  for name, enum in [('vendor', 0x1F00), ('renderer', 0x1F01), ('version', 0x1F02)]:
    value = gl.glGetString(enum)
    result[name] = value.decode() if value else None
  return {**result, 'window_size': [rl.get_screen_width(), rl.get_screen_height()],
          'render_size': [rl.get_render_width(), rl.get_render_height()]}
