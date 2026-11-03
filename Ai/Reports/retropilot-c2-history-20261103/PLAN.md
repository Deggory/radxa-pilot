# RetroPilot reference research and modern Radxa implementation

Owner confirmed existing Radxa Q8B, not a physical comma4. Target parent
35d46c1e179d0f6a541e32e5669ee0c879b408b1, opendbc9da9210adfa4dc213424f36945caccd40182c80d.
Execute the owner's existing modern-port instruction and teacher PORTING_PLAN;
the historical review below supports understanding RetroPilot behavior and
protocols. Owner clarification: implement only what current Sunnypilot on
Radxa needs; do not reproduce the C2 integration or mirror its changed folders.

- [x] Recover complete parent branch delta and every included commit, separating
  28commits dated2025 from7older upstream commits. Compare all3changed submodules.
  Verification: pinned GitHub compare data, complete commit/file coverage table.
- [x] Correct steering source-state semantics from actual Chimera/ZSS producers.
  Verification: failing STATE1 regression, actual parser/state/replay tests.
- [x] Add a receive-only Chimera USB mailbox/health adapter and modern CAN-event
  conversion, with device/version pinning and no transmit/flash/config API.
  Verification: independent wire vectors, malformed inputs, fake USB allowlist,
  timeout/disconnect handling, real Cereal -> CarState -> controller replay.
- [x] Map each history change to current behavior, required adaptation, or a
  rejected legacy shortcut. Include PID/joystick/relay, startup, firmware safety,
  Cereal, Linux build, NEOS and inherited model changes.
  Verification: every parent/submodule changed file and all35parent commits mapped.
- [x] Run applicable regressions/lint, review, commit verified increments and
  update both notebooks, maintenance validation and restart handoff.

Live physical output remains outside this increment. Transport acceptance
does not establish MCU safety, calibrated dynamics/driver inputs, electrical
topology or managed onroad readiness. No firmware/config writes or game control.
Do not copy C2 communication/model/GPS suppression or joystick engagement bypass.
REA GNU symbols/disassembly observes retained Chimera ELF identity and mailbox/health code; native decompilation and
pwntools layout are unavailable on this configured AArch64 host. Preserve those
limits, with source and offline tests as distinct evidence.
