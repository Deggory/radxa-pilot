## 2026-11-03 — Game car/configuration still unconfirmed

Asked which BeamNG vehicle/configuration is selected. Owner referred to the
BeamNG-openpilot author instead of naming the currently loaded vehicle. Saved
Caleb5435d674 source does not force one model: user spawns a car; Covet is an
example, ETK800 appears in geometry examples. Do not silently select either
as the owner's car. Native algorithm tests use artificial limits; final game
profile/command mapping remains unresolved. Continue independent software work
without resuming held Chimera or physical Interceptor tasks.

2026-11-03 identification update: C2-name compatibility is implemented at04a7835.
Remaining identification question is measured automatic CAN/ECU identity, not
fixed selection. Teacher C2 used a forced name and placeholder fingerprint.
No owner question needed for the completed alias/migration increment.

## 2026-11-03 — RetroPilot live-integration facts still needed

Car code stage implemented; no question pending for this completed increment.
Before live integration: confirm installed Chimera image/health/bus route,
producer speed units (C2rawkm/h vs saved Hall*100 and ambiguous MODE), actual
vehicle geometry/dynamics, endpoint calibration and MCU safety. Wheel/gear/
cruise-status/IMU/session gaps remain in the shared contract. Teacher evidence
was recovered first; do not ask the owner to repeat already retained facts.

## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Open implementation facts: canonical wheel/IMU/session/gear and cruise-status mapping, speed units/MODE, selected game actuator family, installed Chimera behavior/routing, timeouts/bus load. Later bench: measured angle authority, endpoint types/calibration and physical stop behavior. Teacher evidence recovered before any owner questions; no new question pending.

# Unknowns and limits

Owner deferred automatic calibration2026-11-02, choosing temporary MM-X
fixed intrinsics in Q8B road-only mode. Future replacement options: target-assisted collection/solve
and measured vehicle-frame target pose, or target-free estimation with
independent validation/alignment. Existing guided capture is not autosave.

These remain open; the notebook must not silently fill them in.

- Current stock model/runtime/parser compatibility with the preserved MSM
  Adreno execution path. Older measured model results concern a different
  model identity and runtime contract.
- Identity is implemented at12e44fee; actual Q8B camera calibration and external
  reader/future-upstream compatibility for local enum ordinal8 remain open.
- IMU model/connection are known:Adafruit LSM6DS3TR-C/I²C9/0x6a. Current
  managed IMU/GNSS providers, installed mounting axes, units, rates and clock
  alignment; comma I²C/GPIO paths are not compatibility evidence.
- Q8B road-only720pVisionIPC layout/source IDs/timestamp pairing and model copy
  now tested; current CPU-warp synthetic parity matches ONNX input. Remaining
  inference/recording/native-UI buffer contracts and Adreno execution are open.
- Actual lens K/distortion, stable optical/focus state and camera mount remain
  unmeasured. Owner selected printable target/tool; candidates are never
  automatically installed. Current continuous autofocus1needs explicit review.
- Real thermal/power/fan behavior, host display/input and recording backend.
- Managed startup, dead-child restart, stale-data and shutdown qualification.
- Later custom steering feedback, car interface, bus routing and safety. A
  copied controller cannot establish measured actuator behavior.
- Deep algorithm-level review outside inspected paths. All tracked paths can
  be indexed while substantial behavior remains unreviewed and untested.

Use [coverage](Knowledge/COVERAGE.md) and the
[workspace question log](/home/radxa/comma/Ai/QUESTION_LOG.md) for related evidence.

2026-11-02 — Open evidence question (no owner answer needed yet): does bundled
Mountain Dew v3/1e219d77 match historical big ONNX6fee5937 graph and weights?
Compare retained source/export/contracts first; NPU38.196ms timing cannot be
assigned to bundled pickle before that. [Review](Sessions/2026-11-02-big-model-npu.md).
