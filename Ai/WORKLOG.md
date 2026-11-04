2026-11-04 owner requirement: Chimera + Interceptor Core + Actuator Core are
all selected required hardware for the Radxa/Sunnypilot RetroPilot project.
Jobs: computer/CAN + vehicle signals; analog pedal/steering sensor interface;
custom actuator motor control, respectively. Recorded in DECISIONS and the
RetroPilot topic/session. Selection is not installed/tested status; existing
Chimera/physical Interceptor holds, noOutput and relay exclusion remain.

2026-11-04 DBC comparison: old/canonical and packaged current ocelot_controls
are identical (7363bytes,20messages,120signals,SHAef6eef74). Current port selects
this DBC already. Direct diff/provenance pass; no code/DBC or runtime change.
C2 source explanation session records details. Existing noOutput/hardware holds
and next actual BeamNG endpoint/profile qualification remain unchanged.

2026-11-04 session reopened: parentec53967/child671f8c4 clean. Explained C2
Ocelot naming from source: module firmware family, ocelotcan.py command encoder,
DBC wire definitions; modern commands.py supplies the encoder role. No runtime
change or hardware resumption. Existing noOutput/profile/Chimera holds remain.
See Sessions/2026-11-04-ocelot-c2-explanation.md.

## 2026-11-03 — Audit saved before owner-requested shutdown

Audited parent469f3c5/child671f8c4, both clean at start;10 source hashes match.
Fresh168 tests pass:50 safety,45 port,53 CAN,20 offline adapter/migration; Ruff
passes. Prior full safety8806/932 skips belongs to unchanged source, not a new
shutdown run. Modern port/shared registrations and two-header safety split are
saved in the audit report. Production noOutput/zero CAN, missing real profile,
held Chimera/Interceptor and excluded relays remain explicit. No device action.
Next after boot: read both handoffs/inbox, verify Git, resolve actual BeamNG car/
configuration and endpoint/units/mode/driver/calibration contract. No automatic
active output or hardware resumption. Owner requests normal local Radxa shutdown
only after all saves/validation; queue/readback is central shutdown receipt.
Report: Ai/Reports/retropilot-shutdown-audit-20261103/README.md.

## 2026-11-03 — RetroPilot active safety software engine, no live profile

Child opendbc671f8c450fc74f5b8b90b2ee53124394108651ce adds profile-dependent
sensor integrity/freshness, fault-latched engagement, driver intervention and
bounded/rate-limited interceptor steering/gas/iBooster-position checks. Only
an artificial native-test fixture supplies limits; no production initializer or
firmware parameter selects an active profile. Normal mode39 remains disabled-
command-only; interface noOutput/dashcamOnly and zero runtime CAN remain.
50 focused tests pass; full native suite8806 run/932 existing skips/no failures;
45 RetroPilot host tests, release-fixture absence, Ruff and whitespace pass.
Independent review required recovery/counter/health/startup fixes; all addressed,
final no Critical/Required findings. Startup models a full16-count disable
cycle peraxis; this is not receipt acknowledgement or installed-firmware proof.
Chimera and physical Interceptor held; relays excluded; no device/game/CAN action.

Owner asked which car Caleb used: pinned5435d674 launch says user spawns a car;
README has Ibishu Covet example and ETK800 rack examples. HONDA_CIVIC_2022 was
CAN/platform identity, newer BEAMPILOT measures the selected car. Owner's actual
vehicle/configuration remains unknown. Next: qualify selected game vehicle,
endpoint/units/mode/driver/calibration contract and then game-only integration.
No production limits inferred from C2 constants, DBC ranges or a demo model.
Report: Ai/Reports/retropilot-active-safety-20261103/README.md; source/test hashes
and remaining firmware/profile limits in the matching evidence JSON.

## 2026-11-03 — RetroPilot restricted safety mode implemented

Modern opendbc a6099a1e141f17ec18ca9b065cf9a8f972e0cac8 registers local
RetroPilot safety ID 39 and a disabled-command-only C policy. Seven canonical
steering/gas/brake disable packets are checked on bus 2; active commands,
relays, malformed frames, unknown parameters and forwarding are blocked.
The interface stays noOutput/dashcamOnly and controller runtime sends no CAN.
21 focused and 8777 full safety tests pass (932 existing skips); 45 RetroPilot,
53 CAN and 303 broader car checks pass (314 broader skips). New policy has
24/24 executable lines covered; debug/release C and Cereal C++ builds pass.
No Cereal source/DBC/model/firmware changes. Chimera is held; relays excluded.
Active policy limits, RX health/freshness and engagement remain unqualified.
Next: qualify those software/vehicle requirements without resuming held hardware.
Evidence: Ai/Evidence/retropilot-safety-20261103.json and report under
Ai/Reports/retropilot-safety-20261103/. This supersedes older "no policy file"
notes, not the remaining active-control limitations.

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

## 2026-11-03 — C2 controller migrated to modern offline replay

