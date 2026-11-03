from opendbc.car import get_safety_config, structs
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.retropilot.carcontroller import CarController
from opendbc.car.retropilot.carstate import CarState
from opendbc.car.retropilot.values import CAN_BUS, MODULES


class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController

  @staticmethod
  def _get_params(ret, candidate, fingerprint, car_fw, alpha_long, is_release, docs):
    ret.brand = 'retropilot'
    ret.dashcamOnly = True
    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.noOutput)]
    ret.radarUnavailable = True
    ret.pcmCruise = False
    ret.openpilotLongitudinalControl = False
    # Zero means unqualified. Explicitly choose 1.0 (legacy km/h) or 0.01
    # (centi-km/h) only after confirming the producer. No unit guessing.
    ret.wheelSpeedFactor = 0.0
    ret.minEnableSpeed = float('inf')
    ret.minSteerSpeed = float('inf')
    ret.lateralTuning.init('pid')
    ret.lateralTuning.pid.kpBP = [0.0]
    ret.lateralTuning.pid.kpV = [0.0]
    ret.lateralTuning.pid.kiBP = [0.0]
    ret.lateralTuning.pid.kiV = [0.0]
    for flag, (_, address, size) in MODULES.items():
      if fingerprint.get(CAN_BUS, {}).get(address) == size:
        ret.flags |= int(flag)
    return ret
