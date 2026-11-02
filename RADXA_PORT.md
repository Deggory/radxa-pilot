# Radxa Dragon Q8B project

This `sunnypilot/` repository is the working project, branch `radxa/q8b`.
Owner clarification, 2026-11-01: keep all active implementation and project
knowledge here; the other Comma workspace folders are references/support.

Initial upstream base: `6f7a2c94c10dffcf9a83b120ab1e6985e4496868`.
Q8B identity implementation: `12e44feeff241334e184c86dc9daccdc7f9e4fa1`.
Read [what we did](readme_wat_we_did.md) and [project memory](Ai/ROUTER.md).
`Ai/` is a regular tracked directory and travels with the project.

The daily job updates only the workspace's `q8b/sunnypilot-upstream/` reference.
It does not modify this branch. Related upstream changes require discussion
before integration. Keep reviewed/tested local commits and validation records.
The former `q8b/sunnypilot-radxa` path is only a compatibility link to this folder.

## Current Q8B support — 2026-11-02

The road-camera → CD210 Thneed model → Sunny onroad UI preview works at about
20 Hz. The panel shows CPU/GPU temperatures, actual fan PWM/mode, model speed,
camera-to-model and camera-to-UI first-draw timing. Model-enabled runs acquire
the installed scoped maximum-clock profile automatically. Camera-only runs do
not acquire that profile. See [installation and launch steps](install.md).

Read the [complete needs-versus-Q8B support table](Ai/Knowledge/NONCAMERA_HARDWARE.md)
for every hardware area: temperatures, cooling, power, load/storage, IMU, GNSS,
timing, network, display/audio, lifecycle, USB and vehicle/ADAS inputs. It
separates exposed interfaces, historical standalone tests and current integration.

Linux exposes 55 thermal zones and additional hwmon readings. Only CPU/GPU
maxima and fan PWM currently feed the preview panel; managed thermal/power/GPU
utilization providers remain pending. The known external LSM6DS3TR-C IMU has
historical raw-I²C tests but no current managed publisher. A tested GNSS receiver
is not established in teacher records. Vehicle data must come from the selected
vehicle/bridge, not the board's internal sensors.

Temporary camera calibration remains provisional. This is a bench preview;
full manager, physical-display latency, current IMU/localization and vehicle
integration remain unqualified. Driver monitoring is deferred. No vehicle-
actuation qualification is claimed. Current source/run evidence is linked from
[UI telemetry](Ai/Knowledge/UI_TELEMETRY.md).
