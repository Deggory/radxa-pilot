# CD210 Thneed on Q8B

The existing tested model was **copied unchanged**, not converted again:

- Model: `../models/q8b_cd210.thneed`, 99,641,029 bytes.
- SHA256: `eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068`.
- Original name: `driving-02.thneed`, from the accepted October30 export.
- Accompanying `.metadata.json` and `.fixtures.npz` are also unchanged copies.
- CD210 revision: `5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391`.

This directory contains native portable C++ replay, pinned vendor sources and
licenses, a Python runner, a current-history adapter and bounded verification.
`provenance.json` records the copied source/asset hashes; `vendor-manifest.json`
records upstream versions/adaptations. Required code and model assets live in
this Sunnypilot project. No runtime import or asset lookup uses external teacher
experiments. The low-level `runtime.py` requires NumPy and uses ctypes for OpenCL;
it does not import Tinygrad, ONNX, an exporter or a converter. The optional
`state.py` modeld adapter uses this repository's pinned Tinygrad **CPU:LLVM
camera warp** once per geometry to generate exact GPU gather indices. Per-frame
NV12 cropping/packing and four-frame image history stay in the loaded model's
OpenCL context and resident buffers. Driving-model inference uses the existing
saved Thneed GPU instructions.
It does not import the older, modified Tinygrad experiment tree.

## Build and verify

From the Sunnypilot root, with its Python environment and the matching Qualcomm
Adreno690 OpenCL driver installed:

```bash
bash openpilot/selfdrive/modeld/thneed_q8b/build.sh
.venv/bin/python -m unittest openpilot.selfdrive.modeld.thneed_q8b.test_runtime
.venv/bin/python -m openpilot.selfdrive.modeld.thneed_q8b.verify \
  --frames 40 --warmup 10 --output /tmp/q8b-thneed-check.json
```

The report path must be new. `build.sh` compiles only the native replay library;
it does **not** convert or regenerate the model. Build needs g++ and the installed
`libOpenCL.so.1`; OpenCL headers/json11 are vendored. Assertions remain enabled.
The generated `build/` library is ignored; model and fixtures are tracked by LFS.

Before native loading, the runner checks the artifact's fixed SHA256/size and
metadata checksum. It selects a GPU matching the saved device/driver exactly;
a mismatch fails with no CPU fallback. Native upload checks byte sizes; Python
also checks all input names, shapes, dtypes, contiguity and finiteness.
Use only the packaged hash-pinned model with the historical trusted-file loader.

Verification replays all six saved cases twice, checks exact saved OpenCL output
and the preserved independent CPU references at rtol0.001/atol0.005, and exercises
the newer queue interface for every case. It then performs a short timed check.
Reports distinguish input upload/validation/replay time from inference-only and
camera timings. The verification CLI does not open a camera; it acquires the maximum-clock
lease described below and restores prior policies afterward. The low-level
Python runner leaves clock ownership to its caller.

## Python interface

```python
from openpilot.selfdrive.modeld.thneed_q8b.runtime import ThneedModel

with ThneedModel() as model:
  output = model.run(legacy_inputs)          # float32[1,2576]
  result = model.run_current(current_inputs) # output plus three next-state queues
```

See `LEGACY_SPECS` and `CURRENT_SPECS` in [runtime.py](runtime.py) for exact contracts.
`run_current` accepts the current stock model's `new_img`, desire, traffic/action
inputs and caller-owned image/desire/feature queues. It follows the pinned ONNX
wrapper's image subsampling, four-frame desire maximum and feature subsampling.
The caller supplies calibrated, packed model views (not full camera images) and
passes returned next-state queues into the next call. Inputs are not modified.
The instance is synchronous and belongs to one caller; close it when finished.
Output precision preserves the accepted stored model's FP16 output/FP32
arithmetic policy, rather than changing the already-compiled model.

## Live modeld and UI integration

The virtual environment lives inside `sunnypilot/`, not the parent workspace.
From a terminal in `~/comma`, first enter the project:

```bash
cd ~/comma/sunnypilot
.venv/bin/python -m openpilot.system.camerad.webcam.preview --model
```

This opt-in preview starts camera, actual stock `modeld --demo` with Thneed, and
the actual Sunnypilot onroad UI. Closing the window stops all three. Messages and
Params use a private namespace; vehicle/planner/control/driver-monitoring
processes are not started. The window labels the temporary geometry uncalibrated.
Predictions are displayed while model/calibration validity remains false for
the borrowed MM-X profile. Measured geometry needs a separate qualification.

For a bounded timing session, add `--seconds 65 --benchmark` and a new
`--log-dir`. Model completion, model receipt at UI and camera/UI timings have
separate endpoints. The preview sets numeric `DEBUG=0` in its children; modeld
automatically holds a scoped maximum-clock lease.

`--model-checks` explicitly selects the slower CPU-preparation reference path
and saves at most six input/output snapshots for offline CPU checks. It adds
compression/disk cost and is excluded from production latency qualification.
Use `verify_resident` below to qualify GPU-resident images directly.

Stock process integration is selected with
`USE_WEBCAM=1 Q8B_ROAD_ONLY=1 Q8B_THNEED=1 DEBUG=0`. It requires real Q8B and the
accepted720p road-only profile, keeps stock parser/messages, disables alternate
model warmup/compiler selection and bypasses Chestnut. SCons in this mode builds
only the native replay wrapper in modeld's subtree, without regenerating model
artifacts. Full manager/vehicle operation is outside this bench qualification.

## Required maximum-performance lease

