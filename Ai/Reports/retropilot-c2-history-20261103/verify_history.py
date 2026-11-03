"""Verify pinned history/path coverage and retained REA evidence offline."""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
  return json.loads((ROOT / name).read_text())


def main():
  parent, history, coverage = read('parent-compare.json'), read('commit-history.json'), read('coverage.json')
  assert parent['total_commits'] == len(parent['commits']) == len(history) == 35
  assert {c['sha'] for c in parent['commits']} == {c['sha'] for c in history}
  assert coverage['parent_tip'] == history[-1]['sha'] == 'b9a942efd3cb210127bb5efb5cf9ccf6a811c728'
  assert coverage['parent_base'] == parent['base_commit']['sha'] == 'da2ea41241f16c4b0e80a52fdc40ed57becd185b'
  assert sum(c['date'].startswith('2025') for c in history) == 28
  records = coverage['records']
  assert len({(r['repo'], r['path']) for r in records}) == len(records) == 82
  assert {r['path'] for r in records if r['repo'] == 'parent'} == {f['path'] for c in history for f in c['files']}
  assert {r['path'] for r in records if r['repo'] == 'parent' and r['at_tip']} == {f['filename'] for f in parent['files']}
  assert len(parent['files']) == 50
  for name, count, tip in (('panda', 2, '9e6d47f63675d5a45170ae7972c24412034dc136'),
                           ('cereal', 3, 'a7193d0f0e472f90709e6671ce6ff01d1534c2a5'),
                           ('opendbc', 43, '6b90fafe59e81822bfae58e4ecb080248e9de40d')):
    comparison = read(f'{name}-compare.json')
    assert comparison['total_commits'] == len(comparison['commits']) == count
    assert comparison['commits'][-1]['sha'] == tip
    assert {r['path'] for r in records if r['repo'] == name} == {f['filename'] for f in comparison['files']}
  for record in records:
    assert record['family'] and record['status'] and record['modern_path'] and record['disposition']
  for name in ('rea-chimera-symbols.json', 'rea-chimera-disassembly.json'):
    evidence = read(name)['structuredContent']
    result = evidence['normalized_result']
    assert evidence['evidence_id'] and evidence['provider']['id'] == 'gnu.objdump'
    assert result['exit_code'] == 0 and result['completion_status'] == 'complete' and not result['output_truncated']
    assert result['artifact_sha256_after'] == '5ae9b4f6ea99e569028d271c4ec9c2ce59cd11375b5482adbd0781f3480e20b8'
    assert not result['artifact_changed']
  source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.json')}
  print(json.dumps({'result': 'pass', 'parent_commits': 35, 'parent_final_paths': 50, 'parent_history_paths': 64,
                    'total_mapped_paths': 82, 'submodule_commits': {'panda': 2, 'cereal': 3, 'opendbc': 43},
                    'source_sha256': source_hashes}, indent=2))


if __name__ == '__main__':
  main()
