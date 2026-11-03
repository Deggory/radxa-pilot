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

Changed paths: new opendbc car/retropilot package, registry/selection,
CAN checksum handler/test, canonical packaged DBC, torque-data passive bound;
parent docs/RETROPILOT.md/docs README/BeamNG guides, notebook and receipts.
No unrelated source or upstream reference change. All runtime changes in the
actual sunnypilot repository/submodule; only maintenance registration config
changed outside it. Actual parent final SHA is available in Git/teacher closeout.

Initial RED tests reproduced absent DBC/platform/encoder; explicit-selection
RED reproduced diagnostic TX (a first test used an assertion caught by the
query code; corrected to record calls then assert); driver-override RED
reproduced a latched local armed indicator. Fixes pass without changing old
tests or introducing skipped tests/suppressions. Full results and existing
skip counts are preserved; no full route/dataset/manager/vehicle suite claimed.

Source hashes, native compiler and full receipts live in
Ai/Evidence/retropilot-port-20261103.json and retropilot-native-crc-20261103.json.
Logs include codec increment, selection RED and override RED, final CAN/port,
broader interface/fingerprint/docs/vehicle-model/lateral-limit and Ruff checks.
Codec tests52passed before commit eb64a22; finalCAN53includes provenance check.
Initial submodule commit was blocked by absent Git identity; inherited the
parent's existing Codex identity locally, then committed without global edits.
Maintenance configcdc20d4 + installed hook journal both new submodule commits.

Upstream inbox start: a86979d2, no related pending discussions,8historical
failed/blocked records retained. No upstream integration or default runtime
selection. Accepted camera/model path and rejected NPU baseline unchanged.
No remote PC command or SSH trust change in this port task.

Closeout: code649bbb6 and codec eb64a22 committed and validated in the ledger.
Parent includes docs/notebook/submodule pin and receipts; final parent SHA/clean
status is recorded in teacher closeout. Documentation verification passes:
73notebook docs/223links,4guides/30links and96immutable reference files.
No unrelated dirty files were present at startup or added by this task.
Next exact step: inspect actual Chimera receive-only transport and producer
frames with preserved bus IDs, verify speed units and firmware identity, then
implement the owned backend. Do not launch stock Panda flash/recovery on it.

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

2026-11-03 path lookup: shared fingerprints.py is opendbc_repo/opendbc/car/fingerprints.py; Hyundai example is car/hyundai/fingerprints.py. RetroPilot has no fingerprints.py; explicit RETROPILOT_RETROFIT is in car/retropilot/values.py:49. Verified by rg --files and absence check at parent c62cfe2/opendbc649bbb6; no runtime change.

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

Implementation recovery: initially declaring FW_VERSIONS=None registered a
non-iterable database with this pinned get_interface_attr/FW loader; removed
that attribute. No FW_QUERY_CONFIG added. Canonical fingerprint map is empty,
not the old placeholder and not None. Full FW/config consistency suite passes.
Parent changed paths: submodule pin, docs/RETROPILOT.md, existing
openpilot/sunnypilot/system/tests/test_params_migration.py, notebook and receipt.
Project code remained isolated from upstream reference and Ocelot firmware.
