2026-11-04 two-day owner Q&A backfill complete: [62 chronological records](QUESTIONS.md) (47 on November 3,15 on November 4) with [exact original questions/58 completed answers](Evidence/owner-qa-20261103-04.json). Three requests link to clarification continuations; this request has a separately labelled closeout. Existing Q&A/unknowns retained. Local documentation only; no push. Continue recording later questions and read related answers before follow-ups.

2026-11-04 owner Q&A memory rule implemented:explicit recent questions AND actual answers in [existing question log](QUESTIONS.md); startup/closeout instructions require retrieval and continued recording. Older unknowns retained; summaries are not full transcripts or automatic model training. Documentation only,local commit/no push.

2026-11-04 dual-DBC question answered:multi-parser support verified; OEM+RetroPilot requires explicit CarState integration, currently absent. No source/hardware change or push. [Details](Knowledge/RETROPILOT_CAR_PORT.md).

2026-11-04 dzid/ZSS clarification complete:SSC command/status0x22E/0x22F and ZSSangle0x50 already defined; matching layouts do not resolve dzid checksum/controller integration or physical calibration. Source/DBC unchanged; notebooks local only. [Details](Knowledge/RETROPILOT_CAR_PORT.md).

2026-11-04 DBC explanation complete:20messages/120fields,12reports/8commands; all signal names inventoried, defined data distinguished from current CarState mapping and actual producer/calibration. DBC and code unchanged, no live test. [Details](Knowledge/RETROPILOT_CAR_PORT.md). Notebook changes are local; no new remote push.

## 2026-11-04 — Radxa project published to owner GitHub

Public `Deggory/radxa-pilot`:master is original8cf6ff9a,radxa/q8b contains
our project and preserved commits,opendbc/retropilot retains child671f8c4.
All pre-task commit IDs retained; no source/model/history rewrite.290LFS
assets uploaded; fresh recursive checkout verifies all7dependency pins.
The existing sunnypilot-pc fork is untouched; new repo is a standalone public
copy. Camera/Thneed/RetroPilot bytes unchanged; live control stays disabled.
GitHub Actions and automatic upstream updates remain disabled/paused.
See [publication report](Reports/github-publication-20261104/README.md) for source pins, transfer evidence, tests and limits.

## 2026-11-04 — Owner-authorized GitHub publication in progress

Private `Deggory/radxa-pilot` created. Original `master`, Radxa branch and
RetroPilot support history are the accepted scope; only Sunnypilot project
contents. Portable submodule/LFS metadata prepared, large assets uploading,
remote clone verification pending. Original application0758b123 and child671f8c4
source unchanged. See [publication guide](../docs/GITHUB_RADXA.md). Timer remains paused.

## 2026-11-04 — Exactly two upstream updates approved and applied

Later owner instruction authorized a86979d2 and8cf6ff9a only, preserving
camera, Thneed/model and RetroPilot. Local application commits67876efc and
a009818b onradxa/q8b; eight source paths match upstream exactly. Protected
15,384 file hashes/submodule pins unchanged; child671f8c4 clean.217 distinct
tests passed,1 existing skip; native Params rebuilt for new default-on boost
option. This is CPU/source validation, not live driving acceptance.

Automatic reference updates remain paused; future updates need approval.
No further implementation is pending for this request. No live Params,
hardware, model or actuation run. See [the approved-update report](Reports/upstream-approved-20261104/README.md) for source pins, checks,
initial failures and exact scope; older hold-only entries below are historical.

## 2026-11-04 — GitHub master checked; all upstream updates on hold

