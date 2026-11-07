# Checked main startup — November 7, 2026

Owner selected the new Chimera firmware path and prioritized main.c. T03c1 now
connects the existing read-only boot-facts helper to actual ARM reset startup.
The C2-era host-only compatibility idea remains an alternative, not this path.

After RAM initialization, inherited interrupt cleanup and source-defined quiet
GPIO/USB/CAN clock gating, main checks the internal clock. It binds the existing
ordered MMIO callbacks without initializing timing or touching peripheral
registers. `chimera_main_prepare` then reads the existing F413 UID/reset/option
snapshot and records its validity. Main finishes in a named held/error state.
It does not call the USB service, choose a power profile or enable attachment.

The debugger sees `chimera_boot_magic`, `chimera_boot_state` and the new volatile
`chimera_boot_snapshot`. These are local RAM diagnostics, not a USB health ABI.

| State | Meaning |
| --- | --- |
| 0 RESET | Initial zeroed state |
| 1 CLOCK_READY | Preserved historical clock-only code; final success now uses5 |
| 2 CLOCK_FAILED | Clock selection failed; no UID/reset/option reads |
| 3 FAULT | Exception handler reapplies quiet outputs, clears snapshot validity and parks |
| 4 FACTS_FAILED | Blank/all-FF/unstable UID; snapshot invalid |
| 5 USB_HELD | Read-only snapshot succeeded; USB power/VBUS/recovery qualification still outstanding |
| 6 ARGUMENT_FAILED | Missing diagnostic destination or readable IO callback |

`facts_valid=1` means the helper obtained its stable UID/raw snapshot. It does
not prove a watchdog is stopped, attest firmware, authorize USB or qualify the
electrical state. Preparation clears validity before checking; failure preserves
previous raw bytes solely for diagnosis with validity0. Boot calls are serialized
and buffers/callbacks must have separate trusted storage. The callback cannot
report an invalid physical address as an ordinary error; the valid F413 address
space is a prerequisite. IRQs remain masked and all input acquisition remains
unstarted. A callback bus fault goes to the existing exception path.

`chimera_usb_mmio_bind` only assigns callback pointers to caller memory. The
existing initializer retains its DWT initialization/failed-output semantics and
then uses that binding. Main uses only binding and read32. No default current,
self-powered flag, session-valid override, PA9 repurposing, watchdog feed, option
write, settings access or USB/CAN operation is introduced. Clock/output behavior
before the snapshot is unchanged; register intent is not electrical cutoff proof.

Verification:30firmware tests pass with warnings as errors, including the two
new checks. The native test compiles the real preparation function in main.c
with ASan/UBSan, links the real boot reader and exercises65,536snapshots, bad
arguments, failed clocks, blank/unstable UID, validity revocation and canaries.
Writes/delays fail the fixture. Native mode excludes ARM reset/MMIO instructions;
the real ARM build separately confirms reset calls the binder/preparation and
preparation calls the boot reader, with no USB service call. Original startup,
GPIO, codec, USB/register/fault, copied-tree determinism and negative linker/image
checks remain passing. A temporary clock-guard mutation aborts the new fixture;
production source is unchanged by mutation. No assertions or warnings suppressed.

The initial ARM link failed because zero-initializing an IO struct generated an
unavailable libc memset in the freestanding build. Main now passes a callback
object only after successful full binding, or NULL on failure; no libc shim,
linker relaxation or warning suppression was added. Failed and corrected outputs
are retained in the evidence.

Current raw image7592bytes, projected legacy envelope7728bytes, globals32bytes,
reserved stack4096bytes, no undefined symbols. SHA256:
`fbce0bfa171b2bedca369d9913f6e3b661cadfa8ccf8a69063e0b9935b1020d1`.
The original7448-byte image/report is preserved in ignored build evidence;
its historical receipts remain unchanged. Build report now pins24source/header
files. Four prior files intentionally change (main.c, usb_mmio.c, usb_time.h,
build.py);19other previous firmware files remain byte-identical. Header main.h
and native/ARM startup tests are added. No physical run/flash is claimed.

Next main work: specify/test the qualified USB startup profile and recovery/fault
handling before service initialization or attachment. Power/VBUS/current-recovery
evidence remains required. Bulk/controller/health binding, inputs/Core Config/TX
policy and bench qualification remain separate. Host T08b2d publication/reconnect
is still queued after the owner's main-first priority.

[Receipt](../../Ai/Evidence/chimera-main-startup-20261107.json),
[power/recovery requirements](USB_STARTUP_REQUIREMENTS.md).
