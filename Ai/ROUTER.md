## November 5 — GitHub comparison direction corrected

Owner wants Radxa compared against official master. GitHub default changed from
radxa/q8b to master; independent readback passed, all remote branch tips unchanged.
Radxa shows113ahead/3behind master. Counts reflect commit identities, including
separately cherry-picked prior upstream changes. No merge or automatic update.
[Receipt](Reports/github-master-sync-20261105/default-branch.json).
QA-20261105-02 supersedes earlier default-view statements. Chimera remains next.

## November 5, 2026 — GitHub master equals official Sunnypilot

Owner requested GitHub master match real Sunnypilot. Completed normal fast-forward
8cf6ff9a→932ff06d; remote masters independently verified equal. Remote Radxa
f193a3cb and child150f9371 unchanged; default view remains radxa/q8b. Only local
documentation follows. New upstream modeld_v2 low-speed curvature fix was discussed
but is not applied to Radxa. Timer inactive/linked; automatic updates stay paused.
[Report](Reports/github-master-sync-20261105/README.md).
Next remains Chimera receive diagnostics, with noOutput/relay/actuation limits.
Earlier shutdown entries below describe November4; this is the reopened session.

## November 4 shutdown audit — next session November 5: Chimera

Audit/save and GitHub publication verified: fresh165tests pass; DBC and six PC
source/doc files match. Public radxa/q8b and child150f9371pass fresh source-download
checks; default viewRadxa,master8cf6ff9a preserved,Actions disabled. PC kernel42/
GTX1650/595.99.02 healthy; no game/gateway running. Last physical CAN0frames.
Tomorrow November5 start Chimera connector/power/termination/ACK/bitrate and receive
qualification with noOutput and relay/actuation limits retained. Next final action:
normal PC poweroff first,then VS Code/Radxa session shutdown; no force discard.
No automatic upstream update or firmware work now. Central shutdown receipt records
actual request/readbacks; physical completion after host poweroff is not claimed.

2026-11-04 latest checkpoint: NVIDIA repair passed without reboot (GTX1650/595.99.02; kernel38/42 modules; clean dpkg audit); BeamNG runs. Shared RP-SIM-1/PC/Radxa implementation saved at parent880a0adb and child150f9371. Genuine post-start capture492/492 yields valid passive CarState/canValid; 17 focused tests plus regressions pass. Physical CAN gate remains unresolved: genuine game117samples submitted via Waveshare,0Chimera frames. Owner reports CAN3, USB-only Chimera power and Waveshare resistor removed. Next qualify termination, transceiver rails, bitrate and ACK/silent mode; firmware/manager/actuation holds remain. No upstream update or push.

2026-11-04 active BeamNG CAN increment: PC Lua producer/Waveshare gateway, RP-SIM-1 additive DBC, independent Radxa decoder/monitor and explicit receive-only RETROPILOT_BEAMNG profile implemented. 17 focused checks pass plus existing regressions. PC CH340 confirmed and files installed. Live game test blocked by missing NVIDIA modules for running kernel7.0.0-38; owner authorized repair, reviewed package script is waiting for local sudo authentication in PC terminal. No repair success, physical CAN delivery, localization fusion or control is claimed. No reboot or upstream update authorized.

2026-11-04 two-day owner Q&A backfill complete: [62 chronological records](QUESTIONS.md) (47 on November 3,15 on November 4) with [exact original questions/58 completed answers](Evidence/owner-qa-20261103-04.json). Three requests link to clarification continuations; this request has a separately labelled closeout. Existing Q&A/unknowns retained. Local documentation only; no push. Continue recording later questions and read related answers before follow-ups.

2026-11-04 owner requirement:retain questions AND actual answers across sessions. Read [answered owner Q&A](QUESTIONS.md) before related follow-ups; add new answers/status/evidence at closeout.

2026-11-04:public radxa-pilot publication with master/Radxa/RetroPilot history; original commits preserved. [Evidence](Reports/github-publication-20261104/README.md). Upstream updates stay paused.

2026-11-04:owner-approved two upstream updates applied;camera/Thneed/RetroPilot unchanged. Future updates remain on hold. [Evidence](Reports/upstream-approved-20261104/README.md).

UPSTREAM HOLD2026-11-04: read-only GitHub checks allowed; owner approval required before any update. Automatic reference timer paused. Read current upstream policy/session before acting.

History note: [camera/thneed/retropilot subject labels and old/new SHA map](Reports/commit-topics-20261104/README.md). Original evidence preserved; runtime source unchanged.

Restart checkpoint: [RetroPilot audit before shutdown](Reports/retropilot-shutdown-audit-20261103/README.md),168 focused checks pass; live output disabled, hardware holds preserved.

Current2026-11-03: [active safety software checks](Reports/retropilot-active-safety-20261103/README.md), native fixture only; no production profile or live output. Chimera held, relays excluded.

Current safety increment: [restricted RetroPilot policy](Reports/retropilot-safety-20261103/README.md)
registered and tested; active control disabled, Chimera held, relays excluded.

2026-11-03 owner direction: **Chimera work is on hold until the owner resumes it.**
Current discussion is the need for modern RetroPilot messages and why C2 changed
Cereal. Earlier next-step notes about Chimera acceptance are deferred.

2026-11-03 current: [RetroPilot C2 selection compatibility](Knowledge/RETROPILOT_CAR_PORT.md)
now includes fingerprints.py/shared MIGRATION; automatic matching remains pending.

Current2026-11-03: [RetroPilot car platform](Knowledge/RETROPILOT_CAR_PORT.md)
implemented receive-only; Chimera backend/live loop still pending. See HANDOFF.

Radxa simplification assessment: [repository cleanup](Knowledge/REPOSITORY_CLEANUP.md); docs README is the short project entry, no files deleted.

Current BeamNG design2026-11-03: [optical camera + CAN](../openpilot/tools/sim/beamng/README.md), PC/Radxa roles and canonical DBC gaps. Supersedes older network-image next steps below. Runtime implementation pending.

Current BeamNG checkpoint: [complete audit](../openpilot/tools/sim/beamng_reference/AUDIT.md),96source files verified; current opendbc API and simulator contracts block direct integration.

BeamNG files are collected in [sim/beamng_reference](../openpilot/tools/sim/beamng_reference/README.md), exact source pin/verification included.

Current owner task: [BeamNG bridge](Knowledge/BEAMNG_BRIDGE.md); source review complete, adapter not implemented. NPU research paused at rejected baseline.

2026-11-02 fresh NPU baseline: actual200+3 Q8B calls pass execution,
W8A8 accuracy fails;400MB DLC/444MB context, no default switch. Student
`Ai/Knowledge/NPU_CONVERSION.md` and `openpilot/selfdrive/modeld/npu/RESULTS.md`
contain measured per-head errors, retained FP16 failure and proposed next step.

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
