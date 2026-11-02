# Mountain Dew v3 on the Q8B NPU

Fresh conversion research, started 2026-11-02 on `radxa/q8b` at `fd3e0c0`.
The calibrated W8A8 model executes on the real Q8B NPU, but **fails numerical
acceptance and remains unselected**. The accepted CD210/OpenCL camera/model/UI
path is unchanged. Read [measured results](RESULTS.md) before using these tools.

## Source and size

`../models/big_driving_tinygrad.pkl` is compiled Tinygrad, not an ONNX graph:
799,941,965 bytes, SHA-256
`d4c7a3fcfc95813826ca871a80bea18df833aacb2eb6f5333e25a01e65b1a422`.
Jetlink's release lookup located the matching Mountain Dew v3 original ONNX
for ref `1e219d7785cfb7b7343c7f2366347fc86e7ce5f2`. Downloaded afresh:
`artifacts/mountain_dew_v3.onnx`, 768,750,198 bytes, SHA-256
`35976b11be3904eb78e32f7dc55a6abf8e9433ac5aa391a1998f1e9ce001b199`.
[Source](source.json), [inventory](inventory.json), [rewrites](graph-rewrites.json).
Release/checkpoint provenance alone does not prove compiled-pickle parity.

The source has 382,904,774 FP16 initializer values. One byte per value is
approximately 383 MB before scales, biases and graph overhead. The measured
W8A8 DLC is 400,356,844 bytes; its integer-boundary derivative is 400,346,268
bytes and compiled context is 444,203,008 bytes. **Plain INT8 has not met the
200 MB target.** File sizes are not peak RAM. Historical approximately443 MB
contexts used W8A16 (8-bit weights, 16-bit integer activations), a different
model, and are not reused here.

## Conversion and evidence

1. `prepare_road_inputs.py`: this project's pinned CPU:LLVM camera warp on
   paired narrow/wide HEVC road video. Format2 maps each logged frameId through
   `fullHEVCEncodeIdx.segmentId`. The initial ordinal-based extraction and
   incomplete calibration500-v1 were rejected after review exposed a one-frame
   offset. Corrected road700-v2 contains700 unique frames at20Hz. Traffic,
   delays and lane-change rising edges come from the log; no physical camera
   is opened. One daytime route is feasibility material, not broad coverage.
2. `prepare_graph.py`: exact original hash required. FP16 CPU reference only
   replaces Tinygrad Contiguous with Identity. FP32 quantization source hosts
   image FIFO updates, rewrites static Reshape/negative GatherND, and splits
   outputs by head. The compiler removes two constant padding values; the
   evaluator reconstructs zero padding and maps outputs by name.
3. `reference_dataset.py` and `audit_reference.py`: new source-model states,
   zero initialized and advanced using the FP16 reference's own feedback.
   All500 calibration states and3000 native input files independently audited.
   Ten spread-out rewritten FP32 outputs match the independently promoted
   original FP32 graph bit-for-bit. Fresh heldout200 starts at sourceframe500,
   resets independently and warms for132 frames before68 evaluated frames.
4. `qairt_host.sh`: QAIRT2.37.1.250807, W8A8, bias32, per-channel/per-row
   calibration with all500 frames. Generic HTP PTQ succeeds; that SDK rejects
   SC8280XP/SC8280X quantizer target strings. Actual context compilation uses
   explicit **v68/SoC37**, recognized as SC8280X. No SoC39 substitution.
5. `integer_io.py`: SoC37 compilation initially failed on floating boundary
   Converts. Remove exactly6 input and14 output adapters, keeping all597
   static buffers, retained operations/attributes/edges/shapes and calibrated
   encodings unchanged. Independently reload the saved DLC and compare actual
   encodings with sidecars. No second quantization or weight conversion.
6. `compile_integer_context.py`: verify that proof, compile v68/SoC37, inspect
   metadata and validate every native IO scale/offset/name/shape. It has no
   device execution side effect. [Proof](integer-io-receipt.json),
   [context receipt](context-receipt-integer.json), [metadata](context-info-integer.json).
7. `run_qnn.py`: bounded private SDK replay,200 real device calls completed.
   Uses existing scoped max CPU/GPU lease, fast cores4–7 and QNN burst; no
   camera or vehicle process. Exact runtime/context/data hashes checked.
   Float files are quantized/dequantized by the SDK around native U8 graph IO.
   Three extra native-byte cases match all42 heads bit-for-bit. This check
   does not establish FP16 accuracy. cDSP/adsp remain running; clocks restored.
8. `evaluate_outputs.py`: verify execution/output hashes, skip132 warmup
   frames and report per-head and packed FP16-vs-INT8 errors. The teacher-forced
   result fails badly. Candidate self-feedback and parsed driving metrics
   remain unperformed. QNN CPU crosscheck fails on quantized FullyConnected
   validation; PTQ and backend error contributions are not fully isolated.

