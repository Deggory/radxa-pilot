## 2026-11-03 — C2 history-led adaptation on existing Radxa Q8B

Owner explicitly requested all C2 integration work beyond the car folder and
REA plus Agent Skills. Clarification answered: existing Radxa Q8B, not physical
comma4. Protected project remains radxa/q8b, parentbase35d46c1e179d0f6a541e32e5669ee0c879b408b1.
Fresh GitHub upstream master remainsa86979d2; no merge/update to protected code.

Recovered complete pinned parent delta:35commits beyond2022base
 da2ea41241f16c4b0e80a52fdc40ed57becd185b to C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728;
28dated May15–August14,2025 and7older upstream.50final paths/64historically
touched paths. Nested Panda2commits/2paths at9e6d47f, Cereal3/6 at a7193d0,
opendbc43/10 at6b90fafe includes2021/2022/2025 ancestry. All35parent commit
patches fetched through GitHub.82path dispositions verified, with transient
paths and inherited upstream attribution separate from actual retrofit work.
This is path coverage/relevant patch review, not a claim of line-by-line
review or live testing of unrelated kernels/binaries. Immutable retropilot
reference folder not restored or edited. Full report, timeline, source JSON,
coverage verifier and REA Evidence are in Ai/Reports/retropilot-c2-history-20261103/.

Implemented parent openpilot/selfdrive/pandad/chimera{,_protocol}.py and2test
modules: normal-mode serial/product/version pins, mailbox16/health43 decoding,
exact classical CAN DLC/bus/reserved-bit checks, returned/RTR filtering, raw
health, timeout transferred-byte preservation, clean release/close and optional
modern Cereal CAN publication. Default is bounded JSONL monitor. No Panda
import, flash/recovery, kernel auto-detach, vendor-OUT, CAN TX, heartbeat,
relay/bitrate/config mutation, sendcan subscription or fake pandaStates.
Not an automatic manager replacement. No real USB handle or publisher opened
in this task; CLI tests use fake USB/publisher and real Cereal/state/controller.

Corrected actual producer mismatch in opendbc86a839dcec8ed9a3e45315eac804fa1001f1b2d6,
from9da9210: reviewed Chimera TIM3 and ZSSv0.2.0 use angle STATE1=enabled;
prior receiver STATE0 assumption was wrong. Other module STATE0 fault meanings
stay separate. New STATE1 regression failed then passes; canonical DBC bytes
SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce unchanged.
No active profile selected; wheelSpeedFactor0, noOutput/dashcamOnly, unknown
gear/carNotReady, zero live output and CD210/OpenCL/Thneed eb741641 retained.

REA selected retained Chimera ARM ELF SHA5ae9b4f6ea99e569028d271c4ec9c2ce59cd11375b5482adbd0781f3480e20b8.
GNU symbol Evidence ev_ac17a8b5cec16bed89cad2a8ccf9d13d887340650716039ff3890278cb28be78
and assembly ev_6c720630735de45e83f641b76daea07ba4d1813541724750f8670e1cf723a934
complete/no truncation/no artifact change. get_health_pkt0x080077b0 returns43
and stores raw17; usb_cb_ep1_in0x080079b8 uses16byte stride/4record cap;
can_send0x08006e60 visible body queues via can_push/process_can without a
safety hook, corroborated by source. Not whole-firmware safety proof or an
installed-device pin. Native providers unavailable; pwntools layout Linuxx64
only. Those failures retained. GNU provider version/formats remain unknown.
No firmware execution/build/flash or external engine installation performed.

Read-only sysfs currently finds bbaa:ddcc product Interceptor DAC Bench,
serial440048001251333133333633, bus3/device8. It differs from historical Chimera
serial3a0044001651333038373636. No handle opened/CAN consumed and paused
Interceptor project not resumed. New rejection test protects shared-VID/PID
identity. Preserve this descriptor observation/date, not an installed-image
claim; actual Chimera remains unavailable for live acceptance this session.

