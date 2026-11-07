# November 7, 2026 — Main USB runtime increment

Accepted scope: continue new Chimera firmware/main-first path from6865244e73ef;
implement next software lifecycle slice and keep physical attachment gated.
Teacher/student routers, Q&A, handoff, inbox and actual Git state were consulted.
Upstream updates remain held under November4 policy; no integration/push.

Implemented T03c2: ARM reset now calls main_start and retains main_poll loop.
main_runtime.c composes actual preparation/service routines, validates explicit
profile/callbacks before IO, compares12UID bytes, latches start/poll/identity
failures, revokes external validity and exposes cleanup/ownership. Failed service
release is not automatically retried. Explicit stop can retry release and permits
fresh startup. The production NULL profile remains USB_HELD/read-only snapshot;
no physical USB attach routine exists. Exception quiet/park behavior is retained.
No host/model/camera/Thneed/DBC/CAN/inputs/settings code changed.

Changed paths: chimera/firmware main.c/main.h/new main_runtime.c, build/linker,
ARM/native tests, shared fake backend, current Chimera docs/roadmap/README and
notebook. Build report pins25inputs:20old unchanged, four changed, one added.
Old7592-byte image/ELF/report retained under ignored build/main-runtime-20261107.
Current raw8032/globals252/stack4096; SHA256
 da43eb348399fcb05fe203a50d38aa95a9d69bf031e20695ab5ceb9a179427d7.
No undefined symbols, original flash/config/bootstub/stack boundaries retained.

Tests: initial native and ARM checks failed RED before API existed; shared44case
service fixture passed after backend extraction. Final32firmware tests pass with
warnings as errors, real component ASan/UBSan and51new integration scenarios.
Temporary identity and NULL-profile guard mutations fail (-6 and1). ARM disassembly
confirms reset->start/poll and coordinator->actual service start/poll/stop.
Copied-tree deterministic builds and negative vector/ELF/linker checks pass.
Ruff, notebook and preservation receipts are saved in
sunnypilot/Ai/Evidence/chimera-main-runtime-20261107.json. No assertions/skips/
suppressions added. Self-review covered API/alias/lifetime, bounded calls, no
implicit cleanup retry, UID continuity and production NULL call; no delegated
review is claimed. Used incremental/TDD/API/review/Git/docs/source-first skills;
source and GNU ARM tools were sufficient, no REA provider run or live hardware.

Preserved: Panda8a16e089, opendbc150f9371 clean, Ocelotd87892fa with39dirty entries/
19file hashes, archive224cfa64 clean, canonical DBCb4079670 and frozen F4v17refs.
Existing host statsd teardown issue remains unmodified/unresolved; no host suite
rerun or hardware qualification inferred from firmware tests.

Next exact increment: establish board power/profile/VBUS and installed recovery
facts, specify attachment/cable-loss/fault policy before enabling connection.
Bulk/CAN/operational health, inputs, MCU TX policy and Core Config remain later;
hostT08b2d passive normal publication/reconnect queued. No bootloader/DFU restore,
watchdog handling, device access/flash/config/TX, upstream change or push.
All scoped work is to be committed locally with actual ledger validation;
teacher final checkpoint records resulting SHA and clean-tree readback.
