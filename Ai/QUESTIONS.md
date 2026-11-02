# Unknowns and limits

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
