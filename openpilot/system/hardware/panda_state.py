from openpilot.cereal import log


def panda_power_state(panda_states, *, valid: bool, in_car: bool = False) -> tuple[bool, bool]:
  """Reduce one updated pandaStates event to ignition and shutdown context.

  Invalid/empty updates revoke ignition immediately. Retain the last valid primary
  harness state for battery shutdown until a valid non-unknown primary replaces it;
  this history does not assert that a Panda is currently connected. The caller
  retains the existing disconnect grace when there is no new event.
  """
  if not valid or not panda_states:
    return False, in_car

  unknown = log.PandaState.PandaType.unknown
  ignition = any(ps.ignitionLine or ps.ignitionCan for ps in panda_states if ps.pandaType != unknown)
  primary = panda_states[0]
  if primary.pandaType != unknown:
    in_car = primary.harnessStatus != log.PandaState.HarnessStatus.notConnected
  return ignition, in_car
