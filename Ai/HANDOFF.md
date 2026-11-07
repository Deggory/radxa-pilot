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


November7 QA08 clarification: main.c change is checked boot diagnostics only,
not completed Sunnypilot USB integration. Snapshot is local RAM, not USB health;
USB_HELD is a deliberate software stop, not a detected power fault or an automatic
hardware qualification algorithm. Explain power supplies, USB5V/VBUS detection
and bootloader/DFU rollback/settings preservation in plain terms. Offline USB
startup/service work can continue while live-attachment qualification is pending.
Source228ed567e; no implementation/test rerun/hardware/update/push. Main-first
scope and next qualified startup/recovery work remain; hostT08b2d queued.

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
[Session](Sessions/2026-11-07-chimera-main-startup.md).


November7 QA06: owner explicitly requests a progress percentage for the complete
new Chimera idea. Rough subjective planning estimate20–25% implemented/75–80%
remaining overT01–T20;2offline tasks complete,5partial,13pending. Unequal tasks/no
agreed effort weights mean no measured completion/time fraction. New implementation
physical qualification0%. Earlier no reliable measured percentage remains true.
No code/roadmap/route change or hardware/test rerun/update/push. Source9a7489f8c;
next still T08b2d. C2-era host-only alternative remains unselected.


November7 QA05: owner requests an option only, explicitly no implementation:
retain C2-era/original Chimera firmware and adapt Sunnypilot USB/CAN/status/
lifecycle to its exact legacy profile. Viable compatibility strategy for passive
integration; original mailbox16/health43 differs from C2CAN5/health50 and currently
managed F4CAN6/health59. Retain exact firmware/input/config behavior and canonical
DBC with explicit adaptation. Existing MCU/relay defects remain; minimum device-
side safety must be qualified before real actuator commands. New bootstrap work
preserved; no route selected/roadmap or code changed. Exact intended C2image is
unresolved for a future choice. Sourcee8cd79f90; no hardware/tests rerun/update/push.


November7 QA04 main.c explanation:74line minimal bootstrap initializes RAM/IRQ/
internal clock/inactive board state, records boot status and parks. USB driver,
EP0/service and codec are separate offline modules; main calls none of them.
Smallness reflects modularity plus pending operational integration, not completed
USB/CAN firmware. Future main can stay compact as orchestration. Sourceb32b0e9b9,
read-only explanation, no application/hardware/test rerun/update/push. Next remains
hostT08b2d passive normal-status publication/disconnect/reconnect.

## November7 — Stop now; resume Chimera this evening

Owner: "please  shutown now and  will see this in evening". Save work and request
normal shutdown of current Radxahostcomma. Baseline3ec39ebc2ed477309750727bf737d8020b8e4c70,
clean before notebook closeout; today's two explanation commits are local, not
pushed. No application/firmware/runtime implementation resumed. Evening next:
T08b2d passive normal-status publication and disconnect/reconnect handling,
keeping legacy observations nonoperational. Use normal GNOME poweroff with
application/inhibitor cleanup; physical poweroff cannot be asserted in advance.
Actual request/timer readback follows in the shutdown receipt. No remote-PC
connection attempt or upstream update/push is part of this request.


November7 follow-up QA-20261107-02: owner asks about complete replacement and
bidirectional data. Confirm intended Panda-style USB/CAN role forRadxa: CAN→
Chimera→USB→Sunnypilot and reverse through MCU TX policy. Current implementation
remains passive/offline; bootstrap/controller binding and guarded TX/bench work
pending. Three classical CAN buses, truthful declared capabilities; no blanket
H7 feature/physical readiness promise. Existing board inputs/CoreConfig/relay/
OBD-C requirements retained. Next remains T08b2d passive status/reconnect.
Explanation only, source6f788e922; no application/hardware/test rerun/update/push.

## November7 — Status metadata/read-length explanation saved

QA-20261107-01 explains the six unsupported legacy status fields and why a
missing value must not become measured zero/false. Status sizes depend on the
qualified profile: currenthealth49, legacyF4v17health59, controllerhealth64bytes;
short/overlong replies reject. Source verified atdfd316d65, no implementation or
hardware/test rerun/update/push. Documentation only. Next remains T08b2d passive
normal-status publication and disconnect/reconnect; legacy stays observation-only.
[Session](Sessions/2026-11-07-chimera-status-explained.md).

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
[Session](Sessions/2026-11-06-chimera-audit-closeout.md).

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
[Session](Sessions/2026-11-06-chimera-availability.md).

## November6 — Pandad SPI removed; metadata increment in progress

QA31: owner corrected generic-SPI retention. Removed pandad SPI source/class/build/
listing and both generic entries; all platforms require pinned USB. Current Panda
constructor qualifies USB and performs no reset/config.10native/42Python checks
plus strict fake-USB sanitizers pass. ASan reproduced/fixed short-header heap read;
exact tests/output in receipt. Metadata test is RED/uncommitted; continue next.
No hardware/update/push; firmware23hashes preserved. Earlier SPI-retention notes
are superseded. [Session](Sessions/2026-11-06-chimera-remove-spi.md).

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
[Session](Sessions/2026-11-06-chimera-legacy-state.md).

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
[Session](Sessions/2026-11-06-chimera-panda-validity.md).

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
[Session](Sessions/2026-11-06-chimera-usb-receive.md).

## November 6 — Radxa USB-only status startup implemented

QA27/T08a: Radxa wrapper/native entry bypass legacy reset/flash/SPI for mandatory
serial/version-pinned USB status session. Legacy F4v17 only; no CAN/pandaStates/
control threads or ready claim. Failure closes; no cache/retry/SPI fallback.
21Python/7native/sanitizer checks pass; five invalid native invocations exit2,
main.o has no legacy-thread reference. No pins installed or valid hardware run.
Firmware/Ocelot/archive/DBC preserved; updates held. Next T08b passive CAN and
validity-aware publication/exact-read/freshness/reconnect. Other profiles pending.
[Session](Sessions/2026-11-06-chimera-usb-startup.md).

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
[Session](Sessions/2026-11-06-chimera-can-health.md).

## November 6 — Owner progress summary

QA-20261106-25: offline foundations implemented; most operational integration
and all new-firmware physical qualification remain. Saved28firmware/discovery,
6native/15Python/sanitizer results are offline, not end-to-end. Image7448bytes
unflashed/parked; USB-only managed startup still pending. Inputs/Core Config/
MCU policy/relay/OBD-C and bench/release work remain. No reliable percentage.
Next T05c per-bus health. Summary/docs only; no runtime/hardware/update/push.
[Session](Sessions/2026-11-06-chimera-progress-summary.md).

## November 6 — Owner requires USB only for Radxa/Chimera

QA-20261106-24: owner says “no spi is needed since we will use usb only”.
USB-only target excludes SPI wiring/probing/fallback. Updated active plan/rules;
inherited native constructor still opens SPI and awaits T08 pinned USB startup.
Requirement correction only, no runtime/code/hardware change. Next remains T05c
per-bus health, then USB-only managed lifecycle. Upstream updates held.
[Session](Sessions/2026-11-06-chimera-usb-only.md).

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
[Session](Sessions/2026-11-06-chimera-legacy-health.md) records exact checks/limits.

## November 6 — Bootstrap status/capability contract verified

QA-20261106-22: T05a adds strict pure A0/D6 discovery decoding and a status
contract; actual firmware replies decode, unsupported health/safety stays STALL.
28offline tests pass (five new); mutation review detects missing reserved checks.
Firmware sources/image unchanged:7448bytes, SHA d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698.
No operational readiness/measurements, managed admission or startup attachment.
Next T05b source-backed legacy F4health59 decoding/adaptation before managed use;
Chimera operational health/bulk/controller binding and physical power/VBUS/current
recovery remain pending. Upstream checks held; no hardware/update/push.
[Session](Sessions/2026-11-06-chimera-status-contract.md) records sources/tests/limits.

## November 6 — Detached USB service composed and verified

QA-20261106-21: T03b3b adds usb_service.c/.h, real facts/timing/clock/core/EP0
composition with owned IO, pre/post detached guards, failure latching and checked
release.23tests/44pipeline scenarios pass; raw7448bytes, globals8bytes. Main and
all prior helpers/linker unchanged; no service instance/startup call/attachment.
[Session](Sessions/2026-11-06-chimera-usb-service.md) pins exact output/limits.
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
file hashes verified; bundle bootstub is not an installed dump. [Session](Sessions/2026-11-06-chimera-usb-prerequisites.md)
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
admission. [Session](Sessions/2026-11-06-chimera-usb-driver.md) pins details. Next
T03b3 power/VBUS/UID and watchdog/recovery prerequisites, then reviewed startup/
service/attachment. No hardware/flash/config/DBC/actuation/install/update/push;
Ocelot/archive preserved, upstream checks still held. T03 overall remains partial.

## November 6 — Owner-supplied Ocelot Panda Docker source reviewed

QA-20261106-18: pinned Deggory/Ocelot_Panda_docker main04b56ba0 and parent98de83bb.
Current panda target removes GATEWAY/uses stock Panda detection; parent retains
separate Chimera inputs/outputs. Parent Chimera main matches Ocelot committed
source.31exact source files saved;189pure sender/parser vectors, health43/offset39,
flag/preprocessor and signedness checks pass. DD means forwarding in this older
Panda, not versions; stock harness relay differs from PB0. See [session](Sessions/2026-11-06-ocelot-panda-docker.md).
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
See [session](Sessions/2026-11-06-chimera-usb-bootstrap.md).

## November 6 — Chimera classical CAN codec implemented offline

QA-20261106-16: T04 encoder/strict TX decoder and bounded stream state now in
chimera/firmware/.14tests pass,648RX/189PythonTX vectors,4536chunk/split cases,
17280fixed-size corruptions,65536headers/10000fuzz streams; XOR limits tested.
Raw1840bytes; main/GPIO/protocol and phase0 capabilities unchanged. No USB/CAN
binding. [Session](Sessions/2026-11-06-chimera-can-codec.md) pins commands/hashes/limits.
Next T03bUSBclock/controller/EP0 offline work; status/endpoints and hostT05/T08 pending.
No device/flash/config/DBC/actuation/update/push; original references preserved.

## November 6 — Chimera bootstrap identity/query contract implemented

QA-20261106-15: T02b adds protocol.c/.h and USB/source contracts; pure A0manifest/
D6version handler, no operational capabilities or USB wiring.12tests/458920sanitized
request cases pass; ARM byte-load check fixes inherited alignment dependency.
Raw1240bytes. [Session](Sessions/2026-11-06-chimera-identity-contract.md) pins evidence.
Next board T04modern classical CAN codec; USBclock/EP0/status and hostT05/T08 pending.
No device/flash/config/DBC/actuation/update/push. Main/GPIO and references preserved.

## November 6 — First F413 firmware target implemented

QA-20261106-14: T01a source board/flash contract and T03a offline bootstrap now
implemented in chimera/firmware/, baseline9fa1f8110. Original startup/GPIO/main/
linker/build; raw1064bytes, nine tests with sanitizers/negative artifacts and
copied-tree determinism pass. No USB/CAN/acquisition or physical qualification.
Source pins and limits: [session](Sessions/2026-11-06-chimera-f413-bootstrap.md).
Next board T02 identity/RPC/bus-input contract; host T05/T08 still pending.
No hardware/config/DBC/update/push. Ocelot and workspace archive preserved.

## November 6 — README completion is not a remaining gate

November6 QA-20261106-13: README/setup already complete, not a remaining coding
gate. Host USB code exists; future MCU code belongs in sunnypilot/chimera/firmware/
and is still pending the board/flash/build contract. Explanation only; no new
implementation, build or hardware action.

## November 6 — Host code locations versus pending board firmware

