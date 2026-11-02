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
`state.py` modeld adapter reuses this repository's pinned Tinygrad **CPU:LLVM
camera warp**. Driving-model inference still uses saved Thneed GPU instructions.
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
camera timings. The command does not open a camera or set clocks/fan/governors.

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

For a bounded qualification session, add `--seconds 65 --benchmark --model-checks`
and a new `--log-dir`. `--model-checks` saves at most six input/output snapshots
for offline CPU checks; it adds occasional compression/disk cost to those calls.
Model receipt records and camera/UI timing have separate endpoints. The preview
sets numeric `DEBUG=0` and CPU-warp target in its child environment; it does not
modify the calling shell or clock/fan/driver policies.

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
The first complete current-port maximum-clock baseline is20.0008Hz,
11.834ms inference/readback and58.989ms source→output medians; preparation14.693ms.
Thus the current end-to-end target remains unmet. The teacher's35.417ms result
uses its retained different preparation/partial-JPEG pipeline; do not conflate.
GPU-resident image preparation is the next increment; no feature tensor splitting.

## Timing boundaries

The clean65second integrated run measured **36.656ms median /46.326ms p95**
around the complete `model.run()` call: two CPU image warps/packing, history
adaptation/copies, input validation/uploads, Thneed GPU execution/readback and
output parsing. Camera capture, JPEG decode and BGR→NV12 conversion happen in
`camerad` before this call; UI drawing happens afterward. Both are outside this
model-call timer. Capture timestamp→model receipt at UI was separately
94.754/115.031ms median/p95; this endpoint includes UI receipt scheduling and
is not physical display latency.

The historical11.724/12.348ms GPU execution/readback result used a different
max-clock standalone profile. It does not establish the GPU-only time in this
integrated run, which has not been measured separately. Subtracting11.724 from
36.656 cannot identify current camera or preparation cost. Even the historical
run was not always under12ms: its p95 was12.348ms.

The whole-project SCons build currently stops at missing `acados`; the existing
preview/native replay was tested independently and does not need that full
build to launch. Other full-build dependencies remain unchecked.

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
behavior remain. Camera optimisation and clock changes stay deferred. This is
bench inference/UI qualification, not vehicle or road testing.

Project memory: [Thneed reference](../../../../Ai/Knowledge/THNEED_GPU_REFERENCE.md).
