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

Later hardware checkpoint: actual Radxa USB product Chimera/bbaa:ddcc now matches
versionv1.0.0-DEV-de193215-DEBUG. One-second receive-only version/43-byte-health/
bulk-IN probe succeeded with0CAN frames,controls_allowed0; no control/bulkOUT,
bitrate,safety,heartbeat or configuration writes. This is USB receive acceptance
with no observed CAN payload, not a wire-delivery or firmware safety result.
Latest focused suite17passes includes a command-message allowlist rejection.
