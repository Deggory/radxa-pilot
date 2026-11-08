## November8 — Live BeamNG/Waveshare/Chimera test (QA32)

Genuine source501/501decoded. Native real USB/version/health43 now verified;
502samples submitted via Waveshare yielded0CANframes. Independent Python also
0frames during302submitted samples. Thus earlier offline-only USB limit is
superseded, but CAN/managed/vehicle/safety qualification remains unresolved.
Owner confirmed same USB-only/resistor-removed wiring. All readers/gateways
stopped; game open with pause acknowledged. See student live-test report;
2gatesmet/1physical-acceptance handoff.76legacy hashes/DBC/runtime preserved.
Next electrical/bus measurements; no firmware/config/update/actuator work.

## November8 — RetroPilot safety/DBC focused review (QA31)

Modern restricted hooks and synthetic-profile active engine exist; normal init
has no qualified profile and old Chimera does not enforce them. Fresh50compiled
tests pass. Canonical/package DBC match28messages and7TX/7RX IDs/DLCs. Historical
WIP is separate; partial0x301CRC, ADC layout, units/bus qualification gaps remain.
See student Reports/retropilot-safety-dbc-20261108; baseline009ec389/opendbc150f9371.
No product/firmware/DBC/device work; next passive scope and saved holds unchanged.

## November8 — Chimera data availability explained (QA30)

USB detection is confirmed; no local pandad process found and no live telemetry
read performed. Adapter supports raw CAN plus18raw health fields. Vehicle
speed/angle/engine/brake/buttons/module readings depend on actual frames,
hostbus2/config/DBC/freshness; speed scale remains unqualified. Data/placeholder
inventory added to implemented USB contract. Baseline26d97d7b, prior tests reused;
no device/code/runtime changes. Next owner-selected live scope; holds unchanged.

## November8 — Live USB Chimera detected (QA29)

Linux enumerates RetroPilot Chimera bbaa:ddcc, serial3a0044001651333038373636,
bus003/device006 atsysfs3-4.1. Fresh lsusb/sysfs-only receipt is in student
Ai/Evidence/chimera-usb-enumeration-20261108.json. No firmware/health/CAN query
or pandad startup; actual native/vehicle/relay qualification remains pending.
No source/hardware configuration changes; rewrite/update holds unchanged.
Next: owner-selected scope beyond completed USB detection.

## November8 — Safety boundary clarification (QA28)

Read-only host guards prevent commands through this adapter; they do not add
MCU driving safety. Old firmware TX lacks modern hooks and PB0 follows ignition,
so host loss is not a proven relay/actuator cutoff. Raw safety fields and host
noOutput settings do not install a policy. Current source checked at9940a21f;
prior offline tests reused. See implemented USB contract safety section/QA28.
No code/hardware changes; next remains scoped passive-board qualification,
with active safety/profile/electrical validation unresolved and holds retained.

## November8 — C2-era Chimera compatibility and file map (QA27)

Original protocol now has a native receive-only path, subject to exact identity
and physical qualification. Two new runtime files are chimera_usb.h/.cc; six
existing runtime/build files integrate session, publication, main and build.
The implemented contract contains the file map. Source008a7e81; explanation
baseline dd5ac056. Prior offline checks reused; no new runtime/hardware action.
Next remains separately scoped matching-board passive qualification; holds remain.

## November8 — Native Chimera capability clarification (QA26)

Explained implemented USB reception, three-bus classic CAN publication and raw
health diagnostics. Vehicle signal meanings require actual producers and matching
parsers/DBC; no automatic sensor/calibration or driving-command capability.
Source checkpoint008a7e81, documentation baseline0d8c8cfe. Prior offline validation
stands; no new runtime/hardware work. Physical qualification remains pending;
next step unchanged: separately scoped matching-board receive-only qualification.
See QA26 and docs/CHIMERA_OLD_USB.md. Rewrite/update holds remain unchanged.

## November8 — Native original-Chimera passive acceptance (QA25)

