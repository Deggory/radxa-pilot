# Panda, original Chimera and the new rewrite — November 8, 2026

Panda is the CAN interface and firmware policy layer between the host computer
and vehicle buses. The Radxa runs cameras, driving inference, planning and UI;
the interface MCU handles CAN, board hardware and configured safety rules.

## Separate the four names

| Name | Identity and source scope |
| --- | --- |
| Older black Panda | STM32F413/Cortex-M4, classic CAN. Stock older Panda firmware also had safety rules; safety is not a red-only invention. Version-specific capabilities require a pinned firmware. |
| Original Chimera in chimera_old/ | F413 retrofit board/application with three classic CAN buses, direct/pulse/analog inputs, persistent config/JSON RPC, power relay and OBD-C. It is a fork with its own firmware semantics, not a current Panda protocol clone. |
| Modern red Panda | STM32H725/Cortex-M7, classic CAN and CAN FD, with the modern Panda/opendbc interface and policy framework. Its H7 firmware cannot be flashed onto an F413. |
| Our new chimera/ | A halted F413 firmware rewrite on the same board hardware, plus associated Radxa host work. It is incomplete and is not a new red-Panda board. |

## What current Panda offers beyond preserved Chimera

| Area | Preserved original Chimera | Current Panda at 8a16e089/opendbc150f9371 |
| --- | --- | --- |
| Command safety | can_send queues frames without the modern safety dispatcher | Ordinary host TX is checked by selected safety hooks; allowed ID/bus/DLC, command limits, driver override and RX freshness/integrity depend on the model |
| Safety selection | DC changes relay_req_usb; no model installed by that handler | DC selects/initializes compiled safety model and parameter |
| Host loss | Timeout changes a request variable; saved relay loop ignores request gating | Firmware tracks heartbeat/control state and can fall back to SILENT under its defined conditions |
| Status and diagnosis | health43 has limited/placeholder fields; no current C1/C2/DD handlers | Hardware identification, explicit packet-layout hashes, per-bus error/counter/load data and richer safety/fault state |
| CAN USB records | Fixed16-byte mailbox, classic payload0..8, no extra record-XOR byte | Six-byte header plus payload with an extra packet XOR checksum; modern framing also represents CAN FD |
| Hardware CAN FD | Not available on F413; rewrite cannot add it | Supported on H725 hardware, outside our classic-only scope |

Old Chimera already has CAN RX/TX, bitrate/loopback/clear controls, a heartbeat
counter, version/signature/reset/recovery functions and configuration support.
Do not advertise every watchdog, signed image or USB function as new-only.
Conversely, Chimera adds direct IGN/VSS/CPS/BRAKE/ADC1/ADC2 and its retrofit
power/configuration interfaces; red Panda is not a connector-compatible
replacement for those. The board-specific red definition has no SPI/fan and
uses unused callbacks for several internal-board peripherals; those are not
universal Panda functions or measured zero sensor values.

Chimera's relay switches12VR power, not CANH/CANL. In the preserved loop PB0
follows ignition; the USB request condition is commented out. Therefore DC or
heartbeat loss cannot be claimed to cut relay power while ignition stays on.
Physical wiring and exact installed image/source equivalence remain unverified.

## What the new Chimera rewrite actually adds

Saved offline validation covers explicit USB lifecycle/fault/cancel/reconnect
state handling, bounded stream/classic-CAN packet checks, identity/read-only
request models and conservative held GPIO/startup behavior. Those are useful
engineering foundations. Actual main still passes a NULL power/profile reader
and remains USB_HELD. Full operational bulk/CAN flow, direct input acquisition,
configuration/RPC parity, qualified MCU active safety and actual board validation
remain unfinished. The last saved36firmware-test result is historical; it was
not rerun for this answer. Implementation remains halted.

Current Radxa pandad starts the passive F4v17 entry. It recognizes original
Chimera identity and has a guarded USB handle/Python monitor, but a native
mailbox16/health43 session is still proposed. Modern Panda functionality in source
does not mean our launcher currently starts the normal active Panda threads.

## Evidence and limits

Current project baseline efe4e9c951ebd1a994cc04a31ef36533bda65e4d. All31
source hashes from the prior Panda inventory still match; all76preserved old
Chimera file sizes/hashes match. Four selected rewrite source hashes are pinned
in [the receipt](../Evidence/panda-chimera-comparison-20261108.json).
Read [full Panda inventory](PANDA_FUNCTIONS.md), [old host route](CHIMERA_OLD_PANDAD.md),
and [rewrite lifecycle](../../chimera/docs/USB_LIFECYCLE.md).

Fresh primary references: [pinned Panda README](https://github.com/commaai/panda/blob/8a16e089b88593914823743df29e1c30b7dd3e00/README.md),
[comma safety concepts](https://docs.comma.ai/SAFETY/) and
[Chimera hardware documentation](https://wiki.retropilot.org/index/hardware/chimera).
The wiki's broad Panda-API compatibility claim is qualified by the preserved
source's actual packet/command semantics; it is not proof of current host parity.

Used the existing teacher knowledge graph as a route, followed source/notes,
applied relevant explanation/review skills and Unlazy's final claim reconciliation.
No gate ledger is needed for this factual reply. No REA binary/runtime question,
new test suite/build, USB/relay/CAN/device/flash, upstream update or push. The
upstream inbox remains stale at November4 with its saved update hold unchanged.
