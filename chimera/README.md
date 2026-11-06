# Chimera for Radxa Sunnypilot

This is the active Chimera implementation home inside Sunnypilot, created
November 6, 2026. It uses this repository's Git history; it is a regular directory.

## Where the code is

Shared Panda host code runs on the Radxa and belongs in
the existing `openpilot/selfdrive/pandad/` module, where Sunnypilot builds it:

| Code | Location |
| --- | --- |
| New native USB connection | [panda_usb.cc](../openpilot/selfdrive/pandad/panda_usb.cc), [header](../openpilot/selfdrive/pandad/panda_usb.h) |
| New board/protocol identification | [panda_identification.cc](../openpilot/selfdrive/pandad/panda_identification.cc), [header](../openpilot/selfdrive/pandad/panda_identification.h) |
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
- [Roadmap](tasks/plan.md): one verified increment at a time.
- [Existing firmware map](docs/FIRMWARE_SOURCE_MAP.md): recovered GPIO/CAN/config/build behavior.
- [Source provenance](docs/PROVENANCE.md): reference versions and archive locations.
- [Legacy Panda support](docs/LEGACY_PANDA_SUPPORT.md): shared USB/SPI transport with distinct firmware/status profiles.

Completed: folder/source map, T01a source-backed board/flash boundaries, T03a
minimal offline F413 build and T02b identity/request/source contracts with a
tested pure handler. Next board slice: T04 modern classical CAN codec, then USB
clock/EP0 wiring and operational health contracts. Physical
boot/recovery and electrical qualification remain open.

Legacy F4 Panda support is now an explicit host requirement alongside Chimera.
Host increments now include the shared transport interface, pinned native USB
factory/backend and identification tests. Legacy status adaptation and managed
selection remain pending; current startup still uses its existing SPI path.

The workspace-level `../../chimera/` remains the original evidence/recovery
archive. It is optional development evidence, not a runtime dependency. Required
source/assets will be imported with provenance as each implementation slice
needs them. Host changes belong in their existing Sunnypilot modules.
