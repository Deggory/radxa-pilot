## November8 — Live BeamNG/Waveshare/Chimera test (QA32)

Genuine source501/501decoded. Native real USB/version/health43 now verified;
502samples submitted via Waveshare yielded0CANframes. Independent Python also
0frames during302submitted samples. Thus earlier offline-only USB limit is
superseded, but CAN/managed/vehicle/safety qualification remains unresolved.
Owner confirmed same USB-only/resistor-removed wiring. All readers/gateways
stopped; game open with pause acknowledged. See student live-test report;
2gatesmet/1physical-acceptance handoff.76legacy hashes/DBC/runtime preserved.
Next electrical/bus measurements; no firmware/config/update/actuator work.

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

## November 8 — Panda function inventory (QA-20261108-03)

Student Ai/Knowledge/PANDA_FUNCTIONS.md maps firmware/host/board functions;
receipt has31hashes,35normal/9flasher commands and API inventory. Distinguish
standalone red from internal peripherals, historical black and current passive
F4v17 runtime. Stale host E0/E4/FB/PythonF4 APIs and dormant FD-auto setup noted,
not fixed. Source-only at560e3ea87; no code/test/build/hardware/update/push.
Classic-only scope, preserved old firmware, halted rewrite and proposed native
Chimera RX next step retained. Full installed compatibility remains untested.

## November 8 — Panda safety inputs explained (QA-20261108-01)

Safety uses live feedback, requested CAN, model/parameter, timing and heartbeat;
compiled rules enforce model-dependent integrity/override/command limits.
Local RetroPilot active engine has no qualified production profile; old Chimera
TX does not enforce it. Source/doc-only at8fde79345, no implementation/tests or
hardware actions. Classic-only scope retained. Next remains proposed host adapter.

## November 7 — Classic CAN only and 0xDC semantics (QA21)

Owner excludes CAN FD; retain classic CAN0..8bytes in project scope. Panda DC
selects MCU safety hooks; old Chimera DC only changes relay_req_usb. Saved loop
ignores that request condition (commented) and drives PB0 from ignition. No
physical relay-switch/heartbeat-drop guarantee. Source-only at ae145e4c5;
no implementation or hardware action. See QA21 and student CHIMERA_OLD_PANDAD.
Old firmware retained, new rewrite halted; native host adapter remains proposed.

## November 7 — USB formats explained (QA20)

Old Chimera: mailbox16/health43. Current Panda:6-byte XOR header+payload,
health49; our native passive F4v17 session uses6+N/health59/classic-only.
Shared EP0/control, bulk RX0x81/TX0x03 do not imply matching packet/command
semantics. Native old-Chimera integration remains proposed. Source-only at
56b073934; no new tests/device/implementation/update/push. Next remains the
host Chimera session candidate; old firmware preserved and new rewrite halted.

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

## November 7 — Panda / Chimera comparison (QA18)

Compared older black/F413 Panda, original F413 Chimera and red/H725 Panda.
Red adds H7/CAN FD; original Chimera has custom inputs/config/relay behavior.
USB transport is shared but installed firmware protocols differ (original
mailbox16/health43). The new chimera/ remains an unfinished, halted F413 rewrite;
chimera_old/ remains preserved. No integration or physical test claimed.
Baseline ab07117573529c2e54d74f47eb3d66c0542f5506; Panda8a16e089.
Source-only explanation; notebook checks only, no source/build/hardware/update/push.
Next: await owner-selected scope; no automatic resumption. See QA-20261107-18.

## November7 — Jetson Panda identity follow-up

QA17: author says H7 USB; official red/H7 target is STM32H725, legacy black/F4
STM32F413. Author-specific PCB/chip marking remains unconfirmed. Custom
sunnypilot-cuda AGXOrin branch explicitly named; exact upstream base unresolved.
Source-only follow-up on076d73bf and official Panda8a16e089, no source/hardware
change. Modern Chimera remains halted and chimera_old preserved.

## November7 — Jetson Panda USB explanation (read-only)

QA-20261107-16 records H7 USB-A, default SPI gating, rig-specific v17/57 health
repair and cross-fork expected firmware synchronization. Four pinned076d73bf
files reread via GitHub connector; no scripts executed or hardware claim. Pattern
is relevant to host adaptation, not direct Chimera compatibility. Original Chimera
mailbox16/health43 differs. Modern Chimera remains halted; chimera_old/ preserved;
no firmware/host implementation resumed. Baseline591683739.

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

2026-11-04 latest checkpoint: NVIDIA repair passed without reboot (GTX1650/595.99.02; kernel38/42 modules; clean dpkg audit); BeamNG runs. Shared RP-SIM-1/PC/Radxa implementation saved at parent880a0adb and child150f9371. Genuine post-start capture492/492 yields valid passive CarState/canValid; 17 focused tests plus regressions pass. Physical CAN gate remains unresolved: genuine game117samples submitted via Waveshare,0Chimera frames. Owner reports CAN3, USB-only Chimera power and Waveshare resistor removed. Next qualify termination, transceiver rails, bitrate and ACK/silent mode; firmware/manager/actuation holds remain. No upstream update or push.

