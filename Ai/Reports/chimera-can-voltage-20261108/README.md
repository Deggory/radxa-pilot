# Chimera CAN voltage and USB/ignition — November 8, 2026

Owner reports approximately1.15V on CANH and1.15V on CANL, each relative to
GND, using USB-only Chimera power. Follow-up: labelled5V output measures4.5V
to GND. Follow-up labelled3.3V output reading is3.35Vto the same GND.
These are owner measurements; probe point, meter accuracy, load/waveform and
actual transceiver-chip supply have not been independently verified.
[Source/measurement receipt](SOURCES.json).

## Interpretation and ignition

The reference TJA1042 datasheet specifies VCC4.5..5.5V, normal recessive bias
roughly half VCC and loss of normal CAN operation in standby/undervoltage.
Thus1.15V per line is below its usual powered normal-mode idle bias. The reported
4.5V auxiliary rail is at the specified supply minimum; a lower voltage at the
chip or a transient drop is a plausible lead, not demonstrated undervoltage.
Equal line voltages and a DC meter do not prove whether differential CAN pulses
are present. Do not declare the transceiver damaged or supply fault proven.
Primary reference: [NXP TJA1042 Rev11](https://www.nxp.com/docs/en/data-sheet/TJA1042.pdf).

USB already boots this actual board and supports native version/health reads
with reported ignition0. No ignition is needed for that observed USB function.
The owner-accepted Ocelot base schematic (QA20261107-11, with added Chimera I/O)
shows USBVBUS->BAS40diode->shared5V, feeding CANVCC and the3.3V regulator/MCU;
reference transceiver VIO connects3.3V. Existing gateway_init enables all3CAN
transceivers at startup independently of the Chimera ignition-controlled relay.
This supports USB-powered reception as the intended source design, not an
unconditional guarantee about this installed image/assembled board under load.
Do not assume ignition/external12V is a prerequisite merely because USB CAN
frames are absent. IGN/relay-switched connector power is a separate function.

Recovered [accepted base-power note](../../../chimera/docs/OCELOT_BASE_POWER.md)
and [old source map](../../Knowledge/CHIMERA_FIRMWARE_SOURCE_MAP.md). Fresh replay
of trace_power.py passed36source checks. It does not measure rails or prove
current PCB equivalence. This supersedes older November5wording treating the
base drawing as unavailable/inapplicable; current owner baseline is retained.

## Next measurement and limits

The labelled3.3V output reading3.35V is consistent with a nominal3.3V rail. A
controlled check with a short known-good USB cable/direct suitable USB port
and the same5V/3.3V measurements can separate USB feed loss from other causes;
no cable/power change was performed by this source answer. Fresh lsusb/sysfs shows Chimera at3-4.1behind a VIA2109:2812USB2.0hub, making a direct-port comparison useful; this does not prove the hub caused the drop. Avoid probing small
IC pins or supplying power through output rails. Any later termination resistance
measurement must be made with all supplies/USB removed; no resistance value is
currently measured. Shared signal-ground, termination, actual VCC/VIO/STB,
bitrate/ACK and installed firmware remain distinct unresolved factors.

No ignition/relay/config/flash/heartbeat/bitrate/USB/CAN action, new test drive,
product/firmware/DBC/model/dependency change, upstream update or push. Previous
zero-CAN tests remain actual observations; this voltage report does not isolate
their root cause. Debugging and documentation/Git skills plus source-first
hardware/datasheet evidence used; no unrelated REA binary task or completion
gates required for this factual follow-up. Actual36source/notebook/QA/whitespace
checks and final commit/readback are retained centrally.

## IGN input clarification — November 8 (QA35)

Owner reports 0 V and confirms the measured terminal is the separate IGN input
beside VSS/CPS/BRAKE, not CAN2 pin 1. An unconnected input is not expected to
produce an ignition voltage from USB. The official Chimera wiki identifies it
as a car ignition input, nominal 12 V when the car is on, which can power the
board without USB and supply the non-relay ignition-powered peripherals.
CAN connector pin 1 labelled IGN is a separate documented power-distribution role;
this terminal identification does not trace every physical connection between
those nets on this specific Chimera revision.

Fresh source inspection: main.c:1186 configures PA3 as an input with pull-up and
main.c:1026 reads its active-low logical state. These are MCU-side pins behind
board conditioning, not an instruction to apply 12 V to MCU PA3. The loop uses
line-or-CAN ignition to drive PB0 relay and PB1 OBD-C ignition. gateway_init enables
all 3 CAN transceivers and normal mode without an ignition condition. The accepted
base circuit routes USB through a diode to shared 5 V/CAN VCC and downstream 3.3 V.
Actual installed de193215 source equivalence and transceiver state remain open.

For the current USB/Waveshare raw-reception test, leave this IGN input
unconnected rather than bridge it to a USB/logic rail or add an unqualified
12V feed as a guessed CAN fix. Asserting ignition can switch relay/power state;
this is a separate reviewed bench-power/ignition test, not performed here.
The existing low 5 V rail/direct-USB-cable comparison and CAN electrical checks
remain the next diagnostic step. No new hardware action or drive test.

Primary [RetroPilot Chimera wiki](https://wiki.retropilot.org/index/hardware/chimera)
reopened November 8; source hashes/owner clarification in SOURCES.json and the
central IGN_INPUT_FOLLOWUP.json. No firmware/application/DBC change, flash,
relay/heartbeat/config write, upstream update or push; previous holds retained.

## Code activation trace — November 8 (QA36)

The selected GATEWAY application calls board init, usb_init and llcan_init for
all three CAN controllers unconditionally before its main loop. The active
include is chimera/can.h: can_rx queues raw frames without an ignition gate,
and main.c usb_cb_ep1_in drains the queue without one. The relay/OBD-C branch
alone uses ignition_line OR ignition_can. CAN3 can extract a configured CAN
ignition signal before calling can_rx(2); a physical IGN input is therefore
not the only software source for ignition state. PA3 is a conditioned logic
input; code does not measure a literal external 12 V threshold.
Saved moving-test health_first/health_last show both ignition flags zero while
version/health replies work. Exact installed-source identity and actual CAN
rails/enable/termination remain open; no fresh runtime or hardware action.
Baseline 03738248e61f8423de093b550640760d807adec7. Source-first debugging and
documentation verification only; no binary analysis or unrelated graph build.
Central CODE_ACTIVATION_FOLLOWUP.json retains source pins and validation.

## CAN connector IGN clarification — November 8 (QA37)

Latest owner description is the IGN/CANH/CANL/GND connector. Inspected retained
ocelot/hardware/chimera/chimera-board.jpg; its CAN connector labels and separate
IGN/VSS/CPS/BRAKE input are visible. Official wiki identifies CAN connector IGN
as ignition-controlled 12 V peripheral power. With current USB-only power and
no external ignition feed, zero there is expected, not proof of lost internal
CAN transceiver supply. Peripheral power and raw CAN data path remain distinct.
Prior QA35 input identification is historical owner evidence, not overwritten;
this dated clarification records the latest description. No hardware change.
Direct wiki hosted image could not be retrieved (HTTP403/tool error); the local
board photo was viewed instead. Source-first photo/wiki/documentation checks;
no unrelated binary/REA or new graph/runtime test. Source/photo pins and actual
validation receipt: central CONNECTOR_IGN_FOLLOWUP.json. Existing holds remain.

## Voltage-drop follow-up — November 8 (QA38)

Do not interpret 4.5 V as proof that the USB cable alone lost 0.5 V: actual
USB input is unmeasured and the accepted circuit includes a BAS40 series diode.
Forward drop varies with current/temperature (Nexperia BAS40 primary datasheet).
Cable, hub/port supply, contacts and load remain other possible contributors.
The NXP TJA1042 reference range starts at 4.5 V, leaving little margin for chip
voltage below the labelled rail or transient dips; no chip undervoltage is proven.
3.35 V on the logic rail and zero on connector IGN do not qualify CAN power.
Same labelled 5 V/3.3 V points with short/direct USB is the next comparison;
no diode bypass, output injection or physical/runtime action performed.
Fresh primary datasheet checks, saved circuit/measurement review and notebook
validation only. Actual closeout centrally in VOLTAGE_DROP_FOLLOWUP.json.

## CAN voltage range follow-up — November 8 (QA39)

Owner now reports 1.0..1.15 V per wire. Reopened NXP Table 7: normal idle
~0.5VCC (nominal 2.5 V), dominant CANH/L typical 3.5/1.5 V. A DC meter averages
traffic; neither two fixed 3 V wires nor applying 3 V externally is required.
At actual VCC 4.5 V, half-VCC is 2.25 V, so 1.15 V is not explained merely by
that arithmetic rail decrease. Supply/standby/ground/loading/waveform diagnosis
remains unresolved; no new physical test or code change. QA39 and central
CAN_LEVELS_FOLLOWUP.json pin source/closeout; holds preserved.

## Standby code follow-up — November 8 (QA40)

Selected gateway startup drives transceiver enable pins PC1/PC13/PA0 low
through gateway_enable_can_transceivers(true). set_gpio_output also selects
GPIO output mode. Printed CAN2 maps to MCU CAN3 and PA0. A false group call
would hold transceivers 2/3 in standby, leaving 1 enabled by design, but no
such path is used by the Chimera app. power_saving.h contains the generic
routine but is not included/called. Heartbeat's power-save comment is stale:
its executable branch clears relay_req_usb only. health power-save field is
hardcoded zero and cannot qualify physical STB. CAN controller silent support
is separate: startup passes false, whereas DE/E5 reinit helpers consume the
all-silent mask. No command/reconfiguration performed; no state inferred.
NXP STB low selects normal, high selects standby; floating STB has pull-up,
and VCC undervoltage can force standby despite low STB. Source proves intent,
not installed GPIO/STB/VCC state or exact de193215 image equality. Read-only
source/datasheet debugging, no binary/REA task or fresh runtime measurement.
STANDBY_CODE_FOLLOWUP.json retains hashes; central copy holds actual closeout.
