# Hardware requirements versus Q8B support — 2026-11-02

Accepted scope: update the earlier hardware requirements with known Radxa data,
using teacher evidence first. Documentation only. Branch radxa/q8b was clean at
`d88a72c6968e46e93090a7a5bbfb9bab340ab3f3`; latest runtime implementation remains
`ce7b0477c99f501e0393b54efb04d72f00107ddf`. CD210 model SHA-256 remains
`eb74164116723b2601730a19e2f2060a25bfdc3814bf7912ce991798df176068` (prior receipt,
not rehashed for this documentation task).

Updated the [canonical support map](../Knowledge/NONCAMERA_HARDWARE.md) and
[user-facing port guide](../../RADXA_PORT.md), plus notebook state/task/handoff/
worklog and teacher memory. All requested hardware areas now separate available
interfaces from their consumer and remaining integration work. Replaced the
port guide's obsolete assertion that camera/model/UI integration is future work.
Historical Nov 1 source-audit scopes remain clearly labelled.

Evidence: current HardwareRadxa/Pc/Base, read-only preview telemetry reader,
hardwared LinuxSystemStats/thermal/power calls, manager sensor/GNSS selection;
teacher IMU/GPS notes, Nov 1 non-camera host-summary.json, Nov 2 thermal inventory
and existing [UI run receipt](../Evidence/q8b-ui-telemetry-20261102.json).
Power-interface inventory is dated Nov 1; IMU raw/schema tests are Oct 16 at
`a5f44653`, not current IPC/locationd qualification. GNSS presence is unconfirmed
from saved records. Network backend assumes Wi-Fi; inherited zero power/GPU
usage is a placeholder. PWM is not RPM. Other temperature labels are not proof
of matching comma sensor locations.

Applied Agent Skills documentation-and-adrs and git-workflow-and-versioning,
with using-agent-skills routing and source-first evidence. REA binary/runtime
analysis was not applicable; none is claimed. No bus probe, sysfs write, camera/
model run or new runtime test was needed. Prior UI 76-test/65-second evidence
stays tied to its recorded implementation and retained launcher143 limit.

Validation: notebook layout/relative links/current workspace index and Git
whitespace checks pass; actual output saved in teacher hardware-support report.
No code or dependency changes; no new hardware or full-manager qualification.
Completed scope leaves no intended source edits. The documentation commit and
validation receipt are recorded in Git/maintenance ledger. Next bounded hardware
candidate remains read-only managed thermal mapping; power rails and mounted
IMU publication are separate later increments. Controls and driver monitoring
remain off in the current preview, camera geometry remains provisional.
