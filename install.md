# Install Sunnypilot on Radxa Dragon Q8B

This guide is for the Radxa project in this folder, on Ubuntu Linux ARM64.
The upstream reference under `q8b/sunnypilot-upstream` is a separate checkout.
The Q8B camera/model/UI path is experimental; installing dependencies does not
complete sensor, calibration, CAN or vehicle-control integration.

## 1. Prepare Ubuntu and the Q8B driver

Use Ubuntu 24.04 ARM64 and a desktop session for the preview. Check:

```bash
uname -m
cat /etc/os-release
```

The architecture should be `aarch64`. Standard development prerequisites can
be installed by a system administrator:

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  ca-certificates build-essential curl libcurl4-openssl-dev locales git git-lfs \
  python3-venv python3-tk v4l-utils
```

The already-configured workspace may already have these system prerequisites;
run the apt commands on a fresh host or to resolve an actual missing package.

The camera preview also needs the board's working graphics/display stack.
The saved Thneed model requires the matching Qualcomm Adreno 690 OpenCL driver
(OpenCL 3.0 build0855.3 / compilerE031.50.31.01), `libOpenCL.so.1`, and the CPU
image warp needs a loadable LLVM library. These are board-image prerequisites;
Python dependency installation does not install or replace the GPU driver.
Keep the validated Q8B image/driver, and consult the owner before changing it.
No `/AGNOS` or `/TICI` marker is needed; the port identifies Q8B from device tree.

## 2. Obtain the project and check its version

Get the owner's Radxa project checkout, including its Git history, submodules
and Git LFS objects. The plain upstream Sunnypilot repository does not contain
our local `radxa/q8b` changes. For this workspace:

```bash
cd ~/comma/sunnypilot
git status --short --branch
git log -1 --oneline
git submodule status
```

Read `Ai/HANDOFF.md` for the latest tested state. Preserve any local edits.
Do not pull, reset or merge upstream over the protected port. On a fresh copy,
initialize the recorded submodule revisions and retrieve LFS assets:

```bash
git submodule update --init --recursive
git lfs pull
```

These commands require access to the owner's LFS objects, including
`openpilot/selfdrive/modeld/models/q8b_cd210.thneed`. It must be the actual
99,641,029-byte file, not an LFS pointer. Its SHA256 is
`eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068`.
Reuse this already-converted model; do not convert it again during installation.

## 3. Install uv and the pinned Python

The project lists dependencies in `pyproject.toml`, exact versions/hashes in
`uv.lock`, and Python 3.12.13 in `.python-version`. Use a separate bootstrap
environment so Ubuntu's system Python stays independent:

```bash
python3 -m venv ~/.local/share/sunnypilot-uv
~/.local/share/sunnypilot-uv/bin/python -m pip install 'uv==0.13.6'
export PATH="$HOME/.local/share/sunnypilot-uv/bin:$PATH"
uv --version
uv python install 3.12.13
```

Repeat the `export PATH` line in a new terminal, or use the full path to `uv`.

## 4. Install the locked project dependencies

From the project root:

```bash
cd ~/comma/sunnypilot
uv sync --frozen --all-extras
.venv/bin/python - <<'PYTHON'
from pathlib import Path
import sysconfig
Path(sysconfig.get_path('purelib'), 'sunnypilot-q8b.pth').write_text(
  str(Path.cwd() / 'tinygrad_repo') + '\n'
)
PYTHON
source .venv/bin/activate
python --version
uv pip check
```

This includes development, tools, documentation and Q8B extras, plus the default
`standalone` group which installs our recorded submodules as editable packages.
The Q8B extra declares OpenCV JPEG decoding and Pillow for the calibration tool.
The local `.pth` entry exposes Tinygrad's `examples` helpers used by the pinned
image warp; it points inside this checkout and does not reuse teacher experiments.
Create it again after moving the checkout or rebuilding its environment.
`--frozen` uses the checked-in lock without changing its versions. Do not use
`--upgrade` during initial installation. On an existing working installation,
keep a recovery copy of its environment before syncing: exact sync can remove
packages that are not declared in the project.

## One-time maximum-performance access for Q8B

The Q8B Thneed modeld and GPU-verification command now require the tested CPU
maximum/GPU690MHz profile. Before using them on a fresh installation, run this
single command in a local terminal from the project root:

```bash
sudo /usr/bin/python3 -I tools/q8b/install_performance.py
```

Enter the administrator password in the terminal. No password is stored.
The installer copies a standalone helper to a root-owned system location and
adds a sudoers rule for only that helper's fixed `guard` action. Later model
launches use `sudo -n` and need no further prompt. The installer refuses to
replace an existing helper; do not rerun it on the already-configured board.

While modeld owns the lease, CPU performance governors and GPU690MHz are checked.
The helper restores prior settings on lease EOF, process death or handled stop
signals, and stops at85°C. Kernel thermal protections stay active. It refuses
an unsupported board or reduced configured maximum rather than raising limits.
Normal and killed-client restoration have been checked on this Q8B. There is no
boot-wide maximum-mode policy and no unrestricted password-free sudo.

## 5. Build and verify

Activate the environment above so SCons subprocesses find its Python and
vendored compiler tools. Use numeric `DEBUG` (Tinygrad does not accept the
string `release`):

```bash
export DEBUG=0
USE_WEBCAM=1 Q8B_ROAD_ONLY=1 Q8B_THNEED=1 scons --minimal -j2
```

This selects the existing Thneed model and builds native code without
reconverting the driving model. Two parallel jobs keep memory use bounded on
the 8 GB Q8B. `--minimal` leaves desktop development tools out of the build;
all optional Python dependencies were still installed. Building Panda firmware
does not flash a device. Do not start the full manager as an install test.

The generic Linux SConstruct does not visit comma's native camera subtree.
Build the project's USB camera helper explicitly:

```bash
cc -std=gnu11 -O2 -Wall -Wextra -Werror -fPIC -shared \
  openpilot/system/camerad/webcam/native_capture.c \
  -o openpilot/system/camerad/webcam/libuvc_capture.so
