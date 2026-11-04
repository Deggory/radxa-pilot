#!/usr/bin/env python3
"""Read RP-SIM-1 from existing Chimera `can` publication, or JSON replay stdin."""
import argparse
import json
import sys
import time

from opendbc.car.retropilot.simulation import MAX_AGE_NS, SimulationReceiver


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--cereal', action='store_true', help='Read existing can service; does not open Chimera or change manager')
  args = parser.parse_args()
  receiver = SimulationReceiver()
  last = None

  def show(now):
    nonlocal last
    value = receiver.current(now)
    identity = None if value is None else (value['session'], value['sequence'])
    if identity != last:
      print(json.dumps({'valid': value is not None, 'telemetry': value}), flush=True)
      last = identity

  if args.cereal:
    import cereal.messaging as messaging
    sock = messaging.sub_sock('can', timeout=50)
    while True:
      event = messaging.recv_one_or_none(sock)
      now = time.monotonic_ns()
      if event is not None and event.valid and 0 <= now - event.logMonoTime <= MAX_AGE_NS:
        for frame in event.can:
          receiver.feed(frame.address, bytes(frame.dat), frame.src, now)
      show(now)
      if event is None:
        time.sleep(0.01)
  else:
    for line in sys.stdin:
      record = json.loads(line)
      now = int(record['timestamp_ns'])
      for address, data, bus in record['frames']:
        receiver.feed(address, bytes.fromhex(data), bus, now)
      show(now)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