Migration map explicitly preserves modern selfdrived health/model/GPS/safety
checks and manager predicates; C2 suppression/joystick enabled-state toggle/UI
restart shortcut not copied. C2 custom relay buttons, PID hot reload/physical
gains and safety enum26 are not qualified modern runtime features. Offline
controller/relay capability remains distinct from missing live qualification.
NEOS/legacy build fixes and inherited2022Thneed work do not replace current
Linux, UV, model or camera integration. No owner settings/PC/game changes.

Validation:15USB/adapter +45RetroPilot +53CAN +303broader car tests pass
(314existing subtest skips), history82path verification and Ruff pass. Tests
cover literal layout/historical health, fake USB allowlist/disconnect/cleanup,
real Cereal -> CarState -> controller candidates and actual zero output. No
real IPC publisher/manager/game/CAN/device timing or physical/MCU safety test.
Receipt/logs: Ai/Evidence/retropilot-history-adaptation-20261103.json; angle
receipt and sysfs identity receipt alongside it. All code/tests/evidence are
in the project; child/parent commits local/unpushed. Maintenance validation
must attach to actual increment commits. Both notebooks updated.

Skills: source-driven-development, planning/task breakdown, interface design,
incremental/TDD, Git, code review and REA skill with source-first routing.
Existing teacher modern-port plan/owner implementation request supplied scope;
no unrelated skill approval gate, hardware activation or deployment performed.
Inbox0related pending/8historical failed-or-blocked validations retained.

Exact next step: identify the actual Chimera normal-mode device, pin its
installed version/signature and collect receive-only bus/health data with this
adapter. Then qualify units/profile/source ages and missing gear/wheel/motion/
driver-input contract; integrate truthful board health/ignition and exclusive
manager lifecycle/reconnect. Shadow/game-only loop and measured actuation/MCU
safety remain separate. Do not promote raw safety17, C2 constants or source/
offline results to modern safety enforcement or tested integrated driving.

## File-list clarification, 2026-11-03

Owner asked which files changed. Verified clean Git against parent35d46c1→d3cd298
and child9da9210→86a839d: latest adaptation adds runtime chimera.py and
chimera_protocol.py, modifies carstate.py/values.py, and adds/modifies4tests.
Package README, docs/RETROPILOT.md, submodule pin and Ai evidence/notebooks also
changed. profiles.py/fingerprints.py/commands.py/carcontroller.py belong to
preceding increments and were unchanged in this latest adaptation. Read-only
Git inspection; no runtime/hardware changes or new behavioral tests.

## Plain-English/DBC clarification, 2026-11-03

Owner says they are unfamiliar with coding and use vibe coding. Prefer plain
English: explain observable capabilities/completion limits before file/API
names, and avoid implying offline tests establish a working control loop.
Rechecked packaged opendbc_repo/opendbc/dbc/ocelot_controls.dbc against the
canonical retropilot/dbc copy: both SHA256ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
DBC is included and used by the port; actual Chimera acceptance, managed
integration, BeamNG loop, calibration and MCU safety remain pending. No runtime
code/device change or new behavioral test in this clarification.

## Outside-car-folder and Panda clarification, 2026-11-03

Owner asked whether DBC/car folder suffice and whether Panda changed. Read-only
Git comparison from modern opendbcbaseaa9bff6 confirms additional edits to
can/dbc.py, car/values.py, car/car_helpers.py, car/fingerprints.py and
torque_data/override.toml. New host receive files are in
openpilot/selfdrive/pandad/chimera.py and chimera_protocol.py, plus tests.
Parent diff from pre-portdd29f00 confirms no panda/ gitlink or .gitmodules
change for this port. Panda reference/safety comparison JSON is evidence,
not edited/deployed board firmware. Existing stock pandad remains unchanged;
new standalone Chimera receiver is not managed/live actuation integration.
No board flash or new hardware action; tests not rerun for this explanation.

## 2026-11-03 — Complete plain-English 2025 C2 commit list