Modern C2 steering/pedal/relay calculation and timestamped JSONL replay are
implemented in opendbc9da9210adfa4dc213424f36945caccd40182c80d. Explicit offline
calibration only; default absent. update() still returns zero actual output/no
CAN.44port/53CAN/303broader tests pass (314existing skips), Ruff/whitespace pass.
All8linked C2 blobs verified at b9a942e; canonical DBC, hostbus2 and CD210GPU
unchanged. Next: receive-only Chimera backend, producer/profile qualification,
then shadow/game-only loop and actual MCU safety. Hardware/game/vehicle control
remains untested. Full session: Sessions/2026-11-03-retropilot-controller.md.

## 2026-11-03 — C2 RetroPilot identification mapped to modern selection

Owner asked why fingerprint registration was absent and requested teacher C2
comparison. Re-read immutable C2 values.py and selection/car_helpers.py:
values has placeholderIDs0..15/DLC8; selection hard-codes "RETROPILOT RETROFIT",
skipsFW queries and overwrites the matcher result. It did not identify the
retrofit through measured ECU/CAN fingerprints. Earlier explanation omitted
this distinction and compatibility with the old name was missing.

Implemented car/retropilot/fingerprints.py with C2-name MIGRATION and an empty
FINGERPRINTS map. Shared car/fingerprints.py merges that map; car_helpers
normalizes the old name before the RetroPilot no-diagnostic guard. Explicit
argument and FINGERPRINT environment accept both old/new names. Existing
Sunnypilot CarPlatformBundle migration now converts saved C2 names; tested
against actual native Params in caller-owned temporary directories. Other-car
MOCK selection stays unchanged. No global override or automatic matching added.

Source: C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728; parentbasec6917544;
opendbc649bbb6→04a78352a9605a0e07342146fe8481b7d92ee7fd on radxa/retropilot.
27RetroPilot/5Params/53CAN tests and303broader car tests pass (314existing
subtest skips); Ruff and whitespace pass. Canonical DBC, noOutput/passive
controller, speed factor0, hostbus2, CD210GPU eb741641 and firmware unchanged.
No model/manager/game/hardware/CAN TX or persistent owner-settings action.
Next remains receive-only Chimera backend and producer/profile qualification;
automatic identity and active MCU safety remain unimplemented. No new question.

Current receipt: Ai/Evidence/retropilot-c2-selection-20261103.json; source hashes
and RED/GREEN/regression logs retained. Skills: source-driven-development,
interface design, TDD/incremental implementation, Git, documentation and
self-review. Source-first path; no REA artifact/runtime question. No upstream
merge; inbox had0related pending and8historical failed/blocked records retained.

## 2026-11-03 — Car-port checklist: identification and safety remain separate

Reconciled owner's pasted modern car-port checklist with actual source and
commaai/opendbc README (official current structure/safety sections). Added a
file/status matrix to docs/RETROPILOT.md. Existing modern package/state/codecs
and explicit selection are implemented; active controller mapping, automatic
identification, RetroPilot MCU policy and compiled safety tests are pending.
No invented fingerprints or radar/safety stubs added. Current noOutput request
is not proof of Chimera enforcement; CarController itself always emits nothing.
Teacher C2 safety header remains WIP (arbitrary RX enables controls, disabled
integrity checks, DLC mismatches and missing steering/brake limits). Host file
creation alone cannot wire that policy into Chimera's actual TX path.

Source pins unchanged: parentbase1a1cc4025c4233732bbbb86c061c4c54b35add5a,
opendbc649bbb632a020f155fc1eb16ae343f49a5c4bb50; canonical DBC/source/model
unchanged. Documentation/source review only; prior53CAN/22port/1600native CRC
results remain prior results, not new MCU safety tests. No code/device/network
PC/firmware/actuation change; no REA binary question. Next implementation stays
receive-only Chimera transport, producer units/profile, then qualified active
control and MCU policy. No new owner question needed for this clarification.
Skills: source-driven review, code-review-and-quality, interface design and
repository documentation/Git. Validation: notebook, real file-status/relative
link assertions and whitespace, captured in the checklist evidence receipt.

## 2026-11-03 — RetroPilot car port implemented, receive-only

Owner explicitly requested RetroPilot as the car and Chimera as Panda. Modern
RETROPILOT_RETROFIT now registers in opendbc; canonical DBC/CRC/counters,
state/module parsing, button/override/stale handling and all8offline command
IDs implemented. Explicit selection suppresses OEM VIN/FW probes. Hostbus2;
no global car override, forced CAN validity or fake wheels/gear/torque.
Default speed scale0 marks sensors invalid; legacy km/h vs local Hall centi-km/h
must be qualified explicitly. CarController is unconditionally passive;
dashcamOnly/noOutput and placeholder geometry/tune do not establish control.

