# Current Sunnypilot state

## 2026-11-02 — Temporary MM-X geometry selected and implemented

Owner: keep MM-X method for now, change later. get_device_camera_config now
returns borrowed720p/fx=fy900/centre640,360 for radxaQ8b/unknown only when the
existing Q8B_ROAD_ONLY+USE_WEBCAM mode validates the actual board. Cabin/wide
remain absent. Model/v2/UI share this lookup. Outside that opt-in mode, Q8B
calibration remains unconfigured; comma/PC profiles unchanged. Profile is not
measured AK calibration and supplies no distortion or mounting pose. Auto
calibration/target capture deferred; tools retained. Capture60/latest20Hz and
calibration-status/DM/vehicle policies unchanged. No camera/vehicle run.
30focused tests and lint pass; see temporary-mmx-profile session. Next qualify
current model/Adreno integration using this explicitly provisional geometry;
replace intrinsics later, do not auto-resume target/autocalibration work.

## 2026-11-02 — Automatic calibration requested: options explained

Owner asks how to automate intrinsics and extrinsics. Proposed auto-selection/
lens solve plus mounted camera/known vehicle-aligned target pose for R/t; target
motion/placement remains physical input. Current capture still requires Space;
no autosave or vehicle-pose export implemented. Online calibration assumes zero
roll and does not solve K/distortion/full6DOF. COLMAP target-free estimates are
an untested alternative, needing validation and vehicle-frame alignment.
No runtime/settings changed; next resolve preferred measurement workflow before
implementation. See automatic-calibration-options session for sources/limits.

## 2026-11-02 — MM-X RK lens-parameter check

Owner questioned the checkerboard step. RK3ad69b20 README requests external
intrinsics (example:GMLCCalibration); geometry/UI store720p focal900,centre640/360.
Online calibration estimates mounting alignment, assumes zero roll, and does
not solve lens K/distortion. His actual measurement procedure is undocumented.
Checkerboard is an available method, not a Sunnypilot requirement. Next resolve
an appropriate AK lens-parameter source; printing/capture is optional pending
method choice. No runtime edits or geometry activation; guard stays active.
Fresh5Git blobs/4Python AST checks pass; see dated mmx-camera-calibration session.
Prior29runtime/tool tests remain historical, not rerun for this source review.

2026-11-02 latest: padded model-facing NV12 fixed in6fea7ecf; real140frames and
synthetic current CPU-warp input parity qualified, not full inference. Printable
A4target and target/capture/solve calibration tool ready. Real lens/focus/mount
measurements remain pending; no automatic geometry registration. See HANDOFF.

2026-11-02 accepted camera increment: opt-in Q8B road-only AK720pMJPG60capture,
latest20HzNV12/IPC/messages, real driver timestamps and source sequence, optional
rotation(defaultoff), deferred driver camera.21tests plus140actual frame pairs
pass, helper/msgq build and settings restoration verified. Model/calibration
unchanged; full managed stack unqualified. See HANDOFF and latest session.

Current scope2026-11-02: camera work selected, hardware settings deferred.
Webcam source path identified; no capture/model run or application edit.
See [HANDOFF](HANDOFF.md) and [camera path](Knowledge/CAMERA_PATH.md). Older
camera-deferred/H1-next statements below are superseded for current work.

## End-of-day checkpoint — 2026-11-01

Owner finishing work and requested shutdown after audit. Resume2026-11-02 with
H1 real read-only thermal provider, following [handoff](HANDOFF.md) and
[hardware checklist](../tasks/todo.md). Planning baseline2963025 clean; fresh
11identity tests and notebook/index checks passed. Hardware implementation
remains pending; camera work deferred. See shutdown session for exact limits.

## Current focus — non-camera hardware, 2026-11-01

Owner deferred cameras. Read [hardware/sensor map](Knowledge/NONCAMERA_HARDWARE.md)
and [HANDOFF](HANDOFF.md). Board thermal/power/PWM interfaces are exposed; no
IIO motion channels found. Teacher records Adafruit LSM6DS3TR-C/I²C9/0x6a,
prior102Hz raw polling and1040 schema round trips; this uses raw I²C, not IIO. Inventory
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

Recorded 2026-11-01. Live Git and the upstream inbox take precedence over this
snapshot; refresh affected topics when source changes.

| Item | Recorded identity / status |
| --- | --- |
| Upstream reference q8b/sunnypilot-upstream | `a86979d2b2b176413a7f3e5cccf8c807596a7def`, `master`; advanced from `6f7a2c94` during the 17:10 UTC deployment check |
| Source headers | Sunnypilot `2026.003.000`, COMMA `0.11.3` |
| Observed host, 2026-11-01 | Ubuntu24.04.5LTS / Linux7.0.11-6-qcom / aarch64; exact DT Q8B token; protected port selects HardwareRadxa with generic Linux PC policy |
| Protected development | `sunnypilot`, `radxa/q8b`; identity implementation HEAD `12e44feeff241334e184c86dc9daccdc7f9e4fa1`; initial workflow HEAD `824be91b` |
| Stock model | SHA256 `65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce` |
| Stock checkout validation | Prior clean-start evidence verified 286 LFS assets and seven submodule pins; not a runtime test |
| Archived Q8B work | `q8b/preserved-sunnypilot-20261101`; old source/model/patched Adreno runtime retained separately |
| Legacy model | SHA256 `659727c4d4839adc4992a254409a54259a8756a743f2d567bf5fdc6579f8009b`; not the fresh stock model |
| Legacy worker | `q8b/gpu_webcam`, `radxa/legacy`, `5a8fd13ba0b252091d7448017537e798144aa0ba`; frozen helper imports |
| Daily vendor workflow | 15:30 UTC persistent user timer; only vendor advances, port and notebook remain protected |
| Managed Sunnypilot on Q8B | Identity implemented and focused checks passed; managed runtime remains unqualified, stock-contract preflight next |

Completed knowledge work: source/version/fork selection, fresh stock checkout
and preservation, daily commit tracking, system-folder source map, and this
specialist notebook. The latest source index pins actual superproject and
dependency trees; its coverage is navigation, not full code review.

Key findings: actual services live under `openpilot/system`; root `system` is
only an AGNOS-manifest compatibility link. Hardware selection lives under
`common/hardware`; vendor defaults to PC without `/AGNOS`, while our protected
port now selects HardwareRadxa on the exact Q8B device-tree token. Webcam selection does
not enable our MSM Adreno runtime. Live sensors, native UI, lifecycle and the
new stock model contract still need integration and tests.

Latest upstream delta: a86979d2 changes only Sunnylink visual-setting metadata
to hide the Steering Arc toggle on `mici` (comma four). It does not change the
lateral model/controller. Inspected and explained; not merged into the protected
port. The notebook's original source-index pin became stale after the real
update and was refreshed; the historical system review remains pinned to6f7.
