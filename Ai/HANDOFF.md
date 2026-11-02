# Resume Sunnypilot here

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
