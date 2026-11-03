# RetroPilot car platform on Radxa

Implemented 2026-11-03 in the local opendbc branch `radxa/retropilot`, based on
`aa9bff6f5442cef8cb8e25e143ef38865c276ce8`. Sunnypilot now registers
`RETROPILOT_RETROFIT` with brand `retropilot`. This is the **receive-only car-port
stage** for the owner's BeamNG → Waveshare CAN → Chimera → Radxa architecture.
The Chimera USB backend and live BeamNG loop remain separate unfinished work.

## Files, identification and safety status

Comma's [current port structure](https://github.com/commaai/opendbc/blob/master/README.md#structure-of-a-port)
places the host car package in opendbc/car. Our pinned implementation is in
`opendbc_repo/opendbc/car/retropilot/`:

| Component | Current RetroPilot status |
| --- | --- |
| `values.py` | Platform, bus and observed-module flags registered; physical parameters remain non-driving placeholders. |
| `interface.py` | Modern parameter and parser/controller wiring; explicit selection, dashcamOnly and noOutput. |
| `carstate.py` | Existing canonical signals parsed with validity checks; missing gear/wheels and unqualified speed remain explicit. |
| `carcontroller.py` | Implemented passive stage: always returns zero actuators and no CAN frames. Active control mapping is pending. |
| `retropilotcan.py` / `commands.py` | Canonical CRC and offline command constructors; no calibrated normalized-control-to-actuator mapping. |
| `fingerprints.py` | C2-name compatibility and an explicitly empty automatic CAN database. Both old/new names select the modern platform; no ECU firmware versions are asserted. |
| `radar_interface.py` | No radar-specific implementation; inherited base interface with radarUnavailable. |
| `opendbc/dbc/ocelot_controls.dbc` | Packaged canonical DBC; existing wire bytes unchanged. |
| `opendbc/safety/modes/retropilot.h` | Not implemented. A future policy needs registration in the modern safety dispatcher and schema plus compiled safety tests. |
| `opendbc/safety/tests/test_retropilot.py` | Not implemented. Existing host/codec tests do not qualify firmware safety enforcement. |

Paths beginning with `opendbc/` in this table are relative to opendbc_repo;
the two RetroPilot safety paths are planned locations, not existing files.
For comparison, this pinned tree uses `opendbc/safety/modes/hyundai.h`,
`hyundai_canfd.h` and `opendbc/safety/tests/test_hyundai*.py`.

The platform name selects the parser/profile. Observed CAN ID/DLC flags identify
module presence only. Chimera USB identity identifies the interface board;
none of these establishes the selected BeamNG car, vehicle geometry, actuator
calibration or firmware compatibility. Future automatic identification needs
measured ECU/module identities or a qualified CAN signature. There is no reason
to populate fingerprints.py with invented ECU versions for the present explicit
simulator selection.

## How C2 selection maps to this version

The retained C2 source (RetroPilot/openpilot b9a942ef) did not rely on its CAN
fingerprint to identify the retrofit. `car/retropilot/values.py` defined a
placeholder fingerprint containing IDs0..15/DLC8, while
`selection/car_helpers.py` hard-coded `fixed_fingerprint = "RETROPILOT RETROFIT"`
and `skip_fw_query = True`. The fixed name overrode the matcher result.

The modern equivalent keeps selection explicit:

| C2 mechanism | Current implementation |
| --- | --- |
| `CAR.RETROFIT = "RETROPILOT RETROFIT"` | `CAR.RETROPILOT_RETROFIT` in the modern platform registry. |
| Placeholder IDs0..15 in values.py | `retropilot/fingerprints.py` declares `FINGERPRINTS = {}`; no unmeasured automatic signature is installed. |
| Forced old name in car_helpers | Explicit old/new names are normalized before selection and the no-diagnostic guard; other vehicles remain selectable. |
| Old platform names in saved configuration | RetroPilot's alias is merged into shared `car/fingerprints.py:MIGRATION`, used by Sunnypilot's existing CarPlatformBundle migration. |
| Unconditional firmware-query bypass | Query bypass is scoped to explicit RetroPilot selection. No FW_VERSIONS/FW_QUERY_CONFIG is registered for unknown modules. |

Both `RETROPILOT RETROFIT` and `RETROPILOT_RETROFIT` work through the fixed
argument or FINGERPRINT environment variable. Tests use synthetic CAN and a
temporary Params directory; no owner's saved selection was changed. Hostbus2,
passive output, unqualified speed and vehicle/safety limits remain unchanged.
The shared file now contains the RetroPilot migration entry. It still has no
RetroPilot automatic CAN/ECU matching entry. Adding a filename or name alias
does not establish identification of a physical vehicle or installed firmware.

The historical teacher reference `retropilot/safety/safety_retropilot.h` is WIP:
it allows controls on arbitrary reception, disables receive-integrity checks,
lacks steering/brake limits and contains DLC mismatches. It remains reference
evidence. A modern safety file must also be enforced in Chimera's actual TX path;
adding it to host opendbc does not install or activate it on that custom board.
The existing noOutput setting is a host-requested policy; the unconditional
empty output from CarController is the current local enforcement. No claim is
made that installed Chimera firmware implements the modern policy.

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
