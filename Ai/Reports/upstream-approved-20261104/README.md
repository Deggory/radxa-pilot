# Two approved upstream updates — 2026-11-04

Owner approved these two updates and explicitly protected camera, Thneed/model
and RetroPilot. Applied to `radxa/q8b` from clean `ed877d63`; no general pull,
merge, history rewrite or push. Backup: `refs/backups/20261104-before-approved-updates`.
The reference was already at8cf6ff9a and was not advanced again. Only these
objects were imported from that existing local reference.

| Upstream | Local commit | Result |
| --- | --- | --- |
| a86979d2b2b176413a7f3e5cccf8c807596a7def | 67876efcf03e18475565cd56a65726c015375c03 | Hide Sunnylink steering-arc toggle on MICI |
| 8cf6ff9a33c94bdf2fcb02e228a9aef1a7e6dc7f | a009818b752437d1b3c85334d1b292fbf51a7b95 | Predictive acceleration boost, settings and tests |

Eight source files changed; all exactly match the pinned upstream8cf6ff9a
blobs. Original authors/dates/body and cherry-pick provenance retained with
Assisted-by disclosure. `master` and `origin/master` remain at6f7a2c94; this
is a scoped cherry-pick into the actual Radxa branch.

## Behavior and compatibility

Steering-arc visibility changes only for MICI. Boost uses existing model pedal
probabilities, curvature and stop request, with personality caps and gradual
build/release. Upstream `AccelBoostSP` is default-on; selection requires
`CP.openpilotLongitudinalControl`, and switching it off restores existing
AccelBoost. Current planner still takes minimum of MPC/cruise/E2E candidates,
clips acceleration and combines stop requests. No model code, weights or
output schema changes are required. Thneed already emits the required
six gas/brake probabilities through its existing parser/fill-model path.

Source review found no compatibility blocker. One upstream comment says4s
for a probability whose index1 corresponds to2s in current model constants;
kept exact upstream source rather than add an unrequested patch.

## Actual checks

- First update:75 settings/compiler/schema/capability tests,1 existing skip.
- Combined boost/Params/settings suite:102 tests,1 existing skip.
- Entire Sunny controls-lib test directory:124 tests, no skips.
- Six extra CPU-only integration checks:real native planner construction and
  longitudinal selection, stock-longitudinal exclusion, toggle-off restoration,
  actual Cereal message roundtrip, missing-probability reset and settings rules.
- Totals:218 distinct tests,217passed/1skip;14boost tests overlap suites.
- Mutation:inverted enabled guard failed disabled-reset regression; restored
  upstream bytes and reran14boost tests successfully.
- Native Params rebuild passed for new key; before rebuild the isolated test
  rejected `AccelBoostSP` as unknown. No bypass or source workaround.
- Ruff on affected Python files/extra tests and whitespace checks pass.
- Protected before/after SHA256:15,384 files unchanged. Every submodule gitlink
  unchanged; opendbc671f8c450fc74f5b8b90b2ee53124394108651ce remains clean.

Reproduce suites from project root:

```sh
.venv/bin/python -m unittest openpilot.sunnypilot.selfdrive.controls.lib.tests.test_accel_boost openpilot.common.tests.test_params openpilot.sunnypilot.sunnylink.tests.test_compile_settings_ui openpilot.sunnypilot.sunnylink.tests.test_settings_changes openpilot.sunnypilot.sunnylink.tests.test_settings_schema openpilot.sunnypilot.sunnylink.tests.test_capabilities
.venv/bin/python -m unittest discover -s openpilot/sunnypilot/selfdrive/controls/lib/tests
.venv/bin/python -m unittest discover -s Ai/Reports/upstream-approved-20261104 -p test_integration.py
```

[Machine receipt](../../Evidence/sunnypilot-approved-updates-20261104.json),
[protected SHA256 manifest](protected-files.json.gz), [logs](logs),
[extra integration checks](test_integration.py). Logs retain initial expected
missing-feature/stale-native failures, one corrected constructor-import probe,
and the extra test harness's initial API mistakes; those are resolved.

## Preserved scope and next step

Thneed artifact SHA256eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068
and current native Thneed library46c18dc88e507daf5efdbdde848ba70c3e7431850d802775edf048fa6eb8591d
are unchanged. No camera/model/game/firmware/vehicle or full manager run. No
live Params changes. RetroPilot stays noOutput/dashcamOnly, Chimera held and
physical Interceptor work held. CPU unit/source checks are not driving proof.

Automatic update timer stays linked/inactive, with no startup enablement link
or next activation. Only these two commits are approved; future updates still
need owner approval. Next:use this saved revision; discuss any further change
before integration. No outstanding code work for this two-update request.

Skills:Git workflow, incremental implementation, TDD, debugging, source-first
review, documentation and code review (independent read-only reviewer).
REA routing used readable pinned source and native CPU tests/build; no unrelated
binary analysis or invented REA result.