## Retained failed FP16 check

Strict prequant tolerance remains absolute0.01 plus1% relative. Calibration
frame443 fails one hidden value: .00174427 becomes -.00983241; hidden-state
relative RMS .084442% on that frame. [Diagnostic](diagnostic-443.json),
[independent source](semantic-reference.json), [ten FP32 cases](bitwise-semantic-validation.json),
[500-state audit](calibration500-audit-summary.json).

Owner explicitly approved continuing INT8 research with this failure retained.
`quantize` still rejects it. `quantize-research` requires the pinned independent
FP32 checks and audited input provenance, then labels the artifact research.
Heldout prewarm comparisons also retain96 failed hidden values, with independent
original FP32 bitwise agreement on both affected cases; see
[heldout summary](heldout-reference-summary.json). No tolerance was relaxed.

## Reproduce tooling and host stages

Graph conversion uses the trusted x86 PC with32 GB RAM, not the8 GB Q8B.
Workspace: `/home/pc/sunnypilot-npu-20261102`. Installed toolchain:
`/home/pc/q8b-npu-conversion/qairt237-big-model-conversion`, SDK2.37.1.250807,
Python3.10, NumPy1.26.4, ONNX1.16.1, ORT1.22.1. The PC is a build host;
runtime assets and code are kept inside this Sunnypilot project.

Use the normal project environment for road preprocessing (ffmpeg/ffprobe on
its PATH). Conversion/tests use the isolated environment:

```bash
cd ~/comma/sunnypilot
uv venv --python .venv/bin/python openpilot/selfdrive/modeld/npu/.venv
uv pip install --python openpilot/selfdrive/modeld/npu/.venv/bin/python -r openpilot/selfdrive/modeld/npu/requirements-conversion.txt
openpilot/selfdrive/modeld/npu/.venv/bin/python -m unittest discover -s openpilot/selfdrive/modeld/npu/tests -v
```

`qairt_host.sh help` lists floating/strict/research stages. Stage an immutable,
hash-named, read-only script before a long host command. Replacing the first
live wrapper caused shell exit127 after the quantizer had already succeeded
(exit0,15m53s); both outcomes are preserved and calibration was not repeated.
The floating-IO `context-research` stage fails on this target; use the checked
integer-IO route instead. With source staged in `$work/source`, SDK environment
wrapper staged there, and variables pointing to the installed toolchain/work:

```bash
PYTHONPATH="$work/source" bash "$work/source/sdk_python.sh" "$toolchain" -m openpilot.selfdrive.modeld.npu.integer_io "$work/artifacts/dlc-v1/w8a8-research.dlc" "$work/artifacts/dlc-v1/w8a8-integer-io-v2.dlc"
PYTHONPATH="$work/source" bash "$work/source/sdk_python.sh" "$toolchain" -m openpilot.selfdrive.modeld.npu.compile_integer_context "$toolchain/qairt/2.37.1.250807" "$work/artifacts/dlc-v1/w8a8-integer-io-v2.dlc" "$work/artifacts/context-integer-v68-soc37-v1"
```

Destinations must be fresh; never overwrite retained results. `--audit-existing`
reinspects an artifact only with a fresh proof/receipt path, preserving prior
receipts separately. Conversion modes pin this experiment's source/calibration;
they are not general-purpose arbitrary-model deployment commands.

The normal Sunny environment can run `run_qnn --help` and
`evaluate_outputs --help` without ONNX/ORT. Actual replay requires private
`artifacts/runtime-2.37` files matching [runtime manifest](runtime-2.37.json),
context receipt/proof, and relocated heldout inputs with verified provenance.
The runner limits its own child to120s and stops it on SIGTERM/lease failure
before restoring clocks. Do not automatically rerun a failed device context.

## Acceptance and next experiment

The under0.5% goal requires a defined task metric and representative evaluation;
raw tensor error is not driving accuracy. One route, teacher-forced recurrence
and no parsed road/controls test cannot establish it. This W8A8 candidate is
rejected before live integration. Next investigate **W8A16 or mixed activation/
output precision while retaining8-bit weights**, and broader calibration data.
Output-grid diagnostics already show coarse8-bit ranges on sensitive heads.
This is a proposed experiment, not measured accuracy recovery. AIMET SeqMSE/
AdaRound are additional techniques, not already-run calibration magic.

Large models/data/logs/venvs are ignored. Source, small receipts and results are
tracked. Source-first review and actual SDK runtime/context inspection were
used; REA established HTP ELF identity only, not model accuracy. Agent reviews
and the owner-selected Codex CLI review are preserved in teacher evidence.
No modeld/backend default, firmware, calibration or vehicle actuation change.
[Plan](tasks/plan.md) / [checklist](tasks/todo.md) / [results](RESULTS.md).
