# Observed VBUS supervision — T03c3a, November 7, 2026

November7 owner clarification/source correction: Ocelot is the Chimera base
circuit with added I/O. Traced gateway schematic/board and Pro source/original PDF:
VBUS feeds shared5V through a diode; neither supplies an MCU VBUS detector. The
previous sensed supervisor cannot be bound to a nonexistent signal. Next is an
explicit legacy no-VBUS session mode tested offline, not a fake PRESENT reader.
Firmware remains held and unmodified. [Base-power findings](OCELOT_BASE_POWER.md).
Earlier missing/applicability descriptions below are historical and superseded.

Main polling now checks a caller-provided VBUS observation before and after each
bounded detached service poll. This implements the software loss/unknown response;
it does not detect the real cable yet. The actual board build supplies NULL for
both its power profile and its reader, so it still captures boot facts and parks
USB_HELD without starting USB. No attachment API or physical profile is enabled.

## Evidence and scope

Teacher notes and original sources were consulted first. The Chimera hardware
folder supplies a board photo/guide; gateway/pro schematics are separately named
boards. The saved OBD-C drawing is the comma connector reference. None establishes
this Chimera revision's USB power tree or VBUS detector. Original Ocelot USB code
forces B-session-valid and the board map reserves PA9/PA10 for USART1. Retain those
mappings; a software override or a schematic for another board is not detection.
See [power/recovery evidence](USB_STARTUP_REQUIREMENTS.md) and its pinned sources.
No new electrical fact or installed-board recovery proof was found in this slice.

## Reader contract and behavior

`chimera_vbus_io` contains a context and a sample callback. Inputs are serialized,
trusted, bounded, non-aliasing and remain stable/alive throughout the call. A
production callback must use an independently qualified physical source and
report UNKNOWN whenever that source is stale, unavailable or faulted. No physical
pin, ADC threshold, debounce interval, freshness duration or supply mode is chosen
by this software API. A callback returning a constant PRESENT is only a native
test fixture; it is not a production power qualification mechanism.

| Observation | Coordinator action |
| --- | --- |
| PRESENT before and after successful poll | Return service result0/1/2 and remain detached |
| UNKNOWN, absent reader, missing callback, invalid enum | Normalize UNKNOWN, latch USB_POWER, revoke snapshot and stop service |
| ABSENT | Record ABSENT, latch USB_POWER, revoke snapshot and stop service |
| Service fails after first PRESENT sample | Retain USB_POLL/original service cause; do not sample again |
| Runtime held/stopped/failed or NULL | Return-1 without register IO or invoking reader |

`runtime.vbus` is the last normalized observation, not a durable power grant or
USB health field. Start and explicit stop reset it to UNKNOWN; the exception handler also clears
it. Each new poll samples afresh and cannot reuse a prior PRESENT. The function
does not store the reader for later use or acquire hardware itself.

On a power refusal, the existing service stop performs its detached cleanup once.
Successful cleanup invalidates EP0/driver state and releases owned USB. Failed
cleanup retains ownership and its nested RELEASE error. The coordinator records
USB_POWER, preserving service_error=OK when the power observation was the initiating
cause. Later polls/start do not sample or retry cleanup. Explicit stop can retry;
a successful stop permits fresh start. Restored presence does not auto-reconnect.
No PLL/HSE/debug restoration or watchdog/DFU/flash recovery is implied.

A bounded service poll can run between the two samples. This does not promise
instantaneous detection, interrupt-level response or a measured millisecond
bound. A physical reader and the poll scheduling/response budget still need
qualification. The exception path quiets outputs, invalidates facts/observation
and parks; register intent remains separate from electrical cutoff proof.

## Conditions before a future attached mode

The current service deliberately rejects a cleared soft-disconnect bit. It cannot
be made operational by adding a callback or clearing SDIS elsewhere. A separate
attached-mode slice must establish all of these before enabling a connection:

1. Verify exact board power paths, actual host-VBUS indication/levels, supply
   isolation, descriptor power/current profile and suspend behavior.
2. Verify installed bootstub, accepted image packaging, settings preservation and
   an independent working restore path for the intended image/board.
3. Bind reviewed USB pins, timing/clock and physical reader; prepare EP0 detached
   with stable UID, no session-valid override or default stock-board identity.
4. Check fresh qualified presence before attachment; define bounded scheduling,
   reset/suspend/session-end/loss response and test the attached invariants.
5. On loss/uncertainty, disconnect, cancel transfer/session state and release the
   controller through the qualified path. Never reuse stale commands/status;
   any later reconnect must requalify state and host ownership explicitly.

These are remaining requirements, not implemented attachment/recovery features.
CAN/bulk/operational health, direct inputs, Core Config and MCU TX remain later.

## Validation and progress

33firmware tests pass with warnings as errors. The new ASan/UBSan native fixture
links actual preparation/service/clock/core/EP0/driver and covers16scenarios:
missing/invalid/unknown/absent readings before polling, loss after a real driver
reset/budget event, healthy repeated observations, no stale reuse after restart,
failed cleanup/explicit retry, original service-fault precedence and production
held-path silence. The previous51scenario coordinator fixture now supplies an
explicit synthetic PRESENT reader; its existing failures remain covered.
Two temporary mutations removing the before/after guards both fail assertions.
ARM call inspection, copied-tree determinism and negative image/linker checks pass.

**Current stage:100% implemented and verified offline. Overall planning estimate:
approximately25% complete /75% remaining. New-firmware hardware validation:0%.**
The overall figure is an engineering estimate for the unequal T01–T20 roadmap,
not a measured effort fraction or readiness score. See the
[progress guide](PROGRESS_EXPLAINED.md) for the standing reporting rule.
[Receipt](../../Ai/Evidence/chimera-main-power-20261107.json).
