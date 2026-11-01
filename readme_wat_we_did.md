# What we did: Radxa Dragon Q8B identity

Owner-authorized scope, 2026-11-01: let Sunnypilot identify Ubuntu/Linux, ARM64
and the Radxa Dragon Q8B board. Implementation lives in this protected
`radxa/q8b` checkout. The daily-updated `/home/radxa/comma/sunnypilot` remains
the upstream vendor copy; its `Ai/` link opens our shared specialist notebook.

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
upstream `6f7a2c94`. Vendor `master` remains `a86979d2`; that later upstream
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

From this checkout, print the detected identity without starting services:

```bash
cd /home/radxa/comma/q8b/sunnypilot-radxa
export PYTHONPATH="$PWD:$PWD/opendbc_repo:$PWD/msgq_repo"
/home/radxa/comma/q8b/experiments/msm-venv/bin/python -m openpilot.common.hardware
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
/home/radxa/comma/q8b/experiments/msm-venv/bin/python -m unittest -v openpilot.common.hardware.tests.test_radxa
/home/radxa/comma/q8b/experiments/msm-venv/bin/python openpilot/common/hardware/tests/check_native_identity.py \
  --capnproto-root /home/radxa/comma/q8b/tools/radxa-identity-capnproto-1.0.1.post103/comma_deps_capnproto-1.0.1.post103.data/purelib/capnproto/install \
  --build-dir /home/radxa/comma/q8b/experiments/radxa-identity-native
```

The test tools were unpacked separately under `q8b/tools` from wheels already
pinned in `uv.lock`, after SHA256 verification. No system packages or existing
runtime environments were changed. Detailed logs and tool hashes are in
`/home/radxa/comma/Ai/Reports/radxa-board-identity-20261101/`.

The new enum is local to this port: external schema readers need the same
definition, and future upstream enum additions require review for ordinal
conflicts. Camera/model/UI services have not been run or qualified here.
Real camera calibration, stock-model/runtime integration and hardware providers
are still required for a working driving stack.

The specialist notebook in `Ai/` and workspace Ai keep the dated evidence and
Git commit/validation journal. No upstream merge or remote push was performed.
