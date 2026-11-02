#!/usr/bin/env python3
"""One-time administrator installation of the fixed Q8B performance lease."""
import hashlib
import os
from pathlib import Path
import pwd
import re
import stat
import subprocess
import tempfile

DESTINATION = Path('/usr/local/libexec/sunnypilot-q8b-performance')
RULE = Path('/etc/sudoers.d/sunnypilot-q8b-performance')


def install():
  if os.geteuid() != 0:
    raise RuntimeError('Run this installer once with sudo, from a local terminal')
  user = os.environ.get('SUDO_USER', '')
  if not re.fullmatch(r'[a-z_][a-z0-9_-]*', user) or pwd.getpwnam(user).pw_uid == 0:
    raise RuntimeError('Run using sudo from the project owner account')
  source = Path(__file__).resolve().with_name('performance_guard.py')
  if source.stat().st_uid != pwd.getpwnam(user).pw_uid:
    raise RuntimeError('Helper source must belong to the requesting project owner')
  payload = source.read_bytes()
  compile(payload, str(source), 'exec')
  rule = f'{user} ALL=(root) NOPASSWD: {DESTINATION} guard\n'
  os.umask(0o077)
  # Validate existing ancestors before creating anything below them.
  for parent in set(DESTINATION.parents) | set(RULE.parents):
    if parent == DESTINATION.parent and not parent.exists():
      continue
    info = parent.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid or info.st_mode & 0o022:
      raise RuntimeError(f'Administrator-owned non-writable directory required: {parent}')
  if not DESTINATION.parent.exists():
    # Ancestors are trusted; create with the final public read/execute mode.
    previous_mask = os.umask(0o022)
    try:
      DESTINATION.parent.mkdir(mode=0o755)
    finally:
      os.umask(previous_mask)
  if DESTINATION.is_symlink() or RULE.is_symlink():
    raise RuntimeError('Refusing symlink installation destinations')
  for target in (DESTINATION, RULE):
    if target.exists():
      raise RuntimeError(f'{target} already exists; review the installed version before replacing it')
  with tempfile.TemporaryDirectory(prefix='.sunnypilot-', dir=DESTINATION.parent) as helper_dir, \
       tempfile.TemporaryDirectory(prefix='.sunnypilot-', dir=RULE.parent) as rule_dir:
    staged_rule = Path(rule_dir) / 'sudoers'
    staged_rule.write_text(rule)
    staged_rule.chmod(0o440)
    subprocess.run(['/usr/sbin/visudo', '-cf', str(staged_rule)], check=True)
    helper = Path(helper_dir) / 'helper'
    helper.write_bytes(payload)
    helper.chmod(0o755)
    os.link(helper, DESTINATION)  # Atomic publication, refuses any existing destination.
    rule_installed = False
    try:
      os.link(staged_rule, RULE)
      rule_installed = True
      subprocess.run(['/usr/sbin/visudo', '-c'], check=True)
    except BaseException:
      if rule_installed:
        RULE.unlink()
      DESTINATION.unlink()
      raise
  print(f'Installed fixed Q8B performance lease for {user}; no password saved.')
  print(f'Helper SHA256: {hashlib.sha256(payload).hexdigest()}')
  print('Only this helper guard action is password-free; normal sudo policy is unchanged.')


if __name__ == '__main__':
  install()
