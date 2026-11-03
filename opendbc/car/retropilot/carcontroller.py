from opendbc.car import structs
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  """Enforce the receive-only stage independently of incoming control requests."""

  def update(self, CC, CC_SP, CS, now_nanos):
    # Chimera does not yet implement a verified modern safety contract.
    # Even a mutated CP or enabled CC cannot turn this receiver into a sender.
    return structs.CarControl.Actuators(), []
