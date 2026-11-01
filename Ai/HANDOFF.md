# Resume Sunnypilot here

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
- Most recent project HEAD observed before this workflow task:
  99d38e4ca26ca95b7474b3ed5f50e5d207c73f6f, clean. The commit containing this
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

Owner now selected **non-camera hardware/sensors** and deferred cameras. We
completed a read-only map of motion-sensor messages and board-health APIs plus
this host's exposed devices. See [non-camera hardware](Knowledge/NONCAMERA_HARDWARE.md).
This source/inventory checkpoint started at5bcc0028, clean; no application or
hardware configuration changed. Exact Git HEAD must be checked on reopening.

Findings:55 readable thermal zones, system_power/USB/ADC hwmon telemetry and a
radxa_svc_glink PWM interface. Two IIO devices exposed no accel/gyro/magnetic
channels. No /dev/gnss* node; existing CH341 USB Serial is not identified as
GNSS/IMU. No ports were opened or device/bus configuration written.

Pending owner input: actual external IMU model/interface, if any. First bounded
implementation candidate is real read-only Q8B thermal reporting with tests;
then validate power domains/units and implement those separately. IMU provider
needs actual model, axes, acquisition timestamps and live sample/fault tests.
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
