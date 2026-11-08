# RetroPilot Core Config clue — November 8, 2026

Accepted scope: source/config inspection for explanation of zero CAN captures.
Teacher-first recovered original Core Config, source limitations, historical
October4flash incident/quarantine andOctober14readback. Actual clean project
baseline71a48a22f103c709bb55e75fde12d5ed820b8d6e; Ocelot dirty sources pinned
separately and preserved. Pinned local website code reviewed; no current live
website behavior claimed and no desktop app launched.

Read the exact original serial/version with a guard allowing only IN0xD6/FF;
27requests,0OUT/heartbeat. Two776-byte blocks byte-identical, magic/CRCvalid,
SHA4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22.
Independent struct/zlib validation matches Core Config decode. SYS_CFG debug3,
output0x0F/watchdogoff; savedCAN0/1=500k, CAN2/3=0. No signal mappings1..31.

[Report and interpretation](../Reports/chimera-coreconfig-review-20261108/README.md)
retains raw snapshot, full trace, source pins and uncertainty. Zero storedCAN2
matches a real discrepancy at the connected bus, but preserved firmware ignores
saved speed fields and installed nightly source is unknown. Raw receiving does
not depend on generated-output flags/sensor mappings in that preserved source.
Thus no configuration fix or diagnosed500kfailure is claimed. HistoricalOctober14
all-zero saved speeds are superseded for current flash; no change actor/date known.

USB closed; no other device touched, firmware/config/bitrate/relay/heartbeat/
reset/CAN transmission or game action. Product source and76legacy entries stay
unchanged; Ocelot dirt preserved. Teacher/student logs/topic/state/handoff/session
and portable report synchronized, verified notebook increment committed and
source/read validation attached to maintenance ledger. Actual commit/readback is
in the central report FINAL_READBACK.json. Used debugging/source-first/direct
runtime reads; no unrelated REA/decompilation/graph result claimed.

Next qualify installed-image speed-field handling and physical TX/ACK/CAN2;
retain historical write quarantine and upstream/new-firmware holds. This was a
config read, not successful CAN or safety/vehicle integration. No automatic writes.
