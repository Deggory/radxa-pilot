# November7,2026 — Ocelot base-power schematic trace

Accepted scope: continue next main-first USB power/recovery stage from clean
4b6098789f86735a626c9e02c727202498cb748b, branchradxa/q8b. Read teacher/student
routers, resume/handoff/Q&A, topic notes and update inbox. Upstream held under
November4 policy; no update/integration/push. Owner wants percentage at each stage.

Our question about PCB/schematic was answered: "see on ovelot foldeer the sch is
same onli i/o is added". Use Ocelot as owner-identified working base; correct the
prior inapplicable-reference assumption and do not ask the same baseline question
again. The initial recovery-file review was read-only; owner steering redirected
this stage to the concrete power drawing. No recovery tool or assets were changed.

Inspected gateway Eagle XML and board pad/contactref data, Pro ASCII schematic
and rendered original attachment PDF, original F4 USB/common GPIO/SConscript.
36checks pass:17gateway net-to-board comparisons; no gateway PA9net/pad42 signal;
VBUS onlyJ1->D1anode; BAS40/MIC5233 identities; ProVBUS onlyUSB1->D3anode, shared5V
and PA9header route;9CAN pin matches; original session override and raw descriptor.
Saved selected nets and hashes in chimera/hardware/ocelot-base-power-20261107.json,
report in chimera/docs/OCELOT_BASE_POWER.md and standard-library replay helper in
Ai/Reports/chimera-power-schematic-20261107. Primary source remains outside the
standalone project; replay needs original Ocelot, saved facts/report do not.

Pro extraction first used pin-body positions and failed to join obvious nets.
Source geometry/renderer established outer endpoint=position+direction*length.
Corrected trace normalizes fractional export offsets to0.1schematic unit and is
crosschecked against original PDF. This is selected-source geometry, not native
EDA/ERC or physical board tracing. Original/extracted drawings' hashes and this
limitation retained. Initial helper lint errors fixed without suppressions;
final Ruff and replay-output equality checks pass. No arbitrary physical detector
pin, current profile or installed recovery fact inferred.

Result: USBVBUS->BAS40->shared5V; external5Vregulator joins same rail;3.3Vdownstream.
No MCU VBUS detector in either base drawing. GatewayPA9unconnected; ProPA9H5pin9.
Original F413 build uses BVALOEN/BVALOVAL session override, not actual detection.
Nine CAN pins match but base extra outputs differ:gatewayPWRONPB12/ProIGN_SIMPA1
versus ChimeraPB0relay. Preserve Chimera's PC2/PC3 analog/relay/OBD-C/direct inputs.
Power descriptor0xc0/0x32 is historical declaration, not measured operating draw.

No firmware/host source changes:25build input hashes and raw8108/globals256 image
b2c62ee6d05d5b6c720633daf4d34c2aecb3ca15166926a10257d54a9a7f7bb3 unchanged.
33firmware tests from4b6098789remain source-pinned, not freshly rerun. Source replay,
Ruff/notebook/preservation checks captured in Ai/Evidence/chimera-base-power-20261107.json.
Preserve Ocelot39dirty entries/19hashes, archive224cfa64clean, Panda8a16e089 and
opendbc150f9371clean, DBCb4079670, frozen F4v17reference. Existing host statsd issue
unchanged. Source-first/GNU/PDF render sufficient; no REA provider result claimed.
Used incremental/source-first/docs/Git/review skills; no product behavior change
or unnecessary new unit tests. No device/flash/config/TX/runtime/update/push.

Stage T01b source audit100%; overall rough roadmapabout25% complete/75% remaining;
new-firmware hardware validation0%. Owner percentage reporting preference retained.
Next: specify/implement explicit opt-in legacy no-VBUS session mode in offline
controller/service tests, separate from sensed mode. Do not fabricate PRESENT or
require a nonexistent physical reader on the unchanged base circuit. Keep actual
main profile/reader NULL and attachment held until later explicit implementation/
bench/recovery qualification. HostT08b2d passive publication/reconnect stays queued.
Commit verified scoped audit locally; teacher final checkpoint records SHA,
validation ledger/index and clean-tree readback. Saved notes are not a transcript.
