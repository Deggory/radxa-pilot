# Chimera firmware

This is the first application-only STM32F413 bootstrap target. It builds offline;
it is not a modern Panda USB implementation or a flashable release yet.

The [board/flash contract](../docs/BOARD_FLASH_CONTRACT.md) records the source
evidence and qualification limits. Code is original MIT-licensed material; the
restricted legacy linker and vendor startup are not copied. No external SDK,
workspace reference checkout, keys, signer or flasher is needed to build.

| File | Purpose |
| --- | --- |
| [startup.S](startup.S) | Vectors, interrupt masking and explicit MSP reload before C |
| [main.c](main.c) | RAM initialization, inherited IRQ cleanup, bounded HSI selection and parked state |
| [board.c](board.c) | Inactive relay/OBD-C/transceiver levels; digital/analog input modes |
| [stm32f413.ld](stm32f413.ld) | Conservative application/RAM reservations and overflow assertions |
| [build.py](build.py) | Compile, inspect ELF/vectors and publish artifacts with hashes |
| [tests](tests/test_firmware.py) | Native GPIO checks, real ARM builds and negative image/linker fixtures |

From the Sunnypilot root, with ARM GNU tools on PATH:

```sh
python3 chimera/firmware/build.py
python3 -m unittest discover -s chimera/firmware/tests -v
```

An existing workspace toolchain can be selected explicitly:

```sh
python3 chimera/firmware/build.py --toolchain-prefix /home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi-
CHIMERA_TOOLCHAIN_PREFIX=/home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi- python3 -m unittest discover -s chimera/firmware/tests -v
```

Tests also require host `cc` with AddressSanitizer/UndefinedBehaviorSanitizer.
Missing tools fail the check; tests do not install tools or skip silently.
Ignored output goes to `chimera/build/firmware/`: unsigned `chimera.bin`, ELF,
link map and JSON receipt. The binary has a normal stack pointer in vector word
zero; no legacy length/signature packaging is performed. Never feed this raw
bootstrap to the legacy updater as a signed release.

November 6 validation: GCC13.2.1/binutils2.42, nine tests pass, raw1064bytes;
two different source/output paths produce identical bytes. GPIO tests use fake
registers, and disassembly verifies the MSP reload precedes C. No board execution
or electrical state was measured. USB/CAN clocks are gated, interrupts stay masked
and no acquisition or config access is implemented. All physical interfaces
remain reserved for subsequent slices.
