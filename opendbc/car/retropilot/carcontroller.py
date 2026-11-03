import math
from dataclasses import dataclass

from opendbc.can import CANPacker
from opendbc.car import Bus, DT_CTRL, structs
from opendbc.car.can_definitions import CanData
from opendbc.car.interfaces import CarControllerBase
from opendbc.car.retropilot import commands
from opendbc.car.retropilot.profiles import ControllerProfile
from opendbc.car.retropilot.values import CAN_BUS, RetroPilotFlags as F


@dataclass
class ControlPreview:
  actuators: structs.CarControl.Actuators
  can_messages: list[CanData]
  lateral_active: bool = False
  longitudinal_active: bool = False
  block_reason: str = ''


class CarController(CarControllerBase):
  """Modern C2 control calculation; candidate CAN is isolated from live TX.

  Pass an explicit profile to evaluate preview() in replay/simulation. update()
  retains the zero-output runtime boundary until Chimera safety is qualified.
  No environment variable, CP flag or calibration can grant TX permission.
  """

  def __init__(self, dbc_names, CP, CP_SP, *, profile: ControllerProfile | None = None):
    super().__init__(dbc_names, CP, CP_SP)
    self.packer = CANPacker(dbc_names[Bus.main])
    self.profile = profile
    self.last_torque = 0
    self.last_nanos = None
    self.counters = {}
    self.gas = 0.0
    self.gas_enabled = False
    self.relay_enabled = False
    self.last_preview = ControlPreview(structs.CarControl.Actuators(), [], block_reason='calibration_missing')

  def _counter(self, name):
    count = self.counters.get(name, 0)
    self.counters[name] = (count + 1) % 16
    return count

  def preview(self, CC, CS, now_nanos, *, relay_bits=0):
    """Evaluate one timestamped 100 Hz step; returned frames are never sent."""
    result = ControlPreview(structs.CarControl.Actuators(), [])
    p = self.profile
    if p is None:
      result.block_reason = 'calibration_missing'
      return result
    if type(relay_bits) is not int or not 0 <= relay_bits <= 65535:
      raise ValueError('Relay command must be an explicit sixteen-bit mask')

    out = CS.out
    interval = DT_CTRL if self.last_nanos is None else (now_nanos - self.last_nanos) * 1e-9
    self.last_nanos = now_nanos
    if not 0 < interval <= 0.05:
      result.block_reason = 'control_timing'
    elif not CS.control_ready or not 0 <= now_nanos - CS.control_state_nanos <= 100_000_000:
      result.block_reason = 'state_unavailable'
    elif not out.canValid or out.canTimeout or out.vehicleSensorsInvalid or out.carFaultedNonCritical:
      result.block_reason = 'state_invalid'
    elif int(self.CP.flags) & int(p.modules) != int(p.modules):
      result.block_reason = 'endpoint_missing'
    elif not all(math.isfinite(v) for v in (out.vEgo, CC.actuators.torque, CC.actuators.accel)) or out.vEgo < 0:
      result.block_reason = 'nonfinite_or_negative_input'
    elif not CC.enabled or CC.cruiseControl.cancel or out.brakePressed:
      result.block_reason = 'disabled_or_override'

    healthy = not result.block_reason
    result.lateral_active = bool(healthy and CC.latActive and not out.steeringPressed and
                                 not out.steerFaultTemporary and not out.steerFaultPermanent and p.modules & F.STEER_INTERCEPTOR)
    if result.lateral_active:
      limit = max(0, p.steer_max * (1 - out.vEgo / p.steer_zero_speed))
      desired = round(max(-1, min(CC.actuators.torque, 1)) * limit)
      up = p.steer_delta_up * min(interval / DT_CTRL, 1)
      down = p.steer_delta_down * min(interval / DT_CTRL, 1)
      # Return toward zero before changing sign; never cross zero in one step.
      if self.last_torque > 0:
        lower, upper = max(self.last_torque - down, 0), self.last_torque + up
      elif self.last_torque < 0:
        lower, upper = self.last_torque - up, min(self.last_torque + down, 0)
      else:
        lower, upper = -up, up
      self.last_torque = int(max(-limit, min(limit, max(lower, min(desired, upper)))))
    else:
      self.last_torque = 0

    if p.modules & F.STEER_INTERCEPTOR:
      result.can_messages.append(commands.steering_interceptor(
        self.packer, CAN_BUS, result.lateral_active, p.steer_centers[0] + self.last_torque,
        p.steer_centers[1] - self.last_torque, self._counter('steering')))
    result.actuators.torque = self.last_torque / p.steer_max
    result.actuators.torqueOutputCan = self.last_torque

    has_gas = bool(p.modules & (F.GAS_INTERCEPTOR | F.GAS_ACTUATOR))
    has_brake = bool(p.modules & (F.BRAKE_ACTUATOR | F.IBOOSTER))
    result.longitudinal_active = bool(healthy and CC.longActive and not out.gasPressed and not out.accFaulted and has_gas and has_brake)
    gas = max(0, min(CC.actuators.accel / p.gas_accel_full, 1)) if result.longitudinal_active else 0.0
    brake = max(0, min(-CC.actuators.accel / p.brake_decel_full, 1)) if result.longitudinal_active else 0.0
    gas_enabled = result.longitudinal_active and brake == 0 and (bool(p.modules & F.GAS_ACTUATOR) or gas > 0.001)
    if gas <= 0.001 and p.modules & F.GAS_INTERCEPTOR:
      gas = 0.0
    # At 50 Hz hold the last gas request. Flush immediately on disable or when
    # braking starts, so an odd control tick can never overlap gas and brake.
    if has_gas and (self.frame % 2 == 0 or self.gas_enabled and not gas_enabled or self.gas > 0 and gas == 0):
      self.gas = gas
      self.gas_enabled = gas_enabled
      result.can_messages.append(commands.gas(
        self.packer, CAN_BUS, gas_enabled, p.gas_offsets[0] + gas * p.gas_gains[0],
        p.gas_offsets[1] + gas * p.gas_gains[1], self._counter('gas'), actuator=bool(p.modules & F.GAS_ACTUATOR)))
    if has_brake:
      result.can_messages.append(commands.brake(
        self.packer, CAN_BUS, 2 if result.longitudinal_active else 0, brake * p.brake_position_full, 0,
        self._counter('brake'), ibooster=bool(p.modules & F.IBOOSTER)))
    if p.modules & F.RELAY and (self.frame % 2 == 0 or self.relay_enabled and not healthy):
      result.can_messages.append(commands.relay(self.packer, CAN_BUS, healthy, relay_bits, self._counter('relay')))
      self.relay_enabled = healthy
    result.actuators.gas = self.gas
    result.actuators.brake = brake
    result.actuators.accel = self.gas * p.gas_accel_full - brake * p.brake_decel_full
    result.actuators.speed = out.vEgo if math.isfinite(out.vEgo) else 0
    self.frame += 1
    return result

  def update(self, CC, CC_SP, CS, now_nanos):
    self.last_preview = self.preview(CC, CS, now_nanos)
    # Candidate feedback must not be reported as actual actuation.
    return structs.CarControl.Actuators(), []
