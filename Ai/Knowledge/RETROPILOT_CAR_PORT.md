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

## 2026-11-03 — 2025 commit guide

[Plain-English commit guide](../Reports/retropilot-c2-history-20261103/2025_COMMITS.md) covers all53dated2025commits in the
reviewed four-repository comparisons: application28, opendbc20, Panda2,
Cereal3; February6–August14.30older inherited/other-author commits remain
separate. All20individual2025opendbc patches retained and SHAs checked.
C2 branch freshly rechecked at b9a942efd3cb210127bb5efb5cf9ccf6a811c728.
This is history evidence, not proof of completed safety or our live control.

## 2026-11-03 — C2 history-led adaptation on existing Radxa Q8B

Owner explicitly requested all C2 integration work beyond the car folder and
REA plus Agent Skills. Clarification answered: existing Radxa Q8B, not physical
comma4. Protected project remains radxa/q8b, parentbase35d46c1e179d0f6a541e32e5669ee0c879b408b1.
Fresh GitHub upstream master remainsa86979d2; no merge/update to protected code.

Recovered complete pinned parent delta:35commits beyond2022base
 da2ea41241f16c4b0e80a52fdc40ed57becd185b to C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728;
28dated May15–August14,2025 and7older upstream.50final paths/64historically
touched paths. Nested Panda2commits/2paths at9e6d47f, Cereal3/6 at a7193d0,
opendbc43/10 at6b90fafe includes2021/2022/2025 ancestry. All35parent commit
patches fetched through GitHub.82path dispositions verified, with transient
paths and inherited upstream attribution separate from actual retrofit work.
This is path coverage/relevant patch review, not a claim of line-by-line
review or live testing of unrelated kernels/binaries. Immutable retropilot
reference folder not restored or edited. Full report, timeline, source JSON,
coverage verifier and REA Evidence are in Ai/Reports/retropilot-c2-history-20261103/.

Implemented parent openpilot/selfdrive/pandad/chimera{,_protocol}.py and2test
modules: normal-mode serial/product/version pins, mailbox16/health43 decoding,
exact classical CAN DLC/bus/reserved-bit checks, returned/RTR filtering, raw
health, timeout transferred-byte preservation, clean release/close and optional
modern Cereal CAN publication. Default is bounded JSONL monitor. No Panda
import, flash/recovery, kernel auto-detach, vendor-OUT, CAN TX, heartbeat,
relay/bitrate/config mutation, sendcan subscription or fake pandaStates.
Not an automatic manager replacement. No real USB handle or publisher opened
in this task; CLI tests use fake USB/publisher and real Cereal/state/controller.

Corrected actual producer mismatch in opendbc86a839dcec8ed9a3e45315eac804fa1001f1b2d6,
from9da9210: reviewed Chimera TIM3 and ZSSv0.2.0 use angle STATE1=enabled;
prior receiver STATE0 assumption was wrong. Other module STATE0 fault meanings
stay separate. New STATE1 regression failed then passes; canonical DBC bytes
SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce unchanged.
No active profile selected; wheelSpeedFactor0, noOutput/dashcamOnly, unknown
gear/carNotReady, zero live output and CD210/OpenCL/Thneed eb741641 retained.

REA selected retained Chimera ARM ELF SHA5ae9b4f6ea99e569028d271c4ec9c2ce59cd11375b5482adbd0781f3480e20b8.
GNU symbol Evidence ev_ac17a8b5cec16bed89cad2a8ccf9d13d887340650716039ff3890278cb28be78
and assembly ev_6c720630735de45e83f641b76daea07ba4d1813541724750f8670e1cf723a934
complete/no truncation/no artifact change. get_health_pkt0x080077b0 returns43
and stores raw17; usb_cb_ep1_in0x080079b8 uses16byte stride/4record cap;
can_send0x08006e60 visible body queues via can_push/process_can without a
safety hook, corroborated by source. Not whole-firmware safety proof or an
installed-device pin. Native providers unavailable; pwntools layout Linuxx64
only. Those failures retained. GNU provider version/formats remain unknown.
No firmware execution/build/flash or external engine installation performed.

Read-only sysfs currently finds bbaa:ddcc product Interceptor DAC Bench,
serial440048001251333133333633, bus3/device8. It differs from historical Chimera
serial3a0044001651333038373636. No handle opened/CAN consumed and paused
Interceptor project not resumed. New rejection test protects shared-VID/PID
identity. Preserve this descriptor observation/date, not an installed-image
claim; actual Chimera remains unavailable for live acceptance this session.

