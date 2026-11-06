## 2026-11-06 — Isolate legacy USB diagnostics before pandaStates admission

Implemented T08b1 decision: allocate existing reserved Data field/service
customReservedRawData1 to panda-usb-status JSON schema1. Preserve raw0's Thneed
ownership. Publish decoded classical CAN on can, complete legacy status only on
the diagnostic service. hardwared reads ignition from pandaStates without checking
Event.valid, and PandaState has no per-field validity, so incomplete legacy
pandaStates publication is deferred. Diagnostic validity means complete decoded
observation, not readiness; operational=false. No CAN protocol/DBC change. See
QA-20261106-28 and USB_PASSIVE_RECEIVE.md. Profile admission/ignition policy remain
next work, not a tested operational integration.

## 2026-11-06 — USB-only Radxa-to-Chimera/Panda deployment

Accepted owner clarification QA-20261106-24: use USB only. Exclude SPI wiring,
probing and automatic fallback from this deployment. Generic SPI source may remain
historical support; it is not a target requirement. T08 must replace inherited
SPI construction/listing with pinned USB selection and fail disconnected on USB
failure. Earlier preservation wording does not authorize a mixed-transport path.
Requirement/roadmap updated; runtime migration pending, no hardware action.

## 2026-11-05 — Chimera preservation scope; architecture proposed

Owner selected dedicated chimera/board folder and research-before-change roadmap.
Preserve3buses,direct inputs,onboard relay,Core Config; relay preservation is now
in scope,not relay operation or external Relay Core work. Proposed F413modernUSB
plus nativehostUSB,distinct identity,explicit sources and versionedconfig; no
implementation/activeprofile accepted by this document. See QA-20261105-13.

## 2026-11-05 — Master is GitHub default and comparison baseline

Owner corrected the desired branch layout. Set master as default; select
radxa/q8b to view custom project and compare against master. This supersedes
the November4Radxa-default choice. Metadata-only change, remote commits retained;
no branch merge or automatic update authorized. QA-20261105-02/dated receipt.

## 2026-11-05 — Synchronize public master only

The owner's request authorizes making GitHub master equal official Sunnypilot.
Fast-forward only; retain Radxa and support branch histories, default view and
paused automatic updates. No implied Radxa source integration or recurring sync.
Actual result932ff06d; source verification only. QA-20261105-01 records the answer.

## 2026-11-04 — RP-SIM-1 and explicit receive-only BeamNG profile

Owner authorized adding missing BeamNG telemetry centrally to the shared DBC.
Preserve the original20message prefix; version and synchronize the eight new
simulator-only messages. Physical profile/firmware defaults stay unchanged.
RETROPILOT_BEAMNG is explicit and passive,with qualified wire units but no
measured vehicle tune or actuator authority. IMU transport is separate from
measured device-frame/localization integration. Owner separately authorized
PC NVIDIA repair; local authentication provided,no reboot yet authorized.

2026-11-04 two-day owner Q&A backfill complete: [62 chronological records](QUESTIONS.md) (47 on November 3,15 on November 4) with [exact original questions/58 completed answers](Evidence/owner-qa-20261103-04.json). Three requests link to clarification continuations; this request has a separately labelled closeout. Existing Q&A/unknowns retained. Local documentation only; no push. Continue recording later questions and read related answers before follow-ups.

2026-11-04 owner Q&A memory rule implemented:explicit recent questions AND actual answers in [existing question log](QUESTIONS.md); startup/closeout instructions require retrieval and continued recording. Older unknowns retained; summaries are not full transcripts or automatic model training. Documentation only,local commit/no push.

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

## 2026-11-04 — Updates held until explicit owner approval

Latest owner instruction: check GitHub master, "do not update yet without
asking". Read-only status/source checks remain allowed. Apply the hold to both
the actual Radxa project and the separate upstream reference; do not run
updater.py check, fetch/fast-forward the reference, integrate upstream, pull,
merge/rebase or resume automatic updates without explicit approval. This
supersedes earlier standing daily vendor-advance authorization while held.

