# Polling USB packet driver and ordered backend

November 6, 2026 — T03b2 implemented and verified offline. The new driver links
the existing EP0 model to controller register/FIFO operations. No routine is
called from startup, and no USB device has been attached, flashed or exercised.

T03b3a now establishes [power/UID/recovery requirements](USB_STARTUP_REQUIREMENTS.md)
and a read-only boot-facts helper;21combined offline tests pass. The19-test result
below is the original T03b2 snapshot. Next software work is detached startup/
service composition; physical attachment still needs the separate qualifications.

## Backend and call contract

[usb_mmio.c](../firmware/usb_mmio.c) provides ordered volatile32-bit register
access with DMB around reads and DSB after writes. Its factory initializes the
Cortex-M4 DWT counter, then returns the existing chimera_usb_io interface.
[usb_time.c](../firmware/usb_time.c) preserves unrelated debug bits and never
resets CYCCNT. It requires HSI selected/ready, undivided nominal16MHz HCLK and
exclusive counter/clock ownership. An absent, disabled or stopped counter fails.
Delay0..50000us uses unsigned wrap-safe cycle arithmetic and a finite polling
budget. These are nominal clock-based delays, not measured oscillator calibration.
Do not change clocks or counter configuration during a delay. Debugger interaction
and sleep behavior remain physical qualification items.

The future caller must initialize timing, prepare USB48, prepare the detached
core, then initialize the [driver](../firmware/usb_driver.c). Driver init requires
USB clock enabled/reset released, soft-disconnect, non-DMA FS PHY/device mode and
a supplied UID/power profile. UID/power inputs remain unqualified caller data;
this driver does not read physical UID or infer supply capability. Keep io/context
alive and unchanged, initialize before polling, serialize all calls and keep
buffers/state separate. There is no heap or shared global driver context.

GAHBCFG global interrupt enable stays off. Event/endpoint masks support polling;
no NVIC, GPIO, CAN, relay or OBD-C setup occurs. No API clears SDIS to attach.
Register waits use the supplied1..1000000read budget. Poll handles at most1..32
events per call, returning idle, progress, budget-exhausted or failure. These
bounds are not service-latency guarantees; the future scheduler must qualify
USB response latency. Invalid poll arguments return failure without I/O.

## EP0 packet path

- Reset flushes RX/TX, cancels model generations and pending transfers, clears
  address/configuration and endpoint flags, and prepares three SETUP slots.
- Enumeration accepts internal full-speed PHY only, resets EP0 and clears global
  IN NAK. Non-DMA SETUP preparation follows ST's separate EP0_OutStart behavior;
  it does not arm a normal OUT data transfer.
- Received SETUP bytes update the pure model and cancel older work. Active IN is
  NAKed/disabled with a bounded completion wait; TX FIFO is flushed and old
  completion/timeout/disable flags cleared before rearming. Reply waits for STUP.
  Multiple queued SETUPs retain the latest request. SETUP dominates a coalesced
  old OUT completion.
- An already-completed IN is serviced before queued new SETUP reception, allowing
  a successful configuration status handshake to commit before the next query.
- IN replies use one packet, exact transfer length and byte-packed FIFO words.
  Unused tail bytes are zero; there is no unaligned read past the reply. All
  currently supported replies are shorter than64bytes. FIFO room is bounded.
- Status IN commits model address/configuration; DCFG follows successful status
  completion. Status OUT requires an observed zero-length packet and completion.
  This intended ordering still needs real controller/host timing qualification.
- Unsupported requests and malformed OUT status stall EP0; a new SETUP recovers.
  Unexpected endpoints, malformed receive metadata, stale/unexpected control
  events, wrong mode/speed, transfer timeout, FIFO underrun or wait failure latch
  failure, soft-disconnect, mask interrupts and power down the PHY.
- Lost clock/reset ownership invalidates software state without accessing the
  now-gated core. This is not a measured electrical disconnect guarantee.

The software generation is saved at arm time. Tokens cannot tag physical IRQs;
endpoint-disable completion, FIFO flushing and flag clearing supply the tested
hardware cancellation sequence. The fake model is not proof every controller
revision/event ordering behaves identically.

Suspend currently disconnects; wake/resume, session end/VBUS changes, watchdog,
reconnect and recovery are not qualified. There are no operational bulk endpoints,
CAN framing bindings, health responses, Core Config writes or MCU actuation policy.
Current bootstrap capabilities/layout hashes stay zero, and the host selector
continues rejecting this unfinished profile.

## Evidence

19offline tests pass under GCC13.2.1/binutils2.42 and nativeGCC13.3.0:

- ASan/UBSan packet-driver fixture:32768RX metadata combinations,390descriptor
  length transfers and15controller fault scenarios; enumeration/address/config/
  vendor read, STALL recovery, active-IN cancellation, coalesced events, three
  reset phases, generation exhaustion and event-budget behavior.
- Timing fixture:51delay durations, counter wrap, stopped/absent counters,
  rejected enable and clock/callback preconditions.
- ARM symbol/barrier inspection, all prior board/EP0/CAN/negative-image checks,
  copied-tree reproducibility and Ruff pass. Native fixtures never dereference
  physical MMIO. The ARM backend is compiled/inspected, not executed on hardware.

Raw image6420bytes; projected legacy envelope6556/114688bytes; globals8bytes and
reserved stack4096bytes. Exact source hashes, commands and actual output are in
[the receipt](../../Ai/Evidence/chimera-usb-driver-20261106.json).

Primary source: ST
[PCD event driver](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Src/stm32f4xx_hal_pcd.c)
and [LL USB functions](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90/Src/stm32f4xx_ll_usb.c),
with Ocelot's ST CMSIS F413/core_cm4 register definitions and the
[retained legacy implementation](OCELOT_PANDA_DOCKER_REVIEW.md).
This is selected-source inspection; no full USB specification/RM0430 review or
compliance result is claimed. No vendor implementation is copied into the new
MIT source. Reference downloads remain ignored; no SDK installed or vendored.

Next T03b3: source-backed power/VBUS/UID and watchdog/recovery prerequisites,
then separately reviewed startup/service/attachment integration. Physical board
qualification is still required. Operational status and bulk endpoint/CAN binding
follow; host status/lifecycle, input acquisition, Core Config and MCU TX policy
remain separate pending tasks. No hardware action or updater execution occurred.
