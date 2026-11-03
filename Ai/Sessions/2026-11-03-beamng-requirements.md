## 2026-11-03 — Connected PC: Sunnypilot input requirements

Owner reports PC connected with BeamNG and asks what Sunny needs to treat it
as the vehicle. Retained the accepted optical webcam + Waveshare/Chimera CAN
architecture. Added six requirement groups to the existing BeamNG README:
images, vehicle state, simulated motion, per-vehicle parameters, CAN/board
transport, and final command/engagement/failure behavior. No runtime or DBC
implementation was requested by this requirements increment or claimed complete.

Read-only local checks at approximately 10:08 UTC: Q8B eth1 UP/10.43.0.1,
10.43.0.216 reachable in the neighbor table. Strict batch SSH to saved
pc@10.43.0.216 exited255 because no trusted ED25519 host key is known; no remote
command ran. Current game version, selected car, mods and PC USB devices remain
unverified. Historical BeamNG.drive0.39.4.0.20972/BeamNGpy1.35.1 stay historical.
Resolve PC identity through existing trusted evidence or owner fingerprint
before remote inspection; do not silently trust a scanned key.

Source base893e17344975ad8f2b3735b0e2f4e534e02ec3c5, branchradxa/q8b initially
clean. Inspected current car.capnp/card.py/interfaces.py/paramsd.py and existing
PC/Radxa/shared guides. Reference5435d67499f66eca58f95882cbe35e9c577e874c,
canonical DBC6b90fafe/SHAef6eef74 and selected CD210 GPU eb741641 unchanged.
Official https://docs.beamng.com/modding/protocols/ confirms vehicle-Lua custom
telemetry support; basic OutGauge is incomplete for the planned interface.
No current retail-game advanced-sensor capability inferred from Tech docs.

Upstream inbox last checkNov2 15:30UTC: no pending related commits;8historical
failed/blocked local validation entries retained. Timer active, nextNov3 15:30UTC;
last service result success/exit0. No upstream integration. Next implementation
remains increment1: resolve canonical wire semantics/gaps, timing and command
family, then receive-only transport and optical shadow before game control.
No game/model/manager/device launch, CAN TX, firmware change or bench motion.
Skills: source-driven-development, api-and-interface-design, documentation,
git workflow and self-review. Source-only question; no REA binary result claimed.
Validation for this increment is the notebook/reference/whitespace result saved
in Ai/Evidence/beamng-requirements-20261103.json; no live-loop test.

