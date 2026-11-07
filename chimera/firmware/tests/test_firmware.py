# SPDX-License-Identifier: MIT
import importlib.util
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREFIX = os.environ.get("CHIMERA_TOOLCHAIN_PREFIX", "arm-none-eabi-")


def run(*args):
  return subprocess.run(args, capture_output=True, text=True, check=False)


class FirmwareTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.temp = tempfile.TemporaryDirectory()
    cls.addClassCleanup(cls.temp.cleanup)
    cls.out = Path(cls.temp.name)
    spec = importlib.util.spec_from_file_location("chimera_build", ROOT / "build.py")
    cls.build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.build)
    cls.report = cls.build.build(cls.out / "first", PREFIX)
    cls.raw = (cls.out / "first/chimera.bin").read_bytes()

  def test_gpio_contract_from_reset_and_inherited_state(self):
    exe = self.out / "board_test"
    result = run("cc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-fsanitize=address,undefined",
                 "-I", str(ROOT), str(ROOT / "board.c"), str(ROOT / "tests/board_test.c"), "-o", str(exe))
    self.assertEqual(result.returncode, 0, result.stderr)
    result = run(str(exe))
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_read_only_control_contract(self):
    exe = self.out / "protocol_test"
    result = run("cc", "-std=c11", "-Wall", "-Wextra", "-Wstrict-prototypes", "-Werror",
                 "-fsanitize=address,undefined", "-I", str(ROOT), str(ROOT / "protocol.c"),
                 str(ROOT / "tests/protocol_test.c"), "-o", str(exe))
    self.assertEqual(result.returncode, 0, result.stderr)
    result = run(str(exe))
    self.assertEqual(result.returncode, 0, result.stderr)
    print(result.stdout.strip())

  def test_protocol_entry_and_identity_retained_in_arm_image(self):
    result = run(PREFIX + "nm", "--defined-only", str(self.out / "first/chimera.elf"))
    self.assertEqual(result.returncode, 0, result.stderr)
    symbols = {line.split()[-1] for line in result.stdout.splitlines()}
    self.assertTrue({"chimera_control_read", "chimera_manifest", "chimera_usb_product",
                     "chimera_firmware_version"}.issubset(symbols))
    self.assertIn(b"CHMR\x01\x20\x01\x00" + bytes(12) + b"\x03\x08\x00\x00\xff\x01" + bytes(6), self.raw)
    self.assertIn(b"Chimera F413\x00", self.raw)
    self.assertIn(b"chimera-f413-bootstrap-v1\x00", self.raw)

  def test_control_setup_uses_byte_reads_for_unaligned_wire_buffer(self):
    result = run(PREFIX + "objdump", "-d", "--disassemble=chimera_control_read",
                 str(self.out / "first/chimera.elf"))
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertNotIn("ldrh", result.stdout.lower())

  def test_can_codec_entries_retained_in_arm_image(self):
    result = run(PREFIX + "nm", "--defined-only", str(self.out / "first/chimera.elf"))
    self.assertEqual(result.returncode, 0, result.stderr)
    symbols = {line.split()[-1] for line in result.stdout.splitlines()}
    self.assertTrue({"chimera_can_encode_rx", "chimera_can_decode_tx", "chimera_can_stream_init",
                     "chimera_can_stream_feed"}.issubset(symbols))

  def test_usb_clock_core_and_ep0_entries_retained_in_arm_image(self):
    result = run(PREFIX + "nm", "--defined-only", str(self.out / "first/chimera.elf"))
    self.assertEqual(result.returncode, 0, result.stderr)
    symbols = {line.split()[-1] for line in result.stdout.splitlines()}
    self.assertTrue({"chimera_usb_clock48", "chimera_usb_core_detached", "chimera_usb_ep0_init",
                     "chimera_usb_ep0_setup", "chimera_usb_ep0_in_complete", "chimera_usb_ep0_out_complete",
                     "chimera_usb_ep0_reset"}.issubset(symbols))

  def test_real_image_fits_reserved_envelope(self):
    stack, reset = struct.unpack_from("<II", self.raw)
    self.assertEqual(stack, 0x2001FFF8)
    self.assertTrue(reset & 1)
    self.assertGreaterEqual(reset & ~1, 0x08004200)
    self.assertLess(reset & ~1, 0x08020000 - 136)
    self.assertEqual(len(self.raw), self.report["raw_bytes"])
    self.assertLessEqual(len(self.raw) + 136, 0x1C000)
    self.assertEqual(self.report["undefined_symbols"], [])

  def test_usb_driver_backend_symbols_and_mmio_barriers(self):
    elf = str(self.out / "first/chimera.elf")
    result = run(PREFIX + "nm", "--defined-only", elf)
    self.assertEqual(result.returncode, 0, result.stderr)
    symbols = {line.split()[-1] for line in result.stdout.splitlines()}
    self.assertTrue({"chimera_usb_time16_init", "chimera_usb_delay16", "chimera_usb_mmio_init",
                     "chimera_usb_driver_init", "chimera_usb_driver_poll"}.issubset(symbols))
    for name, barrier in [("read32", "dmb"), ("write32", "dsb")]:
      result = run(PREFIX + "objdump", "-d", "--disassemble=" + name, elf)
      self.assertEqual(result.returncode, 0, result.stderr)
      self.assertRegex(result.stdout, r"\b" + barrier + r"\b")

  def test_boot_facts_reader_retained_in_arm_image(self):
    result = run(PREFIX + "nm", "--defined-only", str(self.out / "first/chimera.elf"))
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("chimera_boot_read_facts", {line.split()[-1] for line in result.stdout.splitlines()})

  def test_main_calls_checked_startup_and_keeps_usb_held(self):
    elf = str(self.out / "first/chimera.elf")
    result = run(PREFIX + "objdump", "-d", "--disassemble=chimera_reset", elf)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("<chimera_usb_mmio_bind>", result.stdout)
    self.assertIn("<chimera_main_start>", result.stdout)
    self.assertIn("<chimera_main_poll>", result.stdout)
    self.assertNotIn("chimera_usb_service", result.stdout)
    result = run(PREFIX + "objdump", "-d", "--disassemble=chimera_main_prepare", elf)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("<chimera_boot_read_facts>", result.stdout)
    self.assertNotIn("chimera_usb_service", result.stdout)

  def test_main_coordinator_calls_real_usb_service(self):
    elf = str(self.out / "first/chimera.elf")
    for function, calls in (("chimera_main_start", ("chimera_main_prepare", "chimera_usb_service_start")),
                            ("chimera_main_poll", ("chimera_usb_service_poll",)),
                            ("chimera_main_stop", ("chimera_usb_service_stop",))):
      result = run(PREFIX + "objdump", "-d", "--disassemble=" + function, elf)
      self.assertEqual(result.returncode, 0, result.stderr)
      for target in calls:
        self.assertIn("<" + target + ">", result.stdout)

  def test_detached_usb_service_retained_without_direct_reset_call(self):
    elf = str(self.out / "first/chimera.elf")
    result = run(PREFIX + "nm", "--defined-only", elf)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertTrue({"chimera_usb_service_start", "chimera_usb_service_poll", "chimera_usb_service_stop"}.issubset(
      {line.split()[-1] for line in result.stdout.splitlines()}))
    result = run(PREFIX + "objdump", "-d", "--disassemble=chimera_reset", elf)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertNotIn("chimera_usb_service", result.stdout)

  def test_boot_vectors_reject_corruption(self):
    for offset, value in ((0, 0x20020000), (4, 0x08000001), (4, 0x08004200),
                          (7 * 4, 1), (117 * 4, 0), (117 * 4, 0x08020001)):
      with self.subTest(offset=offset, value=hex(value)):
        damaged = bytearray(self.raw)
        struct.pack_into("<I", damaged, offset, value)
        with self.assertRaises(ValueError):
          self.build.check_vectors(damaged)

  def test_truncated_and_oversized_images_rejected(self):
    for raw in (b"", self.raw[:471], self.raw + bytes(0x1C000)):
      with self.subTest(length=len(raw)), self.assertRaises(ValueError):
        self.build.check_vectors(raw)

  def test_elf_rejects_unsafe_load_segments_and_identity(self):
    original = (self.out / "first/chimera.elf").read_bytes()
    phoff = struct.unpack_from("<I", original, 28)[0]
    phsize = struct.unpack_from("<H", original, 42)[0]
    mutations = ((18, "H", 3), (24, "I", 0x08000001),
                 (phoff + 12, "I", 0x08000000), (phoff + 12, "I", 0x08020000),
                 (phoff + 24, "I", 7),  # RWE is forbidden even within the app.
                 (phoff + phsize + 20, "I", 0x20000))
    for offset, kind, value in mutations:
      with self.subTest(offset=offset, value=hex(value)):
        damaged = bytearray(original)
        struct.pack_into("<" + kind, damaged, offset, value)
        elf = self.out / "damaged.elf"
        elf.write_bytes(damaged)
        with self.assertRaises(ValueError):
          self.build.check_elf(elf, self.raw, PREFIX)

  def test_startup_masks_interrupts_and_loads_msp_before_c(self):
    disassembly = run(PREFIX + "objdump", "-d", "--disassemble=Reset_Handler",
                      str(self.out / "first/chimera.elf"))
    self.assertEqual(disassembly.returncode, 0, disassembly.stderr)
    text = disassembly.stdout.lower()
    self.assertLess(text.index("cpsid"), text.index("msr"))
    self.assertLess(text.index("msp"), text.index("<chimera_reset>"))

  def test_linker_rejects_flash_overflow(self):
    self.check_overflow('.section .rodata.excess,"a"\n.space 0x1C000\n', "FLASH")

  def test_linker_rejects_ram_stack_collision(self):
    self.check_overflow('.section .bss.excess,"aw",%nobits\n.space 0x20000\n', "RAM")

  def check_overflow(self, text, diagnostic):
    extra = self.out / f"excess_{diagnostic}.S"
    extra.write_text(text)
    result = run(PREFIX + "gcc", "-mcpu=cortex-m4", "-mthumb", "-nostdlib", "-Wl,--build-id=none",
                 "-T", str(ROOT / "stm32f413.ld"), str(ROOT / "startup.S"), str(extra),
                 "-Wl,--defsym=chimera_reset=0x08004201,--defsym=chimera_fault=0x08004201",
                 "-o", str(self.out / f"overflow_{diagnostic}.elf"))
    self.assertNotEqual(result.returncode, 0)
    self.assertIn(diagnostic, result.stderr)

  def test_build_is_independent_of_checkout_and_output_path(self):
    copy = self.out / "copied_sources"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "obj"))
    result = run("python3", str(copy / "build.py"), "--out", str(self.out / "second"),
                 "--toolchain-prefix", PREFIX)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(self.raw, (self.out / "second/chimera.bin").read_bytes())


if __name__ == "__main__":
  unittest.main()
