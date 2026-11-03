# RetroPilot car platform on Radxa

Implemented 2026-11-03 in the local opendbc branch `radxa/retropilot`, based on
`aa9bff6f5442cef8cb8e25e143ef38865c276ce8`. Sunnypilot now registers
`RETROPILOT_RETROFIT` with brand `retropilot`. This is the **receive-only car-port
stage** for the owner's BeamNG → Waveshare CAN → Chimera → Radxa architecture.
The Chimera USB backend and live BeamNG loop remain separate unfinished work.

## Implemented

- Explicit platform selection through the existing `FINGERPRINT` or
  `CarPlatformBundle` selection path. No fake fingerprint or global override.
  Selecting RetroPilot suppresses OEM VIN/FW diagnostic transmission.
- Canonical `ocelot_controls.dbc` packaged byte-identically inside opendbc,
  SAE-J1850 CRC generation/checking, counter validation, and exact DLC filtering.
- Base steering angle, speed (after scale qualification), brake input, cruise
  button edges, and eight optional module-status families. Module observation
  is local to each CarParams instance and requires the correct bus and DLC.
- Missing/stale frames retain the modern base's `canValid`/`canTimeout` behavior.
  Stale state, braking, cancel or ignition loss clear the local armed indicator.
- Offline encoders for all eight canonical command IDs: actuator/SSC/Interceptor
  steering, pedal/actuator gas, brake/iBooster and relay. They require explicit
  bus, counter and engineering/raw targets and reject invalid encoded ranges.
  Disabled requests clear targets. They never access a device.

The code lives in [the car package](../opendbc_repo/opendbc/car/retropilot/).
[Package details](../opendbc_repo/opendbc/car/retropilot/README.md) record the
wire pin, scaling issue and unavailable fields. Existing supported-road-car
rows in CARS.md are intentionally not used to imply driving support.

## Explicit limits

`dashcamOnly=True`, safety model `noOutput`, no longitudinal control, infinite
minimum engagement speeds, zero PID gains and an independently passive
CarController prevent actuation. Its apply method returns zero actuators and
no CAN frames even when CC requests active control. Offline encoders are not
connected to that method. Do not replace this with `allOutput` or assume
Chimera honors modern Panda safety commands; the host emits nothing here.

The 2.7 m / 13:1 geometry is a non-driving mock-style computational placeholder,
not a measured game car or owner's vehicle. The 1 m/s² lateral bound is also
unmeasured; there is no active tune. Actual vehicle geometry, dynamics, actuator
mapping, physical limits and safety policy remain required before control.

Host bus **2** is explicit in the car package. Historical wiring maps it to
MCU CAN3 / connector CAN2; current physical wiring is not established by code.
A future transport must preserve this identity or introduce a reviewed route.

`wheelSpeedFactor=0` intentionally leaves speed unqualified and marks sensors
invalid. In an isolated replay, before constructing CarInterface, set that
CarParams field to **1.0** only for a confirmed km/h producer, or **0.01** for a
confirmed centi-km/h producer. Both multiply the canonical raw CAN_SPEED by
km/h→m/s. The legacy C2 consumer uses 1.0; the saved local Chimera Hall producer
multiplies speed by100. Its CAN-signal configuration/MODE and installed image
are not qualified. No scale is automatically inferred or persistently installed.

Separate wheel speeds and gear are unavailable; gear remains unknown. Cruise
buttons do not establish enabled cruise or set speed. The canonical steering
rate is unsigned magnitude, so it is retained in the parser rather than passed
as a signed rate. Interceptor channels do not establish a calibrated driver
Nm value. Optional SSC status semantics and physical pedal normalization remain
unqualified. Board ignition/health must come from the real transport, not
fabricated pandaStates. Message deadlines are the inherited 20 Hz reference
checks (500 ms expiry), not measured producer rates or source-acquisition age.
Timestamped empty batches are needed to advance parser timeout time.

## Verification

From this repository root:

```bash
.venv/bin/python -m unittest discover -s opendbc_repo/opendbc/can/tests -v
.venv/bin/python -m unittest discover -s opendbc_repo/opendbc/car/retropilot/tests -v
.venv/bin/python Ai/verify_memory.py --workspace /home/radxa/comma
```

Actual receipts are retained in Ai/Evidence. Checks cover source, offline
frames and normal platform selection. No Chimera connection, CAN transmission,
firmware flash, game/model/manager launch or physical actuation was performed.
Next: qualify receive-only Chimera transport and producer units using actual
frames, then integrate the BeamNG telemetry/motion contract and optical shadow.
