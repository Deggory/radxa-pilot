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