Migration map explicitly preserves modern selfdrived health/model/GPS/safety
checks and manager predicates; C2 suppression/joystick enabled-state toggle/UI
restart shortcut not copied. C2 custom relay buttons, PID hot reload/physical
gains and safety enum26 are not qualified modern runtime features. Offline
controller/relay capability remains distinct from missing live qualification.
NEOS/legacy build fixes and inherited2022Thneed work do not replace current
Linux, UV, model or camera integration. No owner settings/PC/game changes.

Validation:15USB/adapter +45RetroPilot +53CAN +303broader car tests pass
(314existing subtest skips), history82path verification and Ruff pass. Tests
cover literal layout/historical health, fake USB allowlist/disconnect/cleanup,
real Cereal -> CarState -> controller candidates and actual zero output. No
real IPC publisher/manager/game/CAN/device timing or physical/MCU safety test.
Receipt/logs: Ai/Evidence/retropilot-history-adaptation-20261103.json; angle
receipt and sysfs identity receipt alongside it. All code/tests/evidence are
in the project; child/parent commits local/unpushed. Maintenance validation
must attach to actual increment commits. Both notebooks updated.

Skills: source-driven-development, planning/task breakdown, interface design,
incremental/TDD, Git, code review and REA skill with source-first routing.
Existing teacher modern-port plan/owner implementation request supplied scope;
no unrelated skill approval gate, hardware activation or deployment performed.
Inbox0related pending/8historical failed-or-blocked validations retained.

Exact next step: identify the actual Chimera normal-mode device, pin its
installed version/signature and collect receive-only bus/health data with this
adapter. Then qualify units/profile/source ages and missing gear/wheel/motion/
driver-input contract; integrate truthful board health/ignition and exclusive
manager lifecycle/reconnect. Shadow/game-only loop and measured actuation/MCU
safety remain separate. Do not promote raw safety17, C2 constants or source/
offline results to modern safety enforcement or tested integrated driving.

## 2026-11-03 — C2 controller migrated to modern offline replay

Owner requested implementation after comparing the small modern controller
with the linked C2 directory. Accepted increment: migrate portable control
calculation and provide parser-to-controller offline replay; preserve the
independent zero-live-output boundary until Chimera safety/profile qualification.
The previous11-line controller was a passive placeholder, not a completed
active migration. No physical/game actuation is qualified by this increment.

Fetched linked GitHub directory and c2 branch through the connected GitHub
plugin. Branch resolves to b9a942efd3cb210127bb5efb5cf9ccf6a811c728; all8retained
file Git blobs match. Read every C2 file and current interfaces/schema/parser.
Immutable teacher retropilot source and canonical DBC bytes were not edited.

Implemented modern normalized torque to two-channel steering, bounded speed
taper, asymmetric slew and zero-before-direction-change; separate lat/long
activation, gas/brake scaling and mutual exclusion;100Hz steering/brake and50Hz
gas/relay with immediate disable flush, per-message counters/CRC/hostbus2.
Preview reports held gas between sends. Nonfinite inputs, overrides, faults,
missing selected endpoints, ignition loss, non-monotonic steps/gaps over50ms
and stale accepted state disable candidates.100ms offline age uses the oldest
accepted tracked CAN arrival, not parser update time; empty/bad-CRC/unrelated
traffic cannot refresh it. Arrival age is not source acquisition age.

profiles.py validates immutable explicit calibration; default profile absent.
C2_REFERENCE is deliberately offline/unqualified (1510center,350counts, author
pedal slopes,7mm brake, implicit1m/s²-to-full-pedal slope).350counts yields700
channel difference versus local Core400check. No calibrated measured-torque
feedback limiter or driver-pedal authority is claimed. SSC/motor steering has
codecs but no selected normalized mapping. Zero live tunes/placeholder geometry,
unknown gear and no fake cruise engagement remain. C2 radar forcibly disabled;
no unused Toyota radar parser copied. docs/RETROPILOT.md maps all8C2files.

replay.py consumes timestamped canonical CAN hex and modern CarControl JSONL,
records candidate frames/actuators, actual zero feedback and empty transmitted
CAN. No USB/CAN device is opened. update() never forwards candidates, even with
mutated dashcamOnly. No allOutput, firmware flash, manager/game/model launch,
persistent owner setting, remote PC action or upstream integration performed.

Source: parentbase796059f3457315877ba8d42890d29d0a76ea131b; modern opendbc
baseaa9bff6f5442cef8cb8e25e143ef38865c276ce8, prior04a78352a9605a0e07342146fe8481b7d92ee7fd,
new9da9210adfa4dc213424f36945caccd40182c80d on radxa/retropilot. Canonical
DBC6b90fafe/SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce;
CD210/OpenCL/Thneed eb741641 unchanged. Historical Chimera de193215 observation
is not a current installed-image pin. Child/parent increments remain unpushed.

