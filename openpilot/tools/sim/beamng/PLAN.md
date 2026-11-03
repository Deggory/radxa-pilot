# Implementation plan: optical webcam + CAN loop

2026-11-03. Owner selected the architecture in [README.md](README.md).
This increment reorganizes and specifies the work. Runtime tasks below remain
pending; the existing source audit does not satisfy their acceptance criteria.

| Increment | Deliverable | Acceptance evidence |
| --- | --- | --- |
| 0 — layout and requirements | PC/Radxa folders, signal/routing gaps, teacher/student handoff | Relative links, source pins, preserved96-file bundle and notebook verification. Completed by this documentation increment. |
| 1 — wire contract | Verify recovered Waveshare framing and resolve exact speed semantics; central versioned DBC additions for wheels/IMU/session/gear and cruise gaps; select game-only command family | Independent golden encode/decode/CRC/counter vectors, ranges/units/axes, publisher/routing table, bus-load budget and explicit timeouts. No hardware TX required. |
| 2 — receive-only transport | PC telemetry collector/offline CAN fixtures and Radxa Chimera reader, then isolated live reception | Distinct wheels, sign/units, mailbox framing/health, actual bus mapping and rates; unplug/pause/reset/stale/corruption tests. Real board identity separated from simulated endpoint state. |
| 3 — optical shadow run | Webcam sees game screen; CAN feeds simulator car state and one simulated IMU provider; model/localization/planning/controller outputs logged without CAN control TX | Existing720p/20Hz contract, screen/lens geometry limits, camera and state age; no physical IMU conflict, truthful validity, final controller outputs traced. |
| 4 — game-only closed loop | CAN return, PC actuator model/mapping and explicit engagement/stop | Selected vehicle/sign/lock/dynamics; bounded lateral tracking, driver brake/cancel, pause/reset/disconnect and stale-command tests; final CAN command path included. Bench hardware excluded. |
| 5 — later physical bench | Interceptor/Core, steering-angle feedback, then brake/accelerator endpoints | Owner-selected feedback authority, calibrated hardware/protocols, single publishers, endpoint watchdog/stop and fault/override evidence before motion. Not authorized or performed by this increment. |

## Exact next task

Start increment1 with saved sources: teacher
`Knowledge/Repos/chimera-panda-transport.md`, `retropilot-cores.md`,
`steer-actuator-demo.md`, workspace `canreader/read_can.py`, canonical
`retropilot/dbc/` and companion `retropilot/protocol/`. The reader source confirms
2Mbaud8N1 and AA/55 variable framing, with0x01silent and0x00normal/ACK modes;
its old Radxa serial pathname is not PC discovery.
Follow the existing central DBC change policy before assigning additional IDs.
Choose the simulator actuator family without implying the later physical bench
endpoint is already selected or protocol-compatible.

The later bench angle authority and actual brake/accelerator models remain
open. Existing steering Interceptor observations are not a calibrated torque
law or a qualified motor-control integration. Do not resume the paused standalone
VW Interceptor work merely because it appears in the dependency list.

## Current verification commands

From the Sunnypilot repository root:

```bash
.venv/bin/python Ai/verify_memory.py --workspace /home/radxa/comma
.venv/bin/python openpilot/tools/sim/beamng_reference/verify_bundle.py
.venv/bin/python -m unittest discover -s openpilot/tools/sim/beamng_reference -p test_verify_bundle.py -v
git diff --check
```

These validate documentation memory and reference integrity, not a working HIL
loop. There is no new runtime launcher or dependency installation for this plan.
