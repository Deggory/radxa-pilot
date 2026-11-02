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

2026-11-02 NPU checkpoint d450dbbd committed/validated (12tests). Corrected
calibration500-v2 completed all500native frames but strict prequant FP16/FP32
diagnostic FAILED atframe443:1hidden_state value(reference .00174427 vsFP32
-.00983241), hiddenRMSrelative.0008444, packedRMSrelative.00022077. Gate blocks
PTQ; no INT8/context/NPU loaded. Investigating same-precision full7input/4output
FP32 reference to isolate promotion rounding from graph-rewrite errors; original
failure remains preserved. source/graph/DLC pins unchanged. New uncommitted
qairt_host help/SC8280 target, diagnose_case/semantic_reference scripts and
receipts are expected current work. PC workspace /home/pc/sunnypilot-npu-20261102.
Known HTP/stub/skel now match SDK2.37aarch64-ubuntu-gcc9.4 exactly; oldSystem
stilldifferent, matchingSDKSystemavailable. REA open_binary validated HTP ELF
identity/e33be7a2/arm64 only, no decompilation/execution claim. Initial700-v1/
native500-v1 stay rejected; correctedroad700-v2 complete and format2 now required.
Next inspect semantic-reference/diagnostic443-FP32, preserve failed gate; do not
silently relax it or claim INT8 accuracy. Last code/data checks passed12tests.

# Fresh big-model NPU conversion

## 2026-11-02 — Fresh Mountain Dew v3 NPU experiment in progress

Owner selected fresh big-model INT8/PTQ work inside modeld/npu and requested
Jetlink updates. Read teacher Jetlink/NPU history. Source ONNX35976b11 downloaded
768750198bytes via configured1e219d model ref; original pickle d4c7a3fc unchanged.
Inventory382904774FP16values implies ~383MB INT8payload before overhead;200MB
not promised. Fresh FP16 CPU reference da9506a6 and FP32 source eceadb80 generated
on trusted x86PC, new floatDLC conversion exits0. 10initial FP32/FP16 comparisons
had no values outside .01+1%; not INT8/driving accuracy. Full PTQ pending.
Reviews (agent + owner-selected Codex CLI) caught ordinal/video alignment bug:
old extractedroad700 and incomplete calibration500-v1 rejected, worker stopped.
Corrected road700-v2 complete:700unique/cadenced encoder-mapped inputs; fresh
calibration500-v2 running on the x86 host.
Source/DLC/data hashes, continuity and spread-out warm diagnostics now gated.
12focused tests/Ruff pass; no experimental NPU context/device/clocks/firmware
operation. Current CD210/OpenCL preview ce7b047 unchanged. Conversion tool venv
installed locally; scope/provenance/commands in modeld/npu/README and session.
Jetlink refs now Zoompilotaf9df78/v0.8.13,mouxangithub7425e98,FOREVERb8cbb92;
3clean manifests verified, previousrefs preserved. Old bundleverifier separately
fails pre-existing q8b source drift; not a new clone mismatch. Runtime target
soc37 vs historical39/library-stack identity remains open before NPU execution.
Next: finish corrected road700-v2, validate mapping/cadence, copy toPC, run
fresh pinned500-frame recurrent state builder, verify receipt, then W8A8 PTQ.

Source-first REA routing; no unrelated binary analysis or runtime qualification claimed.
Skills: planning, incremental implementation, source-driven documentation, debugging,
Git/versioning, focused tests and doubt-driven review. CLI review authorized explicitly.
Raw build/review evidence lives in teacher Ai/Reports/sunnypilot-npu-fresh-20261102
and ignored npu/logs; exact conversion/data/source receipts are in the new folder.

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

2026-11-02 research-tooling checkpoint:18focused tests, Ruff, shell syntax,
notebook64documents/196relative links and whitespace pass. Fresh reviewer
findings resolved; independent recurrence audit and PTQ remain in progress.
Strict FP16 failure is preserved and research artifacts remain unqualified.

2026-11-02 held-out/tooling increment in progress:200independently-reset
FP16 frames500-699 complete; all1200native+200golden file hashes and relocated
local list verified inside Sunny. FP32-vs-FP16 diagnostic fails94hidden values
at22 and2at66; all sampled warm cases pass. These failures remain visible;
independent original FP32 matches rewritten FP32 bitwise on both failed cases.
25tests/Ruff/bash pass; runtime/evaluator CLI help works in normal Sunny .venv
without conversion-only ONNX/ORT imports. New metadata/run linkage guards,
bounded private QNN runner and SIGTERM cleanup are reviewed. No NPU context
loaded yet; full500calibration/audit still running. Model defaults unchanged.

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