Owner authorized host adaptation. pandad now dispatches pinned old Chimera
mailbox16/health43 alongside F4, publishes CAN and labelled raw diagnostics,
and closes/clears state on failure. See CHIMERA_OLD_USB contract and the
November8chimera-native-passive session for actual tests/commit/limits. No
managed/control admission or physical qualification. Old firmware preserved,
new rewrite halted, update hold retained. Next: review saved offline evidence
and plan a separately qualified matching-board receive-only check; do not
start hardware or active-control work automatically from this handoff.

## November8 — Panda host connection path explained (QA24)

USB is owned by panda_usb.cc inside pandad. Launcher/main/session, normal
can/sendcan/card path and our passive F4v17-only entry are distinguished in the
comparison topic and November8panda-host-path session. Source explanation only;
no runtime/device work. Next await selected task; original Chimera RX remains
proposed, rewrite halted and saved upstream hold unchanged.

## November 8 — Panda / original Chimera / rewrite explained (QA23)

Compared black/F413 Panda, original Chimera, red/H725 Panda and the halted
F413 rewrite. See PANDA_CHIMERA_COMPARISON and the November8comparison session.
31prior inventory hashes and76legacy files match; no new runtime/build/device
test. Modern safety/diagnostics differ; old retrofit I/O stays distinct. Native
old-Chimera RX remains proposed; classic-only scope and update hold unchanged.
Next: await owner-selected task; this explanation resumes no implementation.

## November 8 — Skills adopted; teacher audit and shutdown (QA21–22)

Understand Anything and Unlazy are installed; the earlier proposed-only status
is superseded. Read [teacher workflow](Knowledge/TEACHER_WORKFLOW.md) and
[skills audit handoff](Sessions/2026-11-08-teacher-skills-audit.md).
Focused knowledge analysis and completion gates audit the saved teacher workflow;
coverage and actual results are recorded there. Owner requested power-off after
closeout. On restart inspect live Git and the audit receipt; keep Chimera halted
and upstream changes held. Do not infer missing hardware/runtime qualification.

## November 8 — Understand Anything / Unlazy assessment (QA20)

Source-only recommendation: optional focused architecture graph and compact
acceptance gates for substantial work; adoption remains proposed. Neither tool
installed/executed and no code/hardware/update changes. See the skills topic
and November 8 skills-fit session for source pins and limits. Chimera rewrite
remains halted; next step is owner-selected scope, no automatic implementation.

## November 7 — Original Chimera native pandad route (QA19)

Owner keeps chimera_old and defers firmware improvements. Source audit identifies
native host work: separate mailbox16/health43 session/decoder and raw diagnostics,
then lifecycle and qualified managed status. Existing USB identity/backend and
Python receiver are reusable; current native session accepts only F4v17. No
implementation resumed.22offline tests pass;76old files still hash-match.
Baseline5722805f8; report sunnypilot/Ai/Knowledge/CHIMERA_OLD_PANDAD.md and QA19.
Keep bus identity, unavailable health and old relay/safety semantics explicit.
Next implementation candidate: native passive Chimera CAN/status path, not new
firmware or active control. Actual USB/image/wiring/units remain unqualified.

## November7 — Separate legacy Chimera copy created

Owner requested `sunnypilot/chimera_old/` first. Copied76legacy source/dependency/
build-reference/recovery files (1,964,585bytes), all SHA256 verified against the
saved Ocelot tree/bundle. Ocelotd87892fa plus39saved dirty entries retained; no
source changes. Exact de193215 historical-image source/C2 installed match remains
unverified. Restricted linker/private keys/generated objects excluded, so no
complete build claim. New README/SOURCES.json explain provenance and limits.
Modern `chimera/` implementation remains halted. This step only preserves files;
no host adaptation/build/device/flash/update/push. Baselinee71640be3; next await
owner's next scoped request for the original-Chimera host route.

## November7 — Owner halted Chimera implementation

Owner: "hault this ,this is is taking too uch time why". Stop implementation;
do not resume automatically from the earlier next-step instructions. Last verified
code commit e71640be3f15262670e38442ec28b3f5f5a7f823; no new implementation,
tests, hardware actions or push. The delay reflects over-fragmented increments
and repeated audits/documentation/handoffs as well as unfinished MCU/host work.
Offline USB lifecycle exists; board startup remains held and operational bulk/CAN
exchange is unfinished. Stop record only; wait for an explicit new instruction.

