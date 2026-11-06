# Chimera identity and request contract

November 6, 2026 — T02b. The compiled bootstrap contains a pure, read-only vendor
request handler and identity data. T03b1 adds detached clock/core preparation and
a descriptor/EP0 model; MMIO/timing binding, FIFO/event handling and startup
connection remain pending. This contract defines the EP0 connection; no board
enumeration, host selection or modern operational compatibility is claimed.

## Separate identity before interpreting requests

Development descriptor contract: retain the legacy normal-mode VID:PID
`bbaa:ddcc`, use product **Chimera F413**, and require a stable, nonempty serial
derived from the MCU unique identity. T03b1 now implements lowercase UID serial
formatting and a control-only descriptor model; hardware UID read/publication
is still future work. This reuses the board's existing development IDs; it is not a
claim of USB-IF allocation or permission for a new commercial VID.

The firmware version response is `chimera-f413-bootstrap-v1`,25ASCIIbytes without
a NUL. It labels this bootstrap ABI, not a unique binary digest or authenticated
image. The build receipt separately records the actual source and image hashes.
Future phases need explicit version/manifest qualification before host admission.

The new image does not impersonate stock Panda C1 hardware types. Local manifest
board-family1 means **our Chimera F413 target**, not a silicon DBGMCU_IDCODE or a
Panda enumeration. Original `Chimera`/mailbox43 and current/F4 Panda profiles stay
distinct. Existing native selection does not support this bootstrap; it must
continue rejecting incomplete/unknown combinations. Managed startup stays SPI.

The future explicit host path must match descriptor serial to the requested pin,
read D6 and A0, validate exact lengths/schema/phase/reserved fields and qualify
capabilities/layout hashes before any operational read or write. Descriptor names,
version strings and USB CRC are not cryptographic authentication. No automatic
Panda updater, reset, DFU sweep or H7 image selection is permitted by this identity.

## Vendor control ABI implemented now

The handler takes an exact8-byte USB SETUP buffer, a separate destination buffer
and its capacity. Setup u16 fields are decoded little-endian. Only `bmRequestType`
`0xC0` (vendor/device/IN), zero wValue and zero wIndex are accepted. wLength must
be at least the full reply size and at most64; destination capacity must cover the
reply. This is an explicit complete-reply rule for these vendor queries. No NUL,
padding or partial reply is returned. Failure returns`CHIMERA_CONTROL_STALL`(-1)
without modifying the destination; a future USB driver must convert that result
to an EP0 STALL. Standard USB requests belong in that separate driver.

| Request | Bootstrap result | Later implementation boundary |
| --- | --- | --- |
| A0 IN |32-byte manifest below | Custom Chimera discovery only; no conflicting A0 handler found in pinned Chimera/current Panda command sources |
| D6 IN |25-byte version | Read-only; exact firmware phase/version policy |
| C1 / DD | STALL | No borrowed Panda hardware type or fabricated current layout hashes |
| D2 / C2 | STALL | Health/CAN health unimplemented; must not emit plausible zero-filled modern health |
| D0 / D3 / D4 / B0..B5 / E0 | STALL | No fabricated provisioning/signature/fan/IR/accessory/debug data |
| DC / DF / F3 | STALL | No safety/alternative-experience/heartbeat semantics until an MCU policy exists |
| DE / E5 / E7 / E8 / F9 / FC | STALL | No bitrate/loopback/power-save/CAN-FD configuration |
| FB / FD / FE / FF | STALL | No legacy JSON/config passthrough or config persistence |
| D8 and all other request numbers | STALL | No reset, recovery or unspecified operation |
| Every control OUT, class/standard/other-recipient request | STALL in this vendor handler | No mutation API; standard enumeration requests are handled separately later |

Endpoint plan remains configuration1/interface0, FS64-byte packets, bulk IN81 and
OUT03. Neither endpoint is enabled by this slice. Future CAN TX/forwarding,
generated reports and maintenance must all be gated by the MCU policy; USB
acceptance or a TX echo never authorizes vehicle actuation.

## A0 manifest v1:32bytes

Multi-byte fields below are unsigned little-endian; reserved bytes must be zero.