The daily timer was enabled/active at startup and had refreshed the reference
at15:30UTC before the request. It is now linked/inactive, with the automatic
timers.target.wants link removed; its source unit and service are retained.
The service is inactive. No future schedule is armed. Resume/reenable only
after approval; a later request asking whether updates exist is not approval.
The actual Radxa project received no upstream source change. Local notebook
records do not represent applying an upstream update.

## Owner commit-topic naming rule — 2026-11-04

For camera work use a camera scope (e.g. feat(camera): ...); for the Thneed
runtime/integration use thneed; for the RetroPilot port use retropilot. Include
multiple scopes when a commit spans them, e.g. perf(camera,thneed): .... Apply
to implementation, tests, tooling and their documentation. Keep other topics
accurately named and retain Assisted-by disclosure required by docs/AI_POLICY.

Owner explicitly authorized rewording existing local messages on2026-11-04.
The original branch history is preserved and old/new IDs are mapped in
Reports/commit-topics-20261104/. Historical test/source SHAs remain original
versions, with current aliases available; do not edit them to imply a retest.
This one requested rewrite does not authorize future automatic rewrites,
merges or pushes. Standard protected-project/upstream rules remain in force.

## 2026-11-04 — Owner-selected required hardware: all three modules

Owner explicitly selected these as required parts of our existing Radxa Q8B /
modern Sunnypilot RetroPilot project and requested both notebooks remember them:

| Required part | Owner-selected job |
| --- | --- |
| Chimera | Connects the computer to CAN and gathers vehicle signals. |
| Interceptor Core | Handles analog accelerator or steering torque-sensor signals. |
| Actuator Core | Controls motors used in custom actuators. |

All three belong to the intended architecture. Do not reduce this selection to
Chimera alone, treat the two Cores merely as examples, or ask the owner to repeat
which three were selected. This is an owner requirement, not proof of purchase,
installed hardware, working firmware, exact per-axis assignments or calibration.

Recording the architecture does not resume held Chimera implementation or the
paused physical Interceptor bench task. Relays remain excluded. No iBooster or
other module is additionally selected by this table. Current noOutput, absent
active vehicle profile and zero runtime CAN remain. Canonical shared
ocelot_controls.dbc remains selected; no rename, wire change or device action.
Exact endpoint/axis mapping and qualification remain future integration work.

## 2026-11-03 — Preserve the tested boundary across shutdown/restart

Record software tests and source matches separately from actual game/vehicle/
firmware integration. Two RetroPilot safety headers form one firmware policy;
registration or host file presence does not install enforcement into Chimera.
Keep production noOutput, explicit selection and absent active profile after
restart. User authorized saving and orderly local shutdown; finish audit/notes/
commit/validation first and allow normal editor/session cleanup without force.

## 2026-11-03 — Profile-dependent active rules without invented calibration

Owner's "why not fix it" authorizes implementing missing safety behavior, not
assuming a BeamNG/physical calibration. Add a parameterized native-tested C
engine for canonical interceptor steering/gas and iBooster position, leaving
production initialization without any active profile. Firmware parameters
cannot select the artificial test fixture. Keep noOutput/zero live controller.
Require fault-latched recovery, bounded commands and retained output history.
Block invalid-sequence disabled sends with an active profile; require a full16-
count startup disable cycle to cover unknown counters in non-resynchronizing
endpoints. Qualify delivery, producer/endpoint semantics and limits separately.
Chimera remains held, relay/physical Interceptor work excluded. Software review
and native tests are not permission or proof for installed vehicle actuation.

## 2026-11-03 — Register restricted safety without guessing active limits

