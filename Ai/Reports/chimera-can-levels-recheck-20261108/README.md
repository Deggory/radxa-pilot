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

## November 8 — Labelled 5V output confirmed at 5.05 V (QA62)

Owner explicitly assigns the earlier “5.05” reply to Chimera’s labelled 5V
output measured to GND. Current owner readings: labelled 5V = 5.05 V;
CAN2 H = 3.3 V and L = 1.8 V to Chimera GND. Separate sensor supply output
remains unknown; asked one numeric question, measured supply + to −.
This resolves QA61’s supply-point ambiguity, not the missing sensor reading.
The earlier 4.5 V is historical. Labelled output does not establish actual
transceiver VCC/STB/RXD or valid frames. Latest capture remains QA61: zero
USB bytes, with no new capture or device action for this clarification.
G3 remains unmet. Last requested CAN2 500 kbit/s and all existing holds remain.
Evidence: chimera-can-levels-recheck-20261108/SUPPLY_CONFIRMATION_FOLLOWUP.json.

# CAN2 voltage confirmation and passive recheck — 2026-11-08

Owner explicitly confirmed CAN2CANH=3.3V and CANL=1.8V, each to ChimeraGND.
These are owner-reported current readings on the sensor/Chimera arrangement,
separate from the earlier Waveshare-only3.33/1.88V readings and historical
Chimera1..1.15V observations. They are not independent electronic measurements.

Owner also replied “5.05” to a question requesting two supply readings. Which
supply this describes is still unconfirmed; asked one multiple-choice question
(Chimera labelled5V, separate sensor supply, or both separately measured).
Do not assign5.05Vto either/both supplies without that answer. Physical gateG3
still requires completed named values. CAN line DC readings alone do not prove
correct CAN frames, current controller timing or actual standby/RXD state.

Because current bus levels were now confirmed after the earlier negative tests,
performed one fresh bounded **read-only** raw USB capture. Exact productChimera,
serial3a0044001651333038373636/versionv1.0.0-DEV-de193215-DEBUG and application
signature match.8.001084505s,4091bulk reads, all return codes0and actual lengths0,
zero CAN bytes before parsing and0frames on every bus0/1/2;16health reports.
Uptime25360..25367versus prior initialization23897is consistent with continuity,
not proof of unmodified controller registers. No evidence of an intervening
reset from these samples, but live BTR remains unread.

No OUT/rate change/reset/heartbeat/CAN dataTX/config/flash/port move. Reader
closed, USB owner listempty. Last requested runtime500kfrom prior test remains
the historical last command; this passive probe did not change or measure it.
Native executable/canonical DBC hashes unchanged. No fresh native/unit tests
needed: raw USB has no payload to pass to the decoder. Project baseline
89ab3037ad7c7ea1cfdfc44a842120c7423a878dclean. Only Ai documentation changed;
existing other holds and the physical diagnostic gap remain.

Next identify which supply measured5.05V, obtain the remaining named reading,
then qualify termination and actual VCC/STB/RXD/controller timing as required.
No healthy-supply or damaged-board diagnosis is established by this response.
The reference transceiver supply range is4.5..5.5V, but comparing5.05Vto that
range requires a confirmed measurement point and does not read the chip VCC:
[NXP TJA1042 Rev11](https://www.nxp.com/docs/en/data-sheet/TJA1042.pdf).

Central report retains OWNER_READINGS.json, USB_AUDIT.json, raw-usb.bin,
application signature, guarded IN-only helper and baseline pins. Reused the
source-first/debugging evidence workflow; no fresh REA/decompilation claim.
