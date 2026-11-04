#!/usr/bin/env python3
"""Read-only BeamNG telemetry -> canonical RetroPilot CAN. No actuator TX path."""
import argparse
from collections import deque
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import secrets
import select
import socket
import struct
import sys
import time

# Packed identically by BeamNG's FFI struct (doubles start at byte8).
FLOAT_FIELDS = ('speed', 'angle', 'rate', 'rpm', 'throttle', 'brake_input', 'brake', 'ignition', 'gear',
                'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z',
                'wheel_fl', 'wheel_fr', 'wheel_rl', 'wheel_rr', 'cruise_available', 'cruise_enabled', 'cruise_speed')
PACKET = struct.Struct('<4sIddII' + 'f' * len(FLOAT_FIELDS) + 'I4x')
MAX_SOURCE_AGE = 0.15
BUS = 2
TELEMETRY_NAMES = frozenset(('SIM_SAMPLE_BEGIN', 'SIM_CLOCK', 'STEER_ANGLE_SENSOR', 'SPEED', 'ENGINE', 'CRUISE',
                             'SIM_ACCEL', 'SIM_GYRO', 'SIM_WHEEL_SPEEDS', 'SIM_INPUTS', 'SIM_CRUISE_STATUS', 'SIM_SAMPLE_END'))


@dataclass
class Sample:
  session: int
  wall_time: float
  sim_time: float
  sequence: int
  valid: int
  speed: float
  angle: float
  rate: float
  rpm: float
  throttle: float
  brake_input: float
  brake: float
  ignition: float
  gear: float
  accel_x: float
  accel_y: float
  accel_z: float
  gyro_x: float
  gyro_y: float
  gyro_z: float
  wheel_fl: float
  wheel_fr: float
  wheel_rl: float
  wheel_rr: float
  cruise_available: float
  cruise_enabled: float
  cruise_speed: float
  buttons: int

  @classmethod
  def decode(cls, raw):
    if len(raw) != PACKET.size:
      raise ValueError('Wrong telemetry packet length')
    magic, *values = PACKET.unpack(raw)
    if magic != b'RPT1':
      raise ValueError('Unknown telemetry packet version')
    return cls(*values)


def crc8(data):
  crc = 255
  for byte in data:
    crc ^= byte
    for _ in range(8):
      crc = ((crc << 1) ^ (0x1d if crc & 128 else 0)) & 255
  return crc ^ 255


class SourceGate:
  def __init__(self):
    self.last = None
    self.retired = deque(maxlen=64)

  def accept(self, sample, wall_now):
    if not all(math.isfinite(v) for v in (sample.wall_time, sample.sim_time, wall_now)):
      return False
    if not -0.05 <= wall_now - sample.wall_time <= MAX_SOURCE_AGE or sample.sim_time <= 0:
      return False
    if self.last:
      if sample.session != self.last.session:
        if sample.session in self.retired:
          return False
        self.retired.append(self.last.session)
      elif sample.sequence <= self.last.sequence or sample.sim_time <= self.last.sim_time:
        return False
    self.last = sample
    return True