User authorized implementing the missing identifier/rules/tests. Existing C2
constants and DBC signal ranges are not measured Radxa/BeamNG actuator limits.
Append local enum 39, keep existing IDs, and implement explicit disabled-only
CAN rules with full compiled tests. Preserve noOutput selection and zero live
output. Repeated counters remain allowed for disabled packets; this is not
an engagement/freshness policy. Reject unknown parameters and exclude relays.
No physical control/flash or held Chimera work follows from source registration.
Review future upstream enum assignments before integrating them.

## 2026-11-03 — Keep modern checks and identify Chimera independently

Use history to migrate capability across the stack, preserving modern safety,
communication/model checks and manager ownership. Receive-only USB adapter is
standalone/pinned, not a stock Panda lifecycle or synthetic pandaStates path.
Decode raw health43 safety17 without modern enum translation. Shared bbaa:ddcc
is also observed on Interceptor DAC Bench; require product, serial and exact
version before receiving. Angle STATE1 follows reviewed Chimera/ZSS producer;
no canonical DBC change. Owner confirmed current Radxa Q8B target. Physical
profile/driver-input/MCU safety and managed health/ignition remain pending.

## 2026-11-03 — C2 controller migrated to modern offline replay

Separate completed controller calculation from pending live qualification.
Use an explicit immutable profile for offline candidates; keep runtime output
zero independently of CP flags. Preserve C2 as a labelled reference, not the
owner's calibration:350counts conflicts with local400channel-difference limit.
Do not reproduce C2 fake drive gear/cruise enable, forced CAN validity, global
ECU defaults or its unqualified feedback torque conversion. The guide records
tunes/radar disposition. Receipt: sunnypilot/Ai/Evidence/retropilot-controller-20261103.json.

## 2026-11-03 — Preserve C2 explicit-selection compatibility

Map "RETROPILOT RETROFIT" to RETROPILOT_RETROFIT through the brand/shared
migration registry and selector normalization. Keep the current platform
explicitly selected, preserving other vehicles. C2's fakeIDs0..15 are not a
modern automatic fingerprint. Do not register unqualified ECU versions or
query configurations; modern FW discovery requires real database/config pairs.
Owner's saved settings are untouched; migration tests use temporary Params.

## 2026-11-03 — Keep file presence distinct from control/safety support

Explicit selection is sufficient for the current simulator monitoring stage;
no fabricated ECU firmware database. Existing host tests and noOutput request
do not qualify firmware safety. Retain the C2 hook as historical WIP and require
a reviewed modern policy enforced in the actual Chimera TX path, with compiled
safety tests, before active control. Documentation only; no runtime change.

## 2026-11-03 — Implement RetroPilot as its own modern car platform

Owner explicitly chose RetroPilot as the car and Chimera as Panda. Implement
in modern opendbc, preserve canonical DBC bytes and normal parser validity.
Use explicit selection, per-instance module observations and hostbus2. Keep
source/transport safety boundaries: noOutput/passive controller, no diagnostic
TX and unqualified speed scale0. Offline encoders do not enable hardware.
Do not inherit C2 calibration, fake drive gear/wheels or claim Chimera's legacy
USB/safety lifecycle matches modern Panda. Live profile/safety remains future
work. [Implementation](Knowledge/RETROPILOT_CAR_PORT.md).

## 2026-11-03 — Keep requirements separate from connection proof

Use the existing optical+CAN plan. A reachable Ethernet neighbor establishes
network adjacency only; no current game/mod/CAN compatibility is inferred.
Preserve strict SSH trust checks and recover trusted identity before remote
inspection. Full requirements and exact checks: Sessions/2026-11-03-beamng-requirements.md.
No new DBC IDs or actuator choice made in this requirements discussion.

## 2026-11-02 — Accept reference audit, keep runtime blocked

Preserve exact upstream source while fixing our inventory/verifier. Record
foreign test failures instead of changing current opendbc or loosening tests.
Curvature-to-position game control cannot validate the actual torque/custom
actuator chain; choose an explicit lateral validation contract before feedback.
Continue first with a sim-only camera/UI adapter. No installer, manager, model,
physical CAN or vehicle action is part of this audit.

