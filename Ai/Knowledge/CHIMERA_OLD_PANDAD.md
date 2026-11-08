# Original Chimera connection to native pandad

November 7, 2026. Research baseline: radxa/q8b `5722805f8aa185ab4cf19a438bdee771dca53b55`.
Owner direction: keep `chimera_old/`, improve its firmware later, investigate how
to connect it to Sunnypilot pandad. This report proposes host work; it does not
implement it or resume the halted new firmware. No hardware operation occurred.

## Connection boundary

```text
Original Chimera firmware (retained)
  USB descriptors + D6 version + D2 health43 + bulk IN 0x81/mailbox16
    PandaUsbHandle (existing, pinned serial/version, exclusive ownership)
      Chimera-specific native session + decoders (proposed)
        can -> existing RetroPilot CANParser / CarState
        isolated raw Chimera diagnostics
        later: separately qualified managed status adapter
```

Use the existing USB backend inside native pandad. The Python receiver is a
reference and available isolated monitor, not a second publisher to run beside
pandad. Firmware source is not uploaded merely to use the installed firmware.

## What exists and what blocks connection

| Boundary | Existing implementation | Required host work |
| --- | --- | --- |
| Identity | panda_identification.cc selects CHIMERA_MAILBOX for product Chimera, bbaa:ddcc, exact serial/version and health43; no C1/DD query | Retain the narrow profile; qualify the actual installed board/image before any live use |
| USB ownership | panda_usb.cc opens/claims exclusively, reads D6/D2 and bulk IN; Chimera control/bulk OUT denied | Reuse, preserving no-write policy and bounded failures |
| Original CAN/status parsing | chimera_protocol.py and chimera.py decode mailbox16/health43 and publish standard can in an isolated Python monitor | Native equivalent using literal fixtures and Python parity; no current/F4 parser substitution |
| Native session | PandaUsbStatusSession::open only admits LEGACY_F4_V17; its parser expects checksum-based 6+N-byte records and sample reads D2 plus C2 per-bus health | Add separate Chimera session/dispatch with health43; never issue C2 or reuse LegacyF4StatusSample |
| Native startup | pandad.py supplies --usb-status SERIAL VERSION; main.cc runs a passive loop and publishes can plus F4-specific diagnostic JSON | Dispatch by identified profile; generalize diagnostics without relabelling Chimera as legacyF4v17 |
| Managed Panda | Panda constructor accepts CURRENT only; get_state expects current health49 | Keep separate until an explicit Chimera state/capability contract exists; do not bypass the constructor check |
| Consumer status | PandaState availability profiles cover current and F4, not Chimera; observation-only states are rejected by normal consumers | If normal pandaStates is later required, add explicit Chimera identity/availability and consumer handling; do not impersonate black/red Panda |

## Proposed implementation increments

1. Native Chimera observation path: implement mailbox16 and health43 decoders,
   integrate profile dispatch and raw diagnostics into the existing native USB
   entry. Preserve arbitration/extended ID, DLC, payload and USB bus; reject bad
   records as a batch. Drop returned TX receipts and remote frames from ordinary
   vehicle reception. Publish timestamped empty batches to advance parser timeouts.
   Verify literal/historical fixtures, Python parity, malformed lengths/flags,
   fake USB ownership and that only D6/D2 and bulk IN occur. No sendcan or generic
   initialization. Expected files: new native codec/session tests plus existing
   status/main/build dispatch; split decoder tests from integration if needed.
2. Lifecycle completion: invalidate data on bad health, unplug or parser failure;
   release ownership, clear partial records and stale samples. Add bounded retry
   using the same explicit identity pin and clean identification each time; no
   fallback, reset, updater or other-device selection. Verify fake disconnect,
   interrupted read, duplicate identity and reconnect with no stale CAN/status.
   Do not carry partial mailbox bytes across sessions. Current native main exits
   on failure; reconnection is not already implemented.
3. Managed status, after observation works: define an honest Chimera-specific
   mapping for actual ignition/error facts and unavailable fields. Test real
   consumer behavior and freshness before allowing any normal ignition use.
   Existing source reports voltage/current=0 and safety_mode=17 constants; raw17
   must not be cast to today's safety enum or interpreted as configured safety.
   Absence of heartbeat-lost/per-bus health and modern safety results is not a
   healthy zero. Keep observation nonoperational until requirements are met.

First complete capability: unchanged legacy firmware -> native pandad -> standard
CAN messages and labelled raw Chimera diagnostics. This is achievable without a
firmware rewrite, subject to actual installed-image/USB qualification. It does
not establish driving/control support.

