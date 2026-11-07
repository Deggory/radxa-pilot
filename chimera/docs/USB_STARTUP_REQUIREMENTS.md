November7 T03c4 supersedes the detached-only lifecycle limitation below:
explicit attach, OTG cause ACK, suspend/resume, reset cancellation, session-end
release and explicit fresh reconnect now pass offline.36firmware tests/92new
composed scenarios; actual board startup remains held and unflashed.
Current image9064bytes/globals264. Full-roadmap rough estimate30%, physical0%.
Next board USB startup binding, then bulk/CAN RX and operational status.
See [current lifecycle contract](USB_LIFECYCLE.md); earlier receipts remain historical.

# Power, UID and recovery requirements before USB startup

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

November7 T03c3a implements pre/post VBUS observation supervision offline. An
unknown/lost indication stops the detached service and latches failure. No actual
reader/profile is selected; all electrical/recovery gaps below remain unresolved.
[Supervision contract](USB_POWER_SUPERVISION.md).33firmware tests pass, no hardware run.

November7 T03c2: the main lifecycle coordinator is implemented and tested offline,
but the board build still supplies no profile and stays USB_HELD. None of the
power/VBUS/installed-recovery gaps below are resolved by this software lifecycle.
[Coordinator](MAIN_USB_RUNTIME.md). Earlier checkpoint descriptions are historical.

November7 T03c1 update: main now invokes read-only boot-facts preparation and
ends in explicit USB_HELD/error diagnostics. This binds no USB service or power
profile and resolves none of the electrical/recovery gaps below.
[Main startup](MAIN_STARTUP.md). Historical image/helper descriptions follow.

November 6, 2026 — T03b3a requirements and read-only boot-facts helper complete
offline. T03b3 attachment/startup qualification remains partial. This contract is
not a flashing procedure or permission to operate hardware.

T03b3b now supplies the [detached startup/service library](USB_SERVICE.md), with
23combined offline tests. Main remains parked; the qualification gaps below are
unchanged. Next board software work is the status/capability contract.

## Decisions established from the evidence

1. Radxa's normal data connection is Chimera's USB Type-B port. OBD-C remains a
   separate accessory interface. Preserve all three CAN bus identities and inputs.
2. USB attachment stays disabled by default. There is no approved self-powered
   flag, current-draw value, VBUS detector or valid-session override for this board.
3. UID supplies24lowercase hex serial characters from12bytes in ascending memory
   order. Use the existing strict EP0 formatter; do not hardcode the historical
   board serial or import a stock Panda board identity.
4. Read raw reset/option settings without clearing flags, starting/feeding the
   watchdog, changing protection/options or programming flash. Raw option/reset
   information cannot prove that a software-started watchdog is currently stopped.
5. Preserve the installed bootstub and entire settings erase sector. Raw bootstrap
   bytes are not a signed legacy image. No generic Panda/H7 updater/recovery path.
6. A detached startup/service sequence can be developed offline independently;
   actual attachment and release require the electrical/recovery evidence below.

## Power and VBUS

