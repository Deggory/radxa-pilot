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
