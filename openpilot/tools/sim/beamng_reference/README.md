# BeamNG bridge reference bundle

Collected from [Caleb-J773/beampilot-drive](https://github.com/Caleb-J773/beampilot-drive)
on2026-11-02, commit **5435d67499f66eca58f95882cbe35e9c577e874c**.
Contains **96 original files / 1,160,682 bytes**, plus this guide and verification metadata.
This folder contains the BeamNG-specific tools, both complete game mods, camera/
vehicle daemons and supporting source needed to study and adapt the bridge.

`upstream/` preserves original repository paths and file bytes. This is a source
bundle inside our Sunnypilot project, not an installed or runnable standalone
fork. The active Radxa camera, model, process configuration and opendbc are
unchanged. No installer, game, daemon or model was executed to collect it.

[Complete audit](AUDIT.md) · [per-file coverage](FILE_AUDIT.json) · [upstream test results](UPSTREAM_TEST_RESULTS.json).

## Contents

| Location under `upstream/` | Purpose |
| --- | --- |
| `tools/beamng_mod/beampilot_bridge/` | Complete vehicle telemetry/control Lua mod and manifest. |
| `tools/beamng_mod/openpilot_cam/` | Complete rigid camera mod, camera tuner Lua and Vue/JavaScript UI. |
| `tools/beamng_mod/test_*.lua` | Original mod tests. |
| `tools/beampilot_*.py` | Setup assistant, settings TUI, telemetry diagnostic and monitor. |
| `tools/opendbc_beampilot_car/`, `tools/install_beampilot_car.py` | Fork-specific simulated car platform and its installer source. |
| `tools/op.sh`, `tools/setup*.sh` | Original setup dependencies used by the setup launcher. |
| `openpilot/selfdrive/beamcamd/` | Game-window/X11/portal capture and camera tests. |
| `openpilot/selfdrive/beamngd/` | Telemetry, game controls, optional virtual joystick and tests. |
| `openpilot/common/beampilot_*.py` | Camera geometry, environment options, vehicle geometry, limits, blindspot and radar support. |
| `openpilot/tools/sim/lib/` | Fork's simulator camera/car/sensor/input helpers. |
| `openpilot/selfdrive/{controls,modeld,car,selfdrived}/`, `openpilot/system/manager/` | Original integration snapshots and relevant tests; these have not been applied to Sunnypilot. |
| Root configuration/launch/setup scripts, `SConstruct`, `pyproject.toml`, `uv.lock`, `.gitmodules` | Original configuration and build/dependency pins. |
| `README.md`, `LICENSE` | Upstream instructions and MIT license. |

The manifest lists every copied source file, its original Git blob/mode and
SHA-256. Models, the full base openpilot tree, compiled components, submodule
checkouts and generic vehicle-porting/release tools are not bundled. Existing
Sunnypilot supplies the base project; adapting imports/APIs remains necessary.
`SHARED_DEPENDENCIES.md` records these boundaries. The upstream README mentions
`steerpilot` as a successor; its public URL returned404 in the saved review.

## Verify the downloaded files

From this directory:

```bash
python3 verify_bundle.py
sha256sum -c SHA256SUMS
```

Verification reads bytes only. Foreign-fork tests are retained under `upstream`
but excluded from automatic parent-project pytest discovery by `conftest.py`;
they import their original fork's APIs and are not Sunnypilot integration tests.
All copied source bytes remain unchanged. Our verifier has12 corruption regressions; the separate upstream compatibility experiment has unresolved failures detailed in AUDIT.md.

## Use for our port

Start with `upstream/tools/beamng_mod/` for the PC game side, then the camera and
vehicle daemons for adapter design. Keep our PC game and Q8B inference separated
through a checked network gateway. The upstream implementation is same-host:
its camera captures the local desktop and its game-control listener is loopback.
Its1928x1208 camera contract also differs from our current1280x720 Thneed path.
See [our adaptation guide](../BEAMNG_RADXA.md) before integrating these sources.

Next slice remains recorded PC frames to a sim-only Q8B VisionIPC/UI producer,
then live camera, timed vehicle state, shadow planning and game-only lateral
feedback. This bundle does not select the rejected INT8 NPU candidate.
