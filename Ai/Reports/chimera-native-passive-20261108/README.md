# Native original-Chimera passive acceptance — November 8, 2026

Implemented existing pandad session admission for the pinned original Chimera
profile, with native mailbox16/health43 decoding, CAN publication and distinctly
labelled raw diagnostics. [Host contract](../../../docs/CHIMERA_OLD_USB.md).

Actual precommit validation passes: native target and11native programs;
45Python regressions;432mailbox/5health native/Python vectors; codec and changed
USB/session/parser units under ASan/UBSan with halt-on-error; two copied-source
mutations caught by failing assertions; Ruff, notebook/QA/whitespace and source
preservation. All76old firmware files and canonical DBC bytes are unchanged.
[Portable source/result receipt](../../Evidence/chimera-native-passive-20261108.json).
[Independent review](REVIEW.md) has no blocking findings and pins reviewed code.

The [acceptance/threat contract](CONTRACT.md) and [TDD red evidence](TDD_RED.json)
retain scope and baseline failure. The first native build attempt lacked venv
capnpc in PATH; the sanitizer harness then needed the existing generated/header
include roots used by SConstruct. These were harness setup issues, corrected
without weakening checks or changing source behavior. Initial raw logs are in
local ignored run/; final commands/outputs also travel in the portable receipt.

The coordinating teacher's Ai/Reports/chimera-native-passive-20261108/GATES.md
is the single active Unlazy ledger. Execute it from the workspace with explicit
root and project CWD, after inspecting verify.py and commands. Runtime verification
outputs go to ignored run/ so clean-commit checks remain meaningful. Re-execution
is available with this report's verify.py native/python/sanitizers/preservation;
closeout additionally checks review pins, actual results and a clean committed tree.

No actual USB session, CAN TX, relay/config command, reset, flash, new firmware,
vehicle/control admission, update or push. New Chimera rewrite remains halted.
The raw interface is observation-only and distinct from normal pandaStates. Pins
are selection constraints, not installed-image authentication. No mailbox record
checksum, ECU timestamp/freshness or physical bus/sensor correctness is inferred.
Next: separately qualify a matching installed board for receive-only bench use;
no automatic hardware or active-control operation is authorized by this report.
