# Chimera progress in plain language

## Current overall status — November 6

The offline foundation is built; most operational integration and all new-firmware
physical qualification remain. The7448-byte unsigned image has never been flashed
and main parks with USB/CAN disabled. Radxa USB libraries/identification and legacy
health59 decoding exist. Radxa now has pinned USB-only startup with passive classical CAN reception and
isolated legacy status diagnostics. Normal pandaStates admission, other profiles
and reconnect policy remain pending. No SPI probing/fallback belongs in the target setup.

Saved results:28firmware/discovery tests; current native pandad build and9native programs,
parser/backend ASan/UBSan and25Python regressions including Thneed telemetry. These are separate offline runs,
not a combined physical end-to-end test. No physical USB/IPC/board run is claimed.

Remaining: normal pandaStates validity/ignition policy; operational USB/CAN/health binding; USB-only host
lifecycle; qualified power/VBUS/recovery/image packaging and passive bench tests;
digital/pulse/ADC acquisition and reports; MCU TX enforcement; Core Config and
recoverable settings/watchdog; relay/OBD-C qualification and release/soak testing.
Active driving is separate later scope. Unequal slices and unresolved electrical
work do not support a reliable completion percentage. T08a USB-only legacy F4 status startup/session now passes offline tests.
T08b1 passive CAN/isolated diagnostics passes offline; next T08b2 specifies normal
pandaStates admission, supported-field validity/ignition and reconnect policy.

See the [passive receive contract](USB_PASSIVE_RECEIVE.md) for limitations.
The detailed component history below explains what each piece does.


November 6, 2026. The goal is to connect the existing Chimera board to the Radxa
over its USB Type-B port, let our Sunnypilot exchange CAN data with it, and later
retain direct inputs and RetroPilot Core Config.

There are two programs to build: **firmware** runs on Chimera's STM32 chip;
**host software** runs on the Radxa inside Sunnypilot. Both need to agree on the
USB messages. Copying old Panda firmware alone would not preserve all of this
board's inputs, power relay and OBD-C behavior.

## What is already written

| Piece | Plain meaning | What has actually been verified |
| --- | --- | --- |
| Evidence and board map | Identify the chip, three buses, inputs and reserved flash areas | Original source/wiki/history reviewed and pinned; electrical gaps recorded |
| Radxa USB connection library | Give the Radxa setup its required USB-only path | Q8B passive CAN/isolated diagnostic publication tested offline; normal pandaStates admission pending |
| Firmware build/startup | Compile our own small F413 program, preserve bootstub/settings space and initialize source-defined inactive outputs | ARM builds and offline register/artifact tests; never loaded to the board |
| CAN codec | Encode/decode classical CAN records in the newer Panda wire format | Current-source interoperability and malformed/chunked record tests; not connected to real CAN controllers |
| USB identity/control model | Supply the board name, serial format and supported read-only queries | Descriptor/request/state tests; control endpoint only |
| USB packet driver | Move control requests and replies through the USB controller's packet buffers | Fake-controller reset/cancellation/STALL/FIFO tests; not called by startup |
| Register/timing backend | Provide ordered MCU register access and bounded16MHz cycle-based delays | ARM code/barriers inspected and timing logic tested with fake registers |
| Boot facts reader, added now | Read the chip's UID and raw reset/option settings without changing them |65536fake snapshots, blank/unstable ID rejection and serial-order checks |
| Detached USB service | Put preparation, polling and cleanup into one coordinated library |44real-component register scenarios; main still does not call it |

Everything above lives inside the actual Sunnypilot project. Firmware is in
`chimera/firmware/`; the host libraries are in `openpilot/selfdrive/pandad/`.
The original Ocelot checkout and workspace Chimera archive are preserved references.

## What is not working on the board yet

The new firmware has not been flashed. Its application startup still parks with
USB/CAN disabled. No new physical USB enumeration, live CAN reception or complete
Sunnypilot integration has been demonstrated. The control driver does not yet
provide bulk CAN endpoints or operational health accepted by the host.

The three CAN identities and IGN/speed/crank/brake/two analog inputs are preserved
in the source design. Sampling those signals, migrating Core Config, enforcing
MCU TX policy and qualifying relay/OBD-C behavior are later tasks. Preservation
does not mean those features are already operational in the new firmware.

## Why this new stage matters

- **VBUS** is the host's USB power wire. We need a reliable way to know when USB
  power is present, especially because IGN can keep Chimera powered separately.
- **UID** is the STM32's unique96-bit identifier. It supplies a stable serial so
  the Radxa can select the intended board. It is not a password or proof of firmware.
- **Recovery** means having the actual board identity, compatible bootstub/image
  format, settings backup and a demonstrated way back if the new app cannot start.
- **Watchdog** is a reset timer. A running inherited watchdog cannot be assumed
  stopped just because our new code does not start one.

The [power/UID/recovery contract](USB_STARTUP_REQUIREMENTS.md) now separates known
source facts, historical bench results and missing current electrical/recovery
evidence. We do not choose a supply mode, VBUS pin or signing method by guesswork.
The new reader is available for a future startup sequence; it is not invoked now.

The tested pieces now form a [detached startup/service library](USB_SERVICE.md).
Main still does not call it. Clearing USB soft-disconnect requires qualified
power/VBUS and recovery evidence. Next board work defines exact health/status
semantics, followed by endpoints and managed host support. This remains a gradual
firmware port, not a released board image.

## November 6 — Bootstrap discovery checked

T05a adds a small Radxa-side decoder for the new firmware's identification reply.
It checks the exact version and board description, and rejects altered or unknown
replies. It can describe the three CAN connections and reserved input/output
connections; it does not claim these are operating or measure ignition, voltage
or health. Tests use replies produced by the actual firmware C function. The new
firmware image and parked startup are unchanged; no board was connected/flashed.
Next is the separate legacy Panda health59 decoder, before managed use. See the
[status contract](STATUS_CAPABILITY_CONTRACT.md).

## November 6 — Old Panda health reply understood by native code

T05b adds the Radxa-side decoder for the selected older Panda firmware's59-byte
health reply. It preserves the actual measurements and flags, and refuses wrong
profiles, malformed data or failed/partial reads. This helps our legacy Panda
compatibility work; it does not make the new Chimera firmware emit health.
Native pandad builds and offline tests pass. At T05b startup still used SPI;
T08a below supersedes that status. No board was accessed. Next is the per-bus CAN-health5 contract, then managed
selection/publication/reconnect work. [Details](LEGACY_F4_HEALTH.md).

## November 6 — Per-controller CAN health decoded

T05c adds native decoding for the legacy Panda CAN controller status reply and
a bounded reader for selectors0/1/2. Tests check counters, speeds, error codes
and flags against the original source. This reports status bytes; it does not
connect USB startup, enable CAN, establish wiring or make Chimera emit health.
Legacy bus-off count also increases during polling, so we preserve that behavior
without calling it a count of distinct faults. Next is USB-only session/startup
integration, with no SPI probing/fallback. [Details](LEGACY_F4_CAN_HEALTH.md).

## November 6 — Radxa startup now chooses USB status monitoring

T08a routes Radxa startup to a native USB session using explicit serial/version
pins, before old Panda reset/flashing/recovery logic. Missing pins or USB/status
failure stops that path without trying SPI. It reads legacy F4 health and all
three controller reports, closes on failure, and can be stopped normally.
This is not yet CAN reception or pandaStates publication; current/original/new
Chimera profiles stay rejected by this session. No pins were installed and no
board/monitor process was run. [Contract](USB_ONLY_STARTUP.md).
