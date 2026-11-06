import unittest

from openpilot.cereal import log
from openpilot.system.hardware.panda_state import panda_power_state


def panda_event(*states, valid=True):
  event = log.Event.new_message(valid=valid)
  pandas = event.init('pandaStates', len(states))
  for panda, fields in zip(pandas, states, strict=True):
    for field, value in fields.items():
      setattr(panda, field, value)
  return event


class TestPandaPowerState(unittest.TestCase):
  def test_invalid_ignition_cannot_start_or_keep_system_onroad(self):
    event = panda_event({'pandaType': 'blackPanda', 'ignitionLine': True, 'harnessStatus': 'normal'})
    state = panda_power_state(event.pandaStates, valid=event.valid)
    self.assertEqual(state, (True, True))
    event.valid = False
    for _ in range(3):
      state = panda_power_state(event.pandaStates, valid=event.valid, in_car=state[1])
      self.assertEqual(state, (False, True))

  def test_empty_updates_clear_ignition_and_retain_shutdown_context(self):
    on = panda_event({'pandaType': 'blackPanda', 'ignitionCan': True, 'harnessStatus': 'flipped'})
    empty = panda_event()
    self.assertEqual(panda_power_state(on.pandaStates, valid=on.valid), (True, True))
    self.assertEqual(panda_power_state(empty.pandaStates, valid=empty.valid, in_car=True), (False, True))

  def test_unknown_board_cannot_assert_ignition_or_harness_presence(self):
    event = panda_event({'pandaType': 'unknown', 'ignitionLine': True, 'ignitionCan': True, 'harnessStatus': 'normal'})
    self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid), (False, False))

  def test_either_ignition_input_on_recognized_board(self):
    for line in (False, True):
      for can in (False, True):
        with self.subTest(line=line, can=can):
          event = panda_event({'pandaType': 'blackPanda', 'ignitionLine': line, 'ignitionCan': can})
          self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid), (line or can, False))

  def test_primary_harness_is_independent_of_ignition(self):
    for harness in ('notConnected', 'normal', 'flipped'):
      event = panda_event({'pandaType': 'blackPanda', 'harnessStatus': harness})
      self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid), (False, harness != 'notConnected'))

  def test_secondary_ignition_and_primary_harness_semantics_preserved(self):
    event = panda_event({'pandaType': 'blackPanda', 'harnessStatus': 'notConnected'},
                        {'pandaType': 'dos', 'ignitionCan': True, 'harnessStatus': 'normal'})
    self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid), (True, False))

  def test_unknown_primary_does_not_hide_secondary_ignition(self):
    event = panda_event({'pandaType': 'unknown', 'harnessStatus': 'normal'},
                        {'pandaType': 'blackPanda', 'ignitionCan': True})
    self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid), (True, False))

  def test_invalid_harness_cannot_replace_last_valid_shutdown_context(self):
    for previous in (False, True):
      event = panda_event({'pandaType': 'blackPanda', 'ignitionLine': True,
                           'harnessStatus': 'notConnected' if previous else 'normal'}, valid=False)
      self.assertEqual(panda_power_state(event.pandaStates, valid=event.valid, in_car=previous), (False, previous))

  def test_unknown_primary_retains_last_valid_harness_context(self):
    event = panda_event({'pandaType': 'unknown', 'ignitionLine': True})
    self.assertEqual(panda_power_state(event.pandaStates, valid=True, in_car=True), (False, True))

  def test_valid_primary_disconnect_replaces_previous_harness_context(self):
    event = panda_event({'pandaType': 'blackPanda', 'harnessStatus': 'notConnected'})
    self.assertEqual(panda_power_state(event.pandaStates, valid=True, in_car=True), (False, False))

  def test_invalid_event_does_not_read_untrusted_fields(self):
    self.assertEqual(panda_power_state(None, valid=False), (False, False))

  def test_serialized_event_validity_and_recovery(self):
    for valid in (False, True):
      event = panda_event({'pandaType': 'dos', 'ignitionLine': True, 'harnessStatus': 'normal'}, valid=valid)
      with log.Event.from_bytes(event.to_bytes()) as reader:
        self.assertEqual(panda_power_state(reader.pandaStates, valid=reader.valid), (valid, valid))



if __name__ == '__main__':
  unittest.main()
