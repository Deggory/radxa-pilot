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

## DBC synchronization follow-up — 2026-11-04

Owner Q&A18 asks whether DBC covers the outgoing data. Fresh canonical and
packaged SHA/count/prefix checks pass:28messages,20old+8new; fresh PC SSH
sha256sum matches RP-SIM-1 b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67.
All emitted telemetry has definitions. Buttons remain defined/unavailable and
wall_time is PC-local by design. Source7f924e81/child150f9371; no runtime/DBC
change or new physical reception test. Documentation skills/source-first route
continue; no binary analysis needed. Next remains electrical CAN qualification.

## Canonical master and opendbc scope clarification — 2026-11-04

Owner Q&A19 explains canonical as our agreed workspace mastercopy, with
synchronized Sunnypilot/PC copies. RP-SIM-1 is a local extension, not a claim
of upstream acceptance. Actual child150f9371 diff shows9latest BeamNG paths:
DBC,decoder,CarState,values/interface,diagnostic-query skip,passive torque-data
placeholder and provenance/docs. These implement passive input support;
no live control activation or measured tune. Parent sourcea644f949/child150f9371.
Source-first/documentation workflow; existing skills apply, no binary analysis
needed. No code/DBC/device modification or runtime test this turn. Next CAN
qualification/manager/return path and existing holds remain unchanged.
