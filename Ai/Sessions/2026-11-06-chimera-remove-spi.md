## November6 — Pandad SPI removed; metadata increment in progress

QA31: owner corrected generic-SPI retention. Removed pandad SPI source/class/build/
listing and both generic entries; all platforms require pinned USB. Current Panda
constructor qualifies USB and performs no reset/config.10native/42Python checks
plus strict fake-USB sanitizers pass. ASan reproduced/fixed short-header heap read;
exact tests/output in receipt. Metadata test is RED/uncommitted; continue next.
No hardware/update/push; firmware23hashes preserved. Earlier SPI-retention notes
are superseded. [Session](Sessions/2026-11-06-chimera-remove-spi.md).

Scope/test/source pins and deleted-file hashes are in the receipt. Skills:
migration/incremental/TDD/API/review/Git/docs, source-first fast path. No delegated
or REA provider result. Existing legacy statistics named spi remain wire facts.
No models/camera/Thneed/DBC/board runtime changed. Metadata/consumer work continues
as the second authorized increment; pending uncommitted test_panda_state_availability.py
is intentionally RED. Actual current firmware pin/readiness and hardware remain
unqualified. No source update/fetch/push. Commit this increment then continue.

[Receipt](../Evidence/chimera-remove-spi-20261106.json).
