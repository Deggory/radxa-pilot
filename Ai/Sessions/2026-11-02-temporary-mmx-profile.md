# Temporary MM-X camera profile — 2026-11-02

Owner decision: keep MM-X method for the time being, change later. This accepts
a temporary fixed camera profile and defers automatic/target calibration work.
Start: radxa/q8b at1c5c6b9d7c40ef5cfbbd580927b7812c8eb76ebe, clean.

Implemented in openpilot/common/transformations/camera.py: borrowed MM-X RK
1280x720/focal900 centred pinhole profile, only narrow road; cabin/wide absent.
get_device_camera_config selects it only for radxaQ8b/unknown in validated
Q8B_ROAD_ONLY mode with USE_WEBCAM and actual Q8B board detection. Reuses the
existing mode validator. Outside the mode, previous unconfigured guard remains.
No global PC/comma profile replacement. Main modeld, modeld_v2, offset helper
and current standard/mici Python UI all use this lookup. No old ui.h copied.

Profile is not measured AK-Camera calibration. No distortion correction or
measured vehicle pose supplied; no calibration-status/zero-roll policy changes
or fake DM data. Existing capture60/publication20Hz/native timestamp/padded
buffer paths preserved. Measurement target/tools retained for later. Do not
automatically resume calibration work contrary to this owner deferral.

MM-X source pin:3ad69b20b2c38172ea24c8388354ee95eca8412a (master-rk3588),
common/transformations/camera.py blob1fa8b6ad26f28cbd0223e15ef2d45f58ab3d5e01,
selfdrive/ui/ui.h blob384825de575f7bc508207936e39fbf3cd430a666. Reused exact
cached/verified readable source from q8b/research/mm-x-camera-20261102. His
README expects external calibration; borrowing900 does not reproduce a measured
calibration of our lens. See MM_X_LINUX_REFERENCE for primary source URLs.

Verification: first added scoped profile test failed at missing-calibration
guard as expected. After implementation, all30focused camera/calibration/
hardware identity tests pass. Projection/inverse, one-camera configuration,
other-sensor rejection, non-Q8B and missing-USE_WEBCAM rejection, default guard
and ordinary profiles checked. Ruff passes changed Python files. Reviewed
current model/UI call sites: shared lookup and narrow stream selection.
No physical camera/UI/inference/Adreno/vehicle run for this parameter change.
Report: optional workspace Ai/Reports/sunnypilot-mmx-profile-20261102.

Changed: common camera geometry/identity tests, webcam README/CALIBRATION guide,
root readme and student memory. Teacher resume/state/task and Sunny/camera repo
notes/session updated. Stock model65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce,
tinygrad92b742f711c7d216fd3ed7a46a30a959e3c43bd4 and
msgqe7396e76dadbb49e374d4b664ff6bbb43a39bcb0 unchanged. No upstream merge.

Skills: incremental-implementation, test-driven-development,
code-review-and-quality, source-driven-development, documentation/Git workflow.
Source-first rg and cached exact GitHub blobs; no unrelated REA artifact/runtime
analysis needed. Next qualify current model/Adreno runtime using explicitly
provisional geometry, with actual optics and mounting replacement still open.

Closeout: notebook verifier passes45documents/98relative links/8source repos/
4252index entries.5cached source blob identities reverified,5current shared
lookup consumer ASTs checked; lint and diff checks pass. No uncommitted owner
work at start; verified increment committed and validation journaled.
