# Chimera firmware source map — 2026-11-06

Owner request: “see the firmware folder insdie the ocelot ,chimera  this will give an idea”.
QA-20261106-04 records the answer and correction to QA-20261106-03.

Accepted scope: inspect original firmware and shared board/build dependencies;
retain all three bus roles, direct inputs and relay/OBD-C interfaces. No runtime
change. Source-driven-development, documentation-and-adrs and git-workflow skills
used; readable source was sufficient and no new REA result is claimed.

Completed: source map, 19-file hash receipt and clarified data gaps. Original
94 source entries/93 copies and 39-line Ocelot dirty status match. Logical pin map
and existing legacy F413 build path recovered. Version-only checks: GCC13.2.1,
objcopy2.42, SCons4.5.2. Initial direct SCons invocation missed local PYTHONPATH;
environment-corrected version check passed. No build performed. Source pin:
Ocelot d87892fa plus preserved dirty bytes. Baselines Sunny91f51ff1,
Chimera603ea76a, Panda8a16e089 and opendbc150f9371.

Changed board docs: docs/FIRMWARE_SOURCE_MAP.md, docs/DATA_GAPS.md, STATE.md and
evidence/firmware-source-map-20261106.json. Student adds self-contained
Knowledge/CHIMERA_FIRMWARE_SOURCE_MAP.md, corrects gap/topic notes and updates
Q&A/router/state/handoff/worklog/session. Teacher mirrors correction and handoff.

Limits: source map is not a complete electrical schematic or an installed-nightly
match. Relay currently follows ignition; commented request gating is not runtime
power cutoff. Qualified modern build and host integration remain proposed.
Next: use recovered mapping for T01/T02 partition/recovery/identity/bus-source
contracts and offline board target. Upstream updates remain paused; no push.

Validation and local commits are recorded in the closeout receipt after checks.

## Validation closeout

PASS: all 94 original entries / 93 frozen copies and Ocelot dirty status unchanged;
document whitespace checks pass; student verifier passes 129 documents,
382 relative links and 246 optional workspace links. Board documentation saved
locally in Chimera224cfa6. Student validation receipt:
`Ai/Evidence/chimera-firmware-map-validation-20261106.json`.
No firmware tests were required for this documentation-only change; no modern
build or live compatibility result is claimed. Only notebook/documentation work
is committed; no push. Exact student commit/ledger receipt follows in teacher.
