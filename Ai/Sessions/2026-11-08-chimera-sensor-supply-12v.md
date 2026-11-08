## November 8 — Sensor supply 12 V; four requested readings complete (QA63)

Owner reports separate sensor supply + to − = 12 V. Together with confirmed
Chimera labelled 5V = 5.05 V, CAN2 H = 3.3 V and L = 1.8 V (to Chimera GND),
this fulfils manual G3’s four-reading collection requirement. These are owner
measurements, not USB telemetry or proof of sensor-rated supply/actual chip
VCC/STB/RXD. Latest CAN capture remains QA61: zero payload bytes on all buses;
no new runtime test or device action. Sensor stays on printed CAN2; separate
supply/common ground retained. Asked visual-only CAN2_TERM jumper position,
leaving wiring and power unchanged. CAN receive fault remains unresolved.
Evidence: Reports/chimera-can-levels-recheck-20261108/PHYSICAL_READINGS_COMPLETE.json.
Existing G1/G2/G4 evidence is historical, not rerun here. No flash/config/save/
reset/rate/wiring/product/upstream change; last requested CAN2 500 kbit/s remains.

Baseline radxa/q8b 22d11b2f872775e337e9f185f5fde7ff4618f128, initially clean.
Debugging, documentation and Git skills applied; reused source/REA evidence, no unrelated binary analysis.
Documentation validation only: Q&A/JSON synchronization, evidence preservation, diff check.
Upstream inbox remains November 4 stale under explicit hold; no related pending commits listed, no update performed.
