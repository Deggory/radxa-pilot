# Classical CAN transport codec

November 6, 2026 — T04 offline implementation. This is a pure byte codec, retained
in the F413 image but not called by the parked application. No USB endpoint,
CAN peripheral, TX queue, forwarding or safety policy is activated. The bootstrap
manifest still reports phase0, capabilities0 and active layout hashes0.

## Exact current wire format, classical subset

The source contract is the project's current opendbc `safety/can.h`, Panda
`board/can_comms.h`, `python/__init__.py` and native pandad packing/unpacking.
Panda8a16e089/opendbc150f9371, exact working-file hashes and tests are pinned in
[the receipt](../../Ai/Evidence/chimera-can-codec-20261106.json). No packed vendor
struct or peripheral implementation is copied into the firmware; it uses explicit
byte operations. The test alone includes the actual current packed header as an
independent compiler/layout oracle and evaluates the current Python pure functions
without importing Panda or invoking a constructor.

| Wire bytes | Meaning |
| --- | --- |
|0|DLC in bits7..4, physical host bus in3..1, FD in0|
|1..4|Little-endian `(address << 3) | (extended << 2) | (returned << 1) | rejected`|
|5|XOR of bytes0..4 and payload; XOR of a complete valid record is0|
|6..13|0..8payload bytes; record size6+DLC|

Only bus0/1/2, DLC0..8, FD0 and29-bit maximum IDs are supported. Standard frames
must have address<=0x7FF; explicit extended frames may use a lower numeric ID.
Frame length0 is valid. No RTR field or conversion is provided; the eventual CAN
driver must handle unsupported remote frames explicitly. No64-byte transport
counter is inserted. USB transfer or packet boundaries do not delimit records.

Example: standard ID0x123, bus2, payload112233 encodes as
`34 18 09 00 00 25 11 22 33`.

## Direction and ownership

The [API](../firmware/can_codec.h) separates board-to-host encoding from host-to-
board decoding. Encoder status is received0, returned1 or rejected2, mutually
exclusive. The wire returned/rejected bits map to current host source offsets
128/192 while the actual bus stays0..2. Both bits together are not generated.
Host TX decoding rejects either metadata bit, FD, out-of-range bus/DLC/address,
incorrect checksum and short/overlong complete records. Decoding a record does
not authorize sending it: the future MCU policy must inspect every command,
generated report, forwarded packet and maintenance path independently. Caller
supplies origin/echo metadata; the codec cannot prove physical RX or TX completion.
Locally generated reports still need the explicit host-delivery/source contract.

Single-record calls return the record byte length or ERROR(-1). All validation
precedes destination writes; failure leaves the destination unchanged. Decode
zeroes unused payload bytes. Wire buffers need byte alignment; frame/state objects
need their normal C alignment. Caller-owned input/output/state/consumed storage
must be separate. Functions allocate no heap and access no registers or queues.

## Streaming and failure handling

`chimera_can_stream` occupies16bytes:14buffer bytes, used count and error latch.
Initialize one state per connection, use it serially and retain it across chunks.
Feed returns FRAME(1) for one validated record, MORE(0) for a partial record or
ERROR(-1). The consumed count includes bytes through that result; caller retains
the rest of the chunk and must handle queue capacity/policy before feeding again.
Output frame changes only on FRAME. At most14input bytes are processed per call.

Headers are checked when six bytes are available, before using the DLC to collect
payload. Corrupt pending-state lengths and invalid arguments are rejected. A
detected header/checksum failure latches ERROR, stops consumption and prevents
sliding-byte resynchronization. Further calls consume0until an explicit local
initialization after session/transport recovery. This is not a new USB reset RPC.
Initialization discards an old partial record. Empty polling can retain a partial
record; timeout/disconnect/epoch handling belongs to the future transport owner.

Records returned before a later malformed record are already returned; there is
no transaction rollback. No implicit retry, frame queue or hardware side effect is
hidden in the codec. USB/CAN wiring and the TX policy remain mandatory next layers.

## Integrity limits and actual verification

XOR matches the current transport but is neither authentication nor a substitute
for OEM/RetroPilot message integrity and safety checks. Balanced data-bit changes
can preserve XOR. A DLC bit change can also make a shorter prefix valid: changing
`10 00 00 00 00 00 10` to`00 00 00 00 00 00 10` yields a checksum-valid six-byte
zero-length prefix and one pending byte. Exact-size decode rejects the seven-byte
mutant; a stream cannot distinguish that prefix from an intentionally shorter
frame. Tests explicitly preserve these two counterexamples. No claim of universal
corruption detection or safety enforcement is made.

Fourteen offline tests pass with GCC13.2.1/binutils2.42 and native ASan/UBSan:

- 648 RX vectors match the actual packed current header and current Python unpacker;
  189automatically addressed TX vectors match current Python packing byte for byte.
- 216 host-TX vectors exercise every split point; a2160-byte concatenation is decoded
  using all chunk sizes1..2160, including crossing64-byte boundaries:4536split/chunk
  scenarios total, with ordering and consumption checked.
- 17280 single-bit corruptions of fixed-size records are rejected; altered-length
  records in that check are rejected by exact-size validation. This is not a
  stronger claim about arbitrary stream corruption.
- 65536 first-two-header-byte combinations are checked against the actual packed
  source header;10000deterministic arbitrary byte streams run with sanitizers.
- Bounds/null/flags/IDs/output canaries, partial reset, sticky failures, invalid
  state lengths and known XOR limitations are exercised. ARM retained symbols,
  boot vectors, memory overflow rejection and copied-tree determinism also pass.

The ARM application initially linked an implicit memset from aggregate zeroing;
explicit validated member/data writes removed that unintended libc dependency.
The strict undefined-symbol check remains enabled. Raw1840bytes, globals8bytes,
reserved stack4096bytes and legacy envelope budget unchanged. There was no ARM
runtime/REA provider run, hardware enumeration, CAN/USB traffic or flash operation.

The [bus/input contract](BUS_INPUT_CONTRACT.md) and canonical RetroPilot DBC
continue to govern physical routing and CAN payloads. This increment neither
interprets nor changes those payload definitions. T03b1 now supplies
[detached USB preparation/EP0 state](USB_BOOTSTRAP.md). T03b2 adds the
[controller event/FIFO packet driver](USB_PACKET_DRIVER.md). Next: power/VBUS/UID
and watchdog/recovery prerequisites and reviewed startup/attachment, then status
and endpoint binding.
