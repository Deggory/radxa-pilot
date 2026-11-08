# Known-working steering sensor through Chimera CAN2 — November 8, 2026

Owner moved the same previously Waveshare-working sensor to printed Chimera
CAN2, with Chimera USB connected to Radxa. Owner confirms separate sensor power
and supply negative joined to Chimera GND. Owner chose to keep CAN2; no physical
CAN0 comparison or cable move was performed.

The expected raw sensor message is OEM0x25/DLC8 at500kbit/s, as previously
observed on Waveshare with4,159valid checksums and motion-responsive payloads.
That earlier test proves the prior sensor/Waveshare setup, not this receive path.
OEM0x25is distinct from canonical RetroPilot0x50; no DBC/ID change was made.

Initial native startup failed with exit2 because Core Config held the exact
Chimera USB interface. PID23504/web_app.py was confirmed to hold the USB node.
This attempt is not a valid zero-frame CAN test. After the owner answered yes to
Disconnect, the USB-owner scan was empty and the bounded capture started.

| Completed observation | Result |
| --- | --- |
| Native reader duration | 20.114 s |
| Native CAN batches / health replies | 1,892 / 20 |
| Raw frames on USB0 / USB1 / USB2 | 0 / 0 / 0 |
| Independent Python USB reader | 8 s requested, 784 polls, 15 health replies |
| Python raw frames | 0 |
| Sensor0x25frames / angle reading | 0 / unavailable |

The actual native profile was chimeraOldMailbox16; both readers exited0 and
stopped. USB version/health work, but no raw sensor data reaches either reader.
Missing angle mapping or calibration cannot explain an empty raw capture in the
preserved receive source. The helper's RP-SIM-1 sample counter is not an OEM
sensor decoder; raw frame counts are the relevant observation here.

Power/common ground are owner-confirmed, not measured. Current CAN2 active
bitrate, supply/standby, wiring/termination and waveform remain unqualified.
The earlier stored CAN2speed0 is a clue, not proof of active disabling: preserved
source ignores saved speeds and installed-image equivalence remains unknown.
No sensor fault, CAN-chip fault or fix is diagnosed. Continue on CAN2 as owner
selected; next qualified electrical/enable/timing checks rather than another
unrequested port move or blind configuration/flash.

Baseline `e886a564588ed4a425f9bf7e6936f51cd79e4500`; original serial
`3a0044001651333038373636`, version `v1.0.0-DEV-de193215-DEBUG`.
Native SHA `e9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84`;
canonical DBC SHA `b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67`.
All76legacy entries and selected runtime/DBC hashes preserved. No product,
firmware, DBC, model, upstream or app-source changes; no host CAN transmission,
USB OUT/config/heartbeat/reset/flash. Core Config window left open/disconnected;
final USB-owner scan empty. [Results and source pins](RESULTS.json).

Teacher report retains initial-failure log, both actual captures, owner recheck,
exact helper and final readback. Used debugging/source-first/direct runtime
capture; no unrelated REA/decompilation or graph result. Physical reception
remains blocked; completed diagnostic observations are not vehicle acceptance.
