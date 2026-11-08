## November8comparison follow-up

See [four identities and capability differences](PANDA_CHIMERA_COMPARISON.md).
The31source pins still match; this is a source follow-up, not a new hardware test.

# Panda functions and Chimera relevance

November 8, 2026. Project baseline `560e3ea87c0961bb9da2cf550b154011ae985184`, Panda `8a16e089`,
opendbc `150f9371`. Source inventory, not a hardware test or an exhaustive audit
of every car model, historical release, Jungle tester or separate comma-body
motor-control target. Current normal Panda application, bootstub/flasher, board
capability callbacks, Python API and local pandad paths are distinguished below.
Owner scope remains classic CAN only, old Chimera preserved, new rewrite halted.

## Major functions

| Function | What Panda does | Relevance to our project |
| --- | --- | --- |
| CAN reception | Services three CAN controllers, queues frames, labels buses/IDs/length and receipt metadata | Required, preserve actual bus routing |
| CAN transmission | Queues requested frames, applies safety and USB checksum checks before controller transmission; reports returned/rejected frames and errors | Later active work; old can_send lacks modern safety hook |
| CAN configuration | Bitrate, transceiver enable/multiplexing, loopback, queue clear and communication-buffer reset | Board-specific; do not send generic setup to old Chimera |
| Forwarding | MCU forwards selected traffic between buses under safety policy | Explicit routing only; not automatically needed for retrofit |
| USB protocol | Enumerates with identity, provides control RPCs and bulk CAN streams, assembles records split across transfers | Current6+N/XOR differs from old mailbox16 |
| SPI transport | Additional host transport on internal boards that implement it | Excluded from Radxa deployment; standalone red has_spi=false |
| Safety state | Selects compiled model/params, tracks allowed control state; checks RX integrity/freshness, driver override and TX limits | Needed before active control; exact checks are model-dependent |
| Liveness | Host heartbeat, engagement consistency and loss handling can select SILENT; separate watchdog timing monitors execution | Needs own old-Chimera contract; old request-variable timeout is not equivalent |
| Harness/ignition | Reads harness orientation/connection/ignition, selects CAN multiplexing and controls harness relay GPIOs | Different from Chimera12VR power relay; actual harness hardware matters |
| Board health | Uptime, available voltage/current/temperature, faults, reset flags, safety status, loads and communication counts | Translate only real supported measurements |
| Per-bus health | Bus-off, error states/counters, traffic counts, lost/buffer/checksum counts and configured bus speeds | Current C2 packet is absent in old Chimera |
| Runtime diagnostics | Timer, interrupt rates, debug-log reads, register-consistency/interrupt/fault monitoring and LEDs | Useful for diagnosis, not all faults imply identical shutdown action |
| Identity/provenance | Hardware type, version, MCU UID, provisioned identity and firmware signatures/layout versions | Required exact profile selection; do not infer from VID/PID alone |
| Power management | Power-save transceiver/interrupt behavior, wake monitoring; debug stop mode where compiled | Qualify physical circuit; stop is not a blanket onroad feature |
| Firmware boot | Bootstub checks image length, signed hash/version tag and approved signature before jump or flasher | Installed bootstub acceptance/recovery must be verified separately |
| Update/recovery | Host can enter bootstub/DFU, erase/program application and recover compatible hardware | Not part of observation startup; no operation run |
| Optional peripherals | Fan power/RPM, IR, siren, clock output, host bootkick/reset and SOM GPIO depending on board | Internal-board functions are not universal standalone Panda features |
| Host tooling | Python discovery/reconnect, packing/unpacking, health readers, programming and debugging utilities; test harnesses | API existence alone does not prove command/board support |

The red definition has no SPI or fan and uses unused callbacks for current
measurement, IR, siren, SOM read, amplifier and bootkick. It does implement
voltage reading and harness/CAN routing. Never report red's unused current
callback as a measured zero. TRES/CUATRO have SPI/fan and their own peripherals.
The retained historical black definition has GPS power/mode functions; this is
legacy board evidence, not a claim that current H7 firmware or every black
firmware implements the same API. Historical serial/UART/GPS capabilities require
separate version/board qualification.

Modern H7 CAN FD controls are present in the inventory for completeness but are
outside our project. Classic CAN uses the same overall transport/safety design
with at most8payload bytes. No FD feature was enabled or code removed.

## MCU versus host

Panda MCU moves CAN, performs policy checks and manages board hardware. It does
not run camera inference, path planning, the full car interface or the UI.
Host code performs DBC/CarState parsing, vehicle selection, controller computation
and diagnostic applications; raw CAN transport can carry their diagnostic
requests but Panda does not itself interpret all ECU diagnostic procedures.

Local pandad contains can -> cereal publication, sendcan -> USB packing with
stale-command rejection, PandaSafety configuration from CarParams, heartbeat,
pandaStates/peripheralState construction, log collection and peripheral control.
Those are host responsibilities. Our current pandad.py execs --usb-status and
main.cc admits only that passive observation entry; it does not start those
normal control threads. PandaUsbStatusSession admits F4v17 only. Native managed
CURRENT constructor support exists but is not an enabled normal entry point;
original Chimera remains a Python monitor plus native identity/USB handle until
its session is implemented. This source map is not a claim these paths ran.

Compatibility gaps found: native Panda::serial_read uses E0, set_uart_baud uses
E4 and enable_deepsleep uses FB; the pinned normal Panda handler has none of
those cases. Python set_can_enable uses F4, also absent from that handler.
Current debug logs use B6; debug stop uses B5. These names are not interchangeable.
Dormant native connect() also requests CAN-FD auto setup; the proposed
classic-only Chimera session must not call it. No fix was applied here.

