# Legacy Panda compatibility

Owner requirement, November 6, 2026: build Chimera support so our Sunnypilot can
also support legacy Panda. Initial legacy target means the older F4 boards in
the reviewed CarrotPilot source: white, grey, black, UNO and DOS. Their hardware
generation does not determine the installed USB protocol. Other old firmware
generations require their own pinned contract before selection.

November6 source follow-up: [Ocelot Panda Docker](OCELOT_PANDA_DOCKER_REVIEW.md)
04b56ba0 retains an older mailbox16/health43 Panda application. Its DD request
changes CAN forwarding rather than returning versions; its target selects stock
Panda board detection, not Chimera acquisition. The parent98de83bb retains the
separate Chimera target. This is an additional reference profile, not admitted
by the current selector or interchangeable with Carrot F4's health59 contract.

## USB-only Radxa connection

Owner clarified November6: Radxa connects to Chimera and the selected legacy
Panda by USB only. No SPI wiring/probe/fallback belongs in this deployment.
`PandaUsbHandle` implements the common control/bulk interface with explicit
serial/version qualification. Sharing an interface does not require using both
transports.

The inherited native `Panda` constructor/list still select `PandaSpiHandle`.
That is a remaining T08 integration gap, not the intended deployment path.
T08 must use pinned USB selection, exclusive ownership and bounded reconnect;
missing/rejected/disconnected USB must stay disconnected without trying SPI.
Existing generic SPI source need not be extended for this project.

The existing chimera_protocol.py handles original mailbox16/health43 decoding
for the separate Python receiver. It is not the new native USB backend or an
F4 health59 decoder. Preserve that distinction when reusing its tests.

## Separate transport, protocol and board behavior

- Transport moves control/bulk bytes over USB or SPI.
- Protocol profiles define CAN framing, status layouts, versions and commands.
- Board support defines MCU, GPIO, inputs, relay and firmware/recovery policy.

Use the existing common host interface with the USB backend for this Radxa
deployment. Preserve qualified protocol framing/bounds and explicit selection.
Chimera retains its own board definition. Do not substitute Panda harness GPIO
or black-Panda power controls for Chimera's input and OBD-C assignments.

| Reference profile | CAN records | Health/version contract | Current project status |
| --- | --- | --- | --- |
| Current Panda, 8a16e089 | Six-byte header, payload, XOR | 49-byte health; DD returns two 32-bit layout hashes | Existing native SPI path |
| Carrot F4 reference, 69a2d3be | Six-byte header, payload, XOR; F4 classical CAN | 59-byte health; DD returns numeric health17/CAN4/CAN-health5 | Offline USB/identification and typed health59 decoder/read helper implemented; publication/lifecycle pending |
| Original Chimera, d87892fa plus dirty source | 16-byte mailbox | 43-byte health; no matching modern DD handler | Separate Python receiver and native read-only USB transport; not managed Panda support |
| New Chimera target | Pinned modern classical CAN codec, unbound | Implemented phase0 A0/D6 contract; no operational health | Offline firmware/service/decoder pieces; startup and operational host integration pending |

Same framing does not make different health layouts interchangeable. Verify
identity, exact response lengths and the applicable versions before selecting a
profile. Translate only evidenced fields into host state; unsupported fields
must not be reported as measured health. Reject unknown/incomplete combinations.
F4 and Chimera cannot acquire CAN-FD support from a host framing change.

Initial USB discovery must avoid generic Panda constructors that perform setup
writes. Separate read-only identification from initialization and from firmware
updates. Each board/image combination needs its own approved update/recovery
policy; discovering an external F4 or Chimera must never invoke an H7 flash path.

## Small implementation slices

1. **T06a transport boundary:** Panda owns a `PandaCommsHandle`; existing SPI
   implements it. Compile native pandad and test polymorphic ownership/error
   propagation plus existing CAN codec behavior. No USB device is selected yet.
2. **T02 profiles:** freeze identification/version/length and command matrices
   for each supported firmware pin. Test unknown, truncated and conflicting
   replies before any initialization write.
3. **T06b USB backend:** bounded libusb I/O, cleanup, partial reads/timeouts and
   unplug behavior, with fake-device tests. Keep enumeration/profile selection
   separate from opening/initializing a supported board.
4. **T05 legacy status adapter:** exact 59-byte F4 status decoder alongside the
   current status contract, with pinned field/length/version fixtures.
5. **T08 lifecycle:** USB-only pinned selection, no SPI probing/fallback, exclusive ownership and
   correct board policy before managed passive RX tests. Unknown firmware stays
   unsupported; no broad reset/DFU/flash sweep.

T06a completes only the shared host boundary. It does not establish USB device
support, legacy status compatibility, managed readiness or driving capability.
T01/T03 Chimera board/flash/build work remains necessary and separate.

Sources: project `Ai/Reports/carrot-wip-panda-20261106/README.md` and
`Ai/Reports/panda-chimera-deep-review-20261105/README.md`; exact source pins and
selected Carrot files are retained in the original workspace archive. Current
native `panda.cc`, `panda.h`, `panda_comms.h` and `spi.cc` are the implementation
baseline. No Carrot SPI implementation or stock board initialization is imported.

