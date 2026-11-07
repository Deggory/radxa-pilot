## November7 — New firmware selected; main startup increment verified

QA07/T03c1: owner chose new Chimera path and main.c first. ARM reset now binds
ordered read callbacks after quiet RAM/IRQ/clock setup and calls actual checked
boot preparation. Captures stable UID/raw reset/options in local diagnostics,
revokes validity on failures and ends USB_HELD5; fault handler clears validity.
USB service/attachment, DWT timing, CAN/input sampling remain unstarted; power/
VBUS/current recovery unqualified.30firmware tests incl native actual preparation
ASan/UBSan65536snapshots and ARM call proof pass; clock-guard mutation fails.
Freestanding memset link issue corrected by passing only fully bound callbacks,
no libc shim/suppression. Newraw7592bytes/globals32/SHA
fbce0bfa171b2bedca369d9913f6e3b661cadfa8ccf8a69063e0b9935b1020d1; unflashed.
Baseline7448-byte image preserved ignored, historical receipts unchanged. Four old
firmware files intentionally changed;19old sources plus Ocelot39dirty entries/
19hashes, archive/DBC/Panda/opendbc and host/camera/model/Thneed preserved.
Next main work: qualified USB startup profile and recovery/fault handling before
service initialization/attachment. Host T08b2d queued behind owner priority.
C2-era host-only option remains preserved/unselected. No hardware/update/push.

Scope: one main-first increment, no hardware operation. Baseline03b89175b40483f3cce7bac6d2292e7dac9f5ed5,
cleanradxa/q8b before edits. Added portable checked preparation to actual main.c,
newmain.h local diagnostic API; callback-only MMIO binder; retained old timing
initializer semantics; build manifest newheader; native and ARM startup tests.
Main still initializes RAM/IRQ/quiet outputs and HSI as before, then captures
read-only identity/reset/options and parks with explicit result. Clock failure
performs no snapshot reads. Blank/allFF/unstable UID rejects and clears validity;
raw old bytes can remain for diagnosis only. Fault path also clears validity.
No profile or operational capability granted; existing phase0 manifest unchanged.

Native tests compile the actual preparation function from main.c under a test
macro that excludes ARM reset/asm. Real ARM build/disassembly separately verifies
reset/main call order and no service invocation; it is not an emulated/live MCU
reset test. Exact output and recipes retained. Full30firmware suite includes new
ASan/UBSan65536snapshot fixture, old codec/control/register fault tests, copied-tree
determinism, ARM vectors/call graph and negative image/linker bounds. Clock-guard
mutation is detected. Host suites/nativepandad are unchanged/not rerun this slice.

Build initially lowered aggregate IO zero-init to missing freestandingmemset;
removed unnecessary aggregate init and pass NULL unless binding succeeded.
No dummy libc, warning suppression, assertions removed or source contract relaxed.
BuildGCC13.2.1/binutils2.42, newunsigned7592bytes/projected7728/globals32/stack4096,
24source/header hashes; old7448-byte image/ELF/report preserved under ignored
chimera/build/main-startup-20261107/baseline. Raw old source changed onlymain.c,
usb_mmio.c,usb_time.h,build.py;19prior files unchanged. Newmain.h added.

Source pins: Panda8a16e089b88593914823743df29e1c30b7dd3e00,
opendbc150f937198ceab43c43b39f94b9bdea63fcb633c clean;
Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 preserved39dirty entries/19hashes;
archive224cfa645134db91103c55d8188d87e7976b0ba4 clean. CanonicalDBC SHA
b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67 unchanged.
Host/camera/model/Thneed/retropilot source untouched. No device access/flash/reset/
config/relay/CAN TX/daemon/install/upstream update/push. Raw read access assumes
valid F413 target and cannot return a bus fault; exception path remains held.
Watchdog and electrical/recovery facts remain unknown as in the existing contract.

Workflow: incremental/TDD/API/source-first/Git/review/docs, selected readable
sources and GNU ARM artifact views; no REA provider/delegation. Review of validity
ordering, clock-gated failure, no new peripheral writes, argument/lifetime scope,
freestanding symbols, limits and no USB activation. Source interface contracts
explicitly serialized/non-aliasing; diagnostic snapshot is not concurrent USB ABI.

At preparation, this increment's code/tests/docs/notes are uncommitted; scope
committed together after final notebook/link/hash/whitespace checks. Next main
slice is qualified USB startup profile and recovery/fault handling before actual
service initialization or attachment; resolve physical gates before connected
profile. Host T08b2d remains queued behind owner priority. No percentage increase
or physical readiness inferred from new lines/tests.

[Contract](../../chimera/docs/MAIN_STARTUP.md).
[Receipt](../Evidence/chimera-main-startup-20261107.json).