Submodule branch radxa/retropilot: codec eb64a22, platform649bbb6
(full649bbb632a020f155fc1eb16ae343f49a5c4bb50), baseaa9bff6f; parentbase dd29f00.
53CAN+22port tests pass;303broader car tests pass (314existing subtest skips),
490lateral-limit tests pass (31existing skips), Ruff/whitespace pass.
Compiled original CRC matches1600vectors across20canonical messages.
No devices/game/model/manager/firmware/CAN TX or actuation tested or enabled.
Next: receive-only Chimera backend + actual producer units/frames/hostbus2,
then full BeamNG telemetry/motion contract and optical shadow. Actual actuator
profile, live safety and endpoint calibration remain open. No owner question
needed to complete this code stage. Detailed topic/session/receipts below.

## 2026-11-03 — Connected PC requirements checkpoint

Owner reports connected BeamNG PC. Existing sim/beamng README now maps six
Sunny needs; actual gateway/Chimera/car/motion/command adapters remain pending.
Q8B eth1 UP10.43.0.1; neighbor10.43.0.216 reachable. Strict SSH exited255:
no trusted ED25519 host key; no remote inspection. Game/car/mods unverified.
Keep optical+CAN architecture/CD210GPU, canonical DBC and existing source pins.
Next: resolve trusted PC identity for read-only inspection and continue wire
contract increment1, then receive-only/shadow. No CAN TX or actuation.
Details/tests: Sessions/2026-11-03-beamng-requirements.md in both notebooks.


## 2026-11-03 — Radxa-focused docs assessment

Owner wants a simpler Radxa project. Inspected docs27files/366532logical bytes
before edit (~440KiBallocated). Useful porting/policy/logging/safety references
remain; comma connection/public-site pages are optional references, not Q8B
setup. Updated docs/README.md with a short Radxa entry index. Existing op docs,
site CI and car-doc generator/maintenance consume this tree. No deletion or
runtime change. Hardware selector still imports HardwareComma unconditionally;
HardwareRadxa inherits HardwarePc, so names alone do not justify pruning.
Detailed scope/limits: Knowledge/REPOSITORY_CLEANUP.md in the student notebook.
Next cleanup needs dependency-checked scope; current BeamNG wire-contract task
remains pending. Documentation-only checks; no REA binary/runtime claim.

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

## 2026-11-02 — Current owner focus: BeamNG bridge discovery

Owner moved from NPU research to running this Sunnypilot with PC BeamNG.drive.
Identified Caleb-J773/beampilot-drive at5435d674 (same as teacherOct28 pin).
Its same-host camera/telemetry/Lua path needs a PC↔Q8B adapter; current local
openpilot/tools/sim implements MetaDrive only. README successor steerpilot
publicURL/API return404. Saved source hashes, concrete API/image-size/freshness
gaps and staged camera→state→shadow→game-lateral plan in
[BeamNG notes](Knowledge/BEAMNG_BRIDGE.md). Research/docs only; no game, mod,
network listener, managed stack or model launched. CD210GPU stays selected;
failed W8A8 NPU baseline retained, precision experiment deferred. Next: prove a
recorded PC frame through sim-only VisionIPC/UI before a live game connection.

Checkpoint: conversion/replay safeguards committed as
`43678a671237bae095c1eb6fea95d78ff69d4261`,29focused tests and software checks
pass in maintenance ledger. All local research DLC/context/runtime assets are
inside ignored `modeld/npu/artifacts`; small receipts/results are tracked by the
following results checkpoint. Large ignored files do not travel through Git.
Actual final project HEAD is available from Git; no unfinished hardware worker.

## 2026-11-02 — Fresh INT8 device baseline complete; accuracy rejected

Owner approved research continuation while retaining the failed strict FP16
check. Fresh Mountain Dew v3 W8A8 runs on actual Q8B SDK2.37/v68/SoC37:
200heldout calls exit0 plus3native-byte cases (all42heads bitwise equal).
Calibrated DLC400356844bytes; integer-IO DLC400346268bytes; context444203008bytes.
200MB goal unmet. After132warmup,68teacher-forced frames have normalized RMS
errors29.65% packed,46.16% lane_lines,16.78% plan,43.31% action and189.26%
hidden_state. These are raw tensor errors, not driving-accuracy loss. Candidate
remains unselected; current CD210/OpenCL preview ce7b047/eb741641 unchanged.

29focused tests/Ruff/two shell syntax checks and normal-venv CLI help pass.
Model numerical acceptance FAIL; strict calibration1value and heldout96prewarm
FP16 checks remain visible. Independent original FP32 agrees bitwise on ten
calibration cases and both failed heldout cases. All500 source-state transitions
were independently replayed. CPU backend crosscheck is unsupported at quantized
FullyConnected; PTQ/backend error contributions remain unresolved. No candidate
self-feedback or parsed driving metric after this failure. DSPs running, scoped
clock lease closed/restored, no owned workers. Entire15.6387s run is not a model
latency benchmark. Next: W8A16/mixed activation/output precision experiment with
8-bit weights, then matched heldout comparison and broader calibration; no
modeld selection or vehicle actuation. Actual commits/validation in Git/ledger.

