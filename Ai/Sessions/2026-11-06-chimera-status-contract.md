# November 6 — Chimera bootstrap status/capability contract

Owner: “proceed”, after QA21. T05a accepted scope is exact status/capability
semantics and offline response fixtures before operational health advertisement.
Read coordinating/student current notes/Q&A, source-first/skills policies, real
branch/HEAD, pending update inbox and existing contracts. Branch radxa/q8b was
clean at e586191ac39e663727aac2cbd453937477350ef8. Upstream updates remain held.

Added pure openpilot/selfdrive/pandad/chimera_identity.py, firmware response C
fixture/Python tests, status contract and roadmap/progress links. It only decodes
the exact phase0 A0/D6 identity; all capabilities/hashes0, full response required,
reserved/topology/version fields strict. Five new tests cover actual C-handler
replies, unsupported request canaries, all single-byte alterations and malformed
length/type cases. No new wire ABI/measurement/ready flag; no runtime caller.
Native current health49 consumer reads ignition/safety and can issue commands;
unknown/unimplemented fields cannot silently become observed healthy zero.
Future operational host profile must explicitly handle unavailable/freshness.

Validation: all28tests pass in16.253s, including real GNU ARM build/symbol/vector/
linker-overflow/ELF/disassembly/determinism checks and native ASan/UBSan fixtures.
Ruff and diff whitespace checks pass. Source parser test initially encountered
system Python's missing capnp through package startup; runpy now loads the pure
module without runtime dependencies. Intended absent-implementation RED confirmed,
five focused tests GREEN. A temporary removed reserved-byte condition is detected
by the manifest mutation fixture and restored before the final suite. No test
suppression or added dependency. Firmware source hashes and raw image match
baseline:7448bytes,8global RAM bytes,4096stack reservation, SHA256
 d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698.

Current Panda8a16e089 health header, native consumer/identifier and bootstrap
protocol.c are exact source inputs. Ocelotd87892fa39dirty status entries and19
source hashes preserved; original Chimera archive clean. Canonical DBC unchanged.
Installed skills: incremental implementation, API/interface, TDD, Git workflow
and code review; source/CLI and GNU artifact path, no new REA provider result.
Agent OpenAI Codex; no additional agents/model inference. No board/device access,
flash/reset/config/CAN/relay/actuation/install/update/push. Main stays parked;
bootstrap still rejected by native identification and managed startup stays SPI.

T05a complete offline; T05 overall partial. Next T05b exact legacy F4health59
source-backed decoding/adaptation, before managed use. New Chimera operational
health, controller/bulk binding and MCU policy remain pending. Actual attachment
requires qualified power/VBUS/current-recovery and inherited-watchdog evidence.
Q&A22 synchronized; previous unanswered entries retained.

[Receipt](../Evidence/chimera-status-contract-20261106.json) contains exact hashes,
commands/output and limits. [Contract](../../chimera/docs/STATUS_CAPABILITY_CONTRACT.md).
Local verified commit/journal/index readback follows; no push authorized here.

Closeout validation: memory verifier passes142documents/465relative links,
124active Chimera Markdown links resolve, all8receipt source hashes match,
Ruff/diff checks pass. Reviewed API/input boundaries and mutation sensitivity;
no blocking finding. New decoder is deliberately not called by managed startup.