## November7 — Integrated USB control lifecycle (T03c4)

Owner wants a larger capability beyond the repeated25% checkpoint. Implemented
explicit main/service/driver attachment, bounded10ms disconnect hold, pre/post
power/invariants and pre-attach event drain, pristine EP0/SDIS readback, captured
OTG cause ACK, suspend/resume with retained address/config/armed transfer, reset
cancellation, session-end priority/release and explicit fresh start/attach reconnect.
No-sense VBUS stays UNKNOWN; default ARM main keeps NULL profile/reader and held.
Main loop now accepts ATTACHED/SUSPENDED; attach call chain is retained in ARM.
36firmware tests pass warnings-as-errors, including92new composed ASan/UBSan
scenarios/40reconnect cycles. Three copied-source mutations caught. Independent
gpt-6-astra review approved final source and independently passed92scenarios;
no required findings unresolved. Raw9064/projected9200/globals264/stack4096, SHA
341ef240b4af887d74ae8a7800b892d116e8aca8ddf1af03640492d6ef83badd.
Seven of25build inputs changed;18same; old8316-byte artifacts retained ignored.
Actual hardware0%; no flash/device/config/CAN/relay/OBD-C/update/push actions.
Revised full-roadmap rough estimate30% complete/70% remaining; lifecycle100% offline.
This dated correction replaces25% as current planning estimate, not a measured
fraction of time/readiness. Earlier checkpoints remain historical. Next opt-in
board USB startup binding (pins/explicit power profile/recovery boundaries), then
bulk/CAN RX and operational status. Physical power/current/recovery/bench proof
remains open; hostT08b2d remains queued. No fake VBUS/cable-presence claim or live
PLL48 health monitoring. Source baseline86c734924; contract chimera/docs/USB_LIFECYCLE.md;
receipt student Ai/Evidence/chimera-usb-lifecycle-20261107.json. Clean/commit/ledger
final readback saved separately in teacher layer. Prior host statsd issue untouched.

## November7 — Explicit legacy no-VBUS session implemented offline (T03c3b)

Owner "proceed" continues the owner-identified Ocelot base circuit; no repeated
schematic question. Core/service expose validated UNFORCED(default) and explicit
LEGACY_NO_VBUS modes. Legacy sets only BVALOEN/BVALOVAL, VBDENoff, SDISstillset.
Main copies/validates mode; legacy requires NULL reader and keeps VBUS UNKNOWN.
Mixed/invalid/mismatched modes reject; no fallback. Exact mode/PHY/VBDEN invariants,
core readback, reset cancellation and accessible override cleanup are tested.
Suspend/wrong-role/OTG summary faults stop; OTG causes are not decoded yet (even
benign summary currently unsupported). Cleanup failures retain ownership until
explicit retry; successful stop resets mode. Actual main.c unchanged, NULL profile/
reader, no attachment/pin/descriptor-power profile selected. No device/flash/TX.
34firmware tests pass incl61new real-component ASan/UBSan scenarios, three caught
mutations, ARM/copy/linker checks. Fixture initially left injected suspend set;
now asserts refault, then clears actual condition before healthy explicit restart.
No production weakening. Raw8316/globals260/stack4096, SHA745f66c5c408a8c046c6c7ed3f3c3edc576b9743b9a0b35d860770a1f24e8826.
25inputs:7changed/18unchanged. Ocelot39dirty/19hashes, archive/DBC/submodules and
host/model/camera/Thneed preserved. Baselineb3ff3d26e; evidence student Ai/Evidence/chimera-legacy-session-20261107.json.
Stage100% offline; overallabout25%/75% remaining; new-firmware physical0%.
Next reviewed OTG cause handling and controlled attached-state lifecycle offline;
actual board power/pins/installed recovery/bench remain pending. HostT08b2d queued.
Updates held; no push. QA-20261107-12/source contracts pin actual implemented scope.

## November7 — Owner identifies Ocelot base; power trace changes next step (T01b)

