# Sunnypilot architecture map

Source snapshot: `6f7a2c94c10dffcf9a83b120ab1e6985e4496868`, 2026-11-01.
This is a navigation map, not exhaustive algorithm or hardware validation.
Use [MODULE_MAP.md](MODULE_MAP.md) and the source index for actual tracked paths.

| Area | Responsibility / first place to look |
| --- | --- |
| Launch and SCons at repository root | Environment, platform/build choices and manager entry |
| `openpilot/system/manager/` | Service registry, conditions, startup/stop and manager status |
| `openpilot/common/` | Params, timing, transforms, reusable utilities and hardware abstraction |
| `openpilot/cereal/` plus `msgq_repo` | Schemas, service definitions, process messaging and VisionIPC |
| `openpilot/system/camerad/` | Camera acquisition, frame metadata and buffer publication |
| `openpilot/selfdrive/modeld/` | Stock model execution, camera inputs and perception message publication |
| `openpilot/sunnypilot/modeld_v2/` | Sunny's alternative model runner and compiled model adapters |
| `openpilot/sunnypilot/models/` | Model selection, metadata, management and associated services |
| `openpilot/selfdrive/locationd/` | Localization, calibration and learned vehicle/delay parameters |
| `openpilot/selfdrive/controls/` | Planning and lateral/longitudinal control |
| `openpilot/selfdrive/selfdrived/` | Driving state, events and engagement coordination |
| `openpilot/selfdrive/car/` plus `opendbc_repo` | Vehicle state/interface/controller integration and car definitions |
| `openpilot/selfdrive/pandad/` plus `panda` | Host board communication and MCU firmware/safety; separate from host planning |
| `openpilot/selfdrive/ui/` | Actual driving/settings UI; consumes camera/model/state messages |
| `openpilot/system/ui/` | Shared raylib toolkit and comma setup/reset/update utility screens |
| `openpilot/system/loggerd/` | Logs, video encoding, rotation, storage cleanup and upload |
| `openpilot/sunnypilot/` | Fork additions including model, sunnylink, map and control/UI extensions |
| `tools/`, tests and replay utilities | Development/replay/verification helpers; inspect before running |
| Pinned external repositories | Messaging, vehicle definitions, Panda, filtering, RTC and Tinygrad sources; exact pins in Evidence |

The principal flow is camera pixels/metadata → model perception messages →
localization/planning → control requests → vehicle interface/board. UI and
logging consume those streams alongside vehicle/device state. The concrete
message contract matters more than launching similarly named processes.

System is not all of hardware support. Generic Linux chooses the PC abstraction
without `/AGNOS`; comma's platform path contains board-specific GPIO, KGSL,
power, modem and OS operations. Setting a marker or webcam flag is not a Q8B
port. See [SYSTEM.md](SYSTEM.md) and [RADXA_PORT.md](RADXA_PORT.md).

Historical deep navigation: [existing brain map](/home/radxa/comma/Ai/AI_BRAIN/00_MASTER_INDEX.md).
Check its own version/coverage before trusting old line numbers and paths.
