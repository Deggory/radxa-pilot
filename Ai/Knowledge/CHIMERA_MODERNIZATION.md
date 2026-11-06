## November6 — Pandad SPI removed; metadata increment in progress

QA31: owner corrected generic-SPI retention. Removed pandad SPI source/class/build/
listing and both generic entries; all platforms require pinned USB. Current Panda
constructor qualifies USB and performs no reset/config.10native/42Python checks
plus strict fake-USB sanitizers pass. ASan reproduced/fixed short-header heap read;
exact tests/output in receipt. Metadata test is RED/uncommitted; continue next.
No hardware/update/push; firmware23hashes preserved. Earlier SPI-retention notes
are superseded. [Session](../Sessions/2026-11-06-chimera-remove-spi.md).

## November6 — Offline legacy PandaState preview implemented

QA30/T08b2b: pure C++ conversion maps24common fields and all25fields of each
of3controllers;6current fields explicitly unavailable. Preview always invalid,
unreferenced by managed pandad. Safety25/26 conflicts and fault27+/unsigned-alt
Int16 overflow rejected; raw isolated diagnostics retained. Native build/10native
programs,41Python tests, converter ASan/UBSan and validity mutation pass. Native
preview read in Python cannot enable ignition. Exact Carrot69a2d3be source queries
and5retained reference/license files pinned. No runtime admission/IPC/hardware run.
Firmware23hashes/7448-byte image, Ocelot39dirty entries/19hashes, archive/DBC and
protected runtime/camera/model/Thneed preserved. Updates held/no push. Next T08b2c
supported-field admission metadata and consumer review before normal publication;
reconnect/backoff, other profiles and operational firmware/bench work remain.
[Session](../Sessions/2026-11-06-chimera-legacy-state.md).

## November 6 — Panda ignition validity prerequisite implemented

QA29/T08b2a: hardwared now passes SubMaster Event.valid into a pure reducer for
every updated pandaStates event. Invalid/empty updates revoke ignition immediately;
retain last valid primary harness for battery shutdown. Non-unknown predicate,
primary/secondary semantics and no-update age>5s grace remain.12new tests,
37focused plus28power/fan tests (65total), Ruff/compile and mutation checks pass.
Seven selected actual source-branch cases reproduce both baseline bugs/preserve
grace with fake clocks; no live thread/IPC/hardware run. USB still emits no
pandaStates; mapping/admission/reconnect remain. Firmware23hashes/7448-byte image,
Ocelot39dirty entries/19hashes, archive/DBC and prior host code preserved. Updates
held; no push. Next T08b2b source-backed fault/enum/supported-field mapping and
an offline PandaState converter before ordinary publication.
[Session](../Sessions/2026-11-06-chimera-panda-validity.md).

## November 6 — Passive USB CAN and isolated diagnostics implemented

QA28/T08b1: pinned legacy F4v17 USB entry now receives classical CAN and publishes
`can` plus complete JSON diagnostics on `customReservedRawData1`. No pandaStates:
hardwared reads ignition without Event.valid gating. RawData0/Thneed untouched.
Fragment age500ms, bounded RX and strict parser errors close ownership; no TX,
reset/retry/cache/SPI fallback. Native build/9native programs,25Python regressions,
ASan/UBSan and checksum mutation check pass offline. No physical USB/IPC session,
pins, firmware or onroad admission.23firmware hashes/7448-byte image, Ocelot39dirty
entries/19hashes, archive and canonical DBC preserved. Updates held; no push.
Next T08b2: profile-aware pandaStates admission, supported-field validity/ignition
and reconnect/backoff policy. New Chimera operational firmware/bench work remain.
[Session](../Sessions/2026-11-06-chimera-usb-receive.md).

## November 6 — Radxa USB-only status startup implemented

