# Chimera progress in plain language

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
| Radxa USB connection library | Give Sunnypilot a USB path alongside its existing SPI connection | Fake-device/native checks; managed startup still uses SPI |
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
Native pandad builds and offline tests pass. Managed startup still uses SPI and
no board was accessed. Next is the per-bus CAN-health5 contract, then managed
selection/publication/reconnect work. [Details](LEGACY_F4_HEALTH.md).
