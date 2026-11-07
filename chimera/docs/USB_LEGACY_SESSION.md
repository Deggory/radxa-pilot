# Explicit legacy no-VBUS session mode — T03c3b

November7,2026. The owner identifies Ocelot as Chimera's base circuit with I/O
added. The [power trace](OCELOT_BASE_POWER.md) shows no MCU VBUS-sense connection;
the original F413 USB code forces B-session-valid. This increment implements
that controller policy as an explicit detached-only option, preserving unforced
entry points and truthful physical-power status. No board connection is enabled.
Legacy here names controller session/power handling only. It does not select an
old CAN/health format; framing, requests and bootstrap capabilities are unchanged.

## Modes and API

| Mode | Core/session policy | Main polling | Physical VBUS status |
| --- | --- | --- | --- |
| UNFORCED=0(default) | Clear A/B session overrides | Requires fresh PRESENT before/after each service poll | External trusted sampler's last normalized observation |
| LEGACY_NO_VBUS=1(explicit) | Set only BVALOEN/BVALOVAL; A overrides clear | Requires NULL reader; poll actual service without substituting a sample | Always UNKNOWN |

`usb_hw.h` defines this local enum and the override masks. The ST F413 CMSIS
V2.6.0 header defines AVALOEN/AVALOVAL at bits4/5, BVALOEN/BVALOVAL at6/7 and
GCCFG VBDEN at21. Legacy selects GOTGCTL mask0xC0; the exact permitted override
fields are checked with0xF0. VBDEN remains off in both preparations. A software
B-session override is not a physical power/cable observation or USB readiness.

The new `chimera_usb_core_detached_mode` and `chimera_usb_service_start_mode`
validate mode before register IO. Existing unsuffixed entry points always choose
UNFORCED. No auto-detection, fallback or reuse of a previous legacy selection.
Main's config gains session_mode, validated and copied with other caller values;
the service owns its immutable copy. Enum values are not a new wire ABI/request.
Contexts remain zero-initialized/stable/non-aliasing and calls serialized as in
[the coordinator contract](MAIN_USB_RUNTIME.md).

Main checks agreement between its copied mode and the service. Invalid/mismatched
mode or a supplied reader in LEGACY_NO_VBUS latches USB_ARGUMENT, releases the
service and invalidates the snapshot. It never ignores a supplied reader or
silently changes policy. A NULL profile still means checked facts/USB_HELD.
**Actual ARM main remains unchanged and supplies NULL profile and NULL reader.**
No descriptor power/current value or GPIO binding has been selected for the board.

## Controller lifecycle and cleanup

Core preparation sets SDIS before powering/resetting the PHY, programs only the
selected session override and checks its readback. All modes remain detached:
no clearing SDIS, global IRQ/DMA enable, USB pin changes, CAN or input acquisition.
The service checks exact mode bits and PHY-on/VBDEN-off before/after each poll.
Missing/partial B override, foreign A override, enabled VBDEN, attachment, clock/
IRQ/DMA violations and post-poll drift fail and invalidate the driver/session.

Driver USB-reset handling cancels EP0 generation/address/configuration while retaining the
selected controller policy. Wrong controller role, suspend and an OTG-summary
interrupt terminate polling through the existing driver failure path. OTG causes
are not decoded/acknowledged in this increment: even a benign summary event is
currently unsupported. The original source acknowledges GOTGINT; reviewed cause
handling is required before an attached mode. No resume, cable-loss timing,
SOF/heartbeat freshness or automatic reconnect is implemented or claimed.

Core failures and accessible service cleanup clear A/B session override fields
while disconnected; service release then powers down PHY, holds reset and gates
the USB clock. If the controller is already gated/reset, release does not access
USB registers. Reset/gate readback failure retains ownership/error for explicit
stop retry. Successful stop resets the local mode to UNFORCED. Old facts/commands
are not re-admitted by an automatic restart. A still-present fault can fail again
after explicit reprepare; cleanup success is not a cure for the underlying event.
This is not watchdog, image signing, DFU or installed-board recovery.

## Verification and remaining work

34firmware tests pass with warnings as errors. New native ASan/UBSan fixture links
actual main preparation/runtime, service, clock/timing/core, driver and EP0.
Its61scenarios include both modes across20startup outcomes each, invalid modes
before IO, copied selection, reset cancellation, NULL-profile non-reuse, refusal
of mixed reader/policy and live policy mismatch,12invariant/event faults, rejected
override writes, failed cleanup/explicit retry and persistent fault requalification.
The shared fake always rejects unexpected register access, unclocked USB access
and attachment; its fault injections do not bypass those assertions. Previous
51coordinator and16power scenarios retain explicit UNFORCED configuration.

Three temporary mutations falsely reporting PRESENT, dropping exact mode checks
and retaining overrides during cleanup all fail assertions. ARM symbol/call
checks, deterministic copied-tree builds and negative image/linker tests pass.
The first new restart check incorrectly expected success while its injected
suspend bit remained set. The fixture now proves that refault first, then clears
the injected condition before expecting successful explicit restart. Production
logic was not weakened. No assertion or warning suppression was introduced.

Unsigned raw image8316bytes/projected8452, globals260/stack4096; SHA256:
`745f66c5c408a8c046c6c7ed3f3c3edc576b9743b9a0b35d860770a1f24e8826`.
25build inputs:7intentionally changed and18unchanged. Prior8108-byte artifacts
are preserved in ignored evidence; historical receipts remain unchanged.

**This stage:100% implemented/verified offline. Overall rough planning estimate:
about25% complete/75% remaining; new-firmware hardware validation:0%.**
Next: reviewed OTG cause handling and controlled attached-state lifecycle offline;
actual board profile/pins, current/recovery qualification and bench work remain.
Bulk/CAN/operational health, inputs, MCU TX and Core Config are later stages.
Host T08b2d remains queued. [Receipt](../../Ai/Evidence/chimera-legacy-session-20261107.json).
