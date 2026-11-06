# Chimera polling USB packet driver — November 6, 2026

Owner “lets continue with chimera next stage”, QA18→QA19. Accepted T03b2 ordered
MMIO/timing backend and controller event/FIFO/EP0 packet handling offline. Baseline
6b83b2e632bc95c53ec58fda748ee87d93b50be6 on radxa/q8b, project clean. Teacher/student
routers/resume/inbox/handoff/state/tasks/relevant Q&A and Chimera contracts/source
study consulted. No upstream reference check/advance; November4 hold remains.

New usb_time.c/.h enables DWT without resetting CYCCNT, preserves unrelated debug
bits, requires HSI selected/ready and undivided nominal16MHz HCLK. Counter absence,
enable failure and stalls reject.0..50000us delays use wrap-safe cycle arithmetic
and finite reads; clock/counter ownership must remain exclusive and fixed. New
usb_mmio.c supplies DMB-ordered reads/DSB-completed writes and a factory returning
chimera_usb_io after timing init. ARM-only MMIO is compiled/inspected, not executed.
No physical UID reading or measured delay calibration. No timer IRQ or heap.

New usb_driver.c/.h connects the EP0 model to polling registers and FIFO. Caller
supplies prepared/detached non-DMA core and persistent exclusive io/context/UID/
power profile. Initializes only EP0, global IRQ enable remains0; no GPIO/NVIC/
attachment API. Poll budgets1..32events, register waits bounded by supplied read
count. Reset cancels pending transfers/generations, flushes queues, clears address/
config/events. Enumeration verifies FS PHY, resets state and clears global IN NAK.
SETUP reception invalidates previous pending work, stops active IN, flushes FIFO
and clears old completion/disable/timeout flags before rearming after STUP. Latest
queued SETUP wins; STUP dominates old OUT completion. Already-completed IN status
commits before a queued new SETUP. Replies are exact one-packet FIFO writes with
zero-padded tails. Address/configuration commits after status IN, status OUT needs
zero packet plus completion. Malformed requests/status stall; new SETUP recovers.
Wrong endpoint/mode/speed, metadata fault, timeout/underrun or bounded wait failure
invalidates/disconnects/masks/PHY-off. Clock/reset ownership loss invalidates
software without accessing gated core. Suspend disconnects; resume/session/VBUS/
watchdog/recovery/scheduler and actual hardware event/address/status timing remain
unqualified. Software tokens alone are not IRQ labels; disable/flush/clear order
is tested register intent, not a physical cancellation measurement.

Build adds time/MMIO/driver sources and ARM retention/barrier checks. Main/startup/
board/protocol/CAN codec/USB clock/EP0 model/linker source hashes unchanged. RAM
8global bytes/4096reserved stack remain. No new driver context allocated by main;
phase0 capabilities/layout hashes stay0. No bulk/health/CAN binding, host profile
admission, input sampling, Core Config or MCU actuation policy implemented.

TDD RED absent time/driver sources → native sanitizer fixtures GREEN. A new isolated
FIFO-underrun fault failed because TXFURM was masked; enabled the documented mask
and retained the test. Review added OUT-idle reset guard, W1C-only global clears,
enumeration cancellation/global-IN-NAK clear, and clock-loss cleanup without MMIO.
Initial fake register whitelist lacked the expected PHY failure-cleanup register;
corrected that fixture without admitting unrelated writes. No rule suppression,
skipped tests, relaxed bounds or production stub used. Source/interface design,
incremental, TDD, Git and self-review/code-quality skills used. Readable source
and GNU ARM artifact inspection follow REA fast path; no provider result invented.

Primary source: existing ST LL6ef30cf0 and middleware2df324bd; selected PCD driver
fetched read-only via GitHub connector at6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90,
blob2165db18d083955a07c944d7ea20ca91bd1bf936, SHA256
1c2e98cbaf49d6a0a881b0f8a8b70d29001fcf300d98b63e6d261a93ad5658b8 (62725bytes).
ST CMSIS core_cm4/F413 definitions and retained Ocelot Panda Docker USB source
also inspected. Original MIT implementation, no vendor SDK/code import. Ignored
PCD reference only; no full USB specification/RM0430/compliance claim.

Actual commands/results from Sunnypilot root:

- CHIMERA_TOOLCHAIN_PREFIX=/home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi- python3 -m unittest discover -s chimera/firmware/tests -v
  —19tests pass in14.463s. ASan/UBSan:32768RX headers,390descriptor transfers,
  15controller faults,51delay durations, counter wrap/stall, reset during three
  phases, cancellation/coalesced completions, malformed OUT/STALL recovery and
  event budget. Prior19register scenarios/458797SETUP queries/458920vendor cases/
  CAN interoperability/bounds/GPIO/artifact/copy-tree checks all pass.
- python3 chimera/firmware/build.py --toolchain-prefix /home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi-
  —pass. GCC13.2.1/binutils2.42; raw6420bytes/projected envelope6556/114688;
  SHA2568bf5429ac5470b225abe1ae5093370954c0c0901e0e6fc8ca3f3b0c1f425f7e3.
  Globals8bytes/stack4096. NativeGCC13.3.0. Unsigned local ignored outputs only.
- .venv/bin/ruff check chimera/firmware and git diff --check —pass.

[The receipt](../Evidence/chimera-usb-driver-20261106.json) records exact hashes/actual output/build report/preserved sources.
[The driver contract](../../chimera/docs/USB_PACKET_DRIVER.md) records API/recovery/physical limits. No new VCDS finding. Ocelot39dirty
entries/all19source hashes unchanged, archive224cfa6clean, canonical DBC/native
host/safety sources preserved. Both memory layers/Q&A/roadmap updated. Next
T03b3: power/VBUS/UID and watchdog/recovery prerequisites, then separately reviewed
startup/service/attachment integration. Status/endpoints/admission and input/
Core Config/MCU TX policy remain later work. No device access, USB/CAN traffic,
flash, relay/config/DBC write, actuation, installation, upstream update or push.

Closeout checks: memory verifier passes139documents/437relative links/246optional
workspace links/8source repositories/4254indexed entries.91active Chimera doc
links resolve. Final source/test SHA256 readback, Ruff and diff checks pass.
