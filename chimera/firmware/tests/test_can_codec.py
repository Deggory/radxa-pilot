# SPDX-License-Identifier: MIT
import ast
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]


class CanCodecTests(unittest.TestCase):
  def test_sanitized_codec_and_current_panda_wire_interoperability(self):
    with tempfile.TemporaryDirectory() as directory:
      executable = Path(directory) / "can_codec_test"
      command = ["cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                 "-fsanitize=address,undefined", "-I", str(ROOT), "-I", str(PROJECT / "opendbc_repo/opendbc/safety"),
                 str(ROOT / "can_codec.c"), str(ROOT / "tests/can_codec_test.c"), "-o", str(executable)]
      compiled = subprocess.run(command, capture_output=True, text=True)
      self.assertEqual(compiled.returncode, 0, compiled.stderr)
      result = subprocess.run([str(executable)], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)

    # Evaluate only actual pure wire functions/constants: no Panda import,
    # constructor, USB library, hardware enumeration or initialization writes.
    source = PROJECT / "panda/python/__init__.py"
    functions = {"calculate_checksum", "pack_can_buffer", "unpack_can_buffer"}
    constants = {"CANPACKET_HEAD_SIZE", "DLC_TO_LEN", "LEN_TO_DLC"}
    nodes = [node for node in ast.parse(source.read_text()).body if
             (isinstance(node, ast.FunctionDef) and node.name in functions) or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in node.targets))]
    self.assertEqual(len(nodes), 6)
    panda = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), panda)
    packed, unpacked = 0, 0
    for line in result.stdout.splitlines():
      if line.startswith("SUMMARY"):
        print(line)
        continue
      kind, address, bus, length, extended, status, raw = line.split()
      self.assertEqual(kind, "V")
      address, bus, length, extended, status = int(address, 16), int(bus), int(length), int(extended), int(status)
      wire = bytes.fromhex(raw)
      payload = wire[6:]
      self.assertEqual(len(payload), length)
      messages, tail = panda["unpack_can_buffer"](wire)
      self.assertEqual(messages, [(address, payload, bus + (0, 128, 192)[status])])
      self.assertEqual(tail, b"")
      unpacked += 1
      if status == 0 and extended == int(address >= 0x800):
        self.assertEqual(panda["pack_can_buffer"]([(address, payload, bus)])[0], wire)
        packed += 1
    self.assertEqual((packed, unpacked), (189, 648))
    print(f"Current Panda source: {packed} exact pack vectors, {unpacked} unpack vectors; no hardware calls")


if __name__ == "__main__":
  unittest.main()