Owner correction: "see on ovelot foldeer the sch is same onli i/o is added".
Use Ocelot drawings as Chimera's working base circuit with added I/O; do not ask
again for a base schematic already identified. Gateway XML/board17net-pad matches
and Pro source/original-PDF comparison yield36source checks: USB VBUS -> BAS40 ->
shared5V, external5V regulator on same rail,3.3V downstream; no MCU VBUS sense net.
Gateway PA9/pad42 unconnected; Pro PA9 goes H5pin9, not VBUS. Nine CAN MCU pins
match existing map. Original F4 code forces BVALOEN/BVALOVAL; raw power descriptor
bytes0xc0/0x32 are declarations, not measurements. Added relay/OBD-C/analog mapping
must stay Chimera-specific (PB0 relay, PC2/PC3 analog), not copied from base IO.
Correction to T03c3a next step: sensed guard cannot bind to an absent detector.
Next implement/test explicit opt-in legacy no-VBUS session mode offline, separate
from sensed mode; no dummy PRESENT callback or automatic activation. Actual
attachment/power measurements/installed recovery remain open; main stays held.
Firmware/host/image unchanged (25inputs,8108bytes);33tests remain pinned to4b6098789,
not freshly rerun here. Source replay/Ruff/notebook/preservation checks recorded.
This source-audit stage100%; overallabout25%/75% remaining; physical0%. Keep stage
percentage reporting. QA-20261107-11 and student Ai/Evidence/chimera-base-power-20261107.json
pin owner statement, sources/limits. No device/flash/config/TX/update/push.

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
[Session](Sessions/2026-11-07-chimera-main-startup.md).

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

## 2026-11-03 — Current RetroPilot safety work

- [x] Register modern ID 39 and implement/test disabled-command-only policy.
- [x] Native debug/release safety, schema/library build and regressions.
- [ ] Qualify active actuator/driver bounds, RX integrity/freshness and engagement.
- [ ] Implement active rules only against those qualified requirements.
- Chimera work is held by owner; relay integration is excluded.
- Current car interface remains noOutput and runtime controller output is zero.

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

Checklist clarification2026-11-03: explicit identification is implemented; automatic fingerprints and active firmware safety/tests remain pending. Current task/next step unchanged: receive-only Chimera transport and producer/profile qualification. docs/RETROPILOT.md has actual file status.

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

## 2026-11-03 — Connected PC requirements checkpoint

Owner reports connected BeamNG PC. Existing sim/beamng README now maps six
Sunny needs; actual gateway/Chimera/car/motion/command adapters remain pending.
Q8B eth1 UP10.43.0.1; neighbor10.43.0.216 reachable. Strict SSH exited255:
no trusted ED25519 host key; no remote inspection. Game/car/mods unverified.
Keep optical+CAN architecture/CD210GPU, canonical DBC and existing source pins.
Next: resolve trusted PC identity for read-only inspection and continue wire
contract increment1, then receive-only/shadow. No CAN TX or actuation.
Details/tests: Sessions/2026-11-03-beamng-requirements.md in both notebooks.

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

# Work status and next task

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

Current next physical action: print/measure flat A4target in webcam/calibration,
then collect varied720pviews using calibrate.py; review fixed optical/focus state
before trusting/activating a lens profile. Tool is ready; physical images are
not yet collected.6fea7ecf fixed the current model NV12 boundary; model/GPU/UI
operation still unqualified. Calibration guard remains active, no FOV guess.

2026-11-02 first road-camera patch implemented and tested after explicit owner
approval. See [session](Sessions/2026-11-02-road-camera-patch.md). Next: qualify
actual camera geometry and current model-input/runtime contract. Keep hardware
plan deferred. Do not claim the new capture/IPC check is a full model/UI run.

## Scope supersedes hardware-first order — 2026-11-02

Owner now defers hardware-setting changes and requests camera work. Current
next task: camera capture/publisher/geometry contract review using teacher
camera evidence and [source map](Knowledge/CAMERA_PATH.md). No driver/camera
change or launch yet. Keep incomplete hardware plan/checklist intact for later.

End-of-day2026-11-01: owner resumes tomorrow2026-11-02. Next technical work H1
read-only thermal reporting. Audit/checkpoint only today; no driver started.
See [shutdown session](Sessions/2026-11-01-shutdown-audit.md).

