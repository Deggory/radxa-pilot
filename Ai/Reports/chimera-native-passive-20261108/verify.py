"""Offline gates for the owner's native original-Chimera receive increment."""
from pathlib import Path
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
WORKSPACE = ROOT.parent
REPORT = Path(__file__).resolve().parent
RESULTS = REPORT / 'run'  # Ignored local output; repeated gates never dirty source.
SOURCE = 'openpilot/selfdrive/pandad/'
NATIVE_TESTS = ['test_pandad_canprotocol', 'test_panda_comms', 'test_panda_identification',
                'test_panda_health', 'test_panda_can_health', 'test_panda_usb', 'test_panda_usb_link',
                'test_panda_usb_can', 'test_chimera_usb', 'test_panda_usb_publish', 'test_panda_state_legacy']


def run(command, *, expected=0, sanitized=False):
  env = os.environ.copy()
  env['PATH'] = str(ROOT / '.venv/bin') + os.pathsep + env['PATH']
  env['PWD'] = str(ROOT)
  if sanitized:
    env['ASAN_OPTIONS'] = 'halt_on_error=1:detect_leaks=1'
    env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
  result = subprocess.run([str(x) for x in command], cwd=ROOT, env=env, text=True, capture_output=True)
  assert result.returncode == expected, (command, result.returncode, result.stdout[-4000:], result.stderr[-4000:])
  return {'command': [str(x) for x in command], 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def save(name, checks):
  RESULTS.mkdir(exist_ok=True)
  (RESULTS / (name + '.json')).write_text(json.dumps({'result': 'pass', 'checks': checks}, indent=2) + '\n')


def native():
  targets = [SOURCE + 'pandad'] + [SOURCE + 'tests/' + name for name in NATIVE_TESTS]
  checks = [run(['.venv/bin/scons', '-j2', *targets])]
  checks += [run([SOURCE + 'tests/' + name]) for name in NATIVE_TESTS]
  # Invalid entry points must fail before USB access, already proved by fake backend tests.
  checks += [run([SOURCE + 'pandad'], expected=2), run([SOURCE + 'pandad', '--usb-status', '', ''], expected=2)]
  save('native', checks)
  print(f'NATIVE CHIMERA VERIFIED: target build, {len(NATIVE_TESTS)} native programs and invalid-entry guards')


def python_checks():
  modules = ['test_usb_startup', 'test_chimera', 'test_chimera_protocol', 'test_chimera_native',
             'test_legacy_state_sources', 'test_panda_state_availability', 'test_panda_consumers']
  modules = ['openpilot.selfdrive.pandad.tests.' + name for name in modules]
  modules += ['openpilot.selfdrive.modeld.thneed_q8b.test_telemetry']
  checks = [run(['.venv/bin/python', '-m', 'unittest', *modules, '-v']),
            run(['.venv/bin/ruff', 'check', SOURCE + 'tests/test_chimera_native.py', str(Path(__file__).relative_to(ROOT))])]
  save('python', checks)
  print('PYTHON REGRESSIONS VERIFIED: protocol, 432 native mailbox/5 health vectors, startup, consumer and telemetry checks')


def sanitizers():
  checks = []
  flags = ['c++', '-std=c++17', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined',
           '-fno-omit-frame-pointer', '-g', '-Iopenpilot', '-I.', '-Iopendbc_repo', '-Imsgq_repo',
           '-Iopenpilot/cereal/gen/cpp']
  with tempfile.TemporaryDirectory(prefix='chimera-native-verify-') as tmp:
    tmp = Path(tmp)
    codec = [SOURCE + 'chimera_usb.cc', SOURCE + 'tests/test_chimera_usb.cc']
    checks.append(run([*flags, *codec, '-o', tmp / 'codec']))
    checks.append(run([tmp / 'codec'], sanitized=True))
    # All changed session/backend/parser units are instrumented; unchanged Panda
    # helpers and shared libraries come from the real build, with fake libusb C API.
    packages = [importlib.import_module(name) for name in ['capnproto', 'json11', 'zeromq', 'libusb']]
    includes = ['-I' + package.INCLUDE_DIR for package in packages]
    libraries = [item for package in packages for item in ['-L' + package.LIB_DIR, '-Wl,-rpath,' + package.LIB_DIR]]
    macros = []
    for macro, path in [('PANDA_HEALTH_VERSION_HASH', 'panda/board/health.h'),
                        ('PANDA_CAN_VERSION_HASH', 'opendbc_repo/opendbc/safety/can.h')]:
      value = int.from_bytes(hashlib.sha256((ROOT / path).read_bytes().replace(b'\r', b'')).digest()[:4], 'little')
      macros.append(f'-D{macro}=0x{value:08x}U')
    sources = [SOURCE + name for name in ['panda_usb.cc', 'panda_identification.cc', 'panda_health.cc',
                                          'panda_usb_can.cc', 'chimera_usb.cc', 'panda_usb_status.cc', 'tests/test_panda_usb.cc']]
    checks.append(run([*flags, *includes, *macros, *sources, SOURCE + 'libpanda.a',
                       'openpilot/common/libcommon.a', 'openpilot/cereal/libcereal.a', *libraries,
                       '-ljson11', '-lzmq', '-lcapnp', '-lkj', '-pthread', '-o', tmp / 'session']))
    checks.append(run([tmp / 'session'], sanitized=True))
    # Mutate copied sources only: the actual tests must catch missing bus checks
    # and accidental receipt/RTR publication rather than simply exercising code.
    original = (ROOT / SOURCE / 'chimera_usb.cc').read_text()
    for name, old, new in [('bus', 'bus >= 3', 'false'),
                           ('receipts', 'if (!remote && !returned)', 'if (!remote || !returned)')]:
      assert old in original
      copied = tmp / (name + '.cc')
      copied.write_text(original.replace(old, new))
      checks.append(run([*flags, copied, SOURCE + 'tests/test_chimera_usb.cc', '-o', tmp / name]))
      checks.append(run([tmp / name], expected=1, sanitized=True))
      assert 'check failed:' in checks[-1]['stderr'], 'negative control must fail an assertion, not its environment'
  save('sanitizers', checks)
  print('SANITIZERS VERIFIED: instrumented codec/session with fake IO; two copied-source regressions rejected')


def preservation():
  baseline = json.loads((REPORT / 'BASELINE.json').read_text())
  manifest = json.loads((ROOT / 'chimera_old/SOURCES.json').read_text())
  for entry in manifest['files']:
    data = (ROOT / 'chimera_old' / entry['destination']).read_bytes()
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
  assert hashlib.sha256((WORKSPACE / 'retropilot/dbc/ocelot_controls.dbc').read_bytes()).hexdigest() == baseline['dbc_sha256']
  for name, status in baseline['preserve'].items():
    assert run(['git', '-C', WORKSPACE / name, 'status', '--porcelain'])['stdout'] == status
  paths = run(['git', 'diff', '--name-only', baseline['head']])['stdout'].splitlines()
  assert all(path.startswith(('Ai/', SOURCE, 'docs/')) or path == '.gitignore' for path in paths), paths
  checks = [run(['.venv/bin/python', 'Ai/verify_memory.py']), run(['git', 'diff', '--check'])]
  teacher = (WORKSPACE / 'Ai/QUESTION_LOG.md').read_text().split('## QA-20261108-25', 1)[1].split('\n---\n', 1)[0]
  student = (ROOT / 'Ai/QUESTIONS.md').read_text().split('## QA-20261108-25', 1)[1].split('\n---\n', 1)[0]
  assert teacher == student
  save('preservation', checks)
  print(f'PRESERVATION VERIFIED: {len(manifest["files"])} original files, canonical DBC, scoped source, notebook and synchronized QA25')


def closeout():
  review = (REPORT / 'REVIEW.md').read_text()
  assert 'No Critical or Required findings remain' in review
  for digest, name in re.findall(r'^([0-9a-f]{64})  (.+)$', review, re.M):
    if not name.startswith('tests/'):
      assert hashlib.sha256((ROOT / SOURCE / name).read_bytes()).hexdigest() == digest, name
  assert not run(['git', 'status', '--porcelain'])['stdout'], 'uncommitted project work'
  assert run(['git', 'rev-parse', 'HEAD'])['stdout'].strip() != json.loads((REPORT / 'BASELINE.json').read_text())['head']
  assert (ROOT / 'docs/CHIMERA_OLD_USB.md').is_file()
  for name in ['native', 'python', 'sanitizers', 'preservation']:
    assert json.loads((RESULTS / (name + '.json')).read_text())['result'] == 'pass'
  print('CLOSEOUT VERIFIED: reviewed source pins, passing evidence, committed project and clean readback')


if __name__ == '__main__':
  actions = {'native': native, 'python': python_checks, 'sanitizers': sanitizers,
             'preservation': preservation, 'closeout': closeout}
  actions[sys.argv[1]]()
