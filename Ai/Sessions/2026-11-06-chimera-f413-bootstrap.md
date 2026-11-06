# Chimera F413 bootstrap — November 6, 2026

Owner “let proceed” after QA-20261106-13. Accepted increment: implement actual
board code under chimera/firmware/, source-backed flash/GPIO contract and minimal
offline F413 image. No device loading, actuation, upstream integration or push.
Teacher router/resume/inbox, Chimera/Ocelot source map and student Q&A consulted.

Baseline9fa1f81108d2102830d13c0fc03c22b9db6e73d0, branchradxa/q8b, initially clean.
Panda8a16e089b88593914823743df29e1c30b7dd3e00;
opendbc150f937198ceab43c43b39f94b9bdea63fcb633c.
Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 retains its39dirty entries and all19
previously pinned working-file hashes. Workspace Chimera archive224cfa645134db91103c55d8188d87e7976b0ba4
remains clean. No source/reference move or dependency on those folders in the new build.

Original MIT startup/board/main/linker/build files now exist. Bootstub region,
config at0x08020000 and RAM boot flag0x2001FFFC are preserved by conservative
layout. Legacy SETLEN reserves8-byte version trailer+128-byte signature; startup
explicitly reloads MSP because source bootstub calls app reset directly and later
signing overwrites vector word0. No signer/key/bootstub import. Source transceiver
enables all high/off, relay low and OBD ignition high/off; digital/analog pins
reserved with original input modes/pulls. Inherited IRQ/SysTick cleanup, bounded
HSI selection and parked status only; CAN/USB clocks off, no data acquisition.
Restricted Atollic linker and ST startup were not copied.

TDD: initial test setup failed for missing build.py before implementation. Strict
orphan checking then exposed linker glue/PLT sections: place glue, assert dynamic
sections empty. Distant NOLOAD stack distorted ELF physical memory extent; use
reserved symbols and RAM collision assertion. Added actual RWE ELF mutation,
saw failure, corrected combined readelf flag parsing. No suppression/skip.

GCC13.2.1/binutils2.42 existing explicit tool prefix, hostGCC13.3.0. Nine tests pass:
ASan/UBSan fake GPIO patterns0/all1/mixed; vectors/size; six vector corruptions;
three truncated/oversize cases; six ELF identity/entry/load/flags/RAM mutations;
real linker flash/RAM failures; MSP-before-C disassembly; identical raw bytes
from copied source/output path. Raw1064bytes, projected legacy envelope1200bytes,
112KiB total budget, globals8bytes/stack4096bytes. Binary SHA256
7d634696ba464d04e13164f09714fe20e85375befa4d5ff37eb884bdb2a9398e.
Ruff passes. Exact commands/hashes/tool output identities are in the
[receipt](../Evidence/chimera-f413-bootstrap-20261106.json).

ST DS11581 Rev7 retrieved; RM0430 retrieval exceeded web size limit and direct
download timed out. Register offsets/masks use the pinned ST V2.6.0 header;
no full-manual/installed-board identification claim. Source-first, TDD,
incremental, interface, debugging, Git and review skills used. Artifact checks
used ARM readelf/nm/objdump directly; no REA provider result was required/invented.
Review covered MMIO ordering, boot/config/stack boundaries, handoff, unsigned
artifact limitations and no host startup change. HSI and exception behavior are
not runtime-tested; inherited watchdog/electrical cutoff/recovery remain open.

[Board contract](../../chimera/docs/BOARD_FLASH_CONTRACT.md) and firmware README
describe implementation and limits. QA14 is a dated status update to QA12/13:
firmware is now implemented, unlike their earlier folder-only snapshot. T01a/T03a
complete offline; full electrical/recovery/signed release qualification remains
pending. Next board T02 distinct identity/RPC/bus/input source contracts, then T04
codec and USB clock/endpoints. Host T05 legacy health and T08 managed selection
are still pending; existing SPI startup unchanged. Upstream hold remains active,
last saved checkNovember4. No flash, config/DBC write, hardware action, installation
or push. New source/docs/notebook files are saved in this scoped local increment;
ignored ELF/bin/map/report are reproducible build output, not committed releases.
