# Work status and next task

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
