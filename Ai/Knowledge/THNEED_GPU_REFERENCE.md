# Teacher's tested Q8B Thneed GPU pipeline

Recovered2026-11-02 at project b67031e3d6bc585fcba4123f188f070fca2ee1fb,
radxa/q8b. Owner asks to consult teacher about the fast Thneed work. Read-only
review and memory promotion; no runtime port or launch authorized by this review.

## What was implemented

Thneed is a saved GPU execution format/runtime, not another trained network.
The earlier CD210 small driving ONNX659727c4d4839adc4992a254409a54259a8756a743f2d567bf5fdc6579f8009b
was adapted to FP32 ONNXee8ca6b35e923c098f0840474cdf826dc6fb7771484048b9202604620420bbb2,
compiled with Tinygrad Qualcomm OpenCL and exported as kernels/buffers/launches.
Native portable C++ Thneed execute/clexec replays saved work, keeping weights
and allocations resident and avoiding model parsing/graph compilation per load.
Inference has162dispatches/106programs, scaled FP16 static weights, FP32
activations/arithmetic and FP16 output; global FP16 was not enabled.
This is portable OpenCL, not KGSL command-buffer replay or the MSM backend.

Serializer adaptations preserve image/buffer aliases, snapshot reused-kernel
arguments, unmap CPU mappings before execution and allocate all declared inputs
even if pruned. Earlier driving-01 artifact failed; only driving-02 is accepted.
Historical openpilot v0.9.5 source87fbeb8787e7a29fa190232f9117192824a193c1;
Tinygrad378950224f4cf3ba13a8bed5797580660e92d54d plus nine recorded local patches.
Do not overwrite current pinned Tinygrad92b742f7 with that older modified tree.

## Actual preserved files

Optional workspace reference (not a deployable-project runtime dependency):
/home/radxa/comma/q8b/experiments/thneed-20261030/artifacts/driving-02.thneed,
99641029bytes, SHA256eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068.
Freshly hashed November2: exact match. Export/fresh-load source in same experiment;
trial commit f987ab72f4ac4a6b09c13ea04a22dc695800f3a5.
Native library SHA256da421a53649c100aade3d3366aae7455c8ba722e4cd7972945d9e220c69a7a14
is a recorded provenance pin, not freshly executed or rehashed in this review.
Qualcomm Adreno690 OpenCL3.0 build0855.3/compilerE031.50.31.01 was the tested driver.
The saved binary is device/driver-specific, not portable to any GPU by filename.

## Measured results and their boundaries

Trial Oct30:640 unpaced resident-input forwards,10.899909ms median/12.012924ms
p95, excluding upload/camera/preparation. Twelve exact same-CL/CPU-ORT tolerance
checks pass. Same-process CL versus portable replay screen23.800569→12.293632ms
is evidence of lower runtime overhead in that configuration, not a universal
advantage over tuned MSM or a comparison to current CD210.

Matched Oct31 max-clock/common-CPU-prep/partial-JPEG camera comparison:
MSM15.607984ms vs Thneed11.864441ms model; camera→output40.098025 vs35.994752ms.
Sixteen paired blocks favor Thneed; previous tuned MSM12.17ms used different
memory-floor/GPU-prep settings. Those differences prevent a blanket backend claim.

Most useful sustained reference: Oct31 source
db5b0da25ae599563705de2179d0fd8cb843630e, experiment/thneed-20min-soak.
720pMJPG60/newest20Hz, exact partial JPEG, CPU calibrated warp/history,
portable Thneed, EGL display; GPU690MHz and CPUs2438.4/2995.2MHz verified.
HIGH context priority was accepted/read back, but separate A/B showed no proven
speed gain from priority itself. No owned memory-floor module in this profile.

| Endpoint | Median | p95 |
| --- | ---: | ---: |
| Thneed execution/readback |11.724ms|12.348ms|
| Driver timestamp→model output |35.417ms|39.721ms|
| Driver timestamp→host EGL draw/swap return |42.186ms|56.996ms|

Frozen100-frame warmup leaves24101frames over1204.999s at20.000014Hz,19gates pass.
Zero camera recovery errors/GPU faults; maxmodel18.841ms/maxoutput50.277ms.
Twelve saved cases plus six changing live recurrent CPU-ORT comparisons pass
rtol.001/atol.005 across2576outputs. These are sampled numerical checks, not
road/lateral-control qualification. Cleanup restored camera/CPU/GPU/fan settings.
Do not confuse generic TIMING_SUMMARY.json's20-warmup summary with the accepted
100-warmup result.json/protocol.json. Host UI endpoint is not optical scanout.

## Reuse in current Sunnypilot

Fresh November2 correction: current CD210 ONNX65a08adc and tested659727c4
share checkpoint and all learned weight contents. New history wrapper changes
ONNX bytes/interface, not the trained core. Earlier different-weights claim was
incorrect. Both60Conv/82Gemm/8MatMul constant-RHS sequences match; all old
constant content fingerprints retained. See [confirmation](../Sessions/2026-11-02-thneed-cd210-confirmation.md).
Current-wrapper runtime still needs qualification; no automatic11ms promise.
Recommended next work: adapt the proven exporter/replay approach to current
weights and exact input/state/output contracts, verify CPU parity first, then
qualify20Hz camera/model publication and Sunny UI. Keep necessary code/assets
inside sunnypilot; do not depend on the external experiments in deployment.
Do not fake AGNOS or copy old Tinygrad wholesale. Current camera optimisation
remains deferred. This is guidance; no implementation started in this review.

Teacher evidence: Ai/Reports/q8b-thneed-trial-20261030/REPORT.md,
Ai/Reports/q8b-jpeg-runners-max-20261031/REPORT.md,
Ai/Reports/q8b-20min-soak-20261031/REPORT.md plus result.json/protocol.json.
Consult those archived sources/manifests before any implementation. Skills:
performance-optimization, documentation and Git; source-first report/source
inspection, no unrelated REA analysis or new inference claimed.
