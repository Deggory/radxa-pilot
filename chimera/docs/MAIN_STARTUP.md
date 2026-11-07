November7 T03c4 supersedes the detached-only lifecycle limitation below:
explicit attach, OTG cause ACK, suspend/resume, reset cancellation, session-end
release and explicit fresh reconnect now pass offline.36firmware tests/92new
composed scenarios; actual board startup remains held and unflashed.
Current image9064bytes/globals264. Full-roadmap rough estimate30%, physical0%.
Next board USB startup binding, then bulk/CAN RX and operational status.
See [current lifecycle contract](USB_LIFECYCLE.md); earlier receipts remain historical.

# Main startup — November 7, 2026

November7 T03c3b: explicit legacy no-VBUS controller/service mode is now
implemented and tested offline. Default entry points remain unforced. Main copies
the selected mode; legacy requires NULL reader and keeps physical VBUS UNKNOWN.
Actual board main still selects NULL profile/reader and stays held.34firmware
tests pass; attachment/OTG cause handling and live qualification remain pending.
[Current session contract](USB_LEGACY_SESSION.md). Earlier checkpoints follow.

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

Verification:34firmware tests pass with warnings as errors. New native coordinator
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

Current unsigned raw image8316bytes, projected legacy envelope8452bytes,
globals260bytes, reserved stack4096bytes, no undefined symbols. SHA256:
`745f66c5c408a8c046c6c7ed3f3c3edc576b9743b9a0b35d860770a1f24e8826`.
Build report still pins25source/header files. Relative to T03c3a/T01b, seven inputs
change (main.h, main_runtime.c, usb_hw.c/h, usb_service.c/h, usb_driver.c),18remain
unchanged. Actual main.c remains byte-identical and selects no profile. Previous
8108-byte artifacts are preserved; historical receipts remain unchanged.

Next: establish the board power/profile/VBUS and installed recovery facts, then
specify the attachment/cable-loss policy before enabling a connection. Bulk/CAN/
operational health, inputs, Core Config and MCU TX policy remain later slices.
Host T08b2d passive publication/reconnect remains queued behind main-first work.

[Current receipt](../../Ai/Evidence/chimera-legacy-session-20261107.json),
[T03c3a receipt](../../Ai/Evidence/chimera-main-power-20261107.json),
[T03c2 receipt](../../Ai/Evidence/chimera-main-runtime-20261107.json),
[prior T03c1 receipt](../../Ai/Evidence/chimera-main-startup-20261107.json),
[power/recovery requirements](USB_STARTUP_REQUIREMENTS.md).
