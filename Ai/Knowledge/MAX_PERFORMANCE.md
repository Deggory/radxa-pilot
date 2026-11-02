# Q8B maximum mode and GPU-resident images

Owner2026-11-02 accepted scope: reuse teacher camera/Thneed methods, maximum
CPU/GPU clocks automatically for Sunny model runs, resident GPU crop/packing/
history, no intermediate CPU image readbacks. Establish baseline before any
feature-level tensor splitting. Existing CD210 artifact remains byte-identical;
no graph conversion, weight/precision change or feature splitting was performed.

## Evidence and pins

Implementation base623f728af43fc220bf432aa698126438b6c67942 on radxa/q8b,
following dependency checkpoint b59f68045e67113b3af1d5457c1c1511d0a4b88c.
CD210 ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391,99,641,029bytes,
SHA256eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068.
Tinygrad92b742f711c7d216fd3ed7a46a30a959e3c43bd4;
msgqe7396e76dadbb49e374d4b664ff6bbb43a39bcb0. Adreno690 OpenCL3.0 Qualcomm
0855.3/compilerE031.50.31.01. Python3.12.13, NumPy2.5.3/OpenCV4.13.0.92.
Native replay ELF SHA25646c18dc88e507daf5efdbdde848ba70c3e7431850d802775edf048fa6eb8591d.

Teacher db5b0da 20min result11.724/12.348ms inference and35.417/39.721ms
source→output used calibrated CPU preparation and partial JPEG. The separate
ONNX/MSM GPU BGR warp has a different bilinear preprocessing contract. Reused
persistent-context/buffer design, not that different sampling math. Current
Sunny keeps pinned nearest NV12 rounding/layout and current wrapper semantics.

## Maximum clocks

Owner completed the one-time local installer; no password was shared/saved.
Frozen root helper/source SHA25657aa1f992afd018a1d7f30fbf07067b24f2c75530d062461f087e66198392056.
Only fixed `/usr/local/libexec/sunnypilot-q8b-performance guard` is authorized
without a password. Runtime uses sudo-n and an stdin lease, not general root
access. CPU2438.4/2995.2MHz and GPU690MHz; kernel protections and85C guard remain.
Normal exit and SIGKILLed unprivileged client restore prior policies. Root
recovery state remains on restoration failure. No boot-wide clock setting.
Three adversarial helper reviews corrected stdout backpressure, signal handling
and trusted-path creation before installation. Do not change this frozen helper
or ask for another password during normal launches. See install.md for new hosts.

## Resident image implementation

In state.py, `Q8B_GPU_PREP=1` is the default within explicit Q8B_THNEED mode.
Exact source-index maps are generated once per geometry using three byte-address
passes through the pinned CPU warp. Every live frame uploads one padded NV12
source and gathers both model views directly into the saved input buffers in
the model's existing OpenCL context/queue. Five-slot resident history preserves
lag4; geometry changes preserve past history. Reset zeros the ring and invalidates
image readiness; the next prepare overwrites both inputs before another run.
No per-frame CPU image warp/history or image readback/reupload. Final2576outputs
are read back for the standard parser; feature/desire wrappers are unchanged.
Blocking source upload protects host lifetime even on errors. A separate history
initialization flag permits setup retry after failed initialization.

Controls validate before image history changes. A failure after resident state
mutation prevents another prediction until explicit reset. Unit regression was
RED before this recovery fix and passes afterward. CLI review's reset-buffer
finding was a contract misread: stale input storage is never consumed after
reset; images_ready is false and next prepare overwrites inputs. Raw ring reset
and fresh-input behavior are exercised by exact GPU qualification.

Q8B_FRESH_CAPTURE=1 defaults to the next60FPS arrival at each20Hz publish
deadline, replacing an already-cached frame. Source timestamps/sequence and
stale/error checks remain. Flags0 retain comparison paths. `--model-checks`
explicitly selects slower CPU snapshots and is excluded from timing qualification.
Runtime/build/assets remain inside this project; CPU reference tools are optional
workspace validation dependencies, not deployment imports.

