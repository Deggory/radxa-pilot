## November 8 — Labelled 5V output confirmed at 5.05 V (QA62)

Owner explicitly assigns the earlier “5.05” reply to Chimera’s labelled 5V
output measured to GND. Current owner readings: labelled 5V = 5.05 V;
CAN2 H = 3.3 V and L = 1.8 V to Chimera GND. Separate sensor supply output
remains unknown; asked one numeric question, measured supply + to −.
This resolves QA61’s supply-point ambiguity, not the missing sensor reading.
The earlier 4.5 V is historical. Labelled output does not establish actual
transceiver VCC/STB/RXD or valid frames. Latest capture remains QA61: zero
USB bytes, with no new capture or device action for this clarification.
G3 remains unmet. Last requested CAN2 500 kbit/s and all existing holds remain.
Evidence: chimera-can-levels-recheck-20261108/SUPPLY_CONFIRMATION_FOLLOWUP.json.

Baseline: `cb581195a1c86ef4016a22dde7d669d5fe6b3916`, branch `radxa/q8b`, initially clean.
Documentation and Git skills used; reused source/REA audit evidence, no new REA or runtime action needed.
Ai-only clarification; no product change or fresh hardware test. Checks: synchronized Q&A/JSON and diff whitespace.
Upstream inbox last checked November 4 and remains stale under the existing update hold.
