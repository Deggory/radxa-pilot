## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Created [BeamNG PC/Radxa folders and CAN plan](openpilot/tools/sim/beamng/README.md) for a physical webcam watching the PC monitor, state/commands through Waveshare and Chimera, and later bench actuators. Replaced the old network-image proposal in current guides. This is a documented architecture; the CAN/Chimera runtime remains pending.

## 2026-11-02 — BeamNG reference audited

Reference bundle expanded to96verified upstream files. Fixed our verifier and
added12corruption regressions. Actual snapshot compatibility tests retain
6failures/2import-blocked modules; direct bridge integration remains blocked.
[Complete audit and next gate](openpilot/tools/sim/beamng_reference/AUDIT.md).
No game/model/manager or physical vehicle action.

## 2026-11-02 — Fresh big-model NPU research baseline

Converted matching Mountain Dew v3 source, calibrated500frames and ran200heldout
Q8B inferences plus3IO checks on SDK2.37/v68/SoC37.400MB W8A8 DLC/444MB context;
200MB target unmet. Execution succeeds but raw tensor errors are too large:
**candidate rejected and GPU model stays selected**. Failed FP16 gate retained
under explicit owner approval.29tool tests pass; this does not qualify driving.
[Results and next experiment](openpilot/selfdrive/modeld/npu/RESULTS.md).

# What we did: Radxa Dragon Q8B identity

## 2026-11-02 — Actual camera-to-UI benchmark

Added opt-in per-frame benchmark to the native Sunnypilot dashboard preview.
65srun/5swarmup/1200steady frames: capture→draw-ready59.40msmedian/78.76msp95;
capture→EndDrawing-return89.39msmedian/109.14msp95, including normal frame pacing.
Fresh video19.98FPS;37focused tests pass, raw samples independently checked,
camera settings restored. Host-call timing is not physical screen-light latency.
See [benchmark session](Ai/Sessions/2026-11-02-camera-ui-benchmark.md).

## 2026-11-02 — Open live camera in Sunnypilot dashboard

Run `.venv/bin/python -m openpilot.system.camerad.webcam.preview` from this
project root. Uses the real onroad dashboard, camera publisher and private
demo state. Close window to stop/restore camera.32tests and live screenshot
verified; inference and vehicle controls are not started. See webcam README
for development environment dependencies and current limitations.

## 2026-11-02 — Temporary MM-X road-camera geometry

Owner chose fixed MM-X geometry for now:1280x720,900pixel focal length,
centre640/360. Q8B road-only mode supplies it to model/UI through their
shared lookup. Borrowed/unmeasured for AK; no lens-distortion or vehicle
mount calibration claimed. Capture60/publication20Hz unchanged. Automatic
calibration deferred; target/tools kept.30tests/lint pass; no model/vehicle run.

## 2026-11-02 — Current model layout and lens-calibration tools

Corrected the road-only publisher to match current modeld's padded NV12 layout;
the old packed buffer failed its copy size.140real IPC pairs and23focused tests
passed after the fix; the pinned current CPU warp matches two synthetic NumPy
views exactly and produces current ONNX's uint8[2,6,128,256] input shape. This
does not run the model or qualify the Adreno backend. Added Q8B720pwarp build
configuration while retaining the existing runtime choice.

Owner requested a printable target/tool. [Print this A4 landscape PDF](openpilot/system/camerad/webcam/calibration/ak-checkerboard-a4.pdf)
at actual size; squares25mm,9×6internal corners. The
[calibration guide](openpilot/system/camerad/webcam/CALIBRATION.md) explains image
collection and offline solving. Candidate data are not installed automatically;
actual lens/focus and mounted geometry remain to be measured/reviewed.

## 2026-11-02 — Approved single road-camera capture

After teacher-first lookup and owner approval, added opt-in
`USE_WEBCAM=1 Q8B_ROAD_ONLY=1` support for our SunplusIT AK-Camera JV.
Capture requests MJPEG1280×720/60FPS from its stable by-id device and publishes
the newest decoded NV12 frame at20Hz. Real V4L2 timestamps and source sequence
are paired with IPC/messages. Rotation defaults off and is configurable.
Only the road stream is opened; driver-camera processes are deferred in this
mode. Native capture/build source is inside this repository; no outside Q8B
source import is required. See [camera instructions](openpilot/system/camerad/webcam/README.md).

Camera's dynamic-framerate control is temporarily disabled, like earlier tests,
and restored with prior format/rate on normal close. No shutter/gain/clock/fan
policy changes. New check:140real IPC/Cereal frame pairs,~19.973Hz publication,
~59.642Hz source sequence, correct720pNV12 layout, one stream, exit0 and matching
before/after camera settings.21focused tests and native builds pass.
This does not validate the model, UI, calibration or vehicle stack. Existing
Q8B calibration guard and model/runtime remain unchanged; next qualify actual
camera geometry and model-input contracts. [Session](Ai/Sessions/2026-11-02-road-camera-patch.md).