## Board and bus facts that the adapter must preserve

Original can.h maps host0/1/2 to MCU CAN1/2/3. The saved RetroPilot car package
selects host2, historically connector CAN2; actual present wiring is unverified.
Do not remap every frame to bus2. The canonical shared DBC and packaged copy
both hash to b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67.

The saved main.c produces angle0x50, engine0x75, speed0x76 and cruise0x100 only
when configured. send_can1_message writes MCU CAN1 TX mailboxes directly; this
is not a direct USB sensor stream. can_rx forwards physical CAN reception into
the USB queue; TX completion receipts are different. Therefore local sensor
visibility on the car parser's host2 cannot be inferred merely from USB opening.
Confirm routing/observed frames before claiming those signals are available.
Speed units remain unresolved for installed firmware (saved Hall producer uses
centi-km/h; old consumer convention differs). Preserve explicit calibration.

## Firmware semantics reserved for later improvement

Stock Panda 0xDC sets a safety model; this old Chimera handler changes
relay_req_usb. Moreover, this saved main loop drives PB0 relay directly from
ignition and comments out the request checks. A receive-only host does not
change that autonomous firmware behavior. No physical ignition/relay test ran.
Do not issue stock safety setup, heartbeat, bit-rate, configuration, reset, DFU
or flash commands through a generic Panda startup sequence.

The old bulk OUT handler can queue CAN, but can_send does not apply a modern
vehicle-specific safety hook. Wiring sendcan to it is not a completed active
integration. TX policy, relay authority, heartbeat/recovery and control mapping
remain a later explicit firmware/host scope. No claim that host-only adaptation
can supply missing MCU enforcement.

## Evidence and verification

Source pins/hashes: [receipt](../Evidence/chimera-old-pandad-route-20261107.json).
Relevant code: openpilot/selfdrive/pandad/{panda_identification.cc,panda_usb.cc,
panda_usb_status.cc,panda_usb_can.cc,panda_usb_publish.cc,main.cc,panda.cc,
chimera.py,chimera_protocol.py}, original chimera_old/firmware/chimera/{main.c,can.h},
openpilot/cereal/log.capnp, and opendbc_repo/opendbc/car/retropilot/values.py.
Existing contracts: ../../docs/RETROPILOT.md and
../../chimera/docs/LEGACY_PANDA_SUPPORT.md.

Fresh offline verification: 22 tests passed using project .venv Python with
warnings as errors: test_chimera_protocol, test_chimera, test_usb_startup.
All 76 preserved file sizes and SHA256 match chimera_old/SOURCES.json.
No native build/test rerun, physical USB claim, firmware execution, model/runtime
or REA artifact analysis. Source-first inspection sufficed. Unresolved exact
historical image source and installed board/image equivalence remain explicit.

## November 7 follow-up — exact USB wire comparison (QA20)

Source baseline56b073934605c7fe2e2e39b06a17ca0ee1704ec7; Panda8a16e089;
opendbc150f9371. Source review only, no device access or test rerun.

| Item | Original Chimera | Current Panda contract in Sunnypilot |
| --- | --- | --- |
| Interface | Vendor-specific USB; control EP0 | Vendor control/bulk USB |
| CAN RX / TX | Bulk0x81 /0x03 | Bulk0x81 /0x03 |
| CAN record | Fixed16bytes: little-endian `<II8s>` |6-byte header + DLC-selected payload |
| Header |32-bit RIR ID/flags +32-bit RDTR DLC/bus/time |1byte FD/bus/DLC +4bytes ID/flags +1byte XOR checksum |
|8-byte classic CAN payload |16bytes on USB |14bytes on USB |
| Maximum CAN payload |8bytes |64bytes in current CAN FD format |
| Additional record checksum | No Panda-style XOR byte | XOR over header/payload must be zero |
|D2 health |43bytes, `<8I7Bh2B>` |49bytes in CURRENT; separate F4v17 adapter uses59 |
|D6 | Firmware version string | Firmware version string |
|C1 /DD | No matching handlers | Hardware byte / two32-bit health+CAN version hashes |
|DC | Changes USB relay request variable | Sets MCU safety policy/model |

CAN payload checksum/counter rules from the canonical DBC are separate from the
USB record checksum. USB packet/transfer boundaries are not CAN message sizes.
Do not describe the6-byte header as a6-byte CAN payload or an incompatible USB
connector. The host translates transport records into standard can messages;
CAN IDs, payload bytes and bus identity must survive.

