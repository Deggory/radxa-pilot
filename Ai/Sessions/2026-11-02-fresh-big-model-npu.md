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
