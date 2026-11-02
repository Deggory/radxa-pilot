# Current webcam camera path

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
