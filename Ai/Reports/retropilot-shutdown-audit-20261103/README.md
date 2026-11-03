# RetroPilot audit and shutdown handoff — 2026-11-03

Owner requested an audit, learning saved in teacher/student Ai, then closing
VS Code and shutting down the local Radxa PC. The remote BeamNG PC is not a
shutdown target. All application work remains in sunnypilot/ on radxa/q8b.

## Audited result

Application baseline469f3c5c3d325380069c4380b8efcab8dc78d2cd and child
671f8c450fc74f5b8b90b2ee53124394108651ce were clean. All10 source hashes from
the active-engine receipt match, including both byte-identical canonical DBC
copies and dirty/reference Ocelot source. This audit changes documentation and
memory only. It does not resume Chimera, Interceptor, relay or device work.

Fresh checks:50 compiled safety tests (29 active engine/21 restricted),45 car
port tests,53 CAN tests and20 offline adapter/migration tests pass:168 total.
Ruff passes. Prior full native safety8806 run/932 existing skips/no failures
remains tied to the same unchanged source; it was not rerun for this shutdown.
Debug/release fixtures are covered by focused safety tests. No new full build,
MISRA/ARM image, camera/model/game/hardware or firmware qualification.
Actual test runner is project Python3.12.13; prior receipt environment3.12.3
was its system-Python writer, not the test runner. No dependency change.

[Receipt](audit.json) lists all scoped changed paths and actual commands.
[Active engine report](../retropilot-active-safety-20261103/README.md) retains
implementation decisions, independent review and initial RED evidence.

## What teacher and student must remember

- Modern car package reads CAN and computes offline candidate commands. The
  canonical DBC describes their byte encoding; its ranges are not calibration.
- retropilot.h is the safety entry/disabled-command checks and includes
  retropilot_active.h; together they form one policy. modes/ supplies firmware
  safety source, not automatic host-side enforcement or a flashed Chimera.
- Shared fingerprint/selection helpers, car registration/torque placeholders,
  car.capnp enum39 and safety declarations/registration are also part of the
  port. The three main folders/files alone are not the entire integration.
- C2 is protocol/behavior evidence, not a checklist to recreate its old stack.
  Its reviewed WIP safety disabled RX integrity checks and enabled controls
  from reception. Its ability to emit commands is not proof of road readiness.
- Our active engine has tested sensor/engagement/driver/command rules using
  artificial native-only limits. No firmware parameter selects that fixture.
  Normal mode39 allows disabled packets only. Interface noOutput/dashcamOnly
  and runtime empty CAN output remain. No active measured profile exists.
- Runtime integration, truthful board health, actual endpoint/units/mode and
  physical driver/vehicle calibration remain unqualified. Automatic car
  detection is not implemented; explicit RetroPilot/C2 alias selection is.
- The receive-only Chimera adapter and its offline tests exist; managed/live
  safety enforcement is unfinished and Chimera remains held by owner direction.
- Cereal source/Panda firmware/model were not changed by this RetroPilot scope;
  car.capnp in opendbc changed and is imported by Cereal. Canonical DBC was
  packaged unchanged. Legacy firmware can still disagree on CRC/layout/units.
- Caleb5435d674 uses the user's spawned game vehicle, with Covet/ETK800 examples;
  its old Honda identity does not identify the owner's actual game car.

## Restart

Read teacher Ai/RESUME_HERE.md/router/inbox, then student HANDOFF/STATE/TASKS
and this report. Check actual HEAD, dirty files and ledger validation. Keep
current CD210 GPU/model path. First resolve actual BeamNG vehicle/configuration
and endpoint/units/mode/driver/calibration contract; then qualify explicit
limits and a game-only loop. Do not enable test fixtures or resume held hardware.
No related upstream commits pending at last check; no automatic project merge.
Daily reference timer is active/persistent, next2026-11-04 15:30UTC, last success.

## Save and shutdown

Tool-written project work is on disk; verified changes are committed before
shutdown. VS Code autosave is afterDelay, stored backup count0. Electron's
AT-SPI tree exposed only frame/application, so Save All could not independently
be inspected. Temporary accessibility/screen-reader signals were restored;
initial failed UI probes are retained centrally, not represented as a pass.
Use normal GNOME session poweroff to allow editor cleanup and respect its
shutdown-delay inhibitor. No force kill, discard or inhibitor override.
Shutdown is requested only after audit/notes/validation/index updates and sync.
The final queued/readback receipt is in teacher
Ai/Reports/retropilot-shutdown-audit-20261103/shutdown.json. Physical poweroff
cannot be confirmed from this host after it turns off.
