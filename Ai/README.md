# Sunnypilot specialist memory

This is the repository's “student notebook”: detailed Sunnypilot knowledge,
our work history, tests, decisions and remaining questions. The workspace-wide
[Ai memory](/home/radxa/comma/Ai/ROUTER.md) is the coordinating “teacher”: it
connects this work to Q8B hardware, the shared DBC and other projects.

Open [ROUTER.md](ROUTER.md) first. Load the relevant topic, then verify its
claims against the pinned or current source. This notebook grows as work is
done; a file index is navigation, not proof we understand every algorithm.

| Location | Purpose |
| --- | --- |
| `sunnypilot/Ai/` | Real knowledge directory tracked inside the actual project |
| `q8b/sunnypilot-upstream/` | Clean daily-updated upstream reference, outside the project |
| `q8b/sunnypilot-memory/` | Retained historical notebook Git repository; no active backing role |
| `/home/radxa/comma/Ai/` | Workspace-wide knowledge, policy and shared evidence |

Owner clarification, 2026-11-01: `sunnypilot/` is the working project and the
folder intended for use when ready. This `Ai/` folder travels with it; there is
no external notebook symlink or nested Git repository. New notebook changes
share project Git history. [REPO_RULES.md](REPO_RULES.md) records the workflow.
The upstream reference's ignored links are preserved and protected against
incoming path collisions. Daily jobs only read the project notebook; agents
maintain its prose. Outside evidence links are optional research context.

Keep current facts in STATE, next work in TASKS, rationale in DECISIONS, unknowns
in QUESTIONS, outcomes in WORKLOG and dated Sessions. Knowledge holds topic
explanations; Evidence holds source indexes/pins. Record exact source/model
versions and actual validation results. Link shared evidence instead of copying
large benchmarks, models, firmware, secrets or old virtual environments here.

Memory commits use the existing local commit journal and validation ledger.
No background model learns from this directory: later agents read the files
and update them after tasks. Daily upstream observations remain authoritative
in the [live inbox](/home/radxa/comma/Ai/SUNNYPILOT_UPDATE_INBOX.md).