## 2026-11-02 — Preserve the upstream BeamNG bundle before adaptation

Owner requested a folder with the needed BeamNG source. Keep it inside sim/
beamng_reference/upstream with source paths/bytes/modes, license and hash
manifest. Include supporting daemons/helpers/integration snapshots outside
upstream tools so the reference is useful. Shared base dependencies are mapped
rather than duplicating an entire fork. No active code/environment replacement;
foreign tests remain references, not current Sunnypilot behavior tests.

## 2026-11-02 — Use Caleb BeamNG source as a reference for a two-host sim adapter

Keep our current Sunnypilot/Radxa project and CD210 runtime. Study pinned
beampilot-drive5435d674 rather than replacing the port with that fork. Begin
with recorded/live PC frames to Q8B VisionIPC, then state/shadow planning and
game-only lateral feedback. Same-host source is not a tested network bridge;
steerpilot successor is presently unavailable via public404. No runtime mode,
physical protocol or control policy changed by this source-review decision.

## 2026-11-02 — Continue INT8 research with strict failure retained; reject W8A8 candidate

Owner explicitly approved retaining failed FP16 precision checks while proceeding
with research. Keep default strict gate unchanged; research path requires source,
independent same-precision checks and all500 own-state transitions. Fresh W8A8
executes on truev68/SoC37 but fails per-head heldout numerical acceptance. Do not
select it in modeld or call successful execution accuracy acceptance. Preserve
all artifacts/results and propose mixed activation/output precision with8-bit
weights; no guaranteed under0.5% recovery,200MB or latency claim. Historical
SoC39/model6fee results and accepted CD210GPU runtime remain distinct.

# Decisions and rationale

## 2026-11-02 — Stop camera work at accepted milestone

Owner accepts current camera bring-up/preview/benchmark. Keep temporary MM-X
profile and defer optimisation; later consult teacher camera/runtime evidence
to reduce latency with matched measurements. Do not automatically restart
camera work. Model/optical/vehicle qualification is not implied by acceptance.

## 2026-11-02 — Benchmark current UI without changing its pacing

Owner requested actual latency. Instrument EndDrawing only inside isolated
preview --benchmark mode, preserve normal30FPS pacing/automatic clock policies
and same-frame source metadata. Report draw-ready and host-call completion
separately; neither proves physical monitor presentation. No GPU fence or
FPS/clock optimisation introduced. Save raw first-display samples with warmup
and count repeated draws/publication gaps explicitly.

## 2026-11-02 — Preview camera through real onroad UI without manager

Owner wants live camera dashboard. Standard uiview starts model/DM/planner
processes, so provide camera-only launcher with existing onroad widget/HUD.
Synthetic ignition/started state stays in a unique private namespace. No
vehicle/control/model processes or fake calibrated geometry state. Closing
UI stops camera and restores settings. This is a preview, not dashcam recording
or a qualified full manager/model run.

## 2026-11-02 — Use temporary MM-X fixed intrinsics; defer calibration

Owner explicitly chose MM-X method now/change later. Use his720p/focal900
centred pinhole profile only in existing Q8B road-only test mode. This
supersedes prior no-runtime-choice/no-estimated-profile decisions for that
mode. Values are borrowed, not measured AK lens calibration. No distortion
profile, fabricated calibrated-status or vehicle-pose claim. Keep measurement
tools for later; no new automatic calibration implementation.

## 2026-11-02 — Separate lens-parameter source from mounting calibration

Checkerboard is the prepared tool's method, not a mandatory Sunnypilot target.
MM-X RK explicitly asks for external intrinsics; online pitch/yaw calibration
does not replace lens calibration. His900px focal value is not adopted for AK.
Alternative verified parameters/method remain open; no runtime choice made.

## 2026-11-01 — Search teacher evidence before asking the owner

