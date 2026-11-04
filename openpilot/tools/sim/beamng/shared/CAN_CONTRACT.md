# RP-SIM-1: BeamNG telemetry on the shared RetroPilot CAN interface

Implemented 2026-11-04. Canonical file remains
`retropilot/dbc/ocelot_controls.dbc` in the Comma workspace; the matching packaged
copy is inside Sunnypilot's `opendbc_repo/opendbc/dbc/`. [Version/hash](dbc-version.json).
The original 7,363-byte / 20-message C2 DBC is preserved as
`retropilot/dbc/reference/ocelot_controls.c2.dbc`. Its existing layouts are
unchanged; eight simulator-only messages are appended. Legacy physical
producers can keep using their existing messages. No firmware was updated.

## Data and units

| CAN ID | Message | Meaning for this explicitly selected simulator profile |
| --- | --- | --- |
| 0x050 | STEER_ANGLE_SENSOR | Measured BeamNG steering-wheel angle, signed0.1degree; unsigned rate magnitude in degree/s; STATE1. Input steering is not substituted for feedback. Source sign is retained until controlled left/right verification. |
| 0x075 | ENGINE | Actual ignitionLevel>0, driver brake_input>0.05, RPM if available. MODE1; pulse fields unused. |
| 0x076 | SPEED | CAN_SPEED is **centi-km/h**: round(abs(wheelspeed_mps)*360). MODE1. This convention is specific to RP-SIM-1, not a change to legacy physical producers. |
| 0x100 | CRUISE | Existing button bits/counter/CRC. Button availability is independently flagged. No generic button API was evidenced, so the current Lua source reports buttons unavailable and sends zero bits. |
| 0x700 | SIM_SAMPLE_BEGIN | CRC, counter4, protocol version4=1, session16, sample16, flags8, group validity8. |
| 0x701 | SIM_CLOCK | CRC/counter, accumulated simulation milliseconds32, sample16. Simulation time must advance; paused data is rejected. |
| 0x702 | SIM_ACCEL | CRC/counter, validity, signed XYZ16 at0.01m/s². |
| 0x703 | SIM_GYRO | CRC/counter, validity, signed XYZ16 at0.001rad/s. |
| 0x704 | SIM_WHEEL_SPEEDS | CRC/counter, four validity bits, FL/FR/RL/RR unsigned12 at0.05m/s. Each is abs(its angular velocity)*its own nominal radius. Missing wheel/radius invalidates all four; no scalar-speed copies. |
| 0x705 | SIM_INPUTS | CRC/counter; throttle_input, brake_input and applied brake separately at1/255; signed engaged gear index; validity mask; ignition, RPM validity, rate validity. Gear index is not an asserted P/R/N/D selector. |
| 0x706 | SIM_CRUISE_STATUS | CRC/counter, valid/available/enabled/set-valid, set speed at0.01m/s. Read-only getConfiguration(), when the extension exists. This is game cruise, not Sunnypilot engagement. |
| 0x707 | SIM_SAMPLE_END | Same metadata as BEGIN; completes a coherent sample. |

The RP-SIM-1 BEGIN/END group validity bits0..7 mean speed,angle,ignition,
inputs,acceleration,gyro,wheels,cruise. Flags bit0=active source,bit1=buttons
available,bit2=angle-rate available. SIM_INPUTS validity bits0..3 mean
throttle,driver brake,applied brake,engaged gear. Unknown fields remain
unavailable in the decoder; zero placeholder bytes never assert validity.
Every frame has CRC-8/SAE-J1850, init/final XOR0xFF, polynomial0x1D,
covering **all payload bytes except byte0**, as in the legacy shared protocol.
All frames in a sample use counter=(sample &15). CRC does not include the ID.
The legacy CRUISE ADC fields overlap counter/mode; this adapter leaves the
ADC fields zero and does not change that historical layout.

## Timing, grouping and routing

One producer: PC game protocol -> PC-loopback UDP49160 -> gateway -> Waveshare
CH340/2Mbaud8N1 variable AA55 framing -> isolated500kbit/s classical CAN ->
Chimera. The selected host route is bus2 (historical MCU CAN3/connector CAN2);
actual Chimera revision/cabling still needs confirmation. No real actuator,
Interceptor, ZSS or other publisher may compete for these IDs on the sim bus.
Physical actuator/control messages, including relays, are never emitted by
this telemetry gateway. It does not fabricate Chimera health or ignition pins.

Nominal50Hz,12frames/sample:600frames/s, conservatively under17% of500kbit/s
using135bits/frame; actual scheduling/delivery remains to be measured. BEGIN
is submitted first and END last. The receiver requires all12 unique IDs,
matching counters, matching BEGIN/END, correct CRC/DLC, source-clock/sample
agreement and the selected bus. Missing/reordered-across-boundary groups are
rejected rather than combined. A group must complete within100ms. Current
telemetry expires150ms after the last completed group; duplicates do not
refresh it. CAN sample16 wraps modulo65536. Sessions reset the assembly state;
64 retired sessions are remembered. These identifiers are not authentication.

PC-local UDP uses a128-byte little-endian FFI record: RPT1,session32,
wall-time64,sim-time64,sequence32,validity32,22float32 values,buttons32 and4
trailing alignment bytes. The source validity bits0..13 are speed,angle,
ignition,RPM,throttle,driver brake,applied brake,gear,accel,gyro,wheels,cruise,
buttons,rate. The gateway checks packet size/version, values/ranges, increasing
sequence and simulation time, and source wall-age <=150ms (future tolerance
50ms) on the **same PC**. Source silence, pause, reset, malformed data and
process exit cannot cause repeated last-known CAN state. Serial writes have
a50ms bound; a failed/partial write terminates transmission. No electrical
ACK/delivery proof is inferred from a successful serial write.

## IMU scope

The Lua producer follows the installed `protocols.lua`/`motionSim.lua` component
convention: acceleration=-ffiSensors.sensorX/Y/Z, gravity excluded;
angular velocity=obj:getRollPitchYawAngularVelocity(),rad/s. It uses sensorZ,
not sensorZnonInertial. Components are unsmoothed at the simulation reference
sensor origin. Raw components are labelled as BeamNG motionSim convention.
Steering sign and physical/device-frame axes/origin have **not** been qualified
by this implementation. Do not publish these as physical Q8B IMU measurements
or feed them to locationd until a measured transform/provider is selected.
The stationary physical LSM6DS3TR-C must not compete with a simulated provider.

## Implementation and verification boundaries

The independent PC cantools encoder and Radxa opendbc decoder are tested
against each other. `RETROPILOT_BEAMNG` explicitly selects the centi-km/h
receive-only profile, wheel/pedal/cruise mapping and sample integrity checks.
Generic `RETROPILOT_RETROFIT` retains its unqualified speed factor and behavior.
Both profiles keep noOutput,carNotReady,dashcamOnly and an empty runtime TX
list. IMU remains decoded telemetry, not an automatically enabled motion service.
Camera/Thneed/model paths and Panda/Chimera firmware are unchanged.

Sources: [BeamNG protocol API](https://documentation.beamng.com/modding/protocols/),
installed game Lua source hashes in the dated evidence receipt, canonical
RetroPilot/opendbc6b90fafe and existing `canreader/read_can.py` / attributed
Waveshare framing evidence. Current app/firmware/wiring acceptance and simulator
control are separate future work; passing CPU fixtures is not a live HIL test.