November6 QA-20261106-12: clarified actual code locations. New host USB and
identification are in Sunnypilot openpilot/selfdrive/pandad/, not the board
firmware directory. New F413 firmware is not written; chimera/firmware/ has only
README. Added clickable host-code map and explicit status to chimera/README.md.
No source move/duplicate, product change or new runtime test; next T05 unchanged.

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

## November 6 — SPI/USB meaning and next slices explained

November6 QA-20261106-09: SPI means the retained integrated-board connection;
Radxa/Chimera will use USB. Explained common interface versus actual backend,
old Python mailbox decoder versus native integration, and the sequence:
read-only identity/profile tests → bounded USB backend → status adaptation →
protected managed passive lifecycle → separate hardware qualification.
Explanation/doc update only; no implementation advanced. Next profile tests.

## November 6 — Legacy Panda compatibility; shared native transport implemented

QA-20261106-08: owner wants older Panda support alongside Chimera. T06a adds
PandaCommsHandle and keeps SPI as its current implementation; Panda now owns the
interface. Native pandad + interface/codec tests build/pass; 15 existing Chimera
Python tests pass. Compatibility matrix distinguishes current49/hash, Carrot
F4 59/numeric versions and Chimera16-mailbox/43. T06 is partial: USB, status
adapters and protected discovery/managed lifecycle remain pending. T01/T02/T03
still required. No live device/firmware/DBC/upstream/push action.

## November 6 — Board/build steps explained

November6 QA-20261106-07: explained T01 as board GPIO plus bootstub/application/
config ownership and T03 as a minimal offline F413 image/build/size check. Legacy
app0x08004000/config0x08020000 are source facts; this is not a new build or
installed dump. Modern USB/host compatibility follows later. Owner asked for
meaning; no implementation advanced. Next T01/T02/T03 unchanged.

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

## November 6 — CarrotPilot F413 and native USB source fetched

QA-20261106-01: interpreted owner spelling as ajouatom/openpilot:carrot-wip.
31selected files pinned69a2d3be; olderF413Panda build and nativeUSB/SPI retained.
CAN6/XOR matches current encoder189classical frames; health59/numeric17,4,5
instead of current49/hash versions. NativeUSB3801filter excludesbbaaChimera.
Snapshot/report under chimera/reference/carrot-wip-20261106 and student Reports.
4158splitchecks/378corruptions/native layouts pass; no hardware/firmware action.
Concrete T03/T06source candidate,not a drop-in port. Next existingT01/T02contracts;
input/relay/bus roles unchanged,updates paused,no push. Prior shutdown is historical.

## Actual shutdown request checkpoint — 2026-11-05

PC original normal GNOME shutdown initiated; SSH now unreachable. A retry failed
to connect and was not delivered. Radxa normal GNOME poweroff timer queued and
confirmed active/waiting,120s delay,unitchimera-radxa-poweroff-20261105T213004Z.
No force/discard/inhibitor override; physical poweroff not directly observed.
Student Reports/chimera-shutdown-audit-20261105/shutdown-request.json and teacher
receipt record actual results. Chimera private closeout77464e0published; source
snapshot306c0c8 unchanged. Final notebook push follows; next roadmapreview/T01/T02.

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

## November 5 — Modern Chimera roadmap and dedicated board folder

QA-20261105-13 records the owner's USB modernization goal and research-first
scope. Created `/home/radxa/comma/chimera/` with94source entries,93copied inputs,
board/OBD-C/recovery evidence and20proposed implementation tasks. Two-sided work:
F413 modern classical USB framing plus nativeUSB/managed host support,Core Config
transport/schema adaptation,explicit bus0/1/2source ownership and all-TX MCU policy.
Preserve IGN/VSS/CPS/BRAKE/ADC1/2and onboard relay; earlier relay exclusion is
superseded only for this circuit's preservation/qualification roadmap. OBD-C code
exists(PA2/PB1),electrical mapping unverified; relay does not prove all-load cutoff.
No functional source/device/flash/config/relay/TXaction,push or upstream update.
Next owner review of roadmap,then T01/T02partition/recovery/identity/bus contracts.

## November 5 — Deep Panda/legacy/Chimera reference saved

QA-20261105-12 records teacher-first review of current Panda8a16e089,C2and mailbox
legacy,Chimera and our receiver.75source hashes;189mailbox/336modern vectors and
21existing tests with fresh native comms fixture pass. New finding: generic
Panda connect emits9setup writes(7with disable_checksFalse)before late filtering;
do not use it as passive Chimera probe. Current MCU safety hooks differ from
Chimera’s unguarded TX; generatedCAN0/current parserbus2routing remains explicit.
Exact nightly source lookup404; matching historical REA ELF reused,not installed
proof. Production source/device state unchanged; updates/actuation holds retained.
Next owner-selected installed-capability,managed-RXor safety work using the report.

## November 5 — Chimera native input contract explained

QA-20261105-11 isolates Chimera hardware/firmware: IGN,VSS,CPS,BRAKE,ADC1/2;
configurable CAN2vehicle angle/rate/speed/ignition/RPM/brake entries1–7. CAN cruise
menu11–14is not implemented by RX handler; ADC button matching exists. CAN0
reports0x50/75/76/100are generated outputs,not fixed OEM input IDs. Local integer/
endian/RPM/integrity/output-path limits retained. No source/device action; next
owner-selected mapping/installed-image review,upstream/actuation holds unchanged.

## November 5 — Wiki vehicle-side bus clarified: CAN2

QA-20261105-10: official Chimera Installation connects car CANH/CANL to CAN2
(board/hostbus2,MCUCAN3). Separate OBD-C is described for comma devices; no
car-side OBD pinout is specified. Documentation only; wiring/device state and
zero-frame result unchanged. Next confirm physical label/receive path; holds stay.

## November 5 — Ocelot Chimera source inspected directly

QA-20261105-09 records source map and receive-path findings. Local raw RX on all
3buses feeds USB regardless of configured signal mappings. GATEWAY init enables
transceivers; health voltage/current and safety17are constants, not measurements
or enforcement proof. Stored bitrate fields do not set startup speed. Default
Core Config is read-only WebKit; separate Tk tool has guarded writes. Retained
nightly image27976bytes matches saved hash; exactde193215source absent locally.
Ocelot’s pre-existing dirty files preserved; no source/device/build/flash action.
Next: installed-behavior and physical CAN receive qualification; noOutput and
relay/actuation limits retained, upstream updates paused.

## November 5 — Chimera teacher review; physical receive is next

Owner resumed Chimera and requested everything the teacher knows. QA-20261105-08
synchronizes the answer. Same Chimera serial is freshly visible via lsusb/sysfs;
versionde193215 and health43 remain historical reads. Physical receive still0
frames after117genuine game samples;492/492software replay is separate evidence.
Corrected silent-mode lead: can.h maskFF does not establish startup silent state;
main.c explicitly initializes all3controllers silent=false. Exact nightly state,
connector/termination/transceiver rails/bitrate/ACK remain unknown. October4
nightly recovery and verified watchdog-off SYS_CFG supersede older empty-config
wording, without a new config read. No device handle, firmware/config writes,
source/control change or push. Upstream updates stay paused. Next: qualify the
actual physical receive path with noOutput and relay/actuation limits retained.

## November 5 — rednose_repo is required, keep it

Owner asked what rednose_repo@28d4a7f is. Source confirms Kalman-filter estimation
used by localization and vehicle-parameter learning; build and Python imports
require it on Radxa. Parent4d6b4c87; child28d4a7f69e80e1c3e0d24ca0733d7daeaeade3d0
matches GitHub. QA-20261105-07 records purpose, consumers and unqualified sensor
integration limits. No source/submodule change, push or runtime test. Next owner
folder question; upstream updates stay paused and Chimera work remains separate.

## November 5 — msgq_repo is required, keep it

Owner asked what msgq_repo@e7396e7 is. Source confirms core process messaging and
VisionIPC camera transport, used by build/cereal/camera/model paths on Radxa.
Parent3a4e97135; submodule e7396e76dadbb49e374d4b664ff6bbb43a39bcb0 matches GitHub.
QA-20261105-06 records the explanation and exact consumers. No source/submodule
change, push or runtime test. Next: further owner-selected cleanup questions.

## November 5 — Docs file-by-file cleanup advice saved

Owner asked purpose/keep advice for GitHub Q8B docs. Inspected29tracked entries
at public/localc93bd4197;390999logical bytes. Keep project/safety/debugging/porting
references. Comma-only tutorials and website/upstream extras are optional, with
navigation/generator/assets dependencies retained until deliberate cleanup.
QA-20261105-05 and the complete inventory record recommendations; no docs removed
or edited and no push/runtime/hardware action. Next owner chooses cleanup scope.
Existing upstream update hold and separate Chimera receive qualification remain.

## November 5 — JetBrains folders removed and published

Owner explicitly authorized local and GitHub Q8B deletion. Removed six .idea/.run
files (6251bytes) in52afd7a3 and pushed radxa/q8b; independent REST/Git readback
passed. .github/.vscode hashes unchanged; master932ff06d/support150f9371 untouched.
Earlier three local documentation commits are now published too. QA-20261105-04
and dated removal evidence supersede the proposed-only status below. No runtime
source change/test or upstream integration. Next: owner-selected folders or the
separate Chimera receive task, preserving noOutput/relay limits and update hold.

## November 5 — Development-folder cleanup explanation

Owner wants folder purposes before project cleanup. Inspected .github/.idea/.run/
.vscode; all171350bytes. JetBrains .idea+.run are removable candidates for VS Code
use (6251bytes); retain .vscode and recommend retaining GitHub workflow/templates.
Nothing deleted, moved or hidden. QA-20261105-03 and the source/size inventory record
recommendations separately from implementation. No new runtime/hardware test/push.
Next: explain next selected folders; keep Chimera diagnostics and update holds.

## November 5 — GitHub comparison direction corrected

Owner wants Radxa compared against official master. GitHub default changed from
radxa/q8b to master; independent readback passed, all remote branch tips unchanged.
Radxa shows113ahead/3behind master. Counts reflect commit identities, including
separately cherry-picked prior upstream changes. No merge or automatic update.
[Receipt](Reports/github-master-sync-20261105/default-branch.json).
QA-20261105-02 supersedes earlier default-view statements. Chimera remains next.

## November 5, 2026 — GitHub master equals official Sunnypilot

Owner requested GitHub master match real Sunnypilot. Completed normal fast-forward
8cf6ff9a→932ff06d; remote masters independently verified equal. Remote Radxa
f193a3cb and child150f9371 unchanged; default view remains radxa/q8b. Only local
documentation follows. New upstream modeld_v2 low-speed curvature fix was discussed
but is not applied to Radxa. Timer inactive/linked; automatic updates stay paused.
[Report](Reports/github-master-sync-20261105/README.md).
Next remains Chimera receive diagnostics, with noOutput/relay/actuation limits.
Earlier shutdown entries below describe November4; this is the reopened session.

## November 4 shutdown audit — next session November 5: Chimera

Audit/save and GitHub publication verified: fresh165tests pass; DBC and six PC
source/doc files match. Public radxa/q8b and child150f9371pass fresh source-download
checks; default viewRadxa,master8cf6ff9a preserved,Actions disabled. PC kernel42/
GTX1650/595.99.02 healthy; no game/gateway running. Last physical CAN0frames.
Tomorrow November5 start Chimera connector/power/termination/ACK/bitrate and receive
qualification with noOutput and relay/actuation limits retained. Next final action:
normal PC poweroff first,then VS Code/Radxa session shutdown; no force discard.
No automatic upstream update or firmware work now. Central shutdown receipt records
actual request/readbacks; physical completion after host poweroff is not claimed.

2026-11-04 later follow-up: additional Sunnypilot/BeamNG requirements explained and recorded in Q&A16; sender folder opened on PC and Radxa, gateway.py in VS Code. PC network reachable again and pending README copy completed. No code/control/firmware change or new CAN test; physical reception remains unqualified.

