# AK-Camera lens calibration

The checkerboard below is this tool's measurement method. Sunnypilot does not
require a particular printed target: verified manufacturer intrinsics matching
the camera mode and focus, or another suitable calibration method, can also
supply lens parameters. MM-X's RK branch asks for externally obtained intrinsics
and stores fixed values; its online mounting calibration does not solve the lens.

This tool measures a lens-calibration candidate, not vehicle mounting angles or
camera height. The saved70°FOV/zero-angle/1.22msettings were a visual estimate.
They are not installed as measured Q8B intrinsics. The Q8B calibration guard
stays active until real data and the required distortion/warp integration are
reviewed. No automatic installation or fabricated driver-monitoring data.

## 1. Print and check the target

For automatic collection and vehicle extrinsics, see the proposed workflow in
[the notebook session](../../../../Ai/Sessions/2026-11-02-automatic-calibration-options.md).
Current capture still requires Space; automatic frame selection and vehicle-pose
export are not implemented. OpenCV's per-image target poses are not automatically
camera-to-vehicle extrinsics: the target's pose in the vehicle frame must be known.

Print [the A4 landscape PDF](calibration/ak-checkerboard-a4.pdf) at **100% / actual
size**, without fit-to-page. The [SVG](calibration/ak-checkerboard-a4.svg) is an
editable vector alternative. Mount the sheet flat on a rigid backing. Measure
the100mmruler and a square: nominal square side is25mm. Enter the actual printed
square size in the solve command. Do not calibrate from a bent sheet or assume
the printer used the requested scale.

Target:10×7squares,9×6internal corners. It is deliberately non-square to avoid
row/column ambiguity. The script can generate another copy with
`python -m openpilot.system.camerad.webcam.calibrate target --directory NEW_FOLDER`.

## 2. Collect images on Q8B

Use the project Python environment with NumPy, OpenCV, Tk/Pillow and the native
camera helper built as described in [README](README.md). Stop other camera
owners first. From the sunnypilot root:

```bash
python -m openpilot.system.camerad.webcam.calibrate capture \
  --directory camera-calibration/ak-session-01 --samples 24
```

The preview uses the actual720pMJPG60AK-Camera and a latest-frame reader. Press
**Space** to save a complete detected grid; **Escape/Finish** stops. It rejects
nearly identical views. Move the target across the image, tilt it in both axes
and vary distance while keeping the whole board clear, sharp and visible.
Each saved image stays full resolution, with source timestamp/sequence/hash in
manifest.json. Close normally to restore frame-rate settings. Camera controls
and orientation are recorded; existing folders are not overwritten.

The camera currently reports continuous autofocus enabled. Reliable intrinsics
need a consistent optical state. This tool records that setting and visibly
marks it provisional; it does not silently change focus. Fixed-focus capture
and the focus state used later by Sunnypilot need review before activation.
Low reprojection error alone cannot establish lens/road accuracy.

## 3. Solve offline and review

With the measured printed square side (example25mm):

```bash
python -m openpilot.system.camerad.webcam.calibrate solve \
  --directory camera-calibration/ak-session-01 --square-mm 25 \
  --output camera-calibration/ak-session-01/candidate.json
```

The solver verifies image hashes/profile/resolution and redetects the corners.
It requires at least12views and target-center coverage of at least15%of both
image dimensions. Candidate gates: finite positive focal lengths/plausible
principal point, overall RMS≤1pixel and each view RMS≤1.5pixels. Failed data
are rejected; no views are silently deleted to improve the score. Output includes
full3×3K, five distortion coefficients, per-view errors, parameter uncertainty,
input hashes, capture profile and explicit `candidate_not_installed` status.
Minimum-count/coverage/error gates are useful checks, not full optical validation.

Review saved images, per-view reprojection errors, focus stability and distortion/field coverage
and a separate held-out capture before installing a profile. Lens distortion
must be handled consistently before using the current pinhole warp. Vehicle
mounting orientation/height is a separate later calibration.

OpenCV primary sources: [calibration workflow](https://docs.opencv.org/doc/doxygen/html/d4/d94/tutorial_camera_calibration.html),
[calibrateCameraExtended and distortion model](https://docs.opencv.org/4.11.0/d9/d0c/group__calib3d.html).

## Current model-buffer boundary

The road-only publisher uses the same get_nv12_info layout as current modeld:
1280×720visible, stride1280, Yrows736, UVrows368, UVoffset942080,
allocation2,220,032bytes. Modeld copies the first1,413,120bytes and derives two
logical model views from the one physical road camera. Current ONNX new_img is
uint8[2,6,128,256]. Buffer/CPU-warp tests do not establish Q8B GPU execution,
correct real-world calibration or full model/UI operation.
