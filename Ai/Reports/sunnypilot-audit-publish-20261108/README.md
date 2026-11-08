**Actual publication — November 8:** normal atomic push published the audited
Radxa source at3eb53c9a2 and official master at3d8f211d4. Independent GitHub
README blob and masterSHA match; default branch remains master. See
[publication receipt](publication.json). Owner explicitly clarified the GitHub
Radxa update target. The following closeout commit saves this receipt and is
published normally; source/tests are unchanged. Three gates met; CAN remains0.
The preparation-stage wording below is historical.

# Audit of Radxa Sunnypilot work — November 8, 2026

The live project is /home/radxa/comma/sunnypilot on radxa/q8b. Baseline
4ab2ab81fe7af8eb8731c7d16c9e9f343027c903 was clean. The previous GitHub Radxa
backup was dfd316d6554bbd39e221759c5637e648b8cd2cc3: 68 local commits and
276 changed paths (141 Ai, 79 preserved-legacy, 56 other paths). This is an
inventory of that interval, not a claim every copied vendor header was newly
reviewed. All76 retained baseline manifest entries are independently rehashed.

## Findings and corrections

1. **Physical CAN reception is still a blocker.** After the owner reflash the
   original USB serial/product/version and full128-byte signature matched the
   saved nightly. Raw4s/2047reads and12s/6134reads after one temporary500krequest
   both returned0bytes. Native15.114s/1420batches/15health had0frames all buses.
   Sensor powered12V/onCAN2/common-ground setup was owner-confirmed. These are
   earlier measured evidence reused, not a new device run during this audit.
2. **Public progress text was stale.** The README still led with November7
   firmware-bootstrap next steps. Corrected project and chimera READMEs and the
   original USB contract to show the halted rewrite, implemented native receive
   support and failed physical reception. Original implementation-only test
   descriptions remain historical, not overwritten as new measurements.
3. **Installed image and readable legacy source differ.** Saved rates500/500/0
   predict500/500/250k at boot in the matching nightly, while preserved source
   starts all3at500k. An acknowledged runtime500krequest is not live BTR readback
   and did not fix reception. No guessed permanent configuration repair applied.
4. **Known legacy status bug retained, not silently fixed.** can_init starts
   false and &=calls, so returnsfalse even when calls run; matching disassembly
   confirms0x08007960..7984. It is not proof of initialization suppression or the
   zero-RX cause. Generic filterbank0/14 handling remains an unproven lead.
5. **Copied-source whitespace is historical.** Full interval diff check reports
   original preserved firmware whitespace. All warnings are retained centrally;
   the interval excluding chimera_old passes. Do not normalize manifest-pinned
   source just to suppress these warnings. New audit edits pass diff --check.

## Code review and fresh verification

Reviewed the native host production diff and codec/session/publisher contract:
identity remains pinned; no write/control path was added; malformed/partial data
fails closed; memory bounds and health43 framing remain explicit. Diagnostic
values are raw/observation-only, not authenticated operational Panda state.
No protocol record checksum or ECU sample-time proof is invented. Existing
F4 behavior and explicit disconnected-state cleanup remain covered. The retained
independent November8review is prior evidence, not a new delegated review.

Reviewed the halted firmware runtime's detached/attach/session boundaries and
reused its documented offline scope; actual main remains held with NULL board
profile. Fresh host/MMIO/sanitizer tests run without devices. No rewrite resumed.
No project knowledge graph was available; actual source/diffs and retained
REA/objdump artifact evidence were used. No new REA result claimed.

- Native SCons target build,11native programs and2invalid-entry guards pass.
- 45host Python unittest cases pass, including432mailbox/5health parity vectors,
  startup, source/availability consumers and Thneed telemetry. Ruff passes.
- 36offline firmware tests pass using existing ARM toolchain; tests build in
  temporary directories, exercise actual ARM artifacts/fake MMIO/lifecycle and
  sanitizer checks, and perform no board flash/run.
- Instrumented codec/session tests pass;2copied-source negative controls fail
  the intended assertions as expected.8compile/run commands in that group.
- Project notebook verifier passes with optional workspace source index.
  Canonical DBC equals the child working copy; all submodule pins retained.
- No camera/model/Thneed/UI or child dependency change exists in this unpublished
  diff. This is preservation, not new hardware/performance validation.

Actual test commands, exit codes, logs and103source-file hashes are recorded in
TEST_RESULTS.json in the coordinating audit; the portable project summary is
TEST_SUMMARY.json. No broad managed daemons, camera/model runs or USB probes.

## Branch update scope

Owner request: “audit wat we hvae done ,update the master with real sunny ,update
teh rdxa our sunny ,”. Saved November5QA-20261105-01 resolves the branch meaning:
GitHub master mirrors official Sunnypilot; radxa/q8b retains our work. An initial
clarification was offered, then this existing explicit branch policy recovered.
This request authorizes the current mirror refresh and audited Radxa publication;
it does not resume automatic updates or merge upstream into the Radxa branch.

Pinned official master is3d8f211d4b2d7c4a981633783232c8ff8dbe402b,3commits after
GitHub master932ff06d: a1a28e467 model major.minor versioning,02ef6e4ce model artifact
parity,3d8f211d4 opendbc bump. Six changed paths affect model conversion/helpers,
model CI/tests/generation and opendbc. These changes will be mirrored as official
source only, not claimed tested/adapted for this Radxa Thneed/RetroPilot port.

The GitHub connector supplied fresh branch/commit/compare evidence. It cannot
upload the local Git object history; Git is used for that transfer. A narrow
fetch updates origin/master only, without checkout/submodule recursion. The
separate daily upstream-reference checkout and its held timer remain unchanged.
No force push or project rebase/reset/merge; old commits/history retained.

At this preparation checkpoint, audited local source is ready for normal
publication. Actual remote-update readbacks belong in publication.json and the
subsequent closeout, not an advance success claim. Child opendbc/retropilot is
already150f937198ceab43c43b39f94b9bdea63fcb633c. Default branch stays as configured.

## Remaining limits and next step

CAN reception remains unresolved; MCU timing/filter/error state is not exposed
by the reviewed USB API. No termination resistance value was supplied. Source
code can be reviewed further; no new hardware measurement is requested here.
Modern firmware implementation/flash/actuation and protected upstream integration
remain held. Next verify the two published branch refs and save actual receipts.
