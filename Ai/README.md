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
| `/home/radxa/comma/sunnypilot/Ai/` | Visible notebook inside the daily-updated vendor checkout |
| `/home/radxa/comma/q8b/sunnypilot-radxa/Ai/` | The same notebook inside the protected Radxa development clone |
| `/home/radxa/comma/q8b/sunnypilot-memory/` | Actual independently versioned backing folder, branch `main` |
| `/home/radxa/comma/Ai/` | Workspace-wide knowledge, policy and shared evidence |

Both visible folders are local directory links. This keeps one specialist
memory while preserving upstream source. The vendor's AGENTS.md points to
[REPO_RULES.md](REPO_RULES.md). Neither link is an upstream code modification.
The maintenance controller reserves these vendor paths and blocks conflicting
upstream updates. It only reads this notebook; agents maintain its prose.

Keep current facts in STATE, next work in TASKS, rationale in DECISIONS, unknowns
in QUESTIONS, outcomes in WORKLOG and dated Sessions. Knowledge holds topic
explanations; Evidence holds source indexes/pins. Record exact source/model
versions and actual validation results. Link shared evidence instead of copying
large benchmarks, models, firmware, secrets or old virtual environments here.

Memory commits use the existing local commit journal and validation ledger.
No background model learns from this directory: later agents read the files
and update them after tasks. Daily upstream observations remain authoritative
in the [live inbox](/home/radxa/comma/Ai/SUNNYPILOT_UPDATE_INBOX.md).
