# Radxa telemetry receiver — implemented 2026-11-04

The explicit `RETROPILOT_BEAMNG` platform now reads RP-SIM-1 speed/angle, four
wheel speeds, driver pedal values and actual game cruise status. It remains
receive-only/noOutput,carNotReady and dashcamOnly. Generic physical RetroPilot
settings are unchanged. The shared DBC now includes eight additive simulator
messages; see [the exact wire contract](../shared/CAN_CONTRACT.md).

To inspect saved PC dry-run output from the Sunnypilot root:

```bash
.venv/bin/python -m openpilot.tools.sim.beamng.radxa.receive < beamng-can-preview.jsonl
```

When a qualified Chimera receive adapter is already publishing real `can`:

```bash
.venv/bin/python -m openpilot.tools.sim.beamng.radxa.receive --cereal
```

This monitor subscribes only; it does not open/flash Chimera, change the
manager or generate board health. It rejects stale Cereal publications and
prints decoded IMU components with their explicit BeamNG frame label. It also
reports invalid state after data loss. No new cantools dependency is added to
the Radxa/Sunnypilot runtime. Select `RETROPILOT_BEAMNG` explicitly for the
simulator; arriving CAN alone does not auto-identify a car.

IMU transport/decoding is implemented. Device-frame conversion and a dedicated
simulated localization provider remain pending measured axis/origin checks;
no sensorEvents are fabricated and the stationary physical IMU is unchanged.
Below is the earlier architecture/hardware checklist, retained for remaining work.

---

# Radxa role: physical webcam, Sunnypilot and Chimera

Updated 2026-11-03: Chimera is selected to replace Panda. The modern RetroPilot
receive-only car platform is now implemented; see the project docs/RETROPILOT.md.
The managed Chimera USB backend and complete BeamNG telemetry/motion integration
remain pending. Earlier requirements below describe the remaining integration.

## Keep the existing optical pipeline

Use the USB AK-Camera pointing at the PC monitor. The saved road-only path
captures 1280×720 MJPEG at 60 FPS and publishes newest frames at 20 Hz to the
existing CD210/OpenCL Thneed model and Sunnypilot UI. Preserve current GPU
buffers and scoped maximum-performance setup. Relevant source:

- [camera.py](../../../../system/camerad/webcam/camera.py)
- [camerad.py](../../../../system/camerad/webcam/camerad.py)
- [modeld.py](../../../../selfdrive/modeld/modeld.py)
- [process_config.py](../../../../system/manager/process_config.py)

Keep the existing explicit Q8B road-only bench configuration. Do not launch
`beamcamd`, a network image producer or a second VisionIPC camera owner. Driver
monitoring is deferred; this is not a production driver-monitoring replacement.
The borrowed MM-X focal900 profile remains provisional. Screen edges, glare,
moire, focus and render FOV can affect model output; check them in a recorded
optical run. Existing camera→model timings exclude PC render-to-light latency.

## Add the Chimera transport boundary

Teacher's 2026-10-17 receive-only probe observed Chimera
`v1.0.0-DEV-de193215-DEBUG`, 43-byte health, a 128-byte signature and zero CAN
frames. The source reference uses legacy 16-byte USB CAN mailboxes. Modern
Sunnypilot's native Panda lifecycle/packet format differs. USB VID/PID discovery
alone does not make it compatible, and a stock Panda flash must not be applied
to this custom board.

An explicit Chimera backend must decode/encode the legacy frames, preserve bus
identity, report actual ignition/health/capabilities, publish `can` and board
state, and handle reconnect and single process ownership. Integrate `sendcan`
only after receive-only validation. Never fabricate safety readiness or use
`allOutput` as a substitute for a reviewed MCU safety policy. Saved source
shows a TX path without the modern safety hook; installed behavior needs its
own verification. Source review is not proof of a hardware failsafe.

Historical bus mapping is **host bus2 → MCU CAN3 → connector labelled CAN2**.
This is a candidate route, not confirmation of current cabling/board revision.
Match the actual connector and bitrate before binding the simulator interface;
do not mix host numbering with connector labels.

## Add the Sunnypilot car and simulated motion providers

Parse the canonical CAN contract into truthful car state: speed, distinct wheel
speeds, steering angle/rate, pedals, gear, cruise/buttons and validity. Add the
explicit simulator platform and calibrated vehicle parameters; there is no
ready equivalent in the downloaded Honda-emulation installer.

For an optical simulation, vehicle motion follows the **simulated car**, while
the physical Q8B is stationary. Feed simulated motion into localization through
one explicitly selected bench provider. The known physical LSM6DS3TR-C on
I²C9/address0x6a remains hardware evidence, but must not compete with the
simulated IMU for the same messages. Body axes, gravity, timestamps and source
availability require validation. GPS may be optional depending on enabled
features; its provider must also be explicit.

Translate final car-controller outputs to the agreed canonical CAN command
family; include enable/mode and valid counters/checksums. Keep stale/missing
state invalid and disengage rather than inventing readiness. Record the final
command alongside received state and camera/model times for later loop analysis.

Future backend source belongs here unless a small integration belongs in its
actual owning subsystem. This document does not enable `pandad`, change the
manager, run a model or transmit a CAN frame.
