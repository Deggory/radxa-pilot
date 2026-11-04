## 2026-11-04 — GitHub master checked; all upstream updates on hold

Live GitHub master is8cf6ff9a (predictive acceleration boost,#2089,Nov4UTC).
It adds AccelBoostSP/defaulton, longitudinal boost logic, settings and tests.
Previousa86979d2 gates sunnylink steering-arc toggle on MICI. GitHub is2commits
ahead of our6f7a2c94 upstream base,1ahead of the previous a869 reference check.
No source integration or compatibility test performed. Actual project master/
origin-master remain6f7a2c94; Radxa code and child671f8c4 unchanged.

The daily job already advanced only the reference to8cf6ff9a at15:30UTC before
the owner asked. New owner instruction requires approval before updates.
Automatic timer is now linked/inactive and not enabled for automatic startup;
service inactive. Do not run mutating updater check or reenable it without
explicit approval. Read-only GitHub checks are allowed. See current upstream
policy, receipt Evidence/sunnypilot-master-check-20261104.json and dated session.

## 2026-11-04 — Owner-authorized topic labels applied to Git history

Camera/Thneed/RetroPilot subjects now use camera, thneed and retropilot scopes.
64titles reworded;28camera/16thneed/29retropilot commits, with mixed scopes.
90IDs changed by ancestry; all92local file trees, dates and message bodies match
originals. New tip before report213cd6d9; original6fb457bc retained under
refs/backups/20261104-before-topic-reword. Child671f8c4/gitlinks unchanged.
Original recorded SHAs are historical evidence, not stale hashes to replace:
use Ai/Reports/commit-topics-20261104/commit-map.csv or mapping.json to resolve
current IDs.90validation histories inherited without rerunning tests;17raw
failed/blocked IDs represent9original lineages, no new software-test failure.
No code/device/DBC/model/firmware or remote change. Preserve noOutput and holds.

# Source identity and update workflow

## 2026-11-02 — All project work committed

Owner requested a complete commit checkpoint. Git audit found a clean
radxa/q8b tree at49d2f07432541d9456acb60369a8f959db4c5611. All57tracked local
commits had validation records; latest GPU increment has a passing receipt.
This documentation checkpoint records that audit. Runtime/source/model are
unchanged; previous68tests and hardware benchmarks were not rerun. Next task
remains owner-selected calibration/hardware or optimisation, with controls off.


## 2026-11-02 — Thneed confirmed as CD210 core

Old tested659727c4 and currentCD21065a08adc share checkpoint/learned weights;
ONNX wrapper differs. Thneedeb741641 traces to old graph via exporter provenance.
[Direct tensor-content confirmation](../Sessions/2026-11-02-thneed-cd210-confirmation.md).

## 2026-11-02 — Big Tinygrad is an AMD artifact; historical NPU path exists

Bundled big pickle799941965bytes/SHA256d4c7a3fc; bounded opcode inspection
confirms Tinygrad/AMD/LLVM, and helpers selects USB+AMD:LLVM for Chestnut.
Teacher historical big ONNX6fee5937 already runs as QNN2.37/v68 W8A16 context;
Oct31 graph38.196ms/host41.515ms medians exclude camera. Graph/weights identity
to this Mountain Dew v3 artifact is not established; quantized parity is not
floating-reference accuracy. No current Sunny NPU integration or inference.
See [detailed review and pins](../Sessions/2026-11-02-big-model-npu.md).

## 2026-11-02 — Bundled driving model identified as CD210

Configured default:CD210, ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391,
openpilot/selfdrive/modeld/models/driving_supercombo.onnx,60918562bytes.
Actual SHA25665a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce.
Recomputed the tracked small-model identity fingerprint from ONNX SHA/name/ref:
afa673add3ffdff2607c4968912a0183c5883fd0159d56218a3c22a508a2ebd5 matches
models/tests/model_hash. Name/ref also match pinned official upstream model_name.py
at6f7a2c94c10dffcf9a83b120ab1e6985e4496868 (blobbd8e9ac2). This establishes
the bundled checkout identity, not a claim about newest online catalog entries
or the exact historical training/release date.

Protobuf metadata:PyTorch2.13.0+cu130 exporter; ONNX new_img uint8[2,6,128,256]
plus desire,traffic_convention,action_t and image/desire/feature state queues.
Output float[1,2576] plus next state queues. Parser/fill source describes path,
velocity/acceleration, lanes, edges, leads and pose. Current model constants target
20Hz. The two logical image views need not imply two physical cameras; existing
single-road-camera path reuses its frame for distinct model view transforms.

The separate big_driving_tinygrad.pkl is configured as Mountain Dew Model v3,
ref1e219d7785cfb7b7343c7f2366347fc86e7ce5f2, for the Chestnut/big model path.
Do not call it a larger copy of CD210. No big pickle was deserialized for this
identification. Driver-monitoring ONNX is also a separate network, deferred here.
No model inference or current Adreno compatibility is proven by identity checks.
See [identity session](../Sessions/2026-11-02-model-identity.md).

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