Owner-authorized scope, 2026-11-01: let Sunnypilot identify Ubuntu/Linux, ARM64
and Radxa Dragon Q8B. The owner clarified that **this `sunnypilot/` directory is
the actual project** and is the folder intended for use when ready.

## Project location correction

The initial identity work was saved in `q8b/sunnypilot-radxa`. We moved that
existing Git repository into `/home/radxa/comma/sunnypilot`, preserving its full
history, branch, source/assets, submodules and IDE files. No application patch
was dropped or silently combined with newer upstream source.

- Work here, on `radxa/q8b`. Identity implementation commit: `12e44fee`.
- `Ai/` is now a **real directory tracked in this project**, copied from the
  specialist notebook without its nested `.git`. It travels with this folder.
- The clean upstream copy moved to `q8b/sunnypilot-upstream` as a reference.
  Daily updates target that copy; they never overwrite this project's branch.
- The old `q8b/sunnypilot-radxa` path is only a compatibility link. Other
  workspace folders retain references, earlier experiments and development
  tools. Active Radxa implementation belongs here.
- The former independent notebook Git history remains archived under q8b.
  New knowledge and code changes are committed together in this project.

The application identity implementation has no runtime dependency on those
outside reference folders. A working deployment still needs the usual Python,
C++ and hardware dependencies and the remaining camera/model integration.
Historical evidence links outside this folder are optional research context.

## Contract

- Recognize the exact `radxa,dragon-q8b` device-tree compatible token on Linux
  aarch64. A missing/unreadable tree, another board, another OS/architecture or
  a similar-looking token does not identify Q8B. Existing AGNOS selection keeps
  precedence; we do not create or modify OS marker files.
- Select `HardwareRadxa` in Python. Report `radxaQ8b` in the shared device enum,
  `Radxa Dragon Q8B` as the board name and the actual Linux OS description.
- Keep the Linux `aarch64` build, `COMMA_HARDWARE=False` and generic `PC=True`
  behavior on this board. PC here is also a service/path policy; identity alone
  must not enable comma's GPIO, power, modem, firmware or sensor operations.
- Append a new schema enum without renumbering existing device identities.
  C++ builds on Q8B use the same identity and retain generic Linux paths.
- Explicitly register Q8B camera geometry as unconfigured. Camera consumers
  must report missing calibration rather than silently use comma intrinsics.

## What this does not implement

Camera capture/calibration, MSM/Adreno inference selection, real IMU/GNSS,
thermal/power/fan controls and vehicle actuation remain separate work. This
identity backend initially inherits generic PC defaults for unimplemented
hardware operations. Their zero/empty values are not measured hardware health.
No manager, model, camera, firmware or vehicle service is started by this work.

## Changes and validation

Implemented 2026-11-01 on `radxa/q8b`, from protected HEAD `dfb86f6a` atop
upstream `6f7a2c94`. The upstream reference was `a86979d2` at migration; that later upstream
commit has not been merged into this port.

| Files | What changed |
| --- | --- |
| `openpilot/common/platform.py` | Shared, read-only Linux/ARM64/device-tree detection, including existing AGNOS precedence. |
| `openpilot/common/hardware/radxa/`, hardware `__init__.py` and `hw.h` | Python/C++ Radxa identity implementations using existing generic Linux hardware operations. |
| `SConstruct` | Selects `__RADXA_Q8B__` while retaining the existing `aarch64` build profile. |
| `openpilot/cereal/log.capnp` | Appends local device identity `radxaQ8b @8`; existing ordinals 0–7 stay unchanged. |
| `openpilot/common/transformations/camera.py` | Registers unconfigured Q8B geometry and provides an explicit missing-calibration error. |
| Both modeld implementations, camera-offset helper and both augmented-road views | Use the checked camera lookup for device-dependent geometry. |
| `openpilot/common/hardware/__main__.py`, hardware `tests/` | Read-only identity command, Python contracts and actual C++/Python schema checks. |

From this checkout, using a Python environment with the project dependencies
installed, print the detected identity without starting services:

```bash
cd /home/radxa/comma/sunnypilot
export PYTHONPATH="$PWD:$PWD/opendbc_repo:$PWD/msgq_repo"
python3 -m openpilot.common.hardware
```

Actual output on this board:

```text
Operating system: Ubuntu 24.04.5 LTS (Linux)
CPU architecture: ARM64 (aarch64)
Board: Radxa Dragon Q8B
Device type: radxaQ8b
Linux development policy (PC): True
```

`PC=True` intentionally preserves generic Linux service and path choices. The
board identity is now Radxa; this flag does not mean it was misdetected as an
x86 desktop. Ubuntu comes from `/etc/os-release`; it is not hardcoded.

Verification completed:

- **11 Python contract tests passed**, including other boards/OS/architecture,
  unreadable device tree, AGNOS precedence, factory selection, schema ordinals,
  OS fallback and missing camera calibration. Inverting the detection condition
  made the tests fail; restoring it returned them to green.
