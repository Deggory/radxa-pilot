# Resume Sunnypilot here

## Approved camera patch completed — 2026-11-02

Owner approved AK-Camera720pMJPG60capture/20Hzlatest publication, only road camera,
optional rotation defaultoff, real timestamps, self-contained capture helper
and opt-in driver-camera deferral. Implemented in webcam camera.py/camerad.py,
config.py/native_capture.py/native_capture.c, camerad/SConscript and manager
registry; tests/docs updated. Enable USE_WEBCAM=1 Q8B_ROAD_ONLY=1 only for this
experimental capture path. Normal close restores previous mode/rate and saved
dynamic-framerate control (temporarily0to actually sustain60FPS).

21focused tests pass; real140frame IPC/Cereal check:19.973Hz publish,59.642Hz
source estimate, one stream/correctNV12 layout/timestamp pairs, exit0/settings
restored. Native helper actual SConscript target and pinned msgq bindings build.
Read session for exact scope/provenance. No model/managed UI/vehicle execution;
Q8B geometry remains unconfigured and its guard active. Driver-monitoring
consumers are not bypassed or supplied invented data. Next camera geometry and
current model-input/runtime contract qualification. Hardware settings still
deferred. Older no-camera-change statements below are historical.

## Current scope — camera work, 2026-11-02

Owner explicitly deferred hardware-setting changes and selected cameras.
Explained current webcam files; see [camera path](Knowledge/CAMERA_PATH.md).
Start openpilot/system/camerad/webcam/camera.py (actual OpenCV capture), then
webcam/camerad.py (device selection, NV12/IPC/messages), manager process selection
and common/transformations/camera.py geometry. Existing source requests720p25fps,
rotates180degrees; publisher loop20Hz with synthetic timestamps. Q8B geometry
remains explicitly unconfigured. No source fix/camera launch yet. Next: recover
teacher's actual camera/capture evidence and compare it to these contracts
before a bounded implementation. H1 thermal plan remains pending/deferred;
do not automatically resume it from older notes. No vehicle action authorized.

2026-11-02 owner narrowed question to webcam-mode prerequisites and requested
MM-X master/RK3588 evidence. Full hardware checklist is NOT required before
initial webcam demonstration: RK3ad69b20 uses generic PC empty/zero/default
telemetry and service exclusions. Literal masterdb27a433 differs from default
master-ticib9b7f488. See updated MM_X_LINUX_REFERENCE for11blob/9AST source audit.
Previous broad yes referred to full-port needs and was overbroad for this scope.
Camera/model/process compatibility still needs qualification; no application
changes or sensor-health bypass adopted. Hardware plan remains pending; this
research has not implemented or launched camera work.

2026-11-02 clarification: current source73773e3 reports Ubuntu/ARM64,
radxaQ8b and PC=True through the read-only identity command. PC denotes Linux
development policy; USE_WEBCAM separately selects a camera process in the same
repository. No separate webcam fork selected and no managed Q8B stack qualified.
Earlier standalone q8b/gpu_webcam remains a reference/demo. H1 hardware work
still next; cameras deferred. No runtime/config change from this explanation.

## Shutdown checkpoint — 2026-11-01; resume 2026-11-02

Owner requested end-of-work audit, then close VS Code and power off. Tomorrow
resume H1 in [hardware checklist](../tasks/todo.md): qualified read-only Q8B
temperature reporting first. No hardware implementation today. Cameras stay
deferred. Read teacher resume/inbox and inspect live Git before continuing.

Audit baseline29630251976104c71dd72f18de53f64adcc70864, clean radxa/q8b.
All application changes since identity12e44fee remain absent: later commits
document project layout, evidence and plans. Fresh11identity tests and notebook
checks pass; no full build, managed stack or hardware-driver test claimed.
Upstream reference a86979d2 and maintenance60f799a are clean. No missing
validation/pending upstream reviews; two corrected historical failures retained.
Daily reference timer remains active/persistent; next Nov2 15:30UTC. Check its
actual state after boot. Last service result success; project is never auto-merged.

VS Code autoSave setting was afterDelay and its Backups directory contained no
files at audit. Normal system shutdown uses VS Code's registered cleanup delay
inhibitor. Power-off is requested only after saved checkpoint/commit/validation;
check the teacher shutdown evidence for the accepted schedule. Saving this
handoff does not prove the later physical power-off completed.

Saved 2026-11-01. Read this after reopening, then check actual files and Git.
This is the current handoff; older session paths and next-task advice may be
historical. Update it after each completed increment and before task closeout.

## Accepted scope and defaults

The owner wants Sunnypilot on Radxa Dragon Q8B/Ubuntu ARM64, eventually lateral
control with a custom steering actuator. This sunnypilot directory is the actual
project. Keep active code, assets and tracked student knowledge inside it.
Teacher memory is the optional Comma workspace Ai; other folders are references
or development support. Both memories must record completed work and next steps.
Use relevant Agent Skills and REA as the default evidence workflow: readable
source first, REA for artifact/runtime analysis where applicable. Record actual
use; documentation changes do not imply binary or runtime verification.

## Completed checkpoint

- Board identity implementation:12e44feeff241334e184c86dc9daccdc7f9e4fa1.
  Exact Linux/aarch64 device-tree token detection, Python/C++ HardwareRadxa,
  append-only radxaQ8b enum8 and checked unconfigured-camera lookups.
- Linux ARM64 profile retained; COMMA_HARDWARE=False and PC=True service/path
  policy. Power/thermal/sensor hardware operations still use generic defaults.
