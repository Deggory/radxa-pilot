# Q8B installation and dependency setup

Owner requested a newcomer install guide and installation of all dependencies
on2026-11-02. [install.md](../../install.md) is the tested step-by-step entry;
top-level README links to it. Source base ed674866289202a765eec17e0680229c52b07213,
protected radxa/q8b; no upstream merge/push.

## Installed environment

- Managed Python3.12.13 (project pin), uv0.13.6 at
  ~/.local/share/sunnypilot-uv/bin/uv; project default .venv rebuilt from lock.
- `uv sync --frozen --all-extras` includes default standalone group;85packages
  checked compatible. All prior package versions retained; only new lock package
  opencv-python-headless4.13.0.92. Added q8b extra declares that and Pillow.
- No teacher/experiment site-packages in new sys.path. All editable dependencies
  use project submodules. .venv's sunnypilot-q8b.pth points only to this project's
  tinygrad_repo because editable Tinygrad omits its examples helpers. Guide
  reproduces this step; recreate it after moving/rebuilding the environment.
- acados0.2.2.post103 includes bundled CasADi3.6.7. Existing template emits version
  and Python escape warnings; retained, no suppression. Native solver constructs.
- Native OpenCL driver/CPU LLVM remain the existing host stack; Python install
  does not replace drivers. No apt, system, clock, firmware or hardware writes.

## Qualification

Clean staging environment initially exposed3missing-examples test errors. Local
project-only path fixes setup without code/test changes; all51tests pass in both
staging and final environments. Final root SCons `--minimal -j2`, with numeric
DEBUG=0/USE_WEBCAM=1/Q8B_ROAD_ONLY=1/Q8B_THNEED=1, passes. No ONNX compile/conversion.
Generic aarch64 root skips comma camera subtree: build native_capture.c helper
explicitly using documented strict cc command; old camera README corrected.
MPC generated C/Cython solver builds, imports and constructs successfully.
Python Tk9/Pillow12.3 PhotoImage smoke passes. uv pip check/lock check pass.

Existing99,641,029byte model SHAeb741641 unchanged; saved12GPU exact/tolerance
checks and12queue-adapter checks pass under matching Adreno690/build0855.3.
Final10second actual UI smoke:193camera frames,183model messages,33rendered path
points, allchildrenexit0, no vehicle/control processes. Camera format/rate and
dynamic-framerate restored exactly; no camera owner or privateIPC remains.
GPU faults0→0. Screenshot visually checked. No new20min or timing claim.

## Recovery and remaining limits

Original .venv-preview-backup-20261102 and5native libs in
.install-backup-20261102/manifest.json retained, ignored by local Git exclude.
Restore renamed virtual environments to original .venv path before using;
absolute script paths are not relocatable. Staging environment removed after
successful final verification; package cache retained. These backups are not
runtime dependencies. Model/driver/submodule pins remain unchanged.

Minimal build excludes desktop native development tools. Full manager, hardware
providers, measured optics/calibration, vehicle integration and sustained timing
remain unqualified; model validity remains false for borrowed MM-X geometry.
Next: use documented setup/preview; select further geometry/hardware/runtime work
with owner. Do not launch manager or vehicle actuation as an installation test.

[Session](../Sessions/2026-11-02-installation.md). Optional workspace reports:
/home/radxa/comma/Ai/Reports/sunnypilot-install-20261102/. Skills used: incremental,
source verification, debugging/TDD for reproduced setup failure, documentation,
Git/review; REA fast path used pinned readable source, actual imports/builds and
native runtime evidence, no unrelated REA decompilation.
