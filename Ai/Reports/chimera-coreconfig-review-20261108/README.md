# RetroPilot Core Config and current Chimera settings — November 8, 2026

Read the pinned Core Config source and the attached original Chimera's saved
configuration. This is a new live flash **read**, not a configuration repair.
Exact serial `3a0044001651333038373636`, version `v1.0.0-DEV-de193215-DEBUG`.

| Saved speed field | Current value |
| --- | --- |
| CAN0 | 500 kbit/s |
| CAN1 | 500 kbit/s |
| CAN2 | 0 (desktop tool labels Disabled) |
| CAN3 | 0 (desktop tool labels Disabled; fourth field, not fourth physical bus) |

The owner-confirmed physical cable is on printed CAN2, corresponding to USB2 /
MCUCAN3. Its saved speed is zero. This is a concrete discrepancy worth resolving,
but not proof of the controller's actual speed or the zero-frame root cause.

Core Config has separate runtime Apply and flash Save operations. The preserved
firmware starts all three controllers at fixed500k and never consumes these
saved speed fields. Its0xDEruntime Apply handler changes only bus0. The website
snapshot can report successful apply/save/reboot instructions without verifying
those semantics on this image. Installed de193215/source equivalence is unknown.
Do not infer active500k or an inactive CAN2 from UI selection/stored bytes alone.

SYS_CFG is present: debug3, output mask0x0F (all four generated angle/engine/
speed/cruise reports enabled), watchdogoff, mode0/override0. Entries1..31are all
zero, so no sensor-signal mappings are saved. Those omissions can matter for
Chimera-generated sensor reports; source raw CAN queuing and USB receive are
independent of these mappings/output flags. They therefore do not explain away
our zero raw BeamNG captures in the preserved source.

Read the776-byte block twice; exact match, valid magic/CRC32 `78aa1591`, SHA256
`4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22`.
Independent struct/zlib decoding agrees with the Core Config decoder. The archived
October14block had all saved speed fields0; current first two fields differ.
The time/actor of that earlier change is unknown; this task made no write.

The helper allowed only vendor-IN0xD6(version) and0xFF(chunked config read):27
requests, no OUT/heartbeat/reset/bitrate/Save/Format/CAN data. USB handle closed;
no desktop app launched. The other Interceptor device was not opened. Retain
historical erase/watchdog incident and write quarantine; no automatic restore.

[Actual read and request trace](CONFIG_READ.json), [independent analysis](ANALYSIS.json),
[raw config snapshot](config-first.bin), [source pins](SOURCES.json).
Central teacher report also retains repeat bytes, baseline dirty-file records
and the inspected read helper. Project baseline `71a48a22f103c709bb55e75fde12d5ed820b8d6e`;
Ocelot existing dirty sources and all76preserved Chimera files remain unchanged.

Next establish whether installed firmware uses saved CAN2 speed, with an exact
image/source or qualified timing observation; independently qualify Waveshare
TX/ACK and Chimera reception. This read does not prove500kcommunication or
vehicle/safety operation. Firmware-rewrite/upstream holds and write restrictions
remain. Used debugging/source-first/direct USB evidence; no new REA binary
analysis or graph was necessary or claimed. No product or firmware changes.
