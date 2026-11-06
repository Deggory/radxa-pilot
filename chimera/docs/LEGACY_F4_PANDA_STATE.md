# Offline legacy F4 PandaState conversion

November6,2026 — T08b2b. Baseline `faf1f8140fab872ee20225813e17e8d724ea8e7a`.

[panda_state_legacy.h](../../openpilot/selfdrive/pandad/panda_state_legacy.h) and
[implementation](../../openpilot/selfdrive/pandad/panda_state_legacy.cc) convert
an already decoded legacy F4 health17/CAN-health5 sample into an offline Cereal
PandaState preview. They do not connect to any publisher or transport. The linked
managed pandad binary does not reference the converter.

## Qualification and validity

The caller supplies LEGACY_F4_V17, hardware1/2/3/5/6, a complete typed status sample
and nonzero host timestamp. The caller is responsible for the existing pinned
identity and exact-read qualification; passing an enum is not authentication.
All validation happens before the builder is initialized. Failure returns a typed
LegacyF4StateError and leaves the builder untouched. Success returns NONE and
constructs exactly one PandaState with **Event.valid=false**, unconditionally.
Use a fresh MessageBuilder. Allocation/serialization exceptions may propagate.

This invalid Event is deliberate: six current fields have no compatible legacy
measurement, and normal consumers/admission are not yet qualified. Raw ignition
and controls flags are preserved as firmware reports, never operational permission.
No firmware safety mode, relay, bus speed or heartbeat is changed. No current
health49 cast, packed-struct reinterpretation or SPI fallback is involved.

## Mapping and unsupported fields

| Source | Preview behavior |
| --- | --- |
| Voltage/current and counters | Preserve full UInt32 width, no current-health UInt16 truncation |
| Interrupt load | Preserve finite nonnegative Float32, including fractions and values above1; no divide-by255 |
| SBU1/SBU2 millivolts | Convert to current Cereal volts using float division by1000 |
| Ignition, controls, power-save, heartbeat and RX-check flags | Preserve reported booleans, while keeping Event.valid=false |
| Harness/fault status | Exact validated0/1/2 to current matching enums; other values rejected |
| Safety model |26explicit name-matched source IDs; conflicting25/26 and all other unsupported IDs rejected |
| Fault bitmap | Preserve every set bit0..26; any bit27..31 rejects the whole preview |
| alternativeExperience | Preserve0..32767;32768..65535 rejected instead of becoming negative Int16 |
| Controllers | Validate selectors0/1/2 in order, then preserve all25current CAN-state fields and validated LEC0..7 |

These six active current fields remain **unavailable**: spiErrorCount,
soundOutputLevel, controlsAllowedLateral, controlsAllowedLongitudinal, nmiReset,
hardfaultReset. The header exposes their names explicitly. Their serialized
zero/false placeholders are not measurements, and that availability list is not
embedded in Cereal. A preview must not be published as ordinary operational
status or made valid. All33active PandaState fields are accounted for as24mapped
fields,3controller structs and6unavailable fields; deprecated fields are excluded.

Keep complete raw samples in the existing isolated JSON diagnostics. Those retain
legacy-only wake_on_can, fan_stall_count, som_reset_triggered and
spi_checksum_error_count; a checksum-specific count is not the broader current
SPI error count. Per-controller total_tx_checksum_error_cnt has no current
PandaCanState field and remains diagnostic-only. Selector identity is represented
by controller position, not proof of physical bus routing or FD capability.
The canonical RetroPilot DBC and host bus identities are unchanged.

## Source evidence and conflicts

[Reference files and licenses](../reference/carrot-f4-state-v17/README.md) pin
Carrot69a2d3be definitions. The original producer/health layout was already pinned
in [health evidence](LEGACY_F4_HEALTH.md). Current schema is this project's
log.capnp and opendbc150f9371 car.capnp/declarations; Panda remains8a16e089.

Legacy safety25 is STELLANTIS and26 is FAW; current schema calls them
volkswagenMlb/hongqi. Numeric equality cannot establish the same meaning.
The other26matched names are display mappings, not claims of matching safety
algorithms, parameters or actuation support. Source IDs may be declared without
being registered for a particular build.

Legacy fault27 is SOUND_DMA, absent from the current Cereal fault enum. Current
Panda also defines it; this is a schema limit shared with that path. Existing
managed fault-list code allocates from all set bits but fills only0..26, a separate
source-level risk retained for later review; this slice does not change it.
The converter rejects unrepresentable faults instead of dropping or inventing
entries. Unknown raw values remain available through isolated diagnostics.

## Verification and remaining work

Native target and10native programs pass, including the new converter fixture.
It checks every16-bit alternative mask, all256safety and hardware bytes,32fault
bits, invalid enum/load/selector/LEC inputs, full-width values, all25controller
fields, empty fault lists, unit conversion and no builder mutation on rejection.
ASan/UBSan covers the new converter/test; linked support libraries are existing
unsanitized builds. No SPI/USB source is linked into that fixture. A temporary
mutation making the Event valid fails the test.41Python tests pass with warnings
as errors, including4new source/enum/coverage/provenance checks plus existing
ignition/USB/Chimera/Thneed tests. A native serialized preview read by Python has
raw ignition/controls=true but is denied ignition by the hardwared reducer.
No live PubMaster/SubMaster/hardware_thread or device is run.

[Receipt](../../Ai/Evidence/chimera-legacy-state-20261106.json) pins source/artifact
hashes and actual commands/results. Firmware sources/image, Ocelot/archive/DBC,
camera/model/Thneed, runtime startup/transport and the ignition gate are unchanged.
No physical USB, flash/reset/config/relay/CAN TX/upstream update/push action occurred.

Next T08b2c: define/test ordinary PandaState admission with explicit supported-field
metadata and review all consumers before wiring a publisher. Keep this preview
invalid. Reconnect/backoff, other profiles, operational Chimera firmware and
power/VBUS/recovery/bench qualification remain separate outstanding work.
