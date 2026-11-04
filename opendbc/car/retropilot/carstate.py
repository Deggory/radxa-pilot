import math

from opendbc.can import CANParser
from opendbc.can.parser import MAX_BAD_COUNTER
from opendbc.car import Bus, structs
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.interfaces import CarStateBase
from opendbc.car.retropilot.values import ANGLE_STATE_ENABLED, CAN_BUS, DBC, MODULES, RetroPilotFlags


BUTTONS = {
  'ON_OFF': structs.CarState.ButtonEvent.Type.mainCruise,
  'RES_UP': structs.CarState.ButtonEvent.Type.accelCruise,
  'SET_DOWN': structs.CarState.ButtonEvent.Type.decelCruise,
  'CANCEL': structs.CarState.ButtonEvent.Type.cancel,
}


class RetroPilotCANParser(CANParser):
  def update(self, packets, sendcan=False):
    # This protocol requires exact classical-CAN DLCs, including all CRC bytes.
    # Preserve timestamps and unrelated bus traffic so timeout detection still works.
    if packets and not isinstance(packets[0], list | tuple):
      packets = [packets]
    filtered = []
    for timestamp, frames in packets:
      frames = [frame for frame in frames if frame[0] not in self.message_states or
                len(frame[1]) == self.message_states[frame[0]].size]
      filtered.append((timestamp, frames))
    return super().update(filtered, sendcan)

  def fresh(self, name):
    state = self.message_states[self.dbc.name_to_msg[name].address]
    return state.valid(self._last_update_nanos, self.bus_timeout) and state.counter_fail < MAX_BAD_COUNTER


