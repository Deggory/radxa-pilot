# Chimera detached USB foundation — November 6, 2026

Owner “proceed”, context QA16→QA17. Accepted T03b1: USB48 clock/core preparation
and pure endpoint-zero enumeration model offline. Baseline
fcdbecdd6f706d21074363b8cca869ce85dace40 on radxa/q8b; clean before this work.
Teacher/student routers, resume, handoff, state/tasks, Q&A, update inbox and
Chimera source notes/contracts read before implementation. Upstream/reference
checks remain held since November4; no fetch/merge/push performed.

New original MIT usb_hw.c/.h uses injected read/write/delay callbacks. Requires
HSI16/no AHB divider, no HSE bypass and exclusive USB clock ownership. Holds
USB reset before clock changes; HSE16/M8/N96/Q4 gives48MHz, CPU stays HSI16.
Core release requires clock/profile/reset checks; PHY remains off until SDIS.
Sets internal FS PHY/device mode, ST TRDT13 for16MHz,50ms delay callback,
RX128/TX064word FIFO allocation and bounded AHB/reset/mode/flush waits.
Failure cleanup disconnects/masks/disables PHY after core access is possible.
No GPIO/IRQ/attach API. Poll budgets count reads, not elapsed deadlines.

New usb_ep0.c/.h is a pure state model. Control-only vendor interface0/config1,
bbaa:ddcc bootstrap identity, 64-byte EP0, no noncontrol endpoints. Serial is24
lowercase hex digits from ascending12UIDbytes supplied by caller; blank UID
rejects. Self-power/maxdraw profile must be supplied/qualified. Strict supported
standard requests; A0/D6 queries require configured state. Address/configuration
commit only after matching status completion. Every SETUP/reset advances a token,
stale completions reject, overflow disables context until reinit. Future driver
must also cancel/drain stale controller events and qualify DCFG/status timing.
All current replies fit one FS data packet. No actual packet/FIFO/event driver.

Build/linker retain seven USB APIs; firmware main/startup/board/protocol/codec
source hashes unchanged. No initialized USB context/global added: global RAM8,
stack reservation4096. Phase0 manifest capabilities/layout hashes remain0.
No host profile admission or existing SPI startup change.

TDD RED began with missing USB source/APIs; added sanitizer fixtures and strict
completion generations. A failing post-reset AHB-idle fault fixture led to
explicit idle waits before FIFO flushes. Reset hold/release failures verify no
clock enable before reset and no core access while reset held. Review tightened
stale completion cancellation; no skipped tests or weakened checks.
Skills used: incremental implementation, TDD, source/interface design, security,
debugging, Git and code review. Readable source first; GNU ARM artifact tools
provide actual symbol/link evidence. No unrelated REA provider result claimed.

Primary evidence: original Ocelot clock16MHz/legacy PLL/USB and CMSISV2.6.0 register
definitions; ST LL USB commit6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90 and device
middleware2df324bd60d4b0bb27404fd70b1c089b467f0e09. Exact hashes/selected URLs in
receipt and USB_BOOTSTRAP. ST files downloaded only as ignored reference evidence;
no vendor implementation/SDK or restricted legacy linker copied. USB-IF landing
page consulted, not a complete USB specification/RM0430 review. Toolchain preexists;
no installation. Ocelot39dirty status lines/all19original source hashes and
archive224cfa6clean unchanged; canonical DBC hash unchanged.

Actual validation from project root:

- CHIMERA_TOOLCHAIN_PREFIX=/home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi- python3 -m unittest discover -s chimera/firmware/tests -v
  —16tests pass in13.339s; native ASan/UBSan,19fake-register scenarios,
  458797EP0 SETUP cases, existing458920vendor query cases,648RX/189TX source
  CAN vectors,4536split scenarios and prior board/artifact checks all pass.
- python3 chimera/firmware/build.py --toolchain-prefix /home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi-
  —ARM build passes: raw4060bytes, projected legacy envelope4196/114688bytes;
  SHA256 aea93ff3aefc7519a3cd6471a0b3881362bee727e75a704727badaaa42071a13.
  GCC13.2.1/binutils2.42; nativeGCC13.3.0. Unsigned ignored local artifact only.
- .venv/bin/ruff check chimera/firmware —pass.

Exact actual test output/source hashes/build report and preserved-source evidence
are recorded in [the receipt](../Evidence/chimera-usb-bootstrap-20261106.json). Documentation/memory/link/diff validation is added
there at closeout. [The roadmap](../../chimera/tasks/plan.md) records T03b1 complete and T03b2 next.

Next exact slice: ordered real MMIO/timing backend and controller event/FIFO/EP0
packet movement with reset/new-SETUP cancellation/STALL tests and qualified
power/VBUS/UID/clock prerequisites before any startup attachment. Then status,
bulk endpoints and host admission; Core Config, input acquisition, MCU policy,
watchdog/recovery and physical electrical qualification remain open. T03 is
partial, not a working USB device or tested Sunnypilot integration. No hardware,
USB/CAN traffic, daemon run, flash, config/DBC write, actuation, install, upstream
update or push. Both notebook layers and Q&A synchronized; project increment
saved locally after validation. Historical entries retain their original results.

Closeout checks: memory verifier passes137documents/419relative links/246optional
workspace links/8source repositories/4254indexed entries;57Chimera Markdown links
resolve. Ruff, source/test/reference SHA256 readback and git diff checks pass.