[Results](../openpilot/selfdrive/modeld/npu/RESULTS.md). Earlier entries below are dated checkpoints, superseded where stated.

---

# Sunnypilot work history

2026-11-02 — Started fresh Mountain Dew v3 NPU conversion in modeld/npu.
Updated Jetlink references; original/hash/IO/size inventory, new FP16/FP32
graphs and floatingDLC succeed. Review caught source video offset; initialdata
rejected, corrected700inputs validated, calibration500-v2 running.12focused
tests/Ruff/shell checks pass. No new NPU context loaded or CD210 change.
[Session](Sessions/2026-11-02-fresh-big-model-npu.md).

## 2026-11-02 — Hardware needs mapped to current Q8B support

Owner asked to update the complete requirements list with what Radxa supplies.
Updated NONCAMERA_HARDWARE with available interfaces, historical tests, actual
preview integration and remaining managed/vehicle work; corrected RADXA_PORT's
stale camera/model/UI-future statement. Read-only source/documentation task,
base d88a72c; runtime remains ce7b047, CD210 eb741641 unchanged. CPU/GPU/PWM and
timing already reach preview; other thermals/power, IMU/GNSS and platform/vehicle
providers remain distinct pending work. No driver, fan, model or runtime change.
Validation/limits and exact next step are in the linked session. Next candidate:
read-only managed thermal mapping; do not start a broader hardware port implicitly.

[Session](Sessions/2026-11-02-q8b-hardware-support.md).

2026-11-02 — Identified bundled driving model as CD210, verified actual ONNX
SHA/name/ref fingerprint and pinned upstream name source. Read protobuf
metadata/current parser; no inference or pickle execution.
[Session](Sessions/2026-11-02-model-identity.md).

2026-11-02 — Recommended current model/Adreno qualification next, using teacher
reference and CPU parity before live model/UI overlay. No implementation started.
Camera deferral and existing hardware plan preserved.

2026-11-02 — Owner accepts camera milestone for now; delay optimisation
and calibration stay deferred. Saved benchmark baseline and teacher-first
reference pointers for later. No runtime change or new engineering task.

2026-11-02 — Added and ran actual camera-to-UI benchmark:1200steady
frames/19.98FPS,draw-ready59.40msmedian and host frame return89.39msmedian.
37tests/lint and independent raw statistics/restoration pass.
[Session](Sessions/2026-11-02-camera-ui-benchmark.md).

2026-11-02 — Recovered actual preview cadence19.87FPS; current camera-to-UI
latency was not logged. Separated Oct31 standalone42msmedian/57msp95 timings.
Documentation only; no camera/clock/runtime changes.

2026-11-02 — Assessed temporary900px intrinsics: calculated70.834degree
HFOV agrees with old visual estimate only; capture/display is not lens proof.
No runtime change; owner calibration deferral retained. See latest UI session.

2026-11-02 — Added camera-only onroad dashboard launcher with private
messages/Params and owned-process cleanup.32tests/lint pass; live screenshot
viewed,173frames/9.06s, settings restored on close. Model not started.
[Session](Sessions/2026-11-02-ui-camera-preview.md).

2026-11-02 — Owner selected temporary MM-X camera method. Added scoped
720p/focal900 road geometry shared by model/UI; default guard and other
profiles preserved.30tests/lint pass; no model/camera run.
[Session](Sessions/2026-11-02-temporary-mmx-profile.md).

2026-11-02 — Explained automatic lens calibration, target-to-camera versus
vehicle-frame extrinsics, stock online-calibration limits and target-free
COLMAP option. Primary docs/source checked; guidance only, no runtime patch.
[Session](Sessions/2026-11-02-automatic-calibration-options.md).

2026-11-02 — Inspected actual MM-X RK camera/geometry/UI/calibration source.
External intrinsics required by README; focal900/720p hardcoded, mounting
calibration separate. Clarified checkerboard is optional measurement method.
5blob/4AST checks pass; docs only. [Session](Sessions/2026-11-02-mmx-camera-calibration.md).

2026-11-02 — Model layout fixed/qualified in6fea7ecf; owner chose printable
calibration target/tool. Added physical-size vector PDF/SVG, guided full-frame
collector and gated candidate solver.29focused tests, PDF/grid checks and real
Tk synthetic smoke test pass; actual printed-target data remain pending.

2026-11-02 — Teacher recovered AK-Camera60capture/20Hzmodel evidence; owner
approved road-only patch. Added self-contained UVC capture/latest NV12 publisher,
real timestamps, scoped driver-camera deferral and fixed-rate restoration.
21tests/140real IPC pairs pass. [Session](Sessions/2026-11-02-road-camera-patch.md).

2026-11-02 — Owner selected camera work and deferred hardware settings. Mapped
OpenCV capture, webcam publisher, process selection and Q8B geometry guard.
No application change/capture run. [Session](Sessions/2026-11-02-camera-entry.md).