Owner corrected the unnecessary IMU-model question: teacher already records
Adafruit LSM6DS3TR-C/I²C9/0x6a, prior ~102Hz raw testing and in-memory schema
smoke. Promote these facts/limits to student. Empty IIO scan is not evidence
against a userspace raw-I²C device. Ask only for unresolved/stale/conflicting
physical details after reading teacher sources. Keep initialb62481cc historical
factual finding and this correction; do not erase ledger history.

## 2026-11-01 — Prioritize non-camera hardware explanation/inventory

Owner said work on hardware and asked which sensor details Sunnypilot needs,
explicitly leaving cameras for later. First explain motion vs board-health vs
vehicle-feedback boundaries and inventory host interfaces read-only. Do not
start camera work, enable comma I²C/GPIO drivers unchanged, simulate missing
sensor health, open unidentified serial ports or change fan mode. Actual IMU
model/interface is unconfirmed; read-only thermal reporting is the first bounded
implementation candidate. This source study is not a tested sensor integration.

## 2026-11-01 — Persistent teacher/student workflow is the default

Owner explicitly asked for Agent Skills and REA on project changes and for
both memories to know where work stopped after shutdown/reopening. Store the
policy in project/workspace AGENTS, read HANDOFF at startup, reconcile live Git,
and update both memories at completed increments and closeout. Keep source-first
routing and actual evidence limits. This authorizes workflow/documentation, not
new runtime/hardware actions or upstream merges. Saved checkpoints do not claim
to recover unsaved work or complete knowledge of uninspected code.

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


## 2026-11-01 — Board identity authorized; generic Linux policy retained

The owner explicitly said "lets do this" for Ubuntu Linux, ARM64 and Radxa
Dragon Q8B and requested a README. Implement the proposed identity slice in the
protected clone, without auto-merging vendor. Keep PC policy true to preserve
existing Linux paths/services; add real board identity separately. Append enum8
without renumbering existing readers, and explicitly reject unconfigured Q8B
camera geometry. Hardware defaults are not health measurements. Camera/model/
sensor/actuator integration remains separate later work.

## 2026-11-01 — Workspace knowledge plus repository specialist memory

The owner asked for a folder inside Sunnypilot that remembers what we do and
learn here. Main `/home/radxa/comma/Ai/` remains the workspace coordinator.
`sunnypilot/Ai/` and protected-port `Ai/` expose one specialist notebook backed
by independent Git at `q8b/sunnypilot-memory`, branch `main`. Local links are
excluded from upstream Git; exact-path collision checks protect them during
daily updates. This preserves one history without placing port code in vendor.

Agents read and maintain the notebook using task-relevant skills. No separate
running AI, automatic knowledge completeness or background semantic review is
claimed. Source pins, evidence, coverage and uncertainty travel with each fact.

## Existing owner selections, retained

- Sunnypilot is the selected source for Q8B + custom steering; lateral is the
  main eventual goal. Fork recommendations were research, not road validation.
- Fresh stock source/assets are the new integration base; the previous custom
  Q8B model/runtime are separate preserved references.
- Daily updates advance only vendor; upstream integration into protected port
  requires discussion, including conflict-free merges. Notifications: next chat.
- Initial implementation milestone is camera/model/messages/native UI. Shared
  CAN interfaces use `/home/radxa/comma/retropilot/dbc/`; no repository audit or
  memory setup establishes actuator/vehicle compatibility.

Sources: [upstream policy](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_UPSTREAM_POLICY.md),
[workspace decisions](/home/radxa/comma/Ai/DECISIONS.md).

2026-11-01 — Owner requested a Linux-platform explanation before changes.
Generic Linux/ARM64 is already selected without /AGNOS. Record an explicit Q8B
hardware/backend design as future work; no flag, hardware class, launch profile,
dependency install or OS modification was authorized by this question.

