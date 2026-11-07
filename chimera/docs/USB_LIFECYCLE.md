# USB attachment and session lifecycle — T03c4

November 7, 2026. This increment completes the offline control-endpoint path from
main coordinator through service and packet driver: prepare, explicit attach,
enumerate, suspend/resume, reset, session end and explicit fresh reconnect.
The actual board startup still supplies a NULL profile and remains USB_HELD.
The attach APIs are retained in the ARM image; no image was flashed or run.

## Entry and state transitions

`chimera_main_start` still prepares DETACHED only. The new separate
`chimera_main_attach(runtime, vbus)` checks the copied session policy and power
before and after calling `chimera_usb_service_attach`. UNFORCED requires fresh
PRESENT samples; LEGACY_NO_VBUS requires NULL reader and keeps VBUS UNKNOWN.
The Ocelot base has no MCU VBUS detector; an override never supplies a measurement.

Service attachment checks its detached invariants, holds SDIS for a bounded
10,000 microsecond delay, checks again, drains at most32controller events and
checks the resulting invariant before clearing SDIS. A saturated drain refuses
attachment. The driver requires initialized, idle, unaddressed/unconfigured EP0
with no armed/pending transfer, then clears SDIS and checks its readback. The
service checks the attached invariant afterwards. GPIO/descriptor power values
are not selected or electrically qualified by these APIs. Global IRQ and DMA
remain disabled; calls must be serialized and the service polled regularly.

| Event or action | Result |
| --- | --- |
| Explicit attach from DETACHED | ATTACHED after checked SDIS clear |
| Confirmed suspend, DSTS.SUSPSTS=1 | SUSPENDED; retain address, configuration and armed control transfer; pause endpoint work |
| Host wake, DSTS.SUSPSTS=0 | ATTACHED; retained control transfer may finish |
| Coalesced suspend/wake | Current DSTS decides; acknowledge only observed event bits |
| USB reset | Cancel EP0 generation/address/configuration; discard old transfers; clear suspension and prepare enumeration |
| OTG session end, SEDET | Cancel EP0 and disconnect before old reset/completion; release PHY/reset/clock; return3 and STOPPED |
| Explicit stop | Full release and snapshot revocation |
| Reconnect after stop/session end | Explicit start with full profile, then attach; identity and preparation checked again |
| Fatal cause/invariant/cleanup failure | FAILED; no automatic retry; retained ownership when cleanup fails |

Reset supersedes coalesced suspend/wake. Session end supersedes reset and endpoint
completion. A normal suspend is not declared a disconnect: retaining its address
and transfer allows host resume. A powered legacy board can later receive a host
reset after cable reconnection and enumerate afresh. Without a detector, the code
cannot distinguish idle/suspend from cable removal or assert cable presence.
There is no elapsed-time unplug deadline, SOF/heartbeat freshness guarantee or
remote-wakeup signaling. Suspend current and physical behavior remain unmeasured.

## OTG cause handling and invariants

GOTGINT is read once per event and acknowledged with exactly that snapshot using
W1C, never a second-read/RMW. ADTOCHG and DBCDNE are acknowledged as benign;
SEDET ends the attached session. HNP/SRP/ID changes, unknown causes and empty
summary events fail. Wrong controller role/mode, connector-role change and
unsupported LPM fail. Detached suspend/wake/session-end events still fail.

Service invariants cover RCC USB access, HSI/system-clock profile, SDIS matching
the expected phase, global IRQ/DMA disabled, PCGCCTL STOPCLK/GATECLK clear,
exact selected session overrides, PHY powered and VBDEN off. They do not implement
continuous PLL48 lock/configuration monitoring. Failed attachment, post-poll drift
or power checks revoke facts and release. A reset/gated core is never accessed as
USB MMIO; reset/gate readbacks establish quiet release. Failed release retains
ownership for explicit retry. No board output, CAN controller, relay, watchdog,
flash/config write, normal health or operational capability is enabled.

## Sources and verification

The implementation follows the pinned ST HAL
[PCD event handling](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Src/stm32f4xx_hal_pcd.c)
and [connect/disconnect functions](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Src/stm32f4xx_ll_usb.c),
local ST F413 CMSIS V2.6.0 bit definitions and original Ocelot USB source.
The current RM0430 PDF fetch exceeded the web tool limit; no new full manual
review is claimed. Existing readable source and GNU ARM tools supplied evidence;
no REA provider result or hardware runtime was fabricated.

36firmware tests pass with warnings-as-errors, including92new composed ASan/UBSan
scenarios: descriptor/address/configuration/A0 enumeration, retained armed transfer
through suspend/resume, reset cancellation, both power policies,40fresh reconnect
cycles, session-end priority, late OTG cause preservation, failed delay/attachment/
readback/pre/post-drain invariants, power loss, gated access and cleanup retry.
The test backend opts into attachment explicitly while previous fixtures retain
their no-attach assertion and strict peripheral write/access guards.

Three copied-source mutations were caught: second-read OTG acknowledgment,
endpoint progress during suspend and missing post-attach power guard. ARM tests
verify the retained main→service→driver attachment chain, absence of a default
startup attach call, deterministic builds, vectors and negative ELF/linker cases.
Independent review covered the production delta and lifecycle fixture; its actual
versioned result is recorded in the receipt. No tests/assertions/warnings skipped.

Unsigned image9064bytes, projected legacy envelope9200, globals264, stack4096,
no undefined symbols; SHA256
`341ef240b4af887d74ae8a7800b892d116e8aca8ddf1af03640492d6ef83badd`.
Seven of25build inputs changed;18unchanged. Previous8316-byte artifacts retained.
[Receipt](../../Ai/Evidence/chimera-usb-lifecycle-20261107.json).

## Progress and next deliverables

This lifecycle stage is100% implemented/verified offline. Revised full-roadmap
planning estimate: **about30% complete /70% remaining**, physical validation **0%**.
This replaces the earlier25% estimate because an integrated lifecycle is now
implemented, rather than incrementing for each helper/test. It is not a measured
fraction of time, effort or readiness, and T03 remains partial until the board is
qualified and bound. Earlier25% checkpoints remain dated historical records.

Next deliverable: opt-in board USB startup binding (PA11/PA12, explicit descriptor
power profile and retained recovery boundaries), tested without hardware actions.
The actual power/current/installed recovery evidence must be resolved before a
live attachment claim. Then bind bulk endpoints to the existing modern CAN codec,
implement passive CAN-controller RX and modern operational status. Host passive
normal-status publication/reconnect remains queued separately; inputs, Core Config,
MCU TX policy, relay and OBD-C keep their roadmap tasks. No SPI is reintroduced.
