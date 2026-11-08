# Chimera 500 kbit/s clarification — November 8, 2026

Accepted scope: answer whether Chimera itself was verified at500k. Used saved
QA48 and raw reports, focused debugging/source-first review. main.c1134/1138/
1142 explicitly configures MCUCAN1/2/3 with5000; llcan.h8defines500k. Printed
CAN2 mapsMCUCAN3/USB2. can_speed defaults match; saved0xDEonly changes bus0.
No generic bus2write, USB read/config action or another game/CAN test performed.

The previous test requested Waveshare500000bit/s, but did not read back installed
Chimera timing. Both readers returned0frames, so working500kreceive is unproven.
Installed de193215image versus preservedsource equivalence is still unknown.
See [selected source pins](../Reports/beamng-chimera-postreset-20261108/BITRATE_FOLLOWUP.json)
and QA49.76manifest hashes/sizes match; source/DBC/native untouched. No new REA
binary/parser work required or claimed. No gates needed for this factual follow-up.

Teacher/student Q&A, topic/state/handoff/worklog/router/session and report are
synchronized. Documentation-only increment committed with source/doc validation;
maintenance ledger distinguishes this passing source review from QA48blocked
physical acceptance. Exact next step remains independent electrical TX/ACK and
Chimera CAN2 qualification; no automatic firmware/config/upstream work. Existing
holds/unanswered entries retained; live Git readback recorded centrally.
