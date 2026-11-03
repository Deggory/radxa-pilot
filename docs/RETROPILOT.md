# RetroPilot car platform on Radxa

Implemented 2026-11-03 in the local opendbc branch `radxa/retropilot`, based on
`aa9bff6f5442cef8cb8e25e143ef38865c276ce8`. Sunnypilot now registers
`RETROPILOT_RETROFIT` with brand `retropilot`. This is the **receive-only car-port
stage**, plus an offline modern controller migration, for the owner's BeamNG → Waveshare CAN → Chimera → Radxa architecture.
A standalone receive-only Chimera USB adapter is now implemented. Managed board
health/ignition integration and the live BeamNG loop remain unfinished.

## Active checks implemented, live output still disabled

The [parameterized C safety engine](../opendbc_repo/opendbc/safety/modes/retropilot_active.h)
now checks sensor integrity/freshness, explicit speed/source mode, driver
intervention, button engagement and bounded/rate-limited interceptor steering,
gas and iBooster position commands. It blocks overlapping gas/brake and retains
outstanding commands across faults until a sequential release. Startup needs
one full16-counter disabled cycle for each selected endpoint. Other command
families remain disabled-only. These checks run in compiled native tests using
artificial limits, **not a qualified vehicle calibration**.

No production profile exists and firmware parameters cannot select the native
fixture. Normal mode39 remains disabled-command-only; the car still requests
noOutput and its runtime controller sends no CAN. No Chimera or vehicle action.
See the [active safety report](../Ai/Reports/retropilot-active-safety-20261103/README.md).

## History-led adaptation beyond the car folder

Owner confirmed the existing Radxa Q8B target. The
[full C2 history report](../Ai/Reports/retropilot-c2-history-20261103/README.md)
covers35parent commits, all50final changed paths and64ever-touched paths,
plus Panda/Cereal/opendbc histories. It maps82paths to modern code or an
explicit remaining requirement. It includes USB, schema, joystick/relay,
PID tuning, process startup and Linux changes. Inherited upstream model work
and legacy disabled health/model checks are distinguished from retrofit code.

The current increment adds
[Chimera receive code](../openpilot/selfdrive/pandad/chimera.py) and
[wire/health decoding](../openpilot/selfdrive/pandad/chimera_protocol.py).
It handles the actual mailbox16/health43 contract rather than treating Chimera
as a stock Panda CAN5/CAN6 device. Serial, product and exact version are required.
The reviewed Chimera/ZSS steering source uses STATE1=enabled; our earlier
STATE0 assumption is corrected. Other endpoint STATE0 fault conventions remain
separate. Canonical DBC bytes and the current CD210 model path are unchanged.

## Standalone receive-only Chimera monitor

Inspect arguments without opening USB:

```bash
.venv/bin/python -m openpilot.selfdrive.pandad.chimera --help
```

After identifying the actual Chimera, supply its confirmed serial/version:

```bash
.venv/bin/python -m openpilot.selfdrive.pandad.chimera \
  --serial '<confirmed Chimera serial>' \
  --expected-version '<confirmed firmware version>' --seconds 5
```

Default output is a JSONL receive trace. `--publish-can` additionally owns the
modern Cereal `can` publisher; other CAN publishers must be stopped first. This
is an explicit standalone tool, not an automatic manager replacement. It does
not subscribe to sendcan, send CAN/control-OUT, flash/configure the board or
publish synthetic pandaStates. Health raw safety numbers are retained as raw
observations, never translated into a claim of modern safety enforcement.
Unplug, malformed data or pin mismatch fail closed and release the handle;
publication ends with an invalid empty event. Reconnect requires a new pinned
session. MCU sample timestamps/source ages and managed lifecycle need further work.

The current sysfs observation is bbaa:ddcc product **Interceptor DAC Bench**,
serial440048001251333133333633. It is not the historically probed Chimera.
No device was opened in this increment. The receiver rejects that product even
when VID/PID match; do not aim the tool at the paused Interceptor experiment.

## Safety mode: identifier, configuration and enforcement

Owner excludes relay features; Chimera work is on hold. C2 is reference evidence,
not an integration checklist. This section explains source behavior only.

A safety-mode identifier selects firmware rules for outgoing CAN. It does not
implement those rules or identify the vehicle automatically. In the reviewed
C2 source, car.capnp named retropilot as26; the car interface requested that
mode; Panda registered matching26 with retropilot_hooks. The hooks checked a
transmit allowlist and attempted limited pedal gating. The final policy remained
WIP: RX integrity checking was disabled, reception unconditionally enabled
controls, and calibrated steering/brake bounds were absent.

In current Sunnypilot the standard source path is:
CarParams.safetyConfigs -> pandad/panda_safety.cc -> Panda::set_safety_model ->
board mode selection -> registered opendbc safety hooks -> CAN transmit checks.
The car schema is opendbc_repo/opendbc/car/car.capnp. Safety definitions and
registration are in opendbc_repo/opendbc/safety/declarations.h and safety.h;
board control/CAN code is in panda/board/main_comms.h and drivers/can_common.h.
The schema now uses26 for hongqi and firmware constants call26 SAFETY_FAW;
C2's26 is occupied, not a reusable RetroPilot assignment.

Our RetroPilot interface currently requests existing noOutput and dashcamOnly.
Current noOutput has no allowed outgoing messages and its TX hook rejects output
(opendbc/safety/modes/defaults.h). The controller also returns no live CAN frames.
These are current source settings, not proof of installed hardware behavior.
The new `retropilot @39` identifier and restricted firmware-source policy are
now registered. The policy accepts only seven canonical disabled commands on
hostbus2, with exact DLC, CRC and zero engineering targets. Active modes,
nonzero targets, reserved bits, relays, unknown parameters and CAN forwarding
are blocked. The car interface continues to request noOutput.

