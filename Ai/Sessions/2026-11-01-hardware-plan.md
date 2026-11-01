# Hardware next-step guidance — 2026-11-01

Owner asked what to do with the collected evidence. Starting source
1dd194f1aa42cfac8cac0f83e73a2f4ecefe1684/radxa/q8b was clean;
Sunny2026.003.000/COMMA0.11.3, identity12e44fee unchanged.

Applied planning-and-task-breakdown, documentation-and-adrs and Git workflow
skills. Used existing teacher/student evidence and readable source; no new REA
runtime work, upstream fetch, hardware read/write or service launch.

Saved tasks/plan.md and tasks/todo.md: propose read-only temperatures first,
then qualified power, real IMU, cooling and remaining needed services. Missing
sensor/error behavior must be explicit. Existing physical LSM6DS3TR-C native
I²C9 path remains selected; actual mount/axes/current IPC are not yet qualified.
No immediate purchase/rewire needed for thermal slice. Camera work deferred.
All implementation tasks pending; next concrete task H1, not a full-stack launch.

Validation for this documentation checkpoint: notebook verifier with workspace
checks, task-plan local-link validation and git diff --check. Actual command
output is stored with central report and attached to the commit journal.
No new application or hardware test is claimed.
