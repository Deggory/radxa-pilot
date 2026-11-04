## RP-SIM-1 receive-only simulator profile — 2026-11-04

Explicit RETROPILOT_BEAMNG selection decodes coherent simulation samples,
centi-km/h speed,wheels,pedals and observed cruise status. It keeps noOutput,
dashcamOnly,carNotReady and empty runtime controller TX. The physical
RETROPILOT_RETROFIT profile keeps its previous behavior and unqualified speed
factor. No automatic identification,measured vehicle tune or live safety claim.

Canonical ocelot_controls.dbc now appends eight RP-SIM-1 messages0x700..0x707;
all original20message definitions are unchanged. Current/parent hashes and
provenance are in SOURCES.json. SimulationReceiver exposes decoded motion
components with an explicit unqualified BeamNG frame label; no localization
or physical sensor provider is enabled. The parent Sunnypilot project's
openpilot/tools/sim/beamng/shared/CAN_CONTRACT.md defines timing,masks and routing.
Actual game/CAN/firmware acceptance remains separate.

# RetroPilot retrofit platform

`CAR.RETROPILOT_RETROFIT` is an explicitly selected **receive-only** platform.
`CarInterface`/`CarState` use the modern Sunnypilot opendbc API; `CarController`
returns zero actual actuators and no outgoing frames unconditionally. Its
`preview()` now migrates C2's steering/pedal/relay calculation to modern requests
and generates candidate CAN with an explicit `ControllerProfile`. The default
profile is absent. `C2_REFERENCE` is available only through explicit offline
selection; it is not an owner/BeamNG calibration or a qualified active port.
`commands.py` implements all eight canonical command IDs for adapter verification.
Its checks enforce encoded bit ranges, not qualified physical actuator limits.

## Registered safety policy: disabled commands only

`CarParams.SafetyModel.retropilot` is registered as39 in modern opendbc, with
C rules in `safety/modes/retropilot.h` and compiled tests in
`safety/tests/test_retropilot.py`. Existing identifiers, including26, retain
their meanings. Cereal already imports this schema; its source is unchanged.

This policy accepts only canonical disabled steering, gas and brake commands
on explicit hostbus2. It checks address/DLC, CRC8J1850, disabled mode/ENABLE,
zero engineering targets and reserved bits. Brake zero is offset encoded:
relative raw0x7e00 and position raw0x0140. All16counter values are allowed;
this is not TX freshness or replay protection. FD/extended/returned/rejected
packets, unknown parameters and RelayCore commands are blocked. No RX message
enables controls, and there is no forwarding. Incoming data is not qualified
by this passive policy, and no physical actuator limit is inferred from a DBC.

**The car interface still requests noOutput**, and runtime controller output
remains zero. Registration is not permission to activate this policy on a board.
The software-only policy is deliberately limited until a vehicle profile,
measured command/driver limits, RX freshness and engagement/disengagement rules
are qualified. Chimera work is held; relays are excluded from requested work.
No firmware image was flashed or hardware mode changed.

## Active safety engine: native tests only

`safety/modes/retropilot_active.h` adds profile-dependent RX CRC/counter/
quality/freshness, explicit speed units/source mode, ignition/pedal/steering
intervention, button-edge engagement and steering/gas/position-brake limits.
It covers interceptor steering0x300, gas0x200 and iBooster position0x20E.
Other endpoint families remain disabled-only; relays remain blocked.

No production initializer supplies an active profile. Firmware mode parameters
cannot select one. The only supplied calibration is an artificial native-test
fixture in tests/libsafety/safety.c under ALLOW_DEBUG; the setter is absent from
release builds. ControllerProfile/C2_REFERENCE is not this safety profile.

The engine checks channel agreement, steering slew/250ms change/speed taper,
pedal slew/range, gas/brake exclusion, command timing and sequential counters.
It requires one full16-counter disabled cycle per selected axis before engagement;
this models endpoint counter synchronization, not receipt acknowledgement.
Out-of-sequence disabled packets are blocked when an active profile exists,
because an endpoint can ignore their target while updating its counter. Invalid
RX latches private disengagement even if the shared controls flag is forced.
Faults retain outstanding command state until a permitted sequential release.

The canonical DBC defines encoding, not safe physical values. Producer/firmware
compatibility, real driver authority and vehicle calibration remain unqualified.
In particular local legacy firmware has CRC/layout/speed/mode discrepancies.
This engine does not make Chimera enforce the policy or enable vehicle output.

## Offline controller replay

From the Sunnypilot root:

```bash
.venv/bin/python -m opendbc.car.retropilot.replay \
  --profile c2-reference --speed-units kph < recording.jsonl > candidates.jsonl
```

