# Radxa Dragon Q8B project

This `sunnypilot/` repository is the working project, branch `radxa/q8b`.
Owner clarification, 2026-11-01: keep all active implementation and project
knowledge here; the other Comma workspace folders are references/support.

Initial upstream base: `6f7a2c94c10dffcf9a83b120ab1e6985e4496868`.
Q8B identity implementation: `12e44feeff241334e184c86dc9daccdc7f9e4fa1`.
Read [what we did](readme_wat_we_did.md) and [project memory](Ai/ROUTER.md).
`Ai/` is a regular tracked directory and travels with the project.

The daily job updates only the workspace's `q8b/sunnypilot-upstream/` reference.
It does not modify this branch. Related upstream changes require discussion
before integration. Keep reviewed/tested local commits and validation records.
The former `q8b/sunnypilot-radxa` path is only a compatibility link to this folder.

Camera/model/UI integration and actual hardware-health providers remain future
work. Old standalone model/runtime experiments are references, not automatic
project dependencies. No vehicle-actuation qualification is claimed.
