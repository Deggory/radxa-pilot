# Legacy Panda compatibility

Owner requirement, November 6, 2026: build Chimera support so our Sunnypilot can
also support legacy Panda. Initial legacy target means the older F4 boards in
the reviewed CarrotPilot source: white, grey, black, UNO and DOS. Their hardware
generation does not determine the installed USB protocol. Other old firmware
generations require their own pinned contract before selection.

## What the SPI and USB paths mean

SPI is a direct hardware connection used by integrated Panda hardware. The
existing native host opens that connection through PandaSpiHandle. Keeping it
means existing SPI users still have their transport available. It does not mean
the Radxa-to-Chimera connection should use SPI: that connection will use USB.

The completed interface gives the native host one set of control/bulk methods.
A future PandaUsbHandle will implement those methods using libusb, alongside
the current PandaSpiHandle. The interface alone cannot discover or use USB.

The existing chimera_protocol.py handles original mailbox16/health43 decoding
for the separate Python receiver. It is not the new native USB backend or an
F4 health59 decoder. Preserve that distinction when reusing its tests.

## Separate transport, protocol and board behavior

- Transport moves control/bulk bytes over USB or SPI.
- Protocol profiles define CAN framing, status layouts, versions and commands.
- Board support defines MCU, GPIO, inputs, relay and firmware/recovery policy.

Use one native host transport interface for SPI and USB. Preserve current SPI
framing, buffer limits and device selection while adding the USB backend later.
Chimera retains its own board definition. Do not substitute Panda harness GPIO
or black-Panda power controls for Chimera's input and OBD-C assignments.

| Reference profile | CAN records | Health/version contract | Current project status |
| --- | --- | --- | --- |
| Current Panda, 8a16e089 | Six-byte header, payload, XOR | 49-byte health; DD returns two 32-bit layout hashes | Existing native SPI path |
| Carrot F4 reference, 69a2d3be | Six-byte header, payload, XOR; F4 classical CAN | 59-byte health; DD returns numeric health17/CAN4/CAN-health5 | Planned USB/status/lifecycle adapter |
| Original Chimera, d87892fa plus dirty source | 16-byte mailbox | 43-byte health; no matching modern DD handler | Existing separate read-only receiver; not managed Panda support |
| New Chimera target | Pinned modern classical CAN framing | Explicit identity and current status contract, still to implement | Firmware and host integration pending |

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
5. **T08 lifecycle:** explicit external USB selection, exclusive ownership and
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
is integrated. USB backend, legacy status decoding, complete RPC/source contracts
and real-device qualification remain pending.
