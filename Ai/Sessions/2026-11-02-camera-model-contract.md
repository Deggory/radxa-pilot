# Model NV12 layout and input qualification — 2026-11-02

Baselinef4f4d01d2c8c8c5bcaeee3a1ed081a1c6fd08aab/radxa/q8b. Owner said proceed
with geometry/model contract; then explicitly selected printable target/tool.
Teacher search found only70degvisual estimate/zero mountangles/1.22mheight,
not measured lens intrinsics. No fabricated calibration installed.

2026-11-02 model-input qualification: reproduced old packed720pbuffer failing
current modeld's1,413,120byte copy. Road-only output now uses get_nv12_info:
stride1280,Yrows736,UVrows368,UVoffset942080,allocation2,220,032bytes with neutral
padding. Generic mode unchanged. Added Q8B-only720pwarp build configuration.
23focused tests pass;140real frame pairs pass20.001Hz/59.628sourceHz with exact
layout/copy/padding/timestamps and restored settings. Pinned tinygrad92b742f7
CPU warp matches independent NumPy reference for two distinct synthetic views
bitwise; outputuint8[2,6,128,256] matches current ONNXnew_img metadata. No full
model/GPU/managed run or measured geometry claim. Weights65a08adc unchanged.
Owner selected printable target/tool; that next increment is in progress and
calibration guard stays active. New unstaged test_calibration.py is expected
RED until tool implementation; do not mistake it for a failure of this slice.

Actual current ONNX SHA65a08adc retains new_img uint8[2,6,128,256], recurrent
image queue[2,5,6,128,256], desire queue[100,1,8], feature queue[96,1,512]; outputs
[1,2576] plus next states. One physical narrow camera supplies both logical
views in current stock modeld. Inspecting safe ONNX protobuf did not execute
model or unpickle foreign data. CPU-only pinned current warp used synthetic
integer translations, no measured lens/Adreno performance conclusion. Unset
incompatible inherited DEBUG=release locally as DEBUG=0 for probe; no global
configuration change. Fixed probe CPU-device alias to match Device.DEFAULT.

Test-driven/source-first/incremental/debugging/review workflows used. Source
READABLE, no unrelated REA invocation. New red regression raised buffer smaller
than requested before fix;23focused tests now pass. Real IPC receiver uses actual
model byte count and verifies neutral padding. Native layout rule follows current
repo helper, not old legacy calibration. Existing Q8B detection tests remain.
SConscript AST tests check720p registration; actual warp build/full model not
claimed. Raw Ruff on SConscript reports pre-existing SCons implicit-global
issues; normal .py lint plus syntax/policy checks used instead of suppressions.
Evidence: central Reports/sunnypilot-camera-contract-20261102.