Each JSONL row contains `timestamp_nanos`, `can` triples `[address, "hex", bus]`
and `control` using this checkout's CarControl schema (`enabled`, `latActive`,
`longActive`, `actuators.torque`, `actuators.accel`). Supply rows at100Hz and
all required base/selected-module status frames on hostbus2 with valid integrity.
Empty CAN rows advance time. Outputs distinguish candidate CAN/actuators from
actual zero feedback and empty transmitted CAN. This tool never opens hardware.

Steering and position brake candidates run100Hz; gas/relay50Hz. Disabled gas
and relay flush on the next step even between normal sends. Steering resets
immediately on disable/override/fault; speed taper is clamped at zero. Gas and
brake have separate acceleration calibration scales and cannot overlap. Modern
lateral/longitudinal activation is independent. Counters increment per emitted
message and wrap at16; canonical CRC/DLC and hostbus2 remain unchanged.

Preview blocks invalid requests, missing endpoints, ignition loss and stale CAN.
Its100ms cutoff measures the oldest accepted tracked CAN arrival; empty, bad-CRC
or unrelated packets cannot refresh it. Non-monotonic steps and gaps over50ms
disable candidates and clear steering/pedals. These are offline evaluation
limits, not measured source-acquisition deadlines or installed MCU watchdogs.

C2's1510-center/350-count steering, pedal slopes and7mm iBooster travel are
historical reference values. The350-count limit creates a700-count channel
difference, exceeding the local Core source's400-count check. No calibrated
driver-torque-to-counts feedback limit, driver-pedal authority, physical tune or
live Chimera safety policy is supplied by this reference profile. Actuator/SSC
steering has codecs but no normalized-control mapping, just as C2's commented
controller paths did not implement them. Unsupported profile endpoints fail.

## Provenance and routing

Canonical DBC: RetroPilot/opendbc6b90fafe59e81822bfae58e4ecb080248e9de40d,
SHA-256ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
`SOURCES.json` records provenance; REFERENCE_LICENSE preserves its MIT license.
The DBC is packaged in opendbc/dbc/ocelot_controls.dbc with unchanged bytes.
CRC-8 SAE-J1850: poly0x1D, init0xFF, xorout0xFF, bytes1..DLC-1; counter4bits.
All eight bytes of 0x301 are covered. Older partial-CRC firmware is incompatible.

Host bus2 is explicit (historical MCU CAN3 / connector CAN2). Actual wiring and
installed firmware remain unverified. No automatic bus reassignment or ECU
calibration follows from seeing a message ID. Optional flags record exact
ID/DLC observation on bus2; required parser checks include those observed modules.
Modern Chimera USB/health/safety compatibility is a separate backend task.

## Deliberately unavailable

The reviewed Chimera TIM3 producer and shared ZSSv0.2.0 encode angle STATE1
as enabled/valid; STATE0 is disabled. CarState requires exactly1 for this source
contract, rejecting other nibble values. This is separate from actuator status
STATE0=healthy. The DBC has no named angle-state enum; its bytes are unchanged.

Speed scale starts at0 and `vehicleSensorsInvalid=True`. Set
`CP.wheelSpeedFactor` before interface construction to1.0 for a confirmed km/h
producer, or0.01 for confirmed centi-km/h, in an isolated replay. Raw speed is
then multiplied by that factor and km/h→m/s. The old C2 consumer and saved local
Chimera Hall producer disagree by100×; MODE does not resolve installed behavior.
No automatic scale inference, guessed four-wheel speeds or drive gear is used.

Wheelbase2.7m/steerRatio13 and lateral bound1m/s² are non-driving computational
placeholders, not vehicle measurements. No fitted endpoint, tune or physical
calibration is claimed. Steering-rate magnitude stays raw because the modern
field needs direction. Interceptor channels stay raw without a Nm conversion.
Gear, pedal normalization, cruise-enabled/set-speed and simulated motion need
further agreed definitions. Cruise ON only changes a local available indicator;
there is no fake engaged state. Stale/missing input, fault, brake, cancel or
ignition loss prevent that indicator. CAN checks are reference20Hz/500ms,
not verified source freshness; callers supply monotonic timestamped batches,
including empty batches to advance timeouts.

The new fingerprints.py declares an empty automatic CAN database and maps
C2's "RETROPILOT RETROFIT" to RETROPILOT_RETROFIT. The alias is included in
shared car/fingerprints.py:MIGRATION and normalized for explicit arguments or
FINGERPRINT environment selection. Saved CarPlatformBundle names use the
existing Sunnypilot migration. No ECU FW database/query configuration is
registered. C2 hard-coded the old name and bypassed FW queries; its IDs0..15
fingerprint was a placeholder. No global override is carried into this port.

Select through the fixed-platform path; no automatic matching is added.
Explicit RetroPilot selection skips VIN/FW diagnostic TX. Other brands are
unchanged. No hardware is opened by this package or its tests.
