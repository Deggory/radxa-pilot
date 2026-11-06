"""Shared normal-consumer admission checks for PandaState field availability."""
from openpilot.cereal import log

FIELD_NAMES = {value: name for name, value in log.PandaState.StatusAvailability.Field.schema.enumerants.items()}
LEGACY_UNAVAILABLE = frozenset(('spiErrorCount', 'soundOutputLevel', 'controlsAllowedLateral',
                                'controlsAllowedLongitudinal', 'nmiReset', 'hardfaultReset'))
ACTIVE_FIELDS = frozenset(log.PandaState.schema.fields) - {'deprecated', 'statusAvailability'}
IGNITION_FIELDS = ('pandaType', 'ignitionLine', 'ignitionCan', 'harnessStatus')
CONTROL_FIELDS = ('controlsAllowed', 'safetyModel', 'safetyParam', 'alternativeExperience', 'safetyRxChecksInvalid', 'faults')


def usable_panda_states(panda_states, *, valid: bool, required_fields: tuple[str, ...] = ()) -> list:
  """Return the entire batch or none; never shift board indices by filtering.

  Absence of metadata retains the historical current-producer convention. Present
  metadata must name a known profile and fields; observation-only data is denied.
  The caller also supplies liveness in valid when consuming a retained sample.
  This checks declared support, not firmware authentication or control permission.
  """
  required = frozenset(required_fields)
  if not required <= ACTIVE_FIELDS:
    raise ValueError('Unknown required PandaState field')
  if not valid:
    return []
  states = list(panda_states)
  for state in states:
    if not state._has('statusAvailability'):
      continue
    info = state.statusAvailability
    if info.profile.raw not in (1, 2) or info.observationOnly:
      return []
    raw_fields = {field.raw for field in info.unavailableFields}
    if not raw_fields <= FIELD_NAMES.keys():
      return []
    missing = {FIELD_NAMES[field] for field in raw_fields}
    if info.profile.raw == 2 and not LEGACY_UNAVAILABLE <= missing:
      return []
    if required & missing:
      return []
  return states
