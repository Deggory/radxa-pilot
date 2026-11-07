# Main USB lifecycle coordinator — T03c2

November7 T03c3b: explicit legacy no-VBUS controller/service mode is now
implemented and tested offline. Default entry points remain unforced. Main copies
the selected mode; legacy requires NULL reader and keeps physical VBUS UNKNOWN.
Actual board main still selects NULL profile/reader and stays held.34firmware
tests pass; attachment/OTG cause handling and live qualification remain pending.
[Current session contract](USB_LEGACY_SESSION.md). Earlier checkpoints follow.

The coordinator in [main_runtime.c](../firmware/main_runtime.c) composes existing
components; it does not replace the USB driver or authorize attachment. Main
supplies a NULL profile in the current board build. Non-NULL profiles are used
only in offline fixtures until actual board requirements are qualified.

November7 T03c3a extends poll with required fresh VBUS observations before/after
the service call. Main still supplies no reader/profile. Power loss/uncertainty
stops the detached service, revokes the snapshot and latches USB_POWER; no actual
cable detector or attachment is bound. [Supervision contract](USB_POWER_SUPERVISION.md).
The original lifecycle below now uses the explicit reader argument.

## Configuration and ownership

Zero-initialize the runtime before first use. Keep its address and the diagnostic
destination stable, serialize all calls, and never reset/copy/move a live context.
IO/config/destination must not alias runtime state. Callbacks and their context
are trusted and must remain alive. IO callback members and configuration are
copied, so changing the caller's temporary objects cannot change active polling.
The driver points into its service-owned IO copy. See [service](USB_SERVICE.md)
for exclusive quiet-board, HSI/HCLK16 and clock-domain ownership requirements.

An explicit profile must supply self_powered0..1, max_power_2ma0..250,
poll_budget1..1,000,000 and event_budget1..32 plus all three IO callbacks.
These are API range checks, not measurements or board qualification. Invalid
explicit configuration is rejected before register access. A NULL profile uses
only read-only preparation; it cannot reuse a profile from an earlier run.
Preparation checks clock readiness and stable nonblank UID before service start.

## Lifecycle

Start accepts RESET or USB_STOPPED. Other states reject without IO or replacing
diagnostics. Preparation errors retain their main state; USB was never started.
A NULL profile ends USB_HELD and returns false. A valid explicit profile starts
the real service, compares its checked12-byte UID with main's snapshot and only
then enters USB_DETACHED/returns true. This is not host enumeration or readiness.
Raw reset/option words are diagnostics, not identity or recovery attestation.

Poll is valid only in USB_DETACHED and requires fresh PRESENT observations before
and after the real service call. It delegates the copied event budget and returns
0idle/1progress/2budget-exhausted/-1failure. Missing/unknown/absent/invalid power
observations stop the service and latch USB_POWER. A service error is retained
without another sample. Start/stop clear the local VBUS observation to UNKNOWN. Start and each
poll are bounded; main's detached loop intentionally continues while healthy.
Service invariants forbid attachment, IRQ/DMA enablement and session overrides.

Failures latch USB_FAILED, record the coordinator cause and the original service
error and invalidate the external snapshot. A service that already failed has
already attempted release; the coordinator does not silently repeat it. An
identity mismatch stops the still-detached service once. cleanup_ok and the
service's owns_usb flag expose incomplete release; a failed cleanup retains
ownership. There is no automatic retry, fallback, controller takeover or flash
recovery. If cleanup itself fails, the nested service retains its release error
while service_error preserves the initiating cause.

Explicit stop invalidates the snapshot and invokes service stop. Success enters
USB_STOPPED, retains prior diagnostic cause until next start, and permits full
requalification. Failed stop records USB_STOP/service RELEASE, remains failed
and retains ownership. A caller may explicitly retry stop after resolving the
cause. Repeated stopped stop performs no IO. This software lifecycle does not
implement DFU, signed-image rollback, watchdog handling or installed-board recovery.
The service does not restore changed PLL/HSE/debug settings.

## Verification and remaining boundaries

The native fixture links actual components with simulated registers, ASan/UBSan
and warnings as errors. Its51 scenarios include no-profile/failed-clock holds,
11bad arguments,20component startup outcomes,4ownership refusals,10poll faults,
identity discontinuity, copied configuration and failed-release retry. Every
DCTL write must retain soft-disconnect; unexpected register writes abort. It also
checks no IO occurs after failure or rejected restart. The existing44scenario
service fixture shares the same backend without replacing production functions.
Two temporary guard mutations are detected. ARM call inspection, image bounds
and deterministic builds pass in the original32-test firmware suite; current supervision extends it to33tests.

No device opened or flashed, no USB attach/CAN/input sampling, no Core Config/
relay/OBD-C behavior and no electrical or host end-to-end qualification. Current
A0/D6 bootstrap requests/capabilities and unsupported D2/C2 STALL remain unchanged.
See [startup](MAIN_STARTUP.md) and [receipt](../../Ai/Evidence/chimera-main-runtime-20261107.json).
