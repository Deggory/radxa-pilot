# Chimera classical CAN codec — November 6, 2026

Owner “procceedd”, context QA15→QA16. Accepted T04 pure modern classical CAN
framing/stream slice under chimera/firmware/, before USB/CAN hardware binding.
Baselinef65ab3639119f9a3e006aa76547d531310e56552 cleanradxa/q8b. Teacher/student
routers/resume/inbox/Q&A and saved deep review/source contracts read first.
Panda8a16e089/opendbc150f9371; source can.h, can_comms.h, can_common.h, Panda Python
pure pack/unpack and native panda.cc inspected. Ocelotd87892fa dirty39/19pinned
hashes and workspace archive224cfa6clean preserved. Exact working-file hashes in
[the receipt](../Evidence/chimera-can-codec-20261106.json).

Original MIT can_codec.c/.h: explicit byte encoding,6-byte header/XOR, data0..8,
bus0..2, standard/extended IDs, distinct received/returned/rejected metadata.
Strict host-TX decode rejects FD, DLC9..15, bus3..7, host metadata flags, bad standard
IDs/checksums/sizes before destination writes. Unused decoded payload bytes zero.
Per-connection16-byte state buffers at most14bytes; one frame per feed, explicit
consumed count/backpressure, partial chunks retained, detected errors latch with
no sliding resync until local init. No heap/register/queue/TX-policy call.
All four API entries retained in ARM image; no call from parked main. Board,
startup, protocol source and bootstrap manifest remain unchanged: phase0, no
operational capability/hash advertisement. Canonical DBC unchanged/uninterpreted.

TDD RED: absent codec source/header compilation failure. Native fixture then
passed but first ARM build exposed compiler-generated memset from aggregate zero
initialization. Replaced with validated explicit member/data writes; no shim,
dependency addition, weakened undefined-symbol check or skipped test. Existing
ARM bounds/artifact checks guard the regression. Source-first/TDD/interface/
incremental/security/debugging/Git/review skills used. No unrelated REA provider
analysis; direct ARM GNU artifact tools supply required link/symbol evidence.

Final14tests pass, source/test hashes and actual output in receipt. ASan/UBSan:
648RX vectors match actual packed current header and source Python decoder;
189TX vectors match source Python packing.216host-TX vectors cover every split
and2160-byte concatenation at every chunk size1..2160:4536scenarios.17280fixed-size
single-bit corruptions rejected;65536first-two-header-byte cases;10000deterministic
random streams; bounds/null/canaries/state/flags/ID/reset/error checks. Two explicit
XOR collision tests demonstrate limits, including a length change yielding a
valid shorter stream prefix. No universal corruption/authentication claim. Valid
frames before a later error are not rolled back; every eventual TX still needs
independent MCU policy and message integrity/freshness checks. Existing458920
control-query cases, GPIO/vectors/ELF/stack/overflow/MSP and copied-tree checks pass.

GCC13.2.1/binutils2.42, hostGCC13.3.0; Ruff passes. Raw1840bytes, projected legacy
envelope1976/114688budget; globals8bytes/stack4096unchanged. SHA256
fce676dcf4822bc5df576d775ce18c59b8d2203cf3ccf8417bb98c0fd9a3ed65.
[Codec contract](../../chimera/docs/CAN_CODEC_CONTRACT.md) records API and tested
limits. Main/startup/board/protocol sources hash-identical to QA15. Native test
includes actual current header, and only pure Python AST functions/constants are
evaluated; no Panda constructor/import/USB initialization. Firmware build remains
standalone; native interoperability tests require project Panda/opendbc source.

T04 complete offline. Next T03b USB clock/controller/EP0 implementation and offline
fixtures, then operational status/capabilities and endpoint binding. HostT05legacy
health/T08managed use, MCU TX policy, input qualification, Core Config, watchdog/
recovery/electrical evidence remain open. No hardware/USB/CAN/daemon run, flash,
config/DBC write, actuation, installation, upstream update or push. Updates still
held atNovember4. Both memory layers/Q&A/roadmap updated; ignored build artifacts
remain local unsigned outputs. Project changes saved in this local increment.
