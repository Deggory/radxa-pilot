"""Offline source-contract checks. No Panda construction or hardware enumeration."""

import ast
import ctypes
import hashlib
import io
import json
from pathlib import Path
import random
import re
import struct
import subprocess
import tempfile
import types
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[3]
WORKSPACE = PROJECT.parent
OUT = Path(__file__).resolve().parent


def functions(path, names, namespace):
  tree = ast.parse(path.read_text())
  nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
  assert len(nodes) == len(names)
  exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
  return namespace


def layout(path, struct_name='health_t'):
  src = path.read_text()
  prefix = r'(?:struct\s+__attribute__\(\(packed\)\)\s+' + struct_name
  suffix = r'\s*\{|typedef\s+struct\s+__attribute__\(\(packed\)\)\s*\{)(.*?)\}'
  body = re.search(prefix + suffix, src, re.S)[1]
  types = {'uint8_t': 'B', 'uint16_t': 'H', 'int16_t': 'h', 'uint32_t': 'I'}
  fields = []
  fmt = '<'
  for line in body.splitlines():
    line = line.split('//')[0].strip()
    if not line:
      continue
    m = re.fullmatch(r'(\w+)\s+(\w+);', line)
    assert m and m[1] in types, line
    fields.append({'name': m[2], 'offset': struct.calcsize(fmt), 'type': m[1]})
    fmt += types[m[1]]
  return {'bytes': struct.calcsize(fmt), 'format': fmt, 'fields': fields}


def connection_writes():
  path = PROJECT / 'panda/python/__init__.py'
  tree = ast.parse(path.read_text())
  cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Panda')
  names = {'connect', 'get_packets_versions', 'set_heartbeat_disabled', 'set_power_save', 'can_reset_communications', 'set_canfd_auto', 'set_can_speed_kbps'}
  methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in names]
  assert len(methods) == len(names)
  ns = {'PANDA_CAN_CNT': 3, 'struct': struct, 'logger': types.SimpleNamespace(debug=lambda *a: None)}
  exec(compile(ast.Module(body=methods, type_ignores=[]), str(path), 'exec'), ns)

  class FakeHandle:
    def __init__(self, calls):
      self.calls = calls

    def controlRead(self, req_type, request, value, index, length):
      self.calls.append(['IN', request, value, index, length])
      return b''  # Chimera has no implemented 0xDD packet-version response.

    def controlWrite(self, req_type, request, value, index, data):
      self.calls.append(['OUT', request, value, index])

  class FakePanda:
    REQUEST_IN = 0xC0
    REQUEST_OUT = 0x40
    _connect_serial = 'FAKE'
    _can_speed_kbps = 500

    def __init__(self, handle, disable_checks):
      self.fake_handle = handle
      self._disable_checks = disable_checks

    def close(self):
      return None

    def usb_connect(self, *args, **kwargs):
      return None, self.fake_handle, 'FAKE', False

    def spi_connect(self, *args):
      raise AssertionError('Unexpected SPI path')

  for name in names:
    setattr(FakePanda, name, ns[name])
  ns['Panda'] = FakePanda
  records = []
  for disable_checks in (True, False):
    calls = []
    fake = FakePanda(FakeHandle(calls), disable_checks)
    fake.connect()
    assert (fake.health_version, fake.can_version) == (0, 0)
    writes = [c[1:] for c in calls if c[0] == 'OUT']
    expected = (
      ([[0xF8, 0, 0], [0xE7, 0, 0]] if disable_checks else []) + [[0xC0, 0, 0]] + [[0xE8, b, 0] for b in range(3)] + [[0xDE, b, 5000] for b in range(3)]
    )
    assert writes == expected, (writes, expected)
    records.append({'disable_checks': disable_checks, 'versions': [0, 0], 'calls': calls, 'write_count': len(writes)})
  return records


