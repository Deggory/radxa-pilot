## 2026-11-03 — C2 controller migrated to modern offline replay

Owner requested implementation after comparing the small modern controller
with the linked C2 directory. Accepted increment: migrate portable control
calculation and provide parser-to-controller offline replay; preserve the
independent zero-live-output boundary until Chimera safety/profile qualification.
The previous11-line controller was a passive placeholder, not a completed
active migration. No physical/game actuation is qualified by this increment.

Fetched linked GitHub directory and c2 branch through the connected GitHub
plugin. Branch resolves to b9a942efd3cb210127bb5efb5cf9ccf6a811c728; all8retained
file Git blobs match. Read every C2 file and current interfaces/schema/parser.
Immutable teacher retropilot source and canonical DBC bytes were not edited.

Implemented modern normalized torque to two-channel steering, bounded speed
taper, asymmetric slew and zero-before-direction-change; separate lat/long
activation, gas/brake scaling and mutual exclusion;100Hz steering/brake and50Hz
gas/relay with immediate disable flush, per-message counters/CRC/hostbus2.
Preview reports held gas between sends. Nonfinite inputs, overrides, faults,
missing selected endpoints, ignition loss, non-monotonic steps/gaps over50ms
and stale accepted state disable candidates.100ms offline age uses the oldest
accepted tracked CAN arrival, not parser update time; empty/bad-CRC/unrelated
traffic cannot refresh it. Arrival age is not source acquisition age.

profiles.py validates immutable explicit calibration; default profile absent.
C2_REFERENCE is deliberately offline/unqualified (1510center,350counts, author
pedal slopes,7mm brake, implicit1m/s²-to-full-pedal slope).350counts yields700
channel difference versus local Core400check. No calibrated measured-torque
feedback limiter or driver-pedal authority is claimed. SSC/motor steering has
codecs but no selected normalized mapping. Zero live tunes/placeholder geometry,
unknown gear and no fake cruise engagement remain. C2 radar forcibly disabled;
no unused Toyota radar parser copied. docs/RETROPILOT.md maps all8C2files.

replay.py consumes timestamped canonical CAN hex and modern CarControl JSONL,
records candidate frames/actuators, actual zero feedback and empty transmitted
CAN. No USB/CAN device is opened. update() never forwards candidates, even with
mutated dashcamOnly. No allOutput, firmware flash, manager/game/model launch,
persistent owner setting, remote PC action or upstream integration performed.

Source: parentbase796059f3457315877ba8d42890d29d0a76ea131b; modern opendbc
baseaa9bff6f5442cef8cb8e25e143ef38865c276ce8, prior04a78352a9605a0e07342146fe8481b7d92ee7fd,
new9da9210adfa4dc213424f36945caccd40182c80d on radxa/retropilot. Canonical
DBC6b90fafe/SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce;
CD210/OpenCL/Thneed eb741641 unchanged. Historical Chimera de193215 observation
is not a current installed-image pin. Child/parent increments remain unpushed.

Validation:44RetroPilot tests,53CAN tests and303broader car tests pass
(314existing subtest skips), Ruff/whitespace pass. RED missing profile import
and expanded controller failures reproduced before implementation. Integration
tests exercise real CANParser -> CarState -> modern apply -> candidate CAN,
including bad CRC/staleness and unconditional zero actual output. CLI help and
notebook verification pass; no real-time/game/physical/MCU-safety test.
Receipt/logs: sunnypilot/Ai/Evidence/retropilot-controller-20261103.json.

Skills used: source-driven-development, interface design, TDD, incremental
implementation, Git and code-review-and-quality, with source-first routing.
Readable-source and offline execution evidence; no REA binary question/result.
Inbox: upstreama86979d2 unchanged,0related pending,8historical failed/blocked
records retained. No new owner question required for this code increment.

Next: implement the receive-only Chimera backend against its actual installed
USB/health format; qualify producer units, selected game/actuator/driver-input
profile and canonical telemetry gaps. Then shadow/game-only loop and enforced
MCU safety/limits before any live physical output. Do not promote C2 constants
or an offline preview to a tested Sunnypilot/Chimera integration.
