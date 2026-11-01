# Radxa Q8B: selected scope and existing work

## 2026-11-01 — Working project is sunnypilot; notebook is inside it

Owner clarified that `sunnypilot/` is the actual project and other workspace
folders are references/support. The existing radxa/q8b repository was moved
from q8b/sunnypilot-radxa into sunnypilot, preserving identity commit12e44fee,
all Git history, assets, submodule pins and IDE files. The clean upstream copy
is now q8b/sunnypilot-upstream and remains the only daily-updated checkout.
No upstream code was merged. The former project path is a compatibility link.

`Ai/` is now a real directory versioned with the project, copied from notebook
ed8afade without nested Git. The old notebook repository retains history only.
Active code, README and knowledge belong here; external references are optional
context and do not supply the new identity implementation at runtime.

See [README](../../readme_wat_we_did.md) from this Ai directory, or
[location session](../Sessions/2026-11-01-project-location.md). Earlier recorded
paths/roles below are historical and must be interpreted using their source
pins. This move does not qualify camera/model/UI/sensors or vehicle actuation.


## 2026-11-01 — Q8B identity implemented and checked

Owner authorized Ubuntu/Linux, ARM64 and Radxa Dragon Q8B identification.
Protected `radxa/q8b` commit `12e44feeff241334e184c86dc9daccdc7f9e4fa1` implements exact device-tree detection,
Python/C++ HardwareRadxa and local cereal enum `radxaQ8b @8`, preserving existing
ordinals and generic Linux `aarch64`, `COMMA_HARDWARE=False`, `PC=True` policy.
The read-only command reports actual Ubuntu24.04.5/ARM64/RadxaDragonQ8B. Dynamic
camera consumers explicitly reject missing Radxa calibration. No comma camera
calibration is claimed for this board.

11 Python tests, 4 actual C++→Python deviceState/initData message checks, SCons
profile detection, Ruff, syntax and diff checks passed. A detection mutation
was rejected by the tests. No full Sunnypilot build, camera/model/UI launch,
MSM runtime integration, hardware-health measurement or vehicle actuation was
performed. Generic hardware defaults remain unimplemented health providers.
Vendor stays clean at a86979d2; no upstream merge/push.

[What we did](/home/radxa/comma/q8b/sunnypilot-radxa/readme_wat_we_did.md) ·
[Evidence](/home/radxa/comma/Ai/Reports/radxa-board-identity-20261101/REPORT.md).

Earlier source-only explanations below retain their original scope and pins.

Current owner goal: Sunnypilot on Q8B/Linux, eventually lateral control with a
custom steering actuator. Native camera/model/messages/UI is the first milestone.
The protected source clone is `q8b/sunnypilot-radxa`; the vendor is an upstream
reference. This notebook does not change that separation.

## Existing evidence we can reuse

There is measured standalone USB camera + patched MSM/Adreno model execution,
preprocessing, frame history and preview work. Read the
[central compute/camera audit](/home/radxa/comma/Reports/sunnypilot-radxa-audit-20261027/reviews/COMPUTE_CAMERA.md)
and the newer measured reports routed by the workspace plan. Their exact model,
precision, timing, camera and clock conditions matter; do not combine unrelated
benchmarks into a new performance claim.

The old model, custom checkout/history and runtime archive are preserved under
`q8b/preserved-sunnypilot-20261101`. The active legacy worker reads frozen old
model/helpers, so the daily vendor update cannot silently change its contracts.
The fresh stock ONNX is different. Archive availability is not a decision to
insert the old model/runtime into the new integration.

## Required adapter boundaries

1. Pin current source/schema/model/parser/runtime. Establish real dependencies
   and build the message/buffer extensions needed for an isolated test slice.
2. Publish standard camera streams and metadata with real acquisition clocks,
   sequence IDs, calibration, color, dimensions, stride/UV layout and lifetime.
   The stock webcam example is a reference, not our final capture provider.
3. Connect the chosen runtime explicitly. The current non-comma stock build
   selects CPU:LLVM and Sunny's modeld_v2 chooses CPU outside comma hardware;
   the existing patched MSM/Adreno runtime is a different implementation.
4. Publish complete model messages with actual recurrent state/input/output
   contracts and frame pairing; consume them in the real raylib Sunny UI.
5. Add actual sensors, thermal/power readings and managed lifecycle/fault tests.
   Generic PC stubs are not healthy sensor readings.
6. Later, separately integrate vehicle state and custom steering feedback/safety.
   Shared RetroPilot CAN definitions come from the
   [canonical DBC policy](/home/radxa/comma/Ai/Knowledge/CAN_DBC_POLICY.md).

Detailed current source explanation: [SYSTEM.md](SYSTEM.md). Active next step:
[TASKS.md](../TASKS.md). Durable cross-project plan:
[SUNNYPILOT_RADXA_PLAN.md](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_RADXA_PLAN.md).
