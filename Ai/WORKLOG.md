# Sunnypilot work history

2026-11-02 — Identified bundled driving model as CD210, verified actual ONNX
SHA/name/ref fingerprint and pinned upstream name source. Read protobuf
metadata/current parser; no inference or pickle execution.
[Session](Sessions/2026-11-02-model-identity.md).

2026-11-02 — Recommended current model/Adreno qualification next, using teacher
reference and CPU parity before live model/UI overlay. No implementation started.
Camera deferral and existing hardware plan preserved.

2026-11-02 — Owner accepts camera milestone for now; delay optimisation
and calibration stay deferred. Saved benchmark baseline and teacher-first
reference pointers for later. No runtime change or new engineering task.

2026-11-02 — Added and ran actual camera-to-UI benchmark:1200steady
frames/19.98FPS,draw-ready59.40msmedian and host frame return89.39msmedian.
37tests/lint and independent raw statistics/restoration pass.
[Session](Sessions/2026-11-02-camera-ui-benchmark.md).

2026-11-02 — Recovered actual preview cadence19.87FPS; current camera-to-UI
latency was not logged. Separated Oct31 standalone42msmedian/57msp95 timings.
Documentation only; no camera/clock/runtime changes.

2026-11-02 — Assessed temporary900px intrinsics: calculated70.834degree
HFOV agrees with old visual estimate only; capture/display is not lens proof.
No runtime change; owner calibration deferral retained. See latest UI session.

2026-11-02 — Added camera-only onroad dashboard launcher with private
messages/Params and owned-process cleanup.32tests/lint pass; live screenshot
viewed,173frames/9.06s, settings restored on close. Model not started.
[Session](Sessions/2026-11-02-ui-camera-preview.md).

2026-11-02 — Owner selected temporary MM-X camera method. Added scoped
720p/focal900 road geometry shared by model/UI; default guard and other
profiles preserved.30tests/lint pass; no model/camera run.
[Session](Sessions/2026-11-02-temporary-mmx-profile.md).

2026-11-02 — Explained automatic lens calibration, target-to-camera versus
vehicle-frame extrinsics, stock online-calibration limits and target-free
COLMAP option. Primary docs/source checked; guidance only, no runtime patch.
[Session](Sessions/2026-11-02-automatic-calibration-options.md).

2026-11-02 — Inspected actual MM-X RK camera/geometry/UI/calibration source.
External intrinsics required by README; focal900/720p hardcoded, mounting
calibration separate. Clarified checkerboard is optional measurement method.
5blob/4AST checks pass; docs only. [Session](Sessions/2026-11-02-mmx-camera-calibration.md).

2026-11-02 — Model layout fixed/qualified in6fea7ecf; owner chose printable
calibration target/tool. Added physical-size vector PDF/SVG, guided full-frame
collector and gated candidate solver.29focused tests, PDF/grid checks and real
Tk synthetic smoke test pass; actual printed-target data remain pending.

2026-11-02 — Teacher recovered AK-Camera60capture/20Hzmodel evidence; owner
approved road-only patch. Added self-contained UVC capture/latest NV12 publisher,
real timestamps, scoped driver-camera deferral and fixed-rate restoration.
21tests/140real IPC pairs pass. [Session](Sessions/2026-11-02-road-camera-patch.md).

2026-11-02 — Owner selected camera work and deferred hardware settings. Mapped
OpenCV capture, webcam publisher, process selection and Q8B geometry guard.
No application change/capture run. [Session](Sessions/2026-11-02-camera-entry.md).

2026-11-02 — Freshly inspected literal MM-X master and master-rk3588:11matched
blobs/9AST parses. Corrected broad answer: full board telemetry is not required
before webcam bring-up; MM-X leaves defaults/disables selected services. No
policy copied/runtime tested. [Session](Sessions/2026-11-02-mmx-rk-webcam.md).

2026-11-02 — Explained PC/Linux policy versus optional webcam input using actual
platform/factory/process source and read-only identity output. Full managed
runtime remains unqualified. [Session](Sessions/2026-11-02-pc-webcam.md).

2026-11-01 — Owner requested end-of-day audit and PC/VS Code shutdown. Fresh
11identity tests pass; clean Git/reference/controller, notebook and journal
checked. Saved tomorrow's H1 thermal starting point in both memories. No
hardware implementation. [Session](Sessions/2026-11-01-shutdown-audit.md).

2026-11-01 — Saved proposed non-camera implementation order from existing Q8B,
MM-X and Jetson evidence. Start with read-only thermal reporting and meaningful
failure/readback/schema tests; power, physical IMU and cooling follow. All
implementation remains pending. [Session](Sessions/2026-11-01-hardware-plan.md).

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

2026-11-01 — Expanded non-camera hardware checklist from current APIs, active
schemas and service consumers: thermals/cooling/power/utilization/IMU/GNSS/time,
network/UI/audio/lifecycle/peripherals and conditional vehicle/CAN/radar signals.
Distinguished outputs/estimates/optional fields and known Q8B evidence; no driver
or runtime change. [Session](Sessions/2026-11-01-hardware-checklist.md).

2026-11-01 — Reviewed MM-X non-camera hardware handling at freshly checked
b9b7f488:9 blob matches/8 AST parses. Compared empty thermal/zero power/GPU,
TICI-only fan/GNSS, real OS resource stats and carState-derived IMU policy.
Source-only, no implementation copied. [Session](Sessions/2026-11-01-mm-x-hardware.md).

2026-11-01 — Consulted teacher Jetson studies first; compared dedicated DP
hardware backend and separate overlay physical-IMU design with Q8B needs.
Fresh6source IDs/4blob/3AST checks; reused prior REA receipts with frozen file
integrity readback, no runtime re-execution. [Session](Sessions/2026-11-01-jetson-hardware.md).

2026-11-02 follow-up: webcam mode does not replace hardware support. hardwared
still reads Q8B providers; PC-disabled IMU/comma-only GNSS do not become active.
Adapt needed real board providers; reuse working OS stats, qualify optional
fitted hardware, and treat CAN/vehicle integration separately. No implementation
or runtime change; H1 thermal reporting remains next.

2026-11-02 model-input qualification: reproduced old packed720pbuffer failing
current modeld's1,413,120byte copy. Road-only output now uses get_nv12_info:
stride1280,Yrows736,UVrows368,UVoffset942080,allocation2,220,032bytes with neutral
padding. Generic mode unchanged. Added Q8B-only720pwarp build configuration.
23focused tests pass;140real frame pairs pass20.001Hz/59.628sourceHz with exact
layout/copy/padding/timestamps and restored settings. Pinned tinygrad92b742f7
CPU warp matches independent NumPy reference for two distinct synthetic views
bitwise; outputuint8[2,6,128,256] matches current ONNXnew_img metadata. No full
model/GPU/managed run or measured geometry claim. Weights65a08adc unchanged.
Owner selected printable target/tool; that next increment is in progress and
calibration guard stays active. New unstaged test_calibration.py is expected
RED until tool implementation; do not mistake it for a failure of this slice.

2026-11-02 — Inspected big pickle statically, recovered teacher's actual big NPU
conversion/timing and separated it from small W8A8 failure. Model identity and
floating-reference accuracy remain open; no runtime change.
[Review](Sessions/2026-11-02-big-model-npu.md).

2026-11-02 — Teacher-first Thneed lookup recovered actual exporter/native replay,
matched comparison and20min-soak evidence. Fresh artifact hash passes; no inference
rerun. Promoted old/current model difference and reusable approach.
[Session](Sessions/2026-11-02-teacher-thneed.md).
