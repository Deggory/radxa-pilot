# Active RetroPilot safety engine contract

Implement and test the missing state/command checks without selecting an
unqualified physical or BeamNG calibration. Chimera and physical Interceptor
work remain held; relays excluded. Existing registered mode39, parameter0,
continues disabled-command-only; unknown parameters allow no TX. Car interface
stays noOutput and controller runtime sends no CAN.

An immutable, explicitly supplied profile describes raw steering neutral/range,
slew/real-time bounds, dual gas channel offsets/ranges/rate, position-brake
bounds/rate, speed units/envelope, angle/rate bounds and incoming freshness.
No production profile is supplied. A test-only fixture is in the native C
harness under ALLOW_DEBUG; it cannot be selected by a firmware mode parameter,
and the fixture setter must be absent from release builds.

The first engine contract covers canonical steering interceptor0x300,
gas interceptor0x200 and iBooster position brake0x20E. Other endpoint families
still accept only disabled packets until their real mode/feedback mappings
are qualified. No RelayCore command is supported.

RX: require exact standard/classical data frames on bus2 and all seven base/
selected feedback messages, their full CRC8J1850, modulo16 counters and valid
quality. Two clean startup samples, no stale/missing feedback, no unexpected
counter repeats. Keep unknown/wrong-bus/DLC/returned frames from refreshing
trusted input. Explicit speed scale and expected SPEED source MODE; no unit inference from
MODE. ENGINE/CRUISE MODE must match the reviewed NO_FAULT0 contract. Track ignition,
engine+driver brake, pedal override, steering OVERRIDE, module health and
angle/rate. Fail shut on faults, stale input, ignition loss or out-of-envelope
feedback. Require released buttons at startup; ON toggles availability and a
separate rising SET/RES engages. CANCEL/driver intervention disengages; fresh
button action required to resume. Incoming packets alone cannot bypass the
missing production profile.

TX: sequential disabled packets remain available to release an endpoint.
With a profile, block invalid-sequence disables so endpoint/safety histories
cannot diverge; retain the last accepted output until release. Require one full16-counter
disabled cycle per selected axis before first engagement; this
models decoder acceptance and does not prove delivery. The unprofiled
production policy still allows all16counter values on disabled commands. Active commands
require healthy/available/engaged state even if controls_allowed is forced.
Check steering channels/sign/range, speed taper, slew and250ms change; gas
range/dual-channel agreement/slew; mode2 position brake/range/slew and zero
relative target; no simultaneous gas and brake. Require counter progress and
minimum command intervals. Reject malformed CRC/reserved fields/metadata.
Invalid active commands disengage. Brake must be released before gas resumes.

Tests use real compiled C hooks with canonical packers and independent vectors.
Cover allowed active commands inside fixture bounds as well as limits, stale/
corrupt/replayed inputs, driver takeover, button edges, startup/fault recovery,
mode changes, timestamp wrap, metadata and release-build containment. These
prove software behavior only, not actual firmware compatibility or vehicle
calibration. Active profile acceptance remains a separately qualified step.
