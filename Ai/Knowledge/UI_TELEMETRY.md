# Live Q8B telemetry on the Sunnypilot onroad UI

Owner request2026-11-02: reuse information from the older testing UI on the
actual Sunny UI. This is diagnostic display, not a vehicle/hardwared health
qualification. Start sourcec744d99f2bed9004bfde493f2c4bd224ffca4516 on radxa/q8b.

## Source and design contract

Teacher-first source: q8b/gpu_webcam/desktop_ui.py thermal_sensor_paths,
hottest_temperature_c,fan_status/update_temperatures; teacher camera note and
student NONCAMERA_HARDWARE. The earlier Tk view reads named CPU/cluster/gpuss
thermal zones, takes the hottest readable sample and polls fan mode/PWM1Hz.
Fresh sysfs read confirms CPU/GPU zones and radxa_svc_glink; fan mode2automatic,
PWM duty readable, no fan1_input/RPM. Never label duty as measured fan RPM.

Panel uses Sunny fonts, white values and translucent dark background on the
right of the camera, preserving central path/speed visibility. It shows hottest
readable CPU/GPU temperatures; raw fan PWM/255, percent and mode; GPU inference
including readback, complete model call, actual modelHz; camera→model return;
and camera→UI first draw. Temperature refresh1Hz off the UI thread. Timing
values are rolling2s medians, stale after1s; sensor samples stale after3s.
Unknown values use dashes rather than zero. Optical exposure/presentation/
scanout latency is not measured. No fan control writes or extra sudo needed.

Timing packet contract: existing unused customReservedRawData0 debug service,
JSON type=q8b.modelTiming/version1, producer PID, inference sequence, camera
publication frame_id, capture_ns/output_ns on the host monotonic clock,
model_ms and inference_ms. No cereal/schema/service change. Q8B Thneed only;
other forks/custom producers must review this reserved-channel allocation.
Bound size4096bytes and window120samples; reject bad types, nonfinite values,
future/stale/out-of-order timestamps. Actual inference sequence computes Hz
even when UI conflation skips packets; camera frame gaps are not model count.
Model process restart clears its window. UI latency uses first draw of each
matching VisionIPC frame with its real timestamp, never repeated redraw age.

## Increment1 — verified data helpers, not yet a UI

Added common/hardware/radxa/telemetry.py read-only health/sampler and
modeld/thneed_q8b/telemetry.py packet/window. Five unit tests cover sensor
name discovery, missing/invalid input, no writes, stale samples, worker stop,
exact timing boundaries, redraw rejection, sequence cadence and model restart.
Ruff passes. Real read-only sample saved in central ui-telemetry report;
CPU56.0C/GPU35.5C/PWM103of255/mode2/RPMnull at that moment. These are readings,
not a fan actuation or thermals-under-load test. No existing runtime changed.

Next: enable Q8B onroad panel and model timing publication, verify actual UI
at current maximum profile, latency/endpoints/clean shutdown and stale states.
Skills: frontend UI, observability, incremental implementation, API/interface,
TDD, performance and Git/code review. Source-first commands and real sysfs
reads; no unrelated REA binary-analysis result claimed.
