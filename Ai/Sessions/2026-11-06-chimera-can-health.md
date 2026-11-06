# November 6 — Legacy F4 per-controller CAN-health5

Owner “proceed” continues T05c after QA25; USB-only/no SPI probe/fallback retained.
Read teacher router/resume/inbox/Q&A and student router/handoff/state/tasks/topic,
actual clean radxa/q8b HEAD288479ccaad916286376fac6fc86ad7dd6c69e85 and task-relevant
skills/rules before work. Upstream held; no pending related commit, no fetch/check.

Added LegacyF4CanHealth (26wire fields plus requested selector), exact64-byte
profile/selector/flags/LEC decoder and one bounded C2 reader in panda_health.h/.cc.
Selector u16 validated0..2 before narrowing/IO; request C2/value=selector/index0/
length64/timeout1000ms. No retries/cache/writes/reset or SPI path. Unhealthy/failed/
non-exact/malformed results nullopt, exceptions propagate; caller owns serialized
qualified transport. No managed caller/publication or new MCU producer added.

New native test target and ignored binary, reused unchanged Carrot header/license.
All26fields' offsets/types/size also match current header at pins; no profile or
main-health/version/policy equivalence. All unsigned widths retained. F4 CMSIS
REC mask8bits/producer shift means128..255 allowed despite H7-derived comment.
FD configuration/DLEC fields remain reports, not evidence of actual F4 FD support.
C2 reply has no selector echo: caller tag not wiring proof; no physical role remap.

Actual legacy C2 calls update_can_health_pkt(selector,0), which increments
bus_off_cnt by bus_off on every invocation, including polls. This is not a distinct
transition count. Stored errors/register/IRQ samples also update. No derived
rate/clear behavior introduced. Source behavior explicitly documented.

TDD absent type/declarations RED recorded; strict native ASan/UBSan GREEN. Tests
compare independent golden bytes/all26fields with original header,3x64boolean
combinations aligned/unaligned,1524invalid booleans,1024LEC cases,65533invalid
selectors,5u32boundary sets, wrong lengths/null/profiles and bounded reader errors/
disconnect/unhealthy/corrupt/no-cache/no-write cases. Temporary removed reader
selector bound compiles but triggers fake transport invalid-IO assertion; restored
before final compilation. Oversized malformed tests use an adequately sized buffer.
Native pandad and all7host executables build/pass; strict sanitized new CAN-health
and existing health59 fixtures pass. SCons AST and whitespace checks pass. Generic
SCons Ruff context limitation is known, not rerun or suppressed. No Python/firmware
suite rerun because unchanged; prior15Python/28firmware results remain historical.
GNU nm confirms new decoder/reader in actual native fixture; no daemon executed.

Carrot69a2d3be header/main_comms/bxcan/Python mapping and current Panda8a16e089
header are primary sources; F413 vendor header REC mask inspected. Exact source/
test/artifact pins and actual outputs in receipt. Source/CLI/GNU artifact route,
no new REA provider/network. Skills: incremental implementation, TDD, API/interface,
code review and Git. OpenAI Codex, no additional agents/model inference.

Ocelot39dirty entries/19hashes and original archive preserved; canonical DBC same.
Firmware23source hashes and retained7448-byte image SHA
 d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698 unchanged.
No board/device/flash/reset/config/CAN/relay/actuation/install/update/push. Power/
VBUS/current recovery/inherited watchdog unqualified. Main remains parked;
inherited native SPI constructor awaits USB-only integration.

T05c complete offline, T05 overall partial (new Chimera operational health absent).
Next T08a: USB-only pinned session/startup ownership and failure lifecycle with
no SPI probe/fallback. Publication/exact-read hardening/reconnect and physical
qualifications remain. Q&A26 synchronized, unanswered entries preserved.

[Receipt](../Evidence/chimera-can-health-20261106.json)
[Contract](../../chimera/docs/LEGACY_F4_CAN_HEALTH.md)

Closeout checks: memory146documents/502relative links pass;146active Chimera
links resolve,8source/4artifact hashes match, diff whitespace passes. Verified
local commit, maintenance validation and coordinating index follow; no push.
