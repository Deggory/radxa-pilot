# November 6 — USB-only Radxa status startup/session

Owner “proceed” continues T08a from QA26. Read teacher/student routers, resume/
handoff/state/tasks/Q&A/inbox, actual clean radxa/q8b HEAD86678975460572b26a03af3354cb0fcc0f7f24c6,
wrapper/native startup/backend/identity/health sources and relevant skills. Updates
held, no related pending commits; no updater check/fetch. Existing wrapper resets/
recovers/DFU/flashes before native startup; that path must be bypassed for Radxa.

Implemented pure usb_startup.py, PandaUsbStatusSession h/cc and native --usb-status
mode. Wrapper requires explicit serial/version pins on Q8B (or if either USB env
key present elsewhere), execv before any legacy probe/reset/flash path, no shell/
defaults/environment writes. Missing pins/exec failures stop, no fallthrough. Native
Q8B bare/legacy entry exits2 before SPI; compiled main.o has no legacy-thread ref.
Generic other-platform legacy entry retained. No manager/config/pins installed.

Session owns actual pinned USB backend, exposes only status/close/active, legacy
F4v17 typed initial health required. Current/original/new Chimera remain rejected.
D2 plus3C2 sequential samples returned only when complete; failed/malformed/short/
unhealthy or exception closes immediately. No cache/retry/implicit reopen/TX.
Reopen explicit/full identification. Native loop logs, waits1s, signal/error closes.
No CAN/pandaStates/Params publication or sendcan/safety/heartbeat/output threads.
Active is ownership, not readiness; no atomic snapshot/freshness/whole-startup
latency guarantee. Manager may relaunch; no new backoff policy. Legacy C2 polling
changes stats. Compatible reviewed version pins required: old IN command collisions
(DD forwarding) are saved evidence; version matching is not authentication.

TDD RED for absent Python helper/native session header. GREEN21Python tests (6new
startup plus15existing Chimera), native pandad/seven executables, strict ASan/UBSan
real factory/session with fake libusb and no SPI translation unit linked. Failure
matrix covers all4read positions, malformed initial/subsequent values, disconnect/
exceptions, immediate release/no stale cache and explicit reopen. Five invalid
native CLI invocations exit2 before device IO; no valid USB invocation/monitor run.
Mutation removing immediate close on D2 failure compiles but fails active/cleanup
assertion; restored. Initial new-test enum/int initializer-list compilation defect
fixed with explicit initializer_list<int>; original log retained, no suppression.
Ruff changed Python, SCons AST/actual build and whitespace checks pass. Source/CLI/
GNU artifacts, no new REA provider/network/fresh-context review. OpenAI Codex,
no additional agents/model inference. Relevant implementation/API/TDD/debugging/
review/Git/documentation skills applied; other considered skills not invoked.

Firmware23source hashes and retained7448-byte raw image unchanged; no ARM/firmware
suite rerun. Ocelot39dirty entries/19hashes, archive and canonical DBC preserved.
No board/flash/reset/config/CAN/relay/actuation/install/upstream update/push. Physical
power/VBUS/current recovery/watchdog still unqualified. New image remains parked.
Earlier Radxa-entry-still-SPI answers now superseded by QA27; generic constructor
still SPI, but Q8B launcher/native route bypasses it. Full T08 remains partial.

Next T08b: passive CAN reception and profile-aware publication with explicit
validity/freshness/exact-read/reconnect; other-profile admission and MCU policy
separate. Q&A27 synchronized, prior unanswered history retained.

[Receipt](../Evidence/chimera-usb-startup-20261106.json)
[Contract](../../chimera/docs/USB_ONLY_STARTUP.md)

Closeout: memory147documents/511relative links pass;162active Chimera links
resolve;11source/4artifact hashes match. Ruff and whitespace pass. Verified local
commit/maintenance validation/index follow. No push.