QA27/T08a: Radxa wrapper/native entry bypass legacy reset/flash/SPI for mandatory
serial/version-pinned USB status session. Legacy F4v17 only; no CAN/pandaStates/
control threads or ready claim. Failure closes; no cache/retry/SPI fallback.
21Python/7native/sanitizer checks pass; five invalid native invocations exit2,
main.o has no legacy-thread reference. No pins installed or valid hardware run.
Firmware/Ocelot/archive/DBC preserved; updates held. Next T08b passive CAN and
validity-aware publication/exact-read/freshness/reconnect. Other profiles pending.
[Session](../Sessions/2026-11-06-chimera-usb-startup.md).

## November 6 — Legacy CAN-health5 decoder/read helper verified

QA-20261106-26: T05c adds all26fields/64bytes plus caller selector, strict legacy
profile/bounds/flags/LEC decoding and one bounded C2 IN reader for0/1/2. Native
pandad builds;7native executables and both health/CAN-health sanitizer fixtures
pass. Invalid-selector-before-IO mutation detected. Exact source/current layout
size/offset/type checks pass; no shared-profile admission. Legacy bus-off count
increments during polling; full8-bit F4 REC retained. No managed/firmware/hardware
change; USB-only/no SPI fallback remains target. Next T08a pinned USB session/
startup ownership; publication/exact-read/reconnect and new board status remain.
Firmware23hashes/retained7448-byte image, Ocelot/archive/DBC preserved. Updates held.
[Session](../Sessions/2026-11-06-chimera-can-health.md).

## November 6 — Owner progress summary

QA-20261106-25: offline foundations implemented; most operational integration
and all new-firmware physical qualification remain. Saved28firmware/discovery,
6native/15Python/sanitizer results are offline, not end-to-end. Image7448bytes
unflashed/parked; USB-only managed startup still pending. Inputs/Core Config/
MCU policy/relay/OBD-C and bench/release work remain. No reliable percentage.
Next T05c per-bus health. Summary/docs only; no runtime/hardware/update/push.
[Session](../Sessions/2026-11-06-chimera-progress-summary.md).

## November 6 — Owner requires USB only for Radxa/Chimera

QA-20261106-24: owner says “no spi is needed since we will use usb only”.
USB-only target excludes SPI wiring/probing/fallback. Updated active plan/rules;
inherited native constructor still opens SPI and awaits T08 pinned USB startup.
Requirement correction only, no runtime/code/hardware change. Next remains T05c
per-bus health, then USB-only managed lifecycle. Upstream updates held.
[Session](../Sessions/2026-11-06-chimera-usb-only.md).

## November 6 — Legacy F4 health59 decoder/read helper verified

QA-20261106-23: T05b adds native LegacyF4Health, exact59-byte decoding and one
bounded D2 read; full widths/fractional load retained, no current-only defaults.
Native pandad builds;6native executables, ASan/UBSan and15existing Python tests
pass. Mutation detects missing profile guard. Exact Carrot69a2d3be header/license
retained in project test fixtures. Firmware23source hashes/7448-byte retained
image unchanged; no fresh ARM build or firmware suite this slice. Managed startup
and get_state unchanged; per-bus health/publication still pending. Next T05c
CAN-health5 compatibility, then T08 lifecycle. Current short-read hardening remains
required there. Upstream updates held; no hardware/update/push. Ocelot/archive/DBC
preserved; physical power/VBUS/current recovery unqualified.
[Session](../Sessions/2026-11-06-chimera-legacy-health.md) records exact checks/limits.

## November 6 — Bootstrap status/capability contract verified

QA-20261106-22: T05a adds strict pure A0/D6 discovery decoding and a status
contract; actual firmware replies decode, unsupported health/safety stays STALL.
28offline tests pass (five new); mutation review detects missing reserved checks.
Firmware sources/image unchanged:7448bytes, SHA d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698.
No operational readiness/measurements, managed admission or startup attachment.
Next T05b source-backed legacy F4health59 decoding/adaptation before managed use;
Chimera operational health/bulk/controller binding and physical power/VBUS/current
recovery remain pending. Upstream checks held; no hardware/update/push.
[Session](../Sessions/2026-11-06-chimera-status-contract.md) records sources/tests/limits.

## November 6 — Detached USB service composed and verified

