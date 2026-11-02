# Maximum performance and resident preparation — 2026-11-02

# Q8B maximum-mode baseline and GPU-resident preparation

Owner2026-11-02 requests reuse teacher max-clock camera/Thneed methods, resident
GPU buffers, no intermediate CPU image readbacks, and feature-level tensor
splitting only after the baseline. Maximum mode should be automatic for Sunny.
Source base b59f68045e67113b3af1d5457c1c1511d0a4b88c; modeleb741641 unchanged.

## Established facts and first completed increment

Teacher db5b0da 20min test: model11.724/12.348ms median/p95; source→output
35.417/39.721ms. That Thneed profile used calibrated CPU preparation, accurate
partial JPEG, maxCPU2438.4/2995.2MHz and GPU690. The separate ONNX/MSM resident
GPU BGR warp uses a different preprocessing contract; it is a reusable method,
not proof that final Thneed already had GPU preparation. Current Sunny instead
uses pinned nearest-neighbor NV12 warps and frame-based current history wrapper.
Do not change either contract silently to reuse the older BGR bilinear kernel.

New fixed root-owned tools/q8b/performance_guard.py and installer grant only
`/usr/local/libexec/sunnypilot-q8b-performance guard` password-free forradxa.
Owner ran one-time installer locally after correcting an accidentally joined
cd/sudo command; password was not shared/saved. Python-I isolates helper imports;
all ancestors checked root-owned/nonwritable, atomic nonoverwriting installation.
Guard uses stdin lease EOF, nonblocking status, flag-only TERM/INT/HUP/QUIT
handlers, exact policy verification and85C cutoff. No overclock or boot policy;
prior state restores on normal/client death, saved state retained on restore
failure. Normal and SIGKILLed client tests pass on actual hardware. Three fresh
adversarial reviews found and resolved backpressure/signal/ancestor issues.

ModelState now acquires/checks/closes lease and refuses lower-policy startup;
verification CLI also owns a lease. Added per-stage replay timings and private
model-completion JSONL. New camera/model-only bench avoids desktop interaction
and distinguishes measurement completion from latency targets. Two UI65s runs
ended externally/early at40.26/42.81s and remain incomplete; no successful full
UI65s max-mode claim. Their model loops stayed healthy, cleanup restored clocks.

Complete65s camera/model-only run:1163steady outputs at20.0008096Hz; all logged
CPU/GPU samples at tested maxima. Medians/p95: inference11.834/13.027ms,
CPUprepare14.693/14.902ms, fullcall27.857/29.309ms, source→output58.989/68.244ms.
Camera<38ms target is not met; benchmark explicitly records false. Low-level
saved12GPU/12adapter checks pass with maximum lease. Existing61tests pass;
summary-order regression added afterward (62total expected; check actual log).
No graph/model conversion or feature tensor splitting. All code is project-local.

## Work still in progress

GPU-resident image path drafted in bridge.cc but not yet built/activated or
qualified at this checkpoint. Planned exact approach: precompute gather indices
with current pinned CPU warp once per transform, then gather NV12/pack/history
straight into the loaded Thneed image buffers in the SAME OpenCL context.
This preserves CPU rounding and current4-frame history lag while removing
per-frame CPU warp/readback and image reupload. Features/desires stay unchanged.
After correctness gates, compare identical maximum-clock camera/model runs;
then address camera decode/cadence bottlenecks against the teacher partial-JPEG
source as needed. No promise of matching35ms until actually measured.

Next exact step: finish native/Python GPU image API and exact map/history gates,
qualify complete raw output parity, run the controlled camera/model comparison.
Keep provisional geometry, controls/DM off; no full-manager/vehicle qualification.
Raw evidence: /home/radxa/comma/Ai/Reports/sunnypilot-max-baseline-20261102/.
Skills: performance/incremental/source/debug/TDD/documentation/Git/doubt reviews;
REA source-first uses actual pinned source and runtime evidence, no unrelated
binary analysis. Root helper source frozen to installed hash; do not change its
installed policy silently or request its password again for normal launches.
