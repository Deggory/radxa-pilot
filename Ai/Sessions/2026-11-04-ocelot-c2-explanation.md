# Ocelot in the C2 port — 2026-11-04

Owner asked what Ocelot mentioned in C2 means. Read teacher/student handoffs,
routers and update inbox, actual Git and retained C2 sources. Parentec53967 /
child671f8c4 clean; local Ocelotd87892fa remains separate dirty reference/project.
No source modification, runtime test, device/CAN/firmware or held-task action.

Ocelot README identifies firmware for RetroPilot gateways/control modules.
C2 values.py selects ocelot_controls; ocelotcan.py creates steering/gas/iBooster
commands; carcontroller.py imports and sends constructors for DetectedEcus.
Hardware roles: Chimera gateway/sensor conversion, Interceptor analog signal
interface, Actuator Core motor control, iBooster brake-control firmware. This
is supported-code evidence, not proof all modules were installed/tested in C2.

Modern commands.py fulfills the CAN constructor role with the canonical DBC;
firmware remains a separate module-side requirement. No need to copy the
entire Ocelot project into modern car code. Existing incompatibility/profile/
noOutput and Chimera hold limits persist. Relays not proposed or resumed.

Pinned C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728, DBC6b90fafe. Verified retained
C2 file SHA hashes against SOURCES.json; documentation/notebook/whitespace checks
only. Previous168 tests/full8806 evidence is historical, not rerun for prose.
Skills source-driven and documentation, existing Git workflow; readable-source
REA route, no unrelated artifact analysis. Inbox0related pending; timer active/
persistent nextNov4 15:30UTC. Last recorded checkNov3 15:30; no new merge.

Teacher repo notes plus student topic/handoff/state/tasks/worklog updated.
Next remains selected BeamNG car/config and actual endpoint/units/modes/driver/
calibration contract. No shutdown requested in this new explanatory turn.

## 2026-11-04 — Old/reference DBC versus current Sunnypilot DBC

Owner asked whether Ocelot DBC is needed and requested comparison. Yes: current
RetroPilot values.py selects ocelot_controls; CarState and CarController use that
mapping, and commands.py requires it. Canonical retropilot/dbc copy and packaged
sunnypilot/opendbc_repo/opendbc/dbc copy are byte-identical:7363bytes,20messages,
120signals,SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
Direct diff returned0/no output; retained SOURCES.json confirms upstream
RetroPilot/opendbc6b90fafe59e81822bfae58e4ecb080248e9de40d. All encoded IDs/DLC/
bit layouts/scales/offsets/signedness match because bytes match. No extra Ocelot
DBC was found in the separate local Ocelot tree, including ignored/hidden paths.

The modernization changes host parser/controller/safety code, not these DBC
bytes. C2 constructor bus0 vs modern explicit hostbus2 is routing outside DBC.
DBC equality does not establish installed firmware CRC/layout/units conformity
or calibration. No schema/code/DBC/device changes, fresh runtime tests or held
hardware work; prior results stay prior. Source comparison only, recorded in
Evidence/retropilot-dbc-comparison-20261104.json.
