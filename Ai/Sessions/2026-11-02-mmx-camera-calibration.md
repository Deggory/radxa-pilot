# MM-X RK camera calibration — 2026-11-02

Request: inspect how MM-X configured RK3588 cameras without assuming he used
our checkerboard. Scope: reference research and documentation clarification.

Project start: radxa/q8b,d273823b4ae08eb51cce8042eea424b9dea062d9, clean.
MM-X master-rk3588 pin:3ad69b20b2c38172ea24c8388354ee95eca8412a.
Fetched5complete pinned files through GitHub plugin: common/transformations/
camera.py, selfdrive/ui/ui.h, tools/webcam/camera.py, tools/webcam/camerad.py,
selfdrive/locationd/calibrationd.py. Reused pinned RK README from prior cache.
5exact Git blob hashes matched;4Python AST parses passed.

README says obtain intrinsics with software such as GMLCCalibration, then edit
geometry and UI. Road K is fx=fy=900,cx=640,cy=360 for1280x720; PC uses that
configuration. MJPG capture requests1280x720/20FPS, publisher20Hz. Calibrator
consumes cameraOdometry/carState for mounting alignment; roll assumed zero.
No K/distortion solver there. Source does not establish how the author measured
900or which physical target he used. Do not say he calibrated automatically or
prove he never used a checkerboard.

Documentation now explains our target is one supported measurement method.
Verified manufacturer parameters matching mode/focus or another appropriate
method could be used. Saved70degree visual estimate remains an estimate, not
measured K. No alternative activated, no code removed, guard remains active.
Next resolve AK lens-parameter source; printing/capture is available, not a
mandatory next action. Actual optics/focus/mount and model backend stay open.

Changed project paths: Ai topic/handoff/state/tasks/worklog/validation/decisions/
this session; webcam/CALIBRATION.md. Teacher repo note/resume/state/current task
and this session updated. No runtime source, weights or settings changed.
Model65a08adc/current runtime and tinygrad92b742f7/msgqe7396e76 untouched.
No camera/model/vehicle run; prior29tests were not rerun for documentation.

Skills: source-driven-development, documentation-and-adrs,
git-workflow-and-versioning. Source-first rg/GitHub inspection; REA parsers or
runtime providers were not needed for readable source. Optional evidence:
q8b/research/mm-x-camera-20261102/{manifest,verification}.json and source/.
Notebook/link/diff checks and commit validation are recorded in the ledger at
closeout. No vehicle actuation, upstream merge or telemetry change.

Closeout: notebook verifier passes43documents/96relative links/8source repos/
4252indexed entries; git diff --check passes; only knowledge and calibration
guide changed. No runtime tests rerun. Source verification.json includes these
results; verified increment committed and attached to the maintenance ledger.
