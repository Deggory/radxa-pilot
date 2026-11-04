# Camera, Thneed and RetroPilot commit names — 2026-11-04

Owner requested updating actual existing Git commit names so camera work says
camera, work for running the Thneed model says thneed, and RetroPilot work says
retropilot. This explicitly authorizes local history rewording for this task;
it does not authorize a remote push or future automatic upstream integration.

## Result

64 existing subjects changed. Labels cover28camera,16thneed and29retropilot
commits; mixed commits carry multiple scopes. One RetroPilot subject already
had its intended scope. The initial Q8B identity commit also touched camera
geometry selection, so it is included. All7local opendbc commit titles already
mention RetroPilot and remain unchanged, as do all historical submodule pins.
NPU research and unrelated work retain their original subjects unless their
actual changed paths include one of the requested camera/runtime components.

Examples:

- feat(camera): add Q8B road-only AK camera capture and publication
- feat(camera,thneed): connect Q8B Thneed to stock modeld and isolated camera UI
- perf(camera,thneed): keep Q8B camera views and history on GPU
- feat(retropilot): pin the RetroPilot receive-only car port and validation
- docs(retropilot): record required Chimera Interceptor and Actuator Core hardware

The branch remains radxa/q8b.90commit IDs changed through ancestry; all92local
commit trees were verified identical to their originals, including unrelated
messages carried forward. No application file, DBC, model, mode setting or
firmware changed during rewording. Author, committer, dates, message bodies
and Assisted-by disclosures were preserved; only subjects and necessary parent
links changed. No commits were squashed, dropped or reordered. No merge,
checkout/reset, remote push or runtime/device action was performed.

## History and evidence access

Original tip:6fb457bcf5013e168fb621f88d195a27006ec91a.
Reworded tip before this documentation checkpoint:
213cd6d9ef39010e5ca807ad856ccfdbb1f6f796.
Original history is retained at refs/backups/20261104-before-topic-reword.
Upstream base6f7a2c94 and child671f8c4 remain unchanged. The local Radxa branch
has no upstream tracking branch; a read-only origin check found no remote
radxa/q8b branch. No fetch/pull/merge/push was performed.

[CSV map](commit-map.csv) and [full mapping](mapping.json) retain old/new IDs and
subjects for all92local commits. Historical notebook/receipt SHAs intentionally
remain as original source-version evidence and still resolve via the backup;
use the map to find the corresponding current-branch commit. Do not blindly
replace old SHAs in recorded tests or rewrite frozen external C2 inputs.

[Independent verification](verification.json) re-read original/new commit
objects, comparing all trees, unchanged headers, exact body bytes, remapped
parents and the expected refs. The application tree at original/reworded tip is
exactly identical. The separate documentation commit adds this report/memory
and future naming rules; its documentation changes are not part of that
history-tree-equality claim. Runtime tests were not rerun for identical code.

## Validation ledger

Original local-commit and validation records were retained.90new-ID records
inherit actual original outcomes/timestamps/evidence, marked
inherited_without_rerun with their original SHA. A fresh history-equivalence
check is attached separately; it is not a new run of historical tests.
No original failure was turned into a pass. The raw inbox now counts17failed/
blocked SHA records corresponding to the same9original failure lineages;
these duplicates result from ID aliases, not newly failing software tests.
The mapping is also saved centrally as maintenance state commit_topic_aliases_20261104.json.
The ordinary daily timer stays enabled; check.lock protected the brief history/
ledger update from concurrent vendor-check snapshots. No upstream policy change.

## Naming rule from now on

Use type(camera), type(thneed), or type(retropilot) for related future work;
include both/all scopes for a commit spanning them. Choose the type describing
the actual change, e.g. feat, fix, perf, build, test or docs. Keep the description
concrete and retain required Assisted-by disclosure. Scope labels do not imply
that recorded benchmarks or a feature are fully integrated/tested on hardware.

NoOutput/zero live CAN, missing active vehicle calibration and hardware holds
are unchanged. Required hardware remains Chimera + Interceptor Core + Actuator
Core; relays excluded. Next engineering step remains actual BeamNG vehicle/
endpoint/units/modes/driver/calibration qualification when that work resumes.
