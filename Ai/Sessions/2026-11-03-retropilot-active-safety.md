# RetroPilot active safety engine — 2026-11-03

Accepted scope: fix missing modern safety behavior for existing Radxa Q8B;
C2 is behavior/protocol reference only. Chimera remains held, relays excluded,
physical Interceptor not resumed. No game/hardware/firmware/USB/CAN action.

Parent baseline14a44ca4f1cbf9579dfd592a1e6faf9759c41e31; childbaseline
 a6099a1e141f17ec18ca9b065cf9a8f972e0cac8. Verified childcommit
671f8c450fc74f5b8b90b2ee53124394108651ce on radxa/retropilot. Parent radxa/q8b
records that pin and report. Canonical DBC6b90fafe/SHAef6eef74 unchanged;
local ocelotd87892fa is dirty/untracked source, hashes retained, not installed
firmware. Current CD210 GPU/model path unchanged. No upstream integration.

Implemented safety/modes/retropilot_active.h, wired from retropilot.h, with
native-only test fixture under ALLOW_DEBUG in tests/libsafety/safety.c and
29 active-engine tests in tests/test_retropilot_active.py. Child README and
SOURCES.json updated. Parent docs/RETROPILOT.md, reference README car explanation,
Ai contract/report/receipt and notebook state updated. Cereal schema/ID39,
DBC, controller runtime, manager and held Chimera source were not changed.

Contract/evidence cover seven required exact/integrity/quality/fresh RX,
explicit speed/source mode, ignition/pedal/steering intervention, ON and SET/RES
edges, fault latch and force-controls resistance. TX checks interceptor channel
agreement/limits/slew/250ms delta/speed taper, gas ratio/limits/slew, iBooster
mode2 position/zero-relative target/limits/slew, counter/time progress and
pedal interlock. Output history persists until permitted sequential releases.
Startup full16-count disabled cycle covers unknown modulo16 previous counters
if delivered. No acknowledgement or installed-decoder qualification is claimed.

Independent review identified release-counter endpoint/model divergence,
corrupt-RX private latch, MODE fault handling and startup counter behavior.
Strong RED regressions were recorded and fixes validated. Self-review fixed
board-fault-blocked release mutation. Final reviewer: no Critical/Required
findings for this software-only increment. Early two-disable startup draft was
insufficient for strict iBooster; final contract uses a complete counter cycle.
The initial incomplete board-fault probe passed due availability toggling; the
corrected probe reproduces the bug. No tests skipped/removed or bars lowered.

Validation: `.venv/bin/python -m unittest opendbc.safety.tests.test_retropilot_active
opendbc.safety.tests.test_retropilot`50 pass (29+21), including debug strict-Werror/
UBSan and release fixture absent. Full native discovery8806 run,932 existing
skips, no failures. Host RetroPilot discovery45 pass. Ruff and whitespace pass.
No new coverage metric; previous policy coverage belongs to prior source.
No ARM image/MISRA qualification or hardware-calibration result. Raw final
logs and all relevant RED failures retained in the report; hashes/commands
in Ai/Evidence/retropilot-active-safety-20261103.json.

During work owner asked which car Caleb's BeamNG-openpilot used. At pinned
5435d674, README233 says spawn a car,509 describes BEAMPILOT replacing old
HONDA_CIVIC_2022 identity; geometry section contains Covet log/ETK800 examples.
No one required model is established. This does not identify the owner's
loaded car/configuration or supply our final torque/pedal mapping. No remote
PC/game inspection. Existing inbox had0related pending commits and9historical
failed/blocked records; protected Radxa project not pulled/rebased/merged.

Skills: source-driven, TDD/incremental, interface design, debugging, independent
code review, documentation and Git. REA/source-first workflow applied: readable
source/native compilation sufficient; no unrelated REA binary/runtime proof.

Next: resolve selected game car/configuration and actual endpoint/units/modes/
driver/calibration contract. Then qualify an explicit measured safety profile
and game-only integration; do not enable production output from test fixtures.
Chimera remains held until resumed. Child committed; parent contains report,
pin and student memory. No push; actual ledger entries attach validation.
