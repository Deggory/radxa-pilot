Current NPU work: [fresh conversion](Knowledge/NPU_CONVERSION.md). Read the dated session before resuming; the first dataset is rejected and corrected v2 calibration is in progress.

Current result: [live Q8B UI telemetry](Knowledge/UI_TELEMETRY.md).

Current performance result: [maximum mode and resident GPU baseline](Knowledge/MAX_PERFORMANCE.md).

2026-11-02 latest: [installation](Knowledge/INSTALLATION.md) now documents a clean
locked environment and passing minimal root build; start HANDOFF for checks/limits.

2026-11-02 latest: [live Thneed modeld integration](Sessions/2026-11-02-thneed-modeld.md)
verified camera→stock modeld→actual Sunny overlay at20Hz bench. Start HANDOFF for limits/launch.

2026-11-02 latest: [existing Thneed import](Sessions/2026-11-02-thneed-import.md)
provides copied CD210 plus in-project native GPU replay/current-queue adapter. No reconversion.

2026-11-02 GPU reference: [teacher Thneed pipeline](Knowledge/THNEED_GPU_REFERENCE.md)
records tested exporter/replay, exact artifacts and sustained timings; CD210 learned weights match; old/new history wrappers differ.

# Start here: Sunnypilot repository memory

2026-11-02 latest: actual Sunnypilot onroad camera preview now verified;
see HANDOFF/resume for launch/active-session state. Model integration pending.

2026-11-02 latest: owner chose temporary MM-X720p/focal900 geometry in Q8B
road-only mode; automatic/checkerboard work deferred. Start HANDOFF/resume.

Latest camera checkpoint: padded model layout fixed; [printable target/tool guide](../openpilot/system/camerad/webcam/CALIBRATION.md)
ready after owner choice. Actual lens data/focus/mount and model backend remain
unqualified. Start HANDOFF for the physical print/capture step, not hardware H1.

Current scope2026-11-02: owner deferred hardware-setting changes and selected
camera work. Start [camera path](Knowledge/CAMERA_PATH.md), then HANDOFF. This
supersedes the older camera-deferred/hardware-first statements below.

Jetson hardware reference: [two teacher studies compared](Knowledge/JETSON_HARDWARE_REFERENCE.md).

Current owner focus: [non-camera hardware/sensors](Knowledge/NONCAMERA_HARDWARE.md);
camera work deferred. Known IMU:Adafruit LSM6DS3TR-C/I²C9/0x6a from teacher
evidence; see HANDOFF and the map for prior tests/current integration gaps.

After reopening, start with [HANDOFF.md](HANDOFF.md). It records where we left
off, what is verified and the next step. Check live Git/files before resuming.
The default Agent Skills + REA workflow and both-memory closeout are standing
owner instructions; see [skills](Knowledge/SKILLS.md) and REPO_RULES.

Current location: this `sunnypilot/` is the project, branch `radxa/q8b`.
`Ai/` is a real tracked directory. Other workspace folders are references or
development tools. See [location correction](Sessions/2026-11-01-project-location.md).
Historical entries below may describe the superseded external notebook layout.

Current implemented identity and checks: [what we did](../readme_wat_we_did.md),
[2026-11-01 session](Sessions/2026-11-01-radxa-board-identity.md).

1. When working in the Comma workspace, read its [ROUTER](/home/radxa/comma/Ai/ROUTER.md) and
   [live update inbox](/home/radxa/comma/Ai/SUNNYPILOT_UPDATE_INBOX.md).
2. Read [STATE.md](STATE.md) and [TASKS.md](TASKS.md). Check actual Git HEAD,
   branch and dirty state in the checkout being discussed. Vendor and Radxa
   port are separate repositories with different purposes.
3. Pick a topic below; inspect its referenced source before changing behavior.
4. Before finishing, update this notebook and promote durable cross-project
   facts plus a concise session record to the workspace Ai memory.

| Question | Read |
| --- | --- |
| What is this repository and where is each subsystem? | [Architecture](Knowledge/ARCHITECTURE.md), [module map](Knowledge/MODULE_MAP.md) |
| What does system code do, file by file? | [System review](Knowledge/SYSTEM.md) |
| What changes for Radxa and what already works? | [Q8B port](Knowledge/RADXA_PORT.md) |
| How does Ubuntu/Linux differ from AGNOS platform selection? | [Linux detection and Q8B plan](Knowledge/LINUX_PLATFORM.md) |
| How does MM-X adapt Sunny to PC/Linux? | [Pinned MM-X reference](Knowledge/MM_X_LINUX_REFERENCE.md) |
| Which branch/model/runtime/version are we using? | [Versions and update workflow](Knowledge/UPSTREAM_AND_VERSIONS.md), STATE |
| What did we change, test or decide? | [Worklog](WORKLOG.md), [validation](VALIDATION.md), [decisions](DECISIONS.md), Sessions |
| What is unfinished or uncertain? | [Tasks](TASKS.md), [questions](QUESTIONS.md), [coverage](Knowledge/COVERAGE.md) |
| Which skill applies? | [Skill workflow](Knowledge/SKILLS.md) |
| Where is a tracked source file? | [Pinned source index](Evidence/source-index.json); search a matching entry, not the whole JSON |
| Where are deeper historical symbols/message traces? | [Existing brain index](/home/radxa/comma/Ai/AI_BRAIN/00_MASTER_INDEX.md); verify freshness first |

Useful checks:

```bash
git -C /home/radxa/comma/sunnypilot status --short --ignore-submodules=none
git -C /home/radxa/comma/sunnypilot rev-parse HEAD
git -C /home/radxa/comma/q8b/sunnypilot-upstream status --short --ignore-submodules=none
git -C /home/radxa/comma/q8b/sunnypilot-upstream rev-parse HEAD
git -C /home/radxa/comma/sunnypilot log -5 --oneline
```

If source HEAD differs from a topic's recorded pin, its findings are historical
until the relevant diff is checked. Preserve old evidence and date the new
finding. Do not silently rewrite an old test into a claim about the new source.
