# Chimera SYS_CFG study — November 8, 2026

The owner asked whether SYS must be configured and requested a deep explanation.
The last actual flash read already has valid SYS_CFG:debug3,output0x0F,watchdog0,
mode0/threshold0,saved CAN rates500/500/0/0kbit/s. No fresh device action here.

This study traces the24-byte record,776-byte block validation/RAM startup copy,
field consumers, raw CAN queue versus separate sensor entries, generated outputs,
whole-block Save/Format and tool/schema compatibility. It does not establish a
SYS-based fix, installed active settings, successful raw reception or vehicle use.

Source findings: saved rate/mode/override fields have no selected app consumer;
0xDEacts on bus0only; SYSoutput0x0Fcontrols message families, not receive buses;
flash Save does not refresh the source's startup RAM snapshot; the CLI zeros
extra bytes; website float CAN layout differs from legacy integer layout. Missing
mapping pointers in some timer/debug paths are source audit findings, not a
measured installed fault. Keep owner-selected CAN2 and existing write holds.

SOURCES.json pins every selected source/range/anchor and known limitations.
LAYOUT.json independently parses the prior CRC-valid snapshot. SITE_DECODE.json
comes from running the actual site's pure decoder and a same-byte encoder round
trip offline. No USB calls, settings writes, reset, flash, CAN TX or source edit.
Central report retains inspected scripts, GATES.md and final verification;
portable student report carries results/source pins and the detailed topic.

The old teacher topic graph was checked and is limited/stale for SYS_CFG; no
current code graph was invented. Source-first/Understand Explain and Unlazy used;
no new REA artifact/decompilation result. Installedde193215source equivalence and
current CAN2electrical/active bitrate remain unresolved, rather than invented.

Verification:3gatesmet/0unmet/0abandoned. Actual source schema/CRC, pure site
decoder roundtrip, changed-byte/source negative controls and notebook/source
preservation checks pass; these are not hardware or installed-image checks.