class Encoder:
  def __init__(self, session=None, dbc_path=None):
    import cantools
    here = Path(__file__).resolve()
    if dbc_path is None:
      # A deployed PC bundle carries its DBC; the repository uses the packaged copy.
      dbc_path = here.parent / 'ocelot_controls.dbc'
      if not dbc_path.exists():
        dbc_path = here.parents[5] / 'opendbc_repo/opendbc/dbc/ocelot_controls.dbc'
    version = json.loads((here.parent.parent / 'shared/dbc-version.json').read_text())
    if hashlib.sha256(Path(dbc_path).read_bytes()).hexdigest() != version['sha256']:
      raise ValueError('DBC does not match the shared RP-SIM-1 version')
    # The unchanged C2 CRUISE ADC fields overlap its counter/mode. We never use
    # those ADC fields; preserve that legacy definition rather than silently edit it.
    self.dbc = cantools.database.load_file(dbc_path, strict=False)
    self.session = secrets.randbelow(65535) + 1 if session is None else session

  def message(self, name, counter, values):
    if name not in TELEMETRY_NAMES:
      raise ValueError('Message is not part of read-only simulator telemetry')
    msg = self.dbc.get_message_by_name(name)
    payload = {signal.name: 0 for signal in msg.signals}
    payload.update(values, COUNTER=counter)
    try:
      data = bytearray(msg.encode(payload, strict=False))
    except (ValueError, OverflowError) as error:
      raise ValueError(f'Cannot encode {name}: {error}') from error
    data[0] = crc8(data[1:])
    return msg.frame_id, bytes(data), BUS

  def encode(self, sample):
    # Never turn an unavailable required value into an apparently healthy frame.
    required = (1 << 0 | 1 << 1 | 1 << 2 | 1 << 5)
    if sample.valid & required != required:
      raise ValueError('Speed, angle, ignition and driver-brake data are required')
    limits = {'speed': (0, 65535/360), 'angle': (-3276.8, 3276.7), 'rate': (-65535, 65535),
              'rpm': (0, 65535), 'throttle': (0, 1), 'brake_input': (0, 1), 'brake': (0, 1),
              'ignition': (0, 1), 'gear': (-1, 127), 'cruise_available': (0, 1),
              'cruise_enabled': (0, 1), 'cruise_speed': (0, 655.35)}
    limits.update({f'accel_{axis}': (-327.68, 327.67) for axis in 'xyz'})
    limits.update({f'gyro_{axis}': (-32.768, 32.767) for axis in 'xyz'})
    limits.update({f'wheel_{wheel}': (0, 204.75) for wheel in ('fl', 'fr', 'rl', 'rr')})
    for name, (low, high) in limits.items():
      value = getattr(sample, name)
      if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'Invalid {name}: {value}')
    if sample.gear != int(sample.gear) or not 0 <= sample.buttons <= 15:
      raise ValueError('Invalid discrete input')
    if not math.isfinite(sample.sim_time) or not 0 < sample.sim_time < 4294967.295:
      raise ValueError('Simulation time outside protocol range')
    counter = sample.sequence & 15
    def valid(bit):
      return bool(sample.valid & (1 << bit))
    mask = int(valid(0)) | int(valid(1)) << 1 | int(valid(2)) << 2 | int(valid(4) or valid(5) or valid(6) or valid(7)) << 3
    mask |= int(valid(8)) << 4 | int(valid(9)) << 5 | int(valid(10)) << 6 | int(valid(11)) << 7
    flags = 1 | int(valid(12)) << 1 | int(valid(13)) << 2
    meta = {'PROTOCOL_VERSION': 1, 'SESSION': self.session, 'SAMPLE': sample.sequence & 65535, 'FLAGS': flags, 'VALID_MASK': mask}
    messages = [
      ('SIM_SAMPLE_BEGIN', meta),
      ('SIM_CLOCK', {'SIM_TIME_MS': round(sample.sim_time*1000), 'SAMPLE': sample.sequence & 65535}),
      ('STEER_ANGLE_SENSOR', {'STEER_ANGLE': sample.angle, 'STEER_RATE': abs(sample.rate) if valid(13) else 0, 'STATE': 1}),
      ('SPEED', {'CAN_SPEED': round(sample.speed*360), 'MODE': 1}),
      ('ENGINE', {'IGNITION_ON': sample.ignition, 'BRAKE_PRESSED': int(sample.brake_input > 0.05), 'CAN_ENG_RPM': sample.rpm if valid(3) else 0, 'MODE': 1}),
      ('CRUISE', {name: int(valid(12) and sample.buttons & (1 << bit) != 0) for bit, name in enumerate(('ON_OFF', 'CANCEL', 'SET_DOWN', 'RES_UP'))}),
      ('SIM_ACCEL', {'VALID': int(valid(8)), **{axis.upper(): getattr(sample, 'accel_'+axis) if valid(8) else 0 for axis in 'xyz'}}),
      ('SIM_GYRO', {'VALID': int(valid(9)), **{axis.upper(): getattr(sample, 'gyro_'+axis) if valid(9) else 0 for axis in 'xyz'}}),
      ('SIM_WHEEL_SPEEDS', {'VALID_MASK': 15 if valid(10) else 0,
                            **{wheel.upper(): getattr(sample, 'wheel_'+wheel) if valid(10) else 0 for wheel in ('fl', 'fr', 'rl', 'rr')}}),
      ('SIM_INPUTS', {'THROTTLE': sample.throttle if valid(4) else 0, 'BRAKE_INPUT': sample.brake_input,
                      'BRAKE_APPLIED': sample.brake if valid(6) else 0, 'GEAR': sample.gear if valid(7) else 0,
                      'VALID_MASK': sum(int(valid(4+i)) << i for i in range(4)), 'IGNITION': sample.ignition,
                      'RPM_VALID': int(valid(3)), 'STEER_RATE_VALID': int(valid(13))}),
      ('SIM_CRUISE_STATUS', {'VALID': int(valid(11)), 'AVAILABLE': sample.cruise_available if valid(11) else 0,
                             'ENABLED': sample.cruise_enabled if valid(11) else 0,
                             'SET_SPEED_VALID': int(valid(11)), 'SET_SPEED': sample.cruise_speed if valid(11) else 0}),
      ('SIM_SAMPLE_END', meta),
    ]
    return [self.message(name, counter, values) for name, values in messages]


