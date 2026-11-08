## 2026-11-08 — Understand Anything and Unlazy suitability (proposed only)

Owner asked: "can understand-anythiing and unlazy skill help our project".
Assessed Egonex-AI/Understand-Anything at `a6ea4024767df85ce4f99140d4f12ecfc5a81eb6` and
Leonxlnx/unlazy at `16671491f6679ad9378f52604d3bc2415b4120c7`, using their pinned README and
SKILL.md sources. Understand Anything combines deterministic source parsing
with LLM summaries and an interactive architecture graph; incremental updates
and exclusions are supported. A focused camera/model/messages/UI map could help
explain relationships alongside our existing module maps. Initial whole-repo
analysis can consume substantial tokens. The analyzed source graph does not
establish runtime behavior, complete C/C++/macro/generated-code coverage or
hardware compatibility. Its build instructions request Node >=22/pnpm >=10;
the separate already-generated dashboard reader documents Node >=18.

Unlazy adds command-backed CHECK/EXPECT gates, evidence binding and re-verification.
A compact solo ledger could make unfinished capability visible, but overlaps
existing plans, tests, validation ledger and handoffs. Its Stop hook is specific
to Claude Code. Passing checks only proves declared command oracles; it cannot
judge whether they cover the real requirement. The README calls current source
2.1.0 unreleased; checker requires Node >=16. No local compatibility/performance
or reliability benefit was measured.

Recommendation: optional focused graph and acceptance gates for substantial work;
keep existing Ai authoritative, avoid deep decomposition/duplicate ledgers and
whole-workspace scanning. This is an assessment, not adoption or authorization
to install, run candidate scripts, enable hooks, resume halted Chimera work or
change upstream updates. Source-first/REA remains the standing workflow; no
binary/runtime question required REA here. Candidate files were read as evidence,
not invoked as installed skills. Existing unanswered questions remain open.

# Agent skills for Sunnypilot work

Owner requires relevant installed `addyosmani/agent-skills` alongside the
source-first/REA workflow. Installed pin:
`aeac41d4d005999432bb7312f7ff06383a91d59d`, version 0.6.13.
Policy: [AGENT_SKILLS_POLICY.md](/home/radxa/comma/Ai/Knowledge/AGENT_SKILLS_POLICY.md).

| Work | Read the relevant installed SKILL.md |
| --- | --- |
| Context and persistent notebook | `context-engineering`, `documentation-and-adrs` |
| Repository/source research | `source-driven-development`, `code-review-and-quality` |
| Branching, commits, conflict/integration review | `git-workflow-and-versioning` |
| Multi-file implementation | `incremental-implementation` |
| Behavioral change or bug | `test-driven-development`; `debugging-and-error-recovery` for failures |
| Camera/model/message interface | `api-and-interface-design` |
| Timing, buffers and measured speed | `performance-optimization`, `observability-and-instrumentation` |
| Nontrivial work breakdown | `planning-and-task-breakdown`; spec workflow when a new feature needs a contract |

Files live under `/home/radxa/comma/.agents/skills/<name>/SKILL.md`. Select by
actual task, read on demand and announce first use. Do not preload all skills
or impose web/browser requirements on native hardware work. Preserve exact
sources, tests and limits; user scope and higher-priority rules take precedence.

For ordinary source use rg and selected ranges. Use REA when binary/artifact
parsing or runtime evidence answers the question. Availability does not require
an irrelevant binary analysis or authorize executing firmware/hardware actions.

## Default workflow and restart persistence — 2026-11-01

Owner reaffirmed Agent Skills + REA for every project change, without repeated
reminders. Select relevant skills on demand and use source-first checks plus
REA artifact/runtime evidence when applicable. Explicitly record used skills,
evidence, exact tests and limits; record when REA is not applicable to a
source/documentation task. This instruction does not require irrelevant binary
analysis, install tools or authorize hardware operations.

At startup/reopen read [HANDOFF](../HANDOFF.md), STATE/TASKS and current Git.
At completed increments/closeout save accepted scope, changed paths, source/
model/runtime identities, verification, dirty work, decisions and exact next
step in student and teacher notes. Unexpected shutdown recovery compares notes
with actual files; do not discard work or assume missing checks passed.
