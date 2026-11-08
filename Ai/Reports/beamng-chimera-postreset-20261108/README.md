# BeamNG through Waveshare after RESET — November 8, 2026

Retested genuine BeamNG → PC Waveshare → original Chimera printed CAN2 →
Radxa native pandad. Owner confirmed “Yes, Chimera CAN2 only”, without actuators.
Waveshare RX had recovered on the separate sensor bench; that earlier result
was not evidence of its TX or Chimera reception.

The saved Bastion `q8b_ego` scene on West Coast USA ran with game AI targeting
20 km/h. Actual body maximum was **21.034 km/h** during wire transmission.
This is simulator AI, not Sunnypilot model/control output.

| Observation | Result |
| --- | --- |
| Genuine source capture, 8 s | 400/400 decoded; 391 above 1 km/h |
| Waveshare serial submission, 12 s | 602 samples / 7,224 telemetry frames |
| Native reader, 32.115 s | 3,032 CAN batches, 32 health replies, zero frames |
| USB buses 0 / 1 / 2 | 0 / 0 / 0 frames |
| Independent Python reader, 10 s | 978 polls, 19 health replies, zero frames |
| Additional serial submission, 6 s | 301 samples / 3,612 telemetry frames |

Serial submission does not prove electrical CAN transmission or acknowledgment.
All three buses were counted before simulation decoding. Chimera USB and health
work, but these captures cannot isolate Waveshare TX, physical wiring/termination,
Chimera transceiver supply/enable, controller state or installed firmware.
The saved source is not proven equivalent to the installed historical image.

Both readers and gateways stopped with exit0. Game AI disable and stop-input
requests were acknowledged; game is left open and paused, with two identical
simulation timestamps/positions. Applied parkingbrake still read0 and wheel
speed was nonzero while paused: a zero-speed parked state is not claimed.
Waveshare500kstandard/silent configuration was written and serial closed;
there is no adapter mode readback. No Chimera USB OUT/config/relay/heartbeat/
reset/flash or physical actuator commands were sent.

Baseline project `bcfc0ca7007e49978a001f84c21c01956070a8be`; Panda `8a16e089`,
opendbc `150f9371`. Native SHA256
`e9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84`;
canonical DBC SHA256
`b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67`.
Exact Chimera serial `3a0044001651333038373636`, version
`v1.0.0-DEV-de193215-DEBUG`. All76legacy manifest entries, selected source/
binary/DBC hashes and pre-existing steering dirty state were preserved.

[Measured results and source pins](RESULTS.json). Central teacher report holds
raw JSONL, native diagnostics, PC motion polls, exact helpers and GATES.md.
Two gates passed (source motion, cleanup/preservation); physical CAN acceptance
failed and is handed off, not counted as a pass. Use a known-good independent
receiver or qualified measurement to verify Waveshare TX/ACK before blaming or
changing Chimera. Existing firmware-rewrite and upstream-update holds remain.

Used debugging, Git/documentation skills and compact Unlazy gates, with teacher
source-first recovery and direct runtime/USB observations. No new REA parser or
binary analysis was required or claimed. No product/firmware/DBC/model update,
managed stack, vehicle qualification or push.

## Follow-up: was Chimera itself verified at 500 kbit/s?

Source review (QA49) confirms all three controllers start with5000, which the
driver defines as500kbit/s. PrintedCAN2 maps toMCUCAN3. The live test set
Waveshare500k; it did not read actual installed Chimera timing and yielded0frames.
Working500kChimera reception is unproven; installed de193215/source equivalence
is also unproven. No new device/config action. [Source pins](BITRATE_FOLLOWUP.json).
