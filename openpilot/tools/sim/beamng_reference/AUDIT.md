# BeamNG reference audit — 2026-11-02

**Verdict: source bundle verified for adaptation; direct runtime integration is
blocked.** This audits the collected BeamNG reference and its interaction with
our current Sunnypilot APIs. It does not certify the entire Sunnypilot repository
or a running BeamNG/Q8B control loop.

Base project: `radxa/q8b`, `f72a1eaf118f422e1aa166e36ddb97dd847ce1d2`.
Upstream reference: Caleb-J773/beampilot-drive
`5435d67499f66eca58f95882cbe35e9c577e874c`. The original 82-file bundle was
expanded to **96 files / 1,160,682 bytes** during this audit. Original upstream
source is preserved byte-for-byte, with MIT license and source/submodule pins.

## Coverage and actual checks

- All 96 files: source Git blob, byte count, mode and SHA-256 verification.
  Fresh pinned GitHub trees and71 default-branch keyword-search results support
  the inventory. Matching non-instruction search hits are now included; foreign
  agent-rule documents were not installed. Keyword search/import tracing is
  not a formal proof of every dynamic dependency of a full fork.
- 69 Python sources parsed, 8 shell sources checked with `bash -n`,2 JSON mod
  manifests parsed. [FILE_AUDIT.json](FILE_AUDIT.json) records every source,
  category, checks and Python definitions/tests. This is static coverage;
  it does not mean every function was behaviorally executed.
- Twelve new corruption/regression tests pass for our verifier. Five initially
  exposed false-success cases. Disabling the checksum-list guard in an isolated
  temporary copy causes the matching test to fail, demonstrating test coverage.
- Upstream source tests were run through process-local import routing against
  the snapshot plus existing Sunnypilot dependencies. Result: **164 passed,
  6 failed, 1 skipped; 2 test modules blocked during collection**. One UI test module
  was deliberately not executed because it imports global UI/hardware objects.
  [UPSTREAM_TEST_RESULTS.json](UPSTREAM_TEST_RESULTS.json) retains per-module
  results and limits. These are not a clean full-upstream environment or a
  current Sunnypilot regression suite.
- Exact extracted upstream packet-parser/tick bodies were exercised with
  controlled data:96-byte BPL1 containing NaN is accepted; no-new-telemetry tick
  still publishes valid state and calls the control sender. No sockets or
  game were used by these probes.
- No live game, mod installation, desktop capture, model inference, manager,
  physical CAN, firmware or actuator was launched. No timing benchmark.

## Findings fixed in this checkpoint

### A1 — Missing supporting source (required; fixed)

The initial82files contained the BeamNG-specific tools and both complete mods,
but missed some modified cruise, event/actuation-check, MPC build/runtime, UI
integration and lane-change/UI test sources. Two direct imports also referenced
helpers absent from current Sunnypilot: `common/file_chunker.py` and
`selfdrive/modeld/compile_modeld.py`.

Added 14 original files, checked against their pinned remote Git blobs, and
regenerated MANIFEST/SHA256SUMS. All copied source remains inside `upstream`;
none of these snapshots replaces active project code. Generated native solver
bindings, models and the full base fork remain separate dependencies.

### A2 — Verifier false-success cases (required; fixed)

The original verifier could accept an empty/missing snapshot accompanied by an
empty file list, a wrong source repository/commit, or a changed SHA256SUMS file.
It now requires the pinned origin/commit and nonempty real source directory,
and checks checksum-list agreement before source integrity checks. Twelve
regressions cover these plus corruption, extra files, mode changes, symlinks,
duplicate paths and escaping paths. This is local consistency verification,
not a cryptographic signature of MANIFEST.json.

## Integration blockers and upstream limitations

### B1 — `beamngd` cannot import our current opendbc API (high)

`beamngd.py:14` imports `scale_tire_stiffness` from `opendbc.car`; the current
Sunny dependency does not export that symbol. After supplying the two missing
test packages in a temporary directory, this still blocks camera-calibration
and vehicle-geometry test modules and fails five gear/telemetry test cases.
Port the interface to current CarParams/vehicle-model APIs in an isolated
adapter. Do not replace our pinned opendbc or run the copied car installer.

### B2 — Stale telemetry continues to drive publication/commands (high)

`beamngd.py:535` drains UDP and parses the latest payload; `tick()` at1030 keeps
calling simulated car/sensors and send_control even when no packet arrives.
The previous state stays valid. A controlled source-body probe reproduces this.
BPL1 carries no source sequence, session or source timestamp. Lua's command-
silence watchdog (`beampilot.lua:1232`) is kept alive by continuing commands
computed from stale state. It does not solve stale telemetry.

