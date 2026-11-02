# Automatic intrinsic/extrinsic calibration options — 2026-11-02

Owner wants automatic intrinsics and extrinsics and asks how to achieve them.
This increment explains options; it does not implement or launch calibration.
Project starts clean on radxa/q8b at c67cb57bf53a16bd3b90b3e4806e232c77e6fbec.

Recommended workflow for the single AK road camera:

1. Keep the operational720p mode/crop/orientation and optical state consistent.
   Continuous autofocus was last observed enabled; a repeatable working focus
   needs review. No focus setting was changed by this advice.
2. Intrinsics: a guided collector could automatically select sharp, distinct
   target observations with varied position, distance and tilt, then solve K
   and distortion and report uncertainty/error/held-out validation. Physical
   target motion remains a human action. Existing checkerboard tool already
   detects and solves, but capture saves only on Space; no autosave added.
3. Vehicle extrinsics: after fixing the camera in its mount, establish a known
   target pose relative to the vehicle coordinate frame, with measured scale,
   orientation and position. solvePnP yields object-to-camera R/t; combine with
   the known target-to-vehicle transform using explicit inversion/frame/unit
   conventions. A freely moved target's per-image pose is not vehicle mounting.
   Level-ground alignment and known target pose are measurement requirements,
   not automatic discoveries. Export/review would be a new implementation.
4. Later online calibration can update pitch/yaw alignment once actual current
   model/odometry and vehicle inputs work. Current calibrationd assumes zero
   roll and has model-derived height state; it does not solve lens K/distortion
   or full independent6DOF camera-to-car pose. Q8B runtime remains unqualified.

Target-free option: COLMAP estimates/refines intrinsics and relative poses from
overlapping natural-scene images and shared intrinsics. Its official FAQ warns
of degenerate solutions and normally fixes principal point initially. This is
an offline candidate/research option, not a tested Q8B road-camera calibrator;
it does not by itself establish vehicle-frame alignment/metric position. Do not
claim patternless estimation is impossible or guaranteed from arbitrary video.

GMLC: MM-X's RK README names external GMLCCalibration, not an integrated online
solver. Original GML site URLs could not be fetched on2026-11-02; package
availability/current ARM64 support unverified. No download/install attempted.
Kyushu's primary project page documents a GML-derived projector calibration
tool using printed patterns; that is not proof of every original GML feature.

Primary sources checked2026-11-02:

- [OpenCV calibration](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html): K, distortion and per-view extrinsics.
- [OpenCV PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html): object-to-camera R/t, not automatic vehicle frame.
- [COLMAP FAQ](https://colmap.github.io/faq.html#fix-intrinsics): self-calibration refinement, degeneracy and principal-point limits.
- [Kyushu GML-derived tool](https://www.cvg.ait.kyushu-u.ac.jp/research/projcalib2.html): printed-pattern workflow for its projector extension.

Local source: webcam/calibrate.py solve discards per-view_rvecs/tvecs and writes
candidate_not_installed with mounted_orientation_calibrated=false; capture uses
Space. locationd/calibrationd.py observed_rpy starts with zero roll and consumes
cameraOdometry/carState. No automatic vehicle-pose implementation exists here.

Skills: source-driven-development, documentation-and-adrs and Git workflow.
Source-first rg/selected reads and primary web documentation used; unrelated
REA binary/runtime providers not needed. No camera/model test or hardware write.
Stock model65a08adc,tinygrad92b742f7,msgqe7396e76 and runtime source unchanged.
Next: explain target-assisted automation versus target-free estimation and
resolve owner's preferred scope before a new runtime patch. Prepared target
remains available; actual AK intrinsics/mount and model backend remain open.

Validation:44notebook documents/97relative links/8source repos/4252index entries
pass; diff whitespace/scope checks pass. Local source confirms Space capture,
discarded per-view R/t and zero-roll online update. No runtime tests rerun.
