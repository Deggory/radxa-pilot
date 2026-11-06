"""Execute production consumer methods/branches with Cereal data, without daemons."""
import ast
import copy
import unittest
from pathlib import Path
from types import SimpleNamespace

from openpilot.cereal import log
from openpilot.selfdrive.pandad.panda_state import CONTROL_FIELDS, IGNITION_FIELDS, usable_panda_states
from openpilot.selfdrive.pandad.tests.test_panda_state_availability import event, MISSING
from openpilot.system.hardware.panda_state import panda_power_state

ROOT = Path(__file__).resolve().parents[4]
IGNORED = (log.PandaState.schema.fields['safetyModel'].schema.enumerants['silent'],
           log.PandaState.schema.fields['safetyModel'].schema.enumerants['noOutput'])


class Samples:
  def __init__(self, msg, alive=True):
    self.msg = msg
    self.valid = {'pandaStates': msg.valid}
    self.alive = {'pandaStates': alive}
    self.updated = {'pandaStates': True}
    self.frame = 2000

  def __getitem__(self, name):
    assert name == 'pandaStates'
    return self.msg.pandaStates

  def update(self, _):
    pass


def tree(path):
  return ast.parse((ROOT / path).read_text())


def method(path, name, globals_):
  node = next(n for n in ast.walk(tree(path)) if isinstance(n, ast.FunctionDef) and n.name == name)
  node = copy.deepcopy(node)
  namespace = dict(globals_)
  exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), path, 'exec'), namespace)
  return namespace[name]


class PandaConsumerTests(unittest.TestCase):
  def test_core_and_mads_mismatch_on_unavailable_or_stale_data(self):
    common = {'usable_panda_states': usable_panda_states, 'CONTROL_FIELDS': CONTROL_FIELDS, 'IGNORED_SAFETY_MODES': IGNORED,
              'messaging': SimpleNamespace(recv_one=lambda _: None)}
    core = method('openpilot/selfdrive/selfdrived/selfdrived.py', 'data_sample', common)
    mads = method('openpilot/sunnypilot/mads/mads.py', 'data_sample', common)
    for msg, alive, rejected in [(event(profile='current'), True, False),
                                 (event(profile='legacyF4v17', observation=True, missing=MISSING), True, True),
                                 (event(profile='current'), False, True), (event(valid=False), True, True)]:
      sm = Samples(msg, alive)
      control = SimpleNamespace(sm=sm, car_state_sock=None, CS_prev=object(), initialized=True, enabled=True, mismatch_counter=0)
      core(control)
      self.assertEqual(control.mismatch_counter, int(rejected))
      lateral = SimpleNamespace(selfdrive=SimpleNamespace(sm=sm, enabled=False), active=True, lateral_mismatch_counter=0)
      mads(lateral)
      self.assertEqual(lateral.lateral_mismatch_counter, int(rejected))
    msg = event(profile='current', missing=['controlsAllowedLateral'])
    lateral = SimpleNamespace(selfdrive=SimpleNamespace(sm=Samples(msg), enabled=False), active=True, lateral_mismatch_counter=0)
    mads(lateral)
    self.assertEqual(lateral.lateral_mismatch_counter, 1)

  def test_manager_ignition_assignment_uses_valid_live_metadata(self):
    source = tree('openpilot/system/manager/manager.py')
    assignment = next(n for n in ast.walk(source) if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Tuple) and ast.unparse(n.targets[0]) == '(ignition, _)')
    code = compile(ast.Module(body=[assignment], type_ignores=[]), 'manager-ignition', 'exec')
    for msg, alive, expected in [(event(), True, True), (event(valid=False), True, False),
                                 (event(profile='legacyF4v17', observation=True, missing=MISSING), True, False),
                                 (event(), False, False)]:
      env = {'sm': Samples(msg, alive), 'panda_power_state': panda_power_state}
      exec(code, env)
      self.assertEqual(env['ignition'], expected)

  def test_ui_clears_observation_invalid_and_stale_ignition(self):
    source = tree('openpilot/selfdrive/ui/ui_state.py')
    branch = next(n for n in ast.walk(source) if isinstance(n, ast.If)
                  and ast.unparse(n.test) == "self.sm.updated['pandaStates']")
    code = compile(ast.Module(body=[branch], type_ignores=[]), 'ui-panda-branch', 'exec')
    for msg, alive, expected in [(event(), True, True), (event(valid=False), True, False),
                                 (event(profile='legacyF4v17', observation=True, missing=MISSING), True, False),
                                 (event(), False, False)]:
      ui = SimpleNamespace(sm=Samples(msg, alive), panda_type=log.PandaState.PandaType.blackPanda, ignition=True)
      exec(code, {'self': ui, 'log': log, 'usable_panda_states': usable_panda_states, 'IGNITION_FIELDS': IGNITION_FIELDS})
      self.assertEqual(ui.ignition, expected)
      self.assertEqual(ui.panda_type == log.PandaState.PandaType.unknown, not expected)

  def test_core_event_branch_blocks_unusable_batch(self):
    source = tree('openpilot/selfdrive/selfdrived/selfdrived.py')
    function = next(n for n in ast.walk(source) if isinstance(n, ast.FunctionDef) and n.name == 'update_events')
    start = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'panda_states')
    code = compile(ast.Module(body=function.body[start:start + 3], type_ignores=[]), 'core-panda-event-branch', 'exec')
    for msg, expected in [(event(profile='current'), False),
                          (event(profile='legacyF4v17', observation=True, missing=MISSING), True)]:
      state = msg.pandaStates[0]
      control = SimpleNamespace(sm=Samples(msg), events=set(), mismatch_counter=0,
                                CP=SimpleNamespace(safetyConfigs=[state], alternativeExperience=0))
      exec(code, {'self': control, 'usable_panda_states': usable_panda_states, 'CONTROL_FIELDS': CONTROL_FIELDS,
                  'EventName': log.OnroadEvent.EventName, 'log': log, 'DT_CTRL': .01, 'IGNORED_SAFETY_MODES': IGNORED})
      self.assertEqual(log.OnroadEvent.EventName.controlsMismatch in control.events, expected)


if __name__ == '__main__':
  unittest.main()
