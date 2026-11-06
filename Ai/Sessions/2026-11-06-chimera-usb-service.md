# Chimera detached USB service — November 6, 2026

Owner “proceed”, context QA20→QA21. Accepted T03b3b detached startup/service
composition, keeping attachment disabled and main parked. Baseline
10fbf46341d6acadc768cea296c7e36044416750 on radxa/q8b, clean before changes.
Teacher/student routers/resume/inbox/handoff/state/tasks/Q&A and current source/
requirements read first. Upstream/reference advance remains held sinceNov4.

New original usb_service.c/.h composes actual boot-facts, DWT timing, USB48 clock,
detached core and EP0 driver. Zeroed stable context; IO methods copied and driver
points into owned copy, external callback context must remain valid/trusted.
Serialized calls and exclusive quiet-board/mainPLL/affected-clock ownership.
Start validates arguments/clock/gated-USB ownership before writes, captures UID/
raw reset/options, checks timing, owns clock/core, initializes driver from UID
and verifies detached invariants. Descriptor profile values are supplied test
parameters, not board qualification. No main instance/call or attachment API.

States STOPPED/DETACHED/FAILED, local diagnostic errors not a USB ABI. Pre/post
poll guards check CPU profile, clock/reset access, SDIS, global IRQ/DMA off, no
forced session-valid and powered PHY. Invalid phase/budget does no I/O. Failures
invalidate driver/model work and latch. Owned accessible core is disconnected,
masked and PHY-off; RCC reset held and clock gated with readback, unrelated bits
preserved. Gated/reset core is never accessed as a USB register. Failed cleanup
retains ownership/failure; only explicit successful stop permits restart. Stopped
stop is an I/O-free no-op. No rollback of PLL/HSE/debug settings. facts_valid
means a successful raw snapshot, not proof a watchdog is stopped or an image is
trusted. Counter/event bounds do not establish elapsed deadlines/service latency.

TDD RED missing service source/header → GREEN actual helper pipeline. A runtime
CPU-clock drift fixture failed until the boundary guard included CPU profile.
Added final-start/pre/post-poll invariant cases, ownership rejection, cleanup
readback failures, explicit stop/retry, copied IO lifetime and argument guards.
Initial fake address guard was too broad and caught Cortex debug registers;
fixed the USB peripheral range while preserving all register-access checks.
No skips, suppressed rules, loosened bounds or child-function success stubs.
Incremental/TDD/API/interface/Git/self-review workflows used. Source-first routing
uses reviewed local components/contracts; no new external/ST/manual/compliance
or REA provider/runtime result invented. No model/inference execution involved.

Actual checks from Sunnypilot root:

- CHIMERA_TOOLCHAIN_PREFIX=/home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi- python3 -m unittest discover -s chimera/firmware/tests -v
  —23tests pass in16.024s.44real-component register scenarios plus all prior
  UID/control/clock/EP0/FIFO/CAN/GPIO/artifact/bounds/copy-tree checks. Native
  ASan/UBSan, explicit write whitelist and enabled/released core-access guard.
- python3 chimera/firmware/build.py --toolchain-prefix /home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi-
  —pass; raw7448bytes/projected legacy7584/114688budget, globals8/stack4096.
  SHA256d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698.
  GCC13.2.1/binutils2.42/nativeGCC13.3.0. Service symbols retained; disassembly
  proves no service call in chimera_reset. Unsigned ignored local artifacts.
- .venv/bin/ruff check chimera/firmware and git diff --check —pass.

[The receipt](../Evidence/chimera-usb-service-20261106.json) records actual output/source/test/build pins and preservation checks.
[The service contract](../../chimera/docs/USB_SERVICE.md) explains API/lifecycle/limits. Only build.py and test_firmware.py change
among preexisting code/test files; all earlier helper/main/startup/board/protocol/
codec/MMIO/linker sources hash-identical to QA20. Native host/safety/canonical DBC
unchanged. Ocelot39dirty entries/all19source hashes preserved; archive224cfa6clean.
No new VCDS evidence. Both notebooks/Q&A21/roadmap/progress guide synchronized.

T03b3b complete offline; full T03 actual startup/attachment remains partial. Next
board T05a: exact status/capability semantics and offline response fixtures before
operational health advertisement; later bulk CAN/controller binding. Host legacy
health decoding and managed lifecycle remain separate pending tasks. Physical
power/VBUS/current-recovery and watchdog/scheduler/session/resume/reconnect
qualification are still required. Input acquisition/Core Config/MCU TX policy
unfinished. No device read/write/flash/reset, relay/config/DBC write, actuation,
installation, upstream reference check/advance or push.

Closeout checks: memory verifier passes141documents/456relative links/246optional
workspace links/8source repositories/4254indexed entries;112active Chimera links
resolve. Final code/test SHA256 readback, Ruff and diff checks pass.
