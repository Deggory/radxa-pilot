# RetroPilot modern safety increment — 2026-11-03

Owner asked to implement the missing safety identifier, registered rules and
compiled tests. Target is current Sunnypilot on Radxa Q8B. Chimera work remains
held; relays excluded. No hardware, vehicle, board mode or firmware was touched.

## Implemented behavior

Local SafetyModel.retropilot39 is appended to the current vehicle schema and
registered in the C dispatcher.26 remains Hongqi/FAW. This source policy allows
only canonical disabled commands for seven steering/gas/brake endpoints on
hostbus2. It rejects active modes, nonzero engineering targets, reserved bits,
incorrect ID/bus/DLC/CRC, FD/extended/returned/rejected packets, unknown safety
parameters and relay messages. No forwarding or receive-derived engagement.
Brake engineering zero uses raw relative0x7e00/position0x0140, verified against
actual canonical encoders and independent literal vectors.

The port still requests noOutput and its runtime controller sends no frames.
This is a disabled-command-only policy, not a qualified active vehicle policy.
Missing measured actuator/driver limits, RX health/freshness and engagement
contracts are not replaced with C2 constants or DBC numeric ranges. Incoming
frames are passively accepted; their integrity is not qualified by this mode.
All16counter values are allowed on disabled messages, without replay protection.
Local identifier39 must be reviewed for collisions on future upstream updates.

## Validation and review

- TDD RED: new named enum absent, expected test import failure before code.
- Final focused native C suite21tests passes, including debug/release builds,
  all16counters, valid-CRC payload bit mutation, malformed DLC/bus/flags,
  unknown parameters, fault/noOutput transitions and randomized valid-CRC data.
- Full native safety suite8777tests passes,932existing skips. UBSan is enabled
  by the normal harness. [Raw result](full-safety-tests.txt).
- New-policy coverage24/24executable lines and53/53function blocks from native
  gcov. This is not a claim of full branch or whole-project coverage.
-45RetroPilot,53CAN and303broader car tests pass (314existing broader skips).
  A separate test_models base-class invocation ran0and skipped1; not validation.
- Existing Cereal schema serializes/deserializes the new safety enum39. C++
  schema/library build passes. [Build log](cereal-build.txt). Initial direct
  invocation lacked capnpc in PATH; used already-installed venv/bin plus
  capnproto.BIN_DIR. No dependency or SConstruct change. Existing PWD warning
  remains in successful build output.
- Independent code-review-and-quality review found no Critical/Required issue.
  Its wrong-DLC test weakness was fixed: canonical truncation/padding now uses
  a recomputed CRC so content validation cannot conceal broken DLC checking.
- Ruff and whitespace pass. Complete receipts and source hashes are in
  Ai/Evidence/retropilot-safety-20261103.json and the matching coverage receipt.

Full CI gcovr/MISRA tooling is not installed. Native gcov was used for the new
header; no MISRA or firmware-image certification is claimed. Complete readable
sources and actual C compilation/runtime tests supplied evidence; REA skill
routes this source-only work away from unrelated artifact analysis. No REA
analysis, external engines or model conversion were fabricated or performed.

Canonical DBC remains RetroPilot/opendbc6b90fafe, SHA256
 ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
Actual modified paths are modern car/car.capnp, safety/declarations.h,
safety/safety.h, new modes/retropilot.h and tests/test_retropilot.py; package
README/provenance and project docs/notebooks describe their limited stage.
Cereal source, Panda firmware, held Chimera code and model/camera runtime stay
unchanged. Native generated Cereal artifacts were rebuilt locally, not committed.
