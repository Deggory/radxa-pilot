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