2026-11-02 — Freshly inspected literal MM-X master and master-rk3588:11matched
blobs/9AST parses. Corrected broad answer: full board telemetry is not required
before webcam bring-up; MM-X leaves defaults/disables selected services. No
policy copied/runtime tested. [Session](Sessions/2026-11-02-mmx-rk-webcam.md).

2026-11-02 — Explained PC/Linux policy versus optional webcam input using actual
platform/factory/process source and read-only identity output. Full managed
runtime remains unqualified. [Session](Sessions/2026-11-02-pc-webcam.md).

2026-11-01 — Owner requested end-of-day audit and PC/VS Code shutdown. Fresh
11identity tests pass; clean Git/reference/controller, notebook and journal
checked. Saved tomorrow's H1 thermal starting point in both memories. No
hardware implementation. [Session](Sessions/2026-11-01-shutdown-audit.md).

2026-11-01 — Saved proposed non-camera implementation order from existing Q8B,
MM-X and Jetson evidence. Start with read-only thermal reporting and meaningful
failure/readback/schema tests; power, physical IMU and cooling follow. All
implementation remains pending. [Session](Sessions/2026-11-01-hardware-plan.md).

This is a curated history of work already recorded in workspace Ai. A historical
result stays tied to its original source/model/runtime and test scope.

| Date | Work and resulting knowledge | Evidence |
| --- | --- | --- |
| 2026-10-27 | Mapped current standalone camera/Adreno work versus missing managed Sunnypilot integration; identified camera/message/runtime/UI boundaries. Audit base was old `a5f44653`, not today's stock checkout. | [Integration audit](/home/radxa/comma/Reports/sunnypilot-radxa-audit-20261027/REPORT.md) |
| 2026-10-30 | Reviewed fork/version/lateral options and newer master changes. Recommendations did not establish Q8B or vehicle reliability. | [Selection](/home/radxa/comma/q8b/SUNNYPILOT_SELECTION.md) |
| 2026-11-01 | Owner selected a fresh stock Sunny start. Archived old complete custom checkout/model/patched runtime; verified fresh `6f7a2c94` assets and pins. | [Clean start](/home/radxa/comma/Ai/Reports/sunnypilot-clean-start-20261101/REPORT.md) |
| 2026-11-01 | Installed daily vendor update and every-commit ledger; created protected port; froze legacy worker helper imports. Original checks: 27 maintenance tests and 15 worker CPU tests. | [Maintenance](/home/radxa/comma/Ai/Reports/sunnypilot-daily-maintenance-20261101/REPORT.md) |
| 2026-11-01 | Mapped all 193 tracked system paths, inspected key functions and documented Q8B treatment. 139 AST parses and source/hash/link checks; no runtime port test. | [Local system guide](Knowledge/SYSTEM.md) |
| 2026-11-01 | Created specialist notebook shared by both Sunny checkouts, seeded history/topic maps and source index; added reserved-path update protection. Three collision regressions first failed; full maintenance suite now passes 31. | [Bootstrap session](Sessions/2026-11-01-bootstrap.md) |
| 2026-11-01 | Real maintenance check advanced vendor6f7a2c94→a86979d2, preserving notebook/port. New commit only hides Sunnylink Steering Arc toggle on mici. Stale notebook pin was detected, retained as a failed check and refreshed; premature no-advance documentation corrected without rewriting history. | [Versions](Knowledge/UPSTREAM_AND_VERSIONS.md), bootstrap session |

Future entries: date, exact changed repository/commit, resulting behavior,
actual tests and remaining limits. Keep full session details under Sessions.
Do not claim an uncommitted file is a tracked source commit.

2026-11-01 — Explained AGNOS versus generic Linux at the owner's request before
changes. Verified host Ubuntu24.04.5/aarch64/noAGNOS and actual source predicates;
generic Linux detection already works. Q8B hardware/GPU integration remains
future work, with no implementation approval or application/OS changes.
See [Linux platform note](Knowledge/LINUX_PLATFORM.md).

2026-11-01 — Reviewed MM-X master-tici b9b7f488 as a Linux reference, with20
Gitblob matches/13ASTparses. Identified reusable backend/camera/service concepts
and non-transferable KGSL, synthetic-clock, localization, calibration and old
schema assumptions. Source-only; implementation held for owner instruction.
See [MM-X study](Knowledge/MM_X_LINUX_REFERENCE.md).

2026-11-01 follow-up — Explained platform detection as hardware routing rather
than an OS-only check. Q8B needs no Rockchip detector; unchanged generic Linux
selection is correct, while CPU/model, camera, sensor and hardware-health gaps
remain. Source-only clarification, no application/OS edits.

2026-11-01 follow-up — Observed real DT modelRadxaDragonQ8B and compatible
radxa,dragon-q8b/qcom,sc8280xp. Proposed explicit board detector/HardwareRadxa,
keeping Linux build/non-comma flags and consistent schema/C++/camera identity.
No implementation applied; plain new device-type string alone would be invalid.

