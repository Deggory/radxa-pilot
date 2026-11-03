
## 2026-11-03 — Radxa-focused docs assessment

Owner wants a simpler Radxa project. Inspected docs27files/366532logical bytes
before edit (~440KiBallocated). Useful porting/policy/logging/safety references
remain; comma connection/public-site pages are optional references, not Q8B
setup. Updated docs/README.md with a short Radxa entry index. Existing op docs,
site CI and car-doc generator/maintenance consume this tree. No deletion or
runtime change. Hardware selector still imports HardwareComma unconditionally;
HardwareRadxa inherits HardwarePc, so names alone do not justify pruning.
Detailed scope/limits: Knowledge/REPOSITORY_CLEANUP.md in the student notebook.
Next cleanup needs dependency-checked scope; current BeamNG wire-contract task
remains pending. Documentation-only checks; no REA binary/runtime claim.

Changed docs/README.md and notebook only. Base d17dc3cd1e71fef7187b5a6267266a51f17a4c81. Validation evidence in teacher Ai/Reports/sunnypilot-docs-cleanup-20261103/validation.json. No new runtime test or deployment.

Validation PASS:70notebook documents/216relative links/8pinned repositories/4252index entries; docs README16relative links and safety symlink valid; staged whitespace check. No runtime/website build or hardware test.
