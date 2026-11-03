## 2026-11-03 — C2 history-led Radxa adaptation checkpoint

Owner confirmed existing Radxa Q8B. Full C2 history/submodules now mapped:
35parent commits,50final/64historical paths,82paths total. Added standalone
receive-only Chimera mailbox16/health43 adapter with pinned identity/version
and modern CAN serialization. Corrected angle STATE1 producer contract in
opendbc86a839dcec8ed9a3e45315eac804fa1001f1b2d6.15USB/45port/53CAN/303broader
tests pass (314existing skips), history coverage and Ruff pass. No live output.
REA GNU symbols/disassembly confirms retained43/16contract; native/layout
limits retained. Sysfs shows Interceptor DAC Bench, not historical Chimera;
no device opened. Current model/DBC/owner settings unchanged. Next: actual
Chimera receive acceptance, units/profile and managed truthful health/ignition;
MCU safety/physical actuation remain unqualified. Full dated session and
Ai/Reports/retropilot-c2-history-20261103/README.md record evidence/limits.

## 2026-11-03 — RetroPilot receive-only car platform now implemented

See [car port](RETROPILOT_CAR_PORT.md). The earlier car-port-pending statement
is superseded for registration/receive decoding/offline command encoders only.
Chimera USB backend, PC gateway, full state/IMU/session contract, optical shadow
and closed-loop control remain pending. Source pin649bbb6; no live CAN test.

## 2026-11-03 — Connected PC requirements checkpoint

Owner reports connected BeamNG PC. Existing sim/beamng README now maps six
Sunny needs; actual gateway/Chimera/car/motion/command adapters remain pending.
Q8B eth1 UP10.43.0.1; neighbor10.43.0.216 reachable. Strict SSH exited255:
no trusted ED25519 host key; no remote inspection. Game/car/mods unverified.
Keep optical+CAN architecture/CD210GPU, canonical DBC and existing source pins.
Next: resolve trusted PC identity for read-only inspection and continue wire
contract increment1, then receive-only/shadow. No CAN TX or actuation.
Details/tests: Sessions/2026-11-03-beamng-requirements.md in both notebooks.

## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Owner selected PC monitor → physical Radxa AK-Camera, and PC game gateway ↔ Waveshare CAN ↔ Chimera USB ↔ Sunnypilot. This supersedes the earlier network-camera next step. Added active openpilot/tools/sim/beamng/ PC/Radxa roles, shared CAN mapping/gaps and ordered plan; rewrote the current guide and reference README. No runtime code, DBC, firmware or remote PC files changed; no hardware/game/model launch or CAN transmission.

Recovered teacher facts: CH340 USB-CAN-A, 2Mbaud8N1 AA/55 variable framing; candidate500k CAN; historical Chimera hostbus2→MCUCAN3/connectorCAN2, 16-byte mailboxes/43-byte health and observed de193215 debug version. These do not prove current wiring/image or modern Panda compatibility. Canonical DBC6b90fafe/SHAef6eef74 lacks complete wheels/IMU/session/gear and cruise-status definitions; keep gaps central, no invented IDs.

Final CAN controller outputs must drive an explicit game actuator mapping; curvature-to-position bypass does not validate torque control. Physical bench steering/Interceptor/Core, brake and accelerator remain later. Resolve feedback authority and calibrated endpoint mapping before motion; do not resume the paused standalone VW experiment. Simulated IMU must not compete with stationary physical LSM6DS3TR-C. CD210GPU remains selected.

Next: wire-contract increment1 (speed semantics, versioned canonical extensions, golden vectors, deadlines/bus budget and game command family), then receive-only Chimera, optical shadow, game-only loop, later bench. Source-first Agent Skills: specification/planning, documentation, Git and review. No REA binary question in this documentation increment. Validation receipt: Ai/Evidence/beamng-hil-layout-20261103.json in Sunny; checks cover documentation/reference integrity, not HIL runtime.

## 2026-11-02 — BeamNG bundle audit complete; runtime adaptation still blocked

Audited collected source at projectbase f72a1ea/upstream5435d674. Added14missing
integration/import references; bundle now96files/1160682bytes, byte-identical
upstream. Allfile Git/SHA/mode/size checks;69Python AST/8bash/2JSON checks pass.
Fixed verifier accepting empty snapshots/wrong origin/pin/checksum list;12new
regressions pass, checksum-guard mutation caught. Snapshot tests with process-
local routing/current Sunny dependencies:164pass/6fail/1skip;2modules blocked
on import,1UI module not run. Five failures and two import blocks stem from
missing opendbc scale_tire_stiffness; onefailure assumes installed xdotool.
Test-only evdev2/mss10.2 installed under /tmp with locked SDist hashes; active
environment unchanged. UI/Lua/JS/Vue/game/model/manager tests not performed.

Source probes reproduce NaN accepted in96byte BPL1 and control-send called after
no new telemetry. Fork steering uses desiredCurvature→position, bypassing final
lateral torque; cannot directly validate custom actuator/NNLC. Same-hostIP,
camera1280vs1928, timing/freshness/session/finite and peripheral4vs2Hz require
adaptation. No copied upstream fixes applied to active runtime/DBC. Verdict:
reference bundle verified, direct runtime integration blocked. Next sim-only
recorded PC frame→VisionIPC/UI, then state/shadow and explicit lateral contract.
Detailed report: openpilot/tools/sim/beamng_reference/AUDIT.md; per-file/test
receipts alongside it. Relevant skills: source-first/code review, TDD/debugging,
git/docs. REA binary analysis not relevant to readable source/packet probes.

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