2026-11-01 clarification — Explained recognition, hardware-interface translation
and shared message/camera identity as separate jobs. Proposal remains unapplied.

2026-11-01 — Owner authorized board identity; implemented protected12e44fee.
11 Python/4 native wire checks, actual SCons profile, mutation rejection, Ruff,
syntax/diff checks pass. Read-only command confirms Ubuntu/ARM64/Q8B. Camera
geometry unconfigured; no full build or driving stack launched.
[Session](Sessions/2026-11-01-radxa-board-identity.md).

2026-11-01 — Owner corrected project location. Existing Radxa repository moved
into sunnypilot, clean upstream moved to q8b/sunnypilot-upstream. Real tracked
Ai replaces external link; old notebook history retained. Daily config/hook
retargeted; README and agent rules corrected. See
[session](Sessions/2026-11-01-project-location.md) for verification.

2026-11-01 — Explained existing board identity/build/schema/camera safeguards,
project memory and tested limits at b7fff536. No new application changes or
runtime launch. [Session](Sessions/2026-11-01-changes-explained.md).

2026-11-01 — Confirmed Git tracking to owner: source520d7f2 clean, journal
hook targets canonical project; all17managed local commits had validation.
Audit closeout is documentation only.

2026-11-01 — Owner made Agent Skills + REA and teacher/student restart continuity
explicit defaults. Added tracked HANDOFF, startup/recovery/closeout instructions,
updated rules and session template; retained T0 as next candidate. Documentation
only; [session](Sessions/2026-11-01-default-workflow-and-resume.md).

2026-11-01 — Owner selected hardware/sensors and deferred cameras. Mapped
accel/gyro/temp/GNSS and board-health API contracts; read-only host inventory
found thermal/power/PWM interfaces but no exposed IIO motion channels. Actual
IMU identity remains pending owner input. No hardware driver/setting/service
change. [Session](Sessions/2026-11-01-noncamera-hardware.md).

2026-11-01 correction — Owner required teacher-first lookup. Recovered known
Adafruit LSM6DS3TR-C/I²C9/0x6a, wiring and prior raw/schema tests from central
IMU/GPS notes and actual retained reports. Corrected model-pending/IIO inference
in current handoffs/map. Initialb62481cc factual-completeness failure retained;
current follow-up rechecks records. No new live I²C sampling or driver changes.

2026-11-01 — Expanded non-camera hardware checklist from current APIs, active
schemas and service consumers: thermals/cooling/power/utilization/IMU/GNSS/time,
network/UI/audio/lifecycle/peripherals and conditional vehicle/CAN/radar signals.
Distinguished outputs/estimates/optional fields and known Q8B evidence; no driver
or runtime change. [Session](Sessions/2026-11-01-hardware-checklist.md).

2026-11-01 — Reviewed MM-X non-camera hardware handling at freshly checked
b9b7f488:9 blob matches/8 AST parses. Compared empty thermal/zero power/GPU,
TICI-only fan/GNSS, real OS resource stats and carState-derived IMU policy.
Source-only, no implementation copied. [Session](Sessions/2026-11-01-mm-x-hardware.md).

2026-11-01 — Consulted teacher Jetson studies first; compared dedicated DP
hardware backend and separate overlay physical-IMU design with Q8B needs.
Fresh6source IDs/4blob/3AST checks; reused prior REA receipts with frozen file
integrity readback, no runtime re-execution. [Session](Sessions/2026-11-01-jetson-hardware.md).

2026-11-02 follow-up: webcam mode does not replace hardware support. hardwared
still reads Q8B providers; PC-disabled IMU/comma-only GNSS do not become active.
Adapt needed real board providers; reuse working OS stats, qualify optional
fitted hardware, and treat CAN/vehicle integration separately. No implementation
or runtime change; H1 thermal reporting remains next.

2026-11-02 model-input qualification: reproduced old packed720pbuffer failing
current modeld's1,413,120byte copy. Road-only output now uses get_nv12_info:
stride1280,Yrows736,UVrows368,UVoffset942080,allocation2,220,032bytes with neutral
padding. Generic mode unchanged. Added Q8B-only720pwarp build configuration.
23focused tests pass;140real frame pairs pass20.001Hz/59.628sourceHz with exact
layout/copy/padding/timestamps and restored settings. Pinned tinygrad92b742f7
CPU warp matches independent NumPy reference for two distinct synthetic views
bitwise; outputuint8[2,6,128,256] matches current ONNXnew_img metadata. No full
model/GPU/managed run or measured geometry claim. Weights65a08adc unchanged.
Owner selected printable target/tool; that next increment is in progress and
calibration guard stays active. New unstaged test_calibration.py is expected
RED until tool implementation; do not mistake it for a failure of this slice.

2026-11-02 — Inspected big pickle statically, recovered teacher's actual big NPU
conversion/timing and separated it from small W8A8 failure. Model identity and
floating-reference accuracy remain open; no runtime change.
[Review](Sessions/2026-11-02-big-model-npu.md).