def main():
  old = functions(WORKSPACE / 'ocelot/firmware/python/__init__.py', {'parse_can_buffer'}, {'struct': struct, 'DEBUG': False})
  dlc = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64]
  modern = functions(
    PROJECT / 'panda/python/__init__.py',
    {'calculate_checksum', 'pack_can_buffer', 'unpack_can_buffer'},
    {'CANPACKET_HEAD_SIZE': 6, 'DLC_TO_LEN': dlc, 'LEN_TO_DLC': {n: i for i, n in enumerate(dlc)}},
  )
  mailbox_vectors = []
  modern_vectors = []
  for bus in range(3):
    for address in (0, 0x50, 0x301, 0x7FF, 0x800, 0x18FF0101, 0x1FFFFFFF):
      for size in range(9):
        data = bytes((address + i) & 255 for i in range(size))
        rir = (address << (3 if address >= 0x800 else 21)) | (4 if address >= 0x800 else 0)
        raw = struct.pack('<II8s', rir, size | (bus << 4), data)
        assert old['parse_can_buffer'](raw) == [(address, 0, data, bus)]
        mailbox_vectors.append((address, bus, size))
      for size in dlc:
        data = bytes((address + i) & 255 for i in range(size))
        raw = bytes(modern['pack_can_buffer']([(address, data, bus)])[0])
        assert len(raw) == 6 + size
        decoded, tail = modern['unpack_can_buffer'](raw)
        assert decoded == [(address, data, bus)] and not tail
        for split in range(len(raw) + 1):
          first, tail = modern['unpack_can_buffer'](raw[:split])
          second, tail = modern['unpack_can_buffer'](tail + raw[split:])
          assert first + second == decoded and not tail
        for offset in range(len(raw)):
          for bit in range(8):
            damaged = bytearray(raw)
            damaged[offset] ^= 1 << bit
            # A changed DLC can make the packet incomplete, rather than yield
            # a checksum failure. It must never produce an accepted frame.
            try:
              accepted, _ = modern['unpack_can_buffer'](damaged)
              assert not accepted, ('corrupt packet accepted', offset, bit)
            except AssertionError as error:
              if str(error) != 'CAN packet checksum incorrect':
                raise
        modern_vectors.append((address, bus, size))
  layouts = {
    'chimera': layout(WORKSPACE / 'ocelot/firmware/chimera/main.c'),
    'legacy_demo': layout(WORKSPACE / 'steer_actuator_demo/openpilot_demo/source/selfdrive/boardd/panda.h'),
    'c2': layout(WORKSPACE / 'retropilot/panda/c2_firmware/health.h'),
    'modern': layout(PROJECT / 'panda/board/health.h'),
  }
  assert {k: v['bytes'] for k, v in layouts.items()} == {'chimera': 43, 'legacy_demo': 43, 'c2': 50, 'modern': 49}
  report = {
    'kind': 'offline source,codec and freshly compiled native comms tests',
    'hardware_access': False,
    'mailbox_vectors': len(mailbox_vectors),
    'modern_vectors_all_splits_and_single_bit_corruptions': len(modern_vectors),
    'health_layouts': layouts,
    'modern_can_health_layout': layout(PROJECT / 'panda/board/health.h', 'can_health_t'),
    'modern_constructor_fake_handle_calls': connection_writes(),
    'version_hashes': {
      p: int.from_bytes(hashlib.sha256((PROJECT / p).read_bytes().replace(b'\r', b'')).digest()[:4], 'little')
      for p in ['panda/board/health.h', 'opendbc_repo/opendbc/safety/can.h']
    },
  }
  random.seed(20261105)
  with tempfile.TemporaryDirectory(prefix='panda-contract-native-') as temp:
    lib = Path(temp) / 'libpanda.so'
    command = [
      'gcc',
      '-shared',
      '-fPIC',
      '-fno-builtin',
      '-std=gnu11',
      '-Wno-pointer-to-int-cast',
      '-I' + str(PROJECT / 'panda'),
      '-I' + str(PROJECT / 'panda/board'),
      '-I' + str(PROJECT / 'opendbc_repo'),
      str(PROJECT / 'panda/tests/libpanda/panda.c'),
      '-o',
      str(lib),
    ]
    build = subprocess.run(command, capture_output=True, text=True)
    report['native_build'] = {
      'command': command,
      'exit_code': build.returncode,
      'output': build.stdout + build.stderr,
      'compiler_version': subprocess.check_output(['gcc', '--version'], text=True).splitlines()[0],
    }
    assert build.returncode == 0, build.stderr
    report['native_build']['library_sha256'] = hashlib.sha256(lib.read_bytes()).hexdigest()
    real_cdll = ctypes.CDLL

    def load(path, *args, **kwargs):
      return real_cdll(str(lib) if str(path).endswith('/panda/tests/libpanda/libpanda.so') else path, *args, **kwargs)

    with patch('ctypes.CDLL', side_effect=load):
      suite = unittest.defaultTestLoader.loadTestsFromNames(
        [
          'panda.tests.usbprotocol.test_pandalib',
          'panda.tests.usbprotocol.test_comms',
          'openpilot.selfdrive.pandad.tests.test_chimera',
          'openpilot.selfdrive.pandad.tests.test_chimera_protocol',
        ]
      )
      output = io.StringIO()
      result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
      report['existing_tests'] = {'run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped)}
      (OUT / 'tests.txt').write_text(output.getvalue())
      assert result.wasSuccessful(), output.getvalue()
  (OUT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
  print(
    json.dumps(
      {
        'result': 'pass',
        'mailbox_vectors': len(mailbox_vectors),
        'modern_vectors': len(modern_vectors),
        'existing_tests': report['existing_tests'],
        'constructor_fake_write_counts': [v['write_count'] for v in report['modern_constructor_fake_handle_calls']],
        'health_bytes': {k: v['bytes'] for k, v in layouts.items()},
      }
    )
  )


if __name__ == '__main__':
  main()
