# Main startup — November 7, 2026

November7 owner clarification/source correction: Ocelot is the Chimera base
circuit with added I/O. Traced gateway schematic/board and Pro source/original PDF:
VBUS feeds shared5V through a diode; neither supplies an MCU VBUS detector. The
previous sensed supervisor cannot be bound to a nonexistent signal. Next is an
explicit legacy no-VBUS session mode tested offline, not a fake PRESENT reader.
Firmware remains held and unmodified. [Base-power findings](OCELOT_BASE_POWER.md).
Earlier missing/applicability descriptions below are historical and superseded.

T03c2/c3a connect main to the detached USB lifecycle coordinator. This extends
T03c1's checked UID/reset/option snapshot; the owner keeps the new firmware path
and main-first priority. The C2 host-only idea remains an unselected alternative.

Actual ARM reset initializes RAM, clears inherited interrupts, applies the quiet
board state and selects HSI/HCLK16. It binds ordered callbacks without peripheral
access, then calls `chimera_main_start`. **The board build passes NULL for the
USB profile**, so it captures the checked snapshot and parks USB_HELD (or an
explicit error), with USB/CAN gated and no acquisition. No board profile was
invented. The compiled poll loop is present but is not reached on held startup. It passes
NULL for the VBUS reader: even a future supplied profile would fail closed until
a physical reader is qualified and bound.

A caller supplying explicit configuration can instead prepare and poll the real
USB service while detached. This path is exercised with simulated registers,
not on a board. See the [coordinator contract](MAIN_USB_RUNTIME.md) for validation,
identity continuity, cleanup, ownership and explicit stop/restart semantics.

| State | Meaning |
| --- | --- |
| 0 RESET | Initial zeroed state |
| 1 CLOCK_READY | Preserved historical diagnostic; final snapshot success uses5 |
| 2 CLOCK_FAILED | Clock selection failed; no snapshot reads |
| 3 FAULT | Exception handler reapplies quiet outputs, invalidates snapshot and parks |
| 4 FACTS_FAILED | Blank/all-FF/unstable UID; snapshot invalid |
| 5 USB_HELD | Snapshot succeeded; no explicit USB profile selected |
| 6 ARGUMENT_FAILED | Missing destination/callback or invalid explicit configuration |
| 7 USB_DETACHED | Explicit configuration prepared the service; no attachment |
| 8 USB_FAILED | Service/coordinator failure latched; explicit cleanup required |
| 9 USB_STOPPED | Explicit stop succeeded; permits fresh start |

Debugger diagnostics are `chimera_boot_magic`, `chimera_boot_state`, volatile
`chimera_boot_snapshot` and the stable BSS `chimera_boot_runtime`. They are not a
USB health ABI. Snapshot validity means only that checked boot facts were read;
it does not attest firmware, prove a watchdog is stopped or qualify power.
Failures/stop revoke snapshot validity; old bytes may remain for diagnosis.
Callbacks require valid F413 address space and trusted, separate, live storage.
A physical bus fault follows the exception path rather than returning an error.

IRQs remain masked. The fault handler applies quiet outputs and records FAULT;
it does not attempt the service's multi-step cleanup from an exception. The
coordinator handles ordinary bounded start/poll/stop failures. No session-valid
override, PA9 repurposing, watchdog feed, flash/options/settings writes, CAN/input
operation or USB attachment is added. Quiet GPIO intent is not electrical proof.

Verification:33firmware tests pass with warnings as errors. New native coordinator
fixture links actual preparation/service/clock/timing/core/EP0/driver components
under ASan/UBSan and covers51 startup, polling, ownership, cleanup and restart
scenarios. Shared fake registers reject unclocked USB access, unexpected register
writes and attachment. ARM inspection verifies reset calls start/poll and the
coordinator calls the real service APIs. Existing65,536snapshot checks, USB and
codec tests, deterministic copied-tree builds, vector/linker/ELF rejection checks
remain passing. Temporary identity/no-profile mutations fail the new fixture.
The new power fixture adds16pre/post observation and cleanup/restart scenarios.
Both before/after power-guard mutations fail. No board run, flash or physical
measurement is claimed.

Current unsigned raw image8108bytes, projected legacy envelope8244bytes,
globals256bytes, reserved stack4096bytes, no undefined symbols. SHA256:
`b2c62ee6d05d5b6c720633daf4d34c2aecb3ca15166926a10257d54a9a7f7bb3`.
Build report still pins25source/header files. Relative to T03c2, main.c/main.h/
main_runtime.c change;22other inputs remain byte-identical. The prior8032-byte
image/report is preserved in ignored evidence; historical receipts are unchanged.
The local VBUS observation is cleared on startup/stop/exception and is not USB health.
See [observed power supervision](USB_POWER_SUPERVISION.md).

Next: establish the board power/profile/VBUS and installed recovery facts, then
specify the attachment/cable-loss policy before enabling a connection. Bulk/CAN/
operational health, inputs, Core Config and MCU TX policy remain later slices.
Host T08b2d passive publication/reconnect remains queued behind main-first work.

[Current receipt](../../Ai/Evidence/chimera-main-power-20261107.json),
[T03c2 receipt](../../Ai/Evidence/chimera-main-runtime-20261107.json),
[prior T03c1 receipt](../../Ai/Evidence/chimera-main-startup-20261107.json),
[power/recovery requirements](USB_STARTUP_REQUIREMENTS.md).
