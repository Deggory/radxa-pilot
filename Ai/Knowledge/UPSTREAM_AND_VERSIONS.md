# Source identity and update workflow

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

Snapshot 2026-11-01: vendor master `a86979d2b2b176413a7f3e5cccf8c807596a7def`,
advanced from `6f7a2c94` during the real maintenance check. Source headers remain
Sunnypilot 2026.003.000 / COMMA 0.11.3. A version header alone does not identify
a source snapshot, release artifact, model or hardware target. Branch tips can
move; use full Git/model hashes and recorded dependency pins.

The protected clone began at the same upstream base plus workflow docs at
`824be91bbffed684bb91fb932e9cb7e509c76dc3`. Local memory-routing changes are
separate commits and do not integrate new upstream code. Source index and
bootstrap evidence record exact identities; live Git is authoritative.

| Location | Automatic behavior |
| --- | --- |
| `sunnypilot/` vendor | Daily fetch, commit journal and guarded fast-forward, assets and pinned dependencies |
| `q8b/sunnypilot-radxa/` | No automatic merge/pull/rebase/reset; discussion before upstream integration |
| `q8b/gpu_webcam/` | Protected legacy worker with frozen imports; scanned for local commit records |
| `q8b/sunnypilot-memory/` | Independently versioned notebook; local commit hook plus recovery scan; daily job only reads it |

The user timer runs at 15:30 UTC with persistent missed-run handling. It needs
the board/user service/network/disk available. It records newly observed
superproject commits, including side/merge commits, changed paths and related
review flags. Dependency pins are tracked, not every internal dependency commit.
Path classification is mechanical; it is not autonomous AI compatibility review.

The local `Ai` and vendor `AGENTS.md` links are excluded using Git metadata,
not edits to upstream .gitignore. Before vendor advancement, reserved-path
collisions are blocked and queued for discussion. The outside backing folder
is retained. Do not use reset/clean/stash to make an unexpected dirty tree pass.

At every chat: read the [live inbox](/home/radxa/comma/Ai/SUNNYPILOT_UPDATE_INBOX.md),
raise pending related commits/failed checks or a stale job, inspect source diffs,
and explain tests/impact before integration. Silence is not approval. The owner
selected next-chat discussion only. Sunnypilot's own updated service is separate
from this maintenance controller and must not bypass protection.

Primary local policy: [upstream policy](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_UPSTREAM_POLICY.md).
Controller commands and units: [maintenance README](/home/radxa/comma/q8b/sunnypilot-maintenance/README.md).

The a86979d2 delta modifies only `sunnylink/settings_ui.json` and its
`settings_ui_src/pages/visuals.yaml` input: the TorqueBar/Steering Arc setting
gets a not-mici visibility condition. This is remote-settings metadata, not a
lateral control algorithm change or Q8B integration. Protected port stays at
its prior upstream base. The commit was journaled, and the live source index
was refreshed after the stale-pin check caught the vendor advance.