2026-11-04 active BeamNG CAN increment: PC Lua producer/Waveshare gateway, RP-SIM-1 additive DBC, independent Radxa decoder/monitor and explicit receive-only RETROPILOT_BEAMNG profile implemented. 17 focused checks pass plus existing regressions. PC CH340 confirmed and files installed. Live game test blocked by missing NVIDIA modules for running kernel7.0.0-38; owner authorized repair, reviewed package script is waiting for local sudo authentication in PC terminal. No repair success, physical CAN delivery, localization fusion or control is claimed. No reboot or upstream update authorized.

2026-11-04 two-day owner Q&A backfill complete: [62 chronological records](QUESTIONS.md) (47 on November 3,15 on November 4) with [exact original questions/58 completed answers](Evidence/owner-qa-20261103-04.json). Three requests link to clarification continuations; this request has a separately labelled closeout. Existing Q&A/unknowns retained. Local documentation only; no push. Continue recording later questions and read related answers before follow-ups.

2026-11-04 owner requirement:retain questions AND actual answers across sessions. Read [answered owner Q&A](QUESTIONS.md) before related follow-ups; add new answers/status/evidence at closeout.

2026-11-04:public radxa-pilot publication with master/Radxa/RetroPilot history; original commits preserved. [Evidence](Reports/github-publication-20261104/README.md). Upstream updates stay paused.

2026-11-04:owner-approved two upstream updates applied;camera/Thneed/RetroPilot unchanged. Future updates remain on hold. [Evidence](Reports/upstream-approved-20261104/README.md).

UPSTREAM HOLD2026-11-04: read-only GitHub checks allowed; owner approval required before any update. Automatic reference timer paused. Read current upstream policy/session before acting.

History note: [camera/thneed/retropilot subject labels and old/new SHA map](Reports/commit-topics-20261104/README.md). Original evidence preserved; runtime source unchanged.

Restart checkpoint: [RetroPilot audit before shutdown](Reports/retropilot-shutdown-audit-20261103/README.md),168 focused checks pass; live output disabled, hardware holds preserved.

Current2026-11-03: [active safety software checks](Reports/retropilot-active-safety-20261103/README.md), native fixture only; no production profile or live output. Chimera held, relays excluded.

Current safety increment: [restricted RetroPilot policy](Reports/retropilot-safety-20261103/README.md)
registered and tested; active control disabled, Chimera held, relays excluded.

2026-11-03 owner direction: **Chimera work is on hold until the owner resumes it.**
Current discussion is the need for modern RetroPilot messages and why C2 changed
Cereal. Earlier next-step notes about Chimera acceptance are deferred.

2026-11-03 current: [RetroPilot C2 selection compatibility](Knowledge/RETROPILOT_CAR_PORT.md)
now includes fingerprints.py/shared MIGRATION; automatic matching remains pending.

Current2026-11-03: [RetroPilot car platform](Knowledge/RETROPILOT_CAR_PORT.md)
implemented receive-only; Chimera backend/live loop still pending. See HANDOFF.

Radxa simplification assessment: [repository cleanup](Knowledge/REPOSITORY_CLEANUP.md); docs README is the short project entry, no files deleted.

Current BeamNG design2026-11-03: [optical camera + CAN](../openpilot/tools/sim/beamng/README.md), PC/Radxa roles and canonical DBC gaps. Supersedes older network-image next steps below. Runtime implementation pending.

Current BeamNG checkpoint: [complete audit](../openpilot/tools/sim/beamng_reference/AUDIT.md),96source files verified; current opendbc API and simulator contracts block direct integration.

BeamNG files are collected in [sim/beamng_reference](../openpilot/tools/sim/beamng_reference/README.md), exact source pin/verification included.

Current owner task: [BeamNG bridge](Knowledge/BEAMNG_BRIDGE.md); source review complete, adapter not implemented. NPU research paused at rejected baseline.

2026-11-02 fresh NPU baseline: actual200+3 Q8B calls pass execution,
W8A8 accuracy fails;400MB DLC/444MB context, no default switch. Student
`Ai/Knowledge/NPU_CONVERSION.md` and `openpilot/selfdrive/modeld/npu/RESULTS.md`
contain measured per-head errors, retained FP16 failure and proposed next step.

Current NPU work: [fresh conversion](Knowledge/NPU_CONVERSION.md). Read the dated session before resuming; the first dataset is rejected and corrected v2 calibration is in progress.

Current result: [live Q8B UI telemetry](Knowledge/UI_TELEMETRY.md).

Current performance result: [maximum mode and resident GPU baseline](Knowledge/MAX_PERFORMANCE.md).

2026-11-02 latest: [installation](Knowledge/INSTALLATION.md) now documents a clean
locked environment and passing minimal root build; start HANDOFF for checks/limits.

2026-11-02 latest: [live Thneed modeld integration](Sessions/2026-11-02-thneed-modeld.md)
verified camera→stock modeld→actual Sunny overlay at20Hz bench. Start HANDOFF for limits/launch.

2026-11-02 latest: [existing Thneed import](Sessions/2026-11-02-thneed-import.md)
provides copied CD210 plus in-project native GPU replay/current-queue adapter. No reconversion.

