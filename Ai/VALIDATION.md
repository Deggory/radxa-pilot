## 2026-11-03 — C2 history-led Radxa adaptation checkpoint

Owner confirmed existing Radxa Q8B. Full C2 history/submodules now mapped:
35parent commits,50final/64historical paths,82paths total. Added standalone
receive-only Chimera mailbox16/health43 adapter with pinned identity/version
and modern CAN serialization. Corrected angle STATE1 producer contract in
opendbc86a839dcec8ed9a3e45315eac804fa1001f1b2d6.15USB/45port/53CAN/303broader
tests pass (314existing skips), history coverage and Ruff pass. No live output.
REA GNU symbols/disassembly confirms retained43/16contract; native/layout
limits retained. Sysfs shows Interceptor DAC Bench, not historical Chimera;
no device opened. Current model/DBC/owner settings unchanged. Next: actual
Chimera receive acceptance, units/profile and managed truthful health/ignition;
MCU safety/physical actuation remain unqualified. Full dated session and
Ai/Reports/retropilot-c2-history-20261103/README.md record evidence/limits.

## 2026-11-03 — C2 controller migrated to modern offline replay

Modern C2 steering/pedal/relay calculation and timestamped JSONL replay are
implemented in opendbc9da9210adfa4dc213424f36945caccd40182c80d. Explicit offline
calibration only; default absent. update() still returns zero actual output/no
CAN.44port/53CAN/303broader tests pass (314existing skips), Ruff/whitespace pass.
All8linked C2 blobs verified at b9a942e; canonical DBC, hostbus2 and CD210GPU
unchanged. Next: receive-only Chimera backend, producer/profile qualification,
then shadow/game-only loop and actual MCU safety. Hardware/game/vehicle control
remains untested. Full session: Sessions/2026-11-03-retropilot-controller.md.

## 2026-11-02 — BeamNG bundle audit complete; runtime adaptation still blocked

Audited collected source at projectbase f72a1ea/upstream5435d674. Added14missing
integration/import references; bundle now96files/1160682bytes, byte-identical
upstream. Allfile Git/SHA/mode/size checks;69Python AST/8bash/2JSON checks pass.
Fixed verifier accepting empty snapshots/wrong origin/pin/checksum list;12new
regressions pass, checksum-guard mutation caught. Snapshot tests with process-
local routing/current Sunny dependencies:164pass/6fail/1skip;2modules blocked
on import,1UI module not run. Five failures and two import blocks stem from
missing opendbc scale_tire_stiffness; onefailure assumes installed xdotool.
Test-only evdev2/mss10.2 installed under /tmp with locked SDist hashes; active
environment unchanged. UI/Lua/JS/Vue/game/model/manager tests not performed.

Source probes reproduce NaN accepted in96byte BPL1 and control-send called after
no new telemetry. Fork steering uses desiredCurvature→position, bypassing final
lateral torque; cannot directly validate custom actuator/NNLC. Same-hostIP,
camera1280vs1928, timing/freshness/session/finite and peripheral4vs2Hz require
adaptation. No copied upstream fixes applied to active runtime/DBC. Verdict:
reference bundle verified, direct runtime integration blocked. Next sim-only
recorded PC frame→VisionIPC/UI, then state/shadow and explicit lateral contract.
Detailed report: openpilot/tools/sim/beamng_reference/AUDIT.md; per-file/test
receipts alongside it. Relevant skills: source-first/code review, TDD/debugging,
git/docs. REA binary analysis not relevant to readable source/packet probes.

Collection validation: all82Git blobs and SHA256 checks pass,56Python AST,
8shell syntax and2JSON parses pass. Ruff passes for our verifier/discovery guard;
notebook66docs/213relative links pass. Using existing isolated pytest9.1.1,
reference-folder collect-only reports no tests collected (expected exit5),
confirming the new foreign snapshot is excluded. Active Sunny venv lacks pytest;
no package installed to change that. No game/model or foreign behavioral test.

## 2026-11-02 — BeamNG reference bundle integrity

82source files/1025072bytes match the pinned5435d674 Git blobs, SHA256 and modes;
56Python AST/8bash syntax/2JSON checks pass. Portable verifier and checksum list
are inside the bundle. These validate collection only; no original behavioral,
Lua/Vue/JS/game or managed integration test. Parent pytest discovery excludes
only the new foreign snapshot. Notebook/staged whitespace checked at commit.

## 2026-11-02 — BeamNG source-reference checkpoint

Fresh GitHub pin5435d674 matches savedOct28 source.3external/7local Python AST
checks, sim-launcher bash syntax, retained source/hash/compatibility assertions,
notebook66docs/211relative links and staged whitespace pass. Research/docs only:
no mod install, BeamNG/game-control/network/manager/model test. Public steerpilot
successor404 recorded; same-host source is not a ready PC↔Q8B adapter.
[Source receipt](Evidence/beamng-reference-20261102.json).

## 2026-11-02 — Fresh INT8 device baseline complete; accuracy rejected

