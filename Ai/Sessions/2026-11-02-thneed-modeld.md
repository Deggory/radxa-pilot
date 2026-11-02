# Thneed connected to stock modeld and Sunny UI — 2026-11-02

Owner says proceed to next stage after31aa29b import. Source start
31aa29b77fca1a9eed216b8bceaf38e041fc3232/radxa/q8b, clean. No reconversion.
CD210/ref5b6436a9, saved artifacteb741641 unchanged. Tinygrad92b742f7 and
msgqe7396e76 unchanged; native binary5f83b4ad from prior checked build reused.

## Implementation

New thneed_q8b/state.py implements stock ModelState contract: paddedNV12,
two separately prepared views, rising-edge desire, current state queues, normal
Parser, warmup reset and explicit close/atexit cleanup. Small-model factory
selects it only for Q8B_THNEED=1/realQ8B/Q8B_ROAD_ONLY/USE_WEBCAM. Modeld bypasses
Chestnut for this mode and keeps borrowed geometry invalid. New output_slices
JSON extracted from pinned current ONNX using slice-only restricted metadata
reader; no graph/weights transformation. Model source still the sameCD210 core.
Manager chooses stock runner, defers alternate runner/warmup; SConscript selects
native wrapper build only before any ONNX/Tinygrad model compile command.

Existing preview adds --model and optional --model-checks. Starts only camera,
actualmodeld--demo and actualUI with private Params/messaging. No manager,
planners, driver monitoring, CAN/vehicle interface, control or actuator process.
Zero-angle uncalibrated message supports explicitly provisional overlays;
model/calibration validity remain false, no fabricated calibration success.
Snapshot mode saves at most6input/output files, private preview namespace only.
ChildDEBUG=0/DEV=CPU:LLVM avoid inherited desktopDEBUG=release and absentclang.
Calling shell and performance policies unchanged. All runtime helpers local.

## Checks and actual results

51focused tests/lint pass. TDD missing state/helper imports red then green;
selection/defaults/invalid-mode/buffer/perspective/warmup/history/desire/cleanup/
private-snapshot/previewprocess tests included. Initial NumPy warp failed1of
196608elements at a perspective-rounding boundary. Replaced it with current
pinnedCPU:LLVM warp; no tolerance relaxation. Regression test now preserves that
case.5full-array exact comparisons pass, including both actual provisional warps.
32changing synthetic recurrent steps pass all2576same-input CPU FP32-reference
values at rtol.001/atol.005 and parsed-head finiteness. These compare each GPU
input state, not two independently free-running reference trajectories.

First12s live:216predictions/33point overlay, screenshot viewed, exit0/0/0.
Diagnostic65s with6compressed snapshots:1179steady receipts/19.632Hz;
fullcall36.547/47.108ms p50/p95,max267.672,28calls>50ms,22receiptID gaps.
All6distinct live input tensors/nonzero feature histories pass fresh CPU ORT
checks,2576outputs each. Reused existingfa07c7ab FP32 reference, no new conversion.
Snapshots intentionally add occasional compression/disk work; timings retained.

Separate clean65s without snapshots:1201steady receipts/19.998063Hz,1274total
UI-received model messages,1293camera frames,33point overlay. Fullcall including
warp/history/upload/GPU/readback/parser36.656111/46.325672ms p50/p95,max54.213885;
23calls>50ms and1receiptID gap. Source→UI model receipt94.754403/115.031215ms,
max143.267439; UI receipt gapmax99.817531ms. These endpoints include subscriber
polling/pacing and are not model-only or publisher/physical-display latency.
Camera→drawready60.071425/78.442747ms andEndDrawing88.613569/106.861388ms
p50/p95. Independent raw record recomputation passes, no outliers discarded.
Runs are consecutive engineering screens, not randomized performance A/B.
Average20Hz is not every frame meeting50ms. No old11.724ms inference-only claim.

Final8s lifecycle check after calibration gate review:140predictions/33points,
exit0/0/0. All four sessions restored1920x1080MJPG30/dynamic-framerate1,
CPU/GPU policies unchanged, GPU faults0→0, no owned processes or IPC remain.
Screenshots inspected. No new clocks/fan/driver/firmware/boot changes.

Targeted actual SConscript native-only dry-run passes; no compile_onnx command.
Whole root SCons stops earlier at missingacados package, other build deps not
assessed. Earlier CLI/test setup failures preserved in optional raw reports;
no test deletion, skipping, suppression or lowered accuracy threshold.

## Saved evidence and next step

[Tracked validation](../Evidence/thneed-modeld-20261102.json),
[actual UI screenshot](../Evidence/thneed-modeld-20261102.png),
[launch instructions](../../openpilot/selfdrive/modeld/thneed_q8b/README.md).
Raw logs/timers/snapshots/repro scripts remain optional central references at
Ai/Reports/sunnypilot-thneed-modeld-20261102. Required application code/assets
remain inside Sunnypilot. Active KIA lateral-network JSON not modified.

Completed: camera→existingGPUmodel→stockmessages→actualUI in isolated bench.
Next review this overlay/timing, then separately choose measured geometry,
longer qualification or hardware-provider work. Camera optimisation/calibration
and existing hardware plan are not automatically resumed. No vehicle/road,
actuator, thermal-soak or full-stack readiness claim. No upstream merge/rebase.
Skills: incremental/TDD/API/performance/source/debugging/review/documentation/Git;
REA fast path uses pinned readable source, existing format pins and fresh runtime
outputs. No unrelated REA decompilation or fabricated provider result.

## 2026-11-02 follow-up — Parent-directory launch and timing interpretation

Owner ran `.venv/bin/python` from `~/comma`; the environment exists inside
`~/comma/sunnypilot`. Both launch READMEs now explicitly enter the project.
Source at07bc78e: modeld brackets the complete model.run; state.py prepares both
views/history and parses outputs; runtime.py validates/uploads/replays/readbacks;
camera.py decodes JPEG/converts NV12 before publication. Thus36.656/46.326ms is
not GPU-only and does not include camera capture/decode or UI rendering. Current
GPU-only time remains unmeasured. Historical11.724/12.348ms uses another profile
and cannot be subtracted to infer current camera cost. No artifact conversion,
runtime edits, clock changes or fresh camera/GPU session.

Validation: project `.venv/bin/python -m openpilot.system.camerad.webcam.preview
--help` exits0, lists --model; notebook verifier and git diff --check pass.
Skills: documentation/Git/performance and source-first REA routing; existing
reports plus readable timer/implementation evidence suffice, no unrelated REA
binary analysis. Runtime/model/driver pins and earlier qualification remain
unchanged. Exact next step: retry the documented launch from project root;
separate per-stage instrumentation is needed before assigning current GPU cost.
