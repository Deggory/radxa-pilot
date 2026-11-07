# November7,2026 — Explicit legacy session mode

Accepted scope: "proceed" from cleanb3ff3d26e4d71e9d7b68dd6a7b3a94310b5cfe7e on
radxa/q8b. Read teacher/student routers, resume/handoff/Q&A, power evidence and
update inbox; Ocelot applicability already supplied by owner, no repeated question.
Upstream remains held under November4 policy. No Page context/action relevant.

T03c3b implemented in existing core/service/coordinator boundaries: local validated
mode enum UNFORCED0/LEGACY_NO_VBUS1; mode variants plus old unforced wrappers.
Main validates/copies selection, rejects mixed-reader/invalid/mismatched mode and
keeps physical VBUS UNKNOWN in explicit no-sense mode. Core programs only B-session
overrides after SDIS, VBDENoff, checks readback. Service verifies exact mode and
PHY/detector settings before/after poll. Existing reset path cancels EP0 session
state. Driver now treats OTG-summary as unsupported fault with existing wrong-role/
suspend path. Accessible core/service failure cleanup clears overrides; reset/gate
readback failure keeps ownership; explicit stop succeeds/reset mode only when
cleanup is confirmed. No implicit retry or invented power measurement.

Actual main.c remains byte-identical with NULL profile/reader. No USB pin, power
profile, attach/IRQ/DMA/CAN/input/flash/watchdog/settings behavior enabled. USB A0/
D6/capabilities and D2/C2 STALL unchanged. Default wrappers remain unforced.
Important limit: original source acknowledges GOTGINT; this stage deliberately
faults any OTG summary, including potentially benign causes. Next cause decoding/
ACK and controlled attached lifecycle are required before live mode. No actual
cable-loss timing, normal resume, SOF/heartbeat freshness or physical readiness.

Tests written first: new fixture failed RED for missing types/APIs. Final34firmware
tests pass warnings-as-errors.61new native real-component scenarios run actual
main/service/clock/time/core/driver/EP0 under ASan/UBSan: both modes x20startup
outcomes, invalid-mode preflight, copied mode, reset cancellation, null-profile
non-reuse, mixed/live-mode rejection,12faults, stuck writes, failed cleanup/retry
and persistent-fault refault. Existing51coordinator/16power cases retain explicit
unforced config. Shared fake injections remain behind clock/access assertions and
all DCTL writes retain SDIS. Three temporary mutations (false PRESENT, missing
mode invariant, uncleared overrides) abort assertions. ARM call/symbol, deterministic
copied-tree, vector/ELF/linker checks pass. Ruff/notebook/source preservation saved
in Ai/Evidence/chimera-legacy-session-20261107.json.

First restart expectation failed because its fake suspend bit was still injected.
Final fixture asserts repeated failure, then clears the injected condition before
expecting healthy explicit restart. Reproduction saved separately; no production
logic/guards/assertions weakened. Self-review checked boundaries, copied/stable
state, mode validation/invariants, cleanup ownership, default wrappers, readback,
truthful status and no attachment. No delegated review claimed. Applied incremental,
TDD/API/Git/review/debug/docs/source-first skills. Source and GNU ARM tools suffice;
no REA provider result or unrelated binary/runtime analysis claimed.

Current image8316/projected8452/globals260/stack4096; no undefined symbols; SHA
745f66c5c408a8c046c6c7ed3f3c3edc576b9743b9a0b35d860770a1f24e8826.
25build inputs:7changed(main.h/main_runtime.c/usb_hw.c,h/usb_service.c,h/usb_driver.c),
18unchanged. Baseline8108image/ELF/report retained under ignored build/legacy-session-20261107.
Preserve Ocelot39dirty entries/19hashes, archive224cfa64clean, Panda8a16e089 and
opendbc150f9371clean, DBCb4079670 and frozen F4reference. Host/model/camera/Thneed,
relay/OBD-C/input/safety code untouched; existing host statsd issue remains open.

Stage100% offline; overall planning estimateabout25%/75% remaining; physical0%.
Keep reporting after each stage without inflating for tiny slices/tests/LOC. Next:
review OTG cause handling and controlled attached-state lifecycle offline, keeping
actual board main held. Actual electrical/profile/pin/recovery/bench qualification
and operational bulk/CAN/health/inputs/Core Config/MCU TX remain later stages;
hostT08b2d queued. No device/flash/config/TX/upstream update/push. Commit verified
increment locally; teacher final checkpoint records SHA/ledger/index/clean readback.
