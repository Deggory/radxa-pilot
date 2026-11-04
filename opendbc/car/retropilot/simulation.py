"""RP-SIM-1 telemetry decoding. This module never transmits or authorizes control."""
from collections import deque

from opendbc.can import CANParser
from opendbc.car.retropilot.retropilotcan import ocelot_checksum
from opendbc.car.retropilot.values import CAN_BUS

NAMES = ('SIM_SAMPLE_BEGIN', 'SIM_CLOCK', 'STEER_ANGLE_SENSOR', 'SPEED', 'ENGINE', 'CRUISE',
         'SIM_ACCEL', 'SIM_GYRO', 'SIM_WHEEL_SPEEDS', 'SIM_INPUTS', 'SIM_CRUISE_STATUS', 'SIM_SAMPLE_END')
MAX_AGE_NS = 150_000_000
BUNDLE_WINDOW_NS = 100_000_000


class SimulationReceiver:
  def __init__(self):
    self.parser = CANParser('ocelot_controls', [(name, 50) for name in NAMES], CAN_BUS)
    self.expected = {self.parser.dbc.name_to_msg[name].address for name in NAMES}
    self.begin = None
    self.pending = {}
    self.began_at = 0
    self.session = None
    self.retired = deque(maxlen=64)
    self.last_sequence = None
    self.last_time_ms = None
    self.sample = None
    self.received_at = 0

  def current(self, now_ns):
    return self.sample if 0 <= now_ns-self.received_at <= MAX_AGE_NS else None

  def feed(self, address, data, bus, now_ns):
    if bus != CAN_BUS or address not in self.expected:
      return
    msg = self.parser.dbc.addr_to_msg[address]
    if len(data) != msg.size or data[0] != ocelot_checksum(address, None, bytearray(data)):
      return
    if address == 0x700:
      self.pending = {}
      self.begin = None
      version, session, sequence = data[1] >> 4, int.from_bytes(data[2:4], 'little'), int.from_bytes(data[4:6], 'little')
      if version != 1 or not data[6] & 1 or not session or (sequence & 15) != (data[1] & 15):
        return
      if session != self.session:
        if session in self.retired:
          return
        if self.session is not None:
          self.retired.append(self.session)
        self.session, self.last_sequence, self.last_time_ms = session, None, None
        self.sample = None
        self.parser = CANParser('ocelot_controls', [(name, 50) for name in NAMES], CAN_BUS)
      elif self.last_sequence is not None and not 0 < (sequence-self.last_sequence) % 65536 < 32768:
        return
      self.begin, self.began_at = bytes(data), now_ns
    if self.begin is None or not 0 <= now_ns-self.began_at <= BUNDLE_WINDOW_NS:
      self.pending = {}
      self.begin = None
      return
    counter = data[5] & 15 if address in (0x50, 0x201, 0x301) else data[7] & 15 if address in (0x75, 0x76, 0x100) else data[1] & 15
    if counter != self.begin[1] & 15:
      return
    self.pending[address] = bytes(data)
    if address != 0x707:
      return
    begin = self.begin
    self.begin = None
    if data != begin or set(self.pending) != self.expected:
      return
    updated = self.parser.update([(now_ns, [(a, d, CAN_BUS) for a, d in self.pending.items()])])
    if updated != self.expected:
      return
    values = self.parser.vl
    clock = values['SIM_CLOCK']
    if clock['SAMPLE'] != int.from_bytes(begin[4:6], 'little') or clock['SIM_TIME_MS'] <= 0:
      return
    if self.last_time_ms is not None and clock['SIM_TIME_MS'] <= self.last_time_ms:
      return
    mask = begin[7]
    if (mask & 15 != 15 or values['STEER_ANGLE_SENSOR']['STATE'] != 1 or
        not int(values['SIM_INPUTS']['VALID_MASK']) & 2 or values['SPEED']['MODE'] != 1 or values['ENGINE']['MODE'] != 1):
      return
    self.last_time_ms = clock['SIM_TIME_MS']
    self.last_sequence = int.from_bytes(begin[4:6], 'little')
    inputs = values['SIM_INPUTS']
    inputs_valid = int(inputs['VALID_MASK'])

    def optional_input(name, bit):
      return inputs[name] if mask & 8 and inputs_valid & 1 << bit else None

    def vector(name, bit):
      return [round(values[name][axis], 9) for axis in 'XYZ'] if mask & 1 << bit and values[name]['VALID'] else None
    cruise = values['SIM_CRUISE_STATUS']
    self.sample = {
      'session': self.session, 'sequence': self.last_sequence, 'sim_time_ms': self.last_time_ms,
      'speed_mps': values['SPEED']['CAN_SPEED']/360.0,
      'steering_angle_deg': values['STEER_ANGLE_SENSOR']['STEER_ANGLE'],
      'steering_rate_magnitude_dps': values['STEER_ANGLE_SENSOR']['STEER_RATE'] if begin[6] & 4 else None,
      'ignition': bool(values['ENGINE']['IGNITION_ON']), 'brake_pressed': bool(values['ENGINE']['BRAKE_PRESSED']),
      'rpm': values['ENGINE']['CAN_ENG_RPM'] if inputs['RPM_VALID'] else None,
      'throttle_input': optional_input('THROTTLE', 0), 'brake_input': optional_input('BRAKE_INPUT', 1),
      'brake_applied': optional_input('BRAKE_APPLIED', 2), 'engaged_gear_index': optional_input('GEAR', 3),
      'acceleration_mps2': vector('SIM_ACCEL', 4), 'angular_velocity_rps': vector('SIM_GYRO', 5),
      'motion_frame': 'BeamNG motionSim component convention; not device-frame qualified',
      'wheel_speeds_mps': [values['SIM_WHEEL_SPEEDS'][wheel] for wheel in ('FL', 'FR', 'RL', 'RR')]
      if mask & 64 and values['SIM_WHEEL_SPEEDS']['VALID_MASK'] == 15 else None,
      'cruise': {'available': bool(cruise['AVAILABLE']), 'enabled': bool(cruise['ENABLED']),
                 'set_speed_mps': cruise['SET_SPEED'] if cruise['SET_SPEED_VALID'] else None}
      if mask & 128 and cruise['VALID'] else None,
      'cruise_buttons': {name: bool(values['CRUISE'][name]) for name in ('ON_OFF', 'CANCEL', 'SET_DOWN', 'RES_UP')} if begin[6] & 2 else None,
    }
    self.received_at = now_ns
