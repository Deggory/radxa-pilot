# CAN-side low-voltage explanation — November 8, 2026

Owner question and yes reply recorded faithfully in QA51; no fresh numbers or
unique clarification inferred. Recovered prior readings and base circuit through
teacher/student routers; reopened primary NXP TJA1042Rev11 sections7.1/7.2.4/
Table7. MCU3.3VUSB versus CANVCC/STB distinction explains a possible failure mode,
not the diagnosed cause. Shared rail/BAS40path and hardcoded healthvoltage0are
source-backed. StoredCAN2zero and current analog readings remain distinct.

See [follow-up record](../Reports/chimera-can-voltage-20261108/LOW_VOLTAGE_FOLLOWUP.json)
for exact sources, dates, hashes, hypotheses and limits. Used debugging/source-
first/datasheet review; no REA binary analysis or gate framework needed for this
factual reply. No new hardware/config/CAN action; no product/firmware/DBC/update.

Teacher/student Q&A/topic/state/worklog/handoff/router/session and report updated,
source/doc checks verified, notebook increment committed and maintenance evidence
recorded centrally. Actual commit/clean readback saved in central voltage report
LOW_VOLTAGE_READBACK.json. Next short/direct USB labelled-rail comparison and
qualified actualCANVCC/STB/waveform if needed; current readings/root cause open.
Existing holds retained; no automatic rewiring/power injection/config repair.
