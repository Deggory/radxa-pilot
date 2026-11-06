# Legacy F4 health17 decoder and read contract

November 6, 2026 — T05b. [Header](../../openpilot/selfdrive/pandad/panda_health.h)
and [implementation](../../openpilot/selfdrive/pandad/panda_health.cc) decode the
Carrot F4 profile's59-byte D2 reply. They are compiled into the native host
library, exercised offline and not connected to managed `Panda::get_state` or
startup. Chimera firmware and current SPI behavior are unchanged.

## Qualification and failure behavior

Caller first identifies the same exclusively owned transport with the explicit
serial/firmware pin. Existing `identify_panda` requires F4 hardware1/2/3/5/6,
exact DD17/4/5 and D2 length59 for `LEGACY_F4_V17`. Neither board age, USB VID/PID
nor length alone chooses a profile. Decoder requires that qualified profile;
current Panda/original Chimera are rejected. The enum is a caller contract,
not authentication.

`decode_legacy_f4_health(profile, data, size)` is pure: exact59bytes, unaligned
input supported, no retained pointers/modification. Boolean bytes must be0or1;
load must be finite/nonnegative. Unknown enum bytes and all integer bits remain
raw. Finite loads above1 are preserved, not clamped. These are our explicit host
validation rules, not claimed legacy firmware behavior.

`read_legacy_f4_health(handle, profile)` makes at most one D2 IN call, value/index0,
64-byte buffer, timeout1000ms. Requesting64 rather than59 detects oversized replies
instead of silently truncating them. Unsupported profiles and disconnected/
unhealthy handles return nullopt before IO. Errors, non-exact lengths, malformed
replies or lost connection/health after reading return nullopt. No cache, retries,
default health, OUT/reset/bulk/update operation. Transport exceptions propagate.
Caller must serialize ownership/disconnect; atomic health flags are not a
lifecycle lock. Timestamp/freshness/reconnect remains future managed work.

## Field mapping

Multibyte values are little-endian. `LegacyF4Health` is an ordinary C++ value,
never a cast of wire bytes or current packed health49.

| Offset | Wire type | Result |
| --- | --- | --- |
|0,4,8|u32 each|uptime, voltage_mV, current_mA; full32-bit width|
|12,16,20,24,28|u32 each|safety_tx_blocked, safety_rx_invalid, tx/rx_buffer_overflow, faults|
|32,33,34,35|u8 each|ignition_line, ignition_can, wake_on_can, controls_allowed; checked booleans|
|36,37|u8 each|harness_status_raw, safety_mode_raw; no current enum translation|
|38|u16|safety_param unsigned|
|40|u8|fault_status_raw|
|41,42|u8 each|power_save_enabled, heartbeat_lost; checked booleans|
|43|u16|alternative_experience|
|45|IEEE754binary32|interrupt_load; fraction preserved, no current u8/255 conversion|
|49|u8|fan_power|
|50|u8|safety_rx_checks_invalid; checked boolean|
|51|u16|spi_checksum_error_count; no silent broader error-count rename|
|53|u8|fan_stall_count|
|54,56|u16 each|sbu1_voltage_mV, sbu2_voltage_mV|
|58|u8|som_reset_triggered; checked boolean|

Current-only NMI/hardfault, sound, temperature and independent lateral/
longitudinal controls fields are absent from this type. A future publisher needs
explicit unsupported/validity behavior; casting/zero-initializing health49 cannot
supply measured zero/false. Legacy mode/parameter/alternative bits also require
command/policy compatibility review before current safety consumers. Decoded
controls-allowed is a firmware report, not actuation or managed permission.

## Sources and tests

Carrot carrot-wip `69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7`, previously fetched
November6. [Exact header/license](../reference/carrot-f4-health-v17/README.md)
are inside the project for standalone tests. Original producer
`panda/board/main_comms.h:get_health_pkt` and Python health format/field mapping
were read in retained source. No network or full firmware audit.

[Native tests](../../openpilot/selfdrive/pandad/tests/test_panda_health.cc) compare
all27fields against the pinned packed header plus independent golden bytes;
exercise256boolean combinations, high32-bit values, fractional/extreme finite
loads and unaligned input.2032noncanonical booleans, wrong lengths/profiles,
nonfinite/negative loads and bounded read/error/disconnect/no-cache cases are
checked. ASan/UBSan and SCons run offline. Mutation review verifies losing profile
qualification is caught. [Receipt](../../Ai/Evidence/chimera-legacy-health-20261106.json)
records actual commands/results/hashes.

T05c now adds [CAN-health5 decoding/read support](LEGACY_F4_CAN_HEALTH.md), verified
offline. T08a now adds [USB-only status startup](USB_ONLY_STARTUP.md); next T08b
passive reception/publication, reconnect and exact-read hardening remain pending. Full T05 stays partial because new Chimera
operational health is absent. Physical attachment remains separately unqualified.
