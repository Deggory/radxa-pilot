# Current webcam camera path

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