2026-11-02 — Teacher-first Thneed lookup recovered actual exporter/native replay,
matched comparison and20min-soak evidence. Fresh artifact hash passes; no inference
rerun. Promoted old/current model difference and reusable approach.
[Session](Sessions/2026-11-02-teacher-thneed.md).

2026-11-02 correction — Confirmed Thneed usedCD210 learned core: direct old/new
ONNX checkpoint and learned-constant comparisons pass. Wrapper differs, weights
match. Corrected earlier different-weights claim in current notes.
[Confirmation](Sessions/2026-11-02-thneed-cd210-confirmation.md).

2026-11-02 — Copied existingCD210 Thneed plus metadata/fixtures unchanged;
packaged native replay/vendor/build and new NumPy/ctypes GPU runner/history
adapter/verification. No converter invoked. Fresh actual GPU12saved/12adapter
checks pass;42tests/lint. [Session](Sessions/2026-11-02-thneed-import.md).

2026-11-02 — Connected existingCD210 Thneed to stock modeld/current history/parser
with opt-in real-Q8B guards and native-only build selection; added isolated
camera/model/UI preview.51tests,32synthetic+6liveCPU checks and20Hz cleanUI bench
pass. All raw tails/restoration/build limits saved. [Session](Sessions/2026-11-02-thneed-modeld.md).

2026-11-02 — Corrected workspace-vs-project launch command and documented model-call
timing boundaries; no new inference benchmark. Help/import and memory/diff checks
pass. [Follow-up](Sessions/2026-11-02-thneed-modeld.md).

2026-11-02 — Explained missing acados via original limited bench-env setup and
actual import/distribution checks; ARM64 wheel is locked but untested. No installs.

2026-11-02 — Added newcomer install.md and Q8B declared dependencies; installed
clean locked Python environment, preserved recovery copies, passed minimal root
build/51tests/MPC/GPU and10sUI smoke. [Session](Sessions/2026-11-02-installation.md).

2026-11-02 — Implemented/reviewed/installed scoped max-clock lease; measured
65sbaseline20Hz/11.834ms inference/58.989ms capture-output. GPU input path remains
in progress. [Session](Sessions/2026-11-02-max-performance.md).

2026-11-02 — Completed resident GPU NV12 views/history and fresh capture defaults.
180s20Hz/11.085ms inference/37.886ms camera→output median; exactGPU and independent
CPU reference gates pass;68tests and live10sUI pass. Review-derived failure/reset
regression fixed. No NN conversion or tensor splitting. See MAX_PERFORMANCE.

2026-11-02 scheduling follow-up: unrestricted repeat38.204ms missed target;
singleCPU7 trial regressed to40.512ms. Fast cores4–7 default instead measured
36.829/41.592ms camera→output and10.817/11.790ms inference median/p95 at20Hz.

2026-11-02 accepted closeout: Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.

2026-11-02 — Owner requested all work committed. Verified clean source49d2f07
and57local commit records with none missing validation; saved documentation
checkpoint. No new runtime tests, upstream integration or remote push.

2026-11-02 — Started owner-requested live onroad telemetry panel. Read-only
sensor and bounded timing/window helpers pass5tests/Ruff; UI integration next.

2026-11-02 — Completed live onroad CPU/GPU/PWM/model/latency panel.76tests,
real15/65/10s UI and independent packet/frame/timer checks pass;65s20.0048Hz.
Controls remainoff; root/native/model unchanged. Outer65s143 anomaly retained,
independent restoration and final10s launcher0 verified. See UI_TELEMETRY.

2026-11-02 — Listed actual Q8B temperature channels:55thermal/58hwmon with
mirrors distinguished; other SoC/board/NVMe channels remain outside UI. Read-only
snapshot and mappings/limits saved; no runtime changes or hardware stress test.

## 2026-11-02 — Owner-approved INT8 research continuation

Owner explicitly chose “Continue INT8 research; retain failed FP16 check”.
The corrected 500-frame dataset is complete. Strict FP16/FP32 diagnostic still
FAILS at frame443: hidden element2218, .0017442703 versus -.0098324120;
hidden relative RMS .084442%, packed relative RMS .022077%. These are tensor
errors, not driving-accuracy percentages. Ten spread-out comparisons against
an independent original-graph FP32 reference are bitwise equal; precision
promotion is isolated from the host-FIFO/head rewrites on those ten cases.

Added explicit quantize-research mode; default strict gate remains unchanged.
Research requires pinned independent graph, exact bitwise diagnostics and full
native-file provenance; no deployment/vehicle acceptance. QAIRT2.37 rejects
SC8280XP and SC8280X target strings; generic HTP is supported and is being used
for PTQ only, without substituting historical SoC39. First rejected target log
is preserved. Full500-frame zero-state/own-FP16 recurrence is now independently
replayed before accepting calibration provenance. Review caught report-path
shadowing; owned audit was stopped before completion and corrected, inputs
preserved. Local17focused tests/Ruff/bash pass. No INT8/context/device result
yet. PC workdir remains /home/pc/sunnypilot-npu-20261102. No camera/GPU runtime,
clocks, firmware or vehicle changes. Next finish recurrent audit and generic
HTP PTQ, record actual size/encodings, then resolve target37 context support.

