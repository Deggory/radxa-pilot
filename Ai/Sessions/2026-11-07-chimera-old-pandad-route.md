# November 7, 2026 — Original Chimera to pandad route

Owner scope: preserve old firmware, improve later, investigate host connection.
QA-20261107-19 is synchronized in teacher/student. Student topic
Ai/Knowledge/CHIMERA_OLD_PANDAD.md contains the existing-versus-proposed map,
ordered implementation candidates, source limits and native acceptance checks.
Evidence: student Ai/Evidence/chimera-old-pandad-route-20261107.json.

Baseline5722805f8aa185ab4cf19a438bdee771dca53b55 onradxa/q8b, clean at start.
Fresh22tests pass with project venv/warnings-as-errors;76legacy size/hash matches;
canonical and packaged DBC match. Source-first rg/selected reads and existing
unit tests used; no REA artifact/runtime work or native/firmware rebuild.
Skills: source-driven-development, documentation-and-adrs, git workflow; planning
skill used for dependency/acceptance guidance. Existing tasks/plan.md and todo.md
are an incomplete unrelated hardware plan, preserved; current repository Ai/TASKS
and the new topic record this research without replacing that plan.

No source/firmware/hardware/config/update/push changes. Saved firmware's 0xDC
request semantics and ignition-driven relay are explicit; host no-write policy
does not prove physical inactivity. Current session gate and managed Panda gate
must be adapted explicitly, not removed. Local CAN1 sensor production is not an
automatic host2 USB feed. Exact installed image/source, wiring, producer units and
modern control enforcement remain open. Next candidate: native Chimera passive
session, leaving new firmware halted. This turn completes the requested research.
Notebook validation and whitespace checks recorded with the local commit ledger.