QA-20261106-21: T03b3b adds usb_service.c/.h, real facts/timing/clock/core/EP0
composition with owned IO, pre/post detached guards, failure latching and checked
release.23tests/44pipeline scenarios pass; raw7448bytes, globals8bytes. Main and
all prior helpers/linker unchanged; no service instance/startup call/attachment.
[Session](../Sessions/2026-11-06-chimera-usb-service.md) pins exact output/limits.
Next board T05a status/capability semantics and offline response fixtures before
operational health; bulk CAN binding and host legacy status/lifecycle pending.
Actual startup/attachment still requires power/VBUS/current-recovery evidence.
No device/flash/reset/config/actuation/install/update/push; Ocelot/archive/DBC
preserved, upstream checks held. Full T03 and end-to-end integration stay partial.

## November 6 — Progress explained; USB startup requirements established

QA-20261106-20: added plain-language progress guide and power/VBUS/UID/watchdog/
recovery contract. T03b3a adds read-only boot facts (UID/raw reset/options), no
startup call.21tests pass incl65536snapshot vectors; raw6608bytes, globals8bytes.
Original USB forces session-valid, PA9 is assigned UART in common init; actual
VBUS route/supply profile unknown. Historical nightly/bootstub bundle and17config
file hashes verified; bundle bootstub is not an installed dump. [Session](../Sessions/2026-11-06-chimera-usb-prerequisites.md)
pins details. Next T03b3b detached startup/service composition. Actual attachment
requires qualified power/VBUS/current-recovery evidence. Main/driver/host/DBC and
Ocelot/archive unchanged. No board read/write/flash/config/actuation/install/
update/push; upstream remains held. Preserved inputs are not yet sampled.

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

## November 6 — Chimera classical CAN codec implemented offline

QA-20261106-16: T04 encoder/strict TX decoder and bounded stream state now in
chimera/firmware/.14tests pass,648RX/189PythonTX vectors,4536chunk/split cases,
17280fixed-size corruptions,65536headers/10000fuzz streams; XOR limits tested.
Raw1840bytes; main/GPIO/protocol and phase0 capabilities unchanged. No USB/CAN
binding. [Session](../Sessions/2026-11-06-chimera-can-codec.md) pins commands/hashes/limits.
Next T03bUSBclock/controller/EP0 offline work; status/endpoints and hostT05/T08 pending.
No device/flash/config/DBC/actuation/update/push; original references preserved.

## November 6 — Chimera bootstrap identity/query contract implemented

QA-20261106-15: T02b adds protocol.c/.h and USB/source contracts; pure A0manifest/
D6version handler, no operational capabilities or USB wiring.12tests/458920sanitized
request cases pass; ARM byte-load check fixes inherited alignment dependency.
Raw1240bytes. [Session](../Sessions/2026-11-06-chimera-identity-contract.md) pins evidence.
Next board T04modern classical CAN codec; USBclock/EP0/status and hostT05/T08 pending.
No device/flash/config/DBC/actuation/update/push. Main/GPIO and references preserved.

## November 6 — First F413 firmware target implemented

QA-20261106-14: T01a source board/flash contract and T03a offline bootstrap now
implemented in chimera/firmware/, baseline9fa1f8110. Original startup/GPIO/main/
linker/build; raw1064bytes, nine tests with sanitizers/negative artifacts and
copied-tree determinism pass. No USB/CAN/acquisition or physical qualification.
Source pins and limits: [session](../Sessions/2026-11-06-chimera-f413-bootstrap.md).
Next board T02 identity/RPC/bus-input contract; host T05/T08 still pending.
No hardware/config/DBC/update/push. Ocelot and workspace archive preserved.

## November 6 — Native pinned USB factory/backend implemented

QA-20261106-11: T06b adds exclusive pinned USB discovery and bounded I/O, then
T02a identification before returning. No reset/config change/detach/flash;
original Chimera restricted to D6/D2 and CAN IN. Native build,33fake scenario
groups, sanitizer and real-library empty-pin link check pass;443identification
cases/native codec+interface/15Chimera Python tests pass. No real USB/daemon run.
Current startup remains SPI; next legacy status decoder then protected managed
USB selection. Teacher/Carrot/Ocelot/libusb evidence used; no install/update/push.

