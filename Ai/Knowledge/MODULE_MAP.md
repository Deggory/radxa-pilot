# Current tracked module map

Source: `a86979d2b2b176413a7f3e5cccf8c807596a7def`, 2026-11-01. Counts are Git entries, not reviewed functions.

| Top-level area | Tracked entries | Role |
| --- | ---: | --- |
| `(root files)` | 27 | Tracked source/configuration/assets; inspect the matching pinned path before drawing behavioral conclusions. |
| `.github` | 26 | Upstream CI/workflow and contribution metadata. |
| `.idea` | 2 | IDE build/project configuration. |
| `.run` | 4 | Tracked source/configuration/assets; inspect the matching pinned path before drawing behavioral conclusions. |
| `.vscode` | 3 | Tracked source/configuration/assets; inspect the matching pinned path before drawing behavioral conclusions. |
| `docs` | 27 | Upstream developer/user documentation. |
| `openpilot` | 1457 | Application services, shared code, schemas, UI and Sunnypilot extensions. |
| `release` | 5 | Tracked source/configuration/assets; inspect the matching pinned path before drawing behavioral conclusions. |
| `scripts` | 22 | Tracked source/configuration/assets; inspect the matching pinned path before drawing behavioral conclusions. |
| `system` | 1 | Compatibility AGNOS manifest link, not the running service tree. |
| `tools` | 67 | Development, replay, simulation and diagnostic utilities. |

## Application source areas

