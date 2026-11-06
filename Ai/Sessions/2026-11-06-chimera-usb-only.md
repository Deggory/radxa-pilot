# November 6 — USB-only transport requirement correction

Owner: “no spi is needed since we will use usb only”. QA24 synchronizes this exact
request/answer in teacher and student, retaining unanswered/historical entries.
Owner's setup is USB-only between Radxa and Chimera/selected legacy Panda. No SPI
wiring/probe/automatic fallback. Corrected earlier preservation framing as generic
inherited source, not deployment need. Startup source still opens SPI; T08 must
replace it using qualified pinned USB selection, exclusive ownership and bounded
reconnect, with failure remaining disconnected. No fake runtime-switch claim.

Startup read routers/resume/handoff/state/tasks/Q&A/inbox, real clean radxa/q8b
HEADc668f6757da3e6a693d9738e99bdc0b5b81b7529. Native panda.cc constructor/list and
USB factory declaration confirm current gap. Existing decoder/backend work stands.
T05c per-bus health remains next; USB-only T08 integration follows prerequisites.

Changed seven active Chimera docs/rules and both notebook layers/decision/Q&A.
No production source, build, firmware, dependency, device or configuration change.
No runtime test needed for prose/requirement correction; link/memory/whitespace
validation follows. Prior6native/15Python/ASan results remain historical, not rerun.
No board access/flash/reset/CAN/relay/actuation/install/update/push. Ocelot/archive/
DBC preserved by no edits; upstream checks held. Physical USB/power/VBUS/current
recovery and managed readiness remain unqualified.

Documentation/ADRs and Git skills used; teacher-first source/CLI route, no unrelated
REA/binary/provider run. OpenAI Codex, no additional agents/model inference.
[Receipt](../Evidence/chimera-usb-only-20261106.json).

Validation: memory144documents/482relative links pass;135active Chimera
links resolve,9source/doc hashes match; diff whitespace/scope checks pass.
