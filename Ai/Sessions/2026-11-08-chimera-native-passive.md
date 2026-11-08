# November 8, 2026 — Native original-Chimera passive pandad

Accepted owner scope: modify pandad to accept retained chimera_old. Implemented
one complete host receive/diagnostic path, using the existing guarded USB owner
and exact identity pins. Separate bounded mailbox16 and raw health43 codecs,
profile-stable session/sample dispatch, typed diagnostics and native main wiring
are implemented. No new current/bootstrap admission, TX/pandaStates/control,
config/reset/heartbeat/flash command, firmware change or physical run.

Baseline249726e133e6e83241faae4699cca6eecb6a9c32 onradxa/q8b, initially clean.
Panda8a16e089/opendbc150f9371 remain pinned. Native protocol source is preserved
chimera_old (Ocelotd87892fa plus saved modifications), not a verified exact match
to historical de193215 installed firmware. The specific guarded identity remains
v1.0.0-DEV-de193215-DEBUG with exact serial, product/VID/PID and health43.

Changed paths: pandad native codec/session/publisher/main/SConscript, new/native
and Python interoperability tests, exact generated-test ignore, host contract and
relevant Ai topics/state/worklog/Q&A. Original source, DBC, camera/Thneed/model,
Panda/opendbc submodules and halted new Chimera firmware are preserved.

Skills actually applied: incremental-implementation, test-driven-development,
api-and-interface-design, security-and-hardening, source-driven/source-first
investigation, code-review-and-quality with its independent reviewer pattern,
Unlazy solo gates, documentation-and-adrs and git-workflow-and-versioning.
Existing Understand Anything teacher graph/notes routed the relevant evidence;
actual source was followed rather than rebuilding a whole graph. REA is not
applicable to this readable-source change; no binary/runtime result fabricated.

TDD: missing codec header initially fails compile; the new acceptance test run
against the original session fails with F4-only rejection. Initial build lacked
venv capnpc in PATH; corrected to project venv. Separate serializer/session tests
and the native target then pass. All432mailbox/5health native/Python vectors match.
Independent production review found no remaining blocking issues and independently
passed codec ASan/UBSan. Final full tests/gates/sanitizer results are saved in the
report and receipt; no offline success is a physical acceptance claim.

Important limits: no mailbox record checksum or ECU freshness proof; host receive
time only. Native rejects bus3 and non-returned TXRQ, deliberately stricter than
Python. Raw safety17/power zeros are not qualified modern status. Old relay still
follows ignition in source. D2 can delay polling; no throughput/whole-loop deadline.
No in-session autoreconnect; a fresh explicit reopen reidentifies and clears
fragments. Existing external supervision may restart the process.

Upstream inbox still stale at November4; saved hold discussed and retained. No
update/integration/push. At closeout save exact test counts, source hashes, gate
results, local commit and clean readback. Next: use saved evidence to plan a
separately qualified matching-board receive-only check; no automatic hardware,
firmware rewrite, active-control or managed status work from this notebook.

## Actual validation before commit

Native target and11native programs pass;45Python regressions pass with no skips.
432mailbox and5health native/Python vectors match. ASan/UBSan with halt-on-error
pass for codec and changed USB/session/parser units with fake IO; both copied
source mutations fail their assertions as intended. The sanitizer standalone
compile initially lacked generated/msgq/opendbc include roots; aligned it with
SConstruct and reran successfully. No product workaround or suppression added.
Ruff and notebook/QA/whitespace checks pass.76old files and canonical DBC match;
independent production source review has no Critical/Required findings. Portable
source/result receipt: Ai/Evidence/chimera-native-passive-20261108.json.

Final Unlazy gate execution and clean commit readback follow this verified source
checkpoint, with the actual active ledger and final receipt in teacher Ai.

## Completed code checkpoint

Committed 008a7e81a8aad2d3c91f31de5463953f56d587bb locally onradxa/q8b, clean, no push.
All five Unlazy gates were executed after that code commit and passed:
5met,0unmet,0abandoned.11native programs/45Python tests,432mailbox/5health
parity vectors, ASan/UBSan and two caught mutations pass. All14source/result
receipt hashes match current files;76original files and canonical DBC preserved.
The portable FINAL_READBACK.json records the actual code checkpoint and native
artifact hash. No real board/session qualification is implied.

This documentation-only closeout saves the measured final result. The next
step and remaining hardware/managed/control limits above remain in force.

## Capability follow-up (QA26)

Owner asked "can u tell wat it can do". Explained passive USB/CAN reception,
three preserved bus numbers, internal CAN publication and labelled raw health.
Actual vehicle signals require producers and matching parser/DBC configuration.
No driving transmission, normal engagement, firmware programming or new safety
policy is provided. Physical-board qualification remains pending and autonomous
legacy relay behavior remains unchanged. Source008a7e81/docs baseline0d8c8cfe;
implemented contract reread, prior validation reused. Documentation and Git
skills applied to synchronized closeout; no new code/runtime/hardware action.
Follow-up validation: notebook verifier, QA26 equality and git diff --check;
actual result/commit recorded in the central follow-up receipt.

## C2-era Chimera compatibility and file-map follow-up (QA27)

Clarified that original-protocol support is implemented for matched-profile
receive-only use, while actual board/vehicle compatibility and full engagement
remain unqualified. Read the actual 008a7e81 A/M list and current codec/session/
publication/main/build/test source at baseline dd5ac056. Documented two new
runtime files, six modified runtime/build files, two new tests and two extended
tests; existing USB/identity source reused unchanged. Added the practical file
map to docs/CHIMERA_OLD_USB.md. Documentation/Git skills guide this closeout;
no current project Understand Anything graph was available, so no graph-derived
claim or refresh was needed for the focused source answer. No new runtime test,
REA artifact task, hardware action, update or push; original firmware and DBC
untouched, rewrite/update holds retained. Actual notebook/QA/whitespace checks,
commit and clean readback are in the central FILE_MAP_FOLLOWUP.json receipt.

## Safety-boundary follow-up (QA28)

Owner asked how safety is handled. Read current USB allowlist/write blocks,
codec bounds, passive main/session/publications and saved old firmware DC,
heartbeat, relay loop and can_send. Checked local noOutput/dashcamOnly interface
and unqualified active-profile initializer; reused QA01/02 evidence. Reopened
https://docs.comma.ai/concepts/safety/ for override/bounded-actuation principles.
Security-and-hardening used narrowly for external-input/write boundaries;
documentation/Git skills guide closeout. Explained protection of the host RX
path versus missing MCU driving-safety enforcement and unqualified electrical
cutoff. No changes to code, firmware, DBC or submodules; no tests rerun beyond
notebook/QA/whitespace/source preservation checks. No REA runtime/binary task,
hardware, update or push. Next step/holds unchanged. Actual source hashes,
validation, commit and clean readback: central SAFETY_FOLLOWUP.json receipt.