```

Run the focused Q8B checks:

```bash
DEBUG=0 .venv/bin/python -B -m unittest -v \
  openpilot.selfdrive.modeld.thneed_q8b.test_state \
  openpilot.selfdrive.modeld.thneed_q8b.test_runtime \
  openpilot.selfdrive.modeld.thneed_q8b.test_benchmark \
  openpilot.system.camerad.webcam.test_benchmark \
  openpilot.system.camerad.webcam.test_preview \
  openpilot.system.camerad.webcam.test_calibration \
  openpilot.system.camerad.webcam.test_road_camera \
  openpilot.common.hardware.tests.test_radxa \
  openpilot.common.hardware.tests.test_q8b_performance
```

An optional bounded native GPU verification uses the existing model and saved
validation samples, without opening the camera or reconverting anything:

```bash
.venv/bin/python -m openpilot.selfdrive.modeld.thneed_q8b.verify \
  --frames 40 --warmup 10 --output /tmp/q8b-thneed-install-check.json
```

Choose a new report path for each run. For GPU-resident image/history checks:

```bash
USE_WEBCAM=1 Q8B_ROAD_ONLY=1 DEBUG=0 .venv/bin/python -m openpilot.selfdrive.modeld.thneed_q8b.verify_resident \
  --output-dir /tmp/q8b-resident-install-check
