# RetroPilot active safety engine — 2026-11-03

Owner requested fixing missing active safety behavior for current Sunnypilot
on existing Radxa Q8B. C2 is a reference, Chimera remains held and relays excluded.
No physical vehicle/game/device action was performed.

## Result and boundary

Added parameterized C safety engine in opendbc/safety/modes/retropilot_active.h,
called through the existing RetroPilot hooks. Normal initialization supplies
no active profile; mode39 parameter0 still accepts disabled commands only,
unknown parameters allow no TX, and forwarding stays disabled. Car interface
still requests noOutput/dashcamOnly; runtime controller sends no CAN.

The first engine covers interceptor steering0x300, gas0x200 and iBooster
position0x20E on explicit bus2. Other families remain disabled-only. Artificial
limits exist only in the native test harness under ALLOW_DEBUG. No firmware
mode parameter can choose them; the fixture setter is absent from release.
There is no qualified BeamNG or physical vehicle profile.

## Implemented checks

Seven required RX messages enforce bus/DLC, full CRC8J1850, modulo16 counters,
metadata/quality, two clean samples and a fixture100ms deadline checked at TX.
ENGINE/CRUISE MODE0 follows the reviewed producer fault contract. SPEED source
MODE and speed divisor are separately explicit. Angle STATE1 and actuator
STATE0 conventions are separate. Speed, angle/rate envelope, ignition, driver
brake/gas/steering override, availability and button edges gate engagement.
Corrupt RX latches private disengagement even if controls_allowed is forced.

Steering requires opposing channel deviations, amplitude/speed taper/slew and
250ms change bounds. Dual gas channels require range/ratio/slew agreement;
iBooster requires mode2 position/zero-relative target, range and slew. Commands
require timing and sequential counters. Gas and brake cannot overlap. Faults
retain accepted output state until a sequential release; board-blocked releases
cannot erase it. Active-profile invalid-counter disables are blocked to avoid
endpoint/model divergence. Production unprofiled disables still allow all16.

Startup requires a full16-count disabled cycle for each selected axis before
engagement. Unlike gas firmware which updates its counter on rejected sequence,
the reviewed iBooster increments only on an accepted counter. Two disables
therefore do not cover an unknown initial counter. One full cycle covers all
possible previous modulo16 values if delivered; this is not a receipt ACK or
proof about installed firmware/session behavior.

## Evidence and review

[Contract](CONTRACT.md), [focused log](focused.txt), [full safety log](full-safety-tests.txt)
and [host log](host-tests.txt) retain actual runs. RED logs retain missing engine,
release/outer fault, corrupt-RX latch, producer MODE and startup-cycle failures.
The initial incomplete release probe passed because availability toggling masked
the state bug; the corrected release-red test reproduces it and now passes.
Independent review found counter/recovery/health/startup issues; all were fixed
with regression evidence. Final review found no Critical/Required issue in this
software-only increment. Full counts/pins/hashes are in
[the receipt](../../Evidence/retropilot-active-safety-20261103.json).

Source baselines: parent14a44ca4, childa6099a1e; canonical DBC6b90fafe,
byte-identical packaged/canonical SHAef6eef74. Local ocelotd87892fa is dirty,
not proof of installed firmware. Important compatibility limits include partial
CRC for0x301, producer units, source modes, and actuator mode/layout differences.
No DBC/Cereal schema/safety ID/model/Chimera source changes in this increment.
No new coverage claim or ARM image/MISRA qualification. No related pending
upstream commits in last inbox; protected project never merged automatically.

## BeamNG vehicle question

Pinned Caleb-J773/beampilot-drive5435d674 tells the user to spawn a car. Its
README includes an Ibishu Covet example log and ETK800 steering-rack examples.
HONDA_CIVIC_2022 is its old CAN/platform identity, not the in-game selection;
BEAMPILOT is the newer identity and geometry comes from the spawned vehicle.
This does not identify the owner's loaded game vehicle/configuration. The
bridge's curvature-to-position path also does not qualify our final CAN
steering/pedal mapping. Reference bundle remains unchanged.

Next: identify the selected game vehicle/configuration and qualify its actual
endpoint/units/driver/command contract, then supply measured safety limits and
validate the complete game-only loop. Do not resume held Chimera or physical
Interceptor work. Readable source plus native compiled tests were sufficient;
REA artifact/runtime analysis was not needed or claimed.
