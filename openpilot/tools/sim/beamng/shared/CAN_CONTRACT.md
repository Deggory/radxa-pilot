# Shared CAN contract and unresolved mappings

Source review, 2026-11-03. This is a mapping/gap record, **not a new wire protocol**.
No DBC bytes, firmware or runtime have been changed.

## Canonical source

Workspace canonical file: `retropilot/dbc/ocelot_controls.dbc`, pinned to
RetroPilot/opendbc `6b90fafe59e81822bfae58e4ecb080248e9de40d`.
SHA-256: `ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce`.
Follow the workspace CAN_DBC_POLICY and companion `retropilot/protocol/`
checksum/counter implementation. This document records the pin inside Sunny;
future executable deployment must carry the attributed, verified required
assets inside this repository rather than depend on a sibling folder.

| Need | Existing canonical message | Remaining work |
| --- | --- | --- |
| Steering-wheel angle/rate | `STEER_ANGLE_SENSOR` 0x050, DLC6 | Angle signed0.1°, rate unsigned magnitude; validate sign, center and producer validity. Sim PC owns this signal in stage1. |
| Vehicle speed | `SPEED` 0x076, DLC8 | `CAN_SPEED` has no physical unit declared; resolve exact producer/consumer convention and MODE, not a guessed m/s or km/h. |
| Ignition/brake pressed/RPM | `ENGINE` 0x075, DLC8 | Match endian/bit layout, MODE and counter conventions; do not invent engine health. |
| Cruise buttons | `CRUISE` 0x100, DLC8 | CANCEL/SET_DOWN/RES_UP/ON_OFF exist. Available/enabled/set-speed need explicit semantics or an extension. |
| Four individual wheel speeds | No dedicated four-wheel message | Central DBC extension required; retain four distinct physical values and validity. |
| Acceleration/gyro and source timing | No IMU message | Central DBC extension required; define axes, gravity, SI scales, grouping/sample identity and stale behavior. |
| Gear and simulation session/pause/heartbeat | No dedicated complete messages | Central DBC extension or explicitly agreed existing semantics required before integration. |
| Steering actuator request/status | 0x12E/DLC6, 0x12F/DLC7 | Candidate actuator family; modes and physical torque mapping must match selected endpoint. |
| Steering Interceptor request/status | 0x300/DLC6, 0x301/DLC8 | Different family: two channel commands and sensor status; raw ADC is not calibrated Nm. Deferred bench selection. |
| Gas pedal/actuator | 0x200/0x201, 0x400/0x401 | Different endpoint families/scales; choose and calibrate one. Neither is automatically a normalized game pedal. |
| Brake actuator/iBooster | 0x10E/0x10F, 0x20E/0x20F | Different endpoints; position/relative/mode semantics need explicit mapping. |
| Engagement/health/override | Distributed command enable/mode and endpoint status | Define overall state machine. No universal engagement bit or safety guarantee should be inferred. |

Preserve ID, DLC, endianness, signedness, scale/offset and exact checksum/counter
rules. A checksum is not a timestamp; a repeatedly refreshed old sample must
not become fresh. `STEER_ANGLE_SENSOR` rate magnitude cannot recover signed
rate without separate angle/time logic. Nominal DBC range annotations are not
proof of calibrated physical limits.

Historical demo steering IDs0x22E/DLC6 and0x22F/DLC7 conflict with canonical SSC
IDs0x22E/DLC5 and0x22F/DLC8. Legacy steering sensor0x301 used a partial CRC;
canonical status covers the full payload. Do not reuse those demos by changing
IDs alone. No new extension IDs are allocated here.

## Routing and signal ownership

Proposed first-stage bus: isolated classical CAN, candidate500kbit/s, PC
Waveshare ↔ Chimera. Historical Chimera hostbus2 maps to MCUCAN3/connectorCAN2;
confirm revision and cabling before use. Real Interceptor/Core, pedal, brake
and angle publishers stay off this simulator bus in stage1. Document the
actual termination, port identity and CAN error state before a live check.

PC publishes simulation telemetry; Radxa publishes accepted controller commands;
PC emulates only the endpoint status needed by the selected simulator port,
clearly logged as simulated. Chimera alone supplies its real transport/board
health. Never emulate that board health to force engagement. Each CAN ID has
one publisher per bus. Later bench status and measured angle must replace the
corresponding simulated publishers, with explicit routing and authority.

## Required timing and failure contract

Before enabling transmit/control, specify per-message rates/deadlines, units,
counter start/wrap/gap handling, full CRC vectors, reboot/session identity,
simulation pause/reset, receiver receipt times and source-sample age. Classical
CAN needs an agreed heartbeat/sample grouping design and a bus-load budget;
do not add arbitrary timestamp bytes to existing messages. Cross-host clock
offset uncertainty must be measured before claiming end-to-end latency.

Receivers reject nonfinite/out-of-range/malformed, duplicate or stale state as
defined by the reviewed contract. Telemetry timeout, command timeout, disabled
mode, operator stop and session reset must terminate game control independently
at the PC. Host shutdown is not proof that a physical motor stops; later bench
operation needs verified endpoint watchdogs, limits and stop behavior.