```

This diagnostic uses explicit readbacks for correctness; production does not.

## 6. Open the isolated camera and model preview

From a graphical terminal inside the project:

```bash
cd ~/comma/sunnypilot
.venv/bin/python -m openpilot.system.camerad.webcam.preview --model
```

Connect the SunplusIT AK-Camera JV to the Q8B. The selected capture profile is
1280×720 MJPEG at 60 FPS, selecting a fresh camera arrival at each 20 Hz deadline.
The Q8B Thneed path defaults to resident GPU crop/packing/history and automatically
holds the fixed maximum-clock lease installed in step 3; no later password prompt. The preview starts camera,
Thneed-backed modeld and the actual Sunnypilot UI in a private namespace. Close
the window or press Ctrl+C to stop. Vehicle/control/driver-monitoring processes
are not started. Geometry remains provisional and the UI labels it uncalibrated.

The Q8B onroad view now includes a live performance panel: CPU/GPU temperatures,
fan PWM duty and mode, inference/full-model time and model Hz, camera-to-model,
and camera-to-UI first-draw time. Values refresh automatically; missing or stale
data shows `--`. Temperatures are the hottest readable CPU/GPU channels. PWM is
not fan RPM. Timings are rolling two-second medians; UI timing excludes screen
presentation. `Q8B_SHOW_STATS=0` hides the panel. No additional installation or
sudo permission is required. See [telemetry details](Ai/Knowledge/UI_TELEMETRY.md).

For launch options without opening the camera:

```bash
.venv/bin/python -m openpilot.system.camerad.webcam.preview --help
```

See the [camera guide](openpilot/system/camerad/webcam/README.md) and
[Thneed guide](openpilot/selfdrive/modeld/thneed_q8b/README.md) for profiles,
timing definitions, model identity and qualification limits.

## Verified installation on 2026-11-02

On this Ubuntu ARM64 Q8B, the fresh environment uses Python 3.12.13 and uv
0.13.6. All Python extras and the standalone group installed successfully;
`uv pip check` checked 85 packages and `uv lock --check` passed. Existing locked
package versions were preserved; OpenCV 4.13.0.92 was the only added package.

The Q8B minimal root build and explicit camera helper build passed. All 51 focused
tests passed, and the generated longitudinal MPC solver imported and initialized.
Native GPU verification passed 12 saved-case and 12 history-adapter checks using the
unchanged CD210 artifact. A 10-second preview received 183 model messages and 193 camera
frames, rendered 33 path points, then all three children exited 0. Camera settings
were restored and GPU faults stayed 0. This is an installation smoke test; the
previous timing qualification remains separate.

The vendored acados template emits a warning about its bundled CasADi 3.6.7
version; the warning is retained in the build log. Native build and solver
construction passed; full planning/vehicle behavior has not been qualified.
No system package, GPU driver, firmware or clock policy was changed by this
installation. The host already supplied the compiler/runtime prerequisites
needed for the tested build; the administrator apt step above was not rerun.

Local recovery copies are ignored by Git:

- `.venv-preview-backup-20261102/`: original limited preview environment.
- `.install-backup-20261102/`: five original native libraries and their manifest.

Keep these until the new setup is accepted. Virtual environments contain
absolute paths: to restore, first stop the preview, retain the new environment
under another name, move the old environment back to `.venv`, then restore the
matching libraries according to the manifest. Running a renamed environment
in place is not a verified recovery method. Fresh installations do not require
these backups or the teacher's experiments.

The project record is [Ai/Knowledge/INSTALLATION.md](Ai/Knowledge/INSTALLATION.md).
Workspace-only raw evidence is retained under
`Ai/Reports/sunnypilot-install-20261102/` in the parent Comma workspace.

## Troubleshooting

- `.venv/bin/python: No such file or directory`: enter `~/comma/sunnypilot`,
  then check that dependency installation completed there.
- `No module named acados`: check the selected interpreter and re-run the
  locked sync; the package name is `comma-deps-acados`, its import is `acados`.
- An LFS pointer in place of a model: obtain the actual objects from the owner.
- GPU device/driver mismatch: the replay intentionally refuses an incompatible
  device; installing more Python packages does not change that driver.
- No camera/display access: check the USB device and desktop permissions;
  do not run the whole project as root.

## Sources

- Repository setup: [tools/README.md](tools/README.md),
  [dependency setup script](tools/setup_dependencies.sh),
  [pyproject.toml](pyproject.toml), [uv.lock](uv.lock).
- Official uv: [installation](https://docs.astral.sh/uv/getting-started/installation/),
  [Python management](https://docs.astral.sh/uv/guides/install-python/),
  [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

Q8B camera/model daemons also default to `Q8B_FAST_CPU=1`, restricting their
entry thread and future workers to allowed fast cores 4–7. Parent/UI affinity
is unchanged and no real-time FIFO policy is enabled. Set 0 for scheduling
comparisons. Pinning all work to CPU7 alone regressed this resident pipeline;
the four-core setting measured 36.829 ms median / 41.592 ms p95 from source
capture timestamp to model output at 20 Hz, with 10.817/11.790 ms inference.
The final repeat is retained in the
[portable qualification receipt](Ai/Evidence/q8b-resident-20261102.json).
