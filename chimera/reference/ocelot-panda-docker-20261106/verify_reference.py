"""Offline source receipt/layout/wire checks; no firmware build or USB imports."""
import ast
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent


def verify():
  receipt = json.loads((ROOT / "retrieval.json").read_text())
  for entry in receipt["selected"]:
    data = (ROOT / entry["path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == entry["blob"], entry["path"]

  # Evaluate only the build flag assignments and project dictionary, not SCons.
  targets = {}
  for prefix in ["", "parent-98de83bb/"]:
    path = ROOT / prefix / "firmware/SConscript"
    names = {"PROJECT_FLAGS_F2", "PROJECT_FLAGS_F4", "projects"}
    nodes = [n for n in ast.parse(path.read_text()).body if isinstance(n, ast.Assign) and
             any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    assert len(nodes) == 3
    env = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), env)
    panda = env["projects"]["panda"]
    assert "-DSTM32F413xx" in panda["flags"] and "-DGATEWAY" not in panda["flags"]
    assert panda["main"] == "panda/main.c"
    if prefix:
      assert "-DGATEWAY" in env["projects"]["chimera"]["flags"]
    else:
      assert list(env["projects"]) == ["panda"]
    targets[prefix or "current"] = list(env["projects"])

  # Compile only the extracted packed C health definition; no MCU code is run.
  main = (ROOT / "firmware/panda/main.c").read_text()
  health = re.search(r"struct __attribute__\(\(packed\)\) health_t \{.*?\n\};", main, re.S).group()
  with tempfile.TemporaryDirectory() as directory:
    directory = Path(directory)
    source = directory / "health.c"
    source.write_text('#include <stdint.h>\n#include <stddef.h>\n#include <stdio.h>\n' + health +
                      '\nint main(void) { printf("%zu %zu\\n", sizeof(struct health_t), ' +
                      'offsetof(struct health_t, safety_param_pkt)); return 0; }\n')
    subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", str(source), "-o", str(directory / "health")], check=True)
    layout = subprocess.check_output([str(directory / "health")], text=True).strip()
    assert layout == "43 39", layout
    (directory / "stm32f4xx.h").write_text("")
    macros = subprocess.check_output(["cc", "-E", "-dM", "-x", "c", "-DSTM32F4", "-I", str(directory),
                                      str(ROOT / "firmware/config.h")], text=True)
    assert re.search(r"^#define PANDA[ \t]*$", macros, re.M) and "#define GATEWAY" not in macros

  # Extract the actual pure parser and sender with an in-memory sink. Never
  # import firmware.python or instantiate its Panda/USB/DFU constructors.
  host = ROOT / "firmware/python/__init__.py"
  tree = ast.parse(host.read_text())
  parser = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "parse_can_buffer")
  cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Panda")
  sender = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "can_send_many")
  env = {"struct": struct, "DEBUG": False, "CAN_SEND_TIMEOUT_MS": 10}
  exec(compile(ast.Module(body=[parser, sender], type_ignores=[]), str(host), "exec"), env)
  writes = []
  handle = SimpleNamespace(bulkWrite=lambda ep, data, timeout: writes.append((ep, data, timeout)))
  fake = SimpleNamespace(wifi=False, _handle=handle)
  vectors = []
  for bus in range(3):
    for address in [0, 1, 0x123, 0x7FF, 0x800, 0x12345, 0x1FFFFFFF]:
      for length in range(9):
        data = bytes((i * 19 + length) & 255 for i in range(length))
        vectors.append((address, None, data, bus))
  env["can_send_many"](fake, vectors)
  assert len(writes) == 1 and writes[0][0] == 3 and writes[0][2] == 10
  wire = writes[0][1]
  assert len(wire) == 189 * 16
  assert env["parse_can_buffer"](wire) == [(address, 0, data, bus) for address, _, data, bus in vectors]
  for index, (address, _, data, bus) in enumerate(vectors):
    rir = (address << 3) | 5 if address >= 0x800 else (address << 21) | 1
    assert wire[index * 16:(index + 1) * 16] == struct.pack("<II8s", rir, len(data) | (bus << 4), data)
  # The Python health parser's unsigned H disagrees with the C signed int16_t.
  assert struct.calcsize("<IIIIIIIIBBBBBBBHBB") == 43
  signed_sample = struct.pack("<8I7Bh2B", *([0] * 15), -1, 0, 0)
  assert struct.unpack("<IIIIIIIIBBBBBBBHBB", signed_sample)[15] == 65535
  assert struct.unpack("<8I7Bh2B", signed_sample)[15] == -1
  return {"result": "pass", "verified_source_files": len(receipt["selected"]), "targets": targets,
          "health_bytes": 43, "safety_param_offset": 39, "legacy_sender_parser_vectors": len(vectors),
          "legacy_can_bytes": len(wire), "config_preprocessor": "STM32F4 without GATEWAY defines PANDA",
          "signedness_fixture": "C -1 versus legacy Python 65535", "python": sys.version.split()[0],
          "scope": "source/host-only; no full firmware build, Docker, USB imports, devices or hardware tests"}


if __name__ == "__main__":
  print(json.dumps(verify(), indent=2))
