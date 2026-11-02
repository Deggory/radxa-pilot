# What we did: Radxa Dragon Q8B identity

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
