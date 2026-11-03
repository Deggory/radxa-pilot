# PC role: BeamNG and Waveshare CAN gateway

Specification, 2026-11-03; no runnable PC gateway has been added yet.

The game PC renders BeamNG on a monitor for Radxa's physical webcam. It also
owns the Waveshare USB-to-CAN adapter. No image sender or PC screen-capture
daemon is required by this design. Future adapted game mod and gateway source
belong in this directory, with provenance back to the reference bundle.

## Outbound state: PC → CAN → Chimera → Sunnypilot

Collect state from the selected vehicle at known simulation times:

- Vehicle identity/configuration, reset/session, pause state and acquisition time.
- Vehicle speed and separately measured FL, FR, RL and RR wheel speeds.
- Observed steering-wheel angle and rate; retain normalized steering input
  separately. Determine left/right sign and lock for the chosen car.
- Body acceleration and angular velocity with documented axes, SI units,
  gravity convention and sensor origin. A velocity difference alone is not a
  qualified IMU stream. Optional GPS/heading need a separate defined provider.
- Brake pedal, brake applied, accelerator, gear, ignition and cruise/buttons.
  Send actual state while cruise is enabled; do not replace driver pedals with zero.

Validate finite values, ranges, availability and reset/pause before encoding.
Missing data must stay unavailable; do not copy scalar speed into all four
wheel-speed fields. Cruise buttons require press/release edges, distinct from
available/enabled/set-speed status. CAN details are in
[the shared contract](../shared/CAN_CONTRACT.md).

## Returning commands: Sunnypilot → Chimera → CAN → PC

Decode the selected canonical actuator command family, including enable/mode,
counter, checksum and its calibrated units. Use accepted **final CAN commands**
as the input to the game adapter. The downloaded reference's
`desiredCurvature → game steering position` shortcut bypasses final torque
control and is unsuitable for validating the intended actuator path.

BeamNG normalized steering input is a position request, not motor torque.
For torque control, the first game loop needs an explicit simulated actuator
model with angle/rate feedback, saturation and measured delay, or a separately
validated BeamNG torque interface. Later the physical bench can supply the
steering plant. Do not relabel Nm as normalized steering or claim torque-loop
validation from a position conversion. Throttle/brake also need a measured
command-to-game mapping; pedal counts and brake millimetres are not percentages.

The gateway must independently expire enabled commands on stale/malformed CAN,
telemetry loss, pause, vehicle reset, disconnect or process exit. Clear the
latched game inputs using the validated simulator stop policy, and require a
fresh disabled handshake plus explicit re-engagement. Exact deadlines and
stop behavior must be specified and tested before game control is enabled.
Continuing to send old commands must not refresh their validity.

## Reuse and deployment limits

The pinned source's vehicle Lua protocol and rigid camera mod are useful
references: [beampilot_bridge](../../beamng_reference/upstream/tools/beamng_mod/beampilot_bridge/)
and [openpilot_cam](../../beamng_reference/upstream/tools/beamng_mod/openpilot_cam/).
Its BPL1 packet lacks the required source timing/session and complete wheel
state. Its Honda CAN emulation and fork installer are not our shared protocol.
Adapt copies here; preserve reference bytes and MIT attribution.

Teacher records identify the Waveshare CH340 adapter (`1a86:7523`), previously
`/dev/ttyUSB0` on Radxa, and a 500 kbit/s isolated bench. That historical device
path does not select a port on the PC. It is a serial-framed CAN adapter; do
not assume it is SocketCAN or SLCAN. The saved `canreader/read_can.py` selects
2,000,000-baud 8N1, a20-byte AA55 configuration packet and variable-length CAN
records (AA, flags/DLC, little-endian ID, payload,55). Silent mode is0x01;
normal/ACK mode is0x00, and0x02 must not be relabelled silent. Its receiver has
no CAN data transmitter. Adapt and verify that framing for the PC OS/driver
and current device identity before deployment; do not assume serial writes
prove CAN delivery or source acquisition time.

The previous measured PC was Linux BeamNG.drive 0.39.4.0.20972 with a limited
BeamNGpy 1.35.1 subset. These are historical observations, not a fresh check or
proof that all Tech sensors work. No new dependency or mod was installed here.