Q8B modeld and the verification CLI require the root-owned fixed clock guard.
Perform the [one-time setup](../../../../install.md) from a local terminal.
Later launches acquire the lease without a password and restore prior clocks
on exit or model-process death; modeld refuses to run if the lease is absent.
The accepted profile uses CPU2438.4/2995.2MHz and GPU690MHz with thermal limits
retained. The root helper never imports project code from its writable checkout.

For camera-to-model measurements without opening a desktop window:

```bash
.venv/bin/python -m openpilot.selfdrive.modeld.thneed_q8b.bench \
  --seconds 65 --log-dir /tmp/q8b-model-max-baseline
```

Choose a new directory. This starts only private camera/modeld workers, keeps
geometry invalid, and records actual model completion independently of UI
polling. `preview --model --benchmark` records the same model timer alongside
UI timings. Output includes CPU preparation, validation, upload, inference/
readback, clock samples, cadence and whether the12ms/38ms median targets were met.
The first complete maximum-clock CPU-preparation baseline measured20.0008Hz,
11.834ms inference/readback,14.693ms CPU preparation and58.989ms source→output
medians. The resident-image run with fresh capture selection measured20.0011Hz,
11.223ms inference/readback,1.833ms GPU preparation,13.805ms complete model call
and37.643ms source→output medians over65seconds; source→output p95 was42.020ms.
These are measured host endpoints, excluding UI receipt/drawing and physical
exposure/display latency. They do not mean every frame takes less than38ms.

## Resident images and reference checks

`Q8B_GPU_PREP=1` is the default inside the opt-in Q8B Thneed ModelState.
The first frame or a geometry change builds a gather map by encoding source
addresses through the exact pinned warp. It preserves FP32 rounding, chroma
layout and clamping. An OpenCL kernel then uploads one padded NV12 source,
gathers both views, maintains a five-slot ring for the current wrapper's
four-frame lag, and writes directly into the saved model's image inputs.
No per-frame CPU image warp, intermediate image readback or image reupload is
performed. Final predictions are read back for the existing parser; features
and desires keep their current validated wrapper. No feature tensor splitting,
model conversion or precision change was made.

`Q8B_FRESH_CAPTURE=1` is the default for the Q8B RoadCamera: at each20Hz
publisher deadline, wait for the next60FPS camera arrival rather than consume
an already-cached frame. Source timestamps/sequence IDs and stale-frame checks
are preserved. `Q8B_GPU_PREP=0` and `Q8B_FRESH_CAPTURE=0` retain the respective
CPU-preparation and cached-capture baselines for explicit comparisons.

For bounded correctness qualification, use a new output directory:

```bash
USE_WEBCAM=1 Q8B_ROAD_ONLY=1 DEBUG=0 .venv/bin/python -m openpilot.selfdrive.modeld.thneed_q8b.verify_resident \
  --output-dir /tmp/q8b-resident-checks
```

This diagnostic deliberately reads back model image inputs and uses CPU warps;
those operations are absent from production. Twelve changing frames cover both
views, startup/history, a geometry change and reset. All image bytes and2576
model outputs must match the original CPU-prepared replay exactly. Six saved
cases additionally passed an independent current-wrapper FP32 ONNX CPU
reference at rtol0.001/atol0.005; no new conversion was required.

The dependency installation resolved the earlier missing-acados block; the
Q8B minimal root build passes. Full manager/planning/vehicle qualification is
separate from the camera/model/UI checks.

## Qualification

Fresh November2 verification: the copied model runs on the matching Q8B GPU;
12 saved-case checks and all12 queue-adapter checks pass. A40-sample short check
measures12.114ms median/15.851ms p95 for **uploads + replay/readback + validation**
under unchanged dynamic policies. A second40-sample check also passed at
14.223/16.545ms median/p95. Both results are retained; this is not a controlled
performance comparison or a new camera/20minute test.

Teacher's earlier selected profile sustained20Hz over20minutes:
model11.724/12.348ms p50/p95, driver→output35.417/39.721ms. That test used maximum
CPU/GPU690MHz, partial JPEG, CPU calibrated preparation and EGL display.
Its timing scope/configuration differs from this verification. The learned
CD210 core matches current stock weights; the older ONNX interface differs.

The opt-in modeld adapter supplies padded NV12 preparation, two distinct views,
rising-edge desires, current history queues and the normal parser. Warmup resets
all queues. Five packed-view comparisons match pinned CPU warp exactly;32changing
synthetic recurrent steps pass same-input CPU-reference checks across all2576
outputs at unchanged tolerances. First12second live test received216predictions
and rendered33path points; all three children exited0 and camera settings were
restored. See project handoff for later results.

Without `Q8B_THNEED=1`/`--model`, existing stock selection and camera-only preview
behavior remain. The Q8B opt-in path uses the resident-image and scoped-clock defaults above.
This remains bench inference/UI qualification, not vehicle or road testing.

Project memory: [Thneed reference](../../../../Ai/Knowledge/THNEED_GPU_REFERENCE.md).

Q8B camera/model daemons also default to `Q8B_FAST_CPU=1`, restricting their
entry thread and future workers to allowed fast cores 4–7. Parent/UI affinity
is unchanged and no real-time FIFO policy is enabled. Set 0 for scheduling
comparisons. Pinning all work to CPU7 alone regressed this resident pipeline;
the four-core setting measured 36.829 ms median / 41.592 ms p95 from source
capture timestamp to model output at 20 Hz, with 10.817/11.790 ms inference.
The final repeat is retained in the
[portable qualification receipt](../../../../Ai/Evidence/q8b-resident-20261102.json).
