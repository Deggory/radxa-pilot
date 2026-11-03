# RetroPilot retrofit platform

`CAR.RETROPILOT_RETROFIT` is an explicitly selected **receive-only** platform.
`CarInterface`/`CarState` use the modern Sunnypilot opendbc API; `CarController`
returns zero actuators and no outgoing frames unconditionally. This is a
functional monitoring stage, not a qualified active controller. Offline
`commands.py` implements the eight canonical command IDs for later adapter
verification, with explicit raw/physical targets and no legacy calibration law.
Its checks enforce encoded bit ranges, not qualified physical actuator limits.

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
