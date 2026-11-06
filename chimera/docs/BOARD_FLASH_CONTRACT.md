# Chimera F413 bootstrap contract

November 6, 2026 — T01a source contract and T03a offline target. This contract
does not identify the installed bootstub or qualify a board for loading.

## Preserved memory

| Address range, end exclusive | Ownership in this target |
| --- | --- |
| `0x08000000..0x08004000` | Existing bootstub; never part of this build |
| `0x08004000..0x0801FF78` | Raw application budget,114552bytes |
| `0x0801FF78..0x08020000` |136bytes reserved from the maximum application budget for possible legacy packaging |
| `0x08020000` and above | Existing config and remaining flash; no loadable bytes or erase operations |
| `0x20000000..0x2001EFF8` | Globals and unused conservative RAM |
| `0x2001EFF8..0x2001FFF8` |4096-byte stack reservation |
| `0x2001FFF8..0x20020000` | Reserved; includes legacy boot flag at`0x2001FFFC` |

The whole legacy application window is112KiB. Original `SConscript` places its
vectors at`0x08004000`; `chimera.h` places the776-byte settings block at sector5
start`0x08020000`. Preserve the entire config erase sector, not just that block.
No erase/write API exists here; no physical flash capacity or sector-end claim
is needed by this target. RAM deliberately uses less than the family capacity:
the original128KiB window with its top8bytes reserved, not a new SKU assumption.

Original `crypto/sign.py` with `SETLEN` adds an8-byte VERS/version trailer,
replaces vector word0 with the payload length, and appends a128-byte signature.
The reservation is a **budget**, not a fixed signature address: a future envelope
would follow the actual raw image. The source bootstub validates then calls
`_app_start[1]` directly, without loading MSP. Therefore our assembly reloads MSP
before C even though the unsigned raw vector contains a stack pointer.
No signer, signature, key read, bootstub rebuild or compatibility certification
is included. The installed bootstub/key/version remain unverified.

## Source-defined board state

| Interface | MCU pins | Bootstrap state |
| --- | --- | --- |
| Board CAN0 / MCU CAN1 / host0, Cores and controlled devices | PB8/PB9 AF8; enable PC1 | Enable high/off; peripheral clock off; data pins untouched |
| Board CAN1 / MCU CAN2 / host1, radar/ADAS | PB5/PB6 AF9; enable PC13 | Enable high/off; peripheral clock off; data pins untouched |
| Board CAN2 / MCU CAN3 / host2, vehicle/retrofit sensors | PA8/PA15 AF11; enable PA0 | Enable high/off; peripheral clock off; data pins untouched |
| Onboard relay | PB0 | Low output, pull-down |
| OBD-C ignition | PB1 | High/off output, pull-up |
| OBD-C request | PA2 | Input, pull-up |
| IGN, VSS, CPS, brake | PA3, PA4, PA5, PA6 | Inputs, pull-ups; no sampling or pulse IRQ |
| ADC1/ADC2, channels12/13 | PC2/PC3 | Analog mode, no pulls; no conversions |

All output latches are preloaded using BSRR before changing output modes. Only
the listed pins change; SWD and CAN alternate functions are left alone. The old
gateway helper intentionally leaves transceiver1 enabled when asked to disable
the group; **this bootstrap explicitly disables all three**. That is an intended
offline-bootstrap policy, not evidence about power-on or electrical relay paths.
The original IGN/brake/OBD request use active-low logic; pulse acquisition and
freshness interpretation remain future work.

## Reset, clocks and failure behavior

Original startup/vector source and ST's interrupt enumeration establish102
external IRQ positions. Our vector region is512-byte aligned/padded, with all
implemented exception/IRQ entries routed to a trap and core-reserved entries zero.
Assembly masks IRQs and initializes MSP; C initializes data/BSS, disables inherited
SysTick/NVIC IRQs, clears pending IRQs and installs VTOR. GPIO inactive levels are
established, then CAN/USB peripheral clocks gated. HSI16MHz is selected with
bounded readiness/switch polling before removing AHB/APB divisors. Existing flash
wait states are retained. No HSE/PLL/USB48MHz configuration is attempted.

Debugger globals report boot magic`0x4348494D` and state1(parked),2(clock failure)
or3(trap). These are not operational health responses. IRQs remain masked and
execution parks. Inherited/option-byte watchdogs, bootstub effects before entry,
power loss, NMI/hardfault recovery, relay cutoff and physical USB/CAN behavior
are **not qualified**. A fault that prevents execution of the handler cannot be
claimed to produce these GPIO levels. No flash/recovery procedure is enabled.

## Evidence and checks

Source baseline: Ocelot`d87892fa25ef2a2474110b97bfb5245ee818b534` with preserved
dirty files; the [source map](FIRMWARE_SOURCE_MAP.md) and
[exact bootstrap receipt](../../Ai/Evidence/chimera-f413-bootstrap-20261106.json)
pin working-file hashes, rather than claiming HEAD alone reproduces them.
Relevant original files are `SConscript`, `bootstub.c`, `crypto/sign.py`, `gpio.h`,
`startup_stm32f413xx.s`, `boards/gateway.h`, `chimera/main.c`, `chimera/chimera.h`
and the ST BSD-licensed `inc/stm32f413xx.h` V2.6.0.

Primary family reference: [ST STM32F413 datasheet DS11581 Rev7](https://www.st.com/resource/en/datasheet/stm32f413vh.pdf)
confirms the internal16MHz oscillator and Cortex-M4 family. The
[RM0430 reference manual](https://www.st.com/resource/en/reference_manual/rm0430-stm32f413423-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
could not be retrieved this session (web size limit/direct download timeout);
register offsets and masks used here were checked against the pinned ST header.
No claim of complete manual review is made.

The original T03a nine offline tests cover three inherited GPIO register patterns with sanitizers,
raw vectors/size, six vector corruptions, six ELF mutations, startup instruction
ordering, flash overflow, RAM/stack collision and identical binaries from a copied
checkout. The build rejects unplaced sections, dynamic linkage, undefined symbols,
writable executable segments and load bytes outside its flash budget. Stack is
reserved by symbols/assertions, not an artificial load segment. These are source,
compiler and artifact checks; there was no device execution or REA provider run.

T02b now adds the [identity/request contract](USB_IDENTITY_CONTRACT.md), pure
handler and source contract. T04 adds the [classical CAN codec](CAN_CODEC_CONTRACT.md);
the combined suite has fourteen tests. Next: USB clock/EP0, then status/endpoint work. Host T05 legacy
status decoding and T08 managed selection remain separate pending increments.
