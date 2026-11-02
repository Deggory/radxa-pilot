# Run openpilot with webcam on PC

For lens measurement, use the [printable target and calibration guide](CALIBRATION.md).
The Q8B path now uses the current model's padded NV12 layout: stride1280,
UVoffset942080,allocation2220032bytes for visible1280×720. The earlier tightly
packed camera-only test is historical; model-facing layout is checked separately.

## Radxa Q8B: one road-facing AK-Camera (experimental capture only)

### Open the Sunnypilot camera dashboard

With the native helper/Params library and Python UI dependencies available,
run from the Sunnypilot project root:

```bash
cd ~/comma/sunnypilot
.venv/bin/python -m openpilot.system.camerad.webcam.preview
```

This opens Sunnypilot's actual onroad view/HUD with live road-camera video.
It starts only the camera publisher and UI, with private messaging/temporary
parameters and synthetic UI-only started/ignition state. No vehicle interface,
model, planners, driver-monitoring, control or recording processes are started.
Speed readouts are demonstration defaults, not measured vehicle data. Close
the window or press Ctrl+C in its launcher to stop; camera settings are restored.
Logs/process IDs/results are saved in the printed session directory under /tmp.
The standard full manager and legacy tools/scripts/uiview.py are separate paths.

For a bounded check, add `--seconds 10 --log-dir /tmp/q8b-ui-check`.
Optional `--screenshot /tmp/q8b-ui-check.png` saves after40distinct camera frames.
The default preview does not install calibration or start inference. Add
`--model` for the opt-in existing CD210 Thneed predictions; see the
[model launch guide and timing boundaries](../../../selfdrive/modeld/thneed_q8b/README.md).
Measured optics remain unqualified.

To benchmark capture-to-UI timing with normal system clock governors:

```bash
.venv/bin/python -m openpilot.system.camerad.webcam.preview \
  --benchmark --seconds 65 --warmup-seconds 5 --log-dir /tmp/q8b-ui-benchmark
```

Leave the window open until it closes automatically. The first5seconds are
retained as warmup but excluded from statistics. Every newly displayed frame
is matched by buffer/IPC frame ID to its actual monotonic V4L2 timestamp.
`timings.jsonl` preserves raw timestamps; `benchmark.json` reports median,
p95,p99,max, fresh-frame cadence, repeated draws and skipped publication IDs.
It records the actual GL renderer and window size. No clock/fan changes, GPU
fences, screenshot or video recording are added by the benchmark itself.

Two endpoints are reported: capture to draw commands ready, and capture to
host Raylib EndDrawing return. The latter includes the normal30FPS frame
pacing and display submission path; it is not a GPU-completion fence, confirmed
compositor presentation, monitor scanout or physical exposure-to-screen-light
measurement. Only the first completion of each new camera frame is sampled;
repeated redraws are counted separately. An early close is marked incomplete.
Raw timings are written after the run to avoid per-frame disk writes.

The current development .venv uses the pinned raylib6.0.0.1.post103 desktop
wheel and freshly compiled libparams_c.so. Its .pth also reuses existing bench
Python dependencies and matching project submodules; it is not a standalone
deployment environment. Normal build/installation of project dependencies
is still required when deploying this folder elsewhere.

### Capture profile

Temporary geometry, selected by the owner2026-11-02: this mode uses MM-X's RK
road profile,1280x720 with fx=fy=900pixels and centre(640,360). It is borrowed
from master-rk3588 at3ad69b20, not measured AK-Camera calibration. Current model
and UI use the same get_device_camera_config lookup; no separate ui.h edit is
needed in this source version. Only the narrow road camera is configured.
Outside USE_WEBCAM=1 Q8B_ROAD_ONLY=1, Q8B geometry remains unconfigured.
Automatic/checkerboard calibration work is deferred; prepared tools remain.
No lens distortion correction or measured mounting pose is supplied by this
temporary profile. Calibration status/online alignment logic are unchanged.

Owner-approved profile: SunplusIT AK-Camera JV, MJPEG1280×720 at60FPS capture,
latest-frame publication at20Hz. No driver/wide camera is opened. This is an
opt-in capture/process adaptation; model runtime and Q8B calibration are separate
and remain unqualified. Do not use the general driving instructions below as
proof this Q8B port is ready to engage.

Build the native UVC helper from the project root with the normal build:

```bash
scons openpilot/system/camerad/webcam/libuvc_capture.so
```

For isolated camera work without building the complete project, the same helper
can be built with the system C compiler:

```bash
cc -std=gnu11 -O2 -Wall -Wextra -Werror -fPIC -shared \
  openpilot/system/camerad/webcam/native_capture.c \
  -o openpilot/system/camerad/webcam/libuvc_capture.so
```

With NumPy, OpenCV Python bindings (`cv2`) and the project's normal Python/
messaging dependencies built, start only the
camera publisher (this command does not start the manager, model or vehicle
controls):

```bash
USE_WEBCAM=1 Q8B_ROAD_ONLY=1 python -m openpilot.system.camerad.webcam.camerad
```

The mode is accepted only on the detected Q8B. It defaults to the stable
`/dev/v4l/by-id/usb-SunplusIT_Inc_AK-Camera_JV-video-index0` path.
`ROAD_CAM`/`NARROW_ROAD_CAM` can override this with a full path or device number.
Unset `DRIVER_CAM` and `WIDE_CAM`; conflicting settings cause an explicit error.
When the manager uses these same flags, dmonitoringmodeld/dmonitoringd are
disabled; remaining driver-monitoring consumers/events have not been bypassed
or supplied with invented attentive-driver data. This is not full-stack readiness.

Images are not rotated by default. Set `ROAD_CAM_ROTATE_180=1` only if needed
for the installed orientation. The capture thread owns one latest compressed
JPEG, decodes selected frames and converts them to NV12. Mode negotiation must
match720p60; invalid/stale frames and capture failures stop publication. Source
sequence is preserved in frameIdSensor while frameId counts20Hz publications.
One monotonic V4L2 driver timestamp is used for both IPC timestamp fields and
camera-state fields; these are not separate measured exposure SOF/EOF times.
The AK-Camera's dynamic-framerate control is temporarily disabled, matching the
earlier fixed-camera-fps tests: automatic exposure must not silently slow the
60FPS source in low light. Ctrl+C/normal manager stop closes capture and restores
prior format/rate and that control where the device is still available. Shutter,
gain, focus, fan and performance-clock settings are not set by this mode.

Native helper provenance: adapted from workspace q8b/gpu_webcam/capture.c and
camera.py/latest_camera.py at legacy5a8fd13; the camera/model benchmark evidence
predates this integration. Required runtime source stays inside this project.
Earlier standalone720p60/20Hz results do not qualify this new publisher/model
pipeline or establish measured intrinsics. The Q8B calibration guard remains
active outside the explicitly selected road-only test mode.

## Setup openpilot
- Follow [this readme](/tools/README.md) to install and build the requirements

## Connect the hardware
- Connect the camera first
- Connect your computer to panda

## GO

```
USE_WEBCAM=1 openpilot/system/manager/manager.py
```
- Start the car, then the UI should show the road webcam's view
- Adjust and secure the webcam
- Finish calibration and engage!

## Specify Cameras

Use the `ROAD_CAM` (default 0) and optional `DRIVER_CAM`, `WIDE_CAM` environment variables to specify which camera is which (ie. `ROAD_CAM=1` uses `/dev/video1`, on Ubuntu, for the road camera):
```
USE_WEBCAM=1 ROAD_CAM=1 openpilot/system/manager/manager.py
```
