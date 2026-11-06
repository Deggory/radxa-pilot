## November 6 — USB packet driver and ordered backend implemented offline

QA-20261106-19: T03b2 adds ARM MMIO/DWT timing and polling EP0/FIFO driver under
chimera/firmware/.19tests pass,32768RX headers/390descriptor transfers/15controller
faults/51delay durations; raw6420bytes, globals8bytes. Reset/SETUP cancellation,
coalesced completions, STALL recovery and bounded fault handling tested. Main/
startup/board/protocol/codec/USB model remain unchanged; no attachment or host
admission. [Session](../Sessions/2026-11-06-chimera-usb-driver.md) pins details. Next
T03b3 power/VBUS/UID and watchdog/recovery prerequisites, then reviewed startup/
service/attachment. No hardware/flash/config/DBC/actuation/install/update/push;
Ocelot/archive preserved, upstream checks still held. T03 overall remains partial.

## November 6 — Owner-supplied Ocelot Panda Docker source reviewed

QA-20261106-18: pinned Deggory/Ocelot_Panda_docker main04b56ba0 and parent98de83bb.
Current panda target removes GATEWAY/uses stock Panda detection; parent retains
separate Chimera inputs/outputs. Parent Chimera main matches Ocelot committed
source.31exact source files saved;189pure sender/parser vectors, health43/offset39,
flag/preprocessor and signedness checks pass. DD means forwarding in this older
Panda, not versions; stock harness relay differs from PB0. See [session](../Sessions/2026-11-06-ocelot-panda-docker.md).
Research only; no runtime/board code changed, no Docker/build/device/flash/CAN/
update/push. Next remains T03b2; analog/Core Config/relay/OBD-C qualification open.

## November 6 — Detached USB foundation implemented offline

QA-20261106-17: T03b1 adds USB48 clock/detached core preparation and a pure EP0
request/state model under chimera/firmware/.16 offline tests pass, including19
fake-register scenarios and458797 SETUP cases; raw4060bytes, globals8bytes.
Main/startup and zero operational capabilities remain unchanged. Next T03b2:
ordered MMIO/timing backend, controller event/FIFO/EP0 packet handling and
reset/cancellation/STALL fixtures before any startup attachment. Status/bulk
endpoints and host admission remain pending. No device/flash/CAN/actuation/
config/DBC/install/update/push; Ocelot/archive preserved. Upstream remains held.
See [session](../Sessions/2026-11-06-chimera-usb-bootstrap.md).

## November 6 — Offline classical codec complete

T04 pure current framing/stream implementation now passes14offline tests with
source interop, sanitizers and ARM bounds/symbol checks; raw1840bytes. Transport
XOR limitations are explicitly tested. USB clock/controller/EP0/endpoints,
operational status/admission and independent MCU policy remain open; no hardware
or payload acquisition qualified. See [session](../Sessions/2026-11-06-chimera-can-codec.md).

## November 6 — Identity contract and pure handler now available

T02b adds distinct bootstrap identity/manifest, a strict read-only handler and
explicit bus/input source requirements.12offline tests pass; raw1240bytes.
Actual USB enumeration/EP0/endpoints, operational status/capabilities and native
profile admission remain open. See [session](../Sessions/2026-11-06-chimera-identity-contract.md).

## November 6 — Offline target gap narrowed

T01a/T03a now implemented: original F413 startup/linker/GPIO/build, raw1064bytes,
nine offline tests pass. New build reproducibility is demonstrated across source
and output paths with GCC13.2.1; physical boot/recovery/electrical qualification,
signed release and modern USB/CAN/input implementation remain open. See
[the bootstrap session](../Sessions/2026-11-06-chimera-f413-bootstrap.md).

# Chimera data completeness — November 6, 2026

## November 6 correction — firmware pin map and legacy build are available

QA-20261106-04: followed the owner's pointer into Ocelot firmware and its shared
board files. The logical GPIO/CAN/transceiver mapping, input/relay/OBD-C code,
776-byte config layout and existing F413 build script/toolchain are present.
Earlier gap wording was too broad: electrical connector/conditioning/load-path
proof and a qualified modern build remain open; source pin definitions and a
legacy build path are not missing. No functional code/build/device/update/push
action. Next use this source baseline for T01/T02 and the offline board target.

[Recovered firmware implementation map](CHIMERA_FIRMWARE_SOURCE_MAP.md).

We have enough source/reference evidence to begin bounded offline engineering;
we do not have a complete verified hardware/installed-firmware dataset. Review
QA-20261106-03 before repeating a claim that all board data is available.

Saved references include selected Ocelot/current Panda/C2/Carrot F413 and native
USB code, Core Config source, canonical DBC context, input/bus source maps,
original nightly image and historical recovery/config evidence. These snapshots
are not complete buildable source distributions or tested managed integration.

A collection gap was closed today: 17 historical Core Config backup/quarantine
files still existed outside the new board folder. They were copied unchanged to
`/home/radxa/comma/chimera/recovery/legacy-core-config-20261106/`, with origin and
SHA-256 manifest. Eight configuration blocks have valid magic/CRC; one all-FF
block is incident evidence. Valid bytes can still represent empty/unsafe/unknown
settings. No restore, quarantine-policy activation or current hardware read.

Remaining facts/decisions:

- Exact owner-board revision/MCU marking, full schematic/power tree and connector
  mapping, input conditioning, relay contacts/load paths and OBD-C levels.
- Exact source/build provenance for the saved de193215 nightly; its original
  image and historical application restore proof already exist.
- A verified complete current recovery set, including installed bootstub and
  current configuration/signature consistency. Local bootstub builds are not dumps.
- Reproducible modern F413 target/dependencies and signed partition budget; legacy Ocelot target/build helper and local toolchain already exist.
- Measured physical reception on all three buses and calibrated direct inputs.
- Actual vehicle/sensor CAN IDs, layout, units, integrity and freshness.
- Explicit bus/source authority, generated-report delivery, modern status and
  versioned configuration contracts; remaining implementation is not missing data.
- Measured relay/fault/endpoint release and later active-control qualification.

OBD-C can remain disabled during initial Radxa USB reception. Exact old source
is useful to reproduce old behavior but is not an absolute barrier to a new
known-source implementation with explicit migration/recovery limits. Full ST
manual reading/archive remains incomplete in the new folder; earlier teacher
notes preserve selected flash/watchdog facts.

Next T01/T02: board/partition/recovery evidence plus identity/RPC/bus contracts.
No firmware/application/DBC change, hardware operation or push. The detailed
[board gap checklist](/home/radxa/comma/chimera/docs/DATA_GAPS.md) is an optional
workspace reference; this note remains self-contained in a standalone clone.
