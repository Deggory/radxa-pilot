"""Verify the in-project notebook; optionally check this host's upstream reference."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--workspace', type=Path, help='Optional Comma workspace for live reference/index checks')
  args = parser.parse_args()
  memory = Path(__file__).resolve().parent
  project = memory.parent
  assert memory.is_dir() and not (project / 'Ai').is_symlink()
  assert not (memory / '.git').exists(), 'Notebook must use project Git history'
  for name in ('AGENTS.md', 'readme_wat_we_did.md', 'RADXA_PORT.md'):
    assert (project / name).is_file(), name
  docs = list(memory.rglob('*.md'))
  relative_links = 0
  workspace_links = 0
  for doc in docs:
    for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
      if '://' in link or link.startswith('#'):
        continue
      target = Path(link.split('#')[0])
      if target.is_absolute():
        workspace_links += 1
        if args.workspace:
          assert target.exists(), (doc, link)
      else:
        assert (doc.parent / target).exists(), (doc, link)
        relative_links += 1
  result = {'result': 'pass', 'memory_layout': 'regular project directory',
            'documents': len(docs), 'relative_links': relative_links,
            'optional_workspace_links': workspace_links}
  if args.workspace:
    workspace = args.workspace.resolve()
    config = json.loads((workspace / 'q8b/sunnypilot-maintenance/config.json').read_text())
    assert Path(config['port']).resolve() == project
    assert Path(config['vendor']).resolve() == workspace / 'q8b/sunnypilot-upstream'
    index = json.loads((memory / 'Evidence/source-index.json').read_text())
    count = 0
    for repo in index['repositories']:
      actual = subprocess.check_output(['git', '-C', repo['path'], 'rev-parse', 'HEAD'], text=True).strip()
      assert actual == repo['head'], (repo['path'], actual, repo['head'])
      raw = subprocess.check_output(['git', '-C', repo['path'], 'ls-tree', '-r', '-z', 'HEAD'])
      entries = []
      for item in filter(None, raw.split(b'\0')):
        metadata, path = item.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        entries.append({'path': path.decode(), 'mode': mode, 'type': kind, 'oid': oid})
      assert entries == repo['entries'], repo['path']
      count += len(entries)
    result.update(source_repositories=len(index['repositories']), indexed_entries=count)
  print(json.dumps(result, indent=2))


if __name__ == '__main__':
  main()
