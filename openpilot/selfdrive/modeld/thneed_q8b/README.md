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
experiments. The Python runner requires NumPy and uses ctypes for OpenCL; it does
not import Tinygrad, ONNX, an exporter or a converter.

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

## Qualification and next integration

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

This increment supplies the copied asset and a runnable, checked inference
backend. Stock manager/modeld selection and camera preview remain unchanged.
Connecting this backend to live modeld/camera publication and Sunny overlays,
then checking recurrent timing/accuracy, is the next integration step. Camera
latency optimisation and clock-policy changes remain deferred. No vehicle or
full driving-stack qualification follows from fixture replay.

Project memory: [Thneed reference](../../../../Ai/Knowledge/THNEED_GPU_REFERENCE.md).
