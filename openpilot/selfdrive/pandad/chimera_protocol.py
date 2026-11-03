"""Chimera mailbox16/health43 receive contract, distinct from Panda CAN5/CAN6.

Sources: Ocelot chimera/main.c:get_health_pkt/usb_cb_ep1_in and can.h:can_rx,
plus the retained 2026-10-17 receive probe. See docs/RETROPILOT.md for pins.
No encoders or Panda safety-mode translation are supplied by this module.
"""
import struct
from dataclasses import dataclass

from openpilot.cereal import log


MAILBOX = struct.Struct('<II8s')
HEALTH = struct.Struct('<8I7Bh2B')
HEALTH_FIELDS = (
  'uptime', 'voltage', 'current', 'can_rx_errs', 'can_send_errs', 'can_fwd_errs', 'gmlan_send_errs', 'faults',
  'ignition_line', 'ignition_can', 'controls_allowed', 'gas_interceptor_detected', 'car_harness_status',
  'usb_power_mode', 'safety_model_raw', 'safety_param_raw', 'fault_status', 'power_save_enabled',
)


@dataclass(frozen=True)
class ChimeraFrame:
  address: int
  data: bytes
  bus: int
  extended: bool
  remote: bool
  returned: bool
  bus_time: int  # Firmware timer, NOT a calibrated host/ECU sample timestamp


def decode_mailboxes(raw: bytes) -> list[ChimeraFrame]:
  if len(raw) % MAILBOX.size:
    raise ValueError('Incomplete Chimera 16-byte mailbox transfer')
  frames = []
  for rir, rdtr, payload in MAILBOX.iter_unpack(raw):
    extended = bool(rir & 4)
    address = rir >> (3 if extended else 21)
    size = rdtr & 15
    src = (rdtr >> 4) & 255
    if size > 8 or src & 127 > 3 or rdtr & 0xf000 or not extended and rir & 0x1ffff8:
      raise ValueError('Malformed classical CAN mailbox, bus or reserved bits')
    frames.append(ChimeraFrame(address, payload[:size], src & 127, extended, bool(rir & 2), bool(src & 128), rdtr >> 16))
  return frames


def decode_health(raw: bytes) -> dict[str, int]:
  if len(raw) != HEALTH.size:
    raise ValueError(f'Expected Chimera health43, received {len(raw)} bytes; do not reinterpret as Panda health')
  # Preserve reported fields, including the unqualified raw safety number.
  return dict(zip(HEALTH_FIELDS, HEALTH.unpack(raw), strict=True))


def can_event_bytes(frames: list[ChimeraFrame], timestamp_nanos: int, *, valid: bool = True) -> bytes:
  if type(timestamp_nanos) is not int or timestamp_nanos <= 0:
    raise ValueError('Host monotonic receive timestamp must be a positive integer')
  received = [frame for frame in frames if not frame.returned and not frame.remote]
  event = log.Event.new_message(logMonoTime=timestamp_nanos, valid=valid)
  can = event.init('can', len(received))
  for message, frame in zip(can, received, strict=True):
    message.address = frame.address
    message.dat = frame.data
    message.src = frame.bus
  return event.to_bytes()
