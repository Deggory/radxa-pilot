# Sunnypilot work history

This is a curated history of work already recorded in workspace Ai. A historical
result stays tied to its original source/model/runtime and test scope.

| Date | Work and resulting knowledge | Evidence |
| --- | --- | --- |
| 2026-10-27 | Mapped current standalone camera/Adreno work versus missing managed Sunnypilot integration; identified camera/message/runtime/UI boundaries. Audit base was old `a5f44653`, not today's stock checkout. | [Integration audit](/home/radxa/comma/Reports/sunnypilot-radxa-audit-20261027/REPORT.md) |
| 2026-10-30 | Reviewed fork/version/lateral options and newer master changes. Recommendations did not establish Q8B or vehicle reliability. | [Selection](/home/radxa/comma/q8b/SUNNYPILOT_SELECTION.md) |
| 2026-11-01 | Owner selected a fresh stock Sunny start. Archived old complete custom checkout/model/patched runtime; verified fresh `6f7a2c94` assets and pins. | [Clean start](/home/radxa/comma/Ai/Reports/sunnypilot-clean-start-20261101/REPORT.md) |
| 2026-11-01 | Installed daily vendor update and every-commit ledger; created protected port; froze legacy worker helper imports. Original checks: 27 maintenance tests and 15 worker CPU tests. | [Maintenance](/home/radxa/comma/Ai/Reports/sunnypilot-daily-maintenance-20261101/REPORT.md) |
| 2026-11-01 | Mapped all 193 tracked system paths, inspected key functions and documented Q8B treatment. 139 AST parses and source/hash/link checks; no runtime port test. | [Local system guide](Knowledge/SYSTEM.md) |
| 2026-11-01 | Created specialist notebook shared by both Sunny checkouts, seeded history/topic maps and source index; added reserved-path update protection. Three collision regressions first failed; full maintenance suite now passes 31. | [Bootstrap session](Sessions/2026-11-01-bootstrap.md) |
| 2026-11-01 | Real maintenance check advanced vendor6f7a2c94→a86979d2, preserving notebook/port. New commit only hides Sunnylink Steering Arc toggle on mici. Stale notebook pin was detected, retained as a failed check and refreshed; premature no-advance documentation corrected without rewriting history. | [Versions](Knowledge/UPSTREAM_AND_VERSIONS.md), bootstrap session |

Future entries: date, exact changed repository/commit, resulting behavior,
actual tests and remaining limits. Keep full session details under Sessions.
Do not claim an uncommitted file is a tracked source commit.

2026-11-01 — Explained AGNOS versus generic Linux at the owner's request before
changes. Verified host Ubuntu24.04.5/aarch64/noAGNOS and actual source predicates;
generic Linux detection already works. Q8B hardware/GPU integration remains
future work, with no implementation approval or application/OS changes.
See [Linux platform note](Knowledge/LINUX_PLATFORM.md).

2026-11-01 — Reviewed MM-X master-tici b9b7f488 as a Linux reference, with20
Gitblob matches/13ASTparses. Identified reusable backend/camera/service concepts
and non-transferable KGSL, synthetic-clock, localization, calibration and old
schema assumptions. Source-only; implementation held for owner instruction.
See [MM-X study](Knowledge/MM_X_LINUX_REFERENCE.md).

2026-11-01 follow-up — Explained platform detection as hardware routing rather
than an OS-only check. Q8B needs no Rockchip detector; unchanged generic Linux
selection is correct, while CPU/model, camera, sensor and hardware-health gaps
remain. Source-only clarification, no application/OS edits.

2026-11-01 follow-up — Observed real DT modelRadxaDragonQ8B and compatible
radxa,dragon-q8b/qcom,sc8280xp. Proposed explicit board detector/HardwareRadxa,
keeping Linux build/non-comma flags and consistent schema/C++/camera identity.
No implementation applied; plain new device-type string alone would be invalid.

2026-11-01 clarification — Explained recognition, hardware-interface translation
and shared message/camera identity as separate jobs. Proposal remains unapplied.

2026-11-01 — Owner authorized board identity; implemented protected12e44fee.
11 Python/4 native wire checks, actual SCons profile, mutation rejection, Ruff,
syntax/diff checks pass. Read-only command confirms Ubuntu/ARM64/Q8B. Camera
geometry unconfigured; no full build or driving stack launched.
[Session](Sessions/2026-11-01-radxa-board-identity.md).

2026-11-01 — Owner corrected project location. Existing Radxa repository moved
into sunnypilot, clean upstream moved to q8b/sunnypilot-upstream. Real tracked
Ai replaces external link; old notebook history retained. Daily config/hook
retargeted; README and agent rules corrected. See
[session](Sessions/2026-11-01-project-location.md) for verification.

2026-11-01 — Explained existing board identity/build/schema/camera safeguards,
project memory and tested limits at b7fff536. No new application changes or
runtime launch. [Session](Sessions/2026-11-01-changes-explained.md).

2026-11-01 — Confirmed Git tracking to owner: source520d7f2 clean, journal
hook targets canonical project; all17managed local commits had validation.
Audit closeout is documentation only.

2026-11-01 — Owner made Agent Skills + REA and teacher/student restart continuity
explicit defaults. Added tracked HANDOFF, startup/recovery/closeout instructions,
updated rules and session template; retained T0 as next candidate. Documentation
only; [session](Sessions/2026-11-01-default-workflow-and-resume.md).

2026-11-01 — Owner selected hardware/sensors and deferred cameras. Mapped
accel/gyro/temp/GNSS and board-health API contracts; read-only host inventory
found thermal/power/PWM interfaces but no exposed IIO motion channels. Actual
IMU identity remains pending owner input. No hardware driver/setting/service
change. [Session](Sessions/2026-11-01-noncamera-hardware.md).

2026-11-01 correction — Owner required teacher-first lookup. Recovered known
Adafruit LSM6DS3TR-C/I²C9/0x6a, wiring and prior raw/schema tests from central
IMU/GPS notes and actual retained reports. Corrected model-pending/IIO inference
in current handoffs/map. Initialb62481cc factual-completeness failure retained;
current follow-up rechecks records. No new live I²C sampling or driver changes.
