"""Read-only diagnostics on the actual Q8B onroad camera view."""
import time

import pyray as rl

from openpilot.cereal import messaging
from openpilot.common.hardware.radxa.telemetry import HealthSampler
from openpilot.selfdrive.modeld.thneed_q8b.telemetry import SERVICE, TimingWindow
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.text_measure import measure_text_cached


def display_number(value, unit):
  return '--' if value is None else f'{value:.1f} {unit}'


def fan_text(health):
  pwm, mode = health['pwm'], health['fan_mode']
  mode_text = {0: 'FW', 1: 'MANUAL', 2: 'AUTO'}.get(mode, '--' if mode is None else f'MODE {mode}')
  rpm = health.get('fan_rpm')
  feedback = 'RPM unavailable' if rpm is None else f'{rpm} RPM'
  if pwm is None:
    return '--', f'PWM duty | {feedback}'
  return f"{health['pwm_percent']:.0f}% {mode_text}", f'{pwm}/255 | {feedback}'


class Q8bStatsPanel:
  def __init__(self):
    self.font = gui_app.font(FontWeight.MEDIUM)
    self.bold = gui_app.font(FontWeight.SEMI_BOLD)
    self.socket = messaging.sub_sock(SERVICE, conflate=True)
    self.window = TimingWindow()
    self.health = HealthSampler()
    self.next_refresh_ns = 0
    self.displayed = {}
    self.model_packets = []
    self.ui_draws = []
    self.received_packets = 0
    self.rejected_packets = 0
    self.draw_count = 0

  def render(self, rect, view):
    # No waiting, sysfs reads, disk writes or GPU fences on this rendering path.
    try:
      packet = messaging.recv_one_or_none(self.socket)
      if packet is not None:
        accepted = packet.which() == SERVICE and self.window.receive(bytes(packet.customReservedRawData0), time.monotonic_ns())
        self.received_packets += int(accepted)
        self.rejected_packets += int(not accepted)
    except Exception:
      self.rejected_packets += 1
    if view.frame is not None and view.client is not None and view.frame.frame_id == view.client.frame_id:
      if self.window.camera_draw(view.client.frame_id, view.client.timestamp_sof, time.monotonic_ns()):
        self.draw_count += 1
    now = time.monotonic_ns()
    if now >= self.next_refresh_ns:
      self.displayed = {**self.window.snapshot(now), 'health': self.health.snapshot(now), 'display_ns': now}
      self.model_packets = list(self.window.model)
      self.ui_draws = list(self.window.ui)
      self.next_refresh_ns = now + 250_000_000
    self._draw(rect)

  def _draw(self, rect):
    scale = min(1., rect.width / 1200., rect.height / 700.)
    width, height = 420 * scale, 474 * scale
    x, y = rect.x + rect.width - width - 20 * scale, rect.y + 24 * scale
    rl.draw_rectangle_rounded(rl.Rectangle(x, y, width, height), .06, 8, rl.Color(10, 18, 24, 220))
    muted = rl.Color(183, 193, 201, 255)

    def text(value, dx, dy, size=22, color=rl.WHITE, bold=False, right=False):
      font = self.bold if bold else self.font
      pos = x + dx * scale
      if right:
        pos -= measure_text_cached(font, value, size * scale).x
      rl.draw_text_ex(font, value, rl.Vector2(pos, y + dy * scale), size * scale, 0, color)

    sample, health = self.displayed, self.displayed['health']
    text('Q8B PERFORMANCE', 20, 16, 23, rl.Color(128, 216, 166, 255), bold=True)
    text('CPU max', 20, 59, 20, muted)
    text('GPU max', 228, 59, 20, muted)
    text(display_number(health['cpu_c'], '°C'), 20, 84, 32, bold=True)
    text(display_number(health['gpu_c'], '°C'), 228, 84, 32, bold=True)
    value, detail = fan_text(health)
    text('Fan PWM', 20, 136, 22, muted)
    text(value, 400, 134, 27, right=True)
    text(detail, 20, 168, 18, muted)
    for index, (label, key) in enumerate((('GPU inference', 'inference_ms'), ('Full model', 'model_ms'),
                                         ('Camera to model', 'camera_model_ms'), ('Camera to UI draw', 'camera_ui_ms'))):
      yy = 211 + index * 44
      text(label, 20, yy, 21, muted)
      text(display_number(sample[key], 'ms'), 400, yy - 2, 27, right=True)
    text('Model rate', 20, 395, 21, muted)
    text(display_number(sample['model_hz'], 'Hz'), 400, 393, 27, right=True)
    text('Timing median 2s | sensors 1Hz', 20, 430, 17, muted)
    text('UI = first draw, not display latency', 20, 448, 15, muted)

  def diagnostics(self):
    return {'displayed': self.displayed, 'model_packets': self.model_packets, 'ui_draws': self.ui_draws,
            'received_packets': self.received_packets, 'rejected_packets': self.rejected_packets, 'draw_count': self.draw_count}

  def close(self):
    self.health.close()
    self.socket = None
