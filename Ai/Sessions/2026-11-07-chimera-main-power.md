# November 7, 2026 — Observed VBUS supervision and percentage checkpoints

Owner request: "proceed after each stage show in % were we reached". Baseline
1dd5a7f63920c8e5a935c0a6fe3ce9a89baedd25, branchradxa/q8b, clean including submodules.
Teacher/student routers, resume/handoff/Q&A, source notes and inbox consulted.
Updates remain held under November4 policy; no remote update/integration/push.

T03c3a implemented: main_poll now takes a trusted bounded VBUS sampler. It checks
fresh PRESENT before and after each successful bounded service poll. Missing/
unknown/invalid/absent observations normalize to UNKNOWN/ABSENT, revoke external
facts and latch USB_POWER while stopping the detached service once. Original
service faults retain their initiating cause and do not trigger a post-failure
sample. Failed release keeps ownership/nested release error; later poll/start
perform no IO or sampling. Explicit stop can retry cleanup; start/stop/exception
reset the local observation. No automatic reconnect or stale PRESENT reuse.
Production main still passes NULL profile and reader, so normal startup remains
USB_HELD/read-only snapshot. No physical detector/pin/threshold/default power
profile or session-valid override is invented. The service still forbids attach.

Changed firmware main.c/main.h/main_runtime.c (3of25inputs),22other inputs
unchanged. Updated existing51case native coordinator fixture to explicitly supply
a synthetic PRESENT sampler. Added16scenario real-component power fixture with
Python sanitizer runner. Added supervision/attached-mode requirements contract,
progress-reporting rule/checkpoints, roadmap/README and both memory layers.
Raw8108/projected8244/globals256/stack4096, unsigned/unflashed; SHA256
b2c62ee6d05d5b6c720633daf4d34c2aecb3ca15166926a10257d54a9a7f7bb3.
Old8032-byte image/report/ELF preserved under ignored build/main-power-20261107.
Original flash/bootstub/config/stack boundaries and capability manifest retained.

Actual tests: new native fixture failed RED before API/types existed. Focused
power/coordinator2tests pass with16+51scenarios under ASan/UBSan. Full33firmware
tests pass warnings-as-errors, real ARM/copy determinism/negative vector/ELF/linker
and existing USB/codec checks. Two temporary mutations removing before/after
power guards both abort assertions(-6). Ruff/notebook/preservation and source
hashes are recorded in sunnypilot/Ai/Evidence/chimera-main-power-20261107.json.
Self-review covered state/error/ownership/lifetime/bounded callback contract,
pre/post ordering, no sampling after failure, no stale reuse and production NULL
profile/reader. No delegated review claimed. Used incremental/TDD/API/Git/review/
documentation/source-first skills; direct source/GNU tools sufficient, no REA
provider or unrelated binary analysis fabricated.

Preserved: Ocelotd87892fa39dirty entries/19hashes, archive224cfa64clean, Panda8a16e089
and opendbc150f9371clean, canonical DBCb4079670, frozen F4v17reference5files/license.
No host/model/camera/Thneed/code/device/flash/settings/input/CAN/relay/OBD-C change.
Original VBUS override does not prove a detector; gateway/pro/OBD-C drawings are
not exact Chimera power schematics. Current power tree/profile and installed
recovery facts remain unqualified. Existing host statsd teardown issue untouched.

Reporting accepted: after each completed Chimera stage give its actual result,
full roadmap rough percent and new-firmware hardware validation. Current stage
100% complete offline; full roadmapabout25% complete/75% remaining; physical0%.
This is subjective planning, not effort/time/readiness. Keep the same denominator
and do not inflate for tests/LOC/tiny commits. Earlier QA06range20–25% is consistent.

Next: establish actual board power/profile/VBUS/installed recovery evidence,
qualify/bind physical reader and implement attached-mode lifecycle separately.
Bulk/CAN/operational health, inputs, Core Config, MCU TX and bench work remain;
hostT08b2d passive normal publication/reconnect is queued behind main-first work.
No live hardware or update/push. Commit verified increment locally; teacher final
checkpoint records resulting SHA, ledger validation, index and clean readback.
