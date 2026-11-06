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
| [protocol.c](protocol.c), [header](protocol.h) | Distinct identity/manifest and pure read-only vendor-request handler; not wired to USB yet |
| [can_codec.c](can_codec.c), [header](can_codec.h) | Current six-byte/XOR classical CAN encoding, strict TX decoding and bounded stream assembly |
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
Codec interoperability tests use the project's current Panda/opendbc source;
the application build itself still needs no external reference checkout or SDK.
Missing tools fail the check; tests do not install tools or skip silently.
Ignored output goes to `chimera/build/firmware/`: unsigned `chimera.bin`, ELF,
link map and JSON receipt. The binary has a normal stack pointer in vector word
zero; no legacy length/signature packaging is performed. Never feed this raw
bootstrap to the legacy updater as a signed release.

November 6 current validation: GCC13.2.1/binutils2.42, fourteen tests pass, raw1840bytes;
two different source/output paths produce identical bytes. GPIO tests use fake
registers, and disassembly verifies the MSP reload precedes C. No board execution
or electrical state was measured. USB/CAN clocks are gated, interrupts stay masked
and no acquisition or config access is implemented. All physical interfaces
remain reserved for subsequent slices.

T02b adds D6 version and A0 manifest queries with exact vendor/device/IN checks,
zero parameters and bounded full responses.458920 native request cases pass
under ASan/UBSan; no writes/health/config/reset operation is accepted. Identity
and handler are retained in the ARM image for offline verification/future EP0
wiring. Operational capabilities/layout hashes are zero. See
[the identity contract](../docs/USB_IDENTITY_CONTRACT.md). There is no USB
enumeration/interrupt/endpoint implementation or new native host profile yet.

T04 adds a pure classical CAN codec with one14-byte stream buffer per connection.
648encoded RX records and189host TX packing vectors match the current Panda
source; fragmentation/negative/sanitizer checks pass. Detected stream errors latch
until explicit reset. Known XOR collision/length limitations are documented in
[the codec contract](../docs/CAN_CODEC_CONTRACT.md). No codec function is called
by the parked application; operational capability/hash fields remain zero.
