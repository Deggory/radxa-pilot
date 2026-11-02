# Dependencies and adaptation boundary

This is a selected source snapshot from beampilot-drive5435d674, not a full
checkout. All BeamNG-specific files from its tools directory are included:
both complete mods and their Lua tests; setup/TUI/diagnostic/monitor tools;
simulated-car installer/platform; tools/op.sh/setup scripts and TUI tests.
Outside tools, the bundle includes both daemons, every named beampilot module/
test, modified simulator helpers, selected integration snapshots, root launch/
config/setup/build/dependency metadata, README and MIT license.

The audit added14missing integration/import references, including MPC/event/UI
source, file_chunker and compile_modeld. No upstream snapshot replaces active code.

## Included references that need adaptation

- `upstream/openpilot/selfdrive/beamcamd`: local game capture, not a network
  camera receiver. PC capture and Q8B VisionIPC publishing must be separated.
- `upstream/openpilot/selfdrive/beamngd`: fork-specific CarParams, Cereal and
  simulator-helper contracts. Its BEAMPILOT car installer belongs to that fork.
- `upstream/openpilot/tools/sim/lib`: snapshot of the modified helpers, including
  SimulatedSensors' create_camera option. Current Sunnypilot helpers were not
  replaced. Configured1928x1208 input differs from Q8B Thneed1280x720.
- `upstream/openpilot/selfdrive/{car,selfdrived,controls,modeld}` and manager
  process config: original integration source for comparison. Their driving
  limits, alert changes, fake driver state and backend selection are not applied.
- Optional blindspot/radar/vehicle geometry, camera tuner and joystick source
  are retained so the daemons' BeamNG-specific imports and mod assets are present.

## Base project dependencies not duplicated

| Dependency | Where it comes from |
| --- | --- |
| Cereal/msgq and VisionIPC, native generated bindings | Base openpilot/Sunnypilot and the msgq submodule/build. |
| Full opendbc, Honda DBC, panda and vehicle model | Base project's pinned dependencies. Only the fork's added BEAMPILOT platform is copied here. |
| Localization, controls/planners/MPC, UI and native libraries | Base project source/build; selected modified files here are comparison snapshots. |
| Driving/DM models and generated GPU/Thneed artifacts | Existing project assets and their pins; no model downloaded or converted for this bundle. |
| Python/system package environment | Original pyproject.toml, uv.lock, setup scripts retained as references; keep active Sunnypilot's own environment/lock. |
| Consumer BeamNG.drive and desktop capture environment | Game PC, supplied separately. Full runtime adaptation/test still needed. |

The original `.gitmodules` is retained for remote provenance. Original root
submodule commits are listed in MANIFEST.json. No nested Git checkout,
submodule clone, compiled artifacts or external runtime symlink is introduced.
Generic car-porting, firmware/ECU tools, unrelated release helpers and most
unchanged core source are excluded from this BeamNG-focused source bundle.

## Validate and resume

`python3 verify_bundle.py` checks exact file coverage, SHA-256, Git blob IDs,
byte sizes and original permissions without importing upstream modules.
`sha256sum -c SHA256SUMS` is a second portable byte check. All 96 source files
were checked;69 Python AST parses,8 shell syntax checks and2 JSON parses pass.
Collection originally used source checks only. The later [audit](AUDIT.md) also
ran selected upstream Python tests with current dependencies:164pass/6fail/1skip,
2 collection-blocked modules and1 UI module not run. Lua/Vue/JavaScript/game
execution remains untested.

Do not run the copied setup launcher against the active port as an integration
step: it expects its full upstream project and installs that fork's simulated
car, environment and game mods. First adapt the recorded-frame camera boundary
from [our plan](../BEAMNG_RADXA.md), then prove live transport/state/shadow and
game-only feedback. Physical RetroPilot CAN/DBC and vehicle actuation remain
separate from this simulator source collection.
