# Chimera identity/query contract — November 6, 2026

Owner “proceed”, context QA14→QA15: T02b distinct firmware identity, request matrix
and bus/input source contracts, then the next testable firmware component. Baseline
0bc14bcfda34a5d087278737fe6293efbfaeac24 cleanradxa/q8b. Teacher/student routers,
handoff/inbox/Q&A, Chimera source map and deep review consulted first. Panda8a16e089,
opendbc150f9371, Ocelotd87892fa with its39dirty entries/19source hashes unchanged;
workspace archive224cfa6clean. Exact current hashes in the receipt below.

Added original MIT protocol.c/.h and native fixture. Product contractChimera F413,
D6versionchimera-f413-bootstrap-v1, A0manifestCHMR/schema1/32bytes/local family1/
phase0. Source-defined physical buses3/classicalmax8/interfaces0x01FF; operational
capabilities/CANhash/healthhash/configABI/updatepolicy all0. Physical presence is
not acquisition or qualification. D6 is an ABI label, not binary attestation.
A0 is our custom request, with no handler found in pinned current/old command
sources. No Panda hardware type borrowed; C1/DD/D2/C2/config/reset/allOUT rejected.
Exact vendor/device/IN, zero value/index and bounded complete replies only; reject
without destination changes. Standard enumeration is a separate future driver.

Builder includes protocol.c and linker deliberately retains the pure query entry
and identity constants. Main/startup/board source unchanged; no handler calls from
the parked application. No USB clock/descriptors/serial generation/EP0/endpoints,
new native host profile or managed selection added. Existing host still rejects
this incomplete bootstrap profile. Bus0Cores/bus1ADAS/bus2vehicle and every direct
input/relay/OBD-C interface preserved. Source freshness/authority rules are design
requirements, not implemented thresholds. Canonical DBC unchanged; no payload copy.

TDD: two new tests failed before protocol files/linked symbols existed. During
test insertion, restored an accidentally displaced GPIO execution check before
the first green suite. Artifact review found GCC combined SETUP byte reads into
LDRH, potentially depending on inherited UNALIGN_TRP state. Added a failing ARM
instruction regression test, then -mno-unaligned-access;12tests now pass. Native
ASan/UBSan458920cases cover all request types/numbers, all16-bit lengths/value/
index values for both queries, capacities/sizes/null/unaligned buffers and canaries.
ARM symbols/bytes and byte reads checked. Existing vector/ELF corruption/linker
overflow/GPIO/MSP checks and copied-tree determinism pass. No skip/suppression.

GCC13.2.1/binutils2.42, hostGCC13.3.0, Ruff pass. Raw1240bytes, projected legacy
envelope1376/114688budget,8-byteglobals/4096stack unchanged. SHA256
5f47ad450bd18a254605fec2d1902beecc187eac5c0310af0447f48471dcac5f.
[Receipt](../Evidence/chimera-identity-contract-20261106.json) pins commands,
source/test hashes and actual results. Official libusb1.0.30 SETUP/type docs used;
existing vendored1.0.29.post103 agrees. Our schema/rejection choices are new design,
not imported Panda semantics. Source-first/TDD/interface/incremental/security/
debugging/documentation/Git/review skills used, ARM GNU artifact inspection;
no REA provider run required or claimed. Review covered bounds, wire alignment,
unchanged rejection buffers, no MMIO, retained data and phase/capability honesty.

[USB contract](../../chimera/docs/USB_IDENTITY_CONTRACT.md) and
[bus/input contract](../../chimera/docs/BUS_INPUT_CONTRACT.md) distinguish evidence,
implementation and future requirements. Next board T04six-byte/XOR classical CAN
codec, then USB clock/EP0 and operational status contracts; hostT05/T08 pending.
Full health/hash/capability/config ABI and physical boot/recovery/electrical proof
remain open. No hardware access, flash, config/DBC write, actuation, daemon,
installation, upstream update or push. Updates remain held, last saved checkNov4.
Both notebook layers/Q&A/roadmap updated; ignored binary/ELF/map/report stay local.
