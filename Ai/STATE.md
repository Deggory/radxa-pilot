# Current Sunnypilot state

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
