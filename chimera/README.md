# Chimera for Radxa Sunnypilot

This is the active Chimera implementation home inside Sunnypilot, created
November 6, 2026. It uses this repository's Git history; it is a regular directory.

The goal is STM32F413 Chimera firmware with modern Panda USB communication,
native Sunnypilot USB support and usable RetroPilot Core Config. Preserve CAN0
Cores/control = host 0, CAN1 ADAS = host 1, CAN2 vehicle = host 2; IGN, VSS, CPS,
BRAKE, both analog inputs, the onboard relay and OBD-C hardware interfaces.

- [Firmware area](firmware/README.md): implementation starts here after the board/build contract.
- [Roadmap](tasks/plan.md): one verified increment at a time.
- [Existing firmware map](docs/FIRMWARE_SOURCE_MAP.md): recovered GPIO/CAN/config/build behavior.
- [Source provenance](docs/PROVENANCE.md): reference versions and archive locations.
- [Legacy Panda support](docs/LEGACY_PANDA_SUPPORT.md): shared USB/SPI transport with distinct firmware/status profiles.

Completed: folder structure, source map and implementation sequence. There is no
new firmware target or compiled image in this folder yet. Next: T01 board/flash
layout, followed by T02 USB identity and bus/source contracts.

Legacy F4 Panda support is now an explicit host requirement alongside Chimera.
The first host increment adds a shared transport interface with the existing
SPI backend; USB, legacy status adaptation and managed selection remain pending.

The workspace-level `../../chimera/` remains the original evidence/recovery
archive. It is optional development evidence, not a runtime dependency. Required
source/assets will be imported with provenance as each implementation slice
needs them. Host changes belong in their existing Sunnypilot modules.
