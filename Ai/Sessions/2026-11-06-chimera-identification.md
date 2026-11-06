# Native Panda identification — November 6, 2026

Owner requested proceed reliably and use the teacher throughout. QA-20261106-10.
Accepted increment T02a: source-pinned read-only identification before USB
initialization; retain current/F4/Chimera distinctions. Teacher November5 deep
review, November6 Carrot report and firmware map followed into source handlers.
Baseline b76db53c3; Panda8a16e089/opendbc150f9371, Carrot69a2d3be and Ocelotd87892fa
plus preserved dirty bytes. Teacher's known absence of Chimera C1/DD determines
its separate branch. No new artifact/REA result needed for readable source.

Changes: native panda_identification.{h,cc}, focused test, pandad SConscript and
ignore; compatibility documentation/roadmap and both memory layers. API requires
exclusive transport ownership, matching descriptor/transport serial and explicit
version pin. Uses D6/C1/DD/D2 for Panda, D6/D2 only for original Chimera. Exact
numeric/hash versions, board families and health lengths; all reads finite1s,
no retries or writes. SCons derives current hashes from firmware source inputs.
Tests use independent pinned hash bytes. Unsupported combinations throw.

TDD red: missing API/header compile error. Native SCons green builds pandad and
all three test targets. Identification19accepted/421rejected/3invalid transports
and zero OUT/bulk operations; strict address/undefined-behavior sanitizers pass.
Native interface/CAN codec and15existing Chimera Python tests pass. Corrected
manually transcribed test hash bytes against the actual retained receipt before
green; no production relaxation. Existing PWD warning remains non-fatal.

API/code review: bound lengths before indexing, exact-version/no default fallback,
separate raw health, correct test failure types so unexpected I/O cannot masquerade
as expected protocol rejection. Caller-supplied descriptor identity remains a
factory responsibility; no cryptographic attestation is claimed.

Selector is compiled into native library, not invoked by startup yet. Generic
Panda constructor/updater side effects are unchanged; future protected USB
factory must invoke this helper before initialization. T02 full matrix/new
Chimera identity/source authority and T06 USB/status/lifecycle remain incomplete.
Next bounded USB adapter/factory. T01/T03 board/flash target remains separate.
No device/daemon/USB enumeration, flashing/config/CAN/relay, vendor update or push.
Validation receipt: Ai/Evidence/chimera-identification-20261106.json.

Review strengthened the original Chimera branch to the saved de193215 nightly
version; a caller-supplied arbitrary new version is not sufficient proof of
mailbox framing. Added rejection fixture; final count421. Sanitized rerun passes.
