## November7 — Status metadata/read-length explanation saved

QA-20261107-01 explains the six unsupported legacy status fields and why a
missing value must not become measured zero/false. Status sizes depend on the
qualified profile: currenthealth49, legacyF4v17health59, controllerhealth64bytes;
short/overlong replies reject. Source verified atdfd316d65, no implementation or
hardware/test rerun/update/push. Documentation only. Next remains T08b2d passive
normal-status publication and disconnect/reconnect; legacy stays observation-only.

[Owner answer](../QUESTIONS.md).

Scope: plain-language explanation of existing code only. Teacher/student
routers/handoff/Q&A/inbox and live cleanradxa/q8b/source read before answering.
Relevant documentation/Git workflow reused; source-first evidence, no REA binary
question or delegated review. Existing test receipts remain tied to their source;
no new native/Python application/hardware tests were required or claimed. Notebook
layout/links, Q&A synchronization and whitespace checked before local commit.
No application/firmware/DBC/model/camera/runtime edits, no physical board access,
source update or push. Source baseline dfd316d6554bbd39e221759c5637e648b8cd2cc3;
Panda8a16e089/opendbc150f9371 unchanged. Pending engineering, physical limits and
statsd teardown finding remain as saved in the November6audit. Upstream checks
remain held under November4policy; no pending related commits in the savedinbox.
Next T08b2d remains explicitly pending; this explanation does not resume coding.

November7 follow-up QA-20261107-02: owner asks about complete replacement and
bidirectional data. Confirm intended Panda-style USB/CAN role forRadxa: CAN→
Chimera→USB→Sunnypilot and reverse through MCU TX policy. Current implementation
remains passive/offline; bootstrap/controller binding and guarded TX/bench work
pending. Three classical CAN buses, truthful declared capabilities; no blanket
H7 feature/physical readiness promise. Existing board inputs/CoreConfig/relay/
OBD-C requirements retained. Next remains T08b2d passive status/reconnect.
Explanation only, source6f788e922; no application/hardware/test rerun/update/push.