- **4 C++ → Python message checks passed**, compiling the actual schemas and
  hardware headers for both generic PC and Q8B, with `-Wall -Werror`. Both
  `deviceState` and `initData` decoded with the expected identity.
- An actual SCons configuration probe selected `aarch64`, non-comma policy and
  `__RADXA_Q8B__`. This was a profile check, **not a full Sunnypilot build**.
- Ruff passed for all changed/new Python files; AST syntax checks and
  `git diff --check` passed.

Reproduce the Python and native checks after setting `PYTHONPATH` above:

```bash
python3 -m unittest -v openpilot.common.hardware.tests.test_radxa
python3 openpilot/common/hardware/tests/check_native_identity.py \
  --capnproto-root "$CAPNPROTO_ROOT" \
  --build-dir /tmp/sunnypilot-radxa-identity-native
```

`CAPNPROTO_ROOT` is a Cap'n Proto installation with bin/include/lib. The original
validation used the existing workspace test environment and test tools
unpacked separately under `q8b/tools` from wheels already
pinned in `uv.lock`, after SHA256 verification. No system packages or existing
runtime environments were changed. Detailed logs and tool hashes are in
`/home/radxa/comma/Ai/Reports/radxa-board-identity-20261101/`.

The new enum is local to this port: external schema readers need the same
definition, and future upstream enum additions require review for ordinal
conflicts. Camera/model/UI services have not been run or qualified here.
Real camera calibration, stock-model/runtime integration and hardware providers
are still required for a working driving stack.

The tracked specialist notebook in `Ai/` and optional workspace Ai keep the
dated evidence and Git commit/validation journal. No upstream merge or remote push was performed.


## Non-camera hardware assessment — 2026-11-01

The current owner focus is hardware/sensors; camera work is deferred. Read the
[hardware and sensor map](Ai/Knowledge/NONCAMERA_HARDWARE.md). A read-only host
inventory found thermal, power and PWM interfaces; no motion channels appeared
in exposed IIO devices. This assessment adds documentation, not a sensor driver.
Teacher memory identifies the existing Adafruit LSM6DS3TR-C on I²C9/address
0x6a, with prior raw/~102Hz and in-memory schema tests. Absence of IIO motion
channels does not negate its raw-I²C path. Current managed integration/mount
calibration and power-domain mappings remain to be established.

## 2026-11-02 — Existing CD210 Thneed copied into Sunnypilot

The model was already converted. We copied it unchanged and added its native
OpenCL replay/source/build, validation fixtures and current-history adapter.
Fresh GPU checks and42focused tests pass; no reconversion or camera changes.
See [build/run instructions](openpilot/selfdrive/modeld/thneed_q8b/README.md).
The full modeld/camera integration remains the next qualification step.

## 2026-11-02 — Camera → Thneed → stock modeld → Sunny UI

Connected existingCD210 without reconversion through Q8B_THNEED opt-in. Actual
UI shows live33point model path. Clean65s test reached19.998model messages/s;
51tests and synthetic/liveCPU checks pass. Uses temporary unmeasured geometry,
so model/calibration validity stays false. No vehicle controls started.
Open with `.venv/bin/python -m openpilot.system.camerad.webcam.preview --model`.
[Details and limits](Ai/Sessions/2026-11-02-thneed-modeld.md).

## 2026-11-02 — Maximum clocks and resident GPU images

Model starts automatically acquire the fixed maximum-performance lease and
restore clocks on exit. Image crop/packing/history now stay in the existing
Thneed OpenCL context. Fresh camera selection reduces source age. Three-minute
bench sustained20Hz:11.085ms inference and37.886ms camera→output medians,
with p9512.068/42.690ms.68tests, exact/CPU checks and10sSunnyUI pass. Existing
model unchanged; controls remain off and geometry provisional.
[Details and limits](Ai/Knowledge/MAX_PERFORMANCE.md).

2026-11-02 scheduling follow-up: unrestricted repeat38.204ms missed target;
singleCPU7 trial regressed to40.512ms. Fast cores4–7 default instead measured
36.829/41.592ms camera→output and10.817/11.790ms inference median/p95 at20Hz.

2026-11-02 accepted closeout: Final repeat: 1164steady outputs/20.0027Hz; inference11.070/12.258ms, fullcall13.574/15.314ms and capture→output37.355/41.790ms median/p95. All clock samples max; target medians pass. Prior fast run36.829ms also passes.68tests/lint/native/exactGPU/CPU checks pass. Final UI194frames/176models/33points, children0/0/0. All reported workers/private IPC removed, camera and clocks restored, GPUfaults0, model/helper hashes unchanged.

## 2026-11-02 — Live performance panel in Sunnypilot UI

Added actual onroad CPU/GPU temperatures, fan PWM duty/mode, GPU and full-model
latency, model Hz, camera-to-model and camera-to-UI first-draw time. Read-only
sensors, rolling timing medians and explicit unavailable/stale states.76tests
and real65s20Hz UI/independent frame checks pass; standard --model preview
shows it automatically. [Details](Ai/Knowledge/UI_TELEMETRY.md).
