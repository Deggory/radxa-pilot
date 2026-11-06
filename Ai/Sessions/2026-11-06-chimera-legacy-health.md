# November 6 — Legacy F4 health59 native decoder/read helper

Owner “proceed” continues T05b from QA22. Startup read teacher/student routers,
resume/handoff/current task/state/Q&A/inbox, actual clean radxa/q8b HEAD
9ada248e6ba7160723623fb62ba07e1d6aa67d63 and project/Chimera rules. Upstream
checks held, no related pending commit in inbox; no fetch/update/integration.

T05b implemented in existing native pandad module: separate LegacyF4Health type,
pure profile-gated exact59-byte decoder and one-call D2 reader. Eight canonical
boolean bytes become bool; full32-bit voltage/current and float load stay intact.
Legacy wake/fan-stall/SOM-reset preserved. Unknown enums/mode/alternative numbers
stay raw; current-only fields absent. No packed-current cast or narrowing. Load
finite/nonnegative; above1 preserved, not clamped. Null/wrong lengths/profile,
malformed fields and unhealthy IO return nullopt. Reader uses64-byte buffer and
1000ms timeout; no retries/cache/OUT/bulk/reset. Caller must pin/identify first,
serialize lifetime/ownership; transport exceptions propagate.

Changed panda_health.h/.cc, native test, SConscript and binary ignore; copied exact
health.h and MIT license into chimera/reference/carrot-f4-health-v17 with Git blob/
SHA256 provenance, source only for tests. Added field/error contract and updated
README/progress/compatibility/roadmap. No project runtime depends on outside files.

Source: Carrot69a2d3be header health17/59 plus actual producer get_health_pkt and
Python format/mapping in frozen source. Current Panda8a16e089 health49/native
identifier/consumer checked; no mapping of legacy modes to current policy.

TDD: strict standalone compile first fails for absent panda_health.h. Native
ASan/UBSan then passes all27field/golden/source checks,256flag combinations aligned
and unaligned,2032invalid boolean cases, integer/float bounds and single-read
failure/no-cache/ownership guards. Removing the profile check in a temporary
mutation compiles but fails the wrong-profile fixture; original restored before
final validation. Strengthened one optional assertion to check presence before
access. Actual SCons native pandad/six test executable builds pass; all6execute
successfully (USB tests are fake or pre-init pin guards, no real USB calls).
Existing Python Chimera receiver/protocol15tests pass in0.069s. GNU file confirms
aarch64 pandad; nm confirms decoder/reader in native fixture. No daemon run.

Direct generic Ruff on SConscript cannot see SCons injected names: baseline11and
current12F821occurrences have identical name set. AST parse/actual SCons succeed;
no ignores or rule/config weakening. This is recorded as a tooling limit, not a
Ruff pass. Existing PWD build warning is retained. No blocking code-review finding.

Ocelot39dirty entries and19source hashes preserved; original archive clean and
canonical DBC unchanged. All23firmware source hashes and retained7448-byte raw
image match prior receipt; no ARM rebuild or28-test firmware rerun needed for this
host-only change. No hardware/device/flash/reset/config/CAN/relay/actuation/install/
upstream update/push. Power/VBUS/current recovery and inherited watchdog open.

T05b decode/read complete offline, full T05 partial. Next T05c per-bus CAN-health5
contract/decode before T08 managed selection/publication/reconnect and exact-read
hardening. Existing current get_state/get_can_state accept non-exact replies;
these functions and managed selection remain untouched. New Chimera operational
health and controller/bulk binding are separate board work. No driving claim.

Skills used: incremental implementation, TDD, API/interface, source-driven, Git
workflow and code review. Teacher-first source/CLI/GNU artifact routing; no new
REA provider or network result. OpenAI Codex, no other agents/model inference.
Q&A23 synchronized, unanswered history preserved.

[Receipt](../Evidence/chimera-legacy-health-20261106.json) contains full commands,
source/artifact hashes, native/Python outputs and limits.
[Contract](../../chimera/docs/LEGACY_F4_HEALTH.md).

Closeout: memory verifier passes143documents/474relative links;138active Chimera
links resolve.12source/3artifact hashes match; whitespace check passes. Scoped
local commit, validation journal and coordinating index follow. No push.