2026-11-02 GPU reference: [teacher Thneed pipeline](Knowledge/THNEED_GPU_REFERENCE.md)
records tested exporter/replay, exact artifacts and sustained timings; CD210 learned weights match; old/new history wrappers differ.

# Start here: Sunnypilot repository memory

2026-11-02 latest: actual Sunnypilot onroad camera preview now verified;
see HANDOFF/resume for launch/active-session state. Model integration pending.

2026-11-02 latest: owner chose temporary MM-X720p/focal900 geometry in Q8B
road-only mode; automatic/checkerboard work deferred. Start HANDOFF/resume.

Latest camera checkpoint: padded model layout fixed; [printable target/tool guide](../openpilot/system/camerad/webcam/CALIBRATION.md)
ready after owner choice. Actual lens data/focus/mount and model backend remain
unqualified. Start HANDOFF for the physical print/capture step, not hardware H1.

Current scope2026-11-02: owner deferred hardware-setting changes and selected
camera work. Start [camera path](Knowledge/CAMERA_PATH.md), then HANDOFF. This
supersedes the older camera-deferred/hardware-first statements below.

Jetson hardware reference: [two teacher studies compared](Knowledge/JETSON_HARDWARE_REFERENCE.md).

Current owner focus: [non-camera hardware/sensors](Knowledge/NONCAMERA_HARDWARE.md);
camera work deferred. Known IMU:Adafruit LSM6DS3TR-C/I²C9/0x6a from teacher
evidence; see HANDOFF and the map for prior tests/current integration gaps.

After reopening, start with [HANDOFF.md](HANDOFF.md). It records where we left
off, what is verified and the next step. Check live Git/files before resuming.
The default Agent Skills + REA workflow and both-memory closeout are standing
owner instructions; see [skills](Knowledge/SKILLS.md) and REPO_RULES.

Current location: this `sunnypilot/` is the project, branch `radxa/q8b`.
`Ai/` is a real tracked directory. Other workspace folders are references or
development tools. See [location correction](Sessions/2026-11-01-project-location.md).
Historical entries below may describe the superseded external notebook layout.

Current implemented identity and checks: [what we did](../readme_wat_we_did.md),
[2026-11-01 session](Sessions/2026-11-01-radxa-board-identity.md).

1. When working in the Comma workspace, read its [ROUTER](/home/radxa/comma/Ai/ROUTER.md) and
   [live update inbox](/home/radxa/comma/Ai/SUNNYPILOT_UPDATE_INBOX.md).
2. Read [STATE.md](STATE.md) and [TASKS.md](TASKS.md). Check actual Git HEAD,
   branch and dirty state in the checkout being discussed. Vendor and Radxa
   port are separate repositories with different purposes.
3. Pick a topic below; inspect its referenced source before changing behavior.
4. Before finishing, update this notebook and promote durable cross-project
   facts plus a concise session record to the workspace Ai memory.

| Question | Read |
| --- | --- |
| What is this repository and where is each subsystem? | [Architecture](Knowledge/ARCHITECTURE.md), [module map](Knowledge/MODULE_MAP.md) |
| What does system code do, file by file? | [System review](Knowledge/SYSTEM.md) |
| What changes for Radxa and what already works? | [Q8B port](Knowledge/RADXA_PORT.md) |
| How does Ubuntu/Linux differ from AGNOS platform selection? | [Linux detection and Q8B plan](Knowledge/LINUX_PLATFORM.md) |
| How does MM-X adapt Sunny to PC/Linux? | [Pinned MM-X reference](Knowledge/MM_X_LINUX_REFERENCE.md) |
| Which branch/model/runtime/version are we using? | [Versions and update workflow](Knowledge/UPSTREAM_AND_VERSIONS.md), STATE |
| What did we change, test or decide? | [Worklog](WORKLOG.md), [validation](VALIDATION.md), [decisions](DECISIONS.md), Sessions |
| What is unfinished or uncertain? | [Tasks](TASKS.md), [questions](QUESTIONS.md), [coverage](Knowledge/COVERAGE.md) |
| Which skill applies? | [Skill workflow](Knowledge/SKILLS.md) |
| Where is a tracked source file? | [Pinned source index](Evidence/source-index.json); search a matching entry, not the whole JSON |
| Where are deeper historical symbols/message traces? | [Existing brain index](/home/radxa/comma/Ai/AI_BRAIN/00_MASTER_INDEX.md); verify freshness first |

Useful checks:

```bash
git -C /home/radxa/comma/sunnypilot status --short --ignore-submodules=none
git -C /home/radxa/comma/sunnypilot rev-parse HEAD
git -C /home/radxa/comma/q8b/sunnypilot-upstream status --short --ignore-submodules=none
git -C /home/radxa/comma/q8b/sunnypilot-upstream rev-parse HEAD
git -C /home/radxa/comma/sunnypilot log -5 --oneline
```

If source HEAD differs from a topic's recorded pin, its findings are historical
until the relevant diff is checked. Preserve old evidence and date the new
finding. Do not silently rewrite an old test into a claim about the new source.
