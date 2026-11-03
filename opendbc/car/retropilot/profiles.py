"""Explicit calibration for offline controller evaluation, never a TX permission.

C2_REFERENCE reproduces the linked author's constants. It is not a calibration
for the owner's car, the paused VW Interceptor, or a selected BeamNG vehicle.
"""
import math
from dataclasses import dataclass

from opendbc.car.retropilot.values import RetroPilotFlags as F


@dataclass(frozen=True)
class ControllerProfile:
  modules: F
  steer_centers: tuple[float, float]
  steer_max: int
  steer_delta_up: int
  steer_delta_down: int
  steer_zero_speed: float  # m/s; taper to zero here, never change sign
  gas_offsets: tuple[float, float]
  gas_gains: tuple[float, float]
  gas_accel_full: float  # m/s² at normalized gas=1; requires a fitted map
  brake_decel_full: float  # positive m/s² at normalized brake=1
  brake_position_full: float  # mm

  def __post_init__(self):
    supported = F.STEER_INTERCEPTOR | F.GAS_INTERCEPTOR | F.GAS_ACTUATOR | F.BRAKE_ACTUATOR | F.IBOOSTER | F.RELAY
    if not self.modules or int(self.modules) & ~int(supported):
      raise ValueError('Select only endpoints whose control mapping is implemented')
    for pair in ((F.GAS_INTERCEPTOR, F.GAS_ACTUATOR), (F.BRAKE_ACTUATOR, F.IBOOSTER)):
      if all(self.modules & flag for flag in pair):
        raise ValueError('Select one endpoint per control axis')
    for value in (self.steer_max, self.steer_delta_up, self.steer_delta_down, self.steer_zero_speed,
                  self.gas_accel_full, self.brake_decel_full, self.brake_position_full):
      if not math.isfinite(value) or value <= 0:
        raise ValueError('Controller limits and calibration scales must be finite and positive')
    if any(type(value) is not int for value in (self.steer_max, self.steer_delta_up, self.steer_delta_down)):
      raise ValueError('Steering counts and slew limits must be integers')
    if any(type(pair) is not tuple or len(pair) != 2 or not all(math.isfinite(v) for v in pair) for pair in
           (self.steer_centers, self.gas_offsets, self.gas_gains)):
      raise ValueError('Channel calibration requires two finite values')
    if any(not -32768 <= center - self.steer_max <= center + self.steer_max <= 32767 for center in self.steer_centers):
      raise ValueError('Steering calibration exceeds signed channel range')
    if any(not 0 <= offset <= offset + gain <= 65535 for offset, gain in zip(self.gas_offsets, self.gas_gains, strict=True)):
      raise ValueError('Gas calibration exceeds unsigned channel range')
    if self.brake_position_full > 47:
      raise ValueError('Brake calibration exceeds canonical position range')


# C2 b9a942e carcontroller.py/ocelotcan.py/values.py. 350 counts means a
# 700-count channel difference: incompatible with the local Core's 400 limit.
# Its accel-to-pedal slope was implicitly 1; this is reference behavior only.
C2_REFERENCE = ControllerProfile(
  modules=F.STEER_INTERCEPTOR | F.GAS_ACTUATOR | F.IBOOSTER,
  steer_centers=(1510, 1510), steer_max=350, steer_delta_up=5, steer_delta_down=5, steer_zero_speed=90,
  gas_offsets=(0, 0), gas_gains=(1500, 0), gas_accel_full=1, brake_decel_full=1, brake_position_full=7,
)
