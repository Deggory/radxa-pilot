# AK-Camera road-only patch — 2026-11-02

Starting4888c949c6b51ef8f83b9d1ac07409361f45939c/radxa/q8b, clean.
Sunny2026.003.000/COMMA0.11.3; stock model SHA256
65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce unchanged.
Teacher camera note, Sep20AK test, Oct31soak PASS and actual legacy capture
source were read first. Known camera is SunplusIT AK-Camera JV stable by-id
index0, currentlyvideo2; query confirms MJPG720p60/30 andYUYV720p10. Read-only
baseline1080pMJPG30/dynamic-framerate1. No new purchase/identity question needed.

Owner explicitly approved proposed patch through approval question:720pMJPG60
capture/newest20Hz publication, one road camera, driver processes deferred in
opt-in Q8B test mode, rotation configurable/defaultoff, real timestamps and
self-contained helper. No model/runtime or invented calibration changes.
Used incremental/TDD/source-first/debugging/review/documentation/Git skills;
readable source, real camera and actual IPC evidence, no REA claim invented.

Changed webcam camera.py/camerad.py, added config.py/native_capture.py/.c,
new21test suite(10camera+11existingidentity), SConscript helper target, manager
driver-camera gates, README and notebook. UVC helper adapted from legacy
q8b/gpu_webcam/capture.c/camera.py/latest_camera.py at5a8fd13. All required
capture source is inside sunnypilot; no runtime import of those references.
Direct helper compile and actual SConscript helper target pass; no full build.

Native handle saves/restores mode/rate; monotonic timestamps checked and JPEG
bytes owned before next capture. Single latest slot is drained continuously;
only selected frames decode to full720p NV12 at20Hz. Failed/malformed/stale
frames stop the publisher. frameIdSensor is source sequence, frameId is sequential
publication ID, one driver timestamp paired across IPC/Cereal SOF/EOF. Not
separately measured exposure times. Scope gates leave other platforms' original
selection intact; no invented attentiveness or broad safety-check bypass.

TDD initially failed on missing config. Fixed discovered native.so/Python-module
name collision by using libuvc_capture.so. Current checkout lacked compiled
messaging bindings; built pinned msgq e7396e76 using hash-verified uv.lock
Cython3.3.0/setproctitle1.3.7 wheels unpacked into optional q8b/tools, existing
SCons4.11.1, matching Ubuntu3.12.3-1ubuntu0.17 headers extracted without system
installation. Existing msm-venv not modified. Missing distutils avoided with
the direct Cython compiler entry point. These are dev/build dependencies, not
external capture source/runtime overrides. Full project dependency setup still
separate. Early probe startup matching corrected to pair by actual frame IDs.

Initial real140frame probe delivered~20.026Hz publication but~23.972Hzsource
despite60FPS negotiation: dynamic-framerate1 permits automatic rate reduction.
Retained failed cadence record. Recovered legacy fixed-camera-fps policy,
temporarily set that one control0and restore old value1on close. Shutter/gain/
focus/CPU/GPU/fan policy not set. Strict C recompilation passed.

Final140actual IPC/Cereal pairs:19.9733637Hzpublication,59.6424305Hzsource-sequence
estimate; correct1280x720NV12 stride1280,UVoffset921600,length1382400. Exactly
one narrow-road stream, matching timestamps and IDs, consecutive publications.
Driver timestamp→receiver median40.243515ms/max62.580232ms; not model latency.
NormalSIGINTexit0; before/after1080p30 and dynamic-framerate1match; no camera
owner remains. Bounded stationary capture/IPC only, not a managed model/UI run.

21focused tests pass; Ruff/diff/notebook verification results recorded centrally.
Evidence: optional workspace Ai/Reports/sunnypilot-road-camera-20261102 includes
unit/build logs, live-result.json/all140records, failed cadence record and probe.
No model weights/runtime, Q8B calibration guard or CAN/vehicle code changed.
Next actual geometry/current model-input/runtime qualification; driver monitoring
and hardware telemetry remain deferred. Do not silently copy estimated70degFOV/
1.22mheight as measured calibration. Commit and journal actual validation.
