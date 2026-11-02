Collection validation: all82Git blobs and SHA256 checks pass,56Python AST,
8shell syntax and2JSON parses pass. Ruff passes for our verifier/discovery guard;
notebook66docs/213relative links pass. Using existing isolated pytest9.1.1,
reference-folder collect-only reports no tests collected (expected exit5),
confirming the new foreign snapshot is excluded. Active Sunny venv lacks pytest;
no package installed to change that. No game/model or foreign behavioral test.

## 2026-11-02 — BeamNG source bundle collected

Owner requested all needed BeamNG files from Caleb's tools in a folder. Created
openpilot/tools/sim/beamng_reference/:82byte-identical upstream files,1025072bytes,
from commit5435d67499f66eca58f95882cbe35e9c577e874c. Both complete game mods,
setup/TUI/monitor/diagnostic, car installer/platform, camera/telemetry daemons,
common modules, sim helpers, relevant integration source/tests and root launch/
config/build/dependency metadata retained under upstream/ with original paths.
MIT license, original submodule pins, MANIFEST/SHA256SUMS and dependency guide
included. verify_bundle.py checks file coverage/bytes/SHA256/Git blobs/modes.
56Python AST/8shell syntax/2JSON source checks pass; original behavioral and
Lua/JS/Vue/game tests not run. Foreign snapshot tests excluded from automatic
parent pytest discovery only; existing project tests are unchanged. No installer,
mod, manager, model or game executed; no dependency/environment/DBC changes.
Next remains sim-only recorded PC frames→VisionIPC/UI; bundle is reference,
not a runnable standalone checkout or qualified PC↔Q8B backend.

# BeamNG bridge — current research checkpoint

Owner selected BeamNG/Sunnypilot simulation on2026-11-02; NPU precision work is
parked at its rejected W8A8 baseline. This is repository discovery/source review,
not an implemented or tested BeamNG backend. Start the portable
[sim guide](../../openpilot/tools/sim/BEAMNG_RADXA.md) and
[source receipt](../Evidence/beamng-reference-20261102.json).

Found Caleb-J773/beampilot-drive master5435d67499f66eca58f95882cbe35e9c577e874c,
unchanged from teacher's2026-10-28 audit. Same-host screen→VisionIPC beamcamd,
telemetry/fake-Honda/control beamngd and BeamNG Lua mod; noTech camera needed
for this approach. README successor steerpilot returns public404; do not infer
why. Current Sunny sim only creates MetaDriveBridge, at openpilot/tools/sim.

Local Q8B CD210 adapter requires1280x720/explicit road-only mode, versus external
1928x1208. External SimulatedSensors(create_camera=False) is incompatible with
our constructor. Game camera intrinsics must match render, not borrowed AK
webcam geometry. Retain PC loopback game control behind a gateway, versioned
network timing/session/freshness; BPL1 state lacks source timing/sequence and
its stale-derived commands could keep the Lua silence watchdog fed. Old BFR2
transport proofs/CPU ONNX game loop are historical and separate from current
Sunny integration. Canonical physical RetroPilot DBC remains distinct from fake
Honda simulator CAN; no bus or actuator opened.

Next exact implementation slice: recorded PC-frame fixture → dedicated sim
VisionIPC producer → existing Q8B UI with identity/time/layout/stale checks;
then live PC camera, timed car/motion state, shadow planning, and only then
game-only lateral feedback. Current USB camera/GPU model code/defaults unchanged.
No game/network/model/manager test in this source-review task. Source-first Agent
Skills; REA binary/runtime analysis not applicable. AST/shell/notebook checks
validate saved evidence/docs only; no full bridge/runtime claim.