## November 6 — Native read-only identification implemented with teacher evidence

QA-20261106-10: owner reaffirmed proceed and teacher-first reliability. T02a
requires matching descriptor/transport serial and explicit version pin, exact
hardware/version/health contracts; Chimera has no C1/DD calls. Native/sanitized
checks:19accepted/421rejected/3invalid transports,zero writes; native codec and
interface tests plus15Chimera Python tests pass. Selector is in the library,
not startup. Next bounded USB transport/factory then status/managed integration;
full T02/T06 and board T01/T03 remain pending. No device/firmware/update/push.

## November 6 — Legacy Panda compatibility; shared native transport implemented

QA-20261106-08: owner wants older Panda support alongside Chimera. T06a adds
PandaCommsHandle and keeps SPI as its current implementation; Panda now owns the
interface. Native pandad + interface/codec tests build/pass; 15 existing Chimera
Python tests pass. Compatibility matrix distinguishes current49/hash, Carrot
F4 59/numeric versions and Chimera16-mailbox/43. T06 is partial: USB, status
adapters and protected discovery/managed lifecycle remain pending. T01/T02/T03
still required. No live device/firmware/DBC/upstream/push action.

## November 6 — Active Chimera home created inside Sunnypilot

QA-20261106-06: owner requested folder-first, incremental implementation.
S00 complete: regular `sunnypilot/chimera/`, no nested Git/symlink; README,
firmware area, T01–T20 sequence, exact source map/receipt and provenance saved.
Workspace `chimera/` stays the preserved evidence archive; active implementation
now belongs inside Sunnypilot. No firmware/build target or host behavior change.
Next T01 source-backed GPIO/reset and flash/config/recovery contract, then T02
identity/bus-source contracts and T03 offline target. No hardware/update/push.

## November 6 — Existing teacher facts were not reconciled

QA-20261106-05: input/transceiver facts were already recorded November 5 and
successful local builds October 4. Earlier completeness wording failed to reuse
that evidence. The firmware map consolidates known facts; do not describe them
all as newly discovered. Follow existing reports/source before calling data
missing. Correction documented; no runtime/hardware action or push.

## November 6 correction — firmware pin map and legacy build are available

QA-20261106-04: followed the owner's pointer into Ocelot firmware and its shared
board files. The logical GPIO/CAN/transceiver mapping, input/relay/OBD-C code,
776-byte config layout and existing F413 build script/toolchain are present.
Earlier gap wording was too broad: electrical connector/conditioning/load-path
proof and a qualified modern build remain open; source pin definitions and a
legacy build path are not missing. No functional code/build/device/update/push
action. Next use this source baseline for T01/T02 and the offline board target.

## November 6 — Chimera completeness audited; remaining gaps recorded

QA-20261106-03: sufficient source references for offline work, not a complete
verified hardware/installed dataset. Found 17 historical config/quarantine files
outside chimera and archived exact bytes; eight CRC-valid blocks plus one erased
incident sample. No restore or board access. Full schematic/current recovery,
exact nightly source, reproducible new build, physical CAN/input/relay evidence
and interface decisions remain open. See DATA_GAPS and student CHIMERA_DATA_GAPS.
Next T01/T02 unchanged; no runtime source, hardware, update or push action.

[Detailed student gap note](CHIMERA_DATA_GAPS.md).

## November 6 — CarrotPilot F413 and native USB source fetched

QA-20261106-01: interpreted owner spelling as ajouatom/openpilot:carrot-wip.
31selected files pinned69a2d3be; olderF413Panda build and nativeUSB/SPI retained.
CAN6/XOR matches current encoder189classical frames; health59/numeric17,4,5
instead of current49/hash versions. NativeUSB3801filter excludesbbaaChimera.
Snapshot/report under chimera/reference/carrot-wip-20261106 and student Reports.
4158splitchecks/378corruptions/native layouts pass; no hardware/firmware action.
Concrete T03/T06source candidate,not a drop-in port. Next existingT01/T02contracts;
input/relay/bus roles unchanged,updates paused,no push. Prior shutdown is historical.