2026-11-01 — MM-X is a reference, not an adopted patch set. Owner's new request
continues the explanation-before-change scope. Inspected backend/camera/process/
localization choices; implement only after owner instruction. Keep Linux/Q8B
runtime and real sensor contracts; no approval inferred for sensor bypasses,
fork switching, old schemas or MM-X delay/driver assumptions.

## 2026-11-02 — Measure AK lens; keep candidate separate from active geometry

Owner chose printable target and calibration tool after teacher-first lookup
found only a visual70degree estimate. Prepare exact-scale A4PDF/SVG and guided
capture/solve. Do not silently register guessed intrinsics or activate a profile
from lowRMSalone. Record optical/focus state and source images; current AF1and
physical lens/mount measurement remain unresolved. Keep Q8B guard active until
real data, distortion mapping and optical-state consistency are reviewed.

2026-11-02 — Owner selected already-convertedCD210 Thneed for GPU work.
Reuse/copy acceptedeb741641; do not convert again. Package required replay code
and assets inside Sunny; preserve original model and defaults while qualifying
backend. Current-history adapter reuses existing graph. [Session](Sessions/2026-11-02-thneed-import.md).

2026-11-02 — Use Q8B_THNEED=1 in road-only webcam mode for the copiedCD210 GPU
backend. Keep normal stock selection when off. Reuse pinnedCPU:LLVM warp after
NumPy rewrite failed one exact rounding-boundary pixel; keep exact gate.
Borrowed MM-X geometry remains invalid for model messages, even if extrinsics
alone appear calibrated. [Session](Sessions/2026-11-02-thneed-modeld.md).

2026-11-02 — Default Q8B Thneed to exact resident image preparation and road
camera to next-arrival selection after measured20Hz baseline. Keep original
CPU/cached flags0 for comparisons. Scoped max clocks mandatory for model starts;
owner's one-time setup already complete. Feature tensor splitting not attempted.
Rejected controls cannot advance image history; post-mutation errors require reset.

2026-11-02 — Adopt Q8B fast-cluster affinity4–7 for camera/model daemon workers,
intersecting caller restrictions; retain Q8B_FAST_CPU=0 for comparison. SingleCPU7
regressed this pipeline and is rejected. Keep saved failed timing results and
both passing fast-profile runs; do not extrapolate bench medians to all frames.

2026-11-02 — Put read-only Q8B diagnostic panel in the actual onroad view,
with alert overlays taking priority and Q8B_SHOW_STATS=0 opt-out. Reuse existing
customReservedRawData0 for namespaced/versioned Q8B timing packets only; review
allocation before another producer/fork uses it. UI timing means host first
draw, PWM means duty rather than RPM; unavailable/stale values stay unavailable.
Diagnostics never drive controls and send failure does not interrupt the model.

2026-11-02 — Owner approved continuing INT8 research with the failed strict
FP16 prequant diagnostic retained. Keep strict mode as the default. Separate
research mode requires pinned bitwise same-precision graph comparisons, full
native-input hashes and independently replayed recurrent provenance. This is
permission for quantization research, not model/vehicle acceptance. QAIRT2.37
PTQ uses generic HTP because SC8280XP/SC8280X strings are rejected; context
compilation must separately establish target v68/SoC37 support.

## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Use optical monitor capture on Radxa and physical CAN through Waveshare/Chimera for the simulator. This owner-selected architecture supersedes the prior network-image plan. Keep final controller CAN in the test path; stage physical bench actuation later. DBC additions must be canonical/versioned, and physical feedback authority remains unresolved.

2026-11-04: owner requested audit/save, GitHub update and ordered PC→VSCode→Radxa shutdown, with Chimera focus starting November5. Implementation choice under that publication request: show radxa/q8b by default so project status is visible; preserve original master and all history. Verified by API/refs/fresh source downloads. Next-session focus does not authorize arbitrary firmware flashing or physical actuation; normal session cleanup respects prompts/inhibitors.