- Canonical project migration:7c208a33747d4ce279131649f2ca3434ad3b3fc3.
  Ai is a real tracked directory without nested Git. Branch is radxa/q8b.
- Most recent project HEAD observed before this shutdown audit:
  29630251976104c71dd72f18de53f64adcc70864, clean. The commit containing this
  handoff is a later documentation checkpoint; get latest HEAD from Git.
- Source headers:Sunny2026.003.000/COMMA0.11.3. Upstream base6f7a2c94;
  separately updated reference was a86979d2. No newer upstream merge applied.
- Fresh stock model65a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce;
  preserved old Q8B model/runtime remain separate references, not overrides.

## What was actually verified

Prior identity/relocation checks:11 Python tests,4 native C++ to Python message
checks, SCons profile probe (not full build), lint/syntax/diff,31 updater tests,
notebook layout/index and standalone notebook-copy check. Evidence is recorded
in [VALIDATION.md](VALIDATION.md), [README](../readme_wat_we_did.md) and dated
sessions. Those results are tied to their source, not automatically to future
code. This workflow task verifies documentation links/layout only.

## Where we stopped and next technical step

Owner asked what to do with the collected evidence. Saved proposed ordered
[hardware plan](../tasks/plan.md) and [checklist](../tasks/todo.md): H1 read-only
temperatures first, then power, physical IMU, cooling and remaining services.
No immediate purchase/rewiring for H1; qualify fixed IMU mounting before final
axis/bias calibration. Plan only, all implementation tasks remain pending.

Owner now selected **non-camera hardware/sensors** and deferred cameras. A complete
input/output/status checklist is now included in the non-camera hardware map,
covering board, UI/audio/network, timing, bridge and vehicle-dependent inputs. We
completed a read-only map of motion-sensor messages and board-health APIs plus
this host's exposed devices. See [non-camera hardware](Knowledge/NONCAMERA_HARDWARE.md).
This source/inventory checkpoint started at5bcc0028, clean; no application or
hardware configuration changed. Exact Git HEAD must be checked on reopening.

Findings:55 readable thermal zones, system_power/USB/ADC hwmon telemetry and a
radxa_svc_glink PWM interface. Two IIO devices exposed no accel/gyro/magnetic
channels. No /dev/gnss* node; existing CH341 USB Serial is not identified as
GNSS/IMU. No ports were opened or device/bus configuration written.

Jetson teacher studies read back: DragonPilot has explicit board-health/fan
providers; Feiyang overlay has a physical IMU publisher. See JETSON_HARDWARE_REFERENCE
for pinned evidence/limits. No implementation adopted; Q8B native I²C9 and actual
board telemetry remain our path, camera work deferred.

MM-X hardware review complete at b9b7f488: PC thermal/power/fan defaults and
carState-derived IMU policies are documented in the reference note; no code
adopted. Retain actual Q8B telemetry and physical sensor path. Next bounded
implementation remains read-only thermal mapping with tests.

Known from teacher: Adafruit LSM6DS3TR-C on I²C9/address0x6a, VIN1/GND6/SDA3/
SCL5; prior102Hz polling and1040 in-memory schema round trips at olda5f44653.
No new live bus test here. Model/interface are known; no need to ask again.
Fixed mounting/bias, current-source IPC/provider and locationd acceptance remain
open. First bounded implementation candidate is read-only thermal reporting;
then validate power domains/units and implement those separately. IMU provider
needs verified installed axes, acquisition timestamps and live sample/fault tests.
Use existing teacher IMU reports first; raw I²C need not expose IIO channels.
Stock comma sensord remains disabled under PC=True; do not turn on its hardcoded
I²C/GPIO wiring. No runtime/hardware driver was implemented by this explanation.

Camera/model-contract work remains future work, deferred by this scope. Real
thermal/power/fan, IMU/GNSS, full managed runtime and steering remain unqualified.
No firmware/CAN/vehicle actuation is authorized. Discuss upstream integration
before changing this branch; daily updates only advance the reference copy.

## Startup and interrupted-session recovery

1. Read project AGENTS, this handoff, STATE/TASKS and the relevant topic/session.
   In the workspace also read teacher Ai/RESUME_HERE, ROUTER and update inbox.
2. Run `git branch --show-current`, `git log -5 --oneline` and
   `git status --short --ignore-submodules=none` from the project root.
3. Compare dirty files and latest commits/tests with the saved checkpoint.
   Preserve unexpected edits; never clean/reset/stash them automatically.
   Missing validation is an unknown, not a passing test.
4. Resume the owner's current accepted task, or explain the saved next step.
   Saved notes survive normal shutdown; unwritten chat/edits cannot be recovered
   from them after an abrupt interruption.

At every completed increment/closeout update this handoff, relevant topics,
WORKLOG/session, and teacher resume/current-state notes; commit verified scoped
project changes and attach actual validation through the workspace ledger.

Latest workflow verification:27 notebook docs/61 relative links, workspace
source index and a copied standalone notebook check passed. No application
source changed or runtime service started. No actual reboot was performed.

2026-11-02 follow-up: webcam mode does not replace hardware support. hardwared
still reads Q8B providers; PC-disabled IMU/comma-only GNSS do not become active.
Adapt needed real board providers; reuse working OS stats, qualify optional
fitted hardware, and treat CAN/vehicle integration separately. No implementation
or runtime change; H1 thermal reporting remains next.

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
