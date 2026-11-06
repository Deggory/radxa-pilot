# Chimera bus and input source contract

November 6, 2026 — T02b source contract. Tables preserve the reviewed topology;
source-selection/freshness rules below are design requirements for subsequent
implementation. The bootstrap only sets GPIO modes/levels and exposes metadata
through its pure query handler. No acquisition, parsing, reporting or CAN TX is
implemented. See [the flash/GPIO contract](BOARD_FLASH_CONTRACT.md).

| Physical board bus | MCU / host bus | Role and delivery rule |
| --- | --- | --- |
| CAN0 | CAN1 /0 | Cores and controlled devices; eventual canonical generated reports on0 retain that provenance |
| CAN1 | CAN2 /1 | Radar/ADAS; requires an actual sensor-specific decoder before supplying Sunnypilot radar data |
| CAN2 | CAN3 /2 | Vehicle CAN and retrofit sensors; original configurable OEM extraction operates here |

Raw receive from all three buses must remain distinguishable. Do not relabel
locally generated CAN0 reports as physical bus2 RX, or treat transmission/echo as
receive delivery. Current RetroPilot host parsers/safety expect bus2; integration
must explicitly select the qualified source and delivery path. All buses and
transceivers remain disabled in the bootstrap.

| Signal/interface | Direct source retained | Alternative/future processing |
| --- | --- | --- |
| Ignition | PA3 active-low/pull-up | Configured vehicle CAN on2 is a separate ignition source; combined power policy must be explicit |
| Brake | PA6 active-low/pull-up | Configured vehicle CAN on2; retain driver/direct provenance |
| Vehicle speed | PA4 falling-edge pulse source | Configured vehicle CAN on2; pulse scaling, stopped/invalid rules need qualification |
| Crank/RPM | PA5 falling-edge pulse source | Configured vehicle CAN on2; pulse count/period and RPM are distinct quantities |
| Analog1/2 | PC2/PC3 channels12/13 | Raw acquisition, calibration and button matching follow separately |
| Steering angle/fraction/rate | No new direct source assumed | Original configured CAN entries1/2/3 on2; validate units, endian/sign/DLC and paired-angle freshness |
| Core/device status | CAN0 | Use the canonical message definitions and explicit producer identity |
| Radar | CAN1 | Sensor protocol and installation are not inferred from bus role |
| Onboard relay | PB0 low/off bootstrap | Keep physical interface; power, ignition and fault cutoff behavior remain separate qualifications |
| OBD-C request / ignition output | PA2 active-low input /PB1 high/off | Accessory sequencing/current behavior unqualified; keep disabled operational capability |

One selected source must own each derived driving signal. Expose source validity
and age; no silent fallback between direct and CAN values and no use of a stale
last value as a valid stopped/brake/ignition state. OEM IDs/scaling/integrity are
vehicle-specific configuration, not a universal OBD PID list. Required DLC,
checksums/counters, rate/freshness limits, calibrations and fault responses must
be specified and tested in their acquisition/parser increments before use.
Exact numeric thresholds are intentionally unresolved rather than guessed here.

Canonical payload source is workspace `retropilot/dbc/ocelot_controls.dbc`, SHA256
`b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67`.
No DBC is copied or changed in this slice. Original Chimera emits report groups
0x50/DLC6,0x75/DLC8,0x76/DLC8 and0x100/DLC8, nominal20Hz, with J1850 CRC8/counter
code. Their IDs alone do not prove compatible sign/bit/scaling/MODE semantics.
Known legacy extraction/config defects and ambiguous report fields remain listed
in [the deep source review](../../Ai/Reports/panda-chimera-deep-review-20261105/README.md);
do not import them as a validated ABI. The [source map](FIRMWARE_SOURCE_MAP.md)
provides the GPIO/build navigation.

Core Config is still a project requirement. Persistent legacy settings remain
untouched at0x08020000. Read/monitor support precedes an exclusive maintenance
write mode; migration of the776-byte settings layout requires a versioned adapter,
CRC/integrity and recovery/power-loss tests. USB control queries do not grant
config or Core write permission. No firmware/relay/OBD-C actuation is enabled.
