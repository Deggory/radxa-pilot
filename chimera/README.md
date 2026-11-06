**Owner correction, November6:** SPI is removed from pandad's source/build,
classes, constructors, discovery and fallback. All platforms use pinned USB.
[Removal and validation](docs/PANDAD_USB_ONLY.md). Metadata/consumer work continues.

**November6, T08b2b:** offline legacy F4-to-PandaState preview conversion now
passes native/sanitizer/source checks. Conflicting safety IDs and unrepresentable
faults are rejected; six unavailable fields stay explicit and every preview is
invalid. [Mapping contract](docs/LEGACY_F4_PANDA_STATE.md). No normal publication.

**November 6, T08b2a:** normal host ignition now rejects invalid/empty Panda
updates, with shutdown harness history preserved.65Python tests pass this slice.
Legacy PandaState mapping/admission remains pending.
[Validity contract](docs/PANDA_IGNITION_VALIDITY.md).

**November 6 update:** T08b1 adds passive classical CAN RX and isolated legacy
USB diagnostics to the pinned USB entry. Native build/9native programs,
25Python regressions and sanitizer checks pass offline. No pandaStates admission
or physical board qualification. See [receive contract](docs/USB_PASSIVE_RECEIVE.md).

# Chimera for Radxa Sunnypilot

This is the active Chimera implementation home inside Sunnypilot, created
November 6, 2026. It uses this repository's Git history; it is a regular directory.

Start with [the plain-language progress guide](docs/PROGRESS_EXPLAINED.md) for
what has been written, what has actually been tested and what is still pending.

**Connection requirement, November 6: USB only between the Radxa and Chimera or
selected legacy Panda.** No SPI wiring, probing or fallback for this setup.
Radxa startup now requires explicit serial/version pins and enters a USB-only
observation session before legacy reset/flashing logic. Passive CAN and isolated
legacy diagnostics are implemented; ordinary pandaStates admission remains pending.

## Where the code is

Shared Panda host code runs on the Radxa and belongs in
the existing `openpilot/selfdrive/pandad/` module, where Sunnypilot builds it:

| Code | Location |
| --- | --- |
| USB-only status startup | [contract](docs/USB_ONLY_STARTUP.md), [session](../openpilot/selfdrive/pandad/panda_usb_status.cc), [launcher selector](../openpilot/selfdrive/pandad/usb_startup.py) |
| New native USB connection | [panda_usb.cc](../openpilot/selfdrive/pandad/panda_usb.cc), [header](../openpilot/selfdrive/pandad/panda_usb.h) |
| New board/protocol identification | [panda_identification.cc](../openpilot/selfdrive/pandad/panda_identification.cc), [header](../openpilot/selfdrive/pandad/panda_identification.h) |
| New bootstrap discovery decoder | [chimera_identity.py](../openpilot/selfdrive/pandad/chimera_identity.py), pure/offline; no managed profile |
| Legacy F4 per-controller health | [CAN-health5 contract](docs/LEGACY_F4_CAN_HEALTH.md), native typed decoder and bounded C2 reader |
| Legacy F4 health59 decoder/read helper | [panda_health.cc](../openpilot/selfdrive/pandad/panda_health.cc), [header](../openpilot/selfdrive/pandad/panda_health.h); native library, not managed startup |
| Shared transport interface | [panda_comms.h](../openpilot/selfdrive/pandad/panda_comms.h) |
| Existing original-Chimera Python receiver | [chimera.py](../openpilot/selfdrive/pandad/chimera.py), [decoder](../openpilot/selfdrive/pandad/chimera_protocol.py) |
| Offline native USB tests | [test_panda_usb.cc](../openpilot/selfdrive/pandad/tests/test_panda_usb.cc) |

**The first STM32F413 firmware target is implemented in [firmware/](firmware/README.md).**
It builds an unsigned offline bootstrap with its own startup, GPIO initialization
and linker. USB/CAN communication and input acquisition are later increments.
The original firmware remains preserved in the optional workspace Ocelot reference.

The goal is STM32F413 Chimera firmware with modern Panda USB communication,
native Sunnypilot USB support and usable RetroPilot Core Config. Preserve CAN0
Cores/control = host 0, CAN1 ADAS = host 1, CAN2 vehicle = host 2; IGN, VSS, CPS,
BRAKE, both analog inputs, the onboard relay and OBD-C hardware interfaces.

