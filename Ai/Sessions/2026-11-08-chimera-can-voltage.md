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