## Complete normal-application control-command inventory

These35case labels are present in pinned main_comms.h; actual effects remain
board/mode/build-dependent. B5 is ALLOW_DEBUG-only; D1 ROM-boot entry in normal
application also has a debug gate. A DEBUG comment alone is not a compile gate.

| Command | Source meaning |
| --- | --- |
| `0xa8` | get microsecond timer |
| `0xb0` | set IR power |
| `0xb1` | set fan power |
| `0xb2` | get fan rpm |
| `0xb5` | request deep sleep, wakes on CAN or SBU |
| `0xb6` | read debug logs |
| `0xc0` | reset communications state |
| `0xc1` | get hardware type |
| `0xc2` | CAN health stats |
| `0xc3` | fetch MCU UID |
| `0xc4` | get interrupt call rate |
| `0xc5` | DEBUG: drive relay |
| `0xc6` | DEBUG: read SOM GPIO |
| `0xd0` | fetch serial (aka the provisioned dongle ID) |
| `0xd1` | enter bootloader mode |
| `0xd2` | get health packet |
| `0xd3` | get first 64 bytes of signature |
| `0xd4` | get second 64 bytes of signature |
| `0xd6` | get version |
| `0xd8` | reset ST |
| `0xdb` | set OBD CAN multiplexing mode |
| `0xdc` | set safety mode |
| `0xdd` | get health and CAN packet versions |
| `0xde` | set can bitrate |
| `0xdf` | set alternative experience |
| `0xe5` | set CAN loopback (for testing) |
| `0xe6` | set custom clock source period and pulse length |
| `0xe7` | set power save state |
| `0xe8` | set can-fd auto swithing mode |
| `0xf1` | Clear CAN ring buffer. |
| `0xf3` | Heartbeat. Resets heartbeat counter. |
| `0xf6` | set siren enabled |
| `0xf8` | disable heartbeat checks |
| `0xf9` | set CAN FD data bitrate |
| `0xfc` | set CAN FD non-ISO mode |

D0 provision identity must not be exposed as arbitrary user-visible secrets.
D3/D4 expose the two signature halves; DD exposes two layout hashes. C5 is a
relay-drive diagnostic, not a substitute for the selected safety contract.
F8 cannot disable heartbeat monitoring in an active car safety mode. Endpoint2
is unused in the normal application and is a flash-write stream in bootstub.
CAN RX/TX use bulk81/03. Standard USB descriptor/setup requests are additional
to this vendor-command list.

## Bootstub/flasher control inventory

Separate execution mode: opcodes can have entirely different meanings here.

| Command | Source meaning |
| --- | --- |
| `0xb0` | flasher echo |
| `0xb1` | unlock flash |
| `0xb2` | erase sector |
| `0xc1` | get hardware type |
| `0xc3` | fetch MCU UID |
| `0xd0` | fetch serial number |
| `0xd1` | enter bootloader mode |
| `0xd6` | get version |
| `0xd8` | reset ST |

Host DFU recovery is a further ROM-bootloader path, not this application's RPC
set. No reset, erase, unlock, programming or signature experiment was performed.

## Old Chimera differences and next work

Old firmware implements classic CAN receive/transmit, mailbox16 bulk records,
health43, firmware version/signature/reset/recovery commands, heartbeat counter,
CAN bitrate/loopback/clear commands, plus its own direct sensors, persistent
config and JSON RPC. Its active normal command numbers are:
`0xd1`, `0xd2`, `0xd3`, `0xd4`, `0xd6`, `0xd7`, `0xd8`, `0xdc`, `0xde`, `0xe0`, `0xe5`, `0xf1`, `0xf3`, `0xfb`, `0xfc`, `0xfd`, `0xfe`, `0xff`.

B4/B5 relay/OBD snippets are block-commented out, not active handlers. DC only
changes relay_req_usb; saved main loop bypasses that request and drives PB0 from
ignition. Its12VR power relay is not the Panda harness intercept relay. Its CAN
TX path does not enforce the modern safety dispatcher. Health's voltage/current
and safety17 placeholders are not verified sensors/policy state. DD/C1/C2 of
modern Panda are not available. FB/FC/FD/FE/FF belong to old config/JSON behavior,
not generic current-Panda meanings. Installed-image equivalence is unresolved.

The immediate classic-only host work remains a native mailbox16/health43 session
using pinned USB identity, ordinary can publication and raw diagnostics, then
lifecycle and qualified status. Active control separately needs measured limits,
feedback/override requirements and MCU enforcement. Optional peripherals need
not be copied into our project merely because another Panda board has them.

## Evidence and verification

[Machine-readable inventory and source hashes](../Evidence/panda-functions-20261108.json)
retains35normal commands,9flasher commands, original active command numbers,
Python Panda method names and31source hashes. Static extraction excludes C block
comments and verifies expected command counts; actual source effects were read.
No firmware/native builds or test suites were rerun, no real device client was
imported, and no REA artifact/runtime work was needed. Notebook checks do not
prove firmware or vehicle function. Official references freshly opened:
[versioned Panda README](https://github.com/commaai/panda/blob/8a16e089b88593914823743df29e1c30b7dd3e00/README.md)
and [safety concepts](https://docs.comma.ai/SAFETY/). Earlier studies are historical
source pins; this inventory uses the actual current local launcher gates.
