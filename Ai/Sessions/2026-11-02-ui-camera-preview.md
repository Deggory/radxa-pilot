# Live Sunnypilot camera dashboard — 2026-11-02

Owner asked to open Sunnypilot UI in dashboard/dashcam-style mode and see the
camera output. Started from clean radxa/q8b at5de4f3e52b93b037e260ba493013e0db23bb7dfc.

Added openpilot/system/camerad/webcam/preview.py and test_preview.py. Controller
starts only camera publisher and UI child. UI is the real Sunnypilot standard
onroad AugmentedRoadView/HUD with BIG=1,30FPS desktop window, native camera
textures and the shared temporary MM-X geometry. It is not the full home/
settings/manager flow. Existing tools/scripts/uiview.py starts model/DM/planners
and was not used. Synthetic UI-only device started/ignition state and passive
mock CarParams are isolated by a random OPENPILOT_PREFIX and temporary Params.
No terms/training acceptance, normal vehicle parameters or global mode changed.
No model, vehicle interface, planners, controls, DM or recording started. HUD
speed is a default, not measured motion. No fabricated calibrated-status data.

Window close/launcher Ctrl+C/SIGTERM stops owned children, reaps them and removes
private messaging/socket/Params files. Camera retains existing720pMJPG60capture/
latest20Hz publisher and restores prior format/rate/dynamic-framerate on close.
Fixed-size frame counters avoid unbounded memory growth while left open. Logs,
process IDs, rendered-frame summary and child exit codes are retained per run.

Built ignored openpilot/common/libparams_c.so directly from current Params,
util and swaglog source, against pinned json11/zeromq and matching generated
schema/Cap'n Proto headers, with __RADXA_Q8B__. Initial include-path errors
resolved using actual generated-header locations, without source suppression.
Installed lock-pinned comma-deps-raylib6.0.0.1.post103 desktop wheel into new
project .venv; exact wheelSHA256 d9b9bebb39167442bacf627958d57ae95e452550ced1b68337cbf2a73375856a
verified. Slow download completed with ranged reads and whole-file hash check.
Other selected dependency versions come from uv.lock; environment list saved.
Development .pth reuses existing bench Python packages, helper dependencies
and project submodules. Legacy environment untouched. This is not a portable
deployment environment; normal project dependencies need installation elsewhere.

Verification:

-32focused preview/calibration/camera/identity tests and Ruff pass.
-Live9.063s native window:173distinct camera frames, IDs12..190; screenshot
 saved and visually inspected with actual desk-camera video and Sunnypilot HUD.
-Final lifecycle check4.043s:79frames, IDs9..87, camera/UI exit0/0.
-Prior1920x1080MJPG30/dynamic-framerate1 restored exactly after bounded runs.
-First10s run displayed193frames but TakeScreenshot rejected an absolute path;
 raw log/result retained, screenshot_saved=true there was inaccurate. Corrected
 to relative path and actual file existence check; live-verified.png is evidence.
-No camera owner remains after bounded tests. Owner-facing persistent preview
 is reopened separately and its actual process IDs/log path recorded at closeout.

Changed active source stays in sunnypilot. README/root readme and both memory
layers updated. Optional report:workspace Ai/Reports/sunnypilot-ui-preview-20261102;
download manifest:q8b/tools/q8b-ui-deps-20261102/manifest.json. Current upstream
referencea86979d2 unchanged; no merge. Stock ONNX65a08adc, tinygrad92b742f7,
msgqe7396e76 and temporary MM-X720p/focal900 profile unchanged. No model/Adreno
inference, optical/mount/vehicle or full-manager qualification. No performance
clock/fan/shutter/gain/focus changes by launcher; temporary camera cadence
control follows the existing approved capture path.

