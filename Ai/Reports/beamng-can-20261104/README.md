# BeamNG CAN telemetry and PC graphics repair — 2026-11-04

The owner requested PC BeamNG steering, speed, IMU, pedals and optional cruise
through Waveshare/CAN/Chimera to Radxa using the shared DBC. The software is
implemented and genuine game replay works. **Physical CAN delivery to Chimera
has not passed.** The separately authorized NVIDIA repair succeeded without
reboot; BeamNG is open in our temporary Bastion/West Coast reference scene.

## Implemented and saved

Parent implementation880a0adb542d107e59724df954fb08144f0b8f86 and opendbc
150f937198ceab43c43b39f94b9bdea63fcb633c. Both have actual source/fixture
validation attached to the maintenance ledger. No remote push or upstream update.

- Read-only Lua protocol in the game user folder, standalone PC gateway with
  cantools40.7.1, installer and bounded Linux Waveshare serial transport.
- Canonical `retropilot/dbc/ocelot_controls.dbc` RP-SIM-1 adds8sim-only messages;
  original20message layouts remain byte-identical. Packaged/deployed copies
  match SHA256b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67.
- Independent opendbc decoder, Radxa receive monitor and explicit passive
  RETROPILOT_BEAMNG CarInterface. Steering/speed,pedals,wheels,gear,IMU and
  actual cruise status have explicit units and availability. Buttons remain
  unavailable; no invented cruise-button edges.
- CRC,exact DLC,bus2,counters,coherent samples,sessions/sequence/time,
  100ms assembly/150ms receipt freshness and50ms serial-write deadline.
  Encoder allowlist excludes actuator commands. NoOutput,dashcamOnly and
  carNotReady remain; no IMU localization integration or calibrated device axes.

Existing generic physical RetroPilot speed factor stays unqualified; the sim
profile explicitly uses centi-km/h. Legacy CRUISE ADC overlap remains unchanged
and unused. No camera,model,Thneed,Panda/Chimera firmware or manager integration
change; relay and physical actuation work remain excluded.

## Actual verification

17 focused tests pass: independent cantools->opendbc, actual Lua54 with API
fixtures and128-byte FFI layout, missing/invalid fields, CRC/DLC/wrong bus,
partial/mixed/stale/duplicate/order/reset/wrap handling, actual local UDP->CLI
->PTY->decoder, blocked serial timeout and actuator-name rejection.
Existing45RetroPilot,53CAN and50native RetroPilot safety tests pass. Broader
car/interface/platform/model:278run,1existing skip. Ruff,DBC prefix/SHA256SUMS,
Bash syntax and notebook verification pass. These tests did not enable control.
Initial reserved DBC signal/FFI padding/uninitialized pointer/schema-field
failures were corrected before the implementation commit.

The deployed PC synthetic UDP fixture decoded on Radxa. Later **genuine game**
Lua packets produced1480/1480decoded samples over42.387s. Cold loading caused
one3.545s gap; freshness expires rather than repeating data. A separate steady
pre-start12s capture decoded460/460 with max56.993ms interval. After starting
the scenario,492/492samples over11.995s produced valid CarState/canValid through
the actual CarInterface; median19.835ms,p9547.902ms,max57.640ms,0gaps>150ms.
Measured wall throughput was about41Hz;50Hz is a producer cap, not a guarantee.
[Active-game receipt](../../Evidence/beamng-active-game-20261104.json) records
values and raw capture hash. Stationary reference only: moving steering sign,
IMU frame/origin and actuator calibration are unqualified. Cruise available/
disabled/target27.78m/s was real game state; generic buttons unavailable.

## NVIDIA repair completed

Running kernel7.0.0-38 initially lacked NVIDIA modules; only older31had one and
installed next42also lacked one. User libraries were595.84. nvidia-smi failed
and BeamNG reported no usable Vulkan GPU. This explains the observed startup
failure; exact last successful boot/use time is unknown.

The owner authorized repair and authenticated locally. Reviewed Ubuntu plan:
16NVIDIA upgrades,3new packages,1obsolete31NVIDIA-module removal, no kernel
removal/autoremove. Downloads retried for28min42s; independently verified HTTPS
range downloads of the same APT-index packages also completed. Original APT
ultimately installed successfully; no extra cache-copy/root retry was needed.
Driver595.99.02 loaded,GTX1650recognized,38/42module versions verified,dpkg audit
clean. BeamNG NVIDIA Vulkan/swapchain and game loading passed. No reboot or
desktop restart. [GPU receipt](../../Evidence/beamng-nvidia-repair-20261104.json).
Method follows [Ubuntu's driver guide](https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/).

## Physical wire gate remains unresolved

Owner authenticated to add PC account pc to dialout; fresh SSH and actual
Waveshare open succeeded. Before access repair the attempt stopped at Permission
denied without TX. Two later20sample synthetic adapter attempts, before/after
owner's resistor change, received0Chimera frames. A final3s genuine running-game
attempt submitted117samples via the serial gateway and again received0frames.
[Actual game wire receipt](../../Evidence/beamng-real-game-wire-20261104.json).
Serial success is not evidence of successful wire transmission or CAN reception.

Owner reports “CAN3”, USB-only Chimera power and Waveshare resistor removed.
Saved source maps MCUCAN3 to softwarebus2/connectorCAN2; actual terminology and
termination/rails/bitrate/ACK have not been measured. Reader monitored all buses.
Chimera USB versionv1.0.0-DEV-de193215-DEBUG,43-byte health and bulk reads passed;
controls_allowed0. No Chimera OUT/config/bitrate/heartbeat/flash write occurred.

Local modified94efc673source initializes can_silent=0xFF; this is a possible
ACK-related lead, not a read of the installed nightly's state. Exact de193215
source is unavailable. Do not change safety mode/relay or flash a guessed fix.
The [Chimera hardware reference](https://wiki.retropilot.org/index/hardware/chimera)
describes pins/termination but does not prove this USB-only bench's rails.
Next measure actual termination and transceiver power,confirm wiring/bitrate,
then qualify ACK/silent behavior before another end-to-end acceptance test.
Firmware/manager/physical control holds remain.

## Evidence, deployment and limits

PC `/home/pc/beamng-q8b/retropilot-can` uses an isolated .venv; original model
environment/game binaries unchanged. Read-only mod installed with license and
settings backup; Other protocols enabled after checking other installed mods.
Trusted PC host key reused with HostKeyAlias10.42.0.216 at10.43.0.216. Actual
CH3401a86:7523 by-id adapter detected. All bounded gateways/readers stopped;
last observed BeamNG/read-only UDP mod running; no CAN transmitter is left running.

Source evidence: actual installed BeamNG20972 protocol,motionSim,sensors,wheels,
cruise Lua hashes in [receipt](../../Evidence/beamng-can-20261104.json), canonical
RetroPilot/opendbc6b90fafe and reviewed Waveshare source. Source-first/runtime
commands used; REA routing read for firmware lead, no new binary result claimed.
Skills: API/interface,incremental implementation,TDD,debugging,code review,
documentation and Git workflow. Cold map load exceeded the100s client timeout;
game finished loading, then current scenario metadata was recovered to start
it without reload or vehicle control commands. This temporary test vehicle is
not an owner-selected/calibrated platform.

Final network limit: after all captures completed,PC10.43.0.216 became
unreachable (No route to host). No cause/reboot is inferred. Repair/game
receipts are saved; the last5-line README clarification was not copied to PC.
Executable/Lua/DBC deployment predates this loss and had passed actual tests.
Next restore the PC link,copy README,and qualify the physical CAN bus.
