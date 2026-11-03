# BeamNG on PC with Sunnypilot on Radxa

The owner clarified the intended hardware loop on **2026-11-03**. Start with
[beamng/README.md](beamng/README.md) for the current architecture and
[beamng/PLAN.md](beamng/PLAN.md) for implementation steps.

**Images:** PC BeamNG → monitor → physical AK-Camera on Radxa → existing
Sunnypilot camera/model/UI.

**State and commands:** PC game/CAN gateway ↔ Waveshare USB-to-CAN ↔ isolated
CAN bus ↔ Chimera USB ↔ Radxa Sunnypilot. Chimera replaces Panda's interface
role; its required software backend is still pending.

Active work is divided into [PC](beamng/pc/README.md),
[Radxa](beamng/radxa/README.md) and the
[shared CAN contract](beamng/shared/CAN_CONTRACT.md). Later bench steering,
brake and accelerator integration is a separate stage with measured feedback.

The former network-camera/VisionIPC producer proposal is superseded. Use the
existing physical webcam producer. Game motion, including the simulated IMU,
must come through an explicitly selected simulation provider; the stationary
board's physical IMU must not silently supply the simulated car's motion.

[The reference bundle](beamng_reference/README.md) retains96 byte-identical
files from Caleb-J773/beampilot-drive
`5435d67499f66eca58f95882cbe35e9c577e874c`. Its
[audit](beamng_reference/AUDIT.md) remains evidence about that source, including
API, timing and curvature-versus-torque gaps; it is not an installed bridge.

The existing `run_bridge.py` selects MetaDrive, not this CAN BeamNG design.
No new BeamNG launcher, managed Chimera integration, PC deployment, DBC change
or hardware transmission has been performed by this documentation increment.
The working camera/CD210 GPU preview remains selected; rejected NPU research
is separate. Required protocol and implementation work is listed in the plan.
