# Three CAN bus raw-receive expectation — November 8, 2026

Owner asks if connecting any CAN device to any of3Chimera buses should show
output. Source-first trace confirms MCUCAN1/2/3handlers -> can_rx0/1/2 -> RXqueue
-> USBEP1. Conditional expectation only: device must transmit, correct matching
rate/electrical/ACK/controller/transceiver/USB setup required. Some devices are
request-driven. Raw IDs/data do not require angle mappings; decoded values do.

[Topic](../Knowledge/CHIMERA_SYS_CFG.md) and [source follow-up](../Reports/chimera-syscfg-study-20261108/THREE_BUS_FOLLOWUP.json)
retain explicit mapping, conditions and the llcan_init comment about CAN2/3filter
programming difficulties as an unproven software lead. Prior currentCAN2sensor
captures remain0; no new capture, CAN0/1cable comparison, config or firmware fix.
Owner keepsCAN2. All-port operation/installed equivalence remain unqualified.

Teacher/student Q&A/topic/state/worklog/handoff/router/session/report updated;
source hashes/anchors, QA sync/prior items and links/scoped docs verified, then
notebook increment committed with ledger evidence. Central THREE_BUS_READBACK.json
pins final commit/clean state. No device/USB/CAN/port/power/product/firmware/DBC/
model/upstream action or push. Source/debugging/documentation workflow used;
no unrelated REA or gate framework needed for this factual clarification.
