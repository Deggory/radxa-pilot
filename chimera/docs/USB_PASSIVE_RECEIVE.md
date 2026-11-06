# Passive USB CAN and legacy status observation

November 6, 2026 — T08b1. Extends [USB-only startup](USB_ONLY_STARTUP.md)
for the already qualified legacy F4v17 profile. No new firmware profile is admitted.

## Receive contract

The session owns USB exclusively and reads endpoint0x81 into4096bytes with a10ms
per-transfer timeout. Timeout bytes are retained, including partial frames.
[PandaUsbCanStream](../../openpilot/selfdrive/pandad/panda_usb_can.h) accepts
classical six-byte/XOR records, DLC0..8, host bus0..2 and standard/extended IDs.
Returned/rejected receipts are validated and filtered. FD, invalid bus/ID/DLC,
conflicting metadata, bad XOR, clock reversal and oversized input fail closed.
The parser retains at most14bytes. An incomplete record expires after500ms from
its first fragment, including across empty polls. A malformed record discards
all frames from that feed. Earlier separately published batches cannot be revoked.
Any receive/status error closes ownership and discards partial data; later calls
perform no IO. Explicit reopen repeats identification. There is no reset/retry/
resynchronization command or SPI fallback.

Bus numbers remain raw0/1/2; no routing is inferred from status selectors. The
board target remains CAN0/Cores=host0, CAN1/ADAS=host1, CAN2/vehicle=host2, pending
physical qualification. The canonical shared RetroPilot DBC is unchanged.

Legacy CAN6 has no RTR field: host software cannot distinguish or filter an RTR
record encoded as ordinary data by legacy firmware. This requires MCU-side
qualification. XOR does not detect every corruption or length ambiguity.

## Host publication

The explicit USB entry owns two publishers; run it as the single CAN producer.
It publishes Cereal `can` using host receive-completion timestamps; these are not
ECU timestamps or an end-to-end freshness guarantee. Empty successful polls may
publish valid empty lists; malformed/disconnected data publishes invalid empty CAN
on orderly failure. Cereal CAN has no extended-ID flag; the internal parser retains
it, but normal Cereal publication preserves only address, bus and payload.

`customReservedRawData1` is allocated to JSON schema1 with kind
`panda-usb-status`, profile `legacyF4v17`, exact serial/version pins,
`operational:false`, state, startNanos/endNanos, health and controllers.
Timestamps are decimal strings to preserve64bits. Health has all27supported native
fields; each of3controllers has26wire fields plus can_number. Field names/units
match [health](LEGACY_F4_HEALTH.md) and [CAN health](LEGACY_F4_CAN_HEALTH.md).
Raw enum numbers, unsigned measurements and fractional interrupt load are retained.
Unsupported current-only fields are absent. No shared CAN protocol is introduced.

Diagnostic `Event.valid` is true only for a complete decoded observing sample;
it is not permission to control. D2 plus three C2 reports are sequential, not an
atomic MCU snapshot; start/end bound the host query interval. Main polls CAN and
sleeps10ms, attempts status about once per second after the prior sample completes.
Four1000ms control timeouts can delay CAN polling; no throughput/freshness or
whole-loop deadline is claimed. An old partial frame then fails its age limit.
Failure/close diagnostics set valid=false, health=null and controllers=[];
no prior health is replayed. Abrupt process/power loss cannot guarantee a final
message: consumers must check liveness as well as Event.valid.

## Why pandaStates remains deferred

`hardwared.py` reads ignition from nonempty pandaStates without checking
Event.valid. Unsupported legacy fields cannot be expressed with individual
validity there. This increment publishes no pandaStates at all. RawData0 remains
owned by Thneed timing/UI; camera/model/Thneed code is untouched. Normal onroad
admission, validity/ignition policy, heartbeat/safety/TX and reconnect policy remain
separate work. Version matching is not authentication of arbitrary old firmware.

## Verification

The actual native target and9test programs build/pass. New tests cover324records
at every split, malformed batches, age limits, timeout fragments, disconnect,
failure latching and Capnp/JSON round trips with full-width values.25Python
regressions include Thneed telemetry. Parser and real USB backend/session pass
ASan/UBSan with fake libusb and no SPI source linked. Removing checksum rejection
causes the parser test to fail. Invalid CLI checks never open a device.
[Receipt](../../Ai/Evidence/chimera-usb-receive-20261106.json) pins exact sources,
commands/results and preservation checks. No real USB/publisher session, board,
flash, relay or vehicle test was performed. New F413 firmware remains parked.

Next T08b2: specify profile-aware pandaStates admission, supported-field validity,
ignition handling and reconnect/backoff before enabling the normal host lifecycle.
