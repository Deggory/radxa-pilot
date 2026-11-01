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
