# Camera-to-UI benchmark — 2026-11-02

Owner requested actual camera-to-UI benchmarking. Source base5b9704faada74fa4764d72ee0fabd812b2a345f7,
radxa/q8b, clean at start. Added webcam/benchmark.py, test_benchmark.py and
opt-in preview.py flags; README documents exact reproducible command.

Completed65.057srun with5s warmup:1298unique rows retained,98warmup excluded,
1200steady samples,19.97562new frames/s.648repeated redraws in total and1skipped
publication ID in steady data, not a claim about underlying60FPS sensor losses.

| Endpoint from V4L2 driver timestamp | Median ms | p95 ms | p99 ms | Max ms |
| --- | ---: | ---: | ---: | ---: |
| Draw commands ready |59.398|78.755|87.499|100.660|
| Host EndDrawing returned |89.385|109.139|117.940|131.143|

EndDrawing itself30.126msmedian includes normal30FPS UI pacing. These timings
do not establish GPU completion, actual compositor presentation/scanout or
optical exposure-to-monitor-light latency. Draw-ready is CPU command preparation.
No additional GPU fence, clock boost, fan setting or FPS change was introduced.
Timing hook is installed only in the isolated benchmark UI child and restored
on exit. Buffer/IPC frame IDs must agree; metadata is captured before the host
call. Reject invalid clocks/frame reversals; keep first completion and all raw
warmup/steady rows. Write raw data after run, without per-frame disk writes.

Actual desktop GL:freedreno FD690,OpenGL4.6 Mesa25.2.8-0ubuntu0.24.04.2;
1824x912window/render target. Capture720pMJPG60negotiated/latest20Hz,normal
onroad/HUD30FPStarget. GPU simple_ondemand270..690MHz,CPU schedutil,governors
and bounds preserved. Camera previous1080p30MJPG/dynamic-framerate1 restored
exactly. Camera/UI exit0/0; no remaining preview owner. No model/planner/vehicle/
control/DM/recording processes. Temporary MM-X900px intrinsics unchanged.

37focused tests pass, Ruff passes. Tests cover percentile arithmetic, duplicate
handling, warmup/incomplete results, bad timestamps/frame IDs, original frame
metadata preserved across host call and buffer mismatch rejection. Initial RED
was missing new timing module. Independently recomputed raw-record identities,
strict clock/ID order, linear p95/p99/median/mean/min/max and FPS; all agree.
Camera before/after files match byte-for-byte. Notebook/diff checks saved at
closeout; no test threshold weakened. Source-first/actual runtime evidence used.

Optional workspace evidence:Ai/Reports/sunnypilot-camera-ui-benchmark-20261102
contains REPORT.md,run/{timings.jsonl,benchmark.json,session-result.json},test log,
source hashes/environment and validation.json. Exact measured source SHA256s
are in environment.json. Stock model65a08adc,raylib6.0.0.1.post103,
msgqe7396e76,tinygrad92b742f7 unchanged; no upstream merge. Older Oct31
Thneed/EGL/max-clock42.186/56.996ms numbers remain a separate pipeline/endpoint.

Skills: performance-optimization, observability, incremental implementation,
test-driven-development, code review, source-driven/documentation/Git workflow.
Inspected actual msgq/UI loop and installed graphics backend; measured native
runtime. No unrelated REA artifact analysis needed or claimed. Next profile
stages/optimise only if requested; current model/Adreno integration remains open,
automatic lens calibration remains deferred. This benchmark is not road proof.

Closeout verification:47notebook documents/100relative links/8source repos/
4252index entries pass. Diff whitespace checks pass. Measured preview/benchmark
source SHA256s still match the run; no implementation changes after measurement.
37tests/lint and independent raw metrics pass. No uncommitted owner files at
start; verified increment committed and validation attached to maintenance.

## 2026-11-02 — Camera bring-up accepted for now; optimisation deferred

Owner says camera work is done for now and will return to teacher knowledge
later to reduce delay. Preserve current capture/UI and temporary MM-X geometry.
Benchmark baseline7ac07b5:1200steady frames/19.97562FPS; driver→draw-ready
59.398msmedian/78.755msp95; driver→EndDrawing return89.385/109.139ms including
normal pacing. No further camera optimisation/calibration changes now.
Future work starts from teacher camera/Sunnypilot notes and the Oct31 retained
pipeline report/source db5b0da, with its different model/runtime/max-clock
conditions kept explicit. Compare matching endpoints/profiles before porting.
Current optics/mount and full model/vehicle qualification remain open; owner
acceptance covers camera bring-up/preview/benchmark milestone only. No next
engineering task selected in this message. No runtime changes or new tests.

Documentation/Git skills used for owner-directed scope checkpoint. Source-first
existing teacher evidence; no unrelated REA analysis or hardware access needed.
Application source/model/runtime pins and existing37-test result unchanged.