This is a tested disabled-command-only policy, not a qualified active-control
policy. No physical limits are invented from DBC signal ranges or C2 constants.
Active control still requires a measured profile and driver limits, incoming
message integrity/freshness and engagement/disengagement requirements. No
firmware image was flashed or mode sent to hardware; Chimera remains held.

## Files, identification and safety status

Comma's [current port structure](https://github.com/commaai/opendbc/blob/master/README.md#structure-of-a-port)
places the host car package in opendbc/car. Our pinned implementation is in
`opendbc_repo/opendbc/car/retropilot/`:

| Component | Current RetroPilot status |
| --- | --- |
| `values.py` | Platform, bus and observed-module flags registered; physical parameters remain non-driving placeholders. |
| `interface.py` | Modern parameter and parser/controller wiring; explicit selection, dashcamOnly and noOutput. |
| `carstate.py` | Existing canonical signals parsed with validity checks; missing gear/wheels and unqualified speed remain explicit. |
| `carcontroller.py` | Modern steering/pedal/relay calculation and candidate CAN in explicit offline preview; runtime still returns zero actual actuators and no transmitted frames. |
| `retropilotcan.py` / `commands.py` | Canonical CRC and eight offline command constructors, used by the controller preview. |
| `profiles.py` / `replay.py` | Validated explicit calibration, labelled C2 reference and parser-to-controller JSONL replay; no hardware transport. |
| `fingerprints.py` | C2-name compatibility and an explicitly empty automatic CAN database. Both old/new names select the modern platform; no ECU firmware versions are asserted. |
| `radar_interface.py` | No radar-specific implementation; inherited base interface with radarUnavailable. |
| `opendbc/dbc/ocelot_controls.dbc` | Packaged canonical DBC; existing wire bytes unchanged. |
| `opendbc/safety/modes/retropilot.h` | Registered as mode39: disabled-command-only policy with exact bus/DLC, CRC and zero-target checks. Active commands and relays blocked; interface stays noOutput. |
| `opendbc/safety/tests/test_retropilot.py` | Compiled C-policy tests, including debug/release builds, payload mutation, malformed frames, unknown parameters and forwarding. No installed-board qualification. |

Paths beginning with `opendbc/` in this table are relative to opendbc_repo;
both RetroPilot safety paths now exist and are covered by compiled software tests.
For comparison, this pinned tree uses `opendbc/safety/modes/hyundai.h`,
`hyundai_canfd.h` and `opendbc/safety/tests/test_hyundai*.py`.

The platform name selects the parser/profile. Observed CAN ID/DLC flags identify
module presence only. Chimera USB identity identifies the interface board;
none of these establishes the selected BeamNG car, vehicle geometry, actuator
calibration or firmware compatibility. Future automatic identification needs
measured ECU/module identities or a qualified CAN signature. There is no reason
to populate fingerprints.py with invented ECU versions for the present explicit
simulator selection.

## C2 controller migration, 2026-11-03

Checked the [linked C2 directory](https://github.com/RetroPilot/retropilot/tree/b9a942efd3cb210127bb5efb5cf9ccf6a811c728/selfdrive/car/retropilot)
through GitHub: branch c2 still resolves to b9a942efd3cb210127bb5efb5cf9ccf6a811c728.
All eight retained file Git blobs match. The previous11-line controller was a
receive-only placeholder; modern API differences alone did not justify leaving
its control calculation missing. The calculation is now implemented and tested
offline, with the following explicit disposition of every C2 file:

| C2 file | Modern disposition |
| --- | --- |
| `__init__.py` | Standard Python package, unchanged. |
| `carcontroller.py` | Modern torque/accel requests; separate lat/long gating, speed taper, count slew, pedal mapping,100/50Hz scheduling and per-message counters. Candidate feedback stays separate from actual zero output. |
| `ocelotcan.py` | Canonical `commands.py`; profiles hold explicit channel centers/slopes and brake travel. Hostbus2 is an intentional adaptation of C2's bus0. |
| `carstate.py` | Modern parser dictionaries and button events; accepted CAN timestamps feed preview freshness. No forced drive gear or fabricated engaged state. |
| `interface.py` | Modern parameter/state/controller wiring; normal CAN validity. Firmware safety and measured dynamics remain required for live control. |
| `values.py` | Registered platform, per-instance observed modules and explicit routing; no global enabled ECU defaults. |
| `tunes.py` | C2 PID_A uses kp=.05, ki=.05, kf=.00003; PEDAL/ACTUATOR long tunes are vehicle-specific reference data. They are not selected for an unmeasured vehicle; current live gains remain zero. |
| `radar_interface.py` | C2 forcibly set no_radar=True. Current radarUnavailable/base interface preserves that behavior without copying an unused Toyota radar parser. |

Fixed C2's disabled-steering calculation, single-active-flag coupling, negative
speed taper above90m/s, gas/brake handoff and copied-request feedback. C2's
Toyota-style measured-torque limiter depended on an unqualified conversion of
Interceptor channels into EPS torque; it is not represented as a calibrated
physical limit here. Actual feedback calibration/safety remains unfinished.

See the [package replay command and input contract](../opendbc_repo/opendbc/car/retropilot/README.md#offline-controller-replay).
The C2 reference constants must be explicitly selected for offline evaluation.
The owner's Core source rejects a channel difference over400; the C2 profile
can reach700. Runtime transmission remains blocked independently of profiles.
A complete live port still needs Chimera transport/health/safety, selected
vehicle dynamics and calibrated actuator/driver-input mappings. No game or
hardware was operated to validate this migration.

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
no CAN frames even when CC requests active control. The method records
`last_preview` candidates only when an explicit offline profile is supplied. Do not replace this with `allOutput` or assume
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
