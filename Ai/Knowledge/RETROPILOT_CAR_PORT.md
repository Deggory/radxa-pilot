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