Owner asked to see all the C2 author's work during the year. Added
Ai/Reports/retropilot-c2-history-20261103/2025_COMMITS.md: 53 individually linked
2025 commits (28 application, 20 CAN library/DBC, 2 Panda, 3 Cereal), with
original titles and plain-English patch explanations. Dates span February 6–
August 14; application May 15–August 14. The compared history also contains
30 older 2021/2022 commits, including inherited/other-author work. This is the
2025 portion of the four pinned comparisons, not every branch/repository ever
used by the author. Fresh GitHub C2 branch still b9a942efd3cb210127bb5efb5cf9ccf6a811c728.
Fetched all20 individual 2025 opendbc patches through GitHub and retained
opendbc-2025-commits.json (SHA25630b35ad500ded5c465e4331f26aef11b67825ba2a3c9f1d488fe86d0fde23535).
53 unique repo/commit links and the20 patch SHAs match comparison records;
history verifier and notebook/link verifier pass. Documentation/Git skills and
source-first history inspection; no new REA artifact question or runtime test.
Author's July16 "op drives" title remains an author report, not our measured
result. No runtime/DBC/firmware/device changes; live commands stay disabled.
Next remains actual Chimera receive acceptance and units/profile/managed
health/ignition qualification. No upstream integration; inbox0related pending.

## 2026-11-03 — Six-folder C2 integration clarification

Owner highlighted cereal/opendbc/panda/selfdrive/third_party/tools. Inspected
pinned parent patches and complete Cereal/Panda final comparisons; expanded
history report with all six roles and current Radxa implications. third_party
changes are json11 C++ compatibility and PIC libyuv build/x64 archive-reference
updates, not CAN support; binary archive contents not analyzed. tools changes
are threaded gamepad input, five buttons and20Hz publication with an offroad
restriction removed; not a BeamNG implementation. selfdrive also modifies
controlsd engagement/relay/events, inactive PID JSON reload, manager UI restart,
FFmpeg/replay/build and NEOS. boardd changes are header/build compatibility,
not a demonstrated Chimera mailbox adaptation. Cereal relay field is8bits;
canonical wire relay field remains16bits. Old safety/event bypasses remain
unqualified; no runtime/DBC/firmware/device change or new behavioral tests.
Sources remain applicationb9a942e, Cereal a7193d0, Panda9e6d47f, opendbc6b90fafe.
Documentation/source-first skills; no new REA artifact question. Next actual
Chimera receive acceptance/units/profile/managed health remains unchanged.
Validation: history35parent/82path coverage, notebook79docs/236relative links
and whitespace pass. Documentation-only clarification; no new runtime test.

## 2026-11-03 — Owner corrected the C2 research framing

Accepted scope: RetroPilot working on existing Radxa Q8B/current Sunnypilot;
Chimera CAN and intended BeamNG environment. Owner asked to inspect C2 folders
to understand behavior/requirements, not reproduce its old integration or add
all historical changes. Earlier wording implying that all six integration
areas must be recreated was too broad. Current APIs and existing capabilities
determine the minimum necessary implementation. Updated report/plan, student
topic/handoff and central repo/resume to make that explicit.

Source pins unchanged: parent 855bc09fab42d24a0d405a39ca71ce02692ea379;
opendbc 86a839dcec8ed9a3e45315eac804fa1001f1b2d6; reference C2 b9a942e,
opendbc 6b90fafe, Panda 9e6d47f, Cereal a7193d0. No runtime, DBC, settings,
firmware or device changes. Documentation/Git skills; no REA runtime/artifact
question in this clarification. No new behavioral tests. Actual Chimera
receive acceptance and modern lifecycle/health/data contracts remain next.
Upstream inbox has zero related pending commits; no upstream integration.
Validation: notebook verifier passes 79 documents/236 relative links;
whitespace check passes. This increment records scope only.

## 2026-11-03 — Actual changes outside RetroPilot clarified

Rechecked parent diff dd29f00..2304f5a and opendbc aa9bff6f..86a839d.
Outside car/retropilot: can/dbc.py, car/values.py, car/car_helpers.py,
car/fingerprints.py, car/torque_data/override.toml and packaged canonical DBC;
parent adds standalone pandad/chimera.py and chimera_protocol.py, tests and
documentation. Panda firmware/gitlink and .gitmodules unchanged for this port;
no Cereal/third_party/existing manager/controlsd edits in this comparison.
Host pandad files are distinct from Panda firmware. Recent clarification
turns change notes only. No new runtime test/device action; modern Radxa scope
and next Chimera receive acceptance remain unchanged. Source/Git inspection.

