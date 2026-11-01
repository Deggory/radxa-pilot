# Q8B hardware tasks

Planning checkpoint, 2026-11-01. No implementation completed by this plan.
Scope and rationale: [plan](plan.md). Overall status: [Ai tasks](../Ai/TASKS.md).

- [ ] H1 — Qualify and implement read-only thermal reporting. No dependency.
  Accept: type/domain mapping, correct units and explicit failure behavior;
  discovery/conversion/error tests, isolated live readback and current-schema
  encoding; existing identity checks pass.
- [ ] H1 checkpoint — Review, commit, journal actual verification and update
  both memories. Depends on H1; retain observed limitations.
- [ ] H2 — Qualify power domains and implement supported readings. Depends on
  H1 checkpoint. Accept: known rail boundaries/units, conversion/failure tests
  and isolated readback; no unsupported battery/total-power claim.
- [ ] H3 — Implement physical IMU provider. Depends on H1 checkpoint; independent
  of H2. Accept: qualified mounting/axes/scaling/timing, bounded live freshness
  checks and actual IPC/consumer/fault tests.
- [ ] H4 — Qualify cooling ownership and any required fan policy. Depends on
  H1 checkpoint and verified interface. Accept: automatic/manual ownership,
  bounded behavior and failure recovery. Preserve automatic mode until qualified.
- [ ] H5 — Qualify remaining needed services and actual GNSS hardware. Depends
  on consumer requirements. Accept: per-service source mapping, identified
  devices and focused success/failure tests before enabling services.
- [ ] Per-slice checkpoints — After H2–H5, review, commit, attach actual
  validation and update both memories before proceeding.
