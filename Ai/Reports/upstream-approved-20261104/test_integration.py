"""CPU-only checks for the two approved upstream updates; no model or hardware launch."""
import json
from pathlib import Path
from unittest.mock import Mock

from opendbc.car import structs
from openpilot.cereal import custom, log, messaging
from openpilot.common.params import Params
from openpilot.common.realtime import DT_MDL
from openpilot.common.test import OpenpilotTestCase
from openpilot.selfdrive.controls.lib.accel_boost import AccelBoost
from openpilot.selfdrive.controls.lib.longitudinal_planner import LongitudinalPlanner
from openpilot.sunnypilot import PARAMS_UPDATE_PERIOD
from openpilot.sunnypilot.selfdrive.controls.lib.accel_boost import AccelBoostSP
from openpilot.sunnypilot.selfdrive.controls.lib.longitudinal_planner import LongitudinalPlannerSP
from openpilot.sunnypilot.sunnylink.tests.test_settings_changes import _find_item
from openpilot.sunnypilot.sunnylink.tools.compile_settings_ui import DEFAULT_OUT


class TestApprovedIntegration(OpenpilotTestCase):
  def planner(self, longitudinal):
    planner = LongitudinalPlanner(structs.CarParams(openpilotLongitudinalControl=longitudinal), custom.CarParamsSP.new_message())
    # Isolate unrelated alerts; constructor, parameter polling and selector are real.
    planner.e2e_alerts_helper = Mock()
    return planner

  def test_longitudinal_can_select_predictive_boost(self):
    Params().put_bool("AccelBoostSP", True, block=True)
    planner = self.planner(True)
    LongitudinalPlannerSP.update(planner, {})
    self.assertIs(planner.accel_boost, planner.accel_boost_sp)

  def test_stock_longitudinal_cannot_select_predictive_boost(self):
    Params().put_bool("AccelBoostSP", True, block=True)
    planner = self.planner(False)
    LongitudinalPlannerSP.update(planner, {})
    self.assertIsInstance(planner.accel_boost, AccelBoost)

  def test_toggle_off_restores_existing_boost(self):
    Params().put_bool("AccelBoostSP", True, block=True)
    planner = self.planner(True)
    LongitudinalPlannerSP.update(planner, {})
    self.assertIsInstance(planner.accel_boost, AccelBoostSP)
    Params().put_bool("AccelBoostSP", False, block=True)
    for _ in range(int(PARAMS_UPDATE_PERIOD / DT_MDL)):
      LongitudinalPlannerSP.update(planner, {})
    self.assertIsInstance(planner.accel_boost, AccelBoost)

  def model_inputs(self, probabilities):
    msg = messaging.new_message("modelV2")
    msg.modelV2.meta.disengagePredictions.brakePressProbs = probabilities
    msg.modelV2.meta.disengagePredictions.gasPressProbs = probabilities
    msg.modelV2.action.desiredAcceleration = 0.0
    msg.modelV2.action.desiredCurvature = 0.0
    state = messaging.new_message("selfdriveState").selfdriveState
    state.enabled = True
    state.personality = "standard"
    return msg, {"carState": structs.CarState(vEgo=30.0), "selfdriveState": state}

  def test_existing_cereal_model_message_contract(self):
    msg, sm = self.model_inputs([0.0] * 6)
    with log.Event.from_bytes(msg.to_bytes()) as parsed:
      sm["modelV2"] = parsed.modelV2
      boost = AccelBoostSP()
      for _ in range(100):
        result = boost.update(sm, 0.0, 9.0, 9.0)
      self.assertAlmostEqual(result, 0.25)

  def test_missing_model_probabilities_clear_prior_boost(self):
    msg, sm = self.model_inputs([])
    sm["modelV2"] = msg.modelV2
    boost = AccelBoostSP()
    boost.boost = boost.total_boost = 0.25
    self.assertEqual(boost.update(sm, -0.4, 9.0, 9.0), -0.4)
    self.assertEqual((boost.boost, boost.total_boost), (0.0, 0.0))

  def test_settings_capability_rules(self):
    schema = json.loads(Path(DEFAULT_OUT).read_text())
    arc = _find_item(schema, "TorqueBar")
    rule = arc["visibility"][0]
    self.assertEqual(rule, {"type": "not", "condition": {"type": "capability", "field": "device_type", "equals": "mici"}})
    boost = _find_item(schema, "AccelBoostSP")
    self.assertEqual(boost["enablement"], [{"type": "capability", "field": "has_longitudinal_control", "equals": True}])