Current native --usb-status still runs the classic-only F4v17 observer, not an
H7/FD or old-Chimera runtime. Its format is6+N/XOR and health59. CURRENT Panda
library health is49 and its general CAN representation supports FD; that is a
separate admitted profile. Old Chimera remains Python receive-only plus native
identity/raw transport until its own session is implemented. No hard-coded
CAN version number is inferred from an older CAN5/CAN6 label; current identity
uses hashes of the actual pinned headers.

## November 7 — Owner scope: classic CAN only; 0xDC clarification (QA21)

Owner explicitly excludes CAN FD. Plan only classic CAN with0..8payload bytes;
FD support in a generic upstream header is reference capability, not project
scope. No source removal or implementation was performed for this explanation.
Source baseline ae145e4c58c9f154a46cff85b2d2d4b11742425b.

Host Panda::set_safety_model(mode,param) sends vendor commandDC with wValue=mode,
wIndex=param. Current Panda's handler calls set_safety_mode, initializes selected
hooks, falls back to SILENT on unsupported mode, configures relay/CAN mode and
reinitializes CAN. TX/RX/forwarding checks are model-dependent MCU rules, useful
for classic CAN too. This is not a guarantee that selecting a mode qualifies a
vehicle, and it is not the same as simply closing a relay.

Saved old Chimera DC handler:

```c
if (value == 0 || value == 3 || value == 19) relay_req_usb = 0;
else relay_req_usb = 1;
```

Those values match current enum silent0, elm3273 and noOutput19, but the old
handler only classifies the numbers: it does not install those modern policies
or process a safety parameter. Its health safety_mode=17 is a constant, not
proof of successful policy selection. No generic enum translation is admitted.

The operative saved loop sets relay_on from ignition_line OR ignition_can and
writes PB0. The condition using relay_req_obdc OR relay_req_usb is commented
out. Hence the handler changes a request variable, not directly the actual
relay; heartbeat timeout clearing that variable is not a proven relay drop.
These are source facts, not installed-image/electrical observations. Current
native Chimera USB transport denies DC/vendor OUT and permits only D6/D2 reads
plus CAN bulk-IN. Preserve that separation in the proposed host adapter.

## November 7 — Relay disconnect clarification (QA22)

The official Chimera wiki, freshly opened November7, documents12VR relay-switched
power on CAN0 ports1–3; CANH/CANL and USB are separate connections. Do not describe
this as physically opening CAN wires or disconnecting USB. Effect on a powered
Core depends on its wiring/other supplies and is not a tested actuator shutdown.
Saved main.c ignores relay_req_usb in the operative ignition-driven loop, so
neither DC0/noOutput nor host heartbeat expiry is a proven automatic relay-off
path with ignition present. No new implementation or physical action occurred.
Source baseline c1b625eeb854d90bfd04ad082d0a36b8c4d3836a; official source:
https://wiki.retropilot.org/index/hardware/chimera.

## November 7 — USB safety command fields (QA23)

DC + model + parameter means bRequestDC, wValue=model ID, wIndex=model-specific
parameter (both16-bit), with no data payload in the host control_write call.
This is not arithmetic, a CAN frame or an AI-model selection. ExampleDC/19/0
selects Panda noOutput with parameter0; actual parameter meanings are selected
firmware-rule-specific, often flags. No command was executed. Old Chimera19
only clears relay_req_usb and ignores wIndex; previous relay caveats remain.

## November 8 — Safety-rule inputs and remaining requirements (QA-20261108-01)

Rules consume model/parameter, CAN feedback, requested frames, time/history and
heartbeat. Model-dependent checks cover RX validity/freshness, driver override,
TX ID/bus/DLC and command magnitude/rate. Limits are compiled/model-defined;
wIndex is not a generic upload of all safety limits. Camera/model inference is
not a direct input to these MCU hooks. Output includes allow/block decisions
and control/fault state, rather than only relay behavior.

Local opendbc150f9371 includes retropilot_active.h's parameterized engine, but
retropilot_init supplies NULL and no qualified active production profile. The
car interface remains noOutput/dashcam-only. Old Chimera does not enforce this
engine in its TX path. Classic-only future work needs canonical DBC/bus routing,
measured endpoint limits/feedback calibration, override/timeout contract, MCU
hook integration and tests. No such implementation was resumed here.
Source baseline8fde793454f5908e88f6210d9c56b3cd41858212; official concept reference
https://docs.comma.ai/SAFETY/ opened November8. No physical qualification claimed.
