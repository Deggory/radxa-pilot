#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline F413 bootstrap build. No signing, flashing or device operations."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
APP = 0x08004000
CONFIG = 0x08020000
ENVELOPE = 136
STACK = 0x2001FFF8
COMPILATION_SOURCES = ("startup.S", "board.c", "main.c", "protocol.c", "can_codec.c", "usb_hw.c", "usb_ep0.c",
                       "usb_time.c", "usb_mmio.c", "usb_driver.c", "boot_facts.c")
SOURCES = (*COMPILATION_SOURCES, "board.h", "protocol.h", "can_codec.h", "usb_hw.h", "usb_ep0.h",
           "usb_time.h", "usb_driver.h", "boot_facts.h", "stm32f413.ld", "build.py")


def command(*args):
  return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def check_vectors(raw):
  if not 512 <= len(raw) <= CONFIG - APP - ENVELOPE:
    raise ValueError("raw image truncated or exceeds reserved application budget")
  vectors = struct.unpack_from("<118I", raw)
  if vectors[0] != STACK:
    raise ValueError("initial stack does not preserve legacy boot flag")
  for index, pointer in enumerate(vectors[1:], 1):
    if index in (7, 8, 9, 10, 13):
      if pointer != 0:
        raise ValueError("reserved core vector is nonzero")
    elif not pointer & 1 or not APP + 512 <= pointer & ~1 < APP + len(raw):
      raise ValueError(f"vector {index} is not a Thumb application handler")


def check_elf(elf, raw, prefix):
  header = elf.read_bytes()[:52]
  if header[:7] != b"\x7fELF\x01\x01\x01" or struct.unpack_from("<HH", header, 16) != (2, 40):
    raise ValueError("expected ARM ELF32 little-endian executable")
  undefined = command(prefix + "nm", "--undefined-only", str(elf)).splitlines()
  if undefined:
    raise ValueError(f"undefined symbols: {undefined}")
  symbols = {}
  for line in command(prefix + "nm", "--defined-only", str(elf)).splitlines():
    fields = line.split()
    if len(fields) == 3:
      symbols[fields[2]] = int(fields[0], 16)
  if symbols["chimera_vectors"] != APP or symbols["__stack_top"] != STACK:
    raise ValueError("application or stack origin mismatch")
  reset = struct.unpack_from("<I", raw, 4)[0]
  if reset != symbols["Reset_Handler"] | 1 or struct.unpack_from("<I", header, 24)[0] != reset:
    raise ValueError("ELF entry/reset vector mismatch")
  if symbols["__image_end"] != APP + len(raw):
    raise ValueError("binary extent does not match linker image end")
  loads = []
  for line in command(prefix + "readelf", "--program-headers", "--wide", str(elf)).splitlines():
    fields = line.split()
    if not fields or fields[0] != "LOAD":
      continue
    offset, virtual, physical, size, memory = (int(v, 16) for v in fields[1:6])
    if size and not APP <= physical < physical + size <= CONFIG - ENVELOPE:
      raise ValueError("loadable bytes outside raw application partition")
    in_flash = APP <= virtual <= virtual + memory <= CONFIG - ENVELOPE
    in_ram = 0x20000000 <= virtual <= virtual + memory <= STACK
    if not in_flash and not in_ram:
      raise ValueError("ELF segment outside application/RAM reservations")
    flags = "".join(fields[6:-1])
    if "E" in flags and "W" in flags:
      raise ValueError("writable executable ELF segment")
    loads.append({"offset": offset, "virtual": virtual, "physical": physical,
                  "file_bytes": size, "memory_bytes": memory})
  if len(loads) != 2:
    raise ValueError("expected flash and RAM load segments")
  return {"undefined_symbols": undefined, "load_segments": loads,
          "reset_vector": reset, "stack_top": STACK,
          "globals_bytes": symbols["__bss_end"] - 0x20000000, "stack_reserved_bytes": 4096}


def build(out, prefix="arm-none-eabi-"):
  out = Path(out).resolve()
  # Wire buffers have byte alignment; do not rely on inherited UNALIGN_TRP state.
  flags = ["-mcpu=cortex-m4", "-mthumb", "-mfloat-abi=soft", "-mno-unaligned-access", "-Os", "-std=c11",
           "-ffreestanding", "-fno-builtin", "-fno-common", "-ffunction-sections", "-fdata-sections",
           "-fno-unwind-tables", "-fno-asynchronous-unwind-tables", "-Wall", "-Wextra",
           "-Wstrict-prototypes", "-Werror", "-nostdlib"]
  with tempfile.TemporaryDirectory(prefix="chimera-build-") as temporary:
    temp = Path(temporary)
    elf, binary = temp / "chimera.elf", temp / "chimera.bin"
    command(prefix + "gcc", *flags, "-T", str(ROOT / "stm32f413.ld"),
            "-Wl,--gc-sections,--build-id=none,--orphan-handling=error", "-Wl,-Map=" + str(temp / "chimera.map"),
            *(str(ROOT / name) for name in COMPILATION_SOURCES), "-o", str(elf))
    command(prefix + "objcopy", "-O", "binary", str(elf), str(binary))
    raw = binary.read_bytes()
    check_vectors(raw)
    report = check_elf(elf, raw, prefix)
    report.update({"target": "chimera-f413-offline-bootstrap", "signed": False,
                   "raw_bytes": len(raw), "reserved_envelope_bytes": ENVELOPE,
                   "projected_legacy_bytes": len(raw) + ENVELOPE,
                   "application_budget_bytes": CONFIG - APP,
                   "sha256": hashlib.sha256(raw).hexdigest(),
                   "sources_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES},
                   "compiler": command(prefix + "gcc", "--version").splitlines()[0],
                   "objcopy": command(prefix + "objcopy", "--version").splitlines()[0],
                   "flags": flags, "limits": "Unsigned offline build; no installed bootstub, electrical or runtime qualification."})
    (temp / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    out.mkdir(parents=True, exist_ok=True)
    for name in ("chimera.elf", "chimera.bin", "chimera.map", "report.json"):
      (out / name).write_bytes((temp / name).read_bytes())
  return report


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--out", type=Path, default=ROOT.parent / "build/firmware")
  parser.add_argument("--toolchain-prefix", default="arm-none-eabi-")
  args = parser.parse_args()
  try:
    report = build(args.out, args.toolchain_prefix)
  except (OSError, ValueError, subprocess.CalledProcessError) as error:
    parser.exit(1, f"build failed: {error}\n{getattr(error, 'stderr', '')}")
  print(json.dumps(report, indent=2))


if __name__ == "__main__":
  main()