The PC↔Q8B adapter needs independent source-age/session/order/disconnect gates
on telemetry, frames and commands, including pause/reset/reconnect handling.
A fresh Cereal publication timestamp must not make old source data look fresh.

### B3 — Nonfinite packet values are accepted (high)

`parse_telemetry()` at299 validates96 byte size and magic, then returns floats
without finite/range checks. A valid-size NaN-speed packet is accepted by the
exact parser body. Python `min(1.0, NaN)` returns1.0 in a separate diagnostic,
so ordinary clamps cannot substitute for explicit finite checks. This probe
is not a demonstrated full-bridge steering event. Reject nonfinite/unphysical
state before publication and validate every command independently at the PC.
The Lua receiver also applies provided engaged command values directly; its
loopback boundary is not a validated two-host command protocol.

### B4 — Existing steering path bypasses final torque control (high for scope)

`beamngd.py:837` deliberately reads `controlsState.desiredCurvature` and uses
VehicleModel's inverse to calculate a normalized game steering position.
Longitudinal uses `carControl.actuators.accel`. It does not apply the final
lateral `actuators.torque` output. This may test perception/planning/geometry
and game path following, but **does not directly validate our custom actuator
controller, torque response or NNLC performance**. Define whether a future
bench tests desired-path following or the actual lateral actuator chain; use
separate, explicitly mapped adapters and measurements.

### B5 — Same-host camera/address/timing assumptions (high)

`beamngd` uses BEAMNG_ADDRESS both to bind locally and to address commands;
Lua listens on127.0.0.1. Changing one IP is not a two-host bridge. `beamcamd`
captures the local desktop and publishes1928x1208 with publication-time
monotonic timestamps. Our current Thneed adapter requires1280x720 and explicit
Q8B road-only mode. Its borrowed webcam focal900 profile is not the game lens.
The source frame identity/capture age, network clock uncertainty, padded NV12,
stream selection, render FOV/crop and mount all need an explicit contract.
Do not let a new sim producer collide with the live webcam producer.

### B6 — Message rate and environment mismatches (medium)

External `PERIPHERAL_RATE_HZ=4` (`beamngd.py:268`) differs from our
`peripheralState` service frequency2 Hz. IMU is sent at the100 Hz loop versus our
nominal104 Hz service; measure acceptance instead of assuming configured rates.
The6 failed tests include1desktop-detection assertion that assumes xdotool is
installed; it is absent here and explain_not_found correctly reports that.
Do not label that failure a demonstrated BeamNG capture fault.

Current Sunny venv lacks evdev/mss/pytest. For this audit only, evdev 2.0.0 and
mss 10.2.0 were built into `/tmp` using upstream uv.lock SDist hashes; pytest 9.1.1
came from an existing isolated environment. Active project dependency files and
installed environment were not changed. Initial missing-dependency logs are
retained separately. One radar test skips without LuaJIT/game math fixtures;
Lua/Vue/JavaScript/game behavior remains untested.

### B7 — Installer/fork policy is not our deployment policy (required boundary)

The copied installer symlinks a BEAMPILOT car into opendbc and patches its
registration/torque overrides. Setup modifies environment and game mod links;
launch writes simulation Params, seeds calibration and chooses the fork's
process policies. These are reference source, not an approved install recipe
for this Radxa port. Fake Honda simulator CAN remains distinct from canonical
physical RetroPilot DBC. The old NPU W8A8 candidate stays rejected/unselected.

### B8 — Vehicle/motion feedback is a simulator approximation (required validation)

The BPL1 struct contains a single speed rather than four independent wheel
speeds; the fake Honda packer populates all wheel-speed fields from that value.
Simulator GPS uses a fixed-origin approximate XY mapping. Acceleration and
angular-rate fields are assigned into IMU messages without a measured local
axis/gravity convention test. Driver pedals are zeroed while simulated ACC is
engaged, and steering sign/geometry has source-specific assumptions. Keep
these distinctions explicit: match the spawned vehicle, map frame/units and
operator override, and validate actual measured feedback before using the
bridge as a lateral-controller evaluation rig.

## Next implementation gate

Use recorded PC game frames to prove a dedicated sim-only Q8B VisionIPC/UI
producer, source identity/time/layout and stale rejection. Then add measured
vehicle/motion state with current APIs and run shadow planning. Decide the
lateral command/feedback contract before enabling game-only control. Do not
use collection/static/test success as authorization for physical actuation.

[Portable validation](AUDIT_VALIDATION.json), [contract probes](CONTRACT_PROBES.json)
and audit_logs retain the reported evidence inside this project. Portable log
copies remove trailing whitespace; original hashes and original teacher logs
are preserved.

The teacher/student notebooks and maintenance ledger retain the exact source,
checks, failures and open limits. Full raw evidence and test-routing/probe
scripts are retained by teacher under sunnypilot-beamng-audit-20261102.
