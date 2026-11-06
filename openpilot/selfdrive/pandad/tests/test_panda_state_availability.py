import unittest

from openpilot.cereal import log
from openpilot.selfdrive.pandad.panda_state import usable_panda_states

MISSING = ['spiErrorCount', 'soundOutputLevel', 'controlsAllowedLateral',
           'controlsAllowedLongitudinal', 'nmiReset', 'hardfaultReset']


def event(*, valid=True, profile=None, observation=False, missing=()):
  msg = log.Event.new_message(valid=valid)
  state = msg.init('pandaStates', 1)[0]
  state.pandaType = 'blackPanda'
  state.ignitionLine = state.controlsAllowed = state.controlsAllowedLateral = True
  if profile is not None:
    info = state.init('statusAvailability')
    info.profile = profile
    info.observationOnly = observation
    info.unavailableFields = missing
  return msg


class PandaAvailabilityTests(unittest.TestCase):
  def test_old_current_messages_remain_compatible(self):
    msg = event()
    self.assertEqual(len(usable_panda_states(msg.pandaStates, valid=msg.valid, required_fields=('controlsAllowedLateral',))), 1)

  def test_invalid_event_never_reads_fields(self):
    self.assertEqual(usable_panda_states(None, valid=False), [])

  def test_observation_cannot_be_promoted_by_changing_event_valid(self):
    msg = event(profile='legacyF4v17', observation=True, missing=MISSING)
    self.assertEqual(usable_panda_states(msg.pandaStates, valid=True), [])

  def test_legacy_metadata_must_report_all_six_missing_fields(self):
    for missing in ([], MISSING[:-1]):
      msg = event(profile='legacyF4v17', missing=missing)
      self.assertEqual(usable_panda_states(msg.pandaStates, valid=True), [])

  def test_field_requirements_are_explicit(self):
    msg = event(profile='legacyF4v17', missing=MISSING)
    self.assertEqual(len(usable_panda_states(msg.pandaStates, valid=True, required_fields=('ignitionLine', 'controlsAllowed'))), 1)
    for name in MISSING:
      self.assertEqual(usable_panda_states(msg.pandaStates, valid=True, required_fields=(name,)), [])

  def test_current_metadata_can_withhold_a_field(self):
    msg = event(profile='current', missing=['controlsAllowedLateral'])
    self.assertEqual(usable_panda_states(msg.pandaStates, valid=True, required_fields=('controlsAllowedLateral',)), [])
    self.assertEqual(len(usable_panda_states(msg.pandaStates, valid=True, required_fields=('controlsAllowed',))), 1)

  def test_unknown_profile_or_field_rejected(self):
    for profile in ('unknown', 99):
      msg = event(profile=profile)
      self.assertEqual(usable_panda_states(msg.pandaStates, valid=True), [])
    # Pycapnp refuses an unknown integer in an enum list. Make a malformed wire
    # fixture by replacing the first element in the unique encoded enum sequence.
    data = bytearray(event(profile='current', missing=MISSING).to_bytes())
    sequence = bytes.fromhex('000001000200030004000500')
    self.assertEqual(data.count(sequence), 1)
    offset = data.index(sequence)
    data[offset:offset + 2] = b'\xff\xff'
    with log.Event.from_bytes(bytes(data)) as reader:
      self.assertEqual(reader.pandaStates[0].statusAvailability.unavailableFields[0].raw, 65535)
      self.assertEqual(usable_panda_states(reader.pandaStates, valid=True), [])

  def test_bad_board_does_not_shift_other_board_indices(self):
    msg = log.Event.new_message(valid=True)
    states = msg.init('pandaStates', 2)
    states[0] = event(profile='current').pandaStates[0]
    states[1] = event(profile='legacyF4v17', observation=True, missing=MISSING).pandaStates[0]
    self.assertEqual(usable_panda_states(states, valid=True), [])

  def test_serialized_metadata_and_empty_batch(self):
    msg = event(profile='legacyF4v17', observation=True, missing=MISSING)
    with log.Event.from_bytes(msg.to_bytes()) as reader:
      self.assertEqual(usable_panda_states(reader.pandaStates, valid=reader.valid), [])
    self.assertEqual(usable_panda_states([], valid=True), [])

  def test_required_field_typo_is_an_error(self):
    msg = event()
    with self.assertRaises(ValueError):
      usable_panda_states(msg.pandaStates, valid=True, required_fields=('controlsAlowed',))


if __name__ == '__main__':
  unittest.main()
