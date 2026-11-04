# BeamNG read-only CAN telemetry — 2026-11-04

Owner requested steering angle,speed,IMU,brake and optional cruise from the PC
through Waveshare/CAN/Chimera to Radxa, using the shared DBC and adding missing
signals centrally. Later confirmed Waveshare connected, and authorized repair
of the PC NVIDIA driver that blocks BeamNG. Existing control/firmware holds
remain; this task does not authorize physical vehicle actuation.

Implemented the game read-only protocol, canonical RP-SIM-1 DBC additions,
PC cantools40.7.1 encoder/Linux serial gateway and installer, independent Radxa
opendbc decoder/Cereal monitor, and explicit RETROPILOT_BEAMNG passive profile.
Old20DBC messages remain byte-identical. Added8message definitions for sample/
clock,accel,gyro,wheels,pedals/gear and actual cruise status. Original DBC and
provenance retained centrally; packaged/deployed copies match VERSION.json.
Legacy CRUISE ADC overlap is preserved and unused. Generic physical profile
keeps its unqualified speed factor; sim profile explicitly uses centi-km/h.

Telemetry uses full CRC/exact DLC,bus2,counters/coherent sample begin/end,
session/sequence/time checks,100ms assembly and150ms receipt freshness. PC
checks source age/order/simulation progress, never repeats stale data, and
bounds serial writes50ms. No actuator/relay TX path exists. Live noOutput,
carNotReady,dashcamOnly and empty controller TX remain. IMU is decoded using
installed BeamNG motionSim component conventions; measured device-frame axes/
origin and localization-provider integration remain pending. No camera/model/
Thneed/Panda/Chimera firmware changes or fake board health.

