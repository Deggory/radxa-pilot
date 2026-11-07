# Chimera base-power source audit — November7,2026

Owner identifies the Ocelot schematic as Chimera's base, with I/O added. The
[report](../../../chimera/docs/OCELOT_BASE_POWER.md) and
[net data](../../../chimera/hardware/ocelot-base-power-20261107.json) preserve the
result. No firmware/device/flash action was performed.

Replay in the Comma workspace, from Sunnypilot:

```sh
python3 Ai/Reports/chimera-power-schematic-20261107/trace_power.py --workspace /home/radxa/comma
```

The Python standard-library helper prints JSON and performs36selected source
checks. It needs the original Ocelot source files; a standalone Sunnypilot clone
retains the saved report/data without pretending to contain those originals.
The ignored `chimera/build/power-audit-20261107/` contains extraction/replay logs
and the raster rendering inspected from the original Pro attachment PDF.

Coverage: gateway82parts/38nets,17power/USB/CAN nets crosschecked against physical
board pads; Pro1418ASCIIrecords/235wire segments with17selected nets. Pro pin
endpoints use orientation/length; fractional export offsets are normalized to a
0.1unit grid. Selected paths were checked against the original PDF. This is not
full EDA/ERC, a measured PCB trace or firmware integration.

The first exploratory Pro pass used pin-body locations and failed to connect
known nets. Source wire geometry/renderer showed the outer pin endpoint is
location plus direction times pin length. Corrected extraction and the stated
coordinate normalization produce the selected paths in the saved data. Initial
replay-helper lint issues were fixed without suppressions; final Ruff passes.

Main result: host VBUS reaches the shared5V rail through BAS40, with no MCU sense
net. PA9 is unconnected on gateway and header-routed on Pro. The original F4 USB
code forces B-session-valid. Sensed supervision must not use fabricated PRESENT.
Next: explicit opt-in legacy no-VBUS session mode, tested offline and distinct
from actual power/link/heartbeat observations. Production USB remains held.

All existing firmware/host sources, image, references and dirty Ocelot files are
preserved. Validation and exact pins: [receipt](../../Evidence/chimera-base-power-20261107.json).