2026-11-04 latest checkpoint: NVIDIA repair passed without reboot (GTX1650/595.99.02; kernel38/42 modules; clean dpkg audit); BeamNG runs. Shared RP-SIM-1/PC/Radxa implementation saved at parent880a0adb and child150f9371. Genuine post-start capture492/492 yields valid passive CarState/canValid; 17 focused tests plus regressions pass. Physical CAN gate remains unresolved: genuine game117samples submitted via Waveshare,0Chimera frames. Owner reports CAN3, USB-only Chimera power and Waveshare resistor removed. Next qualify termination, transceiver rails, bitrate and ACK/silent mode; firmware/manager/actuation holds remain. No upstream update or push. PC link became unreachable after captures; restore it before further live work (last README clarification copy pending).

2026-11-04 active BeamNG CAN increment: PC Lua producer/Waveshare gateway, RP-SIM-1 additive DBC, independent Radxa decoder/monitor and explicit receive-only RETROPILOT_BEAMNG profile implemented. 17 focused checks pass plus existing regressions. PC CH340 confirmed and files installed. Live game test blocked by missing NVIDIA modules for running kernel7.0.0-38; owner authorized repair, reviewed package script is waiting for local sudo authentication in PC terminal. No repair success, physical CAN delivery, localization fusion or control is claimed. No reboot or upstream update authorized.

2026-11-04 two-day owner Q&A backfill complete: [62 chronological records](QUESTIONS.md) (47 on November 3,15 on November 4) with [exact original questions/58 completed answers](Evidence/owner-qa-20261103-04.json). Three requests link to clarification continuations; this request has a separately labelled closeout. Existing Q&A/unknowns retained. Local documentation only; no push. Continue recording later questions and read related answers before follow-ups.

2026-11-04 owner Q&A memory rule implemented:explicit recent questions AND actual answers in [existing question log](QUESTIONS.md); startup/closeout instructions require retrieval and continued recording. Older unknowns retained; summaries are not full transcripts or automatic model training. Documentation only,local commit/no push.

2026-11-04 dual-DBC question answered:multi-parser support verified; OEM+RetroPilot requires explicit CarState integration, currently absent. No source/hardware change or push. [Details](Knowledge/RETROPILOT_CAR_PORT.md).

2026-11-04 dzid/ZSS clarification complete:SSC command/status0x22E/0x22F and ZSSangle0x50 already defined; matching layouts do not resolve dzid checksum/controller integration or physical calibration. Source/DBC unchanged; notebooks local only. [Details](Knowledge/RETROPILOT_CAR_PORT.md).

2026-11-04 DBC explanation complete:20messages/120fields,12reports/8commands; all signal names inventoried, defined data distinguished from current CarState mapping and actual producer/calibration. DBC and code unchanged, no live test. [Details](Knowledge/RETROPILOT_CAR_PORT.md). Notebook changes are local; no new remote push.

## 2026-11-04 — Radxa project published to owner GitHub

Public `Deggory/radxa-pilot`:master is original8cf6ff9a,radxa/q8b contains
our project and preserved commits,opendbc/retropilot retains child671f8c4.
All pre-task commit IDs retained; no source/model/history rewrite.290LFS
assets uploaded; fresh recursive checkout verifies all7dependency pins.
The existing sunnypilot-pc fork is untouched; new repo is a standalone public
copy. Camera/Thneed/RetroPilot bytes unchanged; live control stays disabled.
GitHub Actions and automatic upstream updates remain disabled/paused.
See [publication report](Reports/github-publication-20261104/README.md) for source pins, transfer evidence, tests and limits.

## 2026-11-04 — Owner-authorized GitHub publication in progress

Private `Deggory/radxa-pilot` created. Original `master`, Radxa branch and
RetroPilot support history are the accepted scope; only Sunnypilot project
contents. Portable submodule/LFS metadata prepared, large assets uploading,
remote clone verification pending. Original application0758b123 and child671f8c4
source unchanged. See [publication guide](../docs/GITHUB_RADXA.md). Timer remains paused.

## 2026-11-04 — Exactly two upstream updates approved and applied

Later owner instruction authorized a86979d2 and8cf6ff9a only, preserving
camera, Thneed/model and RetroPilot. Local application commits67876efc and
a009818b onradxa/q8b; eight source paths match upstream exactly. Protected
15,384 file hashes/submodule pins unchanged; child671f8c4 clean.217 distinct
tests passed,1 existing skip; native Params rebuilt for new default-on boost
option. This is CPU/source validation, not live driving acceptance.

Automatic reference updates remain paused; future updates need approval.
No further implementation is pending for this request. No live Params,
hardware, model or actuation run. See [the approved-update report](Reports/upstream-approved-20261104/README.md) for source pins, checks,
initial failures and exact scope; older hold-only entries below are historical.

## 2026-11-04 — GitHub master checked; all upstream updates on hold

