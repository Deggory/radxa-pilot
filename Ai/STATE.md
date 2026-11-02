# Current Sunnypilot state

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

2026-11-02 next-step advice: recommend current stock model/Adreno
qualification, first one isolated inference/CPU parity, then camera20Hz/modelV2
and UI overlay. Planning only, not started; camera optimisation remains deferred.

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

2026-11-02 latest: padded model-facing NV12 fixed in6fea7ecf; real140frames and
synthetic current CPU-warp input parity qualified, not full inference. Printable
A4target and target/capture/solve calibration tool ready. Real lens/focus/mount
measurements remain pending; no automatic geometry registration. See HANDOFF.

2026-11-02 accepted camera increment: opt-in Q8B road-only AK720pMJPG60capture,
latest20HzNV12/IPC/messages, real driver timestamps and source sequence, optional
rotation(defaultoff), deferred driver camera.21tests plus140actual frame pairs
pass, helper/msgq build and settings restoration verified. Model/calibration
unchanged; full managed stack unqualified. See HANDOFF and latest session.

Current scope2026-11-02: camera work selected, hardware settings deferred.
Webcam source path identified; no capture/model run or application edit.
See [HANDOFF](HANDOFF.md) and [camera path](Knowledge/CAMERA_PATH.md). Older
camera-deferred/H1-next statements below are superseded for current work.

## End-of-day checkpoint — 2026-11-01

Owner finishing work and requested shutdown after audit. Resume2026-11-02 with
H1 real read-only thermal provider, following [handoff](HANDOFF.md) and
[hardware checklist](../tasks/todo.md). Planning baseline2963025 clean; fresh
11identity tests and notebook/index checks passed. Hardware implementation
remains pending; camera work deferred. See shutdown session for exact limits.

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


## 2026-11-01 — Q8B identity implemented and checked

Owner authorized Ubuntu/Linux, ARM64 and Radxa Dragon Q8B identification.
Protected `radxa/q8b` commit `12e44feeff241334e184c86dc9daccdc7f9e4fa1` implements exact device-tree detection,
Python/C++ HardwareRadxa and local cereal enum `radxaQ8b @8`, preserving existing
ordinals and generic Linux `aarch64`, `COMMA_HARDWARE=False`, `PC=True` policy.
The read-only command reports actual Ubuntu24.04.5/ARM64/RadxaDragonQ8B. Dynamic
camera consumers explicitly reject missing Radxa calibration. No comma camera
calibration is claimed for this board.

11 Python tests, 4 actual C++→Python deviceState/initData message checks, SCons
profile detection, Ruff, syntax and diff checks passed. A detection mutation
was rejected by the tests. No full Sunnypilot build, camera/model/UI launch,
MSM runtime integration, hardware-health measurement or vehicle actuation was
performed. Generic hardware defaults remain unimplemented health providers.
Vendor stays clean at a86979d2; no upstream merge/push.

[What we did](/home/radxa/comma/q8b/sunnypilot-radxa/readme_wat_we_did.md) ·
[Evidence](/home/radxa/comma/Ai/Reports/radxa-board-identity-20261101/REPORT.md).

Recorded 2026-11-01. Live Git and the upstream inbox take precedence over this
snapshot; refresh affected topics when source changes.

| Item | Recorded identity / status |
| --- | --- |
| Upstream reference q8b/sunnypilot-upstream | `a86979d2b2b176413a7f3e5cccf8c807596a7def`, `master`; advanced from `6f7a2c94` during the 17:10 UTC deployment check |
| Source headers | Sunnypilot `2026.003.000`, COMMA `0.11.3` |
| Observed host, 2026-11-01 | Ubuntu24.04.5LTS / Linux7.0.11-6-qcom / aarch64; exact DT Q8B token; protected port selects HardwareRadxa with generic Linux PC policy |
| Protected development | `sunnypilot`, `radxa/q8b`; identity implementation HEAD `12e44feeff241334e184c86dc9daccdc7f9e4fa1`; initial workflow HEAD `824be91b` |
| Stock model | SHA256 `65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce` |
| Stock checkout validation | Prior clean-start evidence verified 286 LFS assets and seven submodule pins; not a runtime test |
| Archived Q8B work | `q8b/preserved-sunnypilot-20261101`; old source/model/patched Adreno runtime retained separately |
| Legacy model | SHA256 `659727c4d4839adc4992a254409a54259a8756a743f2d567bf5fdc6579f8009b`; not the fresh stock model |
| Legacy worker | `q8b/gpu_webcam`, `radxa/legacy`, `5a8fd13ba0b252091d7448017537e798144aa0ba`; frozen helper imports |
| Daily vendor workflow | 15:30 UTC persistent user timer; only vendor advances, port and notebook remain protected |
| Managed Sunnypilot on Q8B | Identity implemented and focused checks passed; managed runtime remains unqualified, stock-contract preflight next |

Completed knowledge work: source/version/fork selection, fresh stock checkout
and preservation, daily commit tracking, system-folder source map, and this
specialist notebook. The latest source index pins actual superproject and
dependency trees; its coverage is navigation, not full code review.

Key findings: actual services live under `openpilot/system`; root `system` is
only an AGNOS-manifest compatibility link. Hardware selection lives under
`common/hardware`; vendor defaults to PC without `/AGNOS`, while our protected
port now selects HardwareRadxa on the exact Q8B device-tree token. Webcam selection does
not enable our MSM Adreno runtime. Live sensors, native UI, lifecycle and the
new stock model contract still need integration and tests.

Latest upstream delta: a86979d2 changes only Sunnylink visual-setting metadata
to hide the Steering Arc toggle on `mici` (comma four). It does not change the
lateral model/controller. Inspected and explained; not merged into the protected
port. The notebook's original source-index pin became stale after the real
update and was refreshed; the historical system review remains pinned to6f7.
