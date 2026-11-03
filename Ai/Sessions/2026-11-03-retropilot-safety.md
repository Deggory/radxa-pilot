# RetroPilot registered safety policy — 2026-11-03

Owner: "fix it then" after identifying missing safety enum, rules and compiled
tests. Accepted scope is current Sunnypilot on existing Radxa Q8B. C2 is only
a protocol/behavior reference. Chimera remains on hold; relay features excluded.
No vehicle/firmware action or automatic upstream integration authorized.

Source baseline: parent 3dd853588be9685ce87cd62ed73b9347a8f2b947, child
86a839dcec8ed9a3e45315eac804fa1001f1b2d6. Child increment committed as
a6099a1e141f17ec18ca9b065cf9a8f972e0cac8 on radxa/retropilot. Parent stays
radxa/q8b. Canonical DBC 6b90fafe/SHA ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce unchanged.

Implemented local SafetyModel.retropilot39, SAFETY_RETROPILOT39, dispatcher
registration and safety/modes/retropilot.h with safety/tests/test_retropilot.py.
The policy allows only seven disabled messages on explicit bus2 with exact
ID/DLC/CRC/mode/target/reserved bits. Brake engineering zero is offset encoded.
Relays, active control, malformed/FD/extended/returned/rejected frames, unknown
parameters and CAN forwarding are rejected. No RX message enables controls.
No measured actuator limits or fresh/healthy RX claims are invented. The
interface still requests noOutput/dashcamOnly; controller still sends zero.
README/provenance and docs/RETROPILOT.md document the constrained stage.

TDD expected RED before enum existed, GREEN with21 focused C tests. Final full
native safety suite8777 passes,932 existing skips. Debug/release compiled with
strict warnings; normal debug tests use UBSan. Native gcov24/24 executable
policy lines and53/53function blocks; not whole-suite/branch coverage.45 car
port,53 CAN and303 broader car tests pass (314 existing broader skips).
Test_models direct base invocation ran0/skipped1 and is not validation.
Cereal Event can carry ID39 unchanged; generated C++ schema/static library
rebuilt successfully. First SCons invocation lacked capnpc in PATH, corrected
with project venv/bin and installed capnproto.BIN_DIR; no package/system/build
source change. Existing PWD warning retained in successful build log.
Ruff and whitespace pass; memory verifier80docs/238links before final notes.
Full CI gcovr/MISRA tools absent; native gcov used for new source, no MISRA or
ARM image certification. No firmware build/flash/board mode or hardware action.

Independent review via code-review-and-quality found no Critical/Required issue;
wrong-DLC coverage weakness fixed using canonical truncation/padding and valid
CRC, then focused21 tests and full8777 tests passed. Review agent was read-only.
Skills: source-driven, TDD, incremental, debugging, Git, documentation, code review.
REA skill routes complete readable-source/new compilation work to normal tools;
no binary-dependent claim requiring REA, no invented artifact analysis.

Changed child paths: car/car.capnp; safety/declarations.h; safety/safety.h;
safety/modes/retropilot.h; safety/tests/test_retropilot.py; car/retropilot/README.md
and SOURCES.json. Parent: submodule pin, docs/RETROPILOT.md and Ai evidence/
report/current state/topic/tasks/decision/worklog/session. Model/CD210/camera,
Cereal source, held Chimera code and canonical DBC untouched.

Evidence: Ai/Evidence/retropilot-safety-20261103.json, coverage receipt and
Ai/Reports/retropilot-safety-20261103/ with actual full-suite/build logs.
Next: qualify active profile/driver limits, RX health/freshness and engagement
contracts; active policy remains incomplete. Do not resume held Chimera or add
relay functionality. Local ID39 collision must be checked on upstream updates.
