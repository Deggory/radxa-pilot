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