Actual source evidence: installed PC BeamNG build20972 Lua protocols.lua,
motionSim.lua,sensors.lua,wheels.lua,cruiseControl.lua (hashes in receipt),
canonical RetroPilot/opendbc6b90fafe,existing Waveshare framing source and
[official BeamNG protocols](https://documentation.beamng.com/modding/protocols/).
No unrelated REA binary analysis was needed; readable source and runtime
commands supplied evidence. Skills: API/interface,incremental implementation,
TDD,debugging,code review,documentation and Git workflow.

Validation:17 focused tests pass, including independent cantools->opendbc,
actual Lua54 execution/availability/reset checks,C FFI128-byte layout,CRC/DLC/
wrong-bus/missing/mixed/duplicate/stale cases,counter/sample wrap and session
retirement,real local UDP->gateway->Linux PTY->independent decoder, and blocked
serial timeout. Existing45RetroPilot,53CAN and50native RetroPilot safety tests
pass. Broader car/interface/platform/model suite:278run,1existing skip.
Ruff,diff checks,canonical SHA256SUMS and notebook checks pass. Initial tests
caught reserved DBC signal name,FFI trailing padding and uninitialized sensor
pointer handling; all corrected before completion. These are software checks,
not a live game/physical CAN result.

Actual two-host check: deployed PC gateway accepted a synthetic loopback UDP
fixture and Radxa decoded its12CAN frames returned via SSH. No physical CAN
TX in that test; see fixture receipt. PC bundle is under
/home/pc/beamng-q8b/retropilot-can with an isolated .venv. Read-only mod installed
in the game user folder; Other protocols enabled with settings backup. Existing
other protocol mods were checked before enabling. PC SSH verified against the
previously trusted host key via HostKeyAlias10.42.0.216 at current10.43.0.216.
Actual CH3401a86:7523 enumerates ttyUSB0/by-id; no real adapter was opened yet.

GPU blocker: running kernel7.0.0-38-generic has no NVIDIA module; only31has one.
Next installed kernel42also lacks one. NVIDIA595.84 user libraries are installed,
SecureBoot disabled,dkms absent. nvidia-smi fails; BeamNG logs only llvmpipe and
fatal “Unable to find a usable Vulkan GPU.” Desktop Xauthority was separately
recovered from the current user session. Our failed game/probe were stopped.
APT history records unattended kernel38installation onOct14 and42onNov4.
This establishes the mismatch, not the exact last successful boot/use time.

Owner authorized repair. Reviewed apt-get --simulate plan installs38/42NVIDIA
modules and updates the595-open tracking package/driver to595.99.02:16upgrades,
3new,1obsolete31NVIDIA-module removal; no general upgrade/autoremove or kernel
removal. One-off script is prepared and Bash syntax checked. sudo -n requires
a local password; a PC GNOME terminal now asks the owner to authenticate there.
No password requested/stored in chat. Package installation has not started at
this checkpoint, no repair success or reboot claimed. Official Ubuntu guide:
https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/

Next: after local authentication, inspect repair log,nvidia-smi/module versions,
Vulkan and game startup; ask before any PC reboot. Then capture genuine game
UDP,verify field/sign/availability and only then a bounded isolated CAN delivery
check with the actual Chimera route. Chimera firmware/manager/physical control
work remains held; current telemetry can be inspected from existing receive
publication only. The owner-selected game vehicle/configuration is still unknown.

Later checkpoint: owner supplied sudo authentication locally; APT download started.
No package installation/repair success is claimed yet. CAN implementation child
commit150f937198ceab43c43b39f94b9bdea63fcb633c is saved, with source/fixture checks.

Later hardware checkpoint: actual Radxa USB product Chimera/bbaa:ddcc now matches
versionv1.0.0-DEV-de193215-DEBUG. One-second receive-only version/43-byte-health/
bulk-IN probe succeeded with0CAN frames,controls_allowed0; no control/bulkOUT,
bitrate,safety,heartbeat or configuration writes. This is USB receive acceptance
with no observed CAN payload, not a wire-delivery or firmware safety result.
Latest focused suite17passes includes a command-message allowlist rejection.

## 2026-11-04 — Saved implementation and download recovery checkpoint

CAN implementation parent880a0adb542d107e59724df954fb08144f0b8f86 and
opendbc150f937198ceab43c43b39f94b9bdea63fcb633c are locally committed.
Actual source/fixture validation attached to both in the maintenance ledger;
central code index refreshed. No remote push. Both trees were clean afterward.

PC repair owner authentication succeeded. APT is retrying large NVIDIA files
from in.archive.ubuntu.com; pre-download of the exact same five large packages
in 1MiB HTTPS ranges from security.ubuntu.com was started in a user-owned cache.
Each assembled package must match the SHA256 from the PC's existing APT index.
No package-plan, repository configuration or running root script change;
no installation/driver/game success yet. Installed kernel38/42 module packages
have downloaded to APT cache; driver libraries/firmware remain in progress.
17 focused CAN checks pass. Genuine game and physical CAN remain pending.

## Later physical CAN attempt — serial permission prerequisite

A bounded synthetic telemetry-to-wire check stopped before opening Waveshare:
PC account pc is not in dialout; ttyUSB0 is root:dialout0660. No physical CAN
frame was transmitted by this attempt. Chimera received no configuration writes.
Opened a separate PC terminal for the exact command sudo usermod -aG dialout pc;
owner was asked to authenticate locally, not provide a password in chat.
After authentication a fresh SSH login must verify group membership before
retrying the wire check. Source receipt records the blocked attempt distinctly
from the earlier successful software fixture. GPU package downloads continue.

Owner confirmed second local authentication. Fresh SSH confirms dialout membership; adapter open/config and20synthetic sample writes completed. Chimera version/health/bulk reads succeeded but observed0frames, no errors/controls_allowed0. No physical delivery success claimed. Owner wiring clarification requested because saved source maps hostbus2 to connectorCAN2 but cannot establish present wiring. No Chimera writes/flash or actuator commands.

## CAN wire observations after owner replies

Owner said "connected to can 3 of chimera". Record that exact wording; saved
source maps MCUCAN3 to hostbus2/connectorCAN2, but owner terminology/board label
has not been independently checked. Reader inspected all bus tags, not only2.
Owner then said "i removed the resisitro see now". A second bounded20sample
synthetic physical-adapter attempt again produced0Chimera frames,0decode.
Both captures preserved separately. Which resistor and external power remain
unanswered; another brief clarification is pending. Do not infer correct
termination or powered CAN transceivers from USB enumeration/zero health ADC.

Source lead: ocelot/firmware/chimera/can.h initializes can_silent=0xFF and
passes each silent bit into llcan_set_speed. A two-node link needs an ACK
participant; a silent receiver is a possible zero-frame cause. This is the
94efc673 local source with modifications, NOT recovered de193215 nightly source.
Installed version is de193215; its exact source remains unavailable. The saved
nightly ZIP contains only signed Chimera binary, no ELF/symbols. No claim that
installed silent state was read, and no firmware/config/USB-OUT change made.
REA skill routing reviewed; readable source and saved provenance were used,
no new binary/decompilation result fabricated.

## NVIDIA repair and genuine game acceptance

Original authorized repair finished2026-11-04T19:49:40Z without reboot/desktop
restart. GTX1650 recognized by nvidia-smi595.99.02; nvidia/nvidia_modeset/
nvidia_drm loaded, module versions38and42both595.99.02, dpkg --audit clean.
APT slow/retry download stage took28min42s. Independent exact-package HTTPS
range/hash fallback also completed; original APT ultimately installed itself,
so no third authentication/cache-copy/cancel was needed. Raw repair log saved
centrally. No passwords stored.

BeamNG20972/0.39.4 launches on NVIDIA Vulkan, successful swapchain and mod mount.
No pre-existing vehicle at menu. Loaded temporary Bastion reference on
west_coast_usa at the prior proven observation coordinates; this is our test
fixture, NOT owner-selected/calibrated model. Cold map loading exceeded the
100s BeamNGpy client timeout; game stayed healthy and finished loading.
Recovered current scenario metadata after reconnect and started it; no steering,
throttle or brake commands were sent. Original preview had0packets during map
loading; later actual producer works without BeamNG.tech license.

Genuine game Lua->PCgateway->fileoverSSH->Radxa decoder:1480/1480samples decoded
in42.387s, median19.982ms, largest cold/startup gap3545ms. Last RPM729;
speed/angle0; driver brake0 and applied brake1 in pre-start freeze; independent
wheels, accel, gyro, neutral gear and actual cruise available/disabled/target
27.78m/s present. Buttons unavailable as designed. Receiver expires after
150ms. A separate12s steady pre-start capture decoded460/460, median19.894ms,
max56.993ms,0gaps>150ms; actual ~38Hz wall throughput, not a guaranteed50Hz.
Post-start capture is being checked separately. No moving sign/device-frame
calibration or physical CAN success inferred.

## Final software/GPU checkpoint; physical wire still unresolved

Post-start genuine capture492/492 samples over11.995s passed independent
decoder and actual passive CarInterface (canValidtrue/vehicleSensorsInvalidfalse,
noOutput,dashcamOnly,carNotReadytrue). Median19.835ms,p9547.902,max57.640,0gaps
>150ms. Actual throughput~41Hz, not guaranteed50Hz. Final genuine-game serial
TX attempt117samples/3s received0Chimera frames. Firmware/manager/control holds
unchanged. All bounded gateways/readers stopped; BeamNG remains open with the
temporary Bastion reference scene and read-only UDP producer. PC account now
has dialout access. Next measure termination/transceiver rails,confirm wiring/
bitrate and qualify ACK/silent behavior. Current hardware owner facts retained;
no invented powered-rail or installed silent-state conclusion.

## Final network interruption

After GPU/game/CarState captures and bounded CAN tests completed, SSH/SCP to
10.43.0.216 returned No route to host. Radxa eth1 remains10.43.0.1/24UP;
neighbor FAILED. Prior10.42.0.216 and saved neighboring192.168.1.100 also did
not connect; pc.local did not resolve. Cause is unknown; no interface/reset/
reboot command was issued. No repair failure inferred from network loss.
Successful repair log,all actual captures/compact receipts are already on
Radxa. Last successful observation: GTX1650/595.99.02, BeamNG running temporary
Bastion scene; bounded gateway/readers completed and exited. Final PC README
serial-permission paragraph copy failed; deployed executable/Lua/DBC were
already verified and unchanged. Reconnect the PC link on resume,then copy that
documentation paragraph and continue electrical CAN qualification.
