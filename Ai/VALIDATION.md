# Validation: what is actually established

## Per-frame camera-to-UI timing — 2026-11-02

37focused tests/lint pass. Live65s/5swarmup:1200steady first-display rows,
19.98FPS; driver→draw-ready59.398/78.755msmedian/p95 and driver→EndDrawing
return89.385/109.139ms, normal pacing included. Actual freedreno FD690 renderer.
Independent Python median/manual linear percentiles and raw time/ID identities
match. Camera/UI exit0/0, camera format/rate/control and clock policies restored/
preserved. No full manager/model/optical presentation test. Report contains
all raw rows/warmup and hashes. Existing no-latency-logging note is historical.

## Camera dashboard — 2026-11-02

32focused tests pass, including private environment and owned-child cleanup.
Fresh native Params build and pinned raylib6.0.0.1.post103 wheel SHA verified.
Live9.06s native onroad window rendered173distinct camera frames; screenshot
viewed. Later4s lifecycle exits camera/UI0/0; camera prior1080p30MJPG and
dynamic-framerate1 restored exactly. First screenshot attempt used an absolute
path unsupported by TakeScreenshot; retained log, corrected to relative path
and verified actual file. No model/vehicle/full-manager/recording test.

## Temporary MM-X camera profile — 2026-11-02

30focused calibration/camera/identity tests pass; lint passes. Added test
first failed at the existing missing-geometry guard, then passed with scoped
profile. Checks actual matrix projection/inverse, one camera, rejects other
sensors/non-Q8B/missing USE_WEBCAM, preserves ordinary PC/comma and default
unconfigured behavior. No physical capture, UI render, inference or vehicle
test. Prior live140frame/CPU-warp evidence retains its original scope.

## MM-X RK camera-calibration source review — 2026-11-02

Fresh5full GitHub blobs match exact Git identities at3ad69b20;4Python files
parse. README calibration instruction and matching road/UI focal900/720p
constants checked. No camera/model/runtime run or physical lens calibration;
prior29focused tests are not repeated or newly claimed. See source manifest
and verification in optional workspace q8b/research/mm-x-camera-20261102.

## Model boundary and calibration preparation — 2026-11-02

Model-facing allocation now2220032bytes/UVoffset942080,copy1413120bytes for720p;
old packed frame demonstrably failed.23camera/identity tests and140new actual
IPC/Cereal pairs pass; pinned CPU warp exact two-view uint8[2,6,128,256] matches
ONNX metadata. Source-only720pbuild registration tested; no full model run.
6additional calibration tests verify physical target dimensions, detector,
known-camera recovery, bad/repeated/high-error data rejection and no overwrite/
changed-image protection. PDF A4checked, actual rasterized target grid detected;
real Tk/Pillow GUI path tested with synthetic frames, duplicate save rejected,
source closed. No physical checkerboard images/real lens solution collected.
Q8B calibration guard and model weights/runtime remain unchanged.

## Road-only camera patch — 2026-11-02

21focused tests(10camera+11identity); strict C compilation and actual new SCons
helper target; current pinned msgq e7396e76 Python/VisionIPC bindings built.
140real720pNV12 IPC/Cereal frame pairs, one road stream, timestamp/ID pairing,
~20Hzpublication/~59.64Hzsource sequence, exit0 and full prior format/rate/
dynamic-framerate restoration observed. Driver timestamp→receiver40.244ms median
and62.580ms max is not inference/optical latency. Initial dynamic-rate1 test
delivered~24sourceHz; retained as a failed cadence check and corrected with
temporary control0. No camera owner remains. No full build/manager/model/UI/
calibration/vehicle test; prior standalone model benchmarks remain separate.

## Shutdown audit — 2026-11-01

At source2963025, all11Python hardware identity tests freshly pass. Notebook
layout/links/eight repository pins/4252index entries pass. Project, upstream
reference and maintenance worktrees clean; later application diff from identity
12e44fee is empty. Journal has no missing validation or pending upstream review;
two corrected historical failure records retained. Timer active/persistent,
service last result success. These checks do not qualify thermal/power/IMU/fan
providers or a full managed runtime. Native wire/build-profile results remain
prior scoped evidence and were not rerun for this documentation-only checkpoint.

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

| Evidence | What passed | What it does not establish |
| --- | --- | --- |
| Fresh stock checkout | Prior verification of 286 LFS payloads, stock model hash and seven dependency pins | Build, inference or Q8B integration |
| System source review | 193 Git/content checks, 139 Python AST parses, documented local-link checks | Every line/register/firmware audited or runtime tests passed |
| Daily controller with memory protection | 31 real-Git unit tests; 3 new collision regressions failed before the fix | Semantic compatibility of upstream changes |
| Legacy standalone worker | Prior 15 CPU regression tests after helper-import isolation | Fresh stock model or managed Sunny runtime qualification |
| Notebook installation | Source-index completeness, document links, local mounts/exclusions and Git/journal readback recorded in bootstrap report | Complete knowledge of all algorithms or a running background AI |

Current evidence: [memory setup report](/home/radxa/comma/Ai/Reports/sunnypilot-repo-memory-20261101/REPORT.md),
[system review](/home/radxa/comma/Ai/Reports/sunnypilot-system-review-20261101/REPORT.md).

Deployment check: the actual user update service succeeded on 2026-11-01 at
17:10:53 UTC, Result=success / ExecMainStatus=0. The timer remained active with
next run 2026-11-02 15:30 UTC. It advanced vendor from6f7a2c94 to a86979d2 while
preserving the local links and protected port/notebook. This checks maintenance behavior,
not Sunnypilot runtime or hardware compatibility.

The first post-service notebook check failed because its original vendor pin
was stale. That failure is retained as notebook-stale-pin.log and recorded
against documentation commit02bf09e8. Its premature no-advance statement is
corrected here without rewriting Git history. The source index/current-state
pins were refreshed before repeating the same verification command.

Every future session records the exact command, source identity, outcome and
saved log. Mark an unavailable dependency as blocked; do not substitute syntax
checks for a build/runtime claim. The post-commit hook records commits, not
invented test success. Attach validation explicitly through the controller:

```bash
python3 /home/radxa/comma/q8b/sunnypilot-maintenance/updater.py \
  --config /home/radxa/comma/q8b/sunnypilot-maintenance/config.json \
  validation --sha FULL_SHA --command 'EXACT CHECK COMMAND' \
  --result pass --evidence '/absolute/path/to/saved-log'
```

## Relocation verification completed

From the canonical sunnypilot path:11 Python identity tests,4 native C++→Python
message checks and the actual SCons platform probe passed. Application/build
source is unchanged from12e44fee and both IDE files are byte-identical. The
31-test updater suite passed. Project-local notebook verification passed24docs,
51 relative links and the eight-repository/4252-entry vendor index. A temporary
standalone copy of Ai plus project documentation passed without the workspace.
Verifier Ruff/AST and Git diff checks passed.

The actual retargeted daily service succeeded2026-11-01 20:39:22UTC with exit0,
observing upstreama86979d2. Project HEAD/status and selected source/notebook
hashes stayed identical through the service. Persistent daily timer is enabled,
active/waiting, next run2026-11-02 15:30UTC. No new pending related upstream
commit was discovered. Historical02bf09e8 notebook failure remains retained in
the ledger; it is not a current relocation or application failure.
