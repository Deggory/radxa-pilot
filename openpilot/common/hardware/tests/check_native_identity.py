"""Generate real schemas, compile identity probes, and decode their C++ messages."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--capnproto-root', type=Path, required=True)
  parser.add_argument('--build-dir', type=Path, required=True)
  args = parser.parse_args()
  repo = Path(__file__).resolve().parents[4]
  for path in (repo, repo / 'opendbc_repo'):
    sys.path.insert(0, str(path))
  from openpilot.cereal import log

  native = args.capnproto_root.resolve()
  build = args.build_dir.resolve()
  gen = build / 'openpilot/cereal/gen/cpp'
  gen.mkdir(parents=True, exist_ok=True)
  env = dict(os.environ, PWD=str(repo))
  env['PATH'] = str(native / 'bin') + os.pathsep + env['PATH']

  def run(command):
    print(shlex.join(map(str, command)), flush=True)
    subprocess.run(list(map(str, command)), cwd=repo, env=env, check=True)

  schemas = ['log', 'deprecated', 'custom', 'car']
  run([native / 'bin/capnp', 'compile', '--src-prefix=openpilot/cereal',
       '--src-prefix=opendbc_repo/opendbc/car', '--import-path=opendbc_repo/opendbc/car',
       '--import-path=openpilot/cereal', f'-oc++:{gen}',
       *[f'openpilot/cereal/{name}.capnp' for name in schemas[:3]], 'opendbc_repo/opendbc/car/car.capnp'])

  includes = [f'-I{build}', f'-I{gen}', f'-I{repo}', f'-I{repo / "openpilot"}', f'-I{native / "include"}']
  objects = []
  for name in schemas:
    obj = build / f'{name}.o'
    run(['g++', '-std=c++20', '-Wall', '-Werror', *includes, '-c', gen / f'{name}.capnp.c++', '-o', obj])
    objects.append(obj)

  checked = 0
  for mode, expected in [('pc', 'pc'), ('radxa', 'radxaQ8b')]:
    binary = build / f'identity-{mode}'
    flags = ['-D__RADXA_Q8B__'] if mode == 'radxa' else []
    run(['g++', '-std=c++20', '-Wall', '-Werror', *includes, *flags,
         repo / 'openpilot/common/hardware/tests/identity.cc', *objects,
         native / 'lib/libcapnp.a', native / 'lib/libkj.a', '-pthread', '-o', binary])
    for field in ('deviceState', 'initData'):
      result = subprocess.run([str(binary), *(['init'] if field == 'initData' else [])],
                              cwd=repo, env=env, check=True, capture_output=True)
      with log.Event.from_bytes(result.stdout) as event:
        actual = str(getattr(event, field).deviceType)
        if actual != expected:
          raise AssertionError(f'{mode}/{field}: expected {expected}, got {actual}')
      print(f'PASS {mode}/{field}: {expected}; board={result.stderr.decode().strip()}', flush=True)
      checked += 1
  print(f'PASS: {checked} C++ to Python device identity round trips', flush=True)


if __name__ == '__main__':
  main()
