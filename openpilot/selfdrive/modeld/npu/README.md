# Mountain Dew v3 on the Q8B NPU

Fresh conversion experiment started 2026-11-02 at Sunny `fd3e0c0`, branch
`radxa/q8b`. This folder contains the active NPU work. The accepted CD210/OpenCL
camera/model/UI path is unchanged; no NPU backend is selected in modeld.

## Source and size

Bundled `../models/big_driving_tinygrad.pkl`: 799,941,965 bytes, SHA-256
`d4c7a3fcfc95813826ca871a80bea18df833aacb2eb6f5333e25a01e65b1a422`.
It is compiled Tinygrad, not an ONNX graph to feed directly into QAIRT.
Jetlink's release-ref lookup found the original Mountain Dew v3 ONNX for
configured ref `1e219d7785cfb7b7343c7f2366347fc86e7ce5f2`. Downloaded afresh into
`artifacts/mountain_dew_v3.onnx`, 768,750,198 bytes, SHA-256
`35976b11be3904eb78e32f7dc55a6abf8e9433ac5aa391a1998f1e9ce001b199`.
[Source receipt](source.json) / [IO and initializer inventory](inventory.json).
Matching release provenance does not itself establish compiled-pickle parity.

There are 382,904,774 FP16 initializer values (765,809,548 bytes). At one byte
per value the estimated INT8 payload alone is approximately 383 MB, excluding
scales, bias precision and compiled graph overhead. Includes floating constants;
not a measured compiled size or peak RAM. **The 200 MB target is unmet by plain
INT8.** Historical approximately 443 MB Q8B contexts were W8A16, not FP16:
8-bit weights with 16-bit integer activations. They are not reused here.

## Conversion tools and current progress

1. `prepare_road_inputs.py` runs this project's pinned CPU:LLVM warp on paired
   narrow/wide HEVC road video. Requires versioned road format 2. Frame IDs map through the logged fullHEVC
   encoder `segmentId`; message ordinals are not video positions. Capture
   alignment, actual backend and file/image hashes are recorded. Physical
   camera is not opened. Condition inputs reconstruct rising-edge lane-change
   pulses from logged metadata, driver-side traffic convention and delays.
2. `prepare_graph.py` requires the exact original SHA and a fresh destination.
   FP16 CPU reference replaces only `org.tinygrad::Contiguous` with Identity.
   FP32 quantization graph hosts image/history updates, safely rewrites static
   Reshape/negative GatherND, and exports independent heads. Compiler may omit
   the constant two-value padding output; it must be reconstructed as zeros on
   the host. Never infer compiled output order from ONNX positions alone.
   [Exact derivative hashes and rewrite manifest](graph-rewrites.json).
3. `reference_dataset.py` generates this release's own recurrent states from
   zero, verifies model/source/data/cadence, and compares FP32 versus FP16 at
   spread-out frames. Its receipt hashes every native file and the input list.
   Requires at least min(10, frame count) comparisons. Compatibility diagnostic
   gate: no values outside absolute 0.01 plus 1% relative tolerance.
4. `qairt_host.sh` uses the existing QAIRT 2.37.1.250807 x86 compiler environment
   in an isolated experiment work directory. Floating DLC conversion succeeded.
   Before W8A8 PTQ it verifies the floating DLC/source receipt and calibration
   receipt, including native files and numerical gate. Weights/activations 8,
   bias 32, per-channel/per-row quantization. No NPU context is loaded by it.

Initial ordinal-based 700-frame extraction was rejected: review exposed a
one-frame source-video offset. Its pixel agreement with the older teacher
extractor was not timestamp/alignment proof. The partially generated native
`calibration500-v1` is explicitly rejected and its worker was stopped; never
quantize it. Corrected `road700-v2` uses encoder indices; fresh native state
will use `calibration500-v2`. Existing original/FP32 graph and floating DLC
are unaffected by that dataset error. Exact status and commands are saved in
the project notebook/session; do not assume the full list below has completed.

## Reproduce locally and on the conversion PC

Keep the normal project environment for media/camera preprocessing. It needs
its own `.venv/bin` on PATH for ffmpeg/ffprobe:

```bash
cd ~/comma/sunnypilot
PATH="$PWD/.venv/bin:$PATH" DEBUG=0 .venv/bin/python -m openpilot.selfdrive.modeld.npu.prepare_road_inputs --source /path/to/paired-route-segment --output openpilot/selfdrive/modeld/npu/data/road700-v2 --frames 700
```

Large graph transformation and QAIRT compilation run on the x86 PC with 32 GB
RAM, not this 8 GB Q8B. Current temporary compiler workspace is
`pc@10.43.0.216:/home/pc/sunnypilot-npu-20261102`; strict trusted-key connection
comes from teacher converter.json. Scripts remain owned here and are copied
there for execution. This is a build host, not a required runtime service.
Existing QAIRT work is separate and never overwritten:
`/home/pc/q8b-npu-conversion/qairt237-big-model-conversion`.
The compiler's Python 3.10/NumPy 1.26.4/ONNX 1.16.1/ORT 1.22.1 are retained.
Graph artifact hashes are tied to the recorded tool versions.

For local tooling tests, use a separate conversion environment; the Sunny
runtime lock/environment is not modified:

```bash
uv venv --python .venv/bin/python openpilot/selfdrive/modeld/npu/.venv
uv pip install --python openpilot/selfdrive/modeld/npu/.venv/bin/python -r openpilot/selfdrive/modeld/npu/requirements-conversion.txt
openpilot/selfdrive/modeld/npu/.venv/bin/python -m unittest discover -s openpilot/selfdrive/modeld/npu/tests -v
```

## Acceptance and unresolved limits

Reserve separate road ranges for calibration and held-out testing. Held-out
sequences must reset independently and warm up all state queues (up to 132
steps here); evaluate with reference states and with each candidate's own
feedback. Global cosine alone can hide failed small heads. Report per-head
absolute/relative errors, parsed road/path/controls, saturation and recurrent
drift against floating reference. These are numerical diagnostics, not a
single driving-accuracy percentage. Under 0.5% loss is not guaranteed.

700 frames of one daytime route are feasibility material, not broad road/
weather/night/maneuver coverage. Ordinary PTQ calibrates quantization ranges;
[AIMET](https://github.com/qualcomm/aimet) SeqMSE/AdaRound are additional
optimization techniques to investigate against measured loss, not already-run
accuracy recovery.

Current [Radxa guide](https://docs.radxa.com/en/dragon/q8b/app-dev/npu-dev/qairt-sdk)
reports SC8280XP/v68/SoC37, whereas historical QAIRT2.37 experiments used SoC39
(SA8295). Resolve selected-SDK mapping and pin backend/System/stub/skeleton plus
context metadata before loading a new context. Do not copy current online
settings blindly onto the older working runtime. Historical DSP failures and
unidentified System-library release remain evidence limits. No firmware,
recovery/reboot, clocks/helper, camera calibration, vehicle or actuation change
is part of this conversion. INT8 context execution and accuracy remain pending.

Large artifacts, data, logs and local virtual environments are ignored; source,
receipts and small results are tracked. Keep successful deployment assets inside
this project when qualified. [Plan](tasks/plan.md) / [checklist](tasks/todo.md).
