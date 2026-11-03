# Documentation and Radxa cleanup assessment

Reviewed 2026-11-03 at base d17dc3cd1e71fef7187b5a6267266a51f17a4c81.
Owner wants a simpler Radxa-focused project and asked whether docs/ is needed.

The existing docs tree had27 tracked files,366532 logical bytes (following the
safety symlink),440KiB allocated before the README edit. It is documentation
plus an optional site builder, not the comma-four hardware backend. Changing
these docs does not make the driving pipeline faster; no performance test was
performed. Updated docs/README.md to put actual Q8B install/status/handoff and
BeamNG guides first and label inherited upstream pages as references.

| Group | Current decision and reason |
| --- | --- |
| AI_POLICY.md, CONTRIBUTING.md | Keep development policy and attribution context. |
| SAFETY.md, concepts/safety.md, LIMITATIONS.md, INTEGRATION.md, DEBUGGING_SAFETY.md | Keep conceptual/debugging references; upstream/Panda-specific instructions are not Radxa qualification. concepts/safety.md is a symlink to ../SAFETY.md. |
| how-to/car-port.md, concepts/logs.md, how-to/replay-a-drive.md | Useful car-interface/log/replay guidance; replay page's physical CAN section is device-specific and incomplete. |
| CARS.md and icon assets | Upstream generated catalogue, not loaded car-port code or proof of Radxa/Chimera compatibility. Source generator and maintenance job write this file. |
| how-to/connect-to-comma.md, how-to/turn-the-speed-blue.md | Comma connection/tutorial instructions are not Q8B installation; reference-only during porting. |
| index.md, contributing/{architecture,feedback,roadmap}.md | Upstream public-site/community context; architecture page is currently only a heading. Not our port roadmap. |
| README.md, serve.py, template.html, assets/ | README now Radxa-first; site builder/theme/assets are optional on-board but needed by existing op docs/site workflow. |

Dependencies inspected: tools/op.sh docs function invokes docs/serve.py;
.github/workflows/docs.yaml builds/publishes the optional site;
.github/workflows/repo-maintenance.yaml invokes openpilot/selfdrive/car/docs.py
and stages docs/CARS.md. That generator defaults to docs/CARS.md and emits
relative icon paths. Root pyproject has an assets lint exclusion. A caching
test references remote upstream SAFETY.md, not this local file. git grep also
found a string match in the shipped comma updater binary; string presence is
not proof that the local docs tree is a runtime dependency and was not analysed
as one. No REA runtime/binary question was necessary for this docs decision.

Do not delete hardware directories based on names: actual
openpilot/common/hardware/__init__.py imports HardwareComma unconditionally,
and HardwareRadxa subclasses HardwarePc. Removing either dependency requires
an explicit selector/import/build change and appropriate tests. This inspection
is not a complete hardware/build dependency audit.

Recommendation: keep reference documentation while porting, use the short
Radxa entry page, and omit optional development/site files from a later verified
deployment package. No files were deleted, moved, hidden or executed. No
runtime/backend/build/CI configuration change. The owner's simplification
objective is recorded; a destructive whole-repository pruning was not attempted.
BeamNG optical/CAN requirements and pending implementation remain unchanged.

Skills: code-simplification, deprecation-and-migration, documentation-and-adrs,
Git workflow and source-first review. Validation: README links, notebook checks
and staged whitespace checks; no runtime test needed for the prose-only change.