class CarState(CarStateBase):
  def __init__(self, CP, CP_SP):
    super().__init__(CP, CP_SP)
    self.armed = False
    self.previous_buttons = None
    self.control_ready = False
    self.control_state_nanos = 0

  def update(self, can_parsers):
    cp = can_parsers[Bus.main]
    if self.CP.flags & RetroPilotFlags.BEAMNG:
      return self.update_simulation(cp)
    ret = structs.CarState()
    ret_sp = structs.CarStateSP()
    button_events = []
    ret.carNotReady = True  # Receive-only: gear, profile and control path unqualified.
    ret.vehicleSensorsInvalid = not any(math.isclose(self.CP.wheelSpeedFactor, factor, rel_tol=1e-6) for factor in (1.0, 0.01))
    healthy = all(cp.fresh(state.name) for state in cp.message_states.values())

    if cp.fresh('SPEED') and not ret.vehicleSensorsInvalid:
      ret.vEgoRaw = cp.vl['SPEED']['CAN_SPEED'] * CV.KPH_TO_MS * self.CP.wheelSpeedFactor
      ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)
      ret.standstill = ret.vEgoRaw < 0.001
    else:
      ret.vehicleSensorsInvalid = True

    ret.steerFaultTemporary = not cp.fresh('STEER_ANGLE_SENSOR') or cp.vl['STEER_ANGLE_SENSOR']['STATE'] != ANGLE_STATE_ENABLED

    if cp.fresh('STEER_ANGLE_SENSOR'):
      ret.steeringAngleDeg = cp.vl['STEER_ANGLE_SENSOR']['STEER_ANGLE']
      # Canonical STEER_RATE is unsigned magnitude, not a signed derivative.
      # CarState's rate has direction; leave it unavailable rather than inventing it.
      ret.vehicleSensorsInvalid |= cp.vl['STEER_ANGLE_SENSOR']['STATE'] != ANGLE_STATE_ENABLED
    else:
      ret.vehicleSensorsInvalid = True

    ignition = cp.fresh('ENGINE') and bool(cp.vl['ENGINE']['IGNITION_ON'])
    ret.brakePressed = cp.fresh('ENGINE') and bool(cp.vl['ENGINE']['BRAKE_PRESSED'])
    steering_flags = (RetroPilotFlags.STEER_INTERCEPTOR, RetroPilotFlags.STEER_ACTUATOR, RetroPilotFlags.STEER_SSC)
    if sum(bool(self.CP.flags & flag) for flag in steering_flags) > 1:
      # Multiple observed endpoints do not select a feedback authority.
      ret.vehicleSensorsInvalid = True
    for flag, (name, _, _) in MODULES.items():
      if not self.CP.flags & flag:
        continue
      if not cp.fresh(name):
        ret.vehicleSensorsInvalid = True
        continue
      status = cp.vl[name]
      if flag == RetroPilotFlags.STEER_INTERCEPTOR:
        ret.steeringPressed = bool(status['OVERRIDE'])
        ret.steerFaultTemporary |= status['STATE'] != 0
        # TRQ_1/TRQ_2 are retained raw in the parser; no guessed Nm calibration.
      elif flag == RetroPilotFlags.STEER_ACTUATOR:
        ret.steeringTorque = status['STEERING_TORQUE_DRIVER']
        ret.steeringTorqueEps = status['STEERING_TORQUE_EPS']
        ret.steerFaultTemporary |= not status['STEERING_OK'] or status['STATUS'] != 0
      elif flag == RetroPilotFlags.STEER_SSC:
        ret.steeringTorqueEps = status['STEERING_TORQUE']
        # CONTROL_STATUS is endpoint-specific; no guessed OK/override values.
      elif flag in (RetroPilotFlags.BRAKE_ACTUATOR, RetroPilotFlags.IBOOSTER):
        ret.brakePressed |= bool(status['DRIVER_BRAKE_APPLIED'])
        ret.accFaulted |= not status['BRAKE_OK'] or status['STATUS'] != 0
      else:
        ret.carFaultedNonCritical |= status['STATE'] != 0

    # No gear, separate wheel speeds, cruise-enabled status or calibrated pedal/
    # torque mapping exists in the base contract. Keep their schema defaults.
    cruise_healthy = (healthy and ignition and not ret.brakePressed and not ret.steeringPressed and not ret.vehicleSensorsInvalid and
                      not ret.steerFaultTemporary and not ret.accFaulted and not ret.carFaultedNonCritical)
    # Readiness for offline control calculation only. carNotReady remains true:
    # it additionally covers the unqualified live profile/gear/safety path.
    # Empty/wrong-bus/CRC-rejected traffic must not refresh this timestamp.
    self.control_state_nanos = min((state.timestamps[-1] if state.timestamps else 0) for state in cp.message_states.values())
    self.control_ready = healthy and ignition and not ret.vehicleSensorsInvalid and not ret.carFaultedNonCritical
    if not cruise_healthy:
      self.armed = False
      self.previous_buttons = None
    else:
      samples = zip(*(cp.vl_all['CRUISE'][name] for name in BUTTONS), strict=True)
      for sample in samples:
        buttons = dict(zip(BUTTONS, map(bool, sample), strict=True))
        if self.previous_buttons is not None:
          for name, event_type in BUTTONS.items():
            if buttons[name] != self.previous_buttons[name]:
              button_events.append(structs.CarState.ButtonEvent(type=event_type, pressed=buttons[name]))
          if buttons['ON_OFF'] and not self.previous_buttons['ON_OFF']:
            self.armed = not self.armed
        if buttons['CANCEL']:
          self.armed = False
        self.previous_buttons = buttons

    ret.cruiseState.available = self.armed and cruise_healthy
    # ON/SET is an observed button, never evidence of an engaged controller.
    ret.cruiseState.enabled = False
    ret.buttonEvents = button_events
    return ret, ret_sp

  def update_simulation(self, cp):
    ret, ret_sp = structs.CarState(), structs.CarStateSP()
    ret.carNotReady = True  # Telemetry only, independent of in-game cruise state.
    ret.vehicleSensorsInvalid = True
    self.control_ready = False
    sample = cp.simulation.current(cp._last_update_nanos)
    if sample is None:
      return ret, ret_sp
    ret.vehicleSensorsInvalid = False
    ret.vEgoRaw = sample['speed_mps']
    ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)
    ret.standstill = ret.vEgoRaw < 0.001
    ret.steeringAngleDeg = sample['steering_angle_deg']
    ret.brakePressed = sample['brake_pressed']
    if sample['brake_input'] is not None:
      ret_sp.brake = sample['brake_input']
    if sample['throttle_input'] is not None:
      ret_sp.gas = sample['throttle_input']
      ret.gasPressed = ret_sp.gas > 0.01
    if sample['wheel_speeds_mps'] is not None:
      for name, value in zip(('fl', 'fr', 'rl', 'rr'), sample['wheel_speeds_mps'], strict=True):
        setattr(ret.wheelSpeeds, name, value)
    if sample['cruise'] is not None:
      ret.cruiseState.available = sample['cruise']['available']
      ret.cruiseState.enabled = sample['cruise']['enabled']
      ret.cruiseState.speed = sample['cruise']['set_speed_mps'] or 0
    # RPM, engaged gear index and simulated IMU remain explicitly available in
    # cp.simulation.current(). No guessed gear selector or device-frame IMU.
    return ret, ret_sp

  @staticmethod
  def get_can_parsers(CP, CP_SP):
    if CP.flags & RetroPilotFlags.BEAMNG:
      from opendbc.car.retropilot.simulation import NAMES, SimulationReceiver

      class SimulationParser(RetroPilotCANParser):
        def __init__(self):
          super().__init__('ocelot_controls', [(name, 50) for name in NAMES], CAN_BUS)
          self.simulation = SimulationReceiver()

        def update(self, packets, sendcan=False):
          for timestamp, frames in packets:
            for address, data, bus in frames:
              self.simulation.feed(address, data, bus, timestamp)
          return super().update(packets, sendcan)

      return {Bus.main: SimulationParser()}
    messages = [('STEER_ANGLE_SENSOR', 20), ('ENGINE', 20), ('SPEED', 20), ('CRUISE', 20)]
    messages += [(name, 20) for flag, (name, _, _) in MODULES.items() if CP.flags & flag]
    return {Bus.main: RetroPilotCANParser(DBC[CP.carFingerprint][Bus.main], messages, CAN_BUS)}