- [Firmware area](firmware/README.md): source, offline build and tests.
- [Board/flash contract](docs/BOARD_FLASH_CONTRACT.md): source-defined levels, preserved areas and recovery limits.
- [USB identity/request contract](docs/USB_IDENTITY_CONTRACT.md): distinct bootstrap identity and implemented read-only handler.
- [Bus/input source contract](docs/BUS_INPUT_CONTRACT.md): preserved routing and future validity/source requirements.
- [CAN codec contract](docs/CAN_CODEC_CONTRACT.md): tested current framing, bounded stream behavior and integrity limits.
- [USB bootstrap](docs/USB_BOOTSTRAP.md): detached clock/core preparation and EP0 request model.
- [USB packet driver](docs/USB_PACKET_DRIVER.md): polling EP0 event/FIFO library and ordered MMIO/timing backend, verified offline; startup attachment pending.
- [Power/UID/recovery requirements](docs/USB_STARTUP_REQUIREMENTS.md): attachment prerequisites, known historical recovery evidence and read-only boot facts.
- [Detached USB service](docs/USB_SERVICE.md): coordinated preparation/polling/release with failure latching; not called from main.
- [Status/capability contract](docs/STATUS_CAPABILITY_CONTRACT.md): strict bootstrap decoder, health limits and firmware-response fixtures.
- [USB-only startup](docs/USB_ONLY_STARTUP.md): pinned Radxa status session, failure/ownership boundaries and rejected profiles.
- [Roadmap](tasks/plan.md): one verified increment at a time.
- [Existing firmware map](docs/FIRMWARE_SOURCE_MAP.md): recovered GPIO/CAN/config/build behavior.
- [Source provenance](docs/PROVENANCE.md): reference versions and archive locations.
- [Legacy Panda support](docs/LEGACY_PANDA_SUPPORT.md): USB-only Radxa target with distinct firmware/status profiles.
- [Legacy F4 CAN-health5](docs/LEGACY_F4_CAN_HEALTH.md): exact per-controller fields, selector validation and bounded reads.
- [Legacy F4 health59](docs/LEGACY_F4_HEALTH.md): exact typed decoding and one bounded read; no health49 cast or manufactured current-only fields.
- [Ocelot Panda Docker review](docs/OCELOT_PANDA_DOCKER_REVIEW.md): pinned legacy Panda and parent Chimera source, analog/relay/OBD-C mapping and protocol conflicts.

Completed: folder/source map, T01a source-backed board/flash boundaries, T03a
minimal offline F413 build, T02b identity/request/source contracts and T04 classical
CAN codec with offline interoperability/stream checks. T03b1 adds detached USB
preparation and the pure EP0 model. T03b2 adds the polling controller packet driver
and ordered MMIO/timing backend. T03b3a establishes the power/VBUS/UID/recovery
requirements and adds a read-only boot-facts helper. T03b3b composes these into a
detached startup/service module, still uncalled by main. T05a adds bootstrap
discovery decoding and status/capability semantics. T05b adds native legacy F4
health59 decoding/read support. T05c adds CAN-health5 decoding/read support.
T08a routes Radxa startup into a pinned legacy F4 USB status session.
Next: passive CAN reception and profile-aware status publication; new
Chimera operational health/endpoints remain pending. Qualified attachment
still requires the recorded electrical/recovery evidence. Physical
boot/recovery and electrical qualification remain open.

Legacy F4 Panda support is now an explicit host requirement alongside Chimera.
Host increments now include the shared transport interface, pinned native USB
factory/backend, identification and legacy health59 decoding/read tests. Legacy
CAN-health5 decoding/read support is also tested. Publication and managed
operational profile selection remain pending. The Radxa entry path bypasses
legacy SPI construction; the new status session currently accepts legacy F4v17
only and publishes no CAN/pandaStates. No device has been opened by this work.

The workspace-level `../../chimera/` remains the original evidence/recovery
archive. It is optional development evidence, not a runtime dependency. Required
source/assets will be imported with provenance as each implementation slice
needs them. Host changes belong in their existing Sunnypilot modules.
