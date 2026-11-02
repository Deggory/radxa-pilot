# Existing Thneed import — 2026-11-02

Owner requests student use teacher's testedCD210 Thneed work inside sunnypilot,
explicitly do not convert again if artifact exists. Starting source
6df9a8f92626135b1d475a3ad6822f0edfa4d531/radxa/q8b, clean.

## Completed scope

Copied existing artifacts/driving-02.thneed→models/q8b_cd210.thneed,99641029bytes,
SHA256eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068.
Metadata/fixtures also copied byte-identical; fixturesae51e3d9...,5123782bytes.
Models tracked by LFS. No ONNX→Thneed converter/exporter was invoked or imported.
Kept original ONNX/Tinygrad models, current pin92b742f7 and camera code unchanged.

Copied native bridge, adapted historical portable C++ replay, pinned vendor
headers/json11/licenses/manifest and build script into modeld/thneed_q8b.
New runtime creates matching GPU context through ctypes/installed OpenCL,
loads saved kernels directly, uploads exact typed inputs and retains GPU buffers.
No experiment paths, old Tinygrad import/patch or external asset runtime lookup.
Build compiles native ARM64 replay library only, not the model. Trusted artifact
checksum/size and metadata pin checked before native loading; GPU driver must
match saved Qualcomm Adreno690 OpenCL0855.3/E031.50.31.01, no CPU fallback.
Build ELF SHA2565f83b4ad6d1b083cfe336571d06c8f3b280a307aeaaf7b5f5b1ddecef349adec.

Current queue adapter follows pinned ONNX65a08adc Slice/Concat/ReduceMax:
shift images then select0,4; group100desires by4/max; features0::4; append512
output features at1064:1576. It accepts prepared two-view model input, not raw
camera images. It returns next states without modifying caller input.
SameCD210 learned core; precision stays accepted FP32 arithmetic/FP16 output.
Added README/CLI/provenance and corruption/contract/history regression tests.
Initial staged diff check found inherited extra EOF blank lines in two vendor
files; normalized only those endings, retaining original SHA provenance. No
validation suppression or semantic change. Model/metadata/fixtures unchanged.

## Actual validation

TDD red: missing runtime module, then four contract cases green; later fifth
ensures wrong artifact rejected before any GPU/native access. Full focused
suite42passes (five new +37camera/identity regressions), Ruff and diff checks pass.
Native build passes using copied sources and installedg++/libOpenCL, assertions
on. Direct first GPU replay matches savedCL exactly and independent savedCPU
rtol.001/atol.005. Fresh in-project verifier repeats6cases twice:12exactCL/CPU
checks plus12current-queue adapter cases, all2576outputs finite and equal.
40timed calls/10warmups, input upload+replay/readback+validation12.1140275ms
median/15.8506154msp95, no camera/UI. Before/after CPU/GPU policies match;
no clock/fan/driver setting written. After whitespace-only vendor cleanup, native
rebuild SHA is identical. Repeated40call verifier passes all12+12cases, timing
14.22337/16.54539ms p50/p95 under unchanged dynamic policies. Both receipts
retained, no fastest-run selection. Host check is not old inference-only timer.
No fresh GPU-fault counter measurement or20min/maxclock/camera qualification.
Reference source remains teacher Oct30 trial and Oct31 soakdb5b0da; no new
original-model CPU inference needed because saved independent references reused.

Tracked evidence: [import validation](../Evidence/thneed-q8b-import-20261102.json).
Optional raw logs/report: central Ai/Reports/sunnypilot-thneed-import-20261102/.
Required runtime code/assets remain entirely inside Sunny. Generated native
build library ignored; source/vendor/assets/provenance tracked. Build/run in
[README](../../openpilot/selfdrive/modeld/thneed_q8b/README.md).

## Scope and next step

Copied asset + independent inference backend/current-input adapter completed.
Manager/modeld selection not switched, no camera capture or modelV2 publication
run. Next integration is explicit backend selection and live modeld/queue/parser/
message/overlay qualification, then recurrent20Hz timing. Do not reconvert or
copy old Tinygrad wholesale. Keep camera latency/calibration optimisation parked.
No vehicle-actuation/safety-policy change. No upstream merge/rebase/push.

Skills: incremental implementation, test-driven development, performance,
source-driven review, documentation, code review and Git. REA fast path used
readable pinned source, direct ELF identity/hash and actual replay evidence;
no unrelated decompilation or fabricated REA tool result. Both memory layers
updated with accepted scope/source/runtime pins, checks and exact next step.
