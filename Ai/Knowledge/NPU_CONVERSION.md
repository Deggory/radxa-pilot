# Fresh big-model NPU conversion

Owner selected 2026-11-02: new active work in
[modeld/npu](../../openpilot/selfdrive/modeld/npu/README.md), separate from the
accepted CD210/Adreno preview. See the [dated session](../Sessions/2026-11-02-fresh-big-model-npu.md)
and source/data/graph receipts in that folder. This supersedes the advisory-only
scope in the earlier big-model session; it does not resume the parked Jetlink
split experiment.

Mountain Dew v3 ref1e219d: original ONNX35976b11/768750198bytes, pickle d4c7a3fc
unchanged. Fresh reference da9506a6, FP32 source eceadb80, x86 QAIRT2.37 floating
DLC conversion passes. Approx383millionFP16initializer values imply an INT8
payload estimate near383MB before overhead, not a200MB promise. Corrected
encoder-index-aligned road700-v2 has700unique tensors and two reconstructed
lane-change pulses; first version/incompletecalibration500-v1 are rejected.
Fresh500-frame state generation/calibration500-v2 is running on the x86 PC.
12tests/Ruff pass locally in the project's isolated conversion venv. CPU
reference/FP32 comparison gate is .01+1%; INT8 accuracy and NPU execution are
pending. Current Radxa SoC37 vs historicalSoC39/library-stack mapping remains
open before any new context is loaded. No vehicle/default/model-runtime change.
