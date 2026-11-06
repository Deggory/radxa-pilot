## November6 — PandaState availability and consumers verified

QA32/T08b2c: appended typed statusAvailability metadata; legacy preview remains
invalid and observationOnly with all6missing current fields. Shared all-or-none
batch guard checks validity/profile/required fields; retained consumers check
liveness. hardwared/manager/UI/core/MADS now use it; missing lateral support
cannot look like a measured false. Historical metadata-absent current producers
retain their prior contract, not authentication. Current D2/C2 reads require
exact49/64bytes and bounded healthy ownership. Native build/10native programs,
56focused+68control/power/fan Python tests, two ASan/UBSan suites, native/Python
serialization and7-failure observation mutation pass offline. Existing MADS
fixtures now use real Cereal plus valid/alive metadata; no assertions suppressed.
Pandad SPI removal is committed as0fedef7b0; final binary has no SPI handle or
preview symbol. USB still emits no pandaStates and grants no operational legacy
admission. Hardware/live IPC untested.23firmware hashes/7448-byte image,
Ocelot39dirty entries/19hashes,5reference hashes, archive/DBC and camera/model/
Thneed preserved. Updates held; no push/device/flash/config/TX. Next T08b2d:
passive normal-status publication and disconnect/reconnect policy, keeping
legacy observations nonoperational; operational firmware/bench work remains.

Accepted scope: owner's correction removes SPI from pandad itself and finishes
field-availability/consumer checks before normal publication. No runtime/hardware
work is implied. Baseline0fedef7b04226796ba5785bed24496c1320aaea3 onradxa/q8b.
Actual final source belongs to the local commit containing this session; inspect
Git/ledger on resume, not an inferred self-hash.

Changed paths: openpilot/cereal/log.capnp; pandad metadata helper, current
exact-read helpers, legacy builder/header, isolated JSON publisher, current
fill helper and tests; hardware power reducer, manager, UI, selfdrived and MADS
consumer call sites; MADS steering test fixture; Chimera contracts/roadmap and
both notebooks. Native schema generated outputs are ignored builds. No firmware,
DBC, model/Thneed or camera source changed. Generic current startup stays unwired;
the passive USB monitor still emits can and customReservedRawData1 only.

Tests: 56focused+68regressions (124Python),10native programs, full native target,
USB/current-reader and converter ASan/UBSan with existing unsanitized support
libraries;14new tests detect7failures after temporary removal of observationOnly
guard; native preview read in Python denies forged-valid ignition. Ruff, whitespace,
notebook/source index and preservation readbacks recorded in the receipt. MADS
fixture's initial7errors (missing valid/alive) were corrected with real Cereal
and validity maps; assertions preserved. New exact-read regression first fails
on prior nonnegative-length handling. Selected actual consumer branches are
executed with fake dependencies, not full GUI/daemon or live IPC sessions.

Source pins: Panda8a16e089b88593914823743df29e1c30b7dd3e00,
opendbc150f937198ceab43c43b39f94b9bdea63fcb633c,
Carrot69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7,
Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 (39dirty entries/19hashes),
archive224cfa645134db91103c55d8188d87e7976b0ba4 clean. Firmware23sources and
7448-byte image SHA d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698
preserved/unflashed; canonical DBC SHA
b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67 unchanged.
No source update/fetch or push; updates remain held by November4 policy.

Workflow: installed migration/incremental/TDD/API/review/Git/documentation and
debugging skills plus source-first fast path/GNU symbols. No subagent or REA
provider run claimed. Five-axis self-review checks schema compatibility, exact
boundaries, batch/index integrity, consumer behavior, serialization, bounded IO
and small metadata allocations. No known new blocker. Historic metadata-absent
producer trust and current generic fault27 list limitation remain explicit.

Correction: previous SPI session's broken self-link is fixed here. Its saved
first notebook-check failure was retained; this increment reruns the verifier
rather than treating that log as a pass. QA32 synchronizes this and schema33→34
correction in teacher/student. Previous runtime test receipts are unchanged.

Uncommitted scope at preparation: all second-increment source/tests/docs/notes,
including this receipt; commit together after verification. First increment is
already0fedef7b0. Next T08b2d is explicit passive normal-status publication and
reconnect/failure lifecycle policy with no automatic legacy control admission.
Hardware, current installed identity/recovery and operational Chimera firmware
remain unqualified. No device/flash/reset/config/TX/managed-run/update/push.

[Contract](../../chimera/docs/PANDA_STATE_AVAILABILITY.md).
[Receipt](../Evidence/chimera-availability-20261106.json).

Final build readback initially lacked .venv/bin on PATH and could not find capnpc.
No code change was needed: repeat with project virtualenv PATH succeeds and all
native targets are current. Both outputs are preserved in the receipt. Final
notebook verification passes152documents/555relative links/8indexed reference
repositories. Ruff and whitespace checks pass; QA32 matches both notebooks.
