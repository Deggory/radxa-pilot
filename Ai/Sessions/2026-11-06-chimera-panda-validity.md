## November 6 — Panda ignition validity prerequisite implemented

QA29/T08b2a: hardwared now passes SubMaster Event.valid into a pure reducer for
every updated pandaStates event. Invalid/empty updates revoke ignition immediately;
retain last valid primary harness for battery shutdown. Non-unknown predicate,
primary/secondary semantics and no-update age>5s grace remain.12new tests,
37focused plus28power/fan tests (65total), Ruff/compile and mutation checks pass.
Seven selected actual source-branch cases reproduce both baseline bugs/preserve
grace with fake clocks; no live thread/IPC/hardware run. USB still emits no
pandaStates; mapping/admission/reconnect remain. Firmware23hashes/7448-byte image,
Ocelot39dirty entries/19hashes, archive/DBC and prior host code preserved. Updates
held; no push. Next T08b2b source-backed fault/enum/supported-field mapping and
an offline PandaState converter before ordinary publication.

Accepted scope: one prerequisite slice, T08b2a. Read teacher/student routers,
resume/handoff/current task/Q&A/inbox and local source; startup clean radxa/q8b
bc99ae0d917a99b925840c31a11c3cb34ed5f7e0 with prior validation pass. Inbox no related
pending commits, checks held per November4; no fetch/updater check. Relevant
incremental/TDD/API/review/Git/docs skills; source-first path, no unrelated REA
provider or invented model/runtime evidence, no delegation.

Changed runtime sources: hardwared.py plus pure hardware/panda_state.py; new
hardware/tests/test_panda_state.py. Every updated event is reduced using actual
validity, including empty lists. Invalid/empty clears ignition, leaves last valid
harness shutdown context. Unknown primary cannot establish harness; later valid
primary disconnect can clear history. Either ignition input/secondary ignition
and primary harness semantics retained. No-update grace/logging unchanged.

TDD RED missing helper module, GREEN12new tests. Final focused37tests pass with
warnings-as-errors, plus28existing power/fan regressions pass (65total). Ruff and
Python compile pass. Mutant temporary helper omits validity check, fails3tests;
project source never mutated. Seven cases execute selected actual baseline/current
AST branch with fake SubMaster fields/clock; reproduce invalid acceptance and
empty-update retention, confirm before/at/after strict5s threshold. No live
hardware_thread/IPC or physical provider actions. Initial twice-serialized Capnp
fixture warning fixed by independent sample builders, without suppression.

Current native/firmware sources unchanged; source hashes and retained7448-byte
image match prior evidence. Ocelot39dirty entries/19hashes/archive/DBC preserved.
No fresh native/sanitizer/firmware suite required; prior results not claimed new.
New firmware parked. Host USB entry still only CAN/customReservedRawData1, no
pandaStates/control/TX/admission/schema/pin change. No camera/model/Thneed code,
config/reset/flash/actuation/install/update/push. State that says hardwared ignores
validity is superseded by QA29, while supported-field/other-consumer admission
remains unresolved. Next exact step: T08b2b fault/enum mapping and supported-field
semantics plus an offline tested legacy PandaState conversion, then ordinary
publication qualification/reconnect. No hardware action is inferred.

[Receipt](../Evidence/chimera-panda-validity-20261106.json).
[Contract](../../chimera/docs/PANDA_IGNITION_VALIDITY.md).