def encode_serial(address, data):
  if not 0 <= address <= 0x7ff or len(data) > 8:
    raise ValueError('Only standard classical CAN frames are supported')
  return bytes([0xaa, 0xc0 | len(data)]) + address.to_bytes(2, 'little') + data + b'\x55'


def adapter_config(bitrate):
  codes = {125000: 7, 250000: 6, 500000: 3, 1000000: 1}
  if bitrate not in codes:
    raise ValueError('Unsupported CAN bitrate')
  data = bytearray(20)
  data[:5] = bytes([0xaa, 0x55, 0x12, codes[bitrate], 1])
  data[13:15] = bytes([0, 1])  # Normal mode; disable automatic retransmission.
  data[-1] = sum(data[2:-1]) & 255
  return bytes(data)


def write_serial(fd, data):
  deadline = time.monotonic() + 0.05
  while data:
    if time.monotonic() >= deadline:
      raise TimeoutError('USB-CAN write exceeded 50ms')
    if not select.select([], [fd], [], max(0, deadline-time.monotonic()))[1]:
      raise TimeoutError('USB-CAN write stalled')
    try:
      written = os.write(fd, data)
    except BlockingIOError:
      continue
    if written <= 0:
      raise OSError('USB-CAN write made no progress')
    data = data[written:]


def open_serial(path):
  import fcntl
  import termios
  import tty
  fd = os.open(path, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
  try:
    fcntl.ioctl(fd, termios.TIOCEXCL)
    tty.setraw(fd)
    config = termios.tcgetattr(fd)
    config[2] &= ~(termios.CSIZE | termios.PARENB | termios.CSTOPB | getattr(termios, 'CRTSCTS', 0))
    config[2] |= termios.CS8 | termios.CREAD | termios.CLOCAL
    config[4] = config[5] = termios.B2000000
    termios.tcsetattr(fd, termios.TCSANOW, config)
    termios.tcflush(fd, termios.TCIOFLUSH)
    return fd
  except BaseException:
    os.close(fd)
    raise


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--port', type=int, default=49160)
  parser.add_argument('--duration', type=float, default=0, help='Seconds; zero runs until Ctrl+C')
  parser.add_argument('--serial', help='Explicit Linux Waveshare port; omitted means JSON dry-run')
  parser.add_argument('--transmit', action='store_true', help='Enable telemetry on the isolated simulator CAN bus')
  parser.add_argument('--bitrate', type=int, default=500000)
  args = parser.parse_args()
  if bool(args.serial) != args.transmit or args.duration < 0:
    parser.error('Physical TX requires both --serial and --transmit; duration must be nonnegative')
  encoder, gate = Encoder(), SourceGate()
  fd = None
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.bind(('127.0.0.1', args.port))
      sock.settimeout(0.1)
      if args.serial:
        fd = open_serial(args.serial)
        write_serial(fd, adapter_config(args.bitrate))
      print(json.dumps({'status': 'waiting_for_beamng', 'udp': '127.0.0.1:'+str(args.port),
                        'physical_tx': fd is not None}), file=sys.stderr, flush=True)
      start = time.monotonic()
      last_session = None
      count = 0
      while not args.duration or time.monotonic() - start < args.duration:
        try:
          raw = sock.recv(2048)
        except TimeoutError:
          continue  # No stale sample is repeated onto CAN.
        try:
          sample = Sample.decode(raw)
          if not gate.accept(sample, time.clock_gettime(time.CLOCK_REALTIME)):
            continue
          frames = encoder.encode(sample)
          if sample.session != last_session:
            encoder.session = encoder.session % 65535 + 1
            frames = encoder.encode(sample)
            last_session = sample.session
          if fd is not None:
            write_serial(fd, b''.join(encode_serial(a, d) for a, d, _ in frames))
          else:
            print(json.dumps({'timestamp_ns': time.monotonic_ns(), 'frames': [[a, d.hex(), b] for a, d, b in frames]}), flush=True)
          count += 1
        except (ValueError, struct.error) as error:
          print(f'Rejected telemetry: {error}', file=sys.stderr)
      print(json.dumps({'samples': count, 'physical_tx': fd is not None}), file=sys.stderr)
  finally:
    if fd is not None:
      os.close(fd)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
