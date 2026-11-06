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
