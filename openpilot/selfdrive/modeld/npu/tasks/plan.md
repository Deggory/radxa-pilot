# Fresh Mountain Dew v3 INT8 NPU conversion

Owner scope, 2026-11-02: create modeld/npu, consult teacher, update/study Jetlink,
fresh conversion of the big_driving_tinygrad release for Q8B Hexagon; calibrated
INT8, roughly 200 MB target and minimal measured error. No CD210/default switch.

1. Pin current pickle/ref and retrieve matching original ONNX, hash every source.
   A precompiled Tinygrad JIT pickle is not an ONNX graph; record provenance and
   do not claim compiled-pickle parity from release naming alone.
2. Update clean Jetlink reference clones with saved old refs/manifests; inspect
   changes relevant to exact model selection/export and Snapdragon quantization.
3. Inventory initializer types/counts, IO/state/heads, operators and source sizes.
   Report whether 200 MB follows from INT8 weights; do not equate integer16
   activations with FP16 or compiled-file size with weight size/RAM.
4. Produce guarded, documented compatibility derivatives with CPU reference
   checks before PTQ. Do not bypass old source guards to reuse a mismatched graph.
5. Build fresh floating-reference state from representative road inputs. Start
   with existing road fixtures for feasibility, expand unique frames and retain
   disjoint held-out frame ranges. Never use old-model feature states, duplicate
   frames to reach sample counts, random-only calibration or evaluation leakage.
6. Fresh QAIRT conversion and W8A8 calibration on the trusted x86 compiler host;
   separate outputs, pinned SDK/runtime and known units/IO. Follow compiler help,
   preserve separate perception/policy heads to avoid final range-collapse.
7. Compare floating vs quantized per-head and autoregressive behavior, report
   actual error distributions/finite checks and actual artifact bytes. Ordinary
   PTQ is a baseline; investigate AIMET SeqMSE/AdaRound only against measured loss.
8. Compile for the verified v68 target and inspect context metadata. Current
   Radxa docs soc37 vs historical QAIRT2.37/SA8295 soc39 requires explicit
   reconciliation. No experimental context is loaded until the stack and target
   are verified. Keep DSP recovery/history limits visible, no firmware changes.
9. Save source, scripts, manifests, results and exact next step in project/teacher
   memory; commit tested increments and attach maintenance validation.

The requested under-0.5% loss is an aspiration until an explicit dataset/task
metric exists; per-output numeric agreement is not a driving-accuracy percentage.
A single route cannot establish scene/weather/maneuver coverage. No vehicle
controls, camera calibration, root-helper installation or accepted replay model
changes. Bounded device replay used the already-installed scoped max-clock
lease, then restored clocks. See RESULTS.md for actual completed/failed checks.