Live GitHub master is8cf6ff9a (predictive acceleration boost,#2089,Nov4UTC).
It adds AccelBoostSP/defaulton, longitudinal boost logic, settings and tests.
Previousa86979d2 gates sunnylink steering-arc toggle on MICI. GitHub is2commits
ahead of our6f7a2c94 upstream base,1ahead of the previous a869 reference check.
No source integration or compatibility test performed. Actual project master/
origin-master remain6f7a2c94; Radxa code and child671f8c4 unchanged.

The daily job already advanced only the reference to8cf6ff9a at15:30UTC before
the owner asked. New owner instruction requires approval before updates.
Automatic timer is now linked/inactive and not enabled for automatic startup;
service inactive. Do not run mutating updater check or reenable it without
explicit approval. Read-only GitHub checks are allowed. See current upstream
policy, receipt Evidence/sunnypilot-master-check-20261104.json and dated session.

## 2026-11-04 — Owner-authorized topic labels applied to Git history

Camera/Thneed/RetroPilot subjects now use camera, thneed and retropilot scopes.
64titles reworded;28camera/16thneed/29retropilot commits, with mixed scopes.
90IDs changed by ancestry; all92local file trees, dates and message bodies match
originals. New tip before report213cd6d9; original6fb457bc retained under
refs/backups/20261104-before-topic-reword. Child671f8c4/gitlinks unchanged.
Original recorded SHAs are historical evidence, not stale hashes to replace:
use Ai/Reports/commit-topics-20261104/commit-map.csv or mapping.json to resolve
current IDs.90validation histories inherited without rerunning tests;17raw
failed/blocked IDs represent9original lineages, no new software-test failure.
No code/device/DBC/model/firmware or remote change. Preserve noOutput and holds.

2026-11-04 owner requirement: Chimera + Interceptor Core + Actuator Core are
all selected required hardware for the Radxa/Sunnypilot RetroPilot project.
Jobs: computer/CAN + vehicle signals; analog pedal/steering sensor interface;
custom actuator motor control, respectively. Recorded in DECISIONS and the
RetroPilot topic/session. Selection is not installed/tested status; existing
Chimera/physical Interceptor holds, noOutput and relay exclusion remain.

2026-11-04 DBC comparison: old/canonical and packaged current ocelot_controls
are identical (7363bytes,20messages,120signals,SHAef6eef74). Current port selects
this DBC already. Direct diff/provenance pass; no code/DBC or runtime change.
C2 source explanation session records details. Existing noOutput/hardware holds
and next actual BeamNG endpoint/profile qualification remain unchanged.

2026-11-04 session reopened: parentec53967/child671f8c4 clean. Explained C2
Ocelot naming from source: module firmware family, ocelotcan.py command encoder,
DBC wire definitions; modern commands.py supplies the encoder role. No runtime
change or hardware resumption. Existing noOutput/profile/Chimera holds remain.
See Sessions/2026-11-04-ocelot-c2-explanation.md.

## 2026-11-03 — Audit saved before owner-requested shutdown

Audited parent469f3c5/child671f8c4, both clean at start;10 source hashes match.
Fresh168 tests pass:50 safety,45 port,53 CAN,20 offline adapter/migration; Ruff
passes. Prior full safety8806/932 skips belongs to unchanged source, not a new
shutdown run. Modern port/shared registrations and two-header safety split are
saved in the audit report. Production noOutput/zero CAN, missing real profile,
held Chimera/Interceptor and excluded relays remain explicit. No device action.
Next after boot: read both handoffs/inbox, verify Git, resolve actual BeamNG car/
configuration and endpoint/units/mode/driver/calibration contract. No automatic
active output or hardware resumption. Owner requests normal local Radxa shutdown
only after all saves/validation; queue/readback is central shutdown receipt.
Report: Ai/Reports/retropilot-shutdown-audit-20261103/README.md.

## 2026-11-03 — RetroPilot active safety software engine, no live profile

Child opendbc671f8c450fc74f5b8b90b2ee53124394108651ce adds profile-dependent
sensor integrity/freshness, fault-latched engagement, driver intervention and
bounded/rate-limited interceptor steering/gas/iBooster-position checks. Only
an artificial native-test fixture supplies limits; no production initializer or
firmware parameter selects an active profile. Normal mode39 remains disabled-
command-only; interface noOutput/dashcamOnly and zero runtime CAN remain.
50 focused tests pass; full native suite8806 run/932 existing skips/no failures;
45 RetroPilot host tests, release-fixture absence, Ruff and whitespace pass.
Independent review required recovery/counter/health/startup fixes; all addressed,
final no Critical/Required findings. Startup models a full16-count disable
cycle peraxis; this is not receipt acknowledgement or installed-firmware proof.
Chimera and physical Interceptor held; relays excluded; no device/game/CAN action.

Owner asked which car Caleb used: pinned5435d674 launch says user spawns a car;
README has Ibishu Covet example and ETK800 rack examples. HONDA_CIVIC_2022 was
CAN/platform identity, newer BEAMPILOT measures the selected car. Owner's actual
vehicle/configuration remains unknown. Next: qualify selected game vehicle,
endpoint/units/mode/driver/calibration contract and then game-only integration.
No production limits inferred from C2 constants, DBC ranges or a demo model.
Report: Ai/Reports/retropilot-active-safety-20261103/README.md; source/test hashes
and remaining firmware/profile limits in the matching evidence JSON.

## 2026-11-03 — RetroPilot restricted safety mode implemented

Modern opendbc a6099a1e141f17ec18ca9b065cf9a8f972e0cac8 registers local
RetroPilot safety ID 39 and a disabled-command-only C policy. Seven canonical
steering/gas/brake disable packets are checked on bus 2; active commands,
relays, malformed frames, unknown parameters and forwarding are blocked.
The interface stays noOutput/dashcamOnly and controller runtime sends no CAN.
21 focused and 8777 full safety tests pass (932 existing skips); 45 RetroPilot,
53 CAN and 303 broader car checks pass (314 broader skips). New policy has
24/24 executable lines covered; debug/release C and Cereal C++ builds pass.
No Cereal source/DBC/model/firmware changes. Chimera is held; relays excluded.
Active policy limits, RX health/freshness and engagement remain unqualified.
Next: qualify those software/vehicle requirements without resuming held hardware.
Evidence: Ai/Evidence/retropilot-safety-20261103.json and report under
Ai/Reports/retropilot-safety-20261103/. This supersedes older "no policy file"
notes, not the remaining active-control limitations.

2026-11-03 owner scope: relay features are not wanted. Current discussion is
RetroPilot safety-mode selection and enforcement. Chimera work remains on hold.
Preserve existing offline reference code; do not add relay integration.

2026-11-03 owner direction: **Chimera work is on hold until the owner resumes it.**
Current discussion is the need for modern RetroPilot messages and why C2 changed
Cereal. Earlier next-step notes about Chimera acceptance are deferred.

## 2026-11-03 — Owner clarification: modern RetroPilot implementation

The objective is to make RetroPilot work on the existing Radxa Q8B running
current Sunnypilot, with Chimera providing the CAN interface and BeamNG as
the intended initial vehicle environment. C2 is a behavioral/protocol reference.
The owner requested examination of cereal, opendbc, panda, selfdrive,
third_party and tools to understand what the author achieved and why.
Those folders and commits are research inputs, not an implementation checklist.

Identify the required RetroPilot behavior and CAN/hardware contracts, then
implement only the missing pieces through current Sunnypilot APIs. Reuse
existing modern capabilities. Do not recreate the C2 integration or require
matching edits in every old folder. Old build fixes, schemas, engagement
shortcuts and tuning machinery are not requirements merely because C2 used
them. Evaluate any proposed change against the current Radxa goal and evidence.

This clarification changes the framing, not the tested runtime status. No
runtime code was changed for this clarification. Next remains actual Chimera
receive acceptance, then current board health/lifecycle and vehicle-data
contracts. Historical review is supporting evidence, not live validation.

2026-11-03 history explanation: complete53-commit plain-English2025guide saved in
sunnypilot/Ai/Reports/retropilot-c2-history-20261103/2025_COMMITS.md.
No runtime change; actual Chimera receive acceptance remains next.

Owner communication preference: plain-English explanations first; coding details when requested. DBC inclusion rechecked; partial port versus live integration must remain explicit.

## 2026-11-03 — C2 history-led Radxa adaptation checkpoint

Owner confirmed existing Radxa Q8B. Full C2 history/submodules now mapped:
35parent commits,50final/64historical paths,82paths total. Added standalone
receive-only Chimera mailbox16/health43 adapter with pinned identity/version
and modern CAN serialization. Corrected angle STATE1 producer contract in
opendbc86a839dcec8ed9a3e45315eac804fa1001f1b2d6.15USB/45port/53CAN/303broader
tests pass (314existing skips), history coverage and Ruff pass. No live output.
REA GNU symbols/disassembly confirms retained43/16contract; native/layout
limits retained. Sysfs shows Interceptor DAC Bench, not historical Chimera;
no device opened. Current model/DBC/owner settings unchanged. Next: actual
Chimera receive acceptance, units/profile and managed truthful health/ignition;
MCU safety/physical actuation remain unqualified. Full dated session and
Ai/Reports/retropilot-c2-history-20261103/README.md record evidence/limits.

## 2026-11-03 — History-led modern RetroPilot adaptation in progress

Owner confirmed existing Radxa Q8B, not physical comma4. Parent history:
35commits/50final changed paths/64ever-touched paths;28commits dated2025,
7older upstream. All35commit diffs and pinned panda/cereal/opendbc comparisons
saved under sunnypilot/Ai/Reports/retropilot-c2-history-20261103/.
Angle STATE1 correction passes45port tests; previous STATE0 assumption was wrong
for reviewed Chimera/ZSS producers. Receive-only USB mailbox16/health43 adapter,
serial/version/product pins and modern CAN serialization implemented;15adapter
tests being finalized. No live output or settings/firmware changes.
REA GNU symbols/disassembly of retained Chimera ELF5ae9b4f6 confirms43-byte
health and16-byte mailbox stride; can_send's visible body queues without a
safety hook. No complete safety proof. Native decompiler not configured and
pwntools layout profile is Linuxx64-only; GNU fallback succeeded.
Read-only sysfs currently shows bbaa:ddcc product "Interceptor DAC Bench",
serial440048001251333133333633, bus3/device8. This is not the historical Chimera
serial3a0044001651333038373636. No USB handle opened or CAN consumed. VID/PID
alone must not identify a Chimera or resume the paused bench project.
Next: finish migration coverage map/tests, commit verified code and record
remaining raw health/manager/safety/profile qualification. CD210GPU unchanged.

## 2026-11-03 — C2 controller migrated to modern offline replay

Modern C2 steering/pedal/relay calculation and timestamped JSONL replay are
implemented in opendbc9da9210adfa4dc213424f36945caccd40182c80d. Explicit offline
calibration only; default absent. update() still returns zero actual output/no
CAN.44port/53CAN/303broader tests pass (314existing skips), Ruff/whitespace pass.
All8linked C2 blobs verified at b9a942e; canonical DBC, hostbus2 and CD210GPU
unchanged. Next: receive-only Chimera backend, producer/profile qualification,
then shadow/game-only loop and actual MCU safety. Hardware/game/vehicle control
remains untested. Full session: Sessions/2026-11-03-retropilot-controller.md.

## 2026-11-03 — C2 RetroPilot identification mapped to modern selection

Owner asked why fingerprint registration was absent and requested teacher C2
comparison. Re-read immutable C2 values.py and selection/car_helpers.py:
values has placeholderIDs0..15/DLC8; selection hard-codes "RETROPILOT RETROFIT",
skipsFW queries and overwrites the matcher result. It did not identify the
retrofit through measured ECU/CAN fingerprints. Earlier explanation omitted
this distinction and compatibility with the old name was missing.

Implemented car/retropilot/fingerprints.py with C2-name MIGRATION and an empty
FINGERPRINTS map. Shared car/fingerprints.py merges that map; car_helpers
normalizes the old name before the RetroPilot no-diagnostic guard. Explicit
argument and FINGERPRINT environment accept both old/new names. Existing
Sunnypilot CarPlatformBundle migration now converts saved C2 names; tested
against actual native Params in caller-owned temporary directories. Other-car
MOCK selection stays unchanged. No global override or automatic matching added.

Source: C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728; parentbasec6917544;
opendbc649bbb6→04a78352a9605a0e07342146fe8481b7d92ee7fd on radxa/retropilot.
27RetroPilot/5Params/53CAN tests and303broader car tests pass (314existing
subtest skips); Ruff and whitespace pass. Canonical DBC, noOutput/passive
controller, speed factor0, hostbus2, CD210GPU eb741641 and firmware unchanged.
No model/manager/game/hardware/CAN TX or persistent owner-settings action.
Next remains receive-only Chimera backend and producer/profile qualification;
automatic identity and active MCU safety remain unimplemented. No new question.

Current receipt: Ai/Evidence/retropilot-c2-selection-20261103.json; source hashes
and RED/GREEN/regression logs retained. Skills: source-driven-development,
interface design, TDD/incremental implementation, Git, documentation and
self-review. Source-first path; no REA artifact/runtime question. No upstream
merge; inbox had0related pending and8historical failed/blocked records retained.

## 2026-11-03 — Car-port checklist: identification and safety remain separate

Reconciled owner's pasted modern car-port checklist with actual source and
commaai/opendbc README (official current structure/safety sections). Added a
file/status matrix to docs/RETROPILOT.md. Existing modern package/state/codecs
and explicit selection are implemented; active controller mapping, automatic
identification, RetroPilot MCU policy and compiled safety tests are pending.
No invented fingerprints or radar/safety stubs added. Current noOutput request
is not proof of Chimera enforcement; CarController itself always emits nothing.
Teacher C2 safety header remains WIP (arbitrary RX enables controls, disabled
integrity checks, DLC mismatches and missing steering/brake limits). Host file
creation alone cannot wire that policy into Chimera's actual TX path.

Source pins unchanged: parentbase1a1cc4025c4233732bbbb86c061c4c54b35add5a,
opendbc649bbb632a020f155fc1eb16ae343f49a5c4bb50; canonical DBC/source/model
unchanged. Documentation/source review only; prior53CAN/22port/1600native CRC
results remain prior results, not new MCU safety tests. No code/device/network
PC/firmware/actuation change; no REA binary question. Next implementation stays
receive-only Chimera transport, producer units/profile, then qualified active
control and MCU policy. No new owner question needed for this clarification.
Skills: source-driven review, code-review-and-quality, interface design and
repository documentation/Git. Validation: notebook, real file-status/relative
link assertions and whitespace, captured in the checklist evidence receipt.

## 2026-11-03 — RetroPilot car port implemented, receive-only

Owner explicitly requested RetroPilot as the car and Chimera as Panda. Modern
RETROPILOT_RETROFIT now registers in opendbc; canonical DBC/CRC/counters,
state/module parsing, button/override/stale handling and all8offline command
IDs implemented. Explicit selection suppresses OEM VIN/FW probes. Hostbus2;
no global car override, forced CAN validity or fake wheels/gear/torque.
Default speed scale0 marks sensors invalid; legacy km/h vs local Hall centi-km/h
must be qualified explicitly. CarController is unconditionally passive;
dashcamOnly/noOutput and placeholder geometry/tune do not establish control.

Submodule branch radxa/retropilot: codec eb64a22, platform649bbb6
(full649bbb632a020f155fc1eb16ae343f49a5c4bb50), baseaa9bff6f; parentbase dd29f00.
53CAN+22port tests pass;303broader car tests pass (314existing subtest skips),
490lateral-limit tests pass (31existing skips), Ruff/whitespace pass.
Compiled original CRC matches1600vectors across20canonical messages.
No devices/game/model/manager/firmware/CAN TX or actuation tested or enabled.
Next: receive-only Chimera backend + actual producer units/frames/hostbus2,
then full BeamNG telemetry/motion contract and optical shadow. Actual actuator
profile, live safety and endpoint calibration remain open. No owner question
needed to complete this code stage. Detailed topic/session/receipts below.

## 2026-11-03 — RetroPilot car port in progress: canonical codec

Owner explicitly requested modern RetroPilot as the car and Chimera as Panda.
Read teacher RetroPilot/Chimera notes and canonical policy before coding.
Started opendbc branch radxa/retropilot from aa9bff6f; registered the submodule
in maintenance config (controller cdc20d4) and installed commit journaling.
Canonical DBC copied byte-identically (SHAef6eef74), SAE-J1850 CRC and automatic
counter validation added. RED missing-DBC tests reproduced; GREEN52CAN-library
tests, Ruff and whitespace pass. No hardware, transmit or firmware action.
Legacy speed consumer uses km/h, saved local Chimera Hall source multiplies by100;
MODE/config producer differences remain unqualified. Keep explicit scale/validity.
Next: modern platform/CarState and receive-only controller plus offline commands.

## 2026-11-03 — Connected PC requirements checkpoint

Owner reports connected BeamNG PC. Existing sim/beamng README now maps six
Sunny needs; actual gateway/Chimera/car/motion/command adapters remain pending.
Q8B eth1 UP10.43.0.1; neighbor10.43.0.216 reachable. Strict SSH exited255:
no trusted ED25519 host key; no remote inspection. Game/car/mods unverified.
Keep optical+CAN architecture/CD210GPU, canonical DBC and existing source pins.
Next: resolve trusted PC identity for read-only inspection and continue wire
contract increment1, then receive-only/shadow. No CAN TX or actuation.
Details/tests: Sessions/2026-11-03-beamng-requirements.md in both notebooks.


## 2026-11-03 — Radxa-focused docs assessment

Owner wants a simpler Radxa project. Inspected docs27files/366532logical bytes
before edit (~440KiBallocated). Useful porting/policy/logging/safety references
remain; comma connection/public-site pages are optional references, not Q8B
setup. Updated docs/README.md with a short Radxa entry index. Existing op docs,
site CI and car-doc generator/maintenance consume this tree. No deletion or
runtime change. Hardware selector still imports HardwareComma unconditionally;
HardwareRadxa inherits HardwarePc, so names alone do not justify pruning.
Detailed scope/limits: Knowledge/REPOSITORY_CLEANUP.md in the student notebook.
Next cleanup needs dependency-checked scope; current BeamNG wire-contract task
remains pending. Documentation-only checks; no REA binary/runtime claim.

## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Owner selected PC monitor → physical Radxa AK-Camera, and PC game gateway ↔ Waveshare CAN ↔ Chimera USB ↔ Sunnypilot. This supersedes the earlier network-camera next step. Added active openpilot/tools/sim/beamng/ PC/Radxa roles, shared CAN mapping/gaps and ordered plan; rewrote the current guide and reference README. No runtime code, DBC, firmware or remote PC files changed; no hardware/game/model launch or CAN transmission.

Recovered teacher facts: CH340 USB-CAN-A, 2Mbaud8N1 AA/55 variable framing; candidate500k CAN; historical Chimera hostbus2→MCUCAN3/connectorCAN2, 16-byte mailboxes/43-byte health and observed de193215 debug version. These do not prove current wiring/image or modern Panda compatibility. Canonical DBC6b90fafe/SHAef6eef74 lacks complete wheels/IMU/session/gear and cruise-status definitions; keep gaps central, no invented IDs.

Final CAN controller outputs must drive an explicit game actuator mapping; curvature-to-position bypass does not validate torque control. Physical bench steering/Interceptor/Core, brake and accelerator remain later. Resolve feedback authority and calibrated endpoint mapping before motion; do not resume the paused standalone VW experiment. Simulated IMU must not compete with stationary physical LSM6DS3TR-C. CD210GPU remains selected.

Next: wire-contract increment1 (speed semantics, versioned canonical extensions, golden vectors, deadlines/bus budget and game command family), then receive-only Chimera, optical shadow, game-only loop, later bench. Source-first Agent Skills: specification/planning, documentation, Git and review. No REA binary question in this documentation increment. Validation receipt: Ai/Evidence/beamng-hil-layout-20261103.json in Sunny; checks cover documentation/reference integrity, not HIL runtime.

## 2026-11-02 — BeamNG bundle audit complete; runtime adaptation still blocked

Audited collected source at projectbase f72a1ea/upstream5435d674. Added14missing
integration/import references; bundle now96files/1160682bytes, byte-identical
upstream. Allfile Git/SHA/mode/size checks;69Python AST/8bash/2JSON checks pass.
Fixed verifier accepting empty snapshots/wrong origin/pin/checksum list;12new
regressions pass, checksum-guard mutation caught. Snapshot tests with process-
local routing/current Sunny dependencies:164pass/6fail/1skip;2modules blocked
on import,1UI module not run. Five failures and two import blocks stem from
missing opendbc scale_tire_stiffness; onefailure assumes installed xdotool.
Test-only evdev2/mss10.2 installed under /tmp with locked SDist hashes; active
environment unchanged. UI/Lua/JS/Vue/game/model/manager tests not performed.

Source probes reproduce NaN accepted in96byte BPL1 and control-send called after
no new telemetry. Fork steering uses desiredCurvature→position, bypassing final
lateral torque; cannot directly validate custom actuator/NNLC. Same-hostIP,
camera1280vs1928, timing/freshness/session/finite and peripheral4vs2Hz require
adaptation. No copied upstream fixes applied to active runtime/DBC. Verdict:
reference bundle verified, direct runtime integration blocked. Next sim-only
recorded PC frame→VisionIPC/UI, then state/shadow and explicit lateral contract.
Detailed report: openpilot/tools/sim/beamng_reference/AUDIT.md; per-file/test
receipts alongside it. Relevant skills: source-first/code review, TDD/debugging,
git/docs. REA binary analysis not relevant to readable source/packet probes.

## 2026-11-02 — BeamNG source bundle collected

Owner requested all needed BeamNG files from Caleb's tools in a folder. Created
openpilot/tools/sim/beamng_reference/:82byte-identical upstream files,1025072bytes,
from commit5435d67499f66eca58f95882cbe35e9c577e874c. Both complete game mods,
setup/TUI/monitor/diagnostic, car installer/platform, camera/telemetry daemons,
common modules, sim helpers, relevant integration source/tests and root launch/
config/build/dependency metadata retained under upstream/ with original paths.
MIT license, original submodule pins, MANIFEST/SHA256SUMS and dependency guide
included. verify_bundle.py checks file coverage/bytes/SHA256/Git blobs/modes.
56Python AST/8shell syntax/2JSON source checks pass; original behavioral and
Lua/JS/Vue/game tests not run. Foreign snapshot tests excluded from automatic
parent pytest discovery only; existing project tests are unchanged. No installer,
mod, manager, model or game executed; no dependency/environment/DBC changes.
Next remains sim-only recorded PC frames→VisionIPC/UI; bundle is reference,
not a runnable standalone checkout or qualified PC↔Q8B backend.

## 2026-11-02 — Current owner focus: BeamNG bridge discovery

Owner moved from NPU research to running this Sunnypilot with PC BeamNG.drive.
Identified Caleb-J773/beampilot-drive at5435d674 (same as teacherOct28 pin).
Its same-host camera/telemetry/Lua path needs a PC↔Q8B adapter; current local
openpilot/tools/sim implements MetaDrive only. README successor steerpilot
publicURL/API return404. Saved source hashes, concrete API/image-size/freshness
gaps and staged camera→state→shadow→game-lateral plan in
[BeamNG notes](Knowledge/BEAMNG_BRIDGE.md). Research/docs only; no game, mod,
network listener, managed stack or model launched. CD210GPU stays selected;
failed W8A8 NPU baseline retained, precision experiment deferred. Next: prove a
recorded PC frame through sim-only VisionIPC/UI before a live game connection.

Checkpoint: conversion/replay safeguards committed as
`43678a671237bae095c1eb6fea95d78ff69d4261`,29focused tests and software checks
pass in maintenance ledger. All local research DLC/context/runtime assets are
inside ignored `modeld/npu/artifacts`; small receipts/results are tracked by the
following results checkpoint. Large ignored files do not travel through Git.
Actual final project HEAD is available from Git; no unfinished hardware worker.

## 2026-11-02 — Fresh INT8 device baseline complete; accuracy rejected

Owner approved research continuation while retaining the failed strict FP16
check. Fresh Mountain Dew v3 W8A8 runs on actual Q8B SDK2.37/v68/SoC37:
200heldout calls exit0 plus3native-byte cases (all42heads bitwise equal).
Calibrated DLC400356844bytes; integer-IO DLC400346268bytes; context444203008bytes.
200MB goal unmet. After132warmup,68teacher-forced frames have normalized RMS
errors29.65% packed,46.16% lane_lines,16.78% plan,43.31% action and189.26%
hidden_state. These are raw tensor errors, not driving-accuracy loss. Candidate
remains unselected; current CD210/OpenCL preview ce7b047/eb741641 unchanged.

29focused tests/Ruff/two shell syntax checks and normal-venv CLI help pass.
Model numerical acceptance FAIL; strict calibration1value and heldout96prewarm
FP16 checks remain visible. Independent original FP32 agrees bitwise on ten
calibration cases and both failed heldout cases. All500 source-state transitions
were independently replayed. CPU backend crosscheck is unsupported at quantized
FullyConnected; PTQ/backend error contributions remain unresolved. No candidate
self-feedback or parsed driving metric after this failure. DSPs running, scoped
clock lease closed/restored, no owned workers. Entire15.6387s run is not a model
latency benchmark. Next: W8A16/mixed activation/output precision experiment with
8-bit weights, then matched heldout comparison and broader calibration; no
modeld selection or vehicle actuation. Actual commits/validation in Git/ledger.

[Results](../openpilot/selfdrive/modeld/npu/RESULTS.md). Earlier entries below are dated checkpoints, superseded where stated.

---

## 2026-11-02 —500-frame W8A8 artifact complete; integer-I/O context work active

Fresh calibrated DLC is400356844bytes/SHA6cca7b518b6aa7d557727833d589de8a93dfe253a13a0a14f55fa81a3d7e3343,
inside Sunny npu/artifacts/w8a8-research.dlc and x86 dlc-v1. Quantizer exit0,
15m53s, all500frames. Wrapper later exited127 because its mutable shell source
was replaced during the long command; compiler artifact/exit0 preserved, no
recalibration needed. Future host stages use immutable hash-named snapshots.
Full independent500-frame zero/own-state audit passes, all3000native hashes;
strict FP16 comparison remains FAIL1value. Active audited report SHA77a3a166;
research receipt is npu/w8a8-research.json. Heldout200 localstaged/verified;
strict96prewarm precision failures retained, originalFP32exact on22/66.

SoC37/v68 context compile explicitly recognizes SC8280X but FAILS before device
loading: unsupported FP16 in FLOAT32→UFIXED8 desire I/O Convert. No context
binary and no NPU/clock/helper execution. Investigating removing floating I/O
boundary adapters using calibrated integer tensors, preserving all weights/
scales; do not switch to SoC39 or repeat500calibration blindly. SDK primary
Python source dlc_quantizer.py documents preserve_io_datatype via
ir_graph.modify_io_datatype; applying it again collides with existing converted
tensor names, so that in-memory probe was rejected without saving. Next inspect
IR squash/encoding API and validate any integer-I/O derivative before compiling.
PC workdir /home/pc/sunnypilot-npu-20261102; immutable host snapshotab8ea960;
context-v68-soc37-v1/log retained. No running conversion workers now.

Commits7157164 gatesresearch/18tests;6b16d69 heldout+bounded replay/25tests has
historical staged-EOF whitespace failure, corrected and validated by d2bb1b3a.
New uncommitted small audit/quant receipts and README changes expected. Current
CD210/preview defaults unchanged.200MB target unmet (~400.36MB measured DLC);
NPU numerical error/latency and closed-loop candidate recurrence unmeasured.

2026-11-02 held-out/tooling increment in progress:200independently-reset
FP16 frames500-699 complete; all1200native+200golden file hashes and relocated
local list verified inside Sunny. FP32-vs-FP16 diagnostic fails94hidden values
at22 and2at66; all sampled warm cases pass. These failures remain visible;
independent original FP32 matches rewritten FP32 bitwise on both failed cases.
25tests/Ruff/bash pass; runtime/evaluator CLI help works in normal Sunny .venv
without conversion-only ONNX/ORT imports. New metadata/run linkage guards,
bounded private QNN runner and SIGTERM cleanup are reviewed. No NPU context
loaded yet; full500calibration/audit still running. Model defaults unchanged.

Research tooling71571642 committed and validation journaled:18tests/Ruff/bash/notebook pass. PTQ and independent500-state audit plus heldout200 generation remain active on x86 PC; no NPU model loaded.

## 2026-11-02 — Owner-approved INT8 research continuation

Owner explicitly chose “Continue INT8 research; retain failed FP16 check”.
The corrected 500-frame dataset is complete. Strict FP16/FP32 diagnostic still
FAILS at frame443: hidden element2218, .0017442703 versus -.0098324120;
hidden relative RMS .084442%, packed relative RMS .022077%. These are tensor
errors, not driving-accuracy percentages. Ten spread-out comparisons against
an independent original-graph FP32 reference are bitwise equal; precision
promotion is isolated from the host-FIFO/head rewrites on those ten cases.

Added explicit quantize-research mode; default strict gate remains unchanged.
Research requires pinned independent graph, exact bitwise diagnostics and full
native-file provenance; no deployment/vehicle acceptance. QAIRT2.37 rejects
SC8280XP and SC8280X target strings; generic HTP is supported and is being used
for PTQ only, without substituting historical SoC39. First rejected target log
is preserved. Full500-frame zero-state/own-FP16 recurrence is now independently
replayed before accepting calibration provenance. Review caught report-path
shadowing; owned audit was stopped before completion and corrected, inputs
preserved. Local17focused tests/Ruff/bash pass. No INT8/context/device result
yet. PC workdir remains /home/pc/sunnypilot-npu-20261102. No camera/GPU runtime,
clocks, firmware or vehicle changes. Next finish recurrent audit and generic
HTP PTQ, record actual size/encodings, then resolve target37 context support.

2026-11-02 NPU checkpoint d450dbbd committed/validated (12tests). Corrected
calibration500-v2 completed all500native frames but strict prequant FP16/FP32
diagnostic FAILED atframe443:1hidden_state value(reference .00174427 vsFP32
-.00983241), hiddenRMSrelative.0008444, packedRMSrelative.00022077. Gate blocks
PTQ; no INT8/context/NPU loaded. Investigating same-precision full7input/4output
FP32 reference to isolate promotion rounding from graph-rewrite errors; original
failure remains preserved. source/graph/DLC pins unchanged. New uncommitted
qairt_host help/SC8280 target, diagnose_case/semantic_reference scripts and
receipts are expected current work. PC workspace /home/pc/sunnypilot-npu-20261102.
Known HTP/stub/skel now match SDK2.37aarch64-ubuntu-gcc9.4 exactly; oldSystem
stilldifferent, matchingSDKSystemavailable. REA open_binary validated HTP ELF
identity/e33be7a2/arm64 only, no decompilation/execution claim. Initial700-v1/
native500-v1 stay rejected; correctedroad700-v2 complete and format2 now required.
Next inspect semantic-reference/diagnostic443-FP32, preserve failed gate; do not
silently relax it or claim INT8 accuracy. Last code/data checks passed12tests.

# Resume Sunnypilot here

## 2026-11-02 — Fresh Mountain Dew v3 NPU experiment in progress

Owner selected fresh big-model INT8/PTQ work inside modeld/npu and requested
Jetlink updates. Read teacher Jetlink/NPU history. Source ONNX35976b11 downloaded
768750198bytes via configured1e219d model ref; original pickle d4c7a3fc unchanged.
Inventory382904774FP16values implies ~383MB INT8payload before overhead;200MB
not promised. Fresh FP16 CPU reference da9506a6 and FP32 source eceadb80 generated
on trusted x86PC, new floatDLC conversion exits0. 10initial FP32/FP16 comparisons
had no values outside .01+1%; not INT8/driving accuracy. Full PTQ pending.
Reviews (agent + owner-selected Codex CLI) caught ordinal/video alignment bug:
old extractedroad700 and incomplete calibration500-v1 rejected, worker stopped.
Corrected road700-v2 complete:700unique/cadenced encoder-mapped inputs; fresh
calibration500-v2 running on the x86 host.
Source/DLC/data hashes, continuity and spread-out warm diagnostics now gated.
12focused tests/Ruff pass; no experimental NPU context/device/clocks/firmware
operation. Current CD210/OpenCL preview ce7b047 unchanged. Conversion tool venv
installed locally; scope/provenance/commands in modeld/npu/README and session.
Jetlink refs now Zoompilotaf9df78/v0.8.13,mouxangithub7425e98,FOREVERb8cbb92;
3clean manifests verified, previousrefs preserved. Old bundleverifier separately
fails pre-existing q8b source drift; not a new clone mismatch. Runtime target
soc37 vs historical39/library-stack identity remains open before NPU execution.
Next: finish corrected road700-v2, validate mapping/cadence, copy toPC, run
fresh pinned500-frame recurrent state builder, verify receipt, then W8A8 PTQ.


## 2026-11-02 — Hardware needs mapped to current Q8B support

Owner asked to update the complete requirements list with what Radxa supplies.
Updated NONCAMERA_HARDWARE with available interfaces, historical tests, actual
preview integration and remaining managed/vehicle work; corrected RADXA_PORT's
stale camera/model/UI-future statement. Read-only source/documentation task,
base d88a72c; runtime remains ce7b047, CD210 eb741641 unchanged. CPU/GPU/PWM and
timing already reach preview; other thermals/power, IMU/GNSS and platform/vehicle
providers remain distinct pending work. No driver, fan, model or runtime change.
Validation/limits and exact next step are in the linked session. Next candidate:
read-only managed thermal mapping; do not start a broader hardware port implicitly.

[Session](Sessions/2026-11-02-q8b-hardware-support.md).

## 2026-11-02 — Q8B live onroad statistics complete

Owner-requested panel is on the actual Sunny AugmentedRoadView, enabled by
Q8B road-only mode; Q8B_SHOW_STATS=0 hides it. Shows hottest readable CPU/GPU,
fan PWM percent/raw/mode (RPM unavailable), GPU inference/readback, full model,
modelHz, camera→model and camera→UI first draw. Read-only sensors1Hz on a worker;
2s timing medians, display4Hz, stale timing1s/sensors3s, unavailable as dashes.
76tests/Ruff pass. Complete65sUI:1293camera frames/1274model messages/33path
points,20.0048Hz; inference10.933/12.133ms and capture→model36.832/41.043ms
median/p95. Overlay samples match model benchmark exactly; UI endpoint precedes
benchmark draw-ready by0.781ms median. UI benchmark draw-ready45.390/58.292ms;
host EndDrawing74.590/88.904ms. Physical display latency remains unmeasured.
Full65s child exits0/0/0; outer command143 after completion remains unexplained.
Independent cleanup passes; final10s command/children exit0,179matching packets,
zero rejections. Camera/clocks restored, GPUfaults0, fan mode staysautomatic.
Model/native/root helper hashes unchanged; no new conversion/calibration/control
or vehicle/hardwared integration. Data helpers committed5e01a48; this UI increment
and exact validation are saved in Git/ledger and the portable UI receipt.
Next: normal preview --model shows the panel; owner selects later work.
[Details](Knowledge/UI_TELEMETRY.md), [receipt](Evidence/q8b-ui-telemetry-20261102.json).


## 2026-11-02 — All project work committed

Owner requested a complete commit checkpoint. Git audit found a clean
radxa/q8b tree at49d2f07432541d9456acb60369a8f959db4c5611. All57tracked local
commits had validation records; latest GPU increment has a passing receipt.
This documentation checkpoint records that audit. Runtime/source/model are
unchanged; previous68tests and hardware benchmarks were not rerun. Next task
remains owner-selected calibration/hardware or optimisation, with controls off.


## 2026-11-02 — Resident GPU baseline complete

Q8B Thneed defaults to resident exact NV12 crop/packing/lag4 history, fresh60FPS
source selection at20Hz, and worker affinity on fast cores4–7. Scoped max clocks
are automatic; owner already installed the helper, no routine password request.
Existing CD210eb741641 remains unchanged; no conversion or feature splitting.
Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.
Calibration remains provisional/invalid, controls and DM off. No new20min soak,
full-manager/vehicle test or physical-display-latency claim. Unrestricted38.204ms
repeat and CPU7 regression40.512ms retained; adopted fast profile has two passes.
Next: launch normal preview from project .venv; choose later calibration/hardware
or optimisation separately. No active experiment or unfinished source edits.
This verified increment is recorded by its Git commit and maintenance receipt;
base623f728a, exact source/model/runtime hashes in the portable evidence.
[Details](Knowledge/MAX_PERFORMANCE.md), [receipt](Evidence/q8b-resident-20261102.json).

## 2026-11-02 — Full locked dependencies installed; minimal build passes

New [install guide](../install.md) covers setup/build/tests/preview for newcomers.
Python3.12.13/uv0.13.6;85packages/all extras+standalone, no external bench paths.
q8b OpenCV/Pillow extra; existing lock versions unchanged. Tinygrad examples
local .pth documented. Default .venv replaced after staging51tests; old env and
5native libraries retained as ignored backups. Root minimal Q8B/Thneed build
now passes; previous missing-acados block is resolved. MPC solver constructs.
Final51tests,12GPU/12adapter checks and10sactual camera/model/UI pass:
193frames/183models/33pathpoints, allchildrenexit0, camera restored,faults0→0.
No new conversion/driver/system/clock changes. Provisional geometry/controls off;
full manager/vehicle/sustained performance unqualified. Next use install.md;
hardware/geometry work remains separate. [Details](Knowledge/INSTALLATION.md).

2026-11-02 acados diagnosis: limited preview .venv never received the full
locked dependencies. acados/SCons plus several other native-package imports
are absent; lockfile includes ARM64 comma-deps-acados0.2.2.post103. No install
or runtime change. Full dependency qualification remains separate work.
Details: Ai/Sessions/2026-11-02-thneed-modeld.md (student).

## 2026-11-02 — Launch directory and timing clarified

Enter `~/comma/sunnypilot` before `.venv/bin/python -m openpilot.system.camerad.webcam.preview --model`;
the parent `~/comma` has no project virtual environment. Help/import checked
from the correct directory; no new camera/model run. Current36.656/46.326ms
model-call timer includes CPU warp/history/uploads/GPU/readback/parser, excludes
camera capture/JPEG decode/NV12 and UI drawing. Current GPU-only split remains
unmeasured; historical11.724ms cannot be subtracted to infer camera cost.
Runtime/model unchanged at07bc78e; docs-only follow-up, provisional geometry and
controls-off scope retained. Next: owner retries launch; per-stage timing needs
a separate measurement if requested. See modeld session follow-up.

## 2026-11-02 — Thneed modeld/camera/UI integration verified

ExistingCD210 artifacteb741641 unchanged, no reconversion. Q8B_THNEED=1 selects
new ModelState-compatible GPU replay/current history/parser in stock modeld;
requires real Q8B/road-only webcam. Uses pinnedCPU:LLVM NV12 warp, two views,
zeroed warmup/reset and copied output-slice metadata. Alternate model warmup and
Tinygrad NN compilation bypassed only in this mode. Defaults unchanged.
Launch from project: `.venv/bin/python -m openpilot.system.camerad.webcam.preview --model`.
Private camera/modeld--demo/actualUI session; no vehicle/control/DM processes.
Temporary MM-X/zero-mount assumption stays uncalibrated; model validity false.
51tests/lint pass;5exact warp checks,32synthetic recurrent CPU checks and6actual
live CPU-reference samples pass all2576values at rtol.001/atol.005.
Clean65s run:1201steady model receipts/19.998Hz; full model call36.656/46.326ms
p50/p95; source→model receipt at UI94.754/115.031ms. Includes prep/queues/GPU/parser,
not inference-only.23calls>50ms,max54.214,one receipt ID gap retained.33point overlay
visually verified. Diagnostic run with6snapshot writes19.632Hz/max267.672ms;
kept separately. All children exit0; camera/policies restored,GPU faults0→0.
Targeted native SConscript passes; whole build stops at missingacados, other
build dependencies unchecked. Camera optimisation/vehicle/soak qualification
remain open; no automatic hardware-plan resume. [Session](Sessions/2026-11-02-thneed-modeld.md).

## 2026-11-02 — Existing CD210 Thneed imported and replay verified

Owner says reuse converted model; do not reconvert. Copied accepted99641029byte
Thneedeb741641 unchanged to openpilot/selfdrive/modeld/models/q8b_cd210.thneed,
plus metadata/fixtures. All replay source/vendor/licenses/build scripts now inside
Sunny at openpilot/selfdrive/modeld/thneed_q8b. New NumPy/ctypes runner has no
external-experiment/Tinygrad runtime import and checks hashes/matching GPU driver.
Current history-queue adapter preserves old compiled model; no model conversion.
Native ARM64 library built;12saved exactCL/CPU tolerance checks and12queue cases
pass.42focused tests/lint pass.40same-input host calls12.114msmedian/15.851msp95
includes upload/validation; repeat14.223/16.545ms also passes. Dynamic policies
unchanged, no camera/maxclock/20min rerun.
Current manager/modeld selection unchanged. Next connect checked backend to
live modeld/publication/overlays, qualify current recurrence and20Hz timing.
Camera optimisation remains deferred. [Session](Sessions/2026-11-02-thneed-import.md).

## 2026-11-02 — Confirmed: Thneed ran CD210 learned core

Fresh ONNX checkpoint/tensor-content comparison confirms old659727c4 and
current65a08adc share learned weights; changed history wrapper explains file
differences. Corrects earlier different-weights claim. Thneed artifacteb741641
traces to oldCD210; current-wrapper runtime still needs integration qualification.
[Confirmation](Sessions/2026-11-02-thneed-cd210-confirmation.md).

## 2026-11-02 — Teacher Thneed pipeline recovered

Prior portable OpenCL Thneed small-model pipeline is already implemented and
bench-tested:20min/24101steady frames at20Hz, model11.724msmedian/12.348msp95,
camera→output35.417/39.721ms under maxCPU/GPU690/EGL/partial-JPEG profile.
Fresh existing driving-02 artifact hash matcheseb741641. Old659727c4 and currentCD21065a08adc have
the same learned weights; the ONNX history wrapper differs. Reuse exporter/replay design after
current-contract/parity qualification; no new runtime port/run in this task.
[Reusable methods, files, pins and limits](Knowledge/THNEED_GPU_REFERENCE.md).
[Session](Sessions/2026-11-02-teacher-thneed.md). Camera optimisation stays deferred.

## 2026-11-02 — Big model NPU feasibility reviewed

Bundled big Tinygrad artifact targets Chestnut/AMD, not direct QNN loading.
Fresh static opcode/hash inspection:799941965bytes,SHA256d4c7a3fc, no unpickling.
Teacher already has separate historical big-model W8A16 QNN2.37/v68 conversion:
Oct31 short replay38.196ms graph/41.515ms host medians, excluding camera;
bitwise quantized-baseline parity does not resolve floating-reference accuracy.
Identity of that6fee5937 ONNX versus bundled Mountain Dew v3 is unestablished.
First NPU research step is graph/weights/state identity comparison; do not
recompile/retest or promote historical timings as current Sunny performance.
CD210/Adreno remains recommended next integration; no backend changes started.
Camera optimisation remains deferred. See [NPU review](Sessions/2026-11-02-big-model-npu.md).

## 2026-11-02 — Model identity recovered: CD210 default

Bundled driving_supercombo.onnx is labelled CD210 with ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391.
Actual file SHA25665a08adc/name/ref fingerprint matches tracked model_hash and
pinned official upstream name file. ONNX metadata/input/output schema inspected
without executing pickle metadata. Separate big_driving_tinygrad.pkl is labelled
Mountain Dew Model v3 for Chestnut; do not confuse the two. Parser supplies
path/motion/lane/edge/lead/pose predictions; current source targets20Hz.
Identity verification does not prove current GPU inference or driving behavior.
Next recommendation remains CD210/Q8B Adreno qualification. No runtime change.
See model-identity session and student UPSTREAM_AND_VERSIONS for exact evidence.

## 2026-11-02 — Recommended next step: current model on Q8B Adreno

Owner asks what comes next after accepted camera milestone. Recommendation,
not started: qualify current Sunnypilot stock driving model on Q8B Adreno,
using teacher's earlier MSM/Thneed work as reference while retaining Linux/Q8B
identity. Current helpers.load_oob selects CPU:LLVM on non-AGNOS Linux; simply
opening camera UI does not activate GPU model inference. Do not fake AGNOS.

First increment: map current model inputs/history/state/output parser and run
one isolated correct GPU inference against a CPU reference. Then qualify
bounded camera→model publication at target20Hz, and finally show model path/
road predictions in actual Sunny UI. Validate numerical agreement, real timing,
message freshness and clean restart/stop. Earlier20Hz standalone evidence is
for different model/runtime; it is not proof current weights will meet20Hz.
Source base679bf8d; current stock model65a08adc,tinygrad92b742f7,msgqe7396e76.
Model input uint8[2,6,128,256] and padded camera boundary were previously checked;
full inference, state/history/runtime integration remain open. Teacher first:
Ai/Knowledge/Repos/sunnypilot.md, camera.md and Oct31 soak source db5b0da.

Keep camera optimisation/calibration deferred. Hardware plan tasks/plan.md is
preserved, not automatically resumed or replaced. Known physical IMU/vehicle
feedback/hardware providers remain later integration work. No new runtime,
model conversion/launch, GPU driver or vehicle action by this recommendation.

## 2026-11-02 — Camera bring-up accepted for now; optimisation deferred

Owner says camera work is done for now and will return to teacher knowledge
later to reduce delay. Preserve current capture/UI and temporary MM-X geometry.
Benchmark baseline7ac07b5:1200steady frames/19.97562FPS; driver→draw-ready
59.398msmedian/78.755msp95; driver→EndDrawing return89.385/109.139ms including
normal pacing. No further camera optimisation/calibration changes now.
Future work starts from teacher camera/Sunnypilot notes and the Oct31 retained
pipeline report/source db5b0da, with its different model/runtime/max-clock
conditions kept explicit. Compare matching endpoints/profiles before porting.
Current optics/mount and full model/vehicle qualification remain open; owner
acceptance covers camera bring-up/preview/benchmark milestone only. No next
engineering task selected in this message. No runtime changes or new tests.

## 2026-11-02 — Actual camera-to-UI timing benchmark completed

Added opt-in native preview benchmark,37focused tests/lint pass.65.057srun,
5swarmup,1200steady first-display samples at19.97562FPS. Driver timestamp to
draw-ready59.398msmedian/78.755msp95; to EndDrawing return89.385/109.139ms,
including normal30FPS pacing. Actual GLfreedreno FD690/Mesa25.2.8; default
CPU schedutil/GPU simple_ondemand, no clock/fan overrides. Not optical latency
or confirmed compositor presentation. Raw samples independently recomputed.
Camera/UI exit0/0, previous1080p30/dynamic-rate1 restored; no active preview.
No model/vehicle run or calibration change. See camera-ui-benchmark session
and webcam README command. Model/Adreno integration still pending; automatic
calibration deferred. No optimisation undertaken beyond measuring this baseline.

2026-11-02 timing answer: latest preview19.87new camera frames/s (~50.33ms
interval), not measured camera-to-screen latency. Older standalone42.186ms
median/56.996msp95 is separate. No runtime change or camera relaunch.

2026-11-02 intrinsics assessment: temporary900px/720p implies70.834deg
horizontal FOV under a pinhole assumption; old70deg was only visual. Camera/UI
video is verified, lens geometry is not. Keep owner-selected temporary profile;
no automatic calibration resumed. Persistent preview12790/12793/12794 has now
closed normally:1514distinct frames/76.200s, child exits0/0; no relaunch requested.

Live preview reopened in persistent terminal session21631: controller12790,
camera12793,UI12794; prefixq8b_preview_97ce0a9e4384. Actual screenshot
owner-persistent.png verified and child PIDs alive. Logs:workspace
Ai/Reports/sunnypilot-ui-preview-20261102/owner-persistent. This supersedes the
previous closed-session state. Window intentionally open; close it to stop
camera/restore settings. Check current PIDs before later camera work.

## Owner preview closed normally — 2026-11-02

UI implementation536470bd4fe9ab9abb68f9af9320ee8b315aecd2 is committed.
Owner-facing session controller12416/camera12417/UI12418 displayed849distinct
camera frames over42.917s, then exited normally0/0; closure cause unconfirmed.
No preview process remains. Prior1080p30MJPG/dynamic-framerate1 restored exactly.
Reopen from Sunnypilot root with
`.venv/bin/python -m openpilot.system.camerad.webcam.preview`.
No model/vehicle processes started; automatic calibration remains deferred.

## 2026-11-02 — Live Sunnypilot camera dashboard verified

Owner requested opening the UI to view road-camera output. Added webcam/preview.py
camera-only launcher using the actual Sunnypilot onroad widget/HUD. Private
message prefix/temporary Params; UI-only demo started/ignition data. Starts
camera+UI only, no model/planners/vehicle/controls/recording.32focused tests/lint
pass; live9.06s check rendered173distinct frames, actual screenshot viewed.
Final4s lifecycle check passes; child exit0/0 and prior1080p30/dynamic-rate1
restored. Stock model and temporary MM-X intrinsics unchanged. UI speed is a
demo default, not car telemetry; no AI prediction/vehicle integration claim.
Next: use camera preview; model/Adreno qualification still pending. Automatic
calibration remains deferred. See ui-camera-preview session and webcam README.

Saved implementation commit: `d0d654a66c04f57a39cb3dddb8516c6309e992e6`
(`feat: use temporary MM-X geometry in Q8B road-only mode`). Owner requested
commit update2026-11-02; verified project clean and this commit's validation
journal attached, with no missing local validation or pending upstream review.
Its30tests/lint results are retained evidence, not a new runtime run. This
checkpoint update changes documentation only; next work remains model/Adreno
qualification with provisional geometry and calibration work deferred.

## 2026-11-02 — Temporary MM-X geometry selected and implemented

Owner: keep MM-X method for now, change later. get_device_camera_config now
returns borrowed720p/fx=fy900/centre640,360 for radxaQ8b/unknown only when the
existing Q8B_ROAD_ONLY+USE_WEBCAM mode validates the actual board. Cabin/wide
remain absent. Model/v2/UI share this lookup. Outside that opt-in mode, Q8B
calibration remains unconfigured; comma/PC profiles unchanged. Profile is not
measured AK calibration and supplies no distortion or mounting pose. Auto
calibration/target capture deferred; tools retained. Capture60/latest20Hz and
calibration-status/DM/vehicle policies unchanged. No camera/vehicle run.
30focused tests and lint pass; see temporary-mmx-profile session. Next qualify
current model/Adreno integration using this explicitly provisional geometry;
replace intrinsics later, do not auto-resume target/autocalibration work.

## 2026-11-02 — Automatic calibration requested: options explained

Owner asks how to automate intrinsics and extrinsics. Proposed auto-selection/
lens solve plus mounted camera/known vehicle-aligned target pose for R/t; target
motion/placement remains physical input. Current capture still requires Space;
no autosave or vehicle-pose export implemented. Online calibration assumes zero
roll and does not solve K/distortion/full6DOF. COLMAP target-free estimates are
an untested alternative, needing validation and vehicle-frame alignment.
No runtime/settings changed; next resolve preferred measurement workflow before
implementation. See automatic-calibration-options session for sources/limits.

## 2026-11-02 — MM-X RK lens-parameter check

Owner questioned the checkerboard step. RK3ad69b20 README requests external
intrinsics (example:GMLCCalibration); geometry/UI store720p focal900,centre640/360.
Online calibration estimates mounting alignment, assumes zero roll, and does
not solve lens K/distortion. His actual measurement procedure is undocumented.
Checkerboard is an available method, not a Sunnypilot requirement. Next resolve
an appropriate AK lens-parameter source; printing/capture is optional pending
method choice. No runtime edits or geometry activation; guard stays active.
Fresh5Git blobs/4Python AST checks pass; see dated mmx-camera-calibration session.
Prior29runtime/tool tests remain historical, not rerun for this source review.

## Current checkpoint — layout fixed; printable calibration tool ready, 2026-11-02

Owner said proceed and selected printable target/tool. Layout fix6fea7ecf
aligns actual Q8B NV12 with current modeld: stride1280,Yrows736,UVrows368,
UVoffset942080,allocation2220032,modelcopy1413120.140real frame pairs still
pass~20Hzpublish/~59.63Hzsource with settings restored. CPU-only pinned warp
matches two synthetic independent NumPy views; current ONNX expects
uint8[2,6,128,256] and carries its own image/desire/feature queues. Not model
inference or Adreno qualification. Q8B720pwarp build config added; runtime kept.

Printable A4 PDF/SVG and calibrate.py target/capture/solve tool now live under
openpilot/system/camerad/webcam. See CALIBRATION.md for exact workflow. GUI
uses Tk/Pillow; tested with synthetic frames only.6calibration tests plus prior
23camera/identity tests pass; PDF verified A4 and rasterized grid detected.
Real lens data remain uncollected: owner must print at100%,check25mm squares/
100mmruler and mount flat before collecting24varied views. Current continuous
autofocus is1; optical/focus consistency needs review before any activation.
The solver preserves hashes/profile, rejects weak/high-error data and writes
candidate_not_installed. No profile is installed, no estimated70°K substituted,
and Q8B camera calibration guard stays active. Driver monitoring/hardware
telemetry stay deferred. Next physical step is print/measure target, then guided
capture/focus review; next runtime work remains current model/backend integration.

## Approved camera patch completed — 2026-11-02

Owner approved AK-Camera720pMJPG60capture/20Hzlatest publication, only road camera,
optional rotation defaultoff, real timestamps, self-contained capture helper
and opt-in driver-camera deferral. Implemented in webcam camera.py/camerad.py,
config.py/native_capture.py/native_capture.c, camerad/SConscript and manager
registry; tests/docs updated. Enable USE_WEBCAM=1 Q8B_ROAD_ONLY=1 only for this
experimental capture path. Normal close restores previous mode/rate and saved
dynamic-framerate control (temporarily0to actually sustain60FPS).

21focused tests pass; real140frame IPC/Cereal check:19.973Hz publish,59.642Hz
source estimate, one stream/correctNV12 layout/timestamp pairs, exit0/settings
restored. Native helper actual SConscript target and pinned msgq bindings build.
Read session for exact scope/provenance. No model/managed UI/vehicle execution;
Q8B geometry remains unconfigured and its guard active. Driver-monitoring
consumers are not bypassed or supplied invented data. Next camera geometry and
current model-input/runtime contract qualification. Hardware settings still
deferred. Older no-camera-change statements below are historical.

## Current scope — camera work, 2026-11-02

Owner explicitly deferred hardware-setting changes and selected cameras.
Explained current webcam files; see [camera path](Knowledge/CAMERA_PATH.md).
Start openpilot/system/camerad/webcam/camera.py (actual OpenCV capture), then
webcam/camerad.py (device selection, NV12/IPC/messages), manager process selection
and common/transformations/camera.py geometry. Existing source requests720p25fps,
rotates180degrees; publisher loop20Hz with synthetic timestamps. Q8B geometry
remains explicitly unconfigured. No source fix/camera launch yet. Next: recover
teacher's actual camera/capture evidence and compare it to these contracts
before a bounded implementation. H1 thermal plan remains pending/deferred;
do not automatically resume it from older notes. No vehicle action authorized.

2026-11-02 owner narrowed question to webcam-mode prerequisites and requested
MM-X master/RK3588 evidence. Full hardware checklist is NOT required before
initial webcam demonstration: RK3ad69b20 uses generic PC empty/zero/default
telemetry and service exclusions. Literal masterdb27a433 differs from default
master-ticib9b7f488. See updated MM_X_LINUX_REFERENCE for11blob/9AST source audit.
Previous broad yes referred to full-port needs and was overbroad for this scope.
Camera/model/process compatibility still needs qualification; no application
changes or sensor-health bypass adopted. Hardware plan remains pending; this
research has not implemented or launched camera work.

2026-11-02 clarification: current source73773e3 reports Ubuntu/ARM64,
radxaQ8b and PC=True through the read-only identity command. PC denotes Linux
development policy; USE_WEBCAM separately selects a camera process in the same
repository. No separate webcam fork selected and no managed Q8B stack qualified.
Earlier standalone q8b/gpu_webcam remains a reference/demo. H1 hardware work
still next; cameras deferred. No runtime/config change from this explanation.

## Shutdown checkpoint — 2026-11-01; resume 2026-11-02

Owner requested end-of-work audit, then close VS Code and power off. Tomorrow
resume H1 in [hardware checklist](../tasks/todo.md): qualified read-only Q8B
temperature reporting first. No hardware implementation today. Cameras stay
deferred. Read teacher resume/inbox and inspect live Git before continuing.

Audit baseline29630251976104c71dd72f18de53f64adcc70864, clean radxa/q8b.
All application changes since identity12e44fee remain absent: later commits
document project layout, evidence and plans. Fresh11identity tests and notebook
checks pass; no full build, managed stack or hardware-driver test claimed.
Upstream reference a86979d2 and maintenance60f799a are clean. No missing
validation/pending upstream reviews; two corrected historical failures retained.
Daily reference timer remains active/persistent; next Nov2 15:30UTC. Check its
actual state after boot. Last service result success; project is never auto-merged.

VS Code autoSave setting was afterDelay and its Backups directory contained no
files at audit. Normal system shutdown uses VS Code's registered cleanup delay
inhibitor. Power-off is requested only after saved checkpoint/commit/validation;
check the teacher shutdown evidence for the accepted schedule. Saving this
handoff does not prove the later physical power-off completed.

Saved 2026-11-01. Read this after reopening, then check actual files and Git.
This is the current handoff; older session paths and next-task advice may be
historical. Update it after each completed increment and before task closeout.

## Accepted scope and defaults

The owner wants Sunnypilot on Radxa Dragon Q8B/Ubuntu ARM64, eventually lateral
control with a custom steering actuator. This sunnypilot directory is the actual
project. Keep active code, assets and tracked student knowledge inside it.
Teacher memory is the optional Comma workspace Ai; other folders are references
or development support. Both memories must record completed work and next steps.
Use relevant Agent Skills and REA as the default evidence workflow: readable
source first, REA for artifact/runtime analysis where applicable. Record actual
use; documentation changes do not imply binary or runtime verification.

## Completed checkpoint

- Board identity implementation:12e44feeff241334e184c86dc9daccdc7f9e4fa1.
  Exact Linux/aarch64 device-tree token detection, Python/C++ HardwareRadxa,
  append-only radxaQ8b enum8 and checked unconfigured-camera lookups.
- Linux ARM64 profile retained; COMMA_HARDWARE=False and PC=True service/path
  policy. Power/thermal/sensor hardware operations still use generic defaults.
- Canonical project migration:7c208a33747d4ce279131649f2ca3434ad3b3fc3.
  Ai is a real tracked directory without nested Git. Branch is radxa/q8b.
- Most recent project HEAD observed before this shutdown audit:
  29630251976104c71dd72f18de53f64adcc70864, clean. The commit containing this
  handoff is a later documentation checkpoint; get latest HEAD from Git.
- Source headers:Sunny2026.003.000/COMMA0.11.3. Upstream base6f7a2c94;
  separately updated reference was a86979d2. No newer upstream merge applied.
- Fresh stock model65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce;
  preserved old Q8B model/runtime remain separate references, not overrides.

## What was actually verified

Prior identity/relocation checks:11 Python tests,4 native C++ to Python message
checks, SCons profile probe (not full build), lint/syntax/diff,31 updater tests,
notebook layout/index and standalone notebook-copy check. Evidence is recorded
in [VALIDATION.md](VALIDATION.md), [README](../readme_wat_we_did.md) and dated
sessions. Those results are tied to their source, not automatically to future
code. This workflow task verifies documentation links/layout only.

## Where we stopped and next technical step

Owner asked what to do with the collected evidence. Saved proposed ordered
[hardware plan](../tasks/plan.md) and [checklist](../tasks/todo.md): H1 read-only
temperatures first, then power, physical IMU, cooling and remaining services.
No immediate purchase/rewiring for H1; qualify fixed IMU mounting before final
axis/bias calibration. Plan only, all implementation tasks remain pending.

Owner now selected **non-camera hardware/sensors** and deferred cameras. A complete
input/output/status checklist is now included in the non-camera hardware map,
covering board, UI/audio/network, timing, bridge and vehicle-dependent inputs. We
completed a read-only map of motion-sensor messages and board-health APIs plus
this host's exposed devices. See [non-camera hardware](Knowledge/NONCAMERA_HARDWARE.md).
This source/inventory checkpoint started at5bcc0028, clean; no application or
hardware configuration changed. Exact Git HEAD must be checked on reopening.

Findings:55 readable thermal zones, system_power/USB/ADC hwmon telemetry and a
radxa_svc_glink PWM interface. Two IIO devices exposed no accel/gyro/magnetic
channels. No /dev/gnss* node; existing CH341 USB Serial is not identified as
GNSS/IMU. No ports were opened or device/bus configuration written.

Jetson teacher studies read back: DragonPilot has explicit board-health/fan
providers; Feiyang overlay has a physical IMU publisher. See JETSON_HARDWARE_REFERENCE
for pinned evidence/limits. No implementation adopted; Q8B native I²C9 and actual
board telemetry remain our path, camera work deferred.

MM-X hardware review complete at b9b7f488: PC thermal/power/fan defaults and
carState-derived IMU policies are documented in the reference note; no code
adopted. Retain actual Q8B telemetry and physical sensor path. Next bounded
implementation remains read-only thermal mapping with tests.

Known from teacher: Adafruit LSM6DS3TR-C on I²C9/address0x6a, VIN1/GND6/SDA3/
SCL5; prior102Hz polling and1040 in-memory schema round trips at olda5f44653.
No new live bus test here. Model/interface are known; no need to ask again.
Fixed mounting/bias, current-source IPC/provider and locationd acceptance remain
open. First bounded implementation candidate is read-only thermal reporting;
then validate power domains/units and implement those separately. IMU provider
needs verified installed axes, acquisition timestamps and live sample/fault tests.
Use existing teacher IMU reports first; raw I²C need not expose IIO channels.
Stock comma sensord remains disabled under PC=True; do not turn on its hardcoded
I²C/GPIO wiring. No runtime/hardware driver was implemented by this explanation.

Camera/model-contract work remains future work, deferred by this scope. Real
thermal/power/fan, IMU/GNSS, full managed runtime and steering remain unqualified.
No firmware/CAN/vehicle actuation is authorized. Discuss upstream integration
before changing this branch; daily updates only advance the reference copy.

## Startup and interrupted-session recovery

1. Read project AGENTS, this handoff, STATE/TASKS and the relevant topic/session.
   In the workspace also read teacher Ai/RESUME_HERE, ROUTER and update inbox.
2. Run `git branch --show-current`, `git log -5 --oneline` and
   `git status --short --ignore-submodules=none` from the project root.
3. Compare dirty files and latest commits/tests with the saved checkpoint.
   Preserve unexpected edits; never clean/reset/stash them automatically.
   Missing validation is an unknown, not a passing test.
4. Resume the owner's current accepted task, or explain the saved next step.
   Saved notes survive normal shutdown; unwritten chat/edits cannot be recovered
   from them after an abrupt interruption.

At every completed increment/closeout update this handoff, relevant topics,
WORKLOG/session, and teacher resume/current-state notes; commit verified scoped
project changes and attach actual validation through the workspace ledger.

Latest workflow verification:27 notebook docs/61 relative links, workspace
source index and a copied standalone notebook check passed. No application
source changed or runtime service started. No actual reboot was performed.

2026-11-02 follow-up: webcam mode does not replace hardware support. hardwared
still reads Q8B providers; PC-disabled IMU/comma-only GNSS do not become active.
Adapt needed real board providers; reuse working OS stats, qualify optional
fitted hardware, and treat CAN/vehicle integration separately. No implementation
or runtime change; H1 thermal reporting remains next.

2026-11-02 model-input qualification: reproduced old packed720pbuffer failing
current modeld's1,413,120byte copy. Road-only output now uses get_nv12_info:
stride1280,Yrows736,UVrows368,UVoffset942080,allocation2,220,032bytes with neutral
padding. Generic mode unchanged. Added Q8B-only720pwarp build configuration.
23focused tests pass;140real frame pairs pass20.001Hz/59.628sourceHz with exact
layout/copy/padding/timestamps and restored settings. Pinned tinygrad92b742f7
CPU warp matches independent NumPy reference for two distinct synthetic views
bitwise; outputuint8[2,6,128,256] matches current ONNXnew_img metadata. No full
model/GPU/managed run or measured geometry claim. Weights65a08adc unchanged.
Owner selected printable target/tool; that next increment is in progress and
calibration guard stays active. New unstaged test_calibration.py is expected
RED until tool implementation; do not mistake it for a failure of this slice.

2026-11-03 informational folder explanation saved in Knowledge/ARCHITECTURE.md and Sessions/2026-11-03-root-folders.md; no runtime/folder changes. BeamNG optical/CAN next step remains unchanged.
