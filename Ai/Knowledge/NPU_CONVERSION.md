Checkpoint: conversion/replay safeguards committed as
`43678a671237bae095c1eb6fea95d78ff69d4261`,29focused tests and software checks
pass in maintenance ledger. All local research DLC/context/runtime assets are
inside ignored `modeld/npu/artifacts`; small receipts/results are tracked by the
following results checkpoint. Large ignored files do not travel through Git.
Actual final project HEAD is available from Git; no unfinished hardware worker.

## 2026-11-02 — Fresh INT8 device baseline complete; accuracy rejected

Owner approved research continuation while retaining the failed strict FP16
check. Fresh Mountain Dew v3 W8A8 runs on actual Q8B SDK2.37/v68/SoC37:
200heldout calls exit0 plus3native-byte cases (all42heads bitwise equal).
Calibrated DLC400356844bytes; integer-IO DLC400346268bytes; context444203008bytes.
200MB goal unmet. After132warmup,68teacher-forced frames have normalized RMS
errors29.65% packed,46.16% lane_lines,16.78% plan,43.31% action and189.26%
hidden_state. These are raw tensor errors, not driving-accuracy loss. Candidate
remains unselected; current CD210/OpenCL preview ce7b047/eb741641 unchanged.

29focused tests/Ruff/two shell syntax checks and normal-venv CLI help pass.
Model numerical acceptance FAIL; strict calibration1value and heldout96prewarm
FP16 checks remain visible. Independent original FP32 agrees bitwise on ten
calibration cases and both failed heldout cases. All500 source-state transitions
were independently replayed. CPU backend crosscheck is unsupported at quantized
FullyConnected; PTQ/backend error contributions remain unresolved. No candidate
self-feedback or parsed driving metric after this failure. DSPs running, scoped
clock lease closed/restored, no owned workers. Entire15.6387s run is not a model
latency benchmark. Next: W8A16/mixed activation/output precision experiment with
8-bit weights, then matched heldout comparison and broader calibration; no
modeld selection or vehicle actuation. Actual commits/validation in Git/ledger.

[Results](../../openpilot/selfdrive/modeld/npu/RESULTS.md). Earlier entries below are dated checkpoints, superseded where stated.

---

## 2026-11-02 —500-frame W8A8 artifact complete; integer-I/O context work active

Fresh calibrated DLC is400356844bytes/SHA6cca7b518b6aa7d557727833d589de8a93dfe253a13a0a14f55fa81a3d7e3343,
inside Sunny npu/artifacts/w8a8-research.dlc and x86 dlc-v1. Quantizer exit0,
15m53s, all500frames. Wrapper later exited127 because its mutable shell source
was replaced during the long command; compiler artifact/exit0 preserved, no
recalibration needed. Future host stages use immutable hash-named snapshots.
Full independent500-frame zero/own-state audit passes, all3000native hashes;
strict FP16 comparison remains FAIL1value. Active audited report SHA77a3a166;
research receipt is npu/w8a8-research.json. Heldout200 localstaged/verified;
strict96prewarm precision failures retained, originalFP32exact on22/66.

SoC37/v68 context compile explicitly recognizes SC8280X but FAILS before device
loading: unsupported FP16 in FLOAT32→UFIXED8 desire I/O Convert. No context
binary and no NPU/clock/helper execution. Investigating removing floating I/O
boundary adapters using calibrated integer tensors, preserving all weights/
scales; do not switch to SoC39 or repeat500calibration blindly. SDK primary
Python source dlc_quantizer.py documents preserve_io_datatype via
ir_graph.modify_io_datatype; applying it again collides with existing converted
tensor names, so that in-memory probe was rejected without saving. Next inspect
IR squash/encoding API and validate any integer-I/O derivative before compiling.
PC workdir /home/pc/sunnypilot-npu-20261102; immutable host snapshotab8ea960;
context-v68-soc37-v1/log retained. No running conversion workers now.

Commits7157164 gatesresearch/18tests;6b16d69 heldout+bounded replay/25tests has
historical staged-EOF whitespace failure, corrected and validated by d2bb1b3a.
New uncommitted small audit/quant receipts and README changes expected. Current
CD210/preview defaults unchanged.200MB target unmet (~400.36MB measured DLC);
NPU numerical error/latency and closed-loop candidate recurrence unmeasured.

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
