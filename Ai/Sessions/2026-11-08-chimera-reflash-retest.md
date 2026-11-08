## November 8 — Owner reflash retest: same application, still zero CAN (QA66)

Exact original Chimera detected USB003/024; same version/full nightly signature
and same valid saved776-byte config. Raw4s/2047reads before and12s/6134reads
after one guarded DE/bus2/index5000request both0bytes. Native15.114s/1420batches/
15health0frames on all buses, exit0; readers closed. Runtime500krequest completed,
not BTR proof; flash unchanged. No flash/reset/dataTX/product/upstream action.
Owner confirms sensor powered from separate12V/onCAN2/common ground for retest;
previous numeric voltages are not fresh post-reflash measurements.
Resistance never supplied (k=ack); physical checks held by owner’s code-only
instruction; later reflash retest authorized this run. See new reflash report.
QA65partial code review found can_init alwaysfalse return, also in matching
image; calls still execute, so not a proven zero-RX cause. No code fix/flash.
Next code-side controller/filter/error-observability review; no new hardware
measurement request. Existing implementation/upstream holds retained.

# Chimera retest after owner reflash — 2026-11-08

The original Chimera enumerates and answers USB health/version/signature, but
CAN reception remains zero before and after one temporary CAN2 500 kbit/s
request. Native pandad likewise publishes no received frames. This is a failed
CAN reception test, not a demonstrated hardware failure or repair.

## Identity and firmware

- Original serial3a0044001651333038373636, productChimera, bbaa:ddcc, USB003/024.
  The separate Interceptor DAC Bench003/018 was not opened.
- Versionv1.0.0-DEV-de193215-DEBUG; health43bytes; full128-byte application
  signature matches previous signed nightly. Signature SHA256
  e9a44094a2440fd3621b45fe9d30b505b3abeab29e340e42bf38542620255e5b.
- Matching signed image SHA256e35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b.
  This fingerprints the signed application, not whole-flash readback or flashing
  tool provenance. Owner performed the reflash; agent sent no flash/reset.
- Saved776-byte config is valid and identical to before reflash: SHA256
  4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22.
  Debug3, output0x0F, watchdogoff, saved500/500/0/0kbit/s. The UI decoder’s
  speed fields are100bit/s units; matching image uses250kdefault for saved0.
  Thus reflashing this application/config does not remove the CAN2boot-rate lead.

## Actual test

Raw bulk-IN0x81 lengths recorded before mailbox decoding across all buses:

| Stage | Duration | Reads | Bytes | Bus0/1/2 records |
| --- | --- | --- | --- | --- |
| Before request | 4.000564313s | 2047 | 0 | 0/0/0 |
| After request | 12.000882619s | 6134 | 0 | 0/0/0 |

After identity/version/signature qualification, exactly one vendor OUT0x40/
DE/wValue2/wIndex5000 completed; this requests printedCAN2/MCUCAN3/USBbus2
at500kbit/s. No data payload. USB completion is not active BTR/init-result
readback. Last requested500kleft running, not restored/rebooted. Before/after
flash byte-identical.8+24health packets; uptime86..101during raw captures.

Native15.113864017s:1420CAN batches,0frames all0/1/2,15health diagnostics,
chimeraOldMailbox16profile, exit0. Empty batches are not CAN frames. Reader
stopped and USB released. No CAN dataTX/heartbeat/relay/Save/Format/reset/flash,
port move or upstream update. Native executable/DBC and all76preserved firmware
manifest entries checked; other repositories’ existing dirty work preserved.

## Limits and next step

During this retest the owner explicitly confirmed “Yes, powered and on CAN2”
to the question specifying separate 12 V supply and common ground. This confirms
the stated powered sensor/CAN2 setup; it is not a fresh voltage, waveform or
sensor-transmission measurement. CAN2_TERM jumper fitted is owner-reported;
no resistance reading was supplied. “k” was acknowledgement only. Owner then
requested code-only work; physical measurement work is held, and the later
explicit reflash retest authorized this bounded run.

No further flash or guessed software change is justified by zero USB bytes.
Sensor power/CAN2 setup is owner-confirmed; reception remains zero. Continue
code-side controller/filter/error-observability review within the retained
implementation hold; host parsing/DBC cannot drop bytes USB never returned.

## Interrupted code-only review (QA65)

Before the reflash request, source and existing matching-image disassembly were
read only. Active application includes chimera/can.h, not power_saving.h;
no ignition gate for raw RX found. One additional concrete bug: can_init starts
ret=false then uses &=, so it always returnsfalse even though both init functions
execute. Matching image0x08007960calls speed/init/process, then0x08007982setsr0=0.
This corrupts status reporting, not proof of initialization suppression or the
zero-RX cause. Existing generic CAN filter lead is still unproven for CAN3:
bank14out-of-range is suspect, but validbank0is also enabled. No source edits,
fix/build, complete new audit or flashed correction occurred in that review.

## Verification scope

Three gates check captured evidence, native observation and preservation/handoff.
They do not require nonzero frames or certify a working CAN link. Existing
protocol unit-test results are historical and were not needlessly rerun; no
product code changed. Focused debugging/Unlazy/source/explanation skills used;
saved REA/objdump evidence reused. No new REA provider result or graph coverage
claimed. Baseline03dfd0c7fc7017e3fb0060d34a8e706f5009c558 onradxa/q8b, initially
clean. Upstream inbox remains November4stale under explicit hold; no check/update.
