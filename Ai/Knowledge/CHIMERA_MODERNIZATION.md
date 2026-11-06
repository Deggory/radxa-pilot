## November 6 — CarrotPilot F413 and native USB source fetched

QA-20261106-01: interpreted owner spelling as ajouatom/openpilot:carrot-wip.
31selected files pinned69a2d3be; olderF413Panda build and nativeUSB/SPI retained.
CAN6/XOR matches current encoder189classical frames; health59/numeric17,4,5
instead of current49/hash versions. NativeUSB3801filter excludesbbaaChimera.
Snapshot/report under chimera/reference/carrot-wip-20261106 and student Reports.
4158splitchecks/378corruptions/native layouts pass; no hardware/firmware action.
Concrete T03/T06source candidate,not a drop-in port. Next existingT01/T02contracts;
input/relay/bus roles unchanged,updates paused,no push. Prior shutdown is historical.

[Self-contained Carrot Panda report](../Reports/carrot-wip-panda-20261106/README.md) contains source URLs and validation; no runtime change.

## November 5 — Audit published; ordered shutdown closeout

Owner requested audit,GitHub update,then PC and Radxa shutdown. Fresh21software
checks plus189/336codec vectors and94source entries/93copies pass. Published
audit967082679 on public Deggory/radxa-pilot:radxa/q8b; private Deggory/chimera
306c0c8/defaultplanning/modern-usb verified. Master932ff06d/defaultmaster and
support150f9371 preserved. Final notebook commit follows; actual final remote SHA
and normal PC-first/Radxa-last requests/readbacks are in teacher shutdown receipt.
No force discard/kill; physical poweroff not inferred. Runtime/firmware unchanged,
Ocelot dirty work preserved,upstream updates paused. QA-20261105-14.
Next restart: review chimera/tasks/plan.md,then T01/T02board-memory/recovery,
identity/RPC/bus-source contracts. Modernization remains proposed,not installed.

# Chimera modernization roadmap — 2026-11-05

Owner wants the F413 board connected by USB to our Radxa Sunnypilot, preserving
bus0 Cores,bus1 ADAS,bus2 vehicle; IGN/VSS/CPS/BRAKE/ADC1/2; onboard power relay;
and usable RetroPilot Core Config. Research/roadmap precedes firmware changes.
QA-20261105-13 records the actual answer and limits. In the Comma workspace the
board folder is [chimera](/home/radxa/comma/chimera/README.md), with
[roadmap](/home/radxa/comma/chimera/tasks/plan.md) and
[research](/home/radxa/comma/chimera/docs/RESEARCH.md). Those links are workspace
references; this summary and prior deep review remain available in a standalone
Sunnypilot clone.

Native pandad currently usesSPIonly; plan both native USB/lifecycle and F413
six-byte/XOR classical-CAN firmware,exact health/version/capability handling.
RejectFD; distinguish Chimera identity and prevent H7update/DFUsweeps. Board
app0x08004000and config0x08020000require explicit size/partition/recovery gates.
Core Config's16-byte USB codec must change; retain distinct board-settings and
typed-CoreCAN workflows,exclusive offroad ownership and transactional persistence.

Preserve physical buses; generated reports0x50/75/76/100are on0,currentphysical
parser2is not automatically fed. Define sources/local delivery and invalidation.
Safety hooks must guard host/generated/forwarded/maintenance TX. Existing mode39
production has no active profile. Input-endian/RPM/schema/freshness defects need
specific tests; preserve raw acquisition rather than inheriting those defects.

Onboard PB0relay follows ignition in local code with request gating commented.
Wiki establishes3CAN0 12VRoutputs only,not all actuator feeds. Latestownerrequest
includes preserving/qualifying this circuit; earlier blanket relay exclusions
are superseded only to that extent. OBD-C is a separate comma CAN/power/sideband
accessory connector,not Radxa's ordinaryUSBport. PA2request/PB1ignition code exists;
Chimera electrical pinout remains unknown. Keep accessory features disabled until
qualified and unable to override MCU safety.

Pins:e888f939researchbaseline/Panda8a16e089/opendbc150f9371/Ocelotd87892fadirty.
94manifest entries/93copied,75priorhashes match. Originalnightly/provenance,board
photo,officialcomma connectorPDF and download limits retained. Selected source
review,prior matchingREAELFreuse; no newREA/deviceproof. Folder/docs implemented;
all20firmware/host tasks pending. No application/firmwarechange,device/config/TX/
relayaction,push or upstreamupdate. Currentfreshvalidation is document/artifact
integrity; historical189/336vectors+21tests are not rerun. Next owner review then
T01/T02partitions,recovery,identity/RPCandbus-source contracts.
