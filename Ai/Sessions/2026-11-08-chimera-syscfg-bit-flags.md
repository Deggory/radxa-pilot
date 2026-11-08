# SYS_CFG Debug/output bit values — November 8, 2026

Owner asked how to configure values and why Debug3rather than1/2/4. Recovered
QA53/topic and searched all preserved firmware Debug/output consumers. Only
Debug&1is used in the two branches; odd1/3enable them,0/2/4do not. No defined
Debug2/4categories or historical reason for3are evidenced. Output1/2/4/8select
four generated report families, combined byOR;15=0x0F, examples3and5explained.

[Updated topic](../Knowledge/CHIMERA_SYS_CFG.md) and [truth table/source pins](../Reports/chimera-syscfg-study-20261108/BIT_FLAGS_FOLLOWUP.json)
record meaning, examples and the read-only desktop bridge. Source—not installed
nightly verification. No setting/profile applied; example Debug1/output1is only
an explanation. No power_saving.h/safety/product/firmware change, USB/device action
or zero-frame fix. Existing write/new-firmware/upstream holds remain.

Teacher/student Q&A/topic/state/worklog/handoff/router/session updated; source
hashes, arithmetic/truth table, report copy/links/previous questions and scoped
diff verified. Notebook increment committed with source/doc validation ledger;
central BIT_FLAGS_READBACK.json records exact commit/clean state. No gate
framework or unrelated REA binary analysis required for this factual follow-up.
Next remains matched installed-image/schema and CAN2reception qualification.