The [official Chimera wiki](https://wiki.retropilot.org/index/hardware/chimera),
rechecked November6, describes USB Type-B as the host connection and IGN as a
source that powers the board when USB is absent. It describes battery/IGN and
auxiliary outputs, but does not supply the exact USB power tree, VBUS detector,
reverse-current behavior or measured consumption for the owner's revision.
Its broad Panda-API compatibility claim does not specify a modern USB ABI.

Original Ocelot d87892fa source assigns PA11/PA12 to USB D-/D+. The common GPIO
initializer assigns PA9/PA10 to USART1. Original main/USB initialization sets
GOTGCTL BVALOEN/BVALOVAL, forcing B-session-valid in software while VBDEN sensing
is not enabled. This explains old software intent; it is not evidence that PA9
is wired to VBUS, that cable removal is sensed, or that mixed power is isolated.
Do not repurpose PA9 or inherit the override without board-specific evidence.

| Required evidence | Why it matters | Current result |
| --- | --- | --- |
| Exact MCU/PCB revision and power schematic or verified tracing | Associate firmware with the actual regulator/USB/IGN/battery paths | Owner identifies Ocelot base; power paths traced; assembled-board/I/O differences and measurements remain open |
| USB-only, external-only and simultaneous supply paths | Establish backfeed/isolation and which source keeps MCU/PHY alive | Base drawings show diode-fed USB plus external regulator on shared5V; no electrical qualification |
| VBUS presence/loss detector, pin/levels and debounce | Attach only with valid host power and detach on removal while externally powered | Base drawings show no MCU detector route; original F4 firmware forces B-session-valid |
| Descriptor self-power/current values and suspend behavior | Report the qualified power profile and meet its operating limits | Caller parameters exist; no measured profile approved |
| Disconnect/reset/brownout/fault states on D+/D-, relay and OBD-C outputs | Verify actual electrical behavior beyond intended register values | Not measured for this firmware |

Future bus-powered-only operation needs evidence that no alternate path keeps
the USB device powered after VBUS disappears. Future externally/mixed-powered
operation needs a qualified host-VBUS indication and loss response. These are
alternative qualification paths, not modes selected by this contract. Unknown
VBUS state must not authorize attachment. Do not source host VBUS from a board
output or assume that a5V auxiliary terminal is a USB power input.

Before clearing SDIS, configure only reviewed USB pins, verify fixed clock/timing,
valid UID and power profile, initialize EP0 detached, and establish bounded
service/timeout/disconnect behavior. On VBUS loss or uncertain supply, detach and
invalidate the session through a qualified mechanism. Present driver behavior
disconnects on suspend; wake/session-end/VBUS/reconnect behavior remains pending.

## UID and read-only boot facts

ST CMSIS V2.6.0 defines UID_BASE0x1FFF7A10 for this target. The new
[boot_facts.c](../firmware/boot_facts.c) reads three aligned words there, raw
RCC_CSR at0x40023874 and FLASH_OPTCR at0x40023C14, then repeats the three UID reads.
Blank/allFF or inconsistent UID fails without changing the destination. Success
uses eight reads; the helper never calls write32. Caller must provide valid F413
memory access, lifetime, serialization and separate buffers. Bus faults cannot
be reported by this callback type; validated target/address space is a prerequisite.

The future startup can pass facts.uid to EP0's existing serial formatter. No
physical UID has been read in this increment. The synthetic historical-identity
fixture formats `3a0044001651333038373636`, matching October's saved serial order;
it is not a current device identification or authentication result.

Reset flags may have been cleared/changed by a bootstub and can accumulate across
resets. OPTCR WDG_SW bit5 distinguishes the configured watchdog source; ST's
[HAL definitions](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Inc/stm32f4xx_hal_flash_ex.h)
define software0x20/hardware0. Software selection does not prove a watchdog has
not already been started. The helper reports raw words without granting readiness
or changing BOR/read protection/write protection. Current boot-time watchdog
state, worst-case timing, recovery from reset loops and the feeding policy remain
qualification items. Historical config flash/watchdog failures remain relevant;
no watchdog-on config write is enabled by this work.

## Recovery and packaging

| Item | Existing evidence | What must still be established for a new image |
| --- | --- | --- |
| Historical board identity | October4 serial3a0044001651333038373636, de193215 nightly | Fresh exact board/revision/firmware identity |
| Original application | Saved signed image27976bytes, SHA256e35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b; historical restore/readback and full power-cycle boot | Accessible exact rollback asset and separately qualified new-image boot/recovery |
| Bootstub | Source and a11204-byte bundle build, SHA2562533c53d853826c1fa4e9198d1126446ae5a412adc6ba03c1d5a8171287353ca | Installed16KiB-region dump/identity, accepted keys/format and protection state; bundle build is not an installed dump |
| Settings |17historical archived files, eight CRC-valid blocks and one erased incident sample | Current full configuration/erase-sector preservation and schema identity; valid CRC is insufficient for migration |
| DFU/restart | Historical application-only restore succeeded after full USB power cycle; reset/:leave alone had misleading results | Current independent DFU/recovery access with all active power feeds understood |

Teacher October4 recovery notes record an alternate candidate failing to boot
despite exact application readback, followed by successful restoration of the
nightly with bootstub unchanged. This is actual historical bench evidence, not a
new test, a failure diagnosis, or proof this new image will recover the same way.

Current build reserves bootstub0x08000000..0x08004000, application from0x08004000
up to the protected config boundary0x08020000, and the legacy boot flag. Preserve
the whole config erase sector. Source bootstub reads word0 as signed-image length,
checks VERS/version/RSA and jumps via word1. Our raw image stores an ordinary stack
pointer at word0; future compatible packaging replaces that word. Explicit MSP
reload is already in our startup. Packaging/signature acceptance still needs
installed-bootstub proof; a136-byte budget reserve is not a signing implementation.

No flash/option-byte erase/unprotect command or broad USB reset/discovery sweep
is part of this contract. Keep custom recovery separate from managed Sunnypilot
and preserve current per-device Core Config write restrictions. Required rollback
assets must be staged/verified for any future standalone bench checkout; portable
notebook hashes alone are not a recovery kit.

## Completed now and remaining work

Completed T03b3a: this requirements contract, plain-language progress guide and
original read-only boot-facts library with native sanitizer/ARM retention checks.
Startup/USB driver/board/CAN code remains unchanged, bootstrap capabilities zero.
Exact source, historical-asset checks and actual tests are in
[the receipt](../../Ai/Evidence/chimera-usb-prerequisites-20261106.json).

The detached service module with fault fixtures now exists. Keep main's
attachment disabled. Next define exact status/capability semantics. In parallel resolve
the power/VBUS and installed-recovery evidence before any connected profile is
enabled. Full modern status/bulk CAN endpoints, managed host integration, signal
acquisition, Core Config and MCU TX policy remain pending. No new board operation,
flash, config/option write or actuation was performed.