2026-11-02 research-tooling checkpoint:18focused tests, Ruff, shell syntax,
notebook64documents/196relative links and whitespace pass. Fresh reviewer
findings resolved; independent recurrence audit and PTQ remain in progress.
Strict FP16 failure is preserved and research artifacts remain unqualified.

2026-11-02 held-out/tooling increment in progress:200independently-reset
FP16 frames500-699 complete; all1200native+200golden file hashes and relocated
local list verified inside Sunny. FP32-vs-FP16 diagnostic fails94hidden values
at22 and2at66; all sampled warm cases pass. These failures remain visible;
independent original FP32 matches rewritten FP32 bitwise on both failed cases.
25tests/Ruff/bash pass; runtime/evaluator CLI help works in normal Sunny .venv
without conversion-only ONNX/ORT imports. New metadata/run linkage guards,
bounded private QNN runner and SIGTERM cleanup are reviewed. No NPU context
loaded yet; full500calibration/audit still running. Model defaults unchanged.

2026-11-02 checkpoint6b16d69 has25passing behavior tests but its final staged
whitespace check caught one extra blank EOF in metrics.py; shell continued
and committed. Failure is retained in the maintenance ledger. Immediate
follow-up removes that blank line; no behavior or threshold change.

## 2026-11-02 —500-frame W8A8 artifact complete; integer-I/O context work active

Fresh calibrated DLC is400356844bytes/SHA6cca7b518b6aa7d557727833d589de8a93dfe253a13a0a14f55fa81a3d7e3343,
inside Sunny npu/artifacts/w8a8-research.dlc and x86 dlc-v1. Quantizer exit0,
15m53s, all500frames. Wrapper later exited127 because its mutable shell source
was replaced during the long command; compiler artifact/exit0 preserved, no
recalibration needed. Future host stages use immutable hash-named snapshots.
Full independent500-frame zero/own-state audit passes, all3000native hashes;
strict FP16 comparison remains FAIL1value. Active audited report SHA77a3a166;
research receipt is npu/w8a8-research.json. Heldout200 localstaged/verified;
strict96prewarm precision failures retained, originalFP32exact on22/66.

SoC37/v68 context compile explicitly recognizes SC8280X but FAILS before device
loading: unsupported FP16 in FLOAT32→UFIXED8 desire I/O Convert. No context
binary and no NPU/clock/helper execution. Investigating removing floating I/O
boundary adapters using calibrated integer tensors, preserving all weights/
scales; do not switch to SoC39 or repeat500calibration blindly. SDK primary
Python source dlc_quantizer.py documents preserve_io_datatype via
ir_graph.modify_io_datatype; applying it again collides with existing converted
tensor names, so that in-memory probe was rejected without saving. Next inspect
IR squash/encoding API and validate any integer-I/O derivative before compiling.
PC workdir /home/pc/sunnypilot-npu-20261102; immutable host snapshotab8ea960;
context-v68-soc37-v1/log retained. No running conversion workers now.

Commits7157164 gatesresearch/18tests;6b16d69 heldout+bounded replay/25tests has
historical staged-EOF whitespace failure, corrected and validated by d2bb1b3a.
New uncommitted small audit/quant receipts and README changes expected. Current
CD210/preview defaults unchanged.200MB target unmet (~400.36MB measured DLC);
NPU numerical error/latency and closed-loop candidate recurrence unmeasured.

## 2026-11-03 — Hidden root folders explained

Read-only inspection at bf3c44d: .github contains tracked GitHub workflows/issue templates; .idea contains tracked JetBrains build-tool/custom-target settings; .run contains tracked CLion/Python UI build/run profiles. These are development/service configuration, not camera/model runtime providers. .install-backup-20261102 is an ignored local installation backup: five original native .so libraries plus SHA/size manifest (params, msgq, VisionIPC, UVC capture and Q8B Thneed replay), confirmed by install.md. It is not a complete repository/model backup. .ruff_cache is an ignored, regenerable Ruff lint cache (observed0.16.7). A leading dot normally hides an entry in Linux file listings. No folder deleted, configuration executed or runtime behavior changed. BeamNG optical/CAN implementation remains the active next task. Source-first documentation/Git skills; no applicable REA binary question.

2026-11-03 path lookup: shared fingerprints.py is opendbc_repo/opendbc/car/fingerprints.py; Hyundai example is car/hyundai/fingerprints.py. RetroPilot has no fingerprints.py; explicit RETROPILOT_RETROFIT is in car/retropilot/values.py:49. Verified by rg --files and absence check at parent c62cfe2/opendbc649bbb6; no runtime change.
