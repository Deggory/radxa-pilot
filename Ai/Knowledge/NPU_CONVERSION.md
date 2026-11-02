## 2026-11-02 — Owner-approved INT8 research continuation

Owner explicitly chose “Continue INT8 research; retain failed FP16 check”.
The corrected 500-frame dataset is complete. Strict FP16/FP32 diagnostic still
FAILS at frame443: hidden element2218, .0017442703 versus -.0098324120;
hidden relative RMS .084442%, packed relative RMS .022077%. These are tensor
errors, not driving-accuracy percentages. Ten spread-out comparisons against
an independent original-graph FP32 reference are bitwise equal; precision
promotion is isolated from the host-FIFO/head rewrites on those ten cases.

Added explicit quantize-research mode; default strict gate remains unchanged.
Research requires pinned independent graph, exact bitwise diagnostics and full
native-file provenance; no deployment/vehicle acceptance. QAIRT2.37 rejects
SC8280XP and SC8280X target strings; generic HTP is supported and is being used
for PTQ only, without substituting historical SoC39. First rejected target log
is preserved. Full500-frame zero-state/own-FP16 recurrence is now independently
replayed before accepting calibration provenance. Review caught report-path
shadowing; owned audit was stopped before completion and corrected, inputs
preserved. Local17focused tests/Ruff/bash pass. No INT8/context/device result
yet. PC workdir remains /home/pc/sunnypilot-npu-20261102. No camera/GPU runtime,
clocks, firmware or vehicle changes. Next finish recurrent audit and generic
HTP PTQ, record actual size/encodings, then resolve target37 context support.

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
