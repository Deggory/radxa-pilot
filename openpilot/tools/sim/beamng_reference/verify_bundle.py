"""Verify this source snapshot without importing or running upstream code."""
import hashlib
import json
from pathlib import Path


def main():
  root = Path(__file__).resolve().parent
  manifest = json.loads((root / 'MANIFEST.json').read_text())
  files = manifest['files']
  expected = {item['path'] for item in files}
  if len(expected) != len(files):
    raise ValueError('duplicate manifest paths')
  actual = {str(path.relative_to(root)) for path in (root / 'upstream').rglob('*') if path.is_file() or path.is_symlink()}
  if actual != expected:
    raise ValueError(f'snapshot coverage differs: missing={expected - actual}, extra={actual - expected}')
  total = 0
  for item in files:
    path = root / item['path']
    if path.is_symlink() or not path.resolve().is_relative_to(root / 'upstream'):
      raise ValueError('snapshot path is not a contained regular file')
    data = path.read_bytes()
    git_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if (len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256'] or
        git_blob != item['git_blob_sha1'] or path.stat().st_mode & 0o777 != int(item['source_mode'], 8) & 0o777):
      raise ValueError(f"source identity changed: {item['path']}")
    total += len(data)
  print(json.dumps({'result': 'pass', 'files': len(files), 'bytes': total, 'source_commit': manifest['source_commit']}))


if __name__ == '__main__':
  main()
