import hashlib
import json
import re
import unittest
from pathlib import Path

from openpilot.cereal import log

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / 'chimera/reference/carrot-f4-state-v17'
SOURCE = (ROOT / 'openpilot/selfdrive/pandad/panda_state_legacy.cc').read_text()
HEADER = (ROOT / 'openpilot/selfdrive/pandad/panda_state_legacy.h').read_text()


def normalize(name):
  return re.sub('[^a-z0-9]', '', name.lower().removesuffix('deprecated'))


class TestLegacyStateSources(unittest.TestCase):
  def test_frozen_reference_hashes_and_git_blobs(self):
    manifest = json.loads((REFERENCE / 'SOURCES.json').read_text())
    self.assertEqual(manifest['commit'], '69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7')
    for entry in manifest['files']:
      data = (REFERENCE / entry['path']).read_bytes()
      self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
      self.assertEqual(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(), entry['git_blob'])

  def test_name_matched_safety_ids_and_conflicts(self):
    text = (REFERENCE / 'opendbc_repo/opendbc/safety/safety.h').read_text()
    legacy = {normalize(name): int(code) for name, code in re.findall(r'^#define SAFETY_(\w+) (\d+)U$', text, re.M)}
    legacy['volkswagen'] = legacy.pop('volkswagenmqb')
    current = {normalize(name): code for name, code in log.PandaState.schema.fields['safetyModel'].schema.enumerants.items()}
    expected = {code for name, code in legacy.items() if current.get(name) == code}
    cases = {int(code): normalize(name) for code, name in re.findall(r'case (\d+): return Safety::(\w+);', SOURCE)}
    self.assertEqual(set(cases), expected)
    self.assertEqual(len(expected), 26)
    for code, name in cases.items():
      self.assertEqual(current[name], code)
    self.assertEqual(legacy['stellantis'], current['volkswagenmlb'])
    self.assertEqual(legacy['faw'], current['hongqi'])
    self.assertFalse({25, 26} & expected)

  def test_fault_bit_names_and_unrepresentable_sound_dma(self):
    text = (REFERENCE / 'panda/board/faults_declarations.h').read_text()
    legacy = {int(bit): normalize(name) for name, bit in re.findall(r'^#define FAULT_(\w+)\s+\(1UL << (\d+)\)', text, re.M)}
    current = {value: normalize(name) for name, value in log.PandaState.FaultType.schema.enumerants.items()}
    self.assertEqual({bit: legacy[bit] for bit in range(27)}, current)
    self.assertEqual(legacy[27], 'interruptratesounddma')
    self.assertNotIn(27, current)

  def test_schema_coverage_requires_explicit_unavailable_fields(self):
    unavailable = set(re.findall(r'"(\w+)"', HEADER))
    # Only quoted names inside the metadata array, not include paths.
    self.assertEqual(len(unavailable), 6)
    preview = SOURCE.split('LegacyF4StateError build_legacy_f4_panda_state_preview', 1)[1]
    mapped = {name[0].lower() + name[1:] for name in re.findall(r'state\.(?:set|init)(\w+)\(', preview + HEADER)}
    fields = set(log.PandaState.schema.fields) - {'deprecated'}
    self.assertEqual(mapped | unavailable, fields)
    self.assertFalse(mapped & unavailable)
    can_fields = {name[0].lower() + name[1:] for name in re.findall(r'state\.set(\w+)\(', SOURCE.split('}  // namespace', 1)[0])}
    self.assertEqual(can_fields, set(log.PandaState.schema.fields['canState0'].schema.fields))


if __name__ == '__main__':
  unittest.main()