Skills used: incremental implementation, Git workflow, debugging/error recovery,
code review, source-first development, documentation and observability. Read
local actual UI/process/msgq/native Params source and exact package artifacts;
real runtime/screenshot evidence collected. No unrelated REA binary analysis
was needed or claimed. Next use live preview; current model/Adreno integration
remains next engineering task, automatic calibration remains deferred.

## Owner preview closed normally — 2026-11-02

UI implementation536470bd4fe9ab9abb68f9af9320ee8b315aecd2 is committed.
Owner-facing session controller12416/camera12417/UI12418 displayed849distinct
camera frames over42.917s, then exited normally0/0; closure cause unconfirmed.
No preview process remains. Prior1080p30MJPG/dynamic-framerate1 restored exactly.
Reopen from Sunnypilot root with
`.venv/bin/python -m openpilot.system.camerad.webcam.preview`.
No model/vehicle processes started; automatic calibration remains deferred.

Validation manifest creation initially stopped on the now-closed process check;
regenerated against actual completed-session logs/restoration and attached to
the implementation journal. Do not claim the UI is still running.

Live preview reopened in persistent terminal session21631: controller12790,
camera12793,UI12794; prefixq8b_preview_97ce0a9e4384. Actual screenshot
owner-persistent.png verified and child PIDs alive. Logs:workspace
Ai/Reports/sunnypilot-ui-preview-20261102/owner-persistent. This supersedes the
previous closed-session state. Window intentionally open; close it to stop
camera/restore settings. Check current PIDs before later camera work.

## 2026-11-02 — Assessment of temporary intrinsics

Current borrowed K:fx=fy900,cx640,cy360 at1280x720. Pinhole calculation gives
HFOV70.834deg/VFOV43.603deg, not a physical measurement. Consistent with old
70deg visual estimate, but that estimate cannot validate K. Actual principal
point, separate focal lengths and lens distortion remain unmeasured. Existing
UI video success verifies capture/display, not geometric calibration or model
warp/lateral accuracy. Keep provisional profile as owner chose; automatic
calibration stays deferred. No runtime/optical changes or new camera test.
Source:current camera.py, onroad camera projection and OpenCV4.13calib3d docs.
Next model/runtime qualification can use this explicit estimate; actual lens
validation remains required before judging lateral geometry/performance.

2026-11-02 intrinsics assessment: temporary900px/720p implies70.834deg
horizontal FOV under a pinhole assumption; old70deg was only visual. Camera/UI
video is verified, lens geometry is not. Keep owner-selected temporary profile;
no automatic calibration resumed. Persistent preview12790/12793/12794 has now
closed normally:1514distinct frames/76.200s, child exits0/0; no relaunch requested.

Source-driven/documentation/Git skills; source-first inspection and primary
OpenCV docs. No unrelated REA binary analysis needed. New checks: FOV arithmetic
and notebook/diff validation only; no runtime tests rerun. Runtime/model pins
unchanged from91ded2e.

## 2026-11-02 — Camera-to-UI timing: cadence versus latency

Latest actual Sunnypilot dashboard rendered1514distinct frames in76.200078s:
19.868746new frames/s, mean50.3303ms/new frame. These are application display
cadence statistics, not camera-to-screen delay. preview.py saves frame count/
IDs/duration, not paired capture/render/swap timestamps, so latest-run latency
cannot be recovered from its saved summary. No new runtime measurement made.

Separate Oct31 standalone Thneed/EGL/max-clock source db5b0da reported driver
stamp to host EGL draw/swap return median42.186ms,p9556.996ms. It includes an
older model/runtime/UI and does not qualify current Sunnypilot latency or true
optical capture-to-monitor-light latency. Exact current delay needs per-frame
paired capture/render/presentation evidence. Keep this distinction in replies;
no optimisation or new camera launch requested by the timing question.

Performance skill: measure before claiming optimisation. Source-first saved
JSON/report/current preview source only; no unrelated REA binary analysis.
Runtime/model/temporary intrinsics unchanged at6c834514; preview stays closed.
