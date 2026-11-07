## November7 — VBUS supervision and stage percentage reporting (T03c3a)

Owner: "proceed after each stage show in % were we reached" (QA-20261107-10).
Standing Chimera preference: after each completed stage report its actual result,
overall rough completion/remaining percentage and new-firmware hardware validation.
Current overall estimate about25% complete/75% remaining, consistent with QA06's
20–25% range; no agreed effort weights and no automatic increment per tiny slice.
Current T03c3a stage100% implemented/verified offline; new-firmware physical proof0%.
Main poll now requires fresh PRESENT observations before/after the service call.
Missing/invalid/unknown/absent readings stop detached USB, revoke facts and latch
USB_POWER. Original service faults retain their cause; cleanup failure retains
ownership, no automatic retry/sampling/restart. Explicit stop/start resets the
observation. Main still passes NULL profile/reader; no real detector/attach exists.
33firmware tests pass,16new real-component ASan/UBSan scenarios plus existing51;
before/after guard mutations detected. Raw8108/globals256/stack4096, unsigned,
unflashed. Baseline1dd5a7f63920;25build inputs,22unchanged/3intentional changes.
Teacher source evidence still lacks exact board power/VBUS/current recovery proof.
Next: qualify actual board power/profile/VBUS/installed recovery facts, then bind
physical reader and implement attached-mode lifecycle; hostT08b2d stays queued.
No hardware/update/push. Evidence: student Ai/Evidence/chimera-main-power-20261107.json.

## November7 — Main detached USB coordinator verified (T03c2)

Owner said "proceed" after the main/startup explanation (QA-20261107-09).
Actual ARM reset now calls main_start and retains bounded service polling. New
main_runtime.c validates explicit configuration, preserves UID identity between
snapshots, latches failures and supports explicit stop/restart with cleanup
ownership retained on failure. The board build supplies NULL profile and remains
USB_HELD: no physical attach or operational USB/CAN/input/Config work claimed.
32firmware tests pass, including51new real-component/fake-register scenarios,
ASan/UBSan, ARM call checks and two detected guard mutations. Raw8032bytes,
globals252, stack4096; unsigned/unflashed. Baseline6865244e73ef;25build-input hashes,
20old inputs unchanged/four intentionally changed plus main_runtime.c. Saved
Ocelot39dirty entries/19hashes, archive/DBC/submodules and host/model/camera/Thneed
preserved. No device/update/push. See student Ai/Evidence/chimera-main-runtime-20261107.json.
Next: board power/profile/VBUS and installed recovery facts, then attachment/
cable-loss policy; hostT08b2d remains queued. Earlier T03c1 notes are historical.

## November7 — New firmware selected; main startup increment verified

QA07/T03c1: owner chose new Chimera path and main.c first. ARM reset now binds
ordered read callbacks after quiet RAM/IRQ/clock setup and calls actual checked
boot preparation. Captures stable UID/raw reset/options in local diagnostics,
revokes validity on failures and ends USB_HELD5; fault handler clears validity.
USB service/attachment, DWT timing, CAN/input sampling remain unstarted; power/
VBUS/current recovery unqualified.30firmware tests incl native actual preparation
ASan/UBSan65536snapshots and ARM call proof pass; clock-guard mutation fails.
Freestanding memset link issue corrected by passing only fully bound callbacks,
no libc shim/suppression. Newraw7592bytes/globals32/SHA
fbce0bfa171b2bedca369d9913f6e3b661cadfa8ccf8a69063e0b9935b1020d1; unflashed.
Baseline7448-byte image preserved ignored, historical receipts unchanged. Four old
firmware files intentionally changed;19old sources plus Ocelot39dirty entries/
19hashes, archive/DBC/Panda/opendbc and host/camera/model/Thneed preserved.
Next main work: qualified USB startup profile and recovery/fault handling before
service initialization/attachment. Host T08b2d queued behind owner priority.
C2-era host-only option remains preserved/unselected. No hardware/update/push.
[Session](../Sessions/2026-11-07-chimera-main-startup.md).

## November6 — GitHub verified; PC shutdown unreachable

**Actual publication closeout, November6:** Audit148f77d272e81eccfb7b7f9a195ce9acb8a4f783
pushed normally toDeggory/radxa-pilot:radxa/q8b. Remote SHA matches; GitHub
connector README blobc0f96337cd2a3b1410d2096bc23f52580fd416f1 matches localGit.
Supporting opendbc ref150f9371 already matches. Defaultmaster/upstream preserved.
Final strict PC10.43.0.216 attempt again returns255/no route; alternate refusals/
timeout saved. No authenticated PC shutdown delivered, physical power unknown.
Owner's address/status question remains unanswered. No Radxa shutdown requested.
This follow-up saves actual publication and failed shutdown delivery; next remains
November7 T08b2d passive normal-status publication and disconnect/reconnect.

## November6 — Chimera audit saved; November7 restart fixed

Owner requested audit/save/GitHub update/PC shutdown and tomorrow continuation.
Baseline05a33eb1c;33local commits after remotec1811280, all with latest passing
validation. Fresh56host+68control assertions+28firmware tests (152total),10native
and2existing sanitizer binaries pass offline. Audit found bare control runner
hangs at existing StatLogSP shared-ZMQ destructor; bounded stack saved. After-suite
closure of both metrics sockets gives clean exit0 without altering assertions or
production code. Historical68pass reports established assertions, not clean exit;
production stats teardown remains unresolved.23firmware hashes/7448-byte image,
Ocelot39dirty entries/19hashes, references/archive/DBC and camera/model/Thneed
preserved. No board/runtime/upstream integration. Main README now shows Chimera
state and next step. Publish authorized toDeggory/radxa-pilot:radxa/q8b, normal
push only; retain defaultmaster. Actual publication/shutdown follows closeout.
PC10.43.0.216 unreachable;10.42.0.216 times out;192.168.1.104 refusesSSH. No PC
shutdown delivered; owner asked for current status/address. Current Radxacomma
not selected for shutdown by this request. Tomorrow November7: T08b2d passive
normal-status publication and disconnect/reconnect handling; retain invalid/
observation-only legacy status, no stale reuse/SPI fallback/control admission.
[Session](../Sessions/2026-11-06-chimera-audit-closeout.md).

## November6 — PandaState availability and consumers verified

QA32/T08b2c: appended typed statusAvailability metadata; legacy preview remains
invalid and observationOnly with all6missing current fields. Shared all-or-none
batch guard checks validity/profile/required fields; retained consumers check
liveness. hardwared/manager/UI/core/MADS now use it; missing lateral support
cannot look like a measured false. Historical metadata-absent current producers
retain their prior contract, not authentication. Current D2/C2 reads require
exact49/64bytes and bounded healthy ownership. Native build/10native programs,
56focused+68control/power/fan Python tests, two ASan/UBSan suites, native/Python
serialization and7-failure observation mutation pass offline. Existing MADS
fixtures now use real Cereal plus valid/alive metadata; no assertions suppressed.
Pandad SPI removal is committed as0fedef7b0; final binary has no SPI handle or
preview symbol. USB still emits no pandaStates and grants no operational legacy
admission. Hardware/live IPC untested.23firmware hashes/7448-byte image,
Ocelot39dirty entries/19hashes,5reference hashes, archive/DBC and camera/model/
Thneed preserved. Updates held; no push/device/flash/config/TX. Next T08b2d:
passive normal-status publication and disconnect/reconnect policy, keeping
legacy observations nonoperational; operational firmware/bench work remains.
[Session](../Sessions/2026-11-06-chimera-availability.md).

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
