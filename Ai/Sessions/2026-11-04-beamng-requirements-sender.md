# BeamNG requirements and Waveshare sender navigation — 2026-11-04

Owner asked what else Sunnypilot needs beyond steering,speed,IMU,pedals,wheels
and cruise status, and requested opening the sender folder.

For this BeamNG setup, additionally need gear/ignition readiness (raw gear index is already transported but Drive/Reverse/Park mapping is pending), an explicit engage/cancel input (current cruise status is not button presses), driver override and actuator-ready/fault feedback appropriate to the selected control method, calibrated vehicle/steering parameters, aligned road-camera/model and simulator IMU integration, reliable timely CAN with enforced safety/fault shutdown, and a return path mapping final Sunnypilot CAN commands to game steering/throttle/brake. Real-vehicle doors/seatbelts/parking-brake conditions apply where appropriate; this does not require inventing simulator signals or bypassing checks. Radar is not mandatory for this current radarUnavailable simulator profile. Current runtime remains noOutput/dashcamOnly and live controller TX is empty; previous physical CAN attempt received0frames. No new CAN test or activation this turn.

Source pins: project4cc6d67195c20f1edf19a38d703c58ffff6418b0,
opendbc150f937198ceab43c43b39f94b9bdea63fcb633c. Read current RetroPilot
interface.py/carstate.py/carcontroller.py, gateway.py, PC README and the
existing optical+CAN plan/report. Historical parent BeamNG README tables still
contain older pending statuses; current source and last runtime report were
used to avoid treating those entries as current implementation truth.

PC became reachable again without network changes by this agent. Verified
folder/gateway existence; gio open succeeded on its desktop. Opened gateway.py
in the current Radxa VS Code window and its folder through xdg-open (both0).
PC path: /home/pc/beamng-q8b/retropilot-can/pc.
Radxa source: openpilot/tools/sim/beamng/pc.
Game Lua producer: pc/mod/lua/vehicle/protocols/radxaRetropilot.lua.
Completed the previously pending5-line PC README clarification copy.

Documentation skills/source-first workflow used; no new REA binary result
needed/claimed. No CAN TX, game/control operation, firmware/package/upstream
change or new runtime test. Prior492genuine replay and0physical CAN reception
are historical results, not rerun. Next engineering task remains physical
CAN qualification, then managed receive integration/shadow and game return path.

Validation: student memory checker103documents/335relative links/240optional workspace links/8source repositories/4254indexed entries passes; git diff --check passes. Folder/file launch commands returned0. Runtime regression tests were not rerun for this documentation-only follow-up.
