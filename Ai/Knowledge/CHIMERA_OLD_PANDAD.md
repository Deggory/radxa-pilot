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
