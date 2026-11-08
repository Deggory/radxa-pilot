# Moving BeamNG and all Chimera source buses — November 8, 2026

Owner requested checking all CAN ports while running the BeamNG car at speed.
Baseline d05a820b7d417d9a8a1c8129a38c60c849c35cb4; opendbc150f9371;
Panda8a16e089; native pandad SHAe9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84.
[Measured results/source hashes](RESULTS.json). No product code/firmware/DBC change.

## What was exercised

BeamNG's own span AI drove the existing Bastionq8b_ego in West Coast USA with
a20km/h target. This is game-only AI, not Sunnypilot steering/control output.
Actual body speed reached21.071km/h and wheel speed21.178km/h; the body maximum
was measured during the wire phase. Eight-second genuine-source capture decoded
401/401samples;392were above1km/h, speed0.14..20.31km/h in that source segment.
Then the unchanged gateway submitted602genuine samples during12s through the
Waveshare CH340 adapter at500kbit/s, serial2Mbaud. Serial success is not CAN ACK.

The existing native receiver was monitored for32.116s:3009CAN publications,
0frames,32raw-health diagnostics, no native error, exit0. All frames would be
counted before simulator interpretation; there was no bus2-only capture filter.

| Board group | USB source bus | Source MCU mapping | Frames observed |
| --- | --- | --- | --- |
| CAN0 | 0 | CAN1 | 0 |
| CAN1 | 1 | CAN2 | 0 |
| CAN2 | 2 | CAN3 | 0 |

The [official Chimera guide](https://wiki.retropilot.org/index/hardware/chimera),
reopened November8, documents6CAN0connectors,3CAN1and3CAN2connectors. These are
three shared buses, not12independently selectable USB channels. It documents
separate termination headers and CANH/CANL/GND on pins2/3/4. This is reference
mapping, not a measured continuity/power check of the attached revision.

Owner subsequently confirmed the printed connected group is "CAN2". This
resolves the earlier "CAN3" wording in the teacher notes: the current physical
label is CAN2; preserved source maps it to MCUCAN3/USB2. No cable was moved.
Monitoring all3software buses does not electrically test every unused connector.
There is no evidence of a parser choosing the wrong bus as the explanation
for0raw frames. Native and independent Python zero-frame checks from the prior
QA32run remain separate evidence; Python was not rerun in this moving test.

## Cleanup and limits

Game AI disabled, game-only throttle0/brake1/parkingbrake1acknowledged and pause
acknowledged; game left open. PC gateway and native reader stopped. No physical
actuator commands, MCU control OUT, heartbeat/relay/config/bitrate/flash write,
new firmware, model/camera launch, dependency update, upstream change or push.
76legacy source/recovery manifest entries and selected runtime/binary/DBC hashes
match. USB-only Chimera power and removed Waveshare termination remain the
owner-confirmed setup; actual rails/resistance/ACK/silent-state are unmeasured.
No external-power requirement or specific hardware root cause is inferred.

Moving source data did not restore CAN reception. Source/game-motion/bus-count
and cleanup checks pass, but physical coherent-CAN acceptance is not met:
Unlazy3met/0unmet/1abandoned(G3), with explicit external-measurement handoff.
Next inspect/measure actual CAN2wiring/ground/termination/transceiver supply and
bitrate/ACK/firmware ingress. No random relay/safety/firmware change. The new
Chimera rewrite and saved upstream hold remain unchanged.

Central teacher Ai/Reports/beamng-moving-can-20261108 retains exact helper
source, PC execution, raw game trace/native health, gates and handoff. This
student copy is a portable measured summary, not a full chat transcript.
Skills: Unlazy compact observable gates, systematic debugging, documentation
and Git; source-first inspection plus actual game/USB runtime, no unrelated
REA binary analysis claim. Existing prior-reader evidence reused accurately.
