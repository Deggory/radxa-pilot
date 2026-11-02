# Full dependency installation and newcomer guide — 2026-11-02

Owner authorized install.md and installation of all project dependencies.
Completed on source ed67486, branch radxa/q8b: added q8b OpenCV/Pillow extra,
updated lock without changing existing package versions, installed uv0.13.6 and
managed Python3.12.13. Preserved old env/native libraries, built clean staging,
then clean default .venv. No outside bench Python paths. Added local tinygrad
examples .pth as documented after actual fresh-env test failures; no code/test
suppression. No model reconversion or source/runtime algorithm changes.

Changed project paths: install.md, README.md, pyproject.toml, uv.lock,
openpilot/system/camerad/webcam/README.md and relevant Ai records. Camera README
now correctly uses explicit native helper build on generic aarch64. No protected
branch/upstream/submodule reset/merge; no system packages, driver or firmware
changes. Git-local excludes protect environment/native recovery copies.

Validation: uv pip check85packages, lock check, minimal root SCons build exit0,
strict UVC helper build,51focused tests, MPC solver import/construction,
Tk/Pillow PhotoImage,12savedGPU+12adapter cases, actual10second camera/model/UI
with193camera frames/183models/33pathpoints andchildren0/0/0. Screenshot viewed;
camera restored, GPUfaults0→0, no owned processes/privateIPC remain. All original
Thneed hashes preserved. Initial staging3errors and upstream warnings retained.

Source/model/runtime pins and exact commands/recovery/limits:
[installation topic](../Knowledge/INSTALLATION.md), [guide](../../install.md).
Raw optional central evidence: Ai/Reports/sunnypilot-install-20261102 including
before/after manifests, source pins, lock version diff, native backup manifest,
bootstrap/sync/build/test logs, live UI reports/screenshot and validation.json.

Actual sources: current setup_dependencies.sh/SConstruct/pyproject/uv.lock,
original preview environment session and official uv install/sync/Python docs.
Skills: incremental/source/documentation/Git plus debugging/TDD and review.
Source-first REA routing used actual artifact/import/build/native outputs;
no unrelated binary parser run. Calibration/vehicle/full-manager/sustained
performance remain outside qualification. Next owner can follow install.md
and run isolated preview; later hardware/geometry work requires its own scope.