## 2026-11-03 — Current Cereal location clarified

At parent 15b39ed344179febf8808322fa8bf9a104cf4443, Cereal exists as the
regular project directory openpilot/cereal/, not a root cereal/ submodule.
README defines its messaging role; messaging/__init__.py uses msgq. Vehicle
schema is opendbc_repo/opendbc/car/car.capnp, loaded by car/structs.py;
openpilot/cereal/__init__.py loads log/custom with opendbc imports. Chimera
optional publisher imports existing openpilot.cereal.messaging and PubMaster
can, without schema modifications. Read-only source/filesystem check only;
no new runtime test. Modern Radxa scope/next task unchanged.

## 2026-11-03 — Chimera held; C2 Cereal reasons explained

Owner explicitly said hold Chimera for now. Do not advance Chimera code,
acceptance or hardware work until resumed. Current discussion stays on
RetroPilot/current messaging needs. Rechecked pinned Cereal comparison:
7406e44f fixes Ubuntu24 messaging/VisionIPC compiler compatibility;
58bc67b1 adds retropilot safety enum26 in then-Cereal car.capnp;
a7193d0f adds CarControl.bodycontrol.relayCoreCMD UInt8 for eight relay bits.
Those were specific C2 build/interface requirements, not a universal car-port
checklist. Existing current CAN receive path needs no Cereal schema change;
future end-to-end relay/safety requirements must be checked against current
vehicle schema in opendbc/car/car.capnp. No claim all future features already
fit existing fields. Runtime/source/DBC/firmware unchanged; no device actions.
Parent source checked at79b96e4; child remains86a839d. Documentation/Git skills,
source-first saved patches; no new REA artifact/runtime question or tests.

## 2026-11-03 — Relay exclusion and safety-mode explanation

Owner explicitly does not want relays; preserve reference/offline code but add
no relay integration. Chimera remains held. Explained C2 enum26 -> car interface
safetyConfigs -> board registered retropilot_hooks; identifier alone supplies no
rules. Rechecked current host PandaSafety and Panda::set_safety_model(0xdc),
board mode selection/transmit hook, opendbc safety registry/defaults and current
RetroPilot interface. Current schema26=hongqi, firmware26=SAFETY_FAW, occupied.
Current RetroPilot still dashcamOnly/noOutput; no active policy implemented.
Saved explanation in docs/RETROPILOT.md. Source-only, not installed enforcement;
no board/firmware/mode changes. Source pins parent18054f2/child86a839d;
C2b9a942e/Panda9e6d47f/Cereala7193d0. Skills: source-first/docs/Git; no new REA
artifact question or behavioral tests. Next discussion is modern safety needs;
no Chimera or relay work authorized by this explanation.

## 2026-11-03 — Cereal change requirement checked against actual bindings

Owner asked for verification, not implementation. At parent0e550c7/child86a839d,
openpilot/cereal/log.capnp imports /car.capnp, and cereal/__init__.py supplies
the opendbc/car schema import directory. The safety enum lives in modern
opendbc/car/car.capnp. Therefore adding a future safety identifier belongs
there; no duplicate enum/direct Cereal schema edit is required for that name.
This does not mean active RetroPilot needs no changes: no retropilot enum or
registered safety policy exists yet;26=hongqi/SAFETY_FAW and current noOutput
must not be relabelled as active support.

Ran actual current venv bindings without hardware: constructed RetroPilot
CarParams via get_params(CAR.RETROPILOT_RETROFIT, gen_empty_fingerprint(), [],
False, False, False); asserted noOutput/dashcamOnly, serialized into existing
Cereal log.Event.carParams and decoded it; assertions PASS. Also asserted
absence of retropilot safety enum and hongqi=26. Initial ad hoc probe used an
obsolete experimental_long keyword and raised TypeError; inspected the actual
API and corrected that invocation. No product failure or source modification.
Read-only Git diff confirms Cereal untouched since pre-port dd29f00.
Chimera remains held; relays excluded. Documentation/source-first/Git workflow;
no new REA artifact/runtime question. Hardware enforcement remains untested.
