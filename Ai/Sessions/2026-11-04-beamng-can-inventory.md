# PC outgoing CAN inventory explanation — 2026-11-04

Question: wat all data does pc send through can bus to chimera

Read current encoder,producer and shared contract, following the previously
read documentation/Git skills and source-first route. No new REA/binary
analysis was needed. Detailed answer is owner Q&A17 and existing BeamNG topic.
Source parenta27c269c097c3937fc7877d491877de509e1272a,
child150f937198ceab43c43b39f94b9bdea63fcb633c.

Key distinctions: driver accelerator input; separate driver/applied brake plus
derived pressed bit; game IMU axes and unsigned steering-rate magnitude; gear
index without P/R/N/D mapping; actual optional cruise status without button
presses. All12frame IDs and integrity metadata recorded in the Q&A. Wall time
is only for PC freshness,not CAN; simulation time goes on CAN. Missing optional
values explicitly invalid. 50Hz is a maximum cap. Last117sample serial attempt
still had0Chimera frames; it was not rerun. No behavior/DBC/config/hardware/
model/source/upstream change, CAN TX or control activation this turn.

Next engineering work remains physical CAN qualification and subsequent
managed receive/shadow/return-command integration; existing holds preserved.

Verification: memory checker104docs/335relative links/240optional workspace links passes; git diff --check passes. No runtime tests rerun for this explanation-only increment.
