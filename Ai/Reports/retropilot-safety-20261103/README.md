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

## What is missing compared with an active vehicle policy

Owner compared the short RetroPilot header with Rivian and requested the full
original C2 file. Current counts: RetroPilot62lines, Rivian187lines; retained
C2 safety_retropilot.h113lines. Exact current source confirms behavioral gaps,
not merely different formatting or shared helper use.

| Active safety behavior | Current RetroPilot | Rivian source example |
| --- | --- | --- |
| Incoming checksum/counter/quality and frequency checks | Not implemented by this mode | get_counter/get_checksum/get_quality_flag_valid and RxCheck table |
| Speed, driver steering effort and pedal state | Not used for active safety | rivian_rx_hook reads speed/driver torque/gas/brake |
| Engagement and disengagement | No received message enables control | Cruise state and common driver/state checks |
| Steering command bounds and rate/driver limits | All active requests blocked; no calibrated bounds | TorqueSteeringLimits and steer_torque_cmd_checks |
| Longitudinal command limits | All active requests blocked; no calibrated bounds | LongitudinalLimits and longitudinal_accel_checks |

The21focused tests validate the disabled-command-only contract; passing them
does not complete or verify these absent active behaviors. Rivian constants
are vehicle/protocol-specific, not a source of RetroPilot calibration values.
Original C2 file remains in optional workspace reference
/home/radxa/comma/retropilot/safety/safety_retropilot.h at Panda9e6d47f.
It labels itself WIP, comments out addr_safety_check at lines42–43, and sets
controls_allowed=1 at line51. It is not a complete active-safety template.
This comparison made no runtime/DBC/firmware changes. Chimera remains held,
relays excluded; profile and feedback contracts are still needed.

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
