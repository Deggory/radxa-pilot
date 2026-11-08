# BeamNG / Waveshare / original Chimera live test — November 8, 2026

Owner requested testing after switching on the PC and recovering prior teacher
work. Baseline5c46788e636792905260b883ca2c670f07ccde60; opendbc150f9371;
Panda8a16e089. No application, firmware, DBC or dependency source changes.
[Measured results and source/raw hashes](RESULTS.json).

## Measured result

| Stage | Actual observation |
| --- | --- |
| PC/game | Strict authenticated SSHpc@10.43.0.216; trusted host alias10.42.0.216. CH340Waveshare detected; GTX1650/driver595.99.02 working. |
| Genuine BeamNG source | Saved Bastionq8b_ego/West Coast observation scene loaded, producer resumed.501/501genuine samples decoded independently, all12RP-SIM-1IDs. This file replay is not CAN delivery. |
| Native real USB | Existing built pandad hash e9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84 accepted serial3a0044001651333038373636/versionv1.0.0-DEV-de193215-DEBUG/health43. Baseline5health samples and470empty CAN batches over5.115s. |
| Native wire attempt | PC gateway submitted502genuine samples over10s to Waveshare500kbit/s, serial2Mbaud. Native received0frames in1332CAN batches/14.114s;14raw-health samples, no native error, exit0. |
| Independent cross-check | Existing Python receive-only reader received0frames/979polls over10s,19health samples, exit0, while PC submitted302genuine samples over6s. |
| Cleanup | Native/Python readers and PC gateway stopped. BeamNG remains open; pause RPC acknowledged. Other protocols was true before/after. No duplicate can publisher. |

These observations establish actual Chimera USB version/health communication
with the native host path. They do not establish successful CAN-wire delivery
or full managed/vehicle/safety support. Serial completion does not prove that
CAN left the adapter or was acknowledged. Zero frames in two independent
receivers makes a native-decoder-only explanation insufficient; it does not
isolate cabling, transceiver power, termination, bitrate/ACK or board firmware.
No rail voltage can be inferred from Chimera's placeholder power fields.

## Teacher recovery and owner confirmation

Recovered November4 path: PC screen to Radxa webcam and BeamNG->gateway->
Waveshare->Chimera USB. Then492/492genuine samples decoded from replay, but117
submitted samples produced0received frames. Recovered source500kbit/s and
hostbus2/MCUCAN3/connectorCAN2 distinction; actual current connector remains
unmeasured. Owner reaffirmed "Same setup as before": Chimera USB-only power,
removed Waveshare termination resistor and unchanged wiring. Do not ask for
those retained facts again or infer an external-supply requirement from them.

## Scope and setup corrections

Only simulator telemetry IDs were transmitted by the unchanged gateway allowlist;
no steering/gas/brake/RelayCore commands, heartbeat/safety/config/flash writes or
Chimera firmware changes. Native USB uses guarded D6/D2 and bulk-IN only.
No model/camera/managed-Sunnypilot launch, localization feed, calibration,
NVIDIA/package repair, upstream fetch/merge or push. Source76legacy files,
canonical DBC and selected runtime hashes verified unchanged. New rewrite stays
halted; prior upstream update hold retained and inbox still datedNovember4.

The game was initially launched with an incorrect port option. Stopped only
that newly launched game and relaunched with the recovered -tcom -tport64256.
The first capture helper used the unavailable top-level cereal import; corrected
the helper to openpilot.cereal before any USB/process start. Remote rg was
absent; used Python/standard utilities. Recovered BeamNGpy from the original
Beamng-onnx/.venv without installing/changing dependencies. The existing scene
loader completed normally after a cold load. Protocol mod/gateway/DBC match
saved source; a game settings backup is on PC under retropilot-can/live-20261108-*.

## Handoff

Unlazy ledger in teacher Ai/Reports/beamng-chimera-live-20261108/GATES.md:
2met,0unmet,1abandoned (G2physical acceptance). Checks verify genuine source and
cleanup/preservation; CAN success was not claimed. Raw captures/scripts/PC stderr
and exact source hashes remain in that central report; this student copy is a
portable measured summary, not the full raw session transcript.

Next needs measured connector/CANH/CANL/ground, termination, transceiver rails
and bitrate/ACK before another bounded wire acceptance attempt. No guessed
power/relay/silent-mode change or stock Panda flash. Physical CAN acceptance
remains unresolved; preserved firmware source is not proven identical to the
reported installed de193215image. Code/model/firmware holds are unchanged.
