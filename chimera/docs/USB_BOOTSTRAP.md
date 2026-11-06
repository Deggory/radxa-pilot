# Detached USB preparation and endpoint zero

November 6, 2026 — T03b1 implemented offline. The new library is linked into the
F413 image but not called by main. No USB GPIO, controller interrupt, device
attachment, hardware UID read or physical enumeration has occurred.

T03b2 now adds the [ordered backend and polling packet driver](USB_PACKET_DRIVER.md),
with19offline tests. Main remains parked; next T03b3 power/VBUS/UID/recovery
prerequisites and reviewed startup/attachment work. The16-test result below
records the original T03b1 foundation.

## Clock and detached core

[usb_hw.c](../firmware/usb_hw.c) uses a caller-supplied ordered register backend
and nominal cycle-counter delay. T03b2 supplies an ARM MMIO/DWT adapter; no adapter
is called from startup. Poll budgets
are bounded read counts1..1000000, not elapsed-time guarantees. The backend must
be nonblocking except for the explicit delay and exclusively own USB/main PLL.

Clock preparation requires HSI selected and ready, AHB undivided, HSE bypass off
and USB clock gated. It verifies a held peripheral reset before reprogramming the
PLL and enabling USB's clock. The source-defined16MHz crystal with M8/N96/Q4 gives
48MHz USB; CPU remains at nominal HSI16MHz. PLL stop/HSE-ready/PLL-lock waits are
bounded. The oscillator value is inherited source evidence, not a measurement.
Unrelated PLLR/clock fields are preserved. A failed precondition makes no writes;
later clock failure leaves USB gated/reset rather than publishing readiness.

Detached core initialization verifies the profile/reset hold and release, masks
interrupts, keeps SDIS set, selects the internal FS PHY and forced device mode.
PHY stays off across reset until SDIS is restored. A50ms backend delay and bounded
mode/reset/AHB-idle/flush checks precede success. RXFIFO128words/TX0FIFO64words are
reserved; no endpoint is armed and no packet FIFO is read/written. VBUS-valid
override is deliberately not asserted. Post-entry failure masks/disconnects and
powers down the PHY; a reset-release failure leaves the controller held reset.
These are tested register intentions, not electrical cutoff measurements.

ST's pinned driver specifies turnaround13 for nominal16MHz AHB, unlike the old
application's clock/timing combination. The standalone bootstrap still runs its
original HSI-only parked code; these routines do not change runtime clocks yet.

## Pure EP0 state model

[usb_ep0.c](../firmware/usb_ep0.c) handles descriptors, address/configuration,
GET_STATUS and sole interface/alt0 requests. Address/configuration changes commit
in the model only after successful status-IN completion. New SETUP or bus reset
cancels pending work. Completion calls require the generation saved when that
transfer was armed; stale generations cannot advance/commit a newer transfer.
Counter exhaustion disables the context instead of reusing a token.

The T03b2 controller driver cancels transfers and clears stale hardware events
before rearming. Tokens do not label controller interrupts automatically. The
driver handles reset, STALL and status phases offline; DCFG/status-handshake
timing and hardware event sequencing still need physical qualification. The
pure model remains separate from the control endpoint packet driver.

| Descriptor/property | Implemented model |
| --- | --- |
| Device | USB2.0, FS EP0max64, bbaa:ddcc, software bcdDevice1.00 |
| Configuration/interface | Configuration1, interface0/alt0, vendor classFF |
| Bulk endpoints | None advertised or armed in this bootstrap; IN81/OUT03 remain the later operational plan |
| Manufacturer/product | RetroPilot / Chimera F413, UTF-16LE string descriptors |
| Serial |24lowercase hex digits from12UID bytes in ascending memory order; blank/allFF UID rejected |
| Power | Caller-supplied qualified self-powered flag and maximum in2mAunits, at most500mA; no board supply/draw inferred |

The original ST header locates UID at0x1FFF7A10; a real read is future adapter
work. Fixtures use synthetic bytes, not this board's serial. Descriptor power
values and GET_STATUS reflect the supplied profile, not live measurements; VBUS,
power sourcing/draw, detach policy and supply changes need physical qualification.
All current descriptor replies are shorter than64bytes; standard descriptor reads
truncate to wLength. Unsupported recipients, descriptors/features/endpoints,
malformed lengths and fields stall without modifying the reply buffer. Only a
configured context routes vendor D6/A0 to the existing strict read-only handler.
No configuration/relay/reset/flash or safety-mode vendor write is added.

## Evidence and remaining work

16offline tests pass:19fake-register scenarios,458797SETUP cases including every
request type/number combination and all65536lengths for six descriptors, exact
device/string fixtures, canaries, malformed buffers, deferred commits, canceled
generations and power profiles. ASan/UBSan, retained ARM symbols, copied-tree
reproducibility and all previous codec/GPIO/vector/bounds checks pass. Raw4060bytes,
globals8bytes, reserved stack4096bytes. Source/code/test pins and actual output:
[receipt](../../Ai/Evidence/chimera-usb-bootstrap-20261106.json).

Primary sources: pinned ST
[low-level driver](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Src/stm32f4xx_ll_usb.c)
for PHY/reset/idle/flush/turnaround behavior and
[device-request implementation](https://github.com/STMicroelectronics/stm32-mw-usb-device/blob/2df324bd60d4b0bb27404fd70b1c089b467f0e09/Core/Src/usbd_ctlreq.c)
for request/state handling. No ST implementation is copied into this MIT library.
This selected-source review is not full USB2.0 compliance or a reviewed complete
RM0430 manual. No REA provider/runtime claim is made for source/fake-register checks.

Next T03b3: power/VBUS/UID and watchdog/recovery prerequisites, then reviewed
startup/service/attachment integration. T03b2 is implemented offline. Main stays
parked, CAN disabled, phase0 capabilities/hashes zero. Operational endpoints,
health/native host admission and independent MCU TX policy remain later work.
