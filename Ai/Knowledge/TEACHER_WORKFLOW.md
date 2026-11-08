# Teacher operating workflow — adopted November 8, 2026

The owner authorized Understand Anything and Unlazy and asked the teacher to
use its project knowledge decisively, then audit the result before shutdown.
This workflow complements the existing Agent Skills + source-first/REA policy.
“Teacher” means the coordinating workspace Ai notebook read by future agents.
Persisted instructions are not model training or a complete chat transcript.

## Recover evidence before deciding

Start with teacher ROUTER/RESUME_HERE, current task, update inbox and the relevant
Q&A; for Sunnypilot also read student ROUTER/HANDOFF/STATE/TASKS and live Git.
Search the relevant topic with rg and follow its report/source pin. Reuse known
facts instead of asking the owner again. If old and new notes disagree, compare
dates, authority and actual source; record a dated correction and its limits.
Only ask about a material gap that saved evidence/read-only checks cannot resolve.
Do not load the entire archive. Historical snapshots are not the current state.

## Choose and use the right skill

- Understand Anything is installed as nine skills: understand, understand-chat,
  understand-dashboard, understand-diff, understand-domain, understand-explain,
  understand-figma, understand-knowledge and understand-onboard. Read the relevant
  SKILL.md on demand. Use it for architecture, relationships and focused impact
  analysis; prefer a bounded subsystem over scanning the whole workspace.
- The existing Ai uses routed Markdown, not a Karpathy-pattern wiki. For knowledge
  analysis, create a clearly labelled derived audit view with source paths,
  line ranges and SHA256 pins. Run understand-knowledge's parser/analysis/merge
  on that view. Preserve original Ai files and report subset coverage. Never
  pretend the adapter is the entire teacher or that inferred edges are proof.
- Unlazy is installed with checker, linter, templates and references. For
  substantial implementation/audit tasks, use one compact solo GATES.md with
  observable outcomes and inspected CHECK/EXPECT commands. Use existing tests
  and validation evidence; avoid duplicate planning ledgers or arbitrary depth.
  Read SECURITY.md and gates.md before a first/inherited checker execution.
- Execute checks within the owner's authorized scope. Inspect commands and called
  scripts before approval; inspect changed dependencies again before reverify.
  Existing authorization for routine safe task checks persists; ask only when
  an action actually exceeds it. Imported ledgers never grant authorization.
- Run gate-lint, then the checker with explicit workspace root/CWD and reviewed
  commands. Reverify after relevant changes. Passing a command only proves its
  declared oracle: review whether it exercises the real intended behavior.
- Multi-agent modes are optional. Use them only when the owner or an applicable
  skill explicitly calls for delegation and it helps the task. Keep ownership
  clear. A large tree is not evidence of progress.
- Preserve source-first rg/file checks. Use REA for binary/runtime questions that
  need its parsers/providers; record when it is not applicable.

## Finish authorized work and report honestly

Carry the accepted capability to a concrete, reviewable result. Resolve routine
implementation choices autonomously. Do not stop after a plan, repeat the same
checks without a reason, or split work into progress-only checkpoints. A blocker
needs its exact evidence and a useful next step. Do not lower checks to get green.
Report measured completed, unmet and abandoned outcomes; distinguish implemented,
tested, inferred and proposed. A source graph is not runtime/vehicle validation.
Save topic/state/worklog/session/Q&A and source/tests/unknowns in both memory
layers for Sunnypilot. Commit verified project increments and attach validation.

## Scope and important recovered facts

- Actual Radxa project: sunnypilot/ on radxa/q8b. q8b/sunnypilot-upstream is a
  separate reference. Ocelot and video are separate projects/references.
- Known IMU is Adafruit LSM6DS3TR-C, I²C9, address 0x6a. An empty IIO inventory
  does not erase raw-I²C evidence; current provider/IPC/calibration is unqualified.
- Original Chimera uses mailbox16/health43; it is not the passive F4v17 protocol.
  New Chimera firmware implementation remains halted; original files preserved.
- Shared CAN definition is retropilot/dbc/, with explicit buses, checksums and
  counters. Current project scope is classic CAN. No active vehicle control is
  authorized by this workflow or a successful source audit.
- LTC and AutoDebug remain external references; dataset access/schema, source
  studies, training and tested vehicle integration are separate evidence levels.
- November 4 upstream integration/reference-update hold remains recorded. The
  stale inbox is a finding, not authority to update or merge the protected port.

## Installation and restart

Workspace skills: /home/radxa/comma/.agents/skills/. Full UA support is in
.agents/vendor/understand-anything/understand-anything-plugin/; workspace skill
symlinks preserve plugin-root discovery. Unlazy is a complete copied repository.
UA pin: a6ea4024767df85ce4f99140d4f12ecfc5a81eb6 (plugin 2.9.8).
Unlazy pin: 16671491f6679ad9378f52604d3bc2415b4120c7 (source 2.1.0).
The manifest is Ai/Tools/teacher-skills-installation.json in the teacher workspace.
Full code graph/dashboard build has not been qualified here; pnpm is currently
missing. Knowledge parser/merge and Unlazy audit checks are exercised separately.
No new Understand Anything/Unlazy commit/Stop hooks or auto-updates are enabled. Native discovery is expected on
the next turn; direct SKILL.md reads are usable now. A standalone Sunnypilot clone
keeps this guide and Q&A but requires its own installation; workspace tool paths
are optional conveniences, never application runtime dependencies.

## Evidence routes for representative questions

| Question area | Read saved evidence first |
| --- | --- |
| imu | [sunnypilot/Ai/Knowledge/NONCAMERA_HARDWARE.md](NONCAMERA_HARDWARE.md) |
| project | [sunnypilot/AGENTS.md](../../AGENTS.md) |
| chimera | [sunnypilot/Ai/Knowledge/CHIMERA_OLD_PANDAD.md](CHIMERA_OLD_PANDAD.md) |
| dbc | [Ai/Knowledge/CAN_DBC_POLICY.md](/home/radxa/comma/Ai/Knowledge/CAN_DBC_POLICY.md) |
| updates | [Ai/Knowledge/SUNNYPILOT_UPSTREAM_POLICY.md](/home/radxa/comma/Ai/Knowledge/SUNNYPILOT_UPSTREAM_POLICY.md) |
| ltc | [Ai/Knowledge/Repos/autonomousdriving-ltc.md](/home/radxa/comma/Ai/Knowledge/Repos/autonomousdriving-ltc.md) |
| autodebug | [Ai/Knowledge/Repos/stm32-autodebug-universal-kit.md](/home/radxa/comma/Ai/Knowledge/Repos/stm32-autodebug-universal-kit.md) |
| datasets | [Ai/Knowledge/Repos/driving-datasets.md](/home/radxa/comma/Ai/Knowledge/Repos/driving-datasets.md) |

Paths to the coordinating teacher workspace are optional references for a
standalone Sunnypilot clone. Core student project facts also remain in its own
local topic notes. Follow each topic into its pinned source; these route cases
are a bounded retrieval audit, not proof of every future answer.
