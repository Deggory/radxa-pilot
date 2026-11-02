import copy
import unittest

from openpilot.selfdrive.modeld.npu.integer_io import verify_encoding_evidence, verify_encodings


class TestEncodingPreservation(unittest.TestCase):
  def test_stale_sidecar_cannot_hide_changed_internal_dlc_encoding(self):
    original = {'param_encodings': {}, 'activation_encodings': {'internal': [{'bitwidth': 8, 'scale': .125, 'offset': -128}]}}
    changed = copy.deepcopy(original)
    changed['activation_encodings']['internal'][0]['scale'] = .13
    with self.assertRaisesRegex(ValueError, 'does not match the actual saved DLC'):
      verify_encoding_evidence(original, original, changed, original, {})

  def test_only_boundary_aliases_can_change(self):
    before = {'param_encodings': {'weight': [{'bitwidth': 8, 'scale': .012, 'offset': -128}]},
              'activation_encodings': {'desire_converted': [{'bitwidth': 8, 'scale': 1 / 255, 'offset': 0}],
                                       'internal': [{'bitwidth': 8, 'scale': .003, 'offset': -10}]}}
    after = copy.deepcopy(before)
    after['activation_encodings']['desire'] = after['activation_encodings'].pop('desire_converted')
    aliases = {'desire_converted': 'desire'}
    verify_encodings(before, after, aliases)
    before['activation_encodings']['desire'] = [{'bitwidth': 32, 'dtype': 'float'}]
    verify_encodings(before, after, aliases)
    for group, key in [('param_encodings', 'weight'), ('activation_encodings', 'internal'), ('activation_encodings', 'desire')]:
      changed = copy.deepcopy(after)
      changed[group][key][0]['scale'] *= 1.01
      with self.subTest(tensor=key), self.assertRaises(ValueError):
        verify_encodings(before, changed, aliases)

  def test_alias_collision_is_rejected(self):
    before = {'param_encodings': {}, 'activation_encodings': {'first': [], 'second': []}}
    with self.assertRaises(ValueError):
      verify_encodings(before, {'param_encodings': {}, 'activation_encodings': {'new': []}}, {'first': 'new', 'second': 'new'})