Q8B_FAST_CPU=1 additionally restricts camera/model daemon entry threads and
future workers to the allowed CPUs intersected with fast cluster4–7. It leaves
parent/UI affinity and generic PC real-time policy alone; no FIFO priority or
sudo is needed. Explicit0 retains unrestricted scheduling. An empty allowed
intersection fails rather than widening a caller's CPU restriction. Actual
camera/model affinity4–7 was observed during the run. The teacher's singleCPU7
profile regressed this resident pipeline to40.512ms camera→output/5.373ms prep,
so it was rejected. That trial overlaps a short unit check and is retained as
a diagnostic, not the final controlled result. CLI affinity review found no
material issue; omitted call-site gating was separately checked in source and
existing Q8B/webcam boundary tests.

## Measured gates

| Same endpoint/profile | CPU prep baseline65s | Resident + fresh65s | Unrestricted resident180s |
| --- | --- | --- | --- |
| Steady outputs / Hz |1163 /20.0008|1164 /20.0011|3465 /20.0008|
| Inference/readback median/p95 ms |11.834/13.027|11.223/12.362|11.085/12.068|
| Full model call median/p95 ms |27.857/29.309|13.805/15.300|13.645/15.274|
| Source→model return median/p95 ms |58.989/68.244|37.643/42.020|37.886/42.690|

After adding failed-frame validation, an unrestricted65s repeat measured
38.204/42.802ms source→output median/p95 and explicitly failed the38ms median
target. Keep it alongside the earlier37.886ms result; the margin was unstable.
The final fast-cluster65s run (1164steady/20.0024Hz) measured10.817/11.790ms
inference,13.243/14.885ms fullcall and36.829/41.592ms source→output median/p95.
GPUprepare1.703ms median; source→outputmax44.599ms. A clean repeat is recorded
in the final portable receipt. No higher clocks, graph or image math changed.

All logged clock samples at tested maxima. Three-minute result excludes5s
warmup; source→outputmax46.871ms. A resident-only cached-capture control was
46.676ms median, showing capture selection separately matters. Camera profiling
found cached arrival age24.584ms vs fresh17.100ms; JPEG decode/NV12 remain CPU.
Endpoints exclude UI receipt/drawing and physical exposure/display delay. Target
medians12ms/38ms met in these runs; not every frame stays below either target.
No new20minute qualification or full-manager/vehicle/road qualification claimed.

68focused tests pass, including exact map reconstruction, no live CPU warp or
image inspection, map reuse/change, invalid-control ordering and failed-run reset.
Native build,12savedGPU/12adapter checks,12changing resident exact-image/full2576
output checks including geometry change/reset pass. Six saved resident cases
also pass existing independent current-wrapper FP32 ONNX CPU reference
fa07c7abecc7d662ec37d284fb5f862d6910aaa006137b3da88836dc8647e549,
rtol.001/atol.005; no conversion. Verification-only image readbacks are explicit.
10sactualUI smoke:194camera frames/176model messages/33path points; screenshot
viewed; children0/0/0, settings restored, GPUfaults0→0. Earlier two early-closed
UI65s runs remain incomplete evidence; sustained camera/model run has no UI.

Skills used: performance, incremental, source, debugging, TDD, documentation,
Git, code review and doubt-driven review. Source-first reads/native build and
actual runtime evidence; no unrelated REA binary-analysis result fabricated.
Fresh-context review and owner-selected Codex CLI0.162.0-alpha.17.2
(gpt-6.1-sol/read-only) supplied findings; fixes/limits reconciled as above.

Raw workspace evidence: /home/radxa/comma/Ai/Reports/sunnypilot-max-baseline-20261102/.
Active defaults and launch instructions: Thneed README and install.md. Keep
provisional MM-X geometry invalid, controls/DM off. Next: owner can launch normal
preview; lens/mount measurement, hardware and vehicle integration remain separate.
Feature splitting stays deferred unless a new scoped experiment is selected.

## Final accepted repeat and closeout

Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.

[Portable receipt](../Evidence/q8b-resident-20261102.json). The final diagnostic
requires USE_WEBCAM=1/Q8B_ROAD_ONLY=1 to select provisional geometry; one omitted
environment attempt stopped correctly and its empty output directory is retained.
Guides now give the tested flags.68test final log:resident-units-complete.log;
resident-checks-accepted and resident-cpu-reference-accepted are accepted accuracy
receipts. No remaining source edits are intentionally deferred.
