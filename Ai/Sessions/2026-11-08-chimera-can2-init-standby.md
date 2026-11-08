# 2026-11-08 — CAN2 initialization / standby investigation

Owner “proceed” continued QA58controller/electrical investigation. Started
abe2d2ae1edf0a60b1b71f92bbc294317c997849clean; panda8a16e089/opendbc150f9371.
Teacher/student notes, relevant debugging/Unlazy/REA/docs workflow consulted;
prior matching-image extraction and objdump reused, no new deep provider claim.

Completed software increment: exact identity/signature/flash validated, debug
ring drained before one repeated temporaryCAN2=500kDEcommand;1.370794ms, immediate
empty debug, no new timed-out text later. Raw5.001342342s/2540reads0bytes. Later
normal debug is finite/partially concatenated, not a complete lossless trace.
Flash776bytes unchanged, all76legacy/native/DBC hashes/child pins and preexisting
Ocelot/steering dirty work preserved. USB released; GUI kept disconnected. Last
requested500kretained, no restore/reset/Save/Format/flash/CAN dataTX/wiring change.

Artifact trace pins CAN3clock0x0800520c, board init0x080067cc, inverted standby
PC1/PC13/PA0and modeOUTPUThelper0x08004ebc, CAN mux0x0800501c. APIreview excludes
BTR/ESR/PA0/VCCreadback: B6inputcapturehas configuration effects/selectedPA3..6,
B7VIN1marker, FB/FCunsupported. Source actually includes chimera/can.h; shared
Panda driver and power_saving.h are separate. Fresh NXPRev11source read confirms
STBnormal-low and VCCundervoltage override; not an installed electrical reading.
Saved reference board photo viewed; no current unit/jumper identity inferred.

Physical gate is pending owner current5V/H/L/sensor-supply readings, async asked;
no new numeric measurements yet. Handoff instead of a claim of complete standby
or controller verification. Next triage actual readings; qualified VCC/STB/RXD/
waveform and termination/controller diagnostics if needed. Existing other holds
remain; no upstream update/push. Only teacher/student Ai documentation changed.
See report README/EVIDENCE.json plus central fullraw probe/disassembly evidence.
