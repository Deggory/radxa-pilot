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

November7 QA04 main.c explanation:74line minimal bootstrap initializes RAM/IRQ/
internal clock/inactive board state, records boot status and parks. USB driver,
EP0/service and codec are separate offline modules; main calls none of them.
Smallness reflects modularity plus pending operational integration, not completed
USB/CAN firmware. Future main can stay compact as orchestration. Sourceb32b0e9b9,
read-only explanation, no application/hardware/test rerun/update/push. Next remains
hostT08b2d passive normal-status publication/disconnect/reconnect.

November7 QA05: owner requests an option only, explicitly no implementation:
retain C2-era/original Chimera firmware and adapt Sunnypilot USB/CAN/status/
lifecycle to its exact legacy profile. Viable compatibility strategy for passive
integration; original mailbox16/health43 differs from C2CAN5/health50 and currently
managed F4CAN6/health59. Retain exact firmware/input/config behavior and canonical
DBC with explicit adaptation. Existing MCU/relay defects remain; minimum device-
side safety must be qualified before real actuator commands. New bootstrap work
preserved; no route selected/roadmap or code changed. Exact intended C2image is
unresolved for a future choice. Sourcee8cd79f90; no hardware/tests rerun/update/push.

November7 QA06: owner explicitly requests a progress percentage for the complete
new Chimera idea. Rough subjective planning estimate20–25% implemented/75–80%
remaining overT01–T20;2offline tasks complete,5partial,13pending. Unequal tasks/no
agreed effort weights mean no measured completion/time fraction. New implementation
physical qualification0%. Earlier no reliable measured percentage remains true.
No code/roadmap/route change or hardware/test rerun/update/push. Source9a7489f8c;
next still T08b2d. C2-era host-only alternative remains unselected.