## Proposed implementation sequence — 2026-11-01

See [hardware plan](../tasks/plan.md) and [checklist](../tasks/todo.md).
Start H1 with real read-only thermal mapping/tests; then qualified power,
physical IMU, cooling and needed platform services. All implementation tasks
remain pending. This response saves guidance, not new drivers or runtime tests.

## Current focus — non-camera hardware, 2026-11-01

Owner deferred cameras. Read [hardware/sensor map](Knowledge/NONCAMERA_HARDWARE.md)
and [HANDOFF](HANDOFF.md). Board thermal/power/PWM interfaces are exposed; no
IIO motion channels found. Teacher records Adafruit LSM6DS3TR-C/I²C9/0x6a,
prior102Hz raw polling and1040 schema round trips; this uses raw I²C, not IIO. Inventory
only, no driver/config/runtime change. Next candidate: read-only thermal mapping,
then verified power reporting and actual IMU provider. Earlier camera/model
T0next-task advice below is deferred by the current scope.

Current restart checkpoint and next step: [HANDOFF.md](HANDOFF.md). Agent Skills
+ REA and both-memory closeout are standing defaults, including after reopening.
No additional hardware/runtime implementation was made by this workflow task.

## 2026-11-01 — Working project is sunnypilot; notebook is inside it

Owner clarified that `sunnypilot/` is the actual project and other workspace
folders are references/support. The existing radxa/q8b repository was moved
from q8b/sunnypilot-radxa into sunnypilot, preserving identity commit12e44fee,
all Git history, assets, submodule pins and IDE files. The clean upstream copy
is now q8b/sunnypilot-upstream and remains the only daily-updated checkout.
No upstream code was merged. The former project path is a compatibility link.

`Ai/` is now a real directory versioned with the project, copied from notebook
ed8afade without nested Git. The old notebook repository retains history only.
Active code, README and knowledge belong here; external references are optional
context and do not supply the new identity implementation at runtime.

See [README](../readme_wat_we_did.md) from this Ai directory, or
[location session](Sessions/2026-11-01-project-location.md). Earlier recorded
paths/roles below are historical and must be interpreted using their source
pins. This move does not qualify camera/model/UI/sensors or vehicle actuation.


Current owner authorization,2026-11-01: implement Linux/ARM64/Q8B board identity
and save a README. This is complete in protected port12e44fee. It supersedes
the earlier identity implementation hold; it does not authorize other hardware
providers, model integration or vehicle actuation. Daily vendor/memory work
continues under the standing policy.

## Completed

- Implement Q8B identity across detection, Python/C++, schemas and camera guards;
  11 Python/4 native checks and SCons-profile/lint pass. See
  [README](/home/radxa/comma/q8b/sunnypilot-radxa/readme_wat_we_did.md).

- Preserve previous Q8B source/model/runtime and start a clean stock vendor copy.
- Separate protected Radxa development from the daily-updated vendor.
- Track upstream/local commits and explicit validation; discuss related updates
  in the next chat.
- Explain the system tree and hardware boundary at source pin `6f7a2c94`.
- Create shared specialist memory, seed known facts and reserve its local links
  against conflicting upstream updates.

## Next implementation: T0 stock-contract preflight

Read the [workspace plan](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_RADXA_PLAN.md).
Work in this sunnypilot project. Establish actual dependencies, schemas, current
stock model inputs/outputs, parser, chosen runtime and camera buffer contract.
Do not silently insert the preserved old model/runtime into fresh stock code.

Then pursue a bounded recorded-input camera → model messages → actual Sunny UI
slice; qualify live capture/IMU/health and managed fault recovery afterward.
Vehicle/custom-actuator work is a separate later milestone with canonical DBC
and explicit measured feedback/safety requirements.

## Notebook upkeep after each task

Update only relevant topics and state; append a dated session with exact
source pins, changed paths and validation. Record unknowns honestly. Promote
cross-project facts to main Ai and commit the notebook with its journal hook.
Do not turn an old completed task into the next task because it appears in
an imported historical note.

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
