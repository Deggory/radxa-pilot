## November 8 follow-up — partial voltage reply (QA60)

Owner replied “3.3 and 1.8” to the four-reading question. Measurement points
are not yet confirmed. Asked whether these mean CANH3.3V/CANL1.8V to ChimeraGND,
and for the labelled5V/sensor-supply output readings. No new hardware action;
physical gate remains unmet. Do not overwrite historical rail values or treat
this partial reply as a confirmed healthy CAN supply/standby measurement.

# CAN2 initialization and standby — 2026-11-08

## Current finding and outstanding physical check

The repeated temporary500kinitialization completed quickly and printed no new
initialization timeout, but raw reception remains empty. Installed-image boot
code does enable the CAN3clock, configure the CAN pins and drive the printed
CAN2standby outputPA0low. **This is code-path evidence, not measured register,
pin voltage, transceiver power or valid CAN reception.**

The physical part is waiting for the owner's current readings: labelled Chimera
5V-to-GND, CAN2CANH-to-GND, CAN2CANL-to-GND, and separate sensor supply output.
An asynchronous question was sent; no fresh numeric answer has arrived. The
previous4.5Vrail/1..1.15Vbus values remain historical. Current VCC/STB/RXD,
termination and sensor transmission cannot be inferred through this USB API.

## New runtime evidence

Owner “proceed” followed the proposed controller/power/standby investigation.
Reused the same narrowly scoped volatile CAN2=500kcommand as a diagnostic repeat,
now with the debug ring emptied beforehand so initial timeout messages would
not be hidden behind old buffered text. No flash/config/firmware/port change.

- Exact productChimera/serial3a0044001651333038373636/USB003/021 selected.
- Versionv1.0.0-DEV-de193215-DEBUG and128-byte signed-image fingerprint matched.
- Debug ring read via E0IN/ring0 until empty before the command.
- One OUT40/DE/value2/index5000/no data; completed in0.001370793994s (~1.37ms).
- Immediate debug read was empty. Five seconds later1151bytes were read until
  empty, showing ordinary angle/ADC/IGN logs and no timeout/error pattern.
  The later text contains truncated/concatenated records consistent with finite
  ring capacity/background production; it is not a complete lossless log.
- Five-second raw USB capture:5.001342342s,2540reads, every actual length0,
  zero bytes/records on all0/1/2. Independent native zero capture from QA58is
  previous evidence, not a new native run this turn.
- Health before/immediately afterward uptime23897, faults0and counters0;
  placeholder fields do not provide CAN timing/supply/standby measurements.
- Flash before/after identical776bytes, valid CRC, SHA
  4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22.
- USB released and probe stopped. Last requested CAN2rate remains500k; no reset,
  restore, heartbeat, CAN data-frame TX or command to the other board/buses.

The quick command and empty immediate error log argue against this invocation
hitting a printed long initialization timeout. They do not prove BTR/INAK,
filter acceptance, interrupt routing or electrical RXD behavior. No success
message is returned by this handler and no register readback was obtained.

## Installed-image clock, pins and diagnostic capability

Signed image SHAe35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b;
unsigned application SHAa615f53776c056be4f1214373815abafb5791cffe1a910213497a93494e3d1bb.
Reused QA56ARM objdump/extraction and recorded new focused ranges/literal values;
no fresh REA deep analysis is claimed. Its unavailable provider remains a known
limitation. Constants in the full linear dump are not treated as executable code.

| Reviewed path | Artifact pin | Established behavior |
| --- | --- | --- |
| Board detection |0x0800535c, literal0x08005374 | selects table0x0800a080 |
| Board init pointer |table+8 ->0x080067cd | calls common GPIO then transceiver enable(true) |
| Enable all |0x080067b0, called0x080067d4 | enables transceivers1..3 |
| Transceiver enable |0x08006756..7a4 | PC1/PC13/PA0, inverted boolean, therefore low when enabled |
| Output helper |0x08004ebc..4f00 | changes ODR and sets GPIO modeOUTPUT; not just a floating latch |
| CAN3clock |0x0800520c | sets RCC APB1ENRbit27 (0x08000000) |
| CAN pins |0x0800501c..5064 | CAN1PB8/9 AF8;CAN2PB5/6 AF9;CAN3PA8/15 AF11 |
| Init timeout strings |0x0800a143/a15e/a179 | speed-entry/speed-exit/filter-init timeout diagnostics |
| UART debug read |E0dispatch ->0x0800842e | buffered text; no arbitrary register access |

PrintedCAN0/1/2 maps to MCUCAN1/2/3 in the source/table routing contract; this
is not a new physical trace qualification of every connector. In particular
printedCAN2is the CAN3controller in this investigation.

Inspected the actual vendor dispatcher at0x08008168 onward and its D1..E5 and
F1..FFjump tables. D2returns health43, D3/D4signature, D6version, E0UART data,
FFbounded saved-flash config. No BTR/ESR/RCC or PA0/standby read command is
provided by these reviewed paths. B6is an input-capture diagnostic limited to
selector0..4and GPIOA bits3..6; it has configuration effects and does not read
PA0. B7returns a fixed4-byte capability marker. Neither was probed. FBandFCentries go to the default handler,
so the JSON RPC methods present in the later preserved source cannot supply
installed-image register telemetry. No unsupported requests or JSON commands
were sent. UART debug callback source echoes input; no register dump command
was found there. Do not confuse shared Panda APIs with this firmware's API.

The active application include is firmware/chimera/can.h, not the separate
firmware/drivers/can.h. Its receive queue implementation and unrelated shared
Panda safety/power files must be distinguished. The retained power_saving.h
is not used by the reviewed Chimera application startup; its presence does not
prove this board is in software standby. Installed-image BTR/ESR remains unread.

## Electrical interpretation and next step

The accepted Ocelot base drawing routes USB through a BAS40diode to the shared
5Vrail/CAN VCC; 3.3Vlogic and responding USB alone do not qualify CAN supply.
For the referenced TJA1042family, STBlow selects normal mode with healthy
supplies; high selects standby, which cannot correctly receive CAN frames.
VCCundervoltage can force standby even with STBlow, and normal VCCis specified
4.5..5.5V. These datasheet facts do not measure the installed unit's chip supply.
[NXP TJA1042 Rev11, sections7.1/7.2.4 and table1](https://www.nxp.com/docs/en/data-sheet/TJA1042.pdf).

The saved Chimera board photo was inspected again: it shows labelled5V/3.3V
outputs and CAN termination headers. It is a reference photo, not a current
view of the owner's board or proof of current jumper states. Do not infer
Chimera chip-to-bus assignment merely from physical proximity in that photo.
The peripheral IGN output is separate from the internal CAN power rail.
No new supply/wiring change was made here.

First collect the requested labelled voltages. Depending on those results,
qualify CAN2termination and sensor traffic; then qualified actual chip VCC/STB/
RXD probing or a reviewed controller-register diagnostic route may be needed.
No firmware rewrite, flash, broad loopback/speed sweep or physical port move
is automatically authorized by this investigation. Avoid claiming a hardware
fault or a software fix until the measurement isolates it.

## Scope and verification

Baseline projectabe2d2ae1edf0a60b1b71f92bbc294317c997849clean. All76legacy manifest
files, host executable/DBC hashes and submodule pins unchanged. Existing Ocelot/
steering dirty work retained. Saved configuration unchanged; one temporary
same-rate reinitialization only. Probe cleanup verified; GUI left disconnected.
Debugging/Unlazy/documentation/git workflows used; prior artifact evidence reused.
No product code changes or new compiler/unit test claims. Software investigation
increment is recorded; physical verification remains pending owner readings.
