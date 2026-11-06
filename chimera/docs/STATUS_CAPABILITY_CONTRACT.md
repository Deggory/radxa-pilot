# Bootstrap status and capability contract

November 6, 2026 — T05a. The existing A0 manifest and D6 version are the only
implemented vendor replies. This slice adds a [pure host decoder](../../openpilot/selfdrive/pandad/chimera_identity.py)
and firmware-response fixtures. No new USB request, operational health packet
or managed host profile is added. [Identity bytes](USB_IDENTITY_CONTRACT.md)
and the7448-byte ARM image remain unchanged.

## Discovery contract

`decode_bootstrap_identity(manifest, version)` takes complete immutable response
bytes. It requires manifest32, exact D6 `chimera-f413-bootstrap-v1`, magic CHMR,
schema1, length32, local family1 and phase0. Operational capabilities, both active
layout hashes, automatic update and configuration ABI must all be0. All six
reserved bytes must be0. It requires the source-defined topology: three classical
buses, maximum payload8 and physical interface mask0x01FF.

Unsupported combinations raise ValueError; non-bytes arguments raise TypeError.
Future phases, capability bits and hashes need a separately reviewed decoder/
profile change. No bit currently authorizes an operation. There is no fallback
to old Chimera or Panda decoding. The immutable result reports version, topology,
physical interface names and zero operational capability/hash fields. Physical
names mean source-defined connections, not sampled values or proven electrical
behavior. No ignition, measurement, controls-allowed or ready flag is invented.

This function performs no device access. Descriptor VID/PID/product, requested
serial pin, handle serial and transport ownership remain the future caller's
responsibility. Successful decoding is neither authentication nor permission for
managed use. The existing native identifier still rejects this bootstrap because
C1 is unavailable. Startup stays SPI; original mailbox16/health43 stays separate.

## Health requires implemented producers

Current Panda health is49bytes, distinct from old Chimera43 and legacy F4v17's59.
`fill_panda_state` and `send_panda_states` in [pandad.cc](../../openpilot/selfdrive/pandad/pandad.cc)
consume its fields directly and can issue power-save/safety requests after reading
ignition and safety mode. A plausible zero-filled reply would create behavior and
misleading measurements. D2 and per-bus C2 therefore remain STALL.

| Current Panda fields | Bootstrap truth | Before operational publication |
| --- | --- | --- |
| uptime | No operational timebase/service loop | Monotonic MCU time with defined reset/wrap behavior |
| voltage/current, SBU voltages, temperature | No qualified producer | Actual circuits, units, calibration and validity; SBU fields cannot silently become ADC1/ADC2 |
| ignition line / CAN | No sampled/qualified ignition | Acquire chosen source with polarity, integrity, freshness and fault handling |
| controls allowed, lateral/longitudinal flags, safety mode/parameter, alternative experience | No active MCU policy | Implement policy on every outgoing path; reporting a mode cannot enforce it |
| blocked TX, invalid RX, overflows, faults/status | No operational counters/monitor | Zero must mean observed none, not unimplemented |
| heartbeat lost, RX checks invalid, power save | Services unimplemented | Define loss/fault transitions, timing and physical effects |
| harness/relay status | PB0 source known; contacts/effect unqualified | Distinguish command, contact and bypass behavior; no borrowed stock harness semantics |
| NMI/hardfault/reset flags | Only raw reset/option helper | Establish bootstub flag clearing/preservation and reset provenance |
| interrupt load, fan, SPI errors, sound | No corresponding producers | Explicit unsupported semantics in host profile; no invented measured zero |
| per-bus CAN health | Controllers unbound | Classical counters/bus state, three-bus routing and unsupported CAN-FD fields |

Native health49 has no per-field validity mask. A future Chimera profile must
handle unavailable fields and communication failure before these consumers.
This slice chooses no new health layout and overloads no current field. Failed,
short or unqualified responses must not refresh prior state or be replaced with
healthy defaults. Freshness/reconnect belongs to future managed lifecycle work.

Local detached-service phase/error/cleanup and raw UID/reset/options are C-memory
diagnostics, not USB health. Cleanup readback proves neither physical cutoff nor
vehicle recovery. Main still has no service instance, attachment or CAN activity.
[Power/recovery requirements](USB_STARTUP_REQUIREMENTS.md) remain in force.

## Evidence and verification

The fixture compiles actual `protocol.c` with ASan/UBSan, obtains A0/D6 through
`chimera_control_read`, feeds exact replies to Python and checks C1/DD/D2/C2/DC
STALL with unchanged canaries. Independent fixtures reject8160single-byte manifest
changes,6375single-byte version changes,256incorrect lengths and12invalid-type
arguments. A temporary reserved-validation mutation is detected and restored.

Baselinee586191ac39e663727aac2cbd453937477350ef8; current Panda
8a16e089b88593914823743df29e1c30b7dd3e00 health header and native consumer/identifier
sources were read. Existing [legacy profiles](LEGACY_PANDA_SUPPORT.md) remain
distinct, not newly adapted. Exact hashes/results are in [the receipt](../../Ai/Evidence/chimera-status-contract-20261106.json).
Source/CLI analysis and GNU ARM artifact checks were used; no new REA provider,
electrical measurement or physical USB result is claimed.

Next T05b: exact legacy F4health59 decoding/adaptation before managed use. New
Chimera operational health, bulk/controller binding, MCU policy and qualified
startup/attachment remain separate increments.
