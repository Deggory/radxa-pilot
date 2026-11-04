# PC: BeamNG -> Waveshare -> RetroPilot CAN

Implemented read-only telemetry producer and gateway,2026-11-04. The game is
viewed by Radxa's webcam; no PC image sender is needed. See the
[shared protocol](../shared/CAN_CONTRACT.md) for definitions and limits.

Installed PC bundle: `/home/pc/beamng-q8b/retropilot-can/` on the saved Linux PC.
It has its own `.venv`, not changes to the existing Beamng-onnx environment.
`pc/gateway.py` uses cantools40.7.1 and a hash-verified copy of our shared DBC.

The [Lua mod](mod/lua/vehicle/protocols/radxaRetropilot.lua) reads measured
steering angle, aggregate speed, RPM/ignition, separate driver/applied pedals,
gear index, acceleration, gyro, four independent kinematic wheel speeds and
cruise status/set speed if available. Unavailable fields have explicit validity
bits. It does not drive the car, change cruise, set a camera or operate actuators.
The generic button API is unknown: cruise enabled/set-speed is sent as status;
button bits remain explicitly unavailable rather than invented.

## Install and start on the PC

Open a terminal on the PC:

```bash
cd /home/pc/beamng-q8b/retropilot-can
.venv/bin/python pc/install.py --user-folder /home/pc/.local/share/BeamNG/BeamNG.drive/current
```

Open BeamNG, choose the car/configuration and turn on **Options > Other >
Other protocols**. Press Ctrl+R to reload the vehicle. Other protocols enables
all installed third-party protocol mods; review those if others are installed.
The installer supports `--enable` for an offline settings change with a backup.
It only writes a user-folder mod and optionally that setting, not game binaries.

First inspect real game data without opening the CAN adapter:

```bash
.venv/bin/python pc/gateway.py --duration 10 > beamng-can-preview.jsonl
```

Then, on the isolated simulator CAN bus, start telemetry transmission:

```bash
.venv/bin/python pc/gateway.py --serial /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 --transmit
```

Default bitrate500kbit/s,serial2Mbaud8N1. Ctrl+C stops the gateway. Source silence
or pause stops new telemetry, so the receiver expires it. The current CLI is
Linux-only; do not use SocketCAN/SLCAN settings for this serial-framed adapter.
Waveshare and Chimera need matching bitrate, correct CAN-H/L, termination and a
working ACK participant. A serial write is not confirmation that Chimera received it.

## Copying from another checkout

The PC bundle needs `pc/` and `shared/`, plus the packaged canonical
`opendbc_repo/opendbc/dbc/ocelot_controls.dbc` copied to `pc/ocelot_controls.dbc`.
Create its own Python3.12 virtual environment and install `pc/requirements.txt`.
Do not copy a sibling research checkout or replace an existing model environment.
For tests on Radxa use a separate test environment with cantools40.7.1 and
lupa2.6 exposed only for that command; the Sunny runtime needs neither dependency.

Commands returning from Sunnypilot and a calibrated game actuator model are
outside this telemetry stage. No desired-curvature shortcut or actuator TX is
implemented. Chimera's receive/manager/firmware qualification remains separate.
