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
