# 2026-11-04 — Two approved upstream updates

Owner:"update these2", with camera, Thneed/model and RetroPilot protected.
Acceptance:exact upstream a86979d2 and8cf6ff9a only. Completed onradxa/q8b
as67876efcf03e18475565cd56a65726c015375c03 anda009818b752437d1b3c85334d1b292fbf51a7b95
fromed877d63. Source versions and every changed source path are in [receipt](../Evidence/sunnypilot-approved-updates-20261104.json).

15,384 protected hashes unchanged, including model/runtime; child671f8c4 and
all dependency gitlinks unchanged.217 distinct tests pass/1 existing skip;
Params native library rebuilt, mutation caught and restored, six additional
CPU integration checks pass. Source-independent review found no blocker.
No live model/hardware/vehicle run; default-on upstream boost preserved.
Initial expected missing-module/stale-native failures and corrected test API
mistakes are retained in logs. Existing safety/noOutput and hardware holds stay.

Future updates still approval-only. Timerlinked/inactive,no startup enablement
or next activation. No push or history rewrite. Application increments committed;
closeout notebook/evidence is a separate verified commit, with validation
journaled; inspect Git/ledger for the final documentation HEAD. Next:use this checkpoint and discuss any additional update first.
Full details and limits:[report](../Reports/upstream-approved-20261104/README.md).
