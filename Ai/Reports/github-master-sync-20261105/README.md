# GitHub master synchronized — November 5, 2026 UTC

Owner request: “see can we make the master in github same as real sunnypilot”.
Accepted scope: synchronize only `Deggory/radxa-pilot`'s `master` with official
`sunnypilot/sunnypilot` `master`. Existing Radxa work stays on its own branch.

Master advanced from `8cf6ff9a33c94bdf2fcb02e228a9aef1a7e6dc7f` to
`932ff06d9316e4351d6b6b9f1dd422d5b639badf`. GitHub compare and local Git ancestry
checks show exactly one descendant commit: **modeld_v2: fix action curvature
(#2091)**, changing `max(1.0, v_ego)` to `max(2.5, v_ego)` in the curvature
denominator. Source:
https://github.com/sunnypilot/sunnypilot/commit/932ff06d9316e4351d6b6b9f1dd422d5b639badf

Validation: dry-run and actual normal Git push passed; independent GitHub readback
shows both masters at the same commit (therefore identical committed file tree).
Upstream tree: `a60b6b1fd8683c69de8255f58add368878a38bd7`. Remote `radxa/q8b`
remains `f193a3cbaa0c5abcad971a34e7b754929ba0e907`; `opendbc/retropilot` remains
`150f937198ceab43c43b39f94b9bdea63fcb633c`. Default branch is still `radxa/q8b`.
The local project was clean before documentation. [Receipt](receipt.json).

GitHub connector reads/compare succeeded but ref writes returned403; the existing
Git connection performed the fast-forward without force. A redundant isolated
fetch was stopped; fetching the single new commit into the existing object store
succeeded without a checkout or working-file change. No branch history rewrite,
reference-checkout advancement, timer resume, model run or hardware action.

Skills used: Git workflow/versioning, documentation/ADRs and source-driven
investigation. This uses readable-source/Git evidence; no REA runtime result is
claimed. Documentation closeout is committed locally, not pushed to the protected
Radxa branch. No functional source changes here require a runtime regression run.

Next: owner-selected Chimera receive diagnostics. Keep noOutput and the existing
relay/actuation exclusions. The latest upstream curvature fix is relevant to the
model path but requires separate approval/review before Radxa integration. Future
automatic upstream updates remain paused.

## Follow-up: default branch and comparison direction

Owner asked why master showed3ahead/113behind Radxa and wanted Radxa compared
to master. Set GitHub default to master with gh repo edit; independent connector
readback confirms master. Comparison master...radxa/q8b is113ahead/3behind;
all three remote tips remain unchanged. Counts are commit-based: earlier two
upstream changes were cherry-picked into Radxa under different hashes. No code
merge, firmware work, automatic update, runtime retest or Radxa push. This
supersedes the earlier Radxa-default statement. QA-20261105-02 and the separate
default-branch.json receipt preserve the actual question, answer and metadata.
Documentation links/whitespace checked at closeout; Git workflow/documentation
skills and source-first routing reused. No binary analysis was necessary.
