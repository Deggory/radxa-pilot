from enum import IntFlag

from opendbc.car import Bus, CarSpecs, PlatformConfig, Platforms


# Explicit bench route: historical host bus 2 -> MCU CAN3 -> connector CAN2.
# The transport must preserve host bus numbers; actual wiring is not inferred.
CAN_BUS = 2


class CarControllerParams:
  # Normalized output range and zero slew describe the enforced passive stage.
  # These are not Interceptor/Core motor limits or a physical torque calibration.
  STEER_MAX = 1
  STEER_STEP = 1
  STEER_DELTA_UP = 0
  STEER_DELTA_DOWN = 0

  def __init__(self, CP):
    if not CP.dashcamOnly:
      raise ValueError('RetroPilot has no qualified active controller profile')


class RetroPilotFlags(IntFlag):
  GAS_INTERCEPTOR = 1
  GAS_ACTUATOR = 2
  STEER_INTERCEPTOR = 4
  STEER_ACTUATOR = 8
  STEER_SSC = 16
  BRAKE_ACTUATOR = 32
  IBOOSTER = 64
  RELAY = 128


# Presence is an observation, not a calibrated control capability.
MODULES = {
  RetroPilotFlags.GAS_INTERCEPTOR: ('PEDAL_GAS_SENSOR', 0x201, 6),
  RetroPilotFlags.GAS_ACTUATOR: ('ACTUATOR_GAS_SENSOR', 0x401, 8),
  RetroPilotFlags.STEER_INTERCEPTOR: ('INTERCEPTOR_STEERING_SENSOR', 0x301, 8),
  RetroPilotFlags.STEER_ACTUATOR: ('ACTUATOR_STEERING_STATUS', 0x12F, 7),
  RetroPilotFlags.STEER_SSC: ('STEERING_STATUS_SSC', 0x22F, 8),
  RetroPilotFlags.BRAKE_ACTUATOR: ('ACTUATOR_BRAKE_STATUS', 0x10F, 5),
  RetroPilotFlags.IBOOSTER: ('IBOOSTER_BRAKE_STATUS', 0x20F, 5),
  RetroPilotFlags.RELAY: ('RELAY_CORE_STATUS', 0x601, 4),
}


class CAR(Platforms):
  RETROPILOT_RETROFIT = PlatformConfig(
    [],  # Experimental receive-only port; no supported-road-car claim.
    # Non-driving placeholders, as in mock. Replace with a measured vehicle profile.
    CarSpecs(wheelbase=2.7, steerRatio=13),
    {Bus.main: 'ocelot_controls'},
  )


DBC = CAR.create_dbc_map()
