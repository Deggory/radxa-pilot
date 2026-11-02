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
Bound size4096bytes, signed64-bit integers and window120samples; reject bad types, nonfinite values,
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

## Increment2 — live onroad integration verified

Data helpers source5e01a48d98b2abd62d52add22a05bd8ab2a70dc1. Added onroad/
q8b_stats.py plus guarded AugmentedRoadView rendering/cleanup. Uses existing
fonts/text cache, right-side dark panel, and draws before alerts so alerts
retain priority. Health sampling never blocks the render thread; subscriber
uses nonblocking conflation, data/window sizes and displayed Hz are bounded.
Common config.stats_enabled is board/road-only scoped; Q8B_SHOW_STATS=0 opts out.
Modeld publishes one bounded packet per successful Q8B Thneed output. Message
creation/send failure disables diagnostics and logs once; inference continues.
Preview saves the displayed snapshot and bounded raw windows for auditing.

The first15s integration had health/UI readings but no model timings: primitive
Data requires raw union assignment rather than struct init. Preserved failed
run; added real Cereal publisher regression, then fixed new_message(None,
valid=True) followed by Data assignment. Unit also checks debug-send failure
cannot terminate inference. No schema/service or native build change needed.

Eight new tests (76total focused suite) include zero versus missing, packet
validation/restarts/staleness, repeated draw rejection, actual inferenceHz,
UI scope/opt-out and publisher failure isolation. Deep/oversized JSON and
out-of-range counters are rejected. Ruff passes; no lint suppressions/skips.
Real corrected15s,65s and final10s UI screenshots viewed.65s receives1274debug
packets, zero rejected; all39displayed model samples exactly match benchmark
frame/capture/output IDs and durations.41UI first-draw samples match VisionIPC
metadata and precede benchmark draw-ready by0.781ms median. Final10s similarly
matches40model/40UI samples with179packets/zero rejections; command exits0.

65s model benchmark:1183steady samples/20.0048245Hz; GPU inference10.932599/
12.132907ms and camera→model36.831579/41.043257ms median/p95. UI benchmark
statuscomplete; draw-ready45.389968/58.292098ms, EndDrawing74.590069/88.903643ms.
Panel is a rolling2s snapshot, so displayed values differ from whole-run stats.
All logged CPU/GPU clock samples at tested maxima.76tests, native-model/helper
hash checks and independent frame/timer matching pass. Numerical NN references
were not rerun: graph/weights/native replay/preparation remain unchanged.

One65s outer command returned143 after complete UI data/children0/0/0. Signal
origin remains unestablished; independent postcheck verifies clocks/camera
restored, no root lease/private IPC/owned workers and GPUfaults0. Final10s
launch/cleanup succeeds normally. Keep this anomaly in the raw report; do not
claim all outer launchers exited0. Firmware may change automatic PWM naturally;
only reads were added, automatic mode stays2 and no PWM value is forced/restored.

Changes: modeld timing publication; Q8B packet/window helper and tests;
ui/onroad/q8b_stats, AugmentedRoadView and UI tests; webcam config/preview;
install/camera guides and notebooks. All application code lives in Sunny.
Raw optional workspace evidence: Ai/Reports/sunnypilot-ui-telemetry-20261102/.
Portable receipt is tracked at Ai/Evidence/q8b-ui-telemetry-20261102.json.
Read-only UI diagnostics do not qualify hardwared, optics, vehicle or actuation.
Source-first teacher/native Python/Cereal/sysfs/runtime evidence; REA binary
analysis is not applicable. No additional agent/CLI review claimed this task.
