# Current webcam camera path

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

## Implemented opt-in road capture — 2026-11-02

Owner approved the explicit60FPS-capture/20Hz-publication road-only proposal.
Actual camera: SunplusIT AK-Camera JV at stable
`/dev/v4l/by-id/usb-SunplusIT_Inc_AK-Camera_JV-video-index0` (currently video2).
Read-only current enumeration confirms MJPG720p60/30; uncompressed720p is10FPS.
Earlier standalone AK evidence includes600camera frames at59.64FPS and the
Oct31Thneed20minute soak at20.000014modelHz/estimated59.648sourceHz. Those are
different model/runtime tests, not evidence for current managed Sunny.

The new RoadCamera in webcam/camera.py uses native_capture.py/native_capture.c,
a single owned latest JPEG, checked NV12 conversion and real monotonic V4L2
timestamps. Capture mode must negotiate720p60; stale/malformed/disconnected
data fail explicitly. Config.py scopes this to detected Q8B plus USE_WEBCAM and
Q8B_ROAD_ONLY=1; rejects extra camera settings. ROAD_CAM_ROTATE_180 defaults0.
Webcam/camerad.py declares only narrowRoadCameraState/one VisionIPC stream and
preserves source sequence in frameIdSensor with sequential20Hz frameId. The
same driver timestamp fills both SOF/EOF fields, not separate exposure timings.
Process_config defers both driver-camera processes in this opt-in mode, without
fabricated driver status or global safety-event suppression. Other modes retain
their prior selection. Native helper has a SCons target and lives inside project.

Actual live probe first found negotiated60but delivered~23.97sourceHz when the
camera's dynamic-framerate control was1. Added the same temporary fixed-cadence
control as prior tests; restore its old value after stopping. Final140matched
IPC/Cereal frames show19.973Hz publication/59.642Hz source sequence, exactly one
stream,1280×720stride1280/UVoffset921600/1382400bytes. Driver timestamp→receiver
median40.244ms/max62.580ms, not exposure latency or inference time. Publisher
exit0; prior1080p30mode and dynamic-framerate1 restored. No process left holding
camera.21focused tests pass (10camera+11identity), strict C/SCons helper build
and pinned msgq bindings build. Model and calibration unchanged/unqualified.

Earlier source-map details below describe the generic original webcam path;
the opt-in RoadCamera above now supplies the Q8B path. Next qualify geometry/
current model input and runtime separately, not a full manager launch by default.

Source baseline4585e13954ce3172ece9756b66bc3b8a6de11625, radxa/q8b,
Sunny2026.003.000/COMMA0.11.3. Owner selected cameras on2026-11-02 and deferred
hardware-setting implementation. This is source inspection, not tested capture.

| File relative to project | Responsibility |
| --- | --- |
| openpilot/system/camerad/webcam/camera.py | Camera class opens OpenCV VideoCapture; reads frames, rotates180degrees, converts BGR to NV12 through PyAV |
| openpilot/system/camerad/webcam/camerad.py | Selects /dev/video nodes from ROAD_CAM/NARROW_ROAD_CAM, WIDE_CAM, DRIVER_CAM; creates VisionIPC buffers and publishes camera state/frame messages |
| openpilot/system/manager/process_config.py | USE_WEBCAM selects webcamerad versus native camerad; also affects driver monitoring gates |
| openpilot/common/transformations/camera.py | Device camera geometry/intrinsics lookup; Q8B currently explicitly unconfigured |
| openpilot/system/camerad/main.cc and cameras/camera_qcom2.cc | Native comma Qualcomm camera path; different from USB webcam capture |

Start with camera.py for physical capture and camerad.py for connecting frames
to Sunnypilot. Current camera.py requests1280x720/25fps; publisher paces20Hz and
uses frame_id-derived timestamps. These are existing assumptions, not our
measured Q8B camera capabilities. Actual accepted capture mode, rotation,
timestamp origin, geometry and current message/buffer contracts need review.
No arbitrary comma calibration or wholesale MM-X camera patch adoption.

Next recover teacher's actual camera/capture evidence before asking owner for
known hardware details. Adapt only a bounded agreed camera slice; separately
qualify model backend/current model inputs before claiming end-to-end operation.
No camera opened, services started, runtime/model or application code changed
by this file-map explanation. Incomplete hardware tasks remain saved for later.

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

2026-11-02 preparation complete: [calibration guide](../../openpilot/system/camerad/webcam/CALIBRATION.md)
contains exact print/capture/solve workflow and fixed quality gates. Target PDF/
SVG are checked in; candidate data never activate themselves.29focused tests
and synthetic Tk/PDF checks pass; actual printed-target collection still pending.
