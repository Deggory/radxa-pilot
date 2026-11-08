# November 8, 2026 — CAN bias, USB rail and ignition explanation

QA34: owner reports1.15V each CANwiretoGND, then4.5V labelled5VtoGND withUSB.
Asked labelled3.3V output next; unanswered at checkpoint. Recovered accepted
Ocelot base-power audit/QA20261107-11, current saved startup and power-saving
source. Fresh source-only trace replay passes36checks. Reopened NXP TJA1042
Rev11and official Chimera/Waveshare references.4.5V is specified lowerVCC
boundary; this is a lead, not proof of actual IC undervoltage or CAN failure.
USBboot/version/health is proven; source shows USB powers sharedCAN5V rail and
CAN startup is independent of ignition relay. No guessed IGN/external supply
or modified firmware action. Correct older missing-schematic interpretation.

Baselinea4dbb199/Ocelotd87892fa; source hashes, owner measurements, primary URLs
and unknowns in teacher/student Ai/Reports/chimera-can-voltage-20261108. No
hardware query/switch/TX/drive, product/firmware/DBC/model/upstream change or push.
Debugging/documentation/Git workflow and source-first evidence; no unrelated
binary/REA or Unlazy gate needed for this factual explanation. Next complete
3.3Vreading and supply/ground/termination checks; prior zeroCAN root cause open.
Actual notebook/QA/whitespace/preservation/commit readback saved centrally.

Owner subsequently answered "3.35" for the labelled3.3V output. This resolves
the pending reading above; it is reasonable for the nominal3.3V rail, while
reported4.5V remains the lower referenceVCC boundary. Fresh lsusb -t/sysfs
identifies Chimera3-4.1behind VIA2109:2812USB2.0hub. A short-cable/direct-port
comparison is proposed, not performed and not a demonstrated hub defect.
No more vendor/device/MCU/CAN action; source/report/QA updated with actual reply.

## IGN input follow-up (QA35)

Owner asks zero-voltage IGN and explicitly requests code/wiki review; confirms
input beside VSS/CPS/BRAKE. Reopened official Chimera guide and read source input/
relay/OBD-C/CAN startup ranges. Explained expected unconnected input at 0 V, nominal external
car ignition 12 V role versus MCU-conditioned input and CAN power/initialization independence.
No connection/relay/power change or CAN fix inferred; USB feed diagnosis remains.
Source baseline 775de304; selected source hashes and fresh notebook/QA/whitespace/
clean readback in central IGN_INPUT_FOLLOWUP.json. Documentation/Git/source-first
workflow; no unrelated binary/REA, gate or fresh firmware/runtime test. No push
or resumed held work. Measurement/board equivalence limits retained.

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
