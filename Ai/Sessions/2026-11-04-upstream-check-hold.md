# GitHub master check and update hold — 2026-11-04

Owner asked whether this master has GitHub updates, explicitly "do not update
yet without asking". Context resolves to sunnypilot/sunnypilot/master from
project origin. Read both notebooks/inbox, actual refs and timer/service state.
Project baselineb4f31519edcf3fa0a9ac9fef5ff49864dd33f8a5 clean on radxa/q8b;
master and origin/master6f7a2c94; reference8cf6ff9a already present at startup.

Used live read-only GitHub plugin fetch_commit(master), compare(a869,master),
compare(6f7,8cf) and fetch_commit(a869). Master resolves8cf6ff9a33c94bdf2fcb02e228a9aef1a7e6dc7f,
created2026-11-04T04:16:52Z, controls: predictive accel boost(#2089). Adds
AccelBoostSP param default1, boost gated/faded by predicted pedal/stop/curvature,
longitudinal planner selection, cruise/sunnylink settings and native Python
tests. Read7changed paths; no running/testing/merging this code here.
Older upstreama86979d2b2b176413a7f3e5cccf8c807596a7def,Nov1UTC, gates steering
arc toggle on MICI in sunnylink. Compare confirms2commits since our upstream
base6f7,1sincea869. Current Radxa code/Thneed/RetroPilot are not updated by this.

Daily job had already refreshed the separate reference at2026-11-04T15:30:04Z,
before this request, under the earlier standing authorization. Proactively
disclosed that timing and the absence of Radxa integration. Interpreted latest
hold conservatively for reference and project. systemctl --user disable --now
q8b-sunnypilot-update.timer removed startup/definition links; daemon-reload and
reset-failed cleared transient stale state. Re-linked only the source timer
unit so it remains available but inactive/unarmed. Final UnitFileStatelinked,
ActiveStateinactive, no timer-startup link or next activation; serviceinactive.
Source unit remains maintenance/systemd/q8b-sunnypilot-update.timer. No force,
service execution, upstream source/config/model/firmware change or user-device
access. Reenable/advance only with explicit owner approval. Read-only checks
continue to be permitted; do not invoke updater.py check while held.

Updated central upstream policy/decision/router/current/repo and student
rules/decision/handoff/state/tasks/worklog/version/session. Fresh evidence is
source comparison, Git-ref/source preservation and timer pause/readback plus
notebook/whitespace checks; no runtime tests or hardware integration. No fetch,
pull, rebase, merge or upstream commit applied. Normal local notebook commit
is documentation only and not an upstream update. Preserve existing noOutput,
missing active profile and Chimera/physical Interceptor holds.

Source-driven/Git/documentation workflow; readable source sufficient, no
unrelated REA artifact/runtime claim. Exact URLs/files/results in student
Evidence/sunnypilot-master-check-20261104.json. Next: report updates, then wait
for explicit approval/scope before preparing any upstream integration.

Notebook check initially failed because saved source-index.json still pinned
the older a869 reference. Refreshed only this metadata snapshot from already-
present8cf tree; no source fetch or change, verifier unchanged. Both states
and the correction are retained in the check receipt.
