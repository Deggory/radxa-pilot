# Unknowns and limits

These remain open; the notebook must not silently fill them in.

- Current stock model/runtime/parser compatibility with the preserved MSM
  Adreno execution path. Older measured model results concern a different
  model identity and runtime contract.
- Identity is implemented at12e44fee; actual Q8B camera calibration and external
  reader/future-upstream compatibility for local enum ordinal8 remain open.
- Actual IMU/GNSS devices or providers, mounting axes, units, rates and clock
  alignment; comma I²C/GPIO paths are not compatibility evidence.
- VisionIPC layout/stride/UV offset, ownership and frame-time pairing across
  capture, inference, recording and the native UI.
- Real thermal/power/fan behavior, host display/input and recording backend.
- Managed startup, dead-child restart, stale-data and shutdown qualification.
- Later custom steering feedback, car interface, bus routing and safety. A
  copied controller cannot establish measured actuator behavior.
- Deep algorithm-level review outside inspected paths. All tracked paths can
  be indexed while substantial behavior remains unreviewed and untested.

Use [coverage](Knowledge/COVERAGE.md) and the
[workspace question log](/home/radxa/comma/Ai/QUESTION_LOG.md) for related evidence.
