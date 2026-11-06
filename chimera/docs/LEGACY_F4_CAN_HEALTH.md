# Legacy F4 CAN-health5 decoder and reader

November 6, 2026 — T05c. Added to [panda_health.h](../../openpilot/selfdrive/pandad/panda_health.h)
and [implementation](../../openpilot/selfdrive/pandad/panda_health.cc). This is
native host code for the already identified legacy F4 profile, not a new MCU
status producer or managed publisher. USB only remains the Radxa deployment.

## Profile, selector and failure contract

`decode_legacy_f4_can_health(profile, can_number, data, size)` requires
`LEGACY_F4_V17`, selector0/1/2 and exact64bytes. Prior serial/version/hardware/DD
qualification comes from `identify_panda`; the profile argument is a caller
contract, not authentication. Same-sized current/old-Chimera replies never select
this profile by length. Six boolean bytes must be0or1; all four LEC bytes0..7.
Invalid arguments/fields return nullopt. Unaligned input is supported without
casts, mutation or retained pointers. Integers retain their unsigned widths.

`LegacyF4CanHealth` includes all26wire fields plus the caller's `can_number`.
The reply has no selector echo: this tag records which selector was requested,
not proof that firmware returned the correct physical controller. No remapping
to Chimera Cores/ADAS/vehicle roles or stock Panda harness orientation is inferred.
Physical bus qualification remains separate.

`read_legacy_f4_can_health(handle, profile, can_number)` performs one C2 control-IN
request: value=selector, index0, length64, timeout1000ms. Unsupported profiles,
selectors outside0..2 and disconnected/unhealthy handles fail before IO. A failed,
short, malformed, impossible-length or unhealthy completed read returns nullopt.
No retry, prior-state cache, synthetic healthy default, OUT/bulk/reset or SPI
probe/fallback. Caller must hold exclusive serialized transport ownership;
exceptions propagate. USB control-transfer termination bounds the64-byte response;
there is no application checksum, freshness timestamp or in-band version/length.
Passing validation does not detect every content corruption or establish readiness.

## Exact wire fields

Multibyte fields are little-endian. This ordinary C++ result is not a wire struct.

| Offset | Wire type | Result/meaning |
| --- | --- | --- |
|0|u8|bus_off boolean|
|1|u32|bus_off_cnt, raw legacy counter (see polling behavior below)|
|5,6|u8 each|error_warning/error_passive booleans|
|7,8,9,10|u8 each|last_error, last_stored_error, last_data_error, last_data_stored_error; codes0..7|
|11,12|u8 each|receive_error_cnt/transmit_error_cnt; full0..255 preserved|
|13,17,21|u32 each|total_error_cnt, total_tx_lost_cnt, total_rx_lost_cnt|
|25,29,33,37|u32 each|total_tx_cnt, total_rx_cnt, total_fwd_cnt, total_tx_checksum_error_cnt|
|41,43|u16 each|can_speed_kbps/can_data_speed_kbps; producer already divides configured units by10|
|45,46,47|u8 each|canfd_enabled/brs_enabled/canfd_non_iso, checked reported booleans|
|48,52,56,60|u32 each|irq0/1/2_call_rate and can_core_reset_cnt|

F4 bxCAN remains classical CAN. Reported FD/configuration fields are preserved,
not a CAN-FD capability claim or an instruction to enable FD. Likewise, unused
DLEC fields remain reported values, not evidence of an FD data phase. The common
header's REC comment mentions H7's0..127; F413 CMSIS defines an8-bit REC mask and
the actual bxCAN producer copies it. This decoder does not truncate/reject128..255.

## Legacy polling changes statistics

The source C2 handler calls `update_can_health_pkt(selector, 0)`. The F4 producer
adds `bus_off` to `bus_off_cnt` every time that function runs, including reads
while bus-off is asserted. It is not a count of distinct bus-off transitions and
depends on poll/interrupt cadence. It also updates stored errors and reported
register/IRQ samples. Our helper issues no control OUT, but this legacy IN query
is not a side-effect-free statistics snapshot. No derived event rate or current
counter semantics are fabricated. Arithmetic/wrap/reset remain legacy reports.

## Evidence and validation

Carrot source pin69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7: exact retained
health.h/MIT license, C2 handler in main_comms.h, bxcan.h producer and Python
format/field mapping. Existing [source fixture](../reference/carrot-f4-health-v17/README.md)
is reused unchanged. Current Panda8a16e089's CAN-health header has matching size,
offsets and field types at these pins; every field is asserted in the
[new native fixture](../../openpilot/selfdrive/pandad/tests/test_panda_can_health.cc).
This limited layout compatibility does not equate main health49/59, versions,
command policies, physical wiring or readiness.

Tests cover independent golden bytes/all26fields,3selectors x64flag combinations,
unaligned copies, unsigned boundaries,1524invalid booleans,1024LEC cases and all
65533invalid u16 selectors. Single-call reads test selectors, timeouts/lengths,
disconnect/unhealthy results, malformed payloads and no writes/retry/cache.
A temporary removed reader-selector bound is detected before invalid IO and
restored. Native SCons and strict ASan/UBSan results plus exact source/artifact
hashes are in [the receipt](../../Ai/Evidence/chimera-can-health-20261106.json).
Source/CLI/GNU artifact route; no new REA provider or physical device result.

Next T08a: USB-only session/startup integration with explicit pins and exclusive
ownership, no SPI probing/fallback. Managed health publication, exact-read
hardening and reconnect remain to implement. Full T05 stays partial because new
Chimera operational health is absent; new firmware still parks/unflashed.
