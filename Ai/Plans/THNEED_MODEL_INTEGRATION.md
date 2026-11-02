# Q8B Thneed modeld integration — 2026-11-02

Owner authorized proceeding after the existing converted CD210 import31aa29b.
Keep artifacteb741641 unchanged; no model conversion. Work only in sunnypilot.

1. Add opt-in Q8B_THNEED=1, requiring real Q8B/road-only webcam mode. Select
   a ModelState-compatible backend through normal stock modeld. Default off.
2. Prepare padded NV12 into two packed model views using current pinned warp
   semantics. Maintain current image/desire/feature queues, parser and reset.
   Verify synthetic warp against pinned Tinygrad and input histories against
   current-wrapper/CPU references. Keep all helpers/source/model assets local.
3. Launch camera, actual modeld --demo and actual Sunny UI in a private message/
   Params namespace. No vehicle/planner/control/DM/logging stack. Use temporary
   MM-X geometry with zero mount assumption, while calibration remains invalid.
4. Verify live predictions/modelV2 timestamps, finite paths, source IDs and
   steady cadence/latency with recorded raw data. Verify bounded stop, device
   restoration and absence of owned processes. Inspect actual UI screenshot.

Use incremental/TDD/interface/source/review skills with source-first/REA routing.
No clock/fan/driver changes, camera optimisation or automatic upstream merge.
Report actual failures/limits; previous11.72ms and20minute results are historical.
Update teacher/student notebook and commit verified increments with evidence.

Completed all four bench steps:51tests/lint,5exactCPU warps,32recurrent same-input
CPU checks,6liveCPU snapshots, clean65s19.998Hz model receipts and33point actual
UI overlay. All children exit0/settings restored. Full root build is blocked by
missingacados; measured geometry, hard deadlines, road/vehicle and thermal soak
remain unqualified. [Closeout](../Sessions/2026-11-02-thneed-modeld.md).