| Offset | Size | Field | Bootstrap value/meaning |
| --- | --- | --- | --- |
|0|4|magic|ASCII CHMR|
|4|1|manifest schema|1|
|5|1|manifest length|32|
|6|1|local board family|1=Chimera F413 target|
|7|1|operating phase|0=bootstrap, no operational interfaces|
|8|4|operational capability bits|0; no CAN RX/TX, acquisition, health, config, relay/OBD-C operation or update capability|
|12|4|active CAN layout hash|0=unavailable, no codec advertised|
|16|4|active health layout hash|0=unavailable, no health advertised|
|20|1|physical bus count|3, source-defined board topology|
|21|1|physical classical payload maximum|8, no CAN-FD capability|
|22|1|automatic update policy|0=disabled|
|23|1|configuration ABI|0=unavailable; no legacy flash reinterpretation|
|24|2|source-defined physical interface mask|0x01FF: IGN,VSS,CPS,brake,ADC1,ADC2,relay,OBD-C request,OBD-C ignition in bit order0..8|
|26|6|reserved|all0|

Physical presence describes the reviewed board design. It does not mean any input
is sampled, calibrated or valid, or that outputs/recovery are electrically proven.
Capability0 and hashes0 deliberately prevent operational negotiation. A later
phase must define bit assignments, exact health validity semantics and hash inputs
before setting capabilities; this document does not pre-authorize those changes.

Target CAN framing remains the pinned current six-byte/XOR classical format;
current host hash is derived from opendbc/safety/can.h rather than a firmware
constant copied blindly. Health49 versus F4health59 versus oldChimera43 remains a
separate versioned contract. The bootstrap advertises none of them. Core Config
needs a dedicated read/monitor transport and exclusive future write lifecycle;
legacy FB/FC cannot be mapped through current Panda commands with the same number.

## Evidence and validation

Source routing and source-selection policy are in
[BUS_INPUT_CONTRACT.md](BUS_INPUT_CONTRACT.md). Original command source:
Ocelotd87892fa plus preserved dirty hashes, current Panda8a16e089 and native
identification/USB from baseline0bc14bcfd. Exact versions/hashes/checks are in
[the receipt](../../Ai/Evidence/chimera-identity-contract-20261106.json).

The [libusb SETUP field documentation](https://libusb.sourceforge.io/api-1.0/structlibusb__control__setup.html)
and [request type/recipient definitions](https://libusb.sourceforge.io/api-1.0/group__libusb__misc.html)
confirm the wire fields and request-type interpretation. Online docs1.0.30;
the host's existing vendored1.0.29.post103 header has the same definitions. The
manifest, A0 choice and rejection policy are our new design, not legacy behavior.

The T02b twelve-test suite passed. The native ASan/UBSan handler fixture checks458920
cases: every bmRequestType/request pair, all65536 lengths and wValue/wIndex values
for both queries, destination capacities, malformed SETUP sizes and null pointers.
Two deliberately unaligned SETUP buffers also pass. Canaries verify exact response
bytes and unchanged buffers on rejection. ARM byte-load disassembly verifies the
decoder avoids unaligned halfword access; the target uses `-mno-unaligned-access`
to avoid depending on inherited UNALIGN_TRP state. ARM
symbols/bytes confirm the handler and identity survive linking. Original vector,
GPIO, overflow, startup ordering and copied-tree deterministic-build tests pass.
Handler code is deliberately retained for these checks and future wiring; nothing
calls it from the parked application. This is not a USB runtime test.

T04 now adds the [classical CAN codec](CAN_CODEC_CONTRACT.md) and expands the
combined suite to fourteen tests. It is not connected to USB/CAN hardware; the
bootstrap identity, phase and zero operational capability/layout fields stay as
specified above. Code availability alone does not advertise an active interface.

T03b1 adds [USB preparation/EP0 state](USB_BOOTSTRAP.md), expanding the combined
suite to sixteen tests. The EP0 wrapper permits D6/A0 only after configuration1;
the standalone vendor handler ABI remains unchanged. Its bootstrap descriptor
advertises zero bulk endpoints. The planned IN81/OUT03 operational interface is
not enabled, and the model is not yet connected to a hardware packet driver.
