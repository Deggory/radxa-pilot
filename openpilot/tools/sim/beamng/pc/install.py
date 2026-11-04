#!/usr/bin/env python3
"""Install only the read-only protocol into the BeamNG user folder."""
import argparse
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import shutil


def install(user_folder, enable=False):
  source = Path(__file__).resolve().parent / 'mod'
  target = user_folder / 'mods/unpacked/radxa_retropilot'
  files = {}
  stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
  for path in source.rglob('*'):
    if path.is_file():
      dest = target / path.relative_to(source)
      dest.parent.mkdir(parents=True, exist_ok=True)
      if dest.exists() and dest.read_bytes() != path.read_bytes():
        shutil.copy2(dest, dest.with_name(dest.name + '.backup-' + stamp))
      shutil.copy2(path, dest)
      files[str(dest)] = hashlib.sha256(dest.read_bytes()).hexdigest()
  if enable:
    settings = user_folder / 'settings/settings.json'
    data = json.loads(settings.read_text()) if settings.exists() else {}
    if not data.get('protocols_others_enabled'):
      settings.parent.mkdir(parents=True, exist_ok=True)
      if settings.exists():
        shutil.copy2(settings, settings.with_name('settings.json.backup-' + stamp))
      data['protocols_others_enabled'] = True
      settings.write_text(json.dumps(data, indent=2) + '\n')
  return {'installed': files, 'others_protocols_enabled': enable,
          'next': 'Open BeamNG, select vehicle, enable Other protocols if needed, then Ctrl+R; run gateway.py.'}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--user-folder', type=Path, required=True)
  parser.add_argument('--enable', action='store_true', help='Enable Other protocols; may also enable other installed protocol mods')
  args = parser.parse_args()
  print(json.dumps(install(args.user_folder, args.enable), indent=2))


if __name__ == '__main__':
  main()
