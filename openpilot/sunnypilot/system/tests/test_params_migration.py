"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openpilot.common.params import Params
from openpilot.common.test import OpenpilotTestCase
from openpilot.sunnypilot.system.params_migration import _migrate_car_platform_bundle, _migrate_model_bundle_slots


class TestRetroPilotPlatformMigration(unittest.TestCase):
  def test_saved_c2_platform_maps_to_modern_platform(self):
    with tempfile.TemporaryDirectory() as tmp:
      params = Params(str(Path(tmp) / 'params'))
      old_bundle = {'platform': 'RETROPILOT RETROFIT', 'brand': 'retropilot', 'model': 'Retrofit', 'name': 'Owner profile'}
      params.put('CarPlatformBundle', old_bundle, block=True)
      car_list = Path(tmp) / 'car_list.json'
      car_list.write_text(json.dumps({}))
      with patch('openpilot.sunnypilot.system.params_migration.CAR_LIST_JSON_OUT', str(car_list)):
        _migrate_car_platform_bundle(params)
      self.assertEqual(params.get('CarPlatformBundle'), {**old_bundle, 'platform': 'RETROPILOT_RETROFIT'})

  def test_current_platform_and_profile_metadata_are_preserved(self):
    for platform in ('RETROPILOT_RETROFIT', 'MOCK'):
      with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
        params = Params(str(Path(tmp) / 'params'))
        bundle = {'platform': platform, 'name': 'Existing profile'}
        params.put('CarPlatformBundle', bundle, block=True)
        _migrate_car_platform_bundle(params)
        self.assertEqual(params.get('CarPlatformBundle'), bundle)


class TestModelBundleSlotMigration(OpenpilotTestCase):
  """Pre-split, a chestnut user's big-model selection lived in the single ActiveBundle.
  The migration seeds both slots; per-source validation later drops whichever does not
  match its own manifest."""

  def test_seeds_chestnut_slot_from_active_bundle(self):
    params = Params()
    bundle = {"ref": "big", "minimumSelectorVersion": 18}
    params.put("ModelManager_ActiveBundle", bundle, block=True)
    _migrate_model_bundle_slots(params)
    assert params.get("ModelManager_ActiveBundleChestnut") == bundle
    assert params.get("ModelManager_ActiveBundle") == bundle

  def test_noop_when_chestnut_slot_already_set(self):
    params = Params()
    params.put("ModelManager_ActiveBundle", {"ref": "small"}, block=True)
    params.put("ModelManager_ActiveBundleChestnut", {"ref": "big"}, block=True)
    _migrate_model_bundle_slots(params)
    assert params.get("ModelManager_ActiveBundleChestnut") == {"ref": "big"}

  def test_noop_when_no_selection(self):
    params = Params()
    _migrate_model_bundle_slots(params)
    assert params.get("ModelManager_ActiveBundleChestnut") is None
