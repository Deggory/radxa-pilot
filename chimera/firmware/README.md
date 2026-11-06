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
| [usb_hw.c](usb_hw.c), [header](usb_hw.h) | Backend-driven48MHz clock and detached core preparation; no startup binding |
| [usb_ep0.c](usb_ep0.c), [header](usb_ep0.h) | Descriptor/control-transfer state model, deferred commits and canceled-transfer generations |
| [usb_driver.c](usb_driver.c), [header](usb_driver.h) | Polling EP0 event/FIFO driver with bounded cancellation, reset and failure handling |
| [usb_mmio.c](usb_mmio.c), [timing](usb_time.c), [header](usb_time.h) | Ordered ARM MMIO and bounded nominal16MHz cycle-counter delays; no startup call |
| [boot_facts.c](boot_facts.c), [header](boot_facts.h) | Read-only UID/reset/option snapshot, stable-ID checks; no startup call or write |
| [usb_service.c](usb_service.c), [header](usb_service.h) | Composed detached preparation/poll/release with fault latching; not called by main |
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

November 6 current validation: GCC13.2.1/binutils2.42, twenty-three tests pass, raw7448bytes;
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
[the identity contract](../docs/USB_IDENTITY_CONTRACT.md). There is no live USB
enumeration or new native host profile yet. Packet handling exists as an unbound
library; no startup/physical device qualification is implied.

T04 adds a pure classical CAN codec with one14-byte stream buffer per connection.
648encoded RX records and189host TX packing vectors match the current Panda
source; fragmentation/negative/sanitizer checks pass. Detected stream errors latch
until explicit reset. Known XOR collision/length limitations are documented in
[the codec contract](../docs/CAN_CODEC_CONTRACT.md). No codec function is called
by the parked application; operational capability/hash fields remain zero.

T03b1 adds detached USB preparation and the EP0 state model, tested with19fake-
register scenarios and458797SETUP cases. Descriptors expose only a control
interface; no bulk endpoint or hardware attachment is enabled. Main remains
unchanged. See [USB bootstrap status](../docs/USB_BOOTSTRAP.md) for the original
foundation and power/VBUS requirements.

T03b2 adds the polling packet driver and ordered MMIO/timing backend.32768RX
headers,390descriptor transfers,15controller fault cases and51delay durations
pass offline; the ARM image retains MMIO barriers and API symbols. No routine is
called by main; next is T03b3 power/VBUS/UID/recovery prerequisites and separately
reviewed startup/attachment work. See [the driver contract](../docs/USB_PACKET_DRIVER.md).

T03b3a adds [power/UID/recovery requirements](../docs/USB_STARTUP_REQUIREMENTS.md)
and a read-only boot-facts helper.65536fake snapshots and UID/serial/flag-preservation
checks pass; no physical UID read, flag clearing or option/watchdog write. Main
remains parked. Next is detached startup/service composition; physical attachment
requires the separate electrical and current recovery evidence in that contract.

T03b3b adds [the detached service](../docs/USB_SERVICE.md), combining real boot-
facts/timing/clock/core/driver calls with owned cleanup and failure latching.
44integration scenarios pass; no main/GPIO/IRQ/attachment change. Next board work
is the exact status/capability contract before operational health/endpoints.