## T02a identification increment — November 6

Native `panda_identification.{h,cc}` now provides a bounded, control-IN-only
selector. A caller must supply a normal-mode descriptor identity and an explicit
serial/firmware-version pin. The transport serial must match the descriptor and
pin. Bootstub/DFU, unknown vendors, empty pins and invalid version strings are
rejected before vendor I/O.

Panda candidates use D6 version, one-byte C1 hardware, exact DD versions and D2
health length. F4 hardware 1/2/3/5/6 requires DD17/4/5 and health59; current
hardware 7/9/10/B1 requires the two hashes derived at build time from our current
Panda health and opendbc CAN headers plus health49. Both known Panda VIDs are
eligible; VID/PID alone never selects a profile.

Original Chimera requires bbaa:ddcc, product `Chimera`, the retained nightly
version `v1.0.0-DEV-de193215-DEBUG`, the explicit serial/version pins, D6 and
health43. Arbitrary new Chimera version pins do not select the old protocol. It does not receive unsupported C1/DD requests. The result retains
raw initial health, without treating it as a modern safety or readiness state.
Each read has a one-second timeout and no automatic retries. An exact version
string is a reported-version check, not cryptographic image attestation.

Offline tests cover 19 accepted fixtures, 421 rejected fixtures and three invalid
transport cases; fake handles reject every vendor OUT/bulk operation. Native and
address/undefined-behavior-sanitized runs pass. This selector is built into the
native library but is not wired into startup yet. Existing Panda construction
and updater flows retain their previous behavior until protected USB selection
is integrated. The USB backend increment below is now implemented; legacy status
decoding, complete RPC/source contracts and real-device qualification remain pending.

## T06b native USB connection — November 6

`PandaUsbHandle::open(pin)` implements an explicit connection factory. It rejects
empty pins before libusb initialization, considers only normal-mode bbaa/3801:
ddcc devices, obtains actual serial/product descriptors, rejects duplicate
matching serials, requires configuration 1 and claims interface 0 exclusively.
It then runs T02a identification before returning a handle. Unreadable candidates
are closed; every failed path releases the resources actually acquired.

The factory sends no vendor OUT or bulk traffic. It does not change USB
configuration, detach a driver, reset/clear endpoints or call an updater. A busy
interface or unconfigured device is refused. Ownership must be handed off
explicitly; a competing process is not evicted.

Control/bulk calls are serialized and capped at one second. Bulk IN 0x81 returns
actual received bytes, including partial timeout data. Bulk OUT 3 makes one
attempt; a timeout is an uncertain failure and is not retried. Short writes and
I/O failures mark communications unhealthy; disconnect marks the handle dead.
The host lifecycle must handle these states and invalidate stale data.

Original Chimera remains read-only: control OUT and bulk OUT are denied, and
control IN is limited to D6/D2 with zero parameters. Direction alone is not a
read-only guarantee: the inspected old application dispatches by request number
and includes D8 reset/DC relay-request side effects. No config or accessory API
is enabled by the passive transport. Current/F4 raw transport writes remain a
caller-policy responsibility after identification; this adds no active profile.

Tests link fake libusb C implementations and never enumerate this host. They
cover resource cleanup, ambiguous/failed discovery, current/F4/Chimera profiles,
claim failures, partial/short transfers, timeout/unplug/overflow, dead handles,
idempotent cleanup and Chimera command denial. The separate real-library link
test rejects empty pins before USB initialization. Native/sanitized tests pass;
no physical USB link or managed readiness is claimed.

Dependency: existing vendored `comma-deps-libusb` 1.0.29.post103, not a new system
installation. Semantics checked against the installed header and the official
[synchronous I/O](https://libusb.sourceforge.io/api-1.0/group__libusb__syncio.html)
and [device ownership](https://libusb.sourceforge.io/api-1.0/group__libusb__dev.html)
documentation (published API docs identify themselves as 1.0.30). The reviewed
Carrot backend remains a reference; its retry and constructor policy is not copied.

Next: exact legacy status adaptation (T05), then protected managed USB selection
(T08). The USB factory is not invoked by current Panda construction or startup.

## T05b legacy health increment — November 6

The native library now contains a pure health59 decoder and a one-call bounded
D2 reader. Full32-bit voltage/current, fractional load, separate boolean flags
and legacy-only wake/fan-stall/SOM-reset fields are retained in a distinct type.
No cast to current health49 or current-only defaults. Actual pinned packed header
and independent golden bytes, sanitizers and invalid-read cases pass offline.
Managed get_state/publication, per-bus health and lifecycle remain pending.
See the [field/error contract](LEGACY_F4_HEALTH.md).

## T05c per-controller health increment — November 6

Added exact CAN-health5/64 decoding and one bounded C2 reader for selectors0..2.
All26fields and full counters are preserved. Current/legacy field layouts match
at pinned sources, while profile/version gates remain separate. Invalid selectors
fail before IO. Counter polling semantics and physical routing limits are explicit.
See the [contract](LEGACY_F4_CAN_HEALTH.md). Next T08a USB-only session/startup
ownership; no SPI probe/fallback or managed-readiness claim.