[Self-contained Carrot Panda report](../Reports/carrot-wip-panda-20261106/README.md) contains source URLs and validation; no runtime change.

## November 5 — Audit published; ordered shutdown closeout

Owner requested audit,GitHub update,then PC and Radxa shutdown. Fresh21software
checks plus189/336codec vectors and94source entries/93copies pass. Published
audit967082679 on public Deggory/radxa-pilot:radxa/q8b; private Deggory/chimera
306c0c8/defaultplanning/modern-usb verified. Master932ff06d/defaultmaster and
support150f9371 preserved. Final notebook commit follows; actual final remote SHA
and normal PC-first/Radxa-last requests/readbacks are in teacher shutdown receipt.
No force discard/kill; physical poweroff not inferred. Runtime/firmware unchanged,
Ocelot dirty work preserved,upstream updates paused. QA-20261105-14.
Next restart: review chimera/tasks/plan.md,then T01/T02board-memory/recovery,
identity/RPC/bus-source contracts. Modernization remains proposed,not installed.

# Chimera modernization roadmap — 2026-11-05

Owner wants the F413 board connected by USB to our Radxa Sunnypilot, preserving
bus0 Cores,bus1 ADAS,bus2 vehicle; IGN/VSS/CPS/BRAKE/ADC1/2; onboard power relay;
and usable RetroPilot Core Config. Research/roadmap precedes firmware changes.
QA-20261105-13 records the actual answer and limits. In the Comma workspace the
board folder is [chimera](/home/radxa/comma/chimera/README.md), with
[roadmap](/home/radxa/comma/chimera/tasks/plan.md) and
[research](/home/radxa/comma/chimera/docs/RESEARCH.md). Those links are workspace
references; this summary and prior deep review remain available in a standalone
Sunnypilot clone.

Native pandad currently usesSPIonly; plan both native USB/lifecycle and F413
six-byte/XOR classical-CAN firmware,exact health/version/capability handling.
RejectFD; distinguish Chimera identity and prevent H7update/DFUsweeps. Board
app0x08004000and config0x08020000require explicit size/partition/recovery gates.
Core Config's16-byte USB codec must change; retain distinct board-settings and
typed-CoreCAN workflows,exclusive offroad ownership and transactional persistence.

Preserve physical buses; generated reports0x50/75/76/100are on0,currentphysical
parser2is not automatically fed. Define sources/local delivery and invalidation.
Safety hooks must guard host/generated/forwarded/maintenance TX. Existing mode39
production has no active profile. Input-endian/RPM/schema/freshness defects need
specific tests; preserve raw acquisition rather than inheriting those defects.

Onboard PB0relay follows ignition in local code with request gating commented.
Wiki establishes3CAN0 12VRoutputs only,not all actuator feeds. Latestownerrequest
includes preserving/qualifying this circuit; earlier blanket relay exclusions
are superseded only to that extent. OBD-C is a separate comma CAN/power/sideband
accessory connector,not Radxa's ordinaryUSBport. PA2request/PB1ignition code exists;
Chimera electrical pinout remains unknown. Keep accessory features disabled until
qualified and unable to override MCU safety.

Pins:e888f939researchbaseline/Panda8a16e089/opendbc150f9371/Ocelotd87892fadirty.
94manifest entries/93copied,75priorhashes match. Originalnightly/provenance,board
photo,officialcomma connectorPDF and download limits retained. Selected source
review,prior matchingREAELFreuse; no newREA/deviceproof. Folder/docs implemented;
all20firmware/host tasks pending. No application/firmwarechange,device/config/TX/
relayaction,push or upstreamupdate. Currentfreshvalidation is document/artifact
integrity; historical189/336vectors+21tests are not rerun. Next owner review then
T01/T02partitions,recovery,identity/RPCandbus-source contracts.

2026-11-06 location clarification QA-20261106-02: confirmed chimera/evidence,reference,hardware,recovery and tasks/plan.md exist. Latest Carrot snapshot is reference/carrot-wip-20261106; portable copies remain in Sunnypilot Ai/Reports. No project behavior or next-task change.
