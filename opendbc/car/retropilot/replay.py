"""JSONL CAN/control replay; stdout contains candidates, no CAN/device writes.

Each input row: {"timestamp_nanos": int, "can": [[id, "hex", bus], ...],
                 "control": {modern CarControl fields}}.
Every row advances parsing and the 100 Hz controller, including empty CAN rows.
"""
import argparse
import json
import sys

from opendbc.car import Bus, gen_empty_fingerprint, structs
from opendbc.car.retropilot.carcontroller import CarController
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.profiles import C2_REFERENCE
from opendbc.car.retropilot.values import CAN_BUS, CAR, MODULES


def replay(source, destination, profile, speed_factor):
  fingerprint = gen_empty_fingerprint()
  fingerprint[CAN_BUS] = {address: size for flag, (_, address, size) in MODULES.items() if profile.modules & flag}
  cp = CarInterface.get_params(CAR.RETROPILOT_RETROFIT, fingerprint, [], False, False, False)
  cp.wheelSpeedFactor = speed_factor
  cp_sp = CarInterface.get_non_essential_params_sp(cp, CAR.RETROPILOT_RETROFIT)
  ci = CarInterface(cp, cp_sp)
  ci.CC = CarController({Bus.main: 'ocelot_controls'}, cp, cp_sp, profile=profile)
  for line_number, line in enumerate(source, 1):
    try:
      row = json.loads(line)
      timestamp = row['timestamp_nanos']
      if type(timestamp) is not int or timestamp <= 0:
        raise ValueError('timestamp_nanos must be a positive integer')
      frames = [(address, bytes.fromhex(data), bus) for address, data, bus in row['can']]
      control = structs.CarControl(**row['control'])
      ci.update([(timestamp, frames)])
      actual, transmitted = ci.apply(control, structs.CarControlSP(), timestamp)
      preview = ci.CC.last_preview
      assert not transmitted  # No transport exists in this tool.
      json.dump({'timestamp_nanos': timestamp, 'block_reason': preview.block_reason,
                 'lateral_active': preview.lateral_active, 'longitudinal_active': preview.longitudinal_active,
                 'candidate_actuators': preview.actuators.to_dict(),
                 'candidate_can': [(address, data.hex(), bus) for address, data, bus in preview.can_messages],
                 'actual_actuators': actual.to_dict(), 'transmitted_can': transmitted}, destination, allow_nan=False)
      destination.write('\n')
    except (ValueError, KeyError, TypeError) as exc:
      raise ValueError(f'Replay input line {line_number}: {exc}') from exc


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--profile', required=True, choices=['c2-reference'], help='Unqualified historical constants; offline only')
  parser.add_argument('--speed-units', required=True, choices=['kph', 'centi-kph'], help='Units of the recorded producer')
  args = parser.parse_args()
  replay(sys.stdin, sys.stdout, C2_REFERENCE, 1.0 if args.speed_units == 'kph' else 0.01)


if __name__ == '__main__':
  main()