Live GitHub master is8cf6ff9a (predictive acceleration boost,#2089,Nov4UTC).
It adds AccelBoostSP/defaulton, longitudinal boost logic, settings and tests.
Previousa86979d2 gates sunnylink steering-arc toggle on MICI. GitHub is2commits
ahead of our6f7a2c94 upstream base,1ahead of the previous a869 reference check.
No source integration or compatibility test performed. Actual project master/
origin-master remain6f7a2c94; Radxa code and child671f8c4 unchanged.

The daily job already advanced only the reference to8cf6ff9a at15:30UTC before
the owner asked. New owner instruction requires approval before updates.
Automatic timer is now linked/inactive and not enabled for automatic startup;
service inactive. Do not run mutating updater check or reenable it without
explicit approval. Read-only GitHub checks are allowed. See current upstream
policy, receipt Evidence/sunnypilot-master-check-20261104.json and dated session.

## 2026-11-04 — Owner-authorized topic labels applied to Git history

Camera/Thneed/RetroPilot subjects now use camera, thneed and retropilot scopes.
64titles reworded;28camera/16thneed/29retropilot commits, with mixed scopes.
90IDs changed by ancestry; all92local file trees, dates and message bodies match
originals. New tip before report213cd6d9; original6fb457bc retained under
refs/backups/20261104-before-topic-reword. Child671f8c4/gitlinks unchanged.
Original recorded SHAs are historical evidence, not stale hashes to replace:
use Ai/Reports/commit-topics-20261104/commit-map.csv or mapping.json to resolve
current IDs.90validation histories inherited without rerunning tests;17raw
failed/blocked IDs represent9original lineages, no new software-test failure.
No code/device/DBC/model/firmware or remote change. Preserve noOutput and holds.

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

2026-11-03 owner scope: relay features are not wanted. Current discussion is
RetroPilot safety-mode selection and enforcement. Chimera work remains on hold.
Preserve existing offline reference code; do not add relay integration.

2026-11-03 owner direction: **Chimera work is on hold until the owner resumes it.**
Current discussion is the need for modern RetroPilot messages and why C2 changed
Cereal. Earlier next-step notes about Chimera acceptance are deferred.

## 2026-11-03 — Owner clarification: modern RetroPilot implementation

The objective is to make RetroPilot work on the existing Radxa Q8B running
current Sunnypilot, with Chimera providing the CAN interface and BeamNG as
the intended initial vehicle environment. C2 is a behavioral/protocol reference.
The owner requested examination of cereal, opendbc, panda, selfdrive,
third_party and tools to understand what the author achieved and why.
Those folders and commits are research inputs, not an implementation checklist.

Identify the required RetroPilot behavior and CAN/hardware contracts, then
implement only the missing pieces through current Sunnypilot APIs. Reuse
existing modern capabilities. Do not recreate the C2 integration or require
matching edits in every old folder. Old build fixes, schemas, engagement
shortcuts and tuning machinery are not requirements merely because C2 used
them. Evaluate any proposed change against the current Radxa goal and evidence.

This clarification changes the framing, not the tested runtime status. No
runtime code was changed for this clarification. Next remains actual Chimera
receive acceptance, then current board health/lifecycle and vehicle-data
contracts. Historical review is supporting evidence, not live validation.

2026-11-03 history explanation: complete53-commit plain-English2025guide saved in
sunnypilot/Ai/Reports/retropilot-c2-history-20261103/2025_COMMITS.md.
No runtime change; actual Chimera receive acceptance remains next.

Owner communication preference: plain-English explanations first; coding details when requested. DBC inclusion rechecked; partial port versus live integration must remain explicit.

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

## 2026-11-03 — History-led modern RetroPilot adaptation in progress

Owner confirmed existing Radxa Q8B, not physical comma4. Parent history:
35commits/50final changed paths/64ever-touched paths;28commits dated2025,
7older upstream. All35commit diffs and pinned panda/cereal/opendbc comparisons
saved under sunnypilot/Ai/Reports/retropilot-c2-history-20261103/.
Angle STATE1 correction passes45port tests; previous STATE0 assumption was wrong
for reviewed Chimera/ZSS producers. Receive-only USB mailbox16/health43 adapter,
serial/version/product pins and modern CAN serialization implemented;15adapter
tests being finalized. No live output or settings/firmware changes.
REA GNU symbols/disassembly of retained Chimera ELF5ae9b4f6 confirms43-byte
health and16-byte mailbox stride; can_send's visible body queues without a
safety hook. No complete safety proof. Native decompiler not configured and
pwntools layout profile is Linuxx64-only; GNU fallback succeeded.
Read-only sysfs currently shows bbaa:ddcc product "Interceptor DAC Bench",
serial440048001251333133333633, bus3/device8. This is not the historical Chimera
serial3a0044001651333038373636. No USB handle opened or CAN consumed. VID/PID
alone must not identify a Chimera or resume the paused bench project.
Next: finish migration coverage map/tests, commit verified code and record
remaining raw health/manager/safety/profile qualification. CD210GPU unchanged.

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

## 2026-11-03 — RetroPilot car port in progress: canonical codec

Owner explicitly requested modern RetroPilot as the car and Chimera as Panda.
Read teacher RetroPilot/Chimera notes and canonical policy before coding.
Started opendbc branch radxa/retropilot from aa9bff6f; registered the submodule
in maintenance config (controller cdc20d4) and installed commit journaling.
Canonical DBC copied byte-identically (SHAef6eef74), SAE-J1850 CRC and automatic
counter validation added. RED missing-DBC tests reproduced; GREEN52CAN-library
tests, Ruff and whitespace pass. No hardware, transmit or firmware action.
Legacy speed consumer uses km/h, saved local Chimera Hall source multiplies by100;
MODE/config producer differences remain unqualified. Keep explicit scale/validity.
Next: modern platform/CarState and receive-only controller plus offline commands.

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

2026-11-02 held-out/tooling increment in progress:200independently-reset
FP16 frames500-699 complete; all1200native+200golden file hashes and relocated
local list verified inside Sunny. FP32-vs-FP16 diagnostic fails94hidden values
at22 and2at66; all sampled warm cases pass. These failures remain visible;
independent original FP32 matches rewritten FP32 bitwise on both failed cases.
25tests/Ruff/bash pass; runtime/evaluator CLI help works in normal Sunny .venv
without conversion-only ONNX/ORT imports. New metadata/run linkage guards,
bounded private QNN runner and SIGTERM cleanup are reviewed. No NPU context
loaded yet; full500calibration/audit still running. Model defaults unchanged.

Research tooling71571642 committed and validation journaled:18tests/Ruff/bash/notebook pass. PTQ and independent500-state audit plus heldout200 generation remain active on x86 PC; no NPU model loaded.

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

2026-11-02 NPU checkpoint d450dbbd committed/validated (12tests). Corrected
calibration500-v2 completed all500native frames but strict prequant FP16/FP32
diagnostic FAILED atframe443:1hidden_state value(reference .00174427 vsFP32
-.00983241), hiddenRMSrelative.0008444, packedRMSrelative.00022077. Gate blocks
PTQ; no INT8/context/NPU loaded. Investigating same-precision full7input/4output
FP32 reference to isolate promotion rounding from graph-rewrite errors; original
failure remains preserved. source/graph/DLC pins unchanged. New uncommitted
qairt_host help/SC8280 target, diagnose_case/semantic_reference scripts and
receipts are expected current work. PC workspace /home/pc/sunnypilot-npu-20261102.
Known HTP/stub/skel now match SDK2.37aarch64-ubuntu-gcc9.4 exactly; oldSystem
stilldifferent, matchingSDKSystemavailable. REA open_binary validated HTP ELF
identity/e33be7a2/arm64 only, no decompilation/execution claim. Initial700-v1/
native500-v1 stay rejected; correctedroad700-v2 complete and format2 now required.
Next inspect semantic-reference/diagnostic443-FP32, preserve failed gate; do not
silently relax it or claim INT8 accuracy. Last code/data checks passed12tests.

# Resume Sunnypilot here

## 2026-11-02 — Fresh Mountain Dew v3 NPU experiment in progress

Owner selected fresh big-model INT8/PTQ work inside modeld/npu and requested
Jetlink updates. Read teacher Jetlink/NPU history. Source ONNX35976b11 downloaded
768750198bytes via configured1e219d model ref; original pickle d4c7a3fc unchanged.
Inventory382904774FP16values implies ~383MB INT8payload before overhead;200MB
not promised. Fresh FP16 CPU reference da9506a6 and FP32 source eceadb80 generated
on trusted x86PC, new floatDLC conversion exits0. 10initial FP32/FP16 comparisons
had no values outside .01+1%; not INT8/driving accuracy. Full PTQ pending.
Reviews (agent + owner-selected Codex CLI) caught ordinal/video alignment bug:
old extractedroad700 and incomplete calibration500-v1 rejected, worker stopped.
Corrected road700-v2 complete:700unique/cadenced encoder-mapped inputs; fresh
calibration500-v2 running on the x86 host.
Source/DLC/data hashes, continuity and spread-out warm diagnostics now gated.
12focused tests/Ruff pass; no experimental NPU context/device/clocks/firmware
operation. Current CD210/OpenCL preview ce7b047 unchanged. Conversion tool venv
installed locally; scope/provenance/commands in modeld/npu/README and session.
Jetlink refs now Zoompilotaf9df78/v0.8.13,mouxangithub7425e98,FOREVERb8cbb92;
3clean manifests verified, previousrefs preserved. Old bundleverifier separately
fails pre-existing q8b source drift; not a new clone mismatch. Runtime target
soc37 vs historical39/library-stack identity remains open before NPU execution.
Next: finish corrected road700-v2, validate mapping/cadence, copy toPC, run
fresh pinned500-frame recurrent state builder, verify receipt, then W8A8 PTQ.


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

## 2026-11-02 — Q8B live onroad statistics complete

Owner-requested panel is on the actual Sunny AugmentedRoadView, enabled by
Q8B road-only mode; Q8B_SHOW_STATS=0 hides it. Shows hottest readable CPU/GPU,
fan PWM percent/raw/mode (RPM unavailable), GPU inference/readback, full model,
modelHz, camera→model and camera→UI first draw. Read-only sensors1Hz on a worker;
2s timing medians, display4Hz, stale timing1s/sensors3s, unavailable as dashes.
76tests/Ruff pass. Complete65sUI:1293camera frames/1274model messages/33path
points,20.0048Hz; inference10.933/12.133ms and capture→model36.832/41.043ms
median/p95. Overlay samples match model benchmark exactly; UI endpoint precedes
benchmark draw-ready by0.781ms median. UI benchmark draw-ready45.390/58.292ms;
host EndDrawing74.590/88.904ms. Physical display latency remains unmeasured.
Full65s child exits0/0/0; outer command143 after completion remains unexplained.
Independent cleanup passes; final10s command/children exit0,179matching packets,
zero rejections. Camera/clocks restored, GPUfaults0, fan mode staysautomatic.
Model/native/root helper hashes unchanged; no new conversion/calibration/control
or vehicle/hardwared integration. Data helpers committed5e01a48; this UI increment
and exact validation are saved in Git/ledger and the portable UI receipt.
Next: normal preview --model shows the panel; owner selects later work.
[Details](Knowledge/UI_TELEMETRY.md), [receipt](Evidence/q8b-ui-telemetry-20261102.json).


## 2026-11-02 — All project work committed

Owner requested a complete commit checkpoint. Git audit found a clean
radxa/q8b tree at49d2f07432541d9456acb60369a8f959db4c5611. All57tracked local
commits had validation records; latest GPU increment has a passing receipt.
This documentation checkpoint records that audit. Runtime/source/model are
unchanged; previous68tests and hardware benchmarks were not rerun. Next task
remains owner-selected calibration/hardware or optimisation, with controls off.


## 2026-11-02 — Resident GPU baseline complete

Q8B Thneed defaults to resident exact NV12 crop/packing/lag4 history, fresh60FPS
source selection at20Hz, and worker affinity on fast cores4–7. Scoped max clocks
are automatic; owner already installed the helper, no routine password request.
Existing CD210eb741641 remains unchanged; no conversion or feature splitting.
Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.
Calibration remains provisional/invalid, controls and DM off. No new20min soak,
full-manager/vehicle test or physical-display-latency claim. Unrestricted38.204ms
repeat and CPU7 regression40.512ms retained; adopted fast profile has two passes.
Next: launch normal preview from project .venv; choose later calibration/hardware
or optimisation separately. No active experiment or unfinished source edits.
This verified increment is recorded by its Git commit and maintenance receipt;
base623f728a, exact source/model/runtime hashes in the portable evidence.
[Details](Knowledge/MAX_PERFORMANCE.md), [receipt](Evidence/q8b-resident-20261102.json).

## 2026-11-02 — Full locked dependencies installed; minimal build passes

New [install guide](../install.md) covers setup/build/tests/preview for newcomers.
Python3.12.13/uv0.13.6;85packages/all extras+standalone, no external bench paths.
q8b OpenCV/Pillow extra; existing lock versions unchanged. Tinygrad examples
local .pth documented. Default .venv replaced after staging51tests; old env and
5native libraries retained as ignored backups. Root minimal Q8B/Thneed build
now passes; previous missing-acados block is resolved. MPC solver constructs.
Final51tests,12GPU/12adapter checks and10sactual camera/model/UI pass:
193frames/183models/33pathpoints, allchildrenexit0, camera restored,faults0→0.
No new conversion/driver/system/clock changes. Provisional geometry/controls off;
full manager/vehicle/sustained performance unqualified. Next use install.md;
hardware/geometry work remains separate. [Details](Knowledge/INSTALLATION.md).

2026-11-02 acados diagnosis: limited preview .venv never received the full
locked dependencies. acados/SCons plus several other native-package imports
are absent; lockfile includes ARM64 comma-deps-acados0.2.2.post103. No install
or runtime change. Full dependency qualification remains separate work.
Details: Ai/Sessions/2026-11-02-thneed-modeld.md (student).

## 2026-11-02 — Launch directory and timing clarified

Enter `~/comma/sunnypilot` before `.venv/bin/python -m openpilot.system.camerad.webcam.preview --model`;
the parent `~/comma` has no project virtual environment. Help/import checked
from the correct directory; no new camera/model run. Current36.656/46.326ms
model-call timer includes CPU warp/history/uploads/GPU/readback/parser, excludes
camera capture/JPEG decode/NV12 and UI drawing. Current GPU-only split remains
unmeasured; historical11.724ms cannot be subtracted to infer camera cost.
Runtime/model unchanged at07bc78e; docs-only follow-up, provisional geometry and
controls-off scope retained. Next: owner retries launch; per-stage timing needs
a separate measurement if requested. See modeld session follow-up.

## 2026-11-02 — Thneed modeld/camera/UI integration verified

ExistingCD210 artifacteb741641 unchanged, no reconversion. Q8B_THNEED=1 selects
new ModelState-compatible GPU replay/current history/parser in stock modeld;
requires real Q8B/road-only webcam. Uses pinnedCPU:LLVM NV12 warp, two views,
zeroed warmup/reset and copied output-slice metadata. Alternate model warmup and
Tinygrad NN compilation bypassed only in this mode. Defaults unchanged.
Launch from project: `.venv/bin/python -m openpilot.system.camerad.webcam.preview --model`.
Private camera/modeld--demo/actualUI session; no vehicle/control/DM processes.
Temporary MM-X/zero-mount assumption stays uncalibrated; model validity false.
51tests/lint pass;5exact warp checks,32synthetic recurrent CPU checks and6actual
live CPU-reference samples pass all2576values at rtol.001/atol.005.
Clean65s run:1201steady model receipts/19.998Hz; full model call36.656/46.326ms
p50/p95; source→model receipt at UI94.754/115.031ms. Includes prep/queues/GPU/parser,
not inference-only.23calls>50ms,max54.214,one receipt ID gap retained.33point overlay
visually verified. Diagnostic run with6snapshot writes19.632Hz/max267.672ms;
kept separately. All children exit0; camera/policies restored,GPU faults0→0.
Targeted native SConscript passes; whole build stops at missingacados, other
build dependencies unchecked. Camera optimisation/vehicle/soak qualification
remain open; no automatic hardware-plan resume. [Session](Sessions/2026-11-02-thneed-modeld.md).

## 2026-11-02 — Existing CD210 Thneed imported and replay verified

Owner says reuse converted model; do not reconvert. Copied accepted99641029byte
Thneedeb741641 unchanged to openpilot/selfdrive/modeld/models/q8b_cd210.thneed,
plus metadata/fixtures. All replay source/vendor/licenses/build scripts now inside
Sunny at openpilot/selfdrive/modeld/thneed_q8b. New NumPy/ctypes runner has no
external-experiment/Tinygrad runtime import and checks hashes/matching GPU driver.
Current history-queue adapter preserves old compiled model; no model conversion.
Native ARM64 library built;12saved exactCL/CPU tolerance checks and12queue cases
pass.42focused tests/lint pass.40same-input host calls12.114msmedian/15.851msp95
includes upload/validation; repeat14.223/16.545ms also passes. Dynamic policies
unchanged, no camera/maxclock/20min rerun.
Current manager/modeld selection unchanged. Next connect checked backend to
live modeld/publication/overlays, qualify current recurrence and20Hz timing.
Camera optimisation remains deferred. [Session](Sessions/2026-11-02-thneed-import.md).

## 2026-11-02 — Confirmed: Thneed ran CD210 learned core

Fresh ONNX checkpoint/tensor-content comparison confirms old659727c4 and
current65a08adc share learned weights; changed history wrapper explains file
differences. Corrects earlier different-weights claim. Thneed artifacteb741641
traces to oldCD210; current-wrapper runtime still needs integration qualification.
[Confirmation](Sessions/2026-11-02-thneed-cd210-confirmation.md).

## 2026-11-02 — Teacher Thneed pipeline recovered

Prior portable OpenCL Thneed small-model pipeline is already implemented and
bench-tested:20min/24101steady frames at20Hz, model11.724msmedian/12.348msp95,
camera→output35.417/39.721ms under maxCPU/GPU690/EGL/partial-JPEG profile.
Fresh existing driving-02 artifact hash matcheseb741641. Old659727c4 and currentCD21065a08adc have
the same learned weights; the ONNX history wrapper differs. Reuse exporter/replay design after
current-contract/parity qualification; no new runtime port/run in this task.
[Reusable methods, files, pins and limits](Knowledge/THNEED_GPU_REFERENCE.md).
[Session](Sessions/2026-11-02-teacher-thneed.md). Camera optimisation stays deferred.

## 2026-11-02 — Big model NPU feasibility reviewed

Bundled big Tinygrad artifact targets Chestnut/AMD, not direct QNN loading.
Fresh static opcode/hash inspection:799941965bytes,SHA256d4c7a3fc, no unpickling.
Teacher already has separate historical big-model W8A16 QNN2.37/v68 conversion:
Oct31 short replay38.196ms graph/41.515ms host medians, excluding camera;
bitwise quantized-baseline parity does not resolve floating-reference accuracy.
Identity of that6fee5937 ONNX versus bundled Mountain Dew v3 is unestablished.
First NPU research step is graph/weights/state identity comparison; do not
recompile/retest or promote historical timings as current Sunny performance.
CD210/Adreno remains recommended next integration; no backend changes started.
Camera optimisation remains deferred. See [NPU review](Sessions/2026-11-02-big-model-npu.md).

## 2026-11-02 — Model identity recovered: CD210 default

Bundled driving_supercombo.onnx is labelled CD210 with ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391.
Actual file SHA25665a08adc/name/ref fingerprint matches tracked model_hash and
pinned official upstream name file. ONNX metadata/input/output schema inspected
without executing pickle metadata. Separate big_driving_tinygrad.pkl is labelled
Mountain Dew Model v3 for Chestnut; do not confuse the two. Parser supplies
path/motion/lane/edge/lead/pose predictions; current source targets20Hz.
Identity verification does not prove current GPU inference or driving behavior.
Next recommendation remains CD210/Q8B Adreno qualification. No runtime change.
See model-identity session and student UPSTREAM_AND_VERSIONS for exact evidence.

## 2026-11-02 — Recommended next step: current model on Q8B Adreno

Owner asks what comes next after accepted camera milestone. Recommendation,
not started: qualify current Sunnypilot stock driving model on Q8B Adreno,
using teacher's earlier MSM/Thneed work as reference while retaining Linux/Q8B
identity. Current helpers.load_oob selects CPU:LLVM on non-AGNOS Linux; simply
opening camera UI does not activate GPU model inference. Do not fake AGNOS.

First increment: map current model inputs/history/state/output parser and run
one isolated correct GPU inference against a CPU reference. Then qualify
bounded camera→model publication at target20Hz, and finally show model path/
road predictions in actual Sunny UI. Validate numerical agreement, real timing,
message freshness and clean restart/stop. Earlier20Hz standalone evidence is
for different model/runtime; it is not proof current weights will meet20Hz.
Source base679bf8d; current stock model65a08adc,tinygrad92b742f7,msgqe7396e76.
Model input uint8[2,6,128,256] and padded camera boundary were previously checked;
full inference, state/history/runtime integration remain open. Teacher first:
Ai/Knowledge/Repos/sunnypilot.md, camera.md and Oct31 soak source db5b0da.

Keep camera optimisation/calibration deferred. Hardware plan tasks/plan.md is
preserved, not automatically resumed or replaced. Known physical IMU/vehicle
feedback/hardware providers remain later integration work. No new runtime,
model conversion/launch, GPU driver or vehicle action by this recommendation.

## 2026-11-02 — Camera bring-up accepted for now; optimisation deferred

Owner says camera work is done for now and will return to teacher knowledge
later to reduce delay. Preserve current capture/UI and temporary MM-X geometry.
Benchmark baseline7ac07b5:1200steady frames/19.97562FPS; driver→draw-ready
59.398msmedian/78.755msp95; driver→EndDrawing return89.385/109.139ms including
normal pacing. No further camera optimisation/calibration changes now.
Future work starts from teacher camera/Sunnypilot notes and the Oct31 retained
pipeline report/source db5b0da, with its different model/runtime/max-clock
conditions kept explicit. Compare matching endpoints/profiles before porting.
Current optics/mount and full model/vehicle qualification remain open; owner
acceptance covers camera bring-up/preview/benchmark milestone only. No next
engineering task selected in this message. No runtime changes or new tests.

## 2026-11-02 — Actual camera-to-UI timing benchmark completed

Added opt-in native preview benchmark,37focused tests/lint pass.65.057srun,
5swarmup,1200steady first-display samples at19.97562FPS. Driver timestamp to
draw-ready59.398msmedian/78.755msp95; to EndDrawing return89.385/109.139ms,
including normal30FPS pacing. Actual GLfreedreno FD690/Mesa25.2.8; default
CPU schedutil/GPU simple_ondemand, no clock/fan overrides. Not optical latency
or confirmed compositor presentation. Raw samples independently recomputed.
Camera/UI exit0/0, previous1080p30/dynamic-rate1 restored; no active preview.
No model/vehicle run or calibration change. See camera-ui-benchmark session
and webcam README command. Model/Adreno integration still pending; automatic
calibration deferred. No optimisation undertaken beyond measuring this baseline.

2026-11-02 timing answer: latest preview19.87new camera frames/s (~50.33ms
interval), not measured camera-to-screen latency. Older standalone42.186ms
median/56.996msp95 is separate. No runtime change or camera relaunch.

2026-11-02 intrinsics assessment: temporary900px/720p implies70.834deg
horizontal FOV under a pinhole assumption; old70deg was only visual. Camera/UI
video is verified, lens geometry is not. Keep owner-selected temporary profile;
no automatic calibration resumed. Persistent preview12790/12793/12794 has now
closed normally:1514distinct frames/76.200s, child exits0/0; no relaunch requested.

Live preview reopened in persistent terminal session21631: controller12790,
camera12793,UI12794; prefixq8b_preview_97ce0a9e4384. Actual screenshot
owner-persistent.png verified and child PIDs alive. Logs:workspace
Ai/Reports/sunnypilot-ui-preview-20261102/owner-persistent. This supersedes the
previous closed-session state. Window intentionally open; close it to stop
camera/restore settings. Check current PIDs before later camera work.

## Owner preview closed normally — 2026-11-02

UI implementation536470bd4fe9ab9abb68f9af9320ee8b315aecd2 is committed.
Owner-facing session controller12416/camera12417/UI12418 displayed849distinct
camera frames over42.917s, then exited normally0/0; closure cause unconfirmed.
No preview process remains. Prior1080p30MJPG/dynamic-framerate1 restored exactly.
Reopen from Sunnypilot root with
`.venv/bin/python -m openpilot.system.camerad.webcam.preview`.
No model/vehicle processes started; automatic calibration remains deferred.

## 2026-11-02 — Live Sunnypilot camera dashboard verified

Owner requested opening the UI to view road-camera output. Added webcam/preview.py
camera-only launcher using the actual Sunnypilot onroad widget/HUD. Private
message prefix/temporary Params; UI-only demo started/ignition data. Starts
camera+UI only, no model/planners/vehicle/controls/recording.32focused tests/lint
pass; live9.06s check rendered173distinct frames, actual screenshot viewed.
Final4s lifecycle check passes; child exit0/0 and prior1080p30/dynamic-rate1
restored. Stock model and temporary MM-X intrinsics unchanged. UI speed is a
demo default, not car telemetry; no AI prediction/vehicle integration claim.
Next: use camera preview; model/Adreno qualification still pending. Automatic
calibration remains deferred. See ui-camera-preview session and webcam README.

Saved implementation commit: `d0d654a66c04f57a39cb3dddb8516c6309e992e6`
(`feat: use temporary MM-X geometry in Q8B road-only mode`). Owner requested
commit update2026-11-02; verified project clean and this commit's validation
journal attached, with no missing local validation or pending upstream review.
Its30tests/lint results are retained evidence, not a new runtime run. This
checkpoint update changes documentation only; next work remains model/Adreno
qualification with provisional geometry and calibration work deferred.

## 2026-11-02 — Temporary MM-X geometry selected and implemented

Owner: keep MM-X method for now, change later. get_device_camera_config now
returns borrowed720p/fx=fy900/centre640,360 for radxaQ8b/unknown only when the
existing Q8B_ROAD_ONLY+USE_WEBCAM mode validates the actual board. Cabin/wide
remain absent. Model/v2/UI share this lookup. Outside that opt-in mode, Q8B
calibration remains unconfigured; comma/PC profiles unchanged. Profile is not
measured AK calibration and supplies no distortion or mounting pose. Auto
calibration/target capture deferred; tools retained. Capture60/latest20Hz and
calibration-status/DM/vehicle policies unchanged. No camera/vehicle run.
30focused tests and lint pass; see temporary-mmx-profile session. Next qualify
current model/Adreno integration using this explicitly provisional geometry;
replace intrinsics later, do not auto-resume target/autocalibration work.

## 2026-11-02 — Automatic calibration requested: options explained

Owner asks how to automate intrinsics and extrinsics. Proposed auto-selection/
lens solve plus mounted camera/known vehicle-aligned target pose for R/t; target
motion/placement remains physical input. Current capture still requires Space;
no autosave or vehicle-pose export implemented. Online calibration assumes zero
roll and does not solve K/distortion/full6DOF. COLMAP target-free estimates are
an untested alternative, needing validation and vehicle-frame alignment.
No runtime/settings changed; next resolve preferred measurement workflow before
implementation. See automatic-calibration-options session for sources/limits.

## 2026-11-02 — MM-X RK lens-parameter check

Owner questioned the checkerboard step. RK3ad69b20 README requests external
intrinsics (example:GMLCCalibration); geometry/UI store720p focal900,centre640/360.
Online calibration estimates mounting alignment, assumes zero roll, and does
not solve lens K/distortion. His actual measurement procedure is undocumented.
Checkerboard is an available method, not a Sunnypilot requirement. Next resolve
an appropriate AK lens-parameter source; printing/capture is optional pending
method choice. No runtime edits or geometry activation; guard stays active.
Fresh5Git blobs/4Python AST checks pass; see dated mmx-camera-calibration session.
Prior29runtime/tool tests remain historical, not rerun for this source review.

## Current checkpoint — layout fixed; printable calibration tool ready, 2026-11-02

Owner said proceed and selected printable target/tool. Layout fix6fea7ecf
aligns actual Q8B NV12 with current modeld: stride1280,Yrows736,UVrows368,
UVoffset942080,allocation2220032,modelcopy1413120.140real frame pairs still
pass~20Hzpublish/~59.63Hzsource with settings restored. CPU-only pinned warp
matches two synthetic independent NumPy views; current ONNX expects
uint8[2,6,128,256] and carries its own image/desire/feature queues. Not model
inference or Adreno qualification. Q8B720pwarp build config added; runtime kept.

Printable A4 PDF/SVG and calibrate.py target/capture/solve tool now live under
openpilot/system/camerad/webcam. See CALIBRATION.md for exact workflow. GUI
uses Tk/Pillow; tested with synthetic frames only.6calibration tests plus prior
23camera/identity tests pass; PDF verified A4 and rasterized grid detected.
Real lens data remain uncollected: owner must print at100%,check25mm squares/
100mmruler and mount flat before collecting24varied views. Current continuous
autofocus is1; optical/focus consistency needs review before any activation.
The solver preserves hashes/profile, rejects weak/high-error data and writes
candidate_not_installed. No profile is installed, no estimated70°K substituted,
and Q8B camera calibration guard stays active. Driver monitoring/hardware
telemetry stay deferred. Next physical step is print/measure target, then guided
capture/focus review; next runtime work remains current model/backend integration.

## Approved camera patch completed — 2026-11-02

Owner approved AK-Camera720pMJPG60capture/20Hzlatest publication, only road camera,
optional rotation defaultoff, real timestamps, self-contained capture helper
and opt-in driver-camera deferral. Implemented in webcam camera.py/camerad.py,
config.py/native_capture.py/native_capture.c, camerad/SConscript and manager
registry; tests/docs updated. Enable USE_WEBCAM=1 Q8B_ROAD_ONLY=1 only for this
experimental capture path. Normal close restores previous mode/rate and saved
dynamic-framerate control (temporarily0to actually sustain60FPS).

21focused tests pass; real140frame IPC/Cereal check:19.973Hz publish,59.642Hz
source estimate, one stream/correctNV12 layout/timestamp pairs, exit0/settings
restored. Native helper actual SConscript target and pinned msgq bindings build.
Read session for exact scope/provenance. No model/managed UI/vehicle execution;
Q8B geometry remains unconfigured and its guard active. Driver-monitoring
consumers are not bypassed or supplied invented data. Next camera geometry and
current model-input/runtime contract qualification. Hardware settings still
deferred. Older no-camera-change statements below are historical.

## Current scope — camera work, 2026-11-02

Owner explicitly deferred hardware-setting changes and selected cameras.
Explained current webcam files; see [camera path](Knowledge/CAMERA_PATH.md).
Start openpilot/system/camerad/webcam/camera.py (actual OpenCV capture), then
webcam/camerad.py (device selection, NV12/IPC/messages), manager process selection
and common/transformations/camera.py geometry. Existing source requests720p25fps,
rotates180degrees; publisher loop20Hz with synthetic timestamps. Q8B geometry
remains explicitly unconfigured. No source fix/camera launch yet. Next: recover
teacher's actual camera/capture evidence and compare it to these contracts
before a bounded implementation. H1 thermal plan remains pending/deferred;
do not automatically resume it from older notes. No vehicle action authorized.

2026-11-02 owner narrowed question to webcam-mode prerequisites and requested
MM-X master/RK3588 evidence. Full hardware checklist is NOT required before
initial webcam demonstration: RK3ad69b20 uses generic PC empty/zero/default
telemetry and service exclusions. Literal masterdb27a433 differs from default
master-ticib9b7f488. See updated MM_X_LINUX_REFERENCE for11blob/9AST source audit.
Previous broad yes referred to full-port needs and was overbroad for this scope.
Camera/model/process compatibility still needs qualification; no application
changes or sensor-health bypass adopted. Hardware plan remains pending; this
research has not implemented or launched camera work.

2026-11-02 clarification: current source73773e3 reports Ubuntu/ARM64,
radxaQ8b and PC=True through the read-only identity command. PC denotes Linux
development policy; USE_WEBCAM separately selects a camera process in the same
repository. No separate webcam fork selected and no managed Q8B stack qualified.
Earlier standalone q8b/gpu_webcam remains a reference/demo. H1 hardware work
still next; cameras deferred. No runtime/config change from this explanation.

## Shutdown checkpoint — 2026-11-01; resume 2026-11-02

Owner requested end-of-work audit, then close VS Code and power off. Tomorrow
resume H1 in [hardware checklist](../tasks/todo.md): qualified read-only Q8B
temperature reporting first. No hardware implementation today. Cameras stay
deferred. Read teacher resume/inbox and inspect live Git before continuing.

Audit baseline29630251976104c71dd72f18de53f64adcc70864, clean radxa/q8b.
All application changes since identity12e44fee remain absent: later commits
document project layout, evidence and plans. Fresh11identity tests and notebook
checks pass; no full build, managed stack or hardware-driver test claimed.
Upstream reference a86979d2 and maintenance60f799a are clean. No missing
validation/pending upstream reviews; two corrected historical failures retained.
Daily reference timer remains active/persistent; next Nov2 15:30UTC. Check its
actual state after boot. Last service result success; project is never auto-merged.

VS Code autoSave setting was afterDelay and its Backups directory contained no
files at audit. Normal system shutdown uses VS Code's registered cleanup delay
inhibitor. Power-off is requested only after saved checkpoint/commit/validation;
check the teacher shutdown evidence for the accepted schedule. Saving this
handoff does not prove the later physical power-off completed.

Saved 2026-11-01. Read this after reopening, then check actual files and Git.
This is the current handoff; older session paths and next-task advice may be
historical. Update it after each completed increment and before task closeout.

## Accepted scope and defaults

The owner wants Sunnypilot on Radxa Dragon Q8B/Ubuntu ARM64, eventually lateral
control with a custom steering actuator. This sunnypilot directory is the actual
project. Keep active code, assets and tracked student knowledge inside it.
Teacher memory is the optional Comma workspace Ai; other folders are references
or development support. Both memories must record completed work and next steps.
Use relevant Agent Skills and REA as the default evidence workflow: readable
source first, REA for artifact/runtime analysis where applicable. Record actual
use; documentation changes do not imply binary or runtime verification.

## Completed checkpoint

- Board identity implementation:12e44feeff241334e184c86dc9daccdc7f9e4fa1.
  Exact Linux/aarch64 device-tree token detection, Python/C++ HardwareRadxa,
  append-only radxaQ8b enum8 and checked unconfigured-camera lookups.
- Linux ARM64 profile retained; COMMA_HARDWARE=False and PC=True service/path
  policy. Power/thermal/sensor hardware operations still use generic defaults.
- Canonical project migration:7c208a33747d4ce279131649f2ca3434ad3b3fc3.
  Ai is a real tracked directory without nested Git. Branch is radxa/q8b.
- Most recent project HEAD observed before this shutdown audit:
  29630251976104c71dd72f18de53f64adcc70864, clean. The commit containing this
  handoff is a later documentation checkpoint; get latest HEAD from Git.
- Source headers:Sunny2026.003.000/COMMA0.11.3. Upstream base6f7a2c94;
  separately updated reference was a86979d2. No newer upstream merge applied.
- Fresh stock model65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce;
  preserved old Q8B model/runtime remain separate references, not overrides.

## What was actually verified

Prior identity/relocation checks:11 Python tests,4 native C++ to Python message
checks, SCons profile probe (not full build), lint/syntax/diff,31 updater tests,
notebook layout/index and standalone notebook-copy check. Evidence is recorded
in [VALIDATION.md](VALIDATION.md), [README](../readme_wat_we_did.md) and dated
sessions. Those results are tied to their source, not automatically to future
code. This workflow task verifies documentation links/layout only.

## Where we stopped and next technical step

Owner asked what to do with the collected evidence. Saved proposed ordered
[hardware plan](../tasks/plan.md) and [checklist](../tasks/todo.md): H1 read-only
temperatures first, then power, physical IMU, cooling and remaining services.
No immediate purchase/rewiring for H1; qualify fixed IMU mounting before final
axis/bias calibration. Plan only, all implementation tasks remain pending.

Owner now selected **non-camera hardware/sensors** and deferred cameras. A complete
input/output/status checklist is now included in the non-camera hardware map,
covering board, UI/audio/network, timing, bridge and vehicle-dependent inputs. We
completed a read-only map of motion-sensor messages and board-health APIs plus
this host's exposed devices. See [non-camera hardware](Knowledge/NONCAMERA_HARDWARE.md).
This source/inventory checkpoint started at5bcc0028, clean; no application or
hardware configuration changed. Exact Git HEAD must be checked on reopening.

Findings:55 readable thermal zones, system_power/USB/ADC hwmon telemetry and a
radxa_svc_glink PWM interface. Two IIO devices exposed no accel/gyro/magnetic
channels. No /dev/gnss* node; existing CH341 USB Serial is not identified as
GNSS/IMU. No ports were opened or device/bus configuration written.

Jetson teacher studies read back: DragonPilot has explicit board-health/fan
providers; Feiyang overlay has a physical IMU publisher. See JETSON_HARDWARE_REFERENCE
for pinned evidence/limits. No implementation adopted; Q8B native I²C9 and actual
board telemetry remain our path, camera work deferred.

MM-X hardware review complete at b9b7f488: PC thermal/power/fan defaults and
carState-derived IMU policies are documented in the reference note; no code
adopted. Retain actual Q8B telemetry and physical sensor path. Next bounded
implementation remains read-only thermal mapping with tests.

Known from teacher: Adafruit LSM6DS3TR-C on I²C9/address0x6a, VIN1/GND6/SDA3/
SCL5; prior102Hz polling and1040 in-memory schema round trips at olda5f44653.
No new live bus test here. Model/interface are known; no need to ask again.
Fixed mounting/bias, current-source IPC/provider and locationd acceptance remain
open. First bounded implementation candidate is read-only thermal reporting;
then validate power domains/units and implement those separately. IMU provider
needs verified installed axes, acquisition timestamps and live sample/fault tests.
Use existing teacher IMU reports first; raw I²C need not expose IIO channels.
Stock comma sensord remains disabled under PC=True; do not turn on its hardcoded
I²C/GPIO wiring. No runtime/hardware driver was implemented by this explanation.

Camera/model-contract work remains future work, deferred by this scope. Real
thermal/power/fan, IMU/GNSS, full managed runtime and steering remain unqualified.
No firmware/CAN/vehicle actuation is authorized. Discuss upstream integration
before changing this branch; daily updates only advance the reference copy.

## Startup and interrupted-session recovery

1. Read project AGENTS, this handoff, STATE/TASKS and the relevant topic/session.
   In the workspace also read teacher Ai/RESUME_HERE, ROUTER and update inbox.
2. Run `git branch --show-current`, `git log -5 --oneline` and
   `git status --short --ignore-submodules=none` from the project root.
3. Compare dirty files and latest commits/tests with the saved checkpoint.
   Preserve unexpected edits; never clean/reset/stash them automatically.
   Missing validation is an unknown, not a passing test.
4. Resume the owner's current accepted task, or explain the saved next step.
   Saved notes survive normal shutdown; unwritten chat/edits cannot be recovered
   from them after an abrupt interruption.

At every completed increment/closeout update this handoff, relevant topics,
WORKLOG/session, and teacher resume/current-state notes; commit verified scoped
project changes and attach actual validation through the workspace ledger.

Latest workflow verification:27 notebook docs/61 relative links, workspace
source index and a copied standalone notebook check passed. No application
source changed or runtime service started. No actual reboot was performed.

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

2026-11-03 informational folder explanation saved in Knowledge/ARCHITECTURE.md and Sessions/2026-11-03-root-folders.md; no runtime/folder changes. BeamNG optical/CAN next step remains unchanged.
