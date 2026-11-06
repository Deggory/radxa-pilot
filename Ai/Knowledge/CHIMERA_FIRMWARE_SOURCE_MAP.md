# Chimera firmware source map — November 6, 2026

The original firmware is the implementation baseline for preserving Chimera's
hardware. The four files in `ocelot/firmware/chimera/` must be read with their
shared board, peripheral, clock and build dependencies.

## Source ownership

| Source under `ocelot/` | What it implements |
| --- | --- |
| `firmware/chimera/main.c` | Startup, direct inputs, pulse interrupts, signal extraction, generated reports, USB callbacks, status and relay loop |
| `firmware/chimera/can.h` | bxCAN queues, bus tags, receive/send handling |
| `firmware/chimera/chimera.h` | Packed configuration entries, CRC32, flash persistence and deferred writes |
| `firmware/chimera/usb.h` | Legacy USB device/controller and endpoint machinery |
| `firmware/boards/gateway.h` | CAN alternate functions and transceiver enables; selected via GATEWAY in board.h |
| `firmware/boards/common.h` | USB PA11/PA12 and common GPIO/peripheral clock initialization |
| `firmware/drivers/{clock,timer,llcan,adc,json_rpc}.h` | Clocks/watchdog, timing, CAN bitrate, analog acquisition and configuration RPC support |
| `firmware/SConscript`, startup and linker | STM32F413xx, Cortex-M4, Chimera main, image layout and signing |

## Logical board mapping recovered from source

`main.c:1186` defines GPIO modes/pulls and startup outputs; `main.c:1026`
reads active-low IGN, BRAKE and OBD-C request and updates the outputs.

| Function | MCU assignment | Existing behavior |
| --- | --- | --- |
| IGN | PA3 | Active-low input, pull-up |
| VSS | PA4 | Pull-up, falling-edge EXTI4 pulse timing |
| CPS | PA5 | Pull-up, falling-edge EXTI9_5 pulse timing |
| BRAKE | PA6 | Active-low input, pull-up |
| ADC1 / ADC2 | PC2 / PC3 | Analog channels 12 / 13, read at main.c:759 |
| Onboard power relay | PB0 | Output, pull-down, startup low/off |
| OBD-C ignition | PB1 | Output, startup high/off; written as !ignition_on |
| OBD-C relay request | PA2 | Active-low input, pull-up |

`gateway.h:5` and `gateway.h:43` define the following normal-mode map:

| Board / host bus | MCU controller pins | Active-low transceiver enable |
| --- | --- | --- |
| CAN0 / 0, Cores and controls | CAN1, PB8/PB9, AF8 | PC1 |
| CAN1 / 1, ADAS | CAN2, PB5/PB6, AF9 | PC13 |
| CAN2 / 2, vehicle and retrofit sensors | CAN3, PA8/PA15, AF11 | PA0 |

These are MCU-side peripheral pins behind transceivers and input conditioning,
not a connector CANH/CANL or voltage wiring instruction. The logical pin map is
available; connector routing, voltage conditioning and actual load paths still
need electrical evidence.

## Behavior to preserve, behavior to adapt

- Startup explicitly configures all three CAN controllers at 500 kbit/s with
  silent=false (`main.c:1133`); gateway_init enables the transceivers. Do not infer
  startup silence from an unrelated default mask in can.h.
- Raw RX from all three buses is queued for USB independently of configured
  signal extraction. Configurable vehicle extraction uses MCU CAN3/host bus 2.
- Legacy CAN USB IN uses 16-byte mailbox records, at most four per 64-byte packet
  (`main.c:172`); CAN OUT is endpoint 3 (`main.c:200`). Health is 43 bytes, with
  zero voltage/current and a constant safety number. Those fields do not provide
  modern safety enforcement or actual electrical measurements.
- Configuration has 32 entries of 24 bytes plus magic and CRC32: 776 bytes at
  sector 5, 0x08020000 (`chimera.h:5`). App starts at 0x08004000. Config types
  declared in a union are not proof every corresponding feature is implemented.
- Direct acquisition, configurable CAN extraction and generated CAN0 reports
  0x50/0x75/0x76/0x100 are separate paths. TIM3's source configuration intends
  100 Hz scheduling with five slots (nominal 20 Hz per report), not measured rates.
- Relay PB0 follows line-or-CAN ignition. OBD-C/USB request gating is commented
  out (`main.c:1032`); direct B4/B5 USB output handlers are also commented out.
  Thus existing source cannot be described as heartbeat-controlled power cutoff.
- Modernization must adapt USB framing, status/version and host transport while
  retaining this board's GPIO/acquisition. All CAN TX paths need explicit MCU
  policy; stock Panda board GPIO/harness behavior must not replace this mapping.

## Existing build path is present

`firmware/build_local.sh chimera` selects the existing SCons target and local
user tool directory; it builds/signs and has no flashing step. Root
`ocelot/build_project.sh` is an older SCons wrapper. Neither was executed here.
Compiler --version confirms GCC 13.2.1; objcopy is 2.42; SCons is 4.5.2 with the
local PYTHONPATH used by build_local.sh. An initial direct SCons version command
without that environment failed; the environment-corrected check passed.
Existing legacy ELF/bootstub artifacts and BUILDING.md are already retained.
BUILDING.md's old source pin is historical, not the current checkout identity.
A freshly reproducible modern build, partition budget and installed-image match
remain to be established; the legacy build path/toolchain are not missing.

## Dated correction, provenance and next step

This November 6 review narrows QA-20261106-03: source-level GPIO assignments and
legacy build infrastructure are known. Outstanding electrical/installed-state
proof must not be worded as absence of those source definitions. This is enough
to develop an offline board target while resolving T01/T02 contracts.

Source: Ocelot d87892fa25ef2a2474110b97bfb5245ee818b534 plus pre-existing dirty
main.c/chimera.h and local build helpers. It is not exact source proof for the
historical installed de193215 nightly. The board receipt
`chimera/evidence/firmware-source-map-20261106.json` pins 19 inspected/dependency
files and verifies all 94 original source entries / 93 frozen copies and unchanged
Ocelot dirty status. No firmware source was modified, compiled, loaded or tested
on hardware. No new REA analysis, upstream update or push occurred.
