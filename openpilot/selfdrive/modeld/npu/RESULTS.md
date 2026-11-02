# Fresh Q8B INT8 result — 2026-11-02

**Execution passes; numerical acceptance fails. Keep this candidate unselected.**
The existing CD210 Thneed/OpenCL camera/UI path remains selected. This is a
fresh Mountain Dew v3 conversion; previous approximately12ms GPU results and
historical Jetlink NPU timings describe different models/runtimes.

## Measured size and execution

| Artifact | Bytes | SHA-256 prefix |
| --- | ---: | --- |
| Original FP16 ONNX | 768,750,198 |35976b11be39|
| Calibrated W8A8 DLC |400,356,844|6cca7b518b6a|
| Same weights/scales, integer boundary DLC |400,346,268|8b110ab1242c|
| SDK2.37/v68/SoC37 compiled context |444,203,008|71e62a7e184d|

The200 MB target is unmet. Approximately383 million source initializer values
already require383 MB at one byte/value before overhead. Compiled size does
not measure RAM usage. [Inventory](inventory.json), [calibration receipt](w8a8-research.json),
[integer proof](integer-io-receipt.json), [context receipt](context-receipt-integer.json).

Q8B executed all200 heldout frames and saved2800 head files, exit0. Entire
runner elapsed15.6387s includes initialization, file IO and SDK host conversion;
**it is not an inference or camera latency benchmark**. Existing max CPU/GPU
lease and QNN burst were used; clocks restored and DSPs remain running.
Three further native-U8 cases (indices132/166/199) match all42 heads bitwise
against SDK float-file conversion. [Boundary check](native-io-probe.json).
No live camera or vehicle control ran.

## Floating-reference comparison: failed

Calibration:500 unique sequential frames from the original model's own FP16
state feedback, with every transition independently audited. Heldout:200
separate frames, new zero reset,132 warmup steps,68 evaluated frames
(source632–699). Every INT8 call receives FP16 reference states (teacher-forced).

| Raw output | Normalized RMS error |
| --- | ---: |
| Packed output |29.65%|
| Lane lines |46.16%|
| Plan |16.78%|
| Action |43.31%|
| Hidden state |189.26%|

These are raw tensor errors, **not a driving-accuracy percentage**. Definition:
RMS(candidate−reference)/RMS(reference). Packed errors can hide sensitive
heads. Full per-head MAE/max/tolerance counts and output hashes are retained in
[heldout-int8-results.json](heldout-int8-results.json). Candidate self-feedback,
parsed path/control error, broad scenes and vehicle behavior remain untested;
self-feedback was not attempted after this large teacher-forced failure.

## What the checks establish

- Ten calibration cases and both failed heldout prewarm cases match an
  independent original FP32 graph bit-for-bit after rewriting. This supports
  those graph rewrites, not arbitrary-frame equivalence or INT8 accuracy.
- Strict FP16→FP32 check still fails one calibration hidden value and96 heldout
  prewarm values. The owner approved research continuation with failures
  visible; strict mode and its tolerance remain unchanged.
- Removing20 floating IO adapters preserves all597 static buffers, retained
  graph operations/edges/attributes/shapes, and actual serialized quantization
  encodings. Native-byte probe supports sampled boundary conversion.
- QNN CPU crosscheck fails before execution because its quantized
  FullyConnected implementation rejects the graph. Therefore PTQ and HTP
  backend contributions are not fully isolated.
- With ideal FP16 values rounded to this context's exact output grid, the
  minimum normalized RMS error is already1.95% for lane lines,1.62% for plan,
  1.60% for action and5.27% for hidden state. Plan/action have68/26 values
  outside calibrated ranges. [Output-grid diagnostic](output-quantization-grid.json).
  This identifies coarse output precision/range limits, not every internal
  error or a lower bound on driving performance.

## Next research step

Test W8A16 or mixed activation/output precision with8-bit weights, then compare
on the same heldout frames before expanding the calibration/evaluation corpus.
This can increase file size and does not guarantee recovery. Ordinary PTQ
calibrates ranges; it has not established under0.5% loss for this model.
Do not select this candidate in modeld or erase failed checks to proceed.

Source pins, host reproduction and tool boundaries are in [README](README.md).
All active scripts and retained device assets live inside Sunnypilot. Large
artifacts/data are ignored by Git; receipts/tests/reports are tracked. The
teacher and student notes retain the source and validation history.