| Area under openpilot | Tracked entries |
| --- | ---: |
| `__init__.py` | 1 |
| `cereal/README.md` | 1 |
| `cereal/SConscript` | 1 |
| `cereal/__init__.py` | 1 |
| `cereal/custom.capnp` | 1 |
| `cereal/deprecated.capnp` | 1 |
| `cereal/include` | 1 |
| `cereal/log.capnp` | 1 |
| `cereal/messaging` | 13 |
| `cereal/services.py` | 1 |
| `cereal/visionipc.py` | 1 |
| `cereal/visionstream.h` | 1 |
| `common/SConscript` | 1 |
| `common/__init__.py` | 1 |
| `common/api` | 3 |
| `common/basedir.py` | 1 |
| `common/constants.py` | 1 |
| `common/esim` | 5 |
| `common/filter_simple.py` | 1 |
| `common/fuzzy.py` | 1 |
| `common/git.py` | 1 |
| `common/gpio.py` | 1 |
| `common/gps.py` | 1 |
| `common/hardware` | 24 |
| `common/i2c.py` | 1 |
| `common/linux.py` | 1 |
| `common/logging_extra.py` | 1 |
| `common/markdown.py` | 1 |
| `common/mock` | 2 |
| `common/parameterized.py` | 1 |
| `common/params.cc` | 1 |
| `common/params.h` | 1 |
| `common/params.py` | 1 |
| `common/params_c.cc` | 1 |
| `common/params_keys.h` | 1 |
| `common/pid.py` | 1 |
| `common/prefix.h` | 1 |
| `common/prefix.py` | 1 |
| `common/qrcode.py` | 1 |
| `common/queue.h` | 1 |
| `common/ratekeeper.cc` | 1 |
| `common/ratekeeper.h` | 1 |
| `common/realtime.py` | 1 |
| `common/serial.py` | 1 |
| `common/simple_kalman.py` | 1 |
| `common/spinner.py` | 1 |
| `common/stat_live.py` | 1 |
| `common/swaglog.cc` | 1 |
| `common/swaglog.h` | 1 |
| `common/swaglog.py` | 1 |
| `common/test.py` | 1 |
| `common/tests` | 14 |
| `common/text_window.py` | 1 |
| `common/time_helpers.py` | 1 |
| `common/timeout.py` | 1 |
| `common/timing.h` | 1 |
| `common/transformations` | 10 |
| `common/util.cc` | 1 |
| `common/util.h` | 1 |
| `common/utils.py` | 1 |
| `common/version.h` | 1 |
| `common/version.py` | 1 |
| `common/yuv.cc` | 1 |
| `common/yuv.h` | 1 |
| `selfdrive/__init__.py` | 1 |
| `selfdrive/assets` | 250 |
| `selfdrive/car` | 11 |
| `selfdrive/controls` | 27 |
| `selfdrive/locationd` | 19 |
| `selfdrive/modeld` | 15 |
| `selfdrive/monitoring` | 3 |
| `selfdrive/navigation` | 10 |
| `selfdrive/pandad` | 19 |
| `selfdrive/selfdrived` | 9 |
| `selfdrive/test` | 26 |
| `selfdrive/ui` | 185 |
| `sunnypilot/SConscript` | 1 |
| `sunnypilot/__init__.py` | 1 |
| `sunnypilot/common` | 6 |
| `sunnypilot/livedelay` | 3 |
| `sunnypilot/mads` | 5 |
| `sunnypilot/mapd` | 14 |
| `sunnypilot/modeld_v2` | 39 |
| `sunnypilot/models` | 16 |
| `sunnypilot/navd` | 1 |
| `sunnypilot/neural_network_data` | 1 |
| `sunnypilot/selfdrive` | 106 |
| `sunnypilot/sunnylink` | 42 |
| `sunnypilot/system` | 31 |
| `sunnypilot/tools` | 7 |
| `system/__init__.py` | 1 |
| `system/athena` | 10 |
| `system/camerad` | 30 |
| `system/hardware` | 12 |
| `system/journald.py` | 1 |
| `system/loggerd` | 36 |
| `system/logmessaged.py` | 1 |
| `system/manager` | 8 |
| `system/micd.py` | 1 |
| `system/proclogd.py` | 1 |
| `system/qcomgpsd` | 4 |
| `system/sensord` | 9 |
| `system/tests` | 2 |
| `system/timed.py` | 1 |
| `system/tombstoned.py` | 1 |
| `system/ubloxd` | 7 |
| `system/ui` | 60 |
| `system/updated` | 1 |
| `system/webrtc` | 6 |
| `test_native.py` | 1 |
| `third_party/copyparty` | 1 |
| `third_party/mapd_pfeiferj` | 2 |
| `tools/__init__.py` | 1 |
| `tools/auto_source.py` | 1 |
| `tools/cabana` | 111 |
| `tools/camerastream` | 3 |
| `tools/clip` | 1 |
| `tools/jotpluggler` | 53 |
| `tools/joystick` | 3 |
| `tools/lateral_maneuvers` | 4 |
| `tools/lib` | 31 |
| `tools/longitudinal_maneuvers` | 6 |
| `tools/plotjuggler` | 17 |
| `tools/replay` | 34 |
| `tools/sim` | 20 |

## External source pins

| Dependency | Git SHA | Indexed entries |
| --- | --- | ---: |
| `msgq_repo` | `e7396e76dadbb49e374d4b664ff6bbb43a39bcb0` | 47 |
| `opendbc_repo` | `aa9bff6f5442cef8cb8e25e143ef38865c276ce8` | 547 |
| `openpilot/sunnypilot/neural_network_data` | `03cac2d30e111e0689c0429cb8c1fe6cb5a905af` | 115 |
| `panda` | `8a16e089b88593914823743df29e1c30b7dd3e00` | 178 |
| `rednose_repo` | `28d4a7f69e80e1c3e0d24ca0733d7daeaeade3d0` | 37 |
| `teleoprtc_repo` | `1aa8fc433bef1519a95c0700c96258c3be6dfb34` | 20 |
| `tinygrad_repo` | `92b742f711c7d216fd3ed7a46a30a959e3c43bd4` | 1667 |

Use [architecture](ARCHITECTURE.md) for behavior and [source index](../Evidence/source-index.json) for exact tracked paths. Read selected entries rather than loading the entire index.
