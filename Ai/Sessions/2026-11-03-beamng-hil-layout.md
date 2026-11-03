## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Owner selected PC monitor → physical Radxa AK-Camera, and PC game gateway ↔ Waveshare CAN ↔ Chimera USB ↔ Sunnypilot. This supersedes the earlier network-camera next step. Added active openpilot/tools/sim/beamng/ PC/Radxa roles, shared CAN mapping/gaps and ordered plan; rewrote the current guide and reference README. No runtime code, DBC, firmware or remote PC files changed; no hardware/game/model launch or CAN transmission.

Recovered teacher facts: CH340 USB-CAN-A, 2Mbaud8N1 AA/55 variable framing; candidate500k CAN; historical Chimera hostbus2→MCUCAN3/connectorCAN2, 16-byte mailboxes/43-byte health and observed de193215 debug version. These do not prove current wiring/image or modern Panda compatibility. Canonical DBC6b90fafe/SHAef6eef74 lacks complete wheels/IMU/session/gear and cruise-status definitions; keep gaps central, no invented IDs.

Final CAN controller outputs must drive an explicit game actuator mapping; curvature-to-position bypass does not validate torque control. Physical bench steering/Interceptor/Core, brake and accelerator remain later. Resolve feedback authority and calibrated endpoint mapping before motion; do not resume the paused standalone VW experiment. Simulated IMU must not compete with stationary physical LSM6DS3TR-C. CD210GPU remains selected.

Next: wire-contract increment1 (speed semantics, versioned canonical extensions, golden vectors, deadlines/bus budget and game command family), then receive-only Chimera, optical shadow, game-only loop, later bench. Source-first Agent Skills: specification/planning, documentation, Git and review. No REA binary question in this documentation increment. Validation receipt: Ai/Evidence/beamng-hil-layout-20261103.json in Sunny; checks cover documentation/reference integrity, not HIL runtime.

Changed paths: openpilot/tools/sim/beamng/{README.md,PLAN.md,pc/README.md,radxa/README.md,shared/CAN_CONTRACT.md}, BEAMNG_RADXA.md, beamng_reference/README.md, readme_wat_we_did.md and student notebook/receipt. Base81d021e30ee4626c43db2e971ed6810016015410; branch radxa/q8b. Source bundle pin5435d67499f66eca58f95882cbe35e9c577e874c; all96upstream files remain unchanged. Runtime GPU artifact eb741641 remains selected.

2026-11-03 BeamNG optical/CAN layout: documentation-only validation PASS. 67 notebook documents/215 relative links/8 pinned repositories/4252 index entries; 7 current guides/26 relative links;96 preserved source files/1160682bytes; 12 existing verifier regressions and existing Waveshare offline self-test pass. No HIL runtime or hardware execution. Receipt Ai/Evidence/beamng-hil-layout-20261103.json.

Packaging correction: .gitignore PLAN.md rule omitted the linked plan from initial2968735. Explicitly track the plan in the follow-up; all5 active guides and linked file targets pass a Git-index presence check. Initial commit alone is incomplete; use the following checkpoint.