Owner approved research continuation while retaining the failed strict FP16
check. Fresh Mountain Dew v3 W8A8 runs on actual Q8B SDK2.37/v68/SoC37:
200heldout calls exit0 plus3native-byte cases (all42heads bitwise equal).
Calibrated DLC400356844bytes; integer-IO DLC400346268bytes; context444203008bytes.
200MB goal unmet. After132warmup,68teacher-forced frames have normalized RMS
errors29.65% packed,46.16% lane_lines,16.78% plan,43.31% action and189.26%
hidden_state. These are raw tensor errors, not driving-accuracy loss. Candidate
remains unselected; current CD210/OpenCL preview ce7b047/eb741641 unchanged.

29focused tests/Ruff/two shell syntax checks and normal-venv CLI help pass.
Model numerical acceptance FAIL; strict calibration1value and heldout96prewarm
FP16 checks remain visible. Independent original FP32 agrees bitwise on ten
calibration cases and both failed heldout cases. All500 source-state transitions
were independently replayed. CPU backend crosscheck is unsupported at quantized
FullyConnected; PTQ/backend error contributions remain unresolved. No candidate
self-feedback or parsed driving metric after this failure. DSPs running, scoped
clock lease closed/restored, no owned workers. Entire15.6387s run is not a model
latency benchmark. Next: W8A16/mixed activation/output precision experiment with
8-bit weights, then matched heldout comparison and broader calibration; no
modeld selection or vehicle actuation. Actual commits/validation in Git/ledger.

[Measured results](../openpilot/selfdrive/modeld/npu/RESULTS.md).

# Validation: what is actually established

## 2026-11-02 — Q8B live onroad statistics complete

Owner-requested panel is on the actual Sunny AugmentedRoadView, enabled by
Q8B road-only mode; Q8B_SHOW_STATS=0 hides it. Shows hottest readable CPU/GPU,
fan PWM percent/raw/mode (RPM unavailable), GPU inference/readback, full model,
modelHz, camera→model and camera→UI first draw. Read-only sensors1Hz on a worker;
2s timing medians, display4Hz, stale timing1s/sensors3s, unavailable as dashes.
76tests/Ruff pass. Complete65sUI:1293camera frames/1274model messages/33path
points,20.0048Hz; inference10.933/12.133ms and capture→model36.832/41.043ms
median/p95. Overlay samples match model benchmark exactly; UI endpoint precedes
benchmark draw-ready by0.781ms median. UI benchmark draw-ready45.390/58.292ms;
host EndDrawing74.590/88.904ms. Physical display latency remains unmeasured.
Full65s child exits0/0/0; outer command143 after completion remains unexplained.
Independent cleanup passes; final10s command/children exit0,179matching packets,
zero rejections. Camera/clocks restored, GPUfaults0, fan mode staysautomatic.
Model/native/root helper hashes unchanged; no new conversion/calibration/control
or vehicle/hardwared integration. Data helpers committed5e01a48; this UI increment
and exact validation are saved in Git/ledger and the portable UI receipt.
Next: normal preview --model shows the panel; owner selects later work.
[Details](Knowledge/UI_TELEMETRY.md), [receipt](Evidence/q8b-ui-telemetry-20261102.json).


## 2026-11-02 — Resident GPU baseline complete

Q8B Thneed defaults to resident exact NV12 crop/packing/lag4 history, fresh60FPS
source selection at20Hz, and worker affinity on fast cores4–7. Scoped max clocks
are automatic; owner already installed the helper, no routine password request.
Existing CD210eb741641 remains unchanged; no conversion or feature splitting.
Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.
Calibration remains provisional/invalid, controls and DM off. No new20min soak,
full-manager/vehicle test or physical-display-latency claim. Unrestricted38.204ms
repeat and CPU7 regression40.512ms retained; adopted fast profile has two passes.
Next: launch normal preview from project .venv; choose later calibration/hardware
or optimisation separately. No active experiment or unfinished source edits.
This verified increment is recorded by its Git commit and maintenance receipt;
base623f728a, exact source/model/runtime hashes in the portable evidence.
[Details](Knowledge/MAX_PERFORMANCE.md), [receipt](Evidence/q8b-resident-20261102.json).

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

2026-11-02 resident final closeout:68tests/Ruff/native/accuracy gates pass;
notebook59docs/171relative links, regular tracked layout and diff whitespace
checks pass. Portable evidence is Ai/Evidence/q8b-resident-20261102.json.

2026-11-02 hardware-support mapping: documentation/source and saved-evidence
review only; notebook links/layout/index and diff whitespace pass. No runtime
tests rerun. See Sessions/2026-11-02-q8b-hardware-support.md and teacher report
sunnypilot-hardware-support-20261102 for actual output. Runtime ce7b047 unchanged.

2026-11-03 BeamNG optical/CAN layout: documentation-only validation PASS. 67 notebook documents/215 relative links/8 pinned repositories/4252 index entries; 7 current guides/26 relative links;96 preserved source files/1160682bytes; 12 existing verifier regressions and existing Waveshare offline self-test pass. No HIL runtime or hardware execution. Receipt Ai/Evidence/beamng-hil-layout-20261103.json.

Packaging correction: .gitignore PLAN.md rule omitted the linked plan from initial2968735. Explicitly track the plan in the follow-up; all5 active guides and linked file targets pass a Git-index presence check. Initial commit alone is incomplete; use the following checkpoint.

Validation PASS:70notebook documents/216relative links/8pinned repositories/4252index entries; docs README16relative links and safety symlink valid; staged whitespace check. No runtime/website build or hardware test.
