## 2026-11-02 — BeamNG bundle audit complete; runtime adaptation still blocked

Audited collected source at projectbase f72a1ea/upstream5435d674. Added14missing
integration/import references; bundle now96files/1160682bytes, byte-identical
upstream. Allfile Git/SHA/mode/size checks;69Python AST/8bash/2JSON checks pass.
Fixed verifier accepting empty snapshots/wrong origin/pin/checksum list;12new
regressions pass, checksum-guard mutation caught. Snapshot tests with process-
local routing/current Sunny dependencies:164pass/6fail/1skip;2modules blocked
on import,1UI module not run. Five failures and two import blocks stem from
missing opendbc scale_tire_stiffness; onefailure assumes installed xdotool.
Test-only evdev2/mss10.2 installed under /tmp with locked SDist hashes; active
environment unchanged. UI/Lua/JS/Vue/game/model/manager tests not performed.

Source probes reproduce NaN accepted in96byte BPL1 and control-send called after
no new telemetry. Fork steering uses desiredCurvature→position, bypassing final
lateral torque; cannot directly validate custom actuator/NNLC. Same-hostIP,
camera1280vs1928, timing/freshness/session/finite and peripheral4vs2Hz require
adaptation. No copied upstream fixes applied to active runtime/DBC. Verdict:
reference bundle verified, direct runtime integration blocked. Next sim-only
recorded PC frame→VisionIPC/UI, then state/shadow and explicit lateral contract.
Detailed report: openpilot/tools/sim/beamng_reference/AUDIT.md; per-file/test
receipts alongside it. Relevant skills: source-first/code review, TDD/debugging,
git/docs. REA binary analysis not relevant to readable source/packet probes.

Collection validation: all82Git blobs and SHA256 checks pass,56Python AST,
8shell syntax and2JSON parses pass. Ruff passes for our verifier/discovery guard;
notebook66docs/213relative links pass. Using existing isolated pytest9.1.1,
reference-folder collect-only reports no tests collected (expected exit5),
confirming the new foreign snapshot is excluded. Active Sunny venv lacks pytest;
no package installed to change that. No game/model or foreign behavioral test.

## 2026-11-02 — BeamNG source bundle collected

Owner requested all needed BeamNG files from Caleb's tools in a folder. Created
openpilot/tools/sim/beamng_reference/:82byte-identical upstream files,1025072bytes,
from commit5435d67499f66eca58f95882cbe35e9c577e874c. Both complete game mods,
setup/TUI/monitor/diagnostic, car installer/platform, camera/telemetry daemons,
common modules, sim helpers, relevant integration source/tests and root launch/
config/build/dependency metadata retained under upstream/ with original paths.
MIT license, original submodule pins, MANIFEST/SHA256SUMS and dependency guide
included. verify_bundle.py checks file coverage/bytes/SHA256/Git blobs/modes.
56Python AST/8shell syntax/2JSON source checks pass; original behavioral and
Lua/JS/Vue/game tests not run. Foreign snapshot tests excluded from automatic
parent pytest discovery only; existing project tests are unchanged. No installer,
mod, manager, model or game executed; no dependency/environment/DBC changes.
Next remains sim-only recorded PC frames→VisionIPC/UI; bundle is reference,
not a runnable standalone checkout or qualified PC↔Q8B backend.

## 2026-11-02 — Current owner focus: BeamNG bridge discovery

Owner moved from NPU research to running this Sunnypilot with PC BeamNG.drive.
Identified Caleb-J773/beampilot-drive at5435d674 (same as teacherOct28 pin).
Its same-host camera/telemetry/Lua path needs a PC↔Q8B adapter; current local
openpilot/tools/sim implements MetaDrive only. README successor steerpilot
publicURL/API return404. Saved source hashes, concrete API/image-size/freshness
gaps and staged camera→state→shadow→game-lateral plan in
[BeamNG notes](../Knowledge/BEAMNG_BRIDGE.md). Research/docs only; no game, mod,
network listener, managed stack or model launched. CD210GPU stays selected;
failed W8A8 NPU baseline retained, precision experiment deferred. Next: prove a
recorded PC frame through sim-only VisionIPC/UI before a live game connection.

Evidence: normal GitHub plugin read of pinned README, beamngd/beamcamd/Lua,
camera config and launcher; public successor404 independently checked by web.
TeacherOct28 source audit reused where its exact commit still matches. Local
sim interfaces and Q8B model guard inspected; source/hash receipt retained.
No upstream integration. Current research scope does not copy the fork's
manager bypasses, synthetic DM settings or driving-limit changes.
