"""Pinned receive-only Chimera USB monitor, optionally publishing modern CAN.

Not the stock Panda flash/recovery lifecycle. No sendcan subscription, control
OUT, bulk OUT, heartbeat, relay, bitrate or configuration write is implemented.
Health stays a raw observation; this tool does not publish pandaStates or grant
onroad readiness. See docs/RETROPILOT.md for the remaining integration work.
"""
import argparse
from contextlib import contextmanager
from dataclasses import asdict
import json
import time

import usb1

from openpilot.selfdrive.pandad.chimera_protocol import can_event_bytes, decode_health, decode_mailboxes


class ChimeraReceiver:
  def __init__(self, handle, expected_version: str):
    if not expected_version:
      raise ValueError('An explicit expected Chimera version is required')
    self.handle = handle
    self.version = bytes(handle.controlRead(0xc0, 0xd6, 0, 0, 64, timeout=1000)).decode('ascii').rstrip('\x00')
    if self.version != expected_version:
      raise ValueError(f'Chimera version mismatch: expected {expected_version!r}, observed {self.version!r}')
    self.initial_health = self.read_health()  # Reject incompatible layouts before receiving CAN.

  def read_health(self):
    return decode_health(bytes(self.handle.controlRead(0xc0, 0xd2, 0, 0, 64, timeout=1000)))

  def read_can(self):
    try:
      data = bytes(self.handle.bulkRead(0x81, 1024, timeout=10))
    except usb1.USBErrorTimeout as exc:
      # libusb1 attaches bytes actually received before its timeout. Retain full
      # records; reject an incomplete mailbox rather than carrying stale bytes.
      data = bytes(exc.received)
    return decode_mailboxes(data)


@contextmanager
def open_chimera(context, serial: str, expected_version: str):
  if not serial or not expected_version:
    raise ValueError('Explicit serial and version pins are required')
  selected = None
  for device in context.getDeviceIterator(skip_on_error=True):
    if (device.getVendorID(), device.getProductID()) != (0xbbaa, 0xddcc):
      continue  # Never open a bootstub/DFU or another VID/PID.
    handle = device.open()
    try:
      if handle.getSerialNumber() == serial and handle.getProduct() == 'Chimera':
        selected = handle
        break
    finally:
      if selected is not handle:
        handle.close()
  if selected is None:
    raise RuntimeError(f'No normal-mode Chimera with serial {serial!r}')
  claimed = False
  try:
    selected.claimInterface(0)
    claimed = True
    yield ChimeraReceiver(selected, expected_version)
  finally:
    try:
      if claimed:
        selected.releaseInterface(0)
    finally:
      selected.close()


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--serial', required=True)
  parser.add_argument('--expected-version', required=True)
  parser.add_argument('--seconds', type=float, default=5, help='Receive duration, up to60seconds')
  parser.add_argument('--publish-can', action='store_true', help='Own the modern can publisher; stop other can publishers first')
  args = parser.parse_args()
  if not args.serial or not args.expected_version or not 0 < args.seconds <= 60:
    parser.error('Nonempty serial/version and a duration in (0,60] are required')

  publisher = None
  if args.publish_can:
    import openpilot.cereal.messaging as messaging
    publisher = messaging.PubMaster(['can'])
  try:
    with usb1.USBContext() as context, open_chimera(context, args.serial, args.expected_version) as receiver:
      print(json.dumps({'event': 'connected', 'version': receiver.version, 'serial': args.serial,
                        'health_raw': receiver.initial_health, 'live_output': False}), flush=True)
      deadline = time.monotonic() + args.seconds
      next_health = time.monotonic() + 0.5
      while time.monotonic() < deadline:
        start = time.monotonic()
        frames = receiver.read_can()
        timestamp = time.monotonic_ns()
        if publisher is not None:
          publisher.send('can', can_event_bytes(frames, timestamp))
        print(json.dumps({'event': 'can', 'timestamp_nanos': timestamp,
                          'mailboxes': [dict(asdict(frame), data=frame.data.hex()) for frame in frames]}), flush=True)
        if time.monotonic() >= next_health:
          print(json.dumps({'event': 'health', 'health_raw': receiver.read_health()}), flush=True)
          next_health = time.monotonic() + 0.5
        time.sleep(max(0, 0.01 - (time.monotonic() - start)))
  finally:
    if publisher is not None:
      # End the producer session explicitly, including on unplug/malformed data.
      publisher.send('can', can_event_bytes([], time.monotonic_ns(), valid=False))


if __name__ == '__main__':
  main()
