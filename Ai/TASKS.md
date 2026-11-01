# Work status and next task

## Current focus — non-camera hardware, 2026-11-01

Owner deferred cameras. Read [hardware/sensor map](Knowledge/NONCAMERA_HARDWARE.md)
and [HANDOFF](HANDOFF.md). Board thermal/power/PWM interfaces are exposed; no
IIO motion channels found. Actual IMU model is pending owner input. Inventory
only, no driver/config/runtime change. Next candidate: read-only thermal mapping,
then verified power reporting and actual IMU provider. Earlier camera/model
T0next-task advice below is deferred by the current scope.

Current restart checkpoint and next step: [HANDOFF.md](HANDOFF.md). Agent Skills
+ REA and both-memory closeout are standing defaults, including after reopening.
No additional hardware/runtime implementation was made by this workflow task.

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

See [README](../readme_wat_we_did.md) from this Ai directory, or
[location session](Sessions/2026-11-01-project-location.md). Earlier recorded
paths/roles below are historical and must be interpreted using their source
pins. This move does not qualify camera/model/UI/sensors or vehicle actuation.


Current owner authorization,2026-11-01: implement Linux/ARM64/Q8B board identity
and save a README. This is complete in protected port12e44fee. It supersedes
the earlier identity implementation hold; it does not authorize other hardware
providers, model integration or vehicle actuation. Daily vendor/memory work
continues under the standing policy.

## Completed

- Implement Q8B identity across detection, Python/C++, schemas and camera guards;
  11 Python/4 native checks and SCons-profile/lint pass. See
  [README](/home/radxa/comma/q8b/sunnypilot-radxa/readme_wat_we_did.md).

- Preserve previous Q8B source/model/runtime and start a clean stock vendor copy.
- Separate protected Radxa development from the daily-updated vendor.
- Track upstream/local commits and explicit validation; discuss related updates
  in the next chat.
- Explain the system tree and hardware boundary at source pin `6f7a2c94`.
- Create shared specialist memory, seed known facts and reserve its local links
  against conflicting upstream updates.

## Next implementation: T0 stock-contract preflight

Read the [workspace plan](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_RADXA_PLAN.md).
Work in this sunnypilot project. Establish actual dependencies, schemas, current
stock model inputs/outputs, parser, chosen runtime and camera buffer contract.
Do not silently insert the preserved old model/runtime into fresh stock code.

Then pursue a bounded recorded-input camera → model messages → actual Sunny UI
slice; qualify live capture/IMU/health and managed fault recovery afterward.
Vehicle/custom-actuator work is a separate later milestone with canonical DBC
and explicit measured feedback/safety requirements.

## Notebook upkeep after each task

Update only relevant topics and state; append a dated session with exact
source pins, changed paths and validation. Record unknowns honestly. Promote
cross-project facts to main Ai and commit the notebook with its journal hook.
Do not turn an old completed task into the next task because it appears in
an imported historical note.