Validation:44RetroPilot tests,53CAN tests and303broader car tests pass
(314existing subtest skips), Ruff/whitespace pass. RED missing profile import
and expanded controller failures reproduced before implementation. Integration
tests exercise real CANParser -> CarState -> modern apply -> candidate CAN,
including bad CRC/staleness and unconditional zero actual output. CLI help and
notebook verification pass; no real-time/game/physical/MCU-safety test.
Receipt/logs: sunnypilot/Ai/Evidence/retropilot-controller-20261103.json.

Skills used: source-driven-development, interface design, TDD, incremental
implementation, Git and code-review-and-quality, with source-first routing.
Readable-source and offline execution evidence; no REA binary question/result.
Inbox: upstreama86979d2 unchanged,0related pending,8historical failed/blocked
records retained. No new owner question required for this code increment.

Next: implement the receive-only Chimera backend against its actual installed
USB/health format; qualify producer units, selected game/actuator/driver-input
profile and canonical telemetry gaps. Then shadow/game-only loop and enforced
MCU safety/limits before any live physical output. Do not promote C2 constants
or an offline preview to a tested Sunnypilot/Chimera integration.

# RetroPilot car platform — current implementation

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

Guide: [RetroPilot](../../docs/RETROPILOT.md).
Code: [package](../../opendbc_repo/opendbc/car/retropilot/README.md).
Validation: [receipt](../Evidence/retropilot-port-20261103.json),
[native CRC](../Evidence/retropilot-native-crc-20261103.json).

Accepted scope: modern car platform and offline canonical codecs, using the
teacher C2 migration plan. Chimera remains the intended Panda-role device;
its backend, installed firmware safety and board health are not supplied or
fabricated by a car package. Normal CAN parser validity/timeouts retained.

Sources: C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728, canonical
RetroPilot/opendbc6b90fafe59e81822bfae58e4ecb080248e9de40d,
DBC SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
Packaged DBC bytes unchanged; checksum test enforces this pin. Current target
opendbc baseaa9bff6f5442cef8cb8e25e143ef38865c276ce8. Panda8a16e089 unchanged;
CD210/OpenCL GPU eb741641 retained, no new model/camera test. Historical
Chimera de193215/43-byte health observation stays historical; no USB opened.

Teacher source recovered a new implementation-critical discrepancy: saved
ocelot/firmware/chimera/main.c Hall speed computes kph*100, while C2 CarState
uses raw kph. SPEED.MODE uses a different config index in that source; it does
not establish a reliable units selector. CP.wheelSpeedFactor defaults0, and only
explicit1.0/0.01 scales qualify an isolated replay after producer confirmation.
Canonical unsigned steering-rate magnitude stays raw rather than pretending
it is signed rate. Gear/wheels/cruise-enabled/set-speed remain unavailable.
Actual Interceptor differential torque calibration and SSC status semantics
remain unknown. Optional module flags require exact bus/ID/DLC, are per-instance
observations, and never grant active capabilities.

The minimum platform geometry2.7m/ratio13 and 1m/s² bound are explicitly
non-driving computational placeholders; no actual vehicle has been tuned.
No active requests are encoded by CarController even if caller flags mutate.
Offline commands require endpoint targets, bus and counter; bit limits are not
physical actuator limits. Invalid/nonfinite values cannot silently wrap.

Changed owning subsystems: opendbc/can/dbc.py and new test_ocelot.py,
car/{values.py,car_helpers.py,torque_data/override.toml,retropilot/},
dbc/ocelot_controls.dbc. Parent pins submodule; guide/BeamNG guides/notebooks
and validation logs are tracked. Local commits are not pushed. Maintenance
configcdc20d4 registers the submodule and retains journaling/validation.

Workflow: source-driven-development, interface design, TDD, incremental
implementation, security, Git, documentation and self-review. Existing
teacher PORTING_PLAN used; no need for a second approval to execute owner's
explicit port instruction. REA binary analysis was not needed for this
readable-source migration. The native CRC crosscheck is an offline reference
execution, not REA/firmware or hardware verification.

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

2026-11-03 six-folder clarification: history report now maps cereal/opendbc/
panda/selfdrive/third_party/tools. Old third_party is compiler/libyuv work;
tools is joystick control. boardd edits are build fixes, not Chimera transport
validation. Runtime status/next action unchanged; see dated history session.
