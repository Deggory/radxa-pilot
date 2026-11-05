## 2026-11-05 — Wiki car CAN connection is CAN2

Official Chimera wiki Installation,checked November5,explicitly routes vehicle
CANH/CANL to Chimera CAN2. Local can.h maps hostbus2 to MCUCAN3. OBD-C is described
for comma devices; the page does not specify car-side OBD connector pins or
vehicle-specific signal availability. QA-20261105-10 saves the owner’s question
and answer. No wiring/device/source action; actual connector still needs checking.

## 2026-11-05 — Direct Ocelot Chimera source review

Owner asked to inspect inside ocelot. Local HEADd87892fa,pre-existing dirty
Chimera main.c/chimera.h; selected byte hashes/status in student evidence receipt.

- firmware/chimera/main.c: USB mailbox endpoint,health/config/sensor extraction,
  IRQs,TIM3generated messages and main startup. CAN1/2/3RX handlers all call
  can_rx(0/1/2); main.c560queues CAN3raw receive after inspecting configured signals.
- firmware/chimera/can.h: can_rx tags bus and pushes raw mailbox to can_rx_q;
  main.c174–183drains it to endpoint0x81. Raw receive is independent of valid
  signal mappings. Empty configuration alone is not a zero-raw-frame explanation.
- firmware/SConscript selects STM32F413/Cortex-M4/GATEWAY. board.h selects
  board_gateway; boards/gateway.h gateway_init enables all3transceivers and
  normal pin modes. Enable outputs are active-low PC1/PC13/PA0. This proves
  source intent, not actual board rails,GPIO levels or installed-nightly behavior.
- Startup500kbit/s/non-silent is explicit; maskFFis used by reinitialization.
  get_health_pkt hardcodes voltage/current0and safety17; these are not power
  measurements or a negotiated/enforced modern safety profile. TX has no
  safety_tx_hook;0xDCchanges relay_req_usb. No reviewed path installs modern safety.
- Current SYS_CFG speed fields are not consumed at startup; runtime0xDEonly bus0.
  Configured CAN extraction is on MCUCAN3, with existing integer scale/endian/RPM
  limitations already in the hardware guide. Configured extraction and raw RX
  are distinct paths. can_init initializes ret=false,so its reported result is
  alwaysfalse even though &=evaluates both operations; startup uses llcan directly.
- Core Config default launcher uses offline site/WebKit plus read-only native
  bridge; guarded Tk app remains separate. usb_transport.py266–277returns empty
  on libusb timeout without retaining partial actual bytes. Modern Sunnypilot
  ChimeraReceiver retains USBErrorTimeout.received. Desktop limitation is source
  evidence, not root cause of November4modern-reader zero-frame captures.
- hardware/chimera contains photo/guide only; ocelot-gateway schematic/BOM/layout
  describe a separately named reference. No exact Chimera schematic/power tree
  found. Do not conclude USB-only transceiver supply sufficiency from these files.
- Saved nightly ZIP matches SHA8158f291; its Chimera27976-byte signed member
  matches SHAe35df778. Exactde193215Git object is absent locally. Patched public
  main and float-layout candidates remain distinct, with recorded failed float
  boot/original-nightly restore. No new image readback or binary analysis.
- test_relay_chimera.py is active: safetyTOYOTArequest plus repeated heartbeat.
  It was read, not executed. Legacy Python exposes writes/config/flash APIs;
  do not import/run scripts as a passive test merely because named test.

Read-only investigation only. No Ocelot source edit/build/device action. Existing
source-driven/documentation/Git skills and REA source-first routing reused; no new
REA artifact result needed. QA-20261105-09 retains answer, versions and limits.
Next actual installed behavior/physical receive qualification, noOutput retained.

## 2026-11-05 — Teacher-first Chimera reconciliation

Owner resumed Chimera knowledge/receive work. Fresh lsusb/sysfs shows bbaa:ddcc,
RetroPilot Chimera, serial3a0044001651333038373636,bus3/device6. No USB handle was
opened; de193215/health43/signature/configuration are historical observations.
Current parent9376a7f3/child150f9371 have the standalone receive-only bridge;
managed health/ignition/reconnect integration and MCU enforcement remain open.
The active safety header does not supply a production profile or install itself
into Chimera. Genuine492/492game replay and117submitted/0received wire results
are separate November4 evidence. Canonical RP-SIM-1 DBC SHA256b4079670 remains.

Dated correction to the November4silent-mode lead: local can.h declares maskFF,
but main.c1134–1151 explicitly initializes CAN1/2/3 at5000 with loopback=false,
silent=false. can_set_speed uses the mask on later reinitialization. No conclusion
about installed-nightly silent state or cause of zero frames follows. Ocelot
reference is now HEADd87892fa with pre-existing dirty Chimera sources; byte hashes
are saved in the student evidence receipt, not labelled as exact installed source.

Older hardware guide says empty config; October4isolated-recovery evidence later
restored the original nightly and verified watchdog-off SYS_CFG across reset and
a second write. Full776-byte readback passed then; signal writes/watchdog-on write
safety remain unqualified. Do not infer current config without a fresh read.
Owner’s CAN3/USB-only/removed-resistor reports remain saved facts, not measurements
of connector label, powered transceivers or termination. Pin2CANH/3CANL/4GND and
CAN0/1/2roles were rechecked against official wiki November5; wiki’s broad Panda
API compatibility claim does not resolve modern mailbox/health/safety differences.
TI SLAAET4A sections5.1/5.3 confirms ACK, matched bitrate and endpoint termination
requirements generally; it does not identify this bench’s fault.

Next establish actual connector/wiring, termination/transceiver supplies, bitrate
and ACK, then bounded genuine telemetry receive before managed passive integration.
No flash/config/output/relay change or physical test today. Source-first,Git and
documentation skills used; historical REA evidence reused with its source limits,
no new REA binary claim. QA-20261105-08 and dated session retain the answer.

2026-11-04: additional explicit receive-only RETROPILOT_BEAMNG profile reads RP-SIM-1 telemetry and uses centi-km/h; generic physical RETROPILOT_RETROFIT stays unchanged. Canonical DBC adds8simulator-only messages, preserving all20legacy layouts. [Contract](../../openpilot/tools/sim/beamng/shared/CAN_CONTRACT.md). No controller output or firmware change.

## 2026-11-04 — OEM CAN plus RetroPilot through separate DBC parsers

Owner asked whether connecting the car CAN bus can supply data while keeping
RetroPilot DBC. Yes as supported architecture, not current implementation:
CarInterfaceBase stores a dictionary of CANParser instances, updates every
parser from received packets and passes all to CarState. Each CANParser owns
its DBC and filters numeric source bus. Existing Honda HAS_BSM code combines
Bus.pt honda_civic_hatchback_ex_2017_can_generated with Bus.body
honda_crv_ex_2017_body_generated in an actual platform configuration.

Proposed use only:OEM DBC decodes available vehicle speed/brake/gear/RPM/etc;
canonical ocelot_controls decodes ZSS/module feedback. CarState explicitly
chooses authoritative signals and combines them, including source-specific
units, CRC/counter/freshness and readiness checks. Same physical bus is possible
for distinct compatible IDs; conflicting ID meanings require separate bus
routing or explicit translation. Preserve OEM definitions and canonical DBC.
No new bus number/wiring or adapter capability is inferred from this discussion.

Current RetroPilot CarState returns one parser on hostbus2 and still expects
its base RetroPilot ENGINE/SPEED/CRUISE/angle messages. A real OEM addition
needs a second parser, mapping/required-source changes and a sourced car DBC.
Two files placed in a directory do not implement that integration. No vehicle
selection, OEM port, hardware connection, CAN TX or control permission here.
Live receive-only/noOutput and prior holds remain. Source child671f8c4,
application40a0c9f8 unchanged; documentation-only review, no runtime test.
Source references:opendbc/car/interfaces.py114,263-271;can/parser.py114,215;
honda/carstate.py240-246;honda/values.py233;retropilot/carstate.py134-137.
Documentation/Git skills, readable-source REA route; no binary analysis needed.

## 2026-11-04 — dzid stepper commands and separate ZSS feedback

Owner asked whether our DBC includes dzid stepper control and ZSS angle.
Yes at the definition level:STEERING_COMMAND_SSC0x22E/DLC5 requests
angle/torque/mode;STEERING_STATUS_SSC0x22F/DLC8 reports motor encoder
angle/speed,torque estimate,module temperature,control/debug state.
STEER_ANGLE_SENSOR0x50/DLC6 is separate calibrated steering-wheel feedback
from the updated ZSS v0.2.0 AS5047P/ADMT4000 code. Original smartZSS0x23
is a different format. Motor encoder angle is not automatically wheel angle.

Fresh source comparison:both SSC messages match retained dzid dependency DBC
fields(bit positions,width,endian,sign,scale/offset,DLC). dzid source main
782676bc4cd8f0ae578a73835e0a778b7e63f162 BSP/can.c instead uses additive
CAN-ID checksum; canonical host uses CRC8J1850. Generic actuator0x12E/0x12F
is another message pair. Current commands.py has an SSC builder, while
ControllerProfile excludes STEER_SSC and live interface stays noOutput.
No ready-to-connect dzid or owner-board/installed-firmware match is claimed.
Checksum/mode/limits/override/controller integration and calibration remain.

Fresh zss/common/scripts/check_dbc.py passes0x50/DLC6 field/hash check;
shared encoder implements matching CRC/layout. Defaults remain uncalibrated,
not a measured/live angle source. Canonical/package hash unchangedef6eef74.
This clarification makes no new actuator/axis selection and does not replace
prior Toyota0x25 feedback choices in separate actuator/brake projects.
No hardware access, firmware edit/build/flash, motor output or source changes.
Documentation/source-first skill workflow; no unrelated REA binary analysis.

## 2026-11-04 — What the shared DBC can describe

Owner requested a plain-English inventory, not a protocol or hardware change.
Canonical and packaged ocelot_controls.dbc remain identical,7363bytes,
SHA256ef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
Source parent40a0c9f8/child671f8c4. Direct source inventory:20messages,
120signals total;12sensor/status messages and8command messages. Repeated
checksum/counter/state/mode fields count toward120; these are not120sensors.

| Incoming source | Data defined |
| --- | --- |
| Angle sensor | Steering angle, unsigned speed magnitude, sensor state. |
| ENGINE | CAN RPM, crank pulse timing/count, ignition, brake switch, mode. |
| SPEED | CAN speed, vehicle-speed pulse timing/count, mode. |
| CRUISE | On/off, cancel, set/down, resume/up, two raw ADC channels, mode. |
| Gas interceptor | Two pedal sensor channels and state. |
| Gas actuator | Throttle position, VSS, VSS encoder and state. |
| Steering interceptor | Two sensor channels, driver override and state. |
| Steering actuator | Driver/EPS torque, steering OK and status. |
| Brake actuator | Pedal position(mm), driver-brake/applied flags, brake OK/status/extended states. |
| Optional legacy iBooster | Corresponding brake position/applied/health/extended status. |
| Optional legacy SSC | Steering angle/speed/torque, steering-module temperature, control/debug states. |
| Legacy relay | Relay status/state only; owner excludes relays from the project. |

All messages also define counters/checksums. Outgoing definitions cover gas
(two channels/enable), steering(two channels or angle/torque/mode), brake
(position/relative/mode), and legacy excluded relay commands. These definitions
are not enabled live actuation. DBC is a wire dictionary, not a sensor or
producer. Hardware or a future BeamNG adapter must supply compatible frames.

Current CarState consumes selected base/module fields, with freshness/health
checks. It does not publish every DBC signal into standard CarState:engine
RPM and calibrated pedal values are not mapped; interceptor channels are not
qualified Nm; STEER_RATE is unsigned and not copied to signed CarState rate.
Speed scale defaults0 until a producer is qualified. Optional modules depend
on detected flags, not an assumption that all legacy hardware is fitted.
No gear, separate wheel speeds, actual cruise-enabled/set speed, seatbelt,
doors, indicators, fuel/battery level, GPS/IMU or radar tracks in this DBC.
Live port remains noOutput/dashcamOnly. Chimera/hardware holds stay in force.

[Exact message/signal inventory](../Evidence/retropilot-dbc-inventory-20261104.json).
Checked readable DBC, current CarState/interface/values and canonical publisher
notes; no native/runtime or physical CAN test. Documentation/Git skills with
source-first REA routing, no unrelated binary analysis. No DBC/source change.

## 2026-11-04 — Owner-selected required hardware: all three modules

Owner explicitly selected these as required parts of our existing Radxa Q8B /
modern Sunnypilot RetroPilot project and requested both notebooks remember them:

| Required part | Owner-selected job |
| --- | --- |
| Chimera | Connects the computer to CAN and gathers vehicle signals. |
| Interceptor Core | Handles analog accelerator or steering torque-sensor signals. |
| Actuator Core | Controls motors used in custom actuators. |

All three belong to the intended architecture. Do not reduce this selection to
Chimera alone, treat the two Cores merely as examples, or ask the owner to repeat
which three were selected. This is an owner requirement, not proof of purchase,
installed hardware, working firmware, exact per-axis assignments or calibration.

Recording the architecture does not resume held Chimera implementation or the
paused physical Interceptor bench task. Relays remain excluded. No iBooster or
other module is additionally selected by this table. Current noOutput, absent
active vehicle profile and zero runtime CAN remain. Canonical shared
ocelot_controls.dbc remains selected; no rename, wire change or device action.
Exact endpoint/axis mapping and qualification remain future integration work.

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

## 2026-11-04 — What Ocelot means in the C2 RetroPilot port

Ocelot is RetroPilot's firmware/hardware family for automotive gateways and
control modules, per local ocelot/README.md. It includes Chimera, Interceptor
Core, Actuator Core and iBooster firmware; naming support is not proof every
module was fitted to the author's vehicle. C2 ocelotcan.py constructs commands
using ocelot_controls.dbc; its controller calls the appropriate constructors
according to DetectedEcus. It is host CAN encoding, not board firmware.

Modern Sunnypilot packages the same canonical DBC and uses commands.py for
these constructors. Ocelot board firmware executes on the selected modules;
the external ocelot/ directory is a separate reference/project, not a folder
to copy wholesale into the car port. Producer CRC/layout/units compatibility
still needs qualification. NoOutput/zero live CAN, absent active profile,
held Chimera/physical Interceptor and excluded relay integration remain.

Sources: retained C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728, canonical DBC
6b90fafe59e81822bfae58e4ecb080248e9de40d, local Ocelotd87892fa dirty source.
Current parentec53967/child671f8c4 clean at session start. Source-only explanation;
no runtime/firmware/device test or code change. Next active work still needs
actual BeamNG vehicle/configuration and endpoint/units/mode/calibration contract.

## 2026-11-03 — Audit saved before owner-requested shutdown

Audited parent469f3c5/child671f8c4, both clean at start;10 source hashes match.
Fresh168 tests pass:50 safety,45 port,53 CAN,20 offline adapter/migration; Ruff
passes. Prior full safety8806/932 skips belongs to unchanged source, not a new
shutdown run. Modern port/shared registrations and two-header safety split are
saved in the audit report. Production noOutput/zero CAN, missing real profile,
held Chimera/Interceptor and excluded relays remain explicit. No device action.
Next after boot: read both handoffs/inbox, verify Git, resolve actual BeamNG car/
configuration and endpoint/units/mode/driver/calibration contract. No automatic
active output or hardware resumption. Owner requests normal local Radxa shutdown
only after all saves/validation; queue/readback is central shutdown receipt.
Report: Ai/Reports/retropilot-shutdown-audit-20261103/README.md.

## 2026-11-03 — RetroPilot active safety software engine, no live profile

Child opendbc671f8c450fc74f5b8b90b2ee53124394108651ce adds profile-dependent
sensor integrity/freshness, fault-latched engagement, driver intervention and
bounded/rate-limited interceptor steering/gas/iBooster-position checks. Only
an artificial native-test fixture supplies limits; no production initializer or
firmware parameter selects an active profile. Normal mode39 remains disabled-
command-only; interface noOutput/dashcamOnly and zero runtime CAN remain.
50 focused tests pass; full native suite8806 run/932 existing skips/no failures;
45 RetroPilot host tests, release-fixture absence, Ruff and whitespace pass.
Independent review required recovery/counter/health/startup fixes; all addressed,
final no Critical/Required findings. Startup models a full16-count disable
cycle peraxis; this is not receipt acknowledgement or installed-firmware proof.
Chimera and physical Interceptor held; relays excluded; no device/game/CAN action.

Owner asked which car Caleb used: pinned5435d674 launch says user spawns a car;
README has Ibishu Covet example and ETK800 rack examples. HONDA_CIVIC_2022 was
CAN/platform identity, newer BEAMPILOT measures the selected car. Owner's actual
vehicle/configuration remains unknown. Next: qualify selected game vehicle,
endpoint/units/mode/driver/calibration contract and then game-only integration.
No production limits inferred from C2 constants, DBC ranges or a demo model.
Report: Ai/Reports/retropilot-active-safety-20261103/README.md; source/test hashes
and remaining firmware/profile limits in the matching evidence JSON.

## 2026-11-03 — RetroPilot restricted safety mode implemented

Modern opendbc a6099a1e141f17ec18ca9b065cf9a8f972e0cac8 registers local
RetroPilot safety ID 39 and a disabled-command-only C policy. Seven canonical
steering/gas/brake disable packets are checked on bus 2; active commands,
relays, malformed frames, unknown parameters and forwarding are blocked.
The interface stays noOutput/dashcamOnly and controller runtime sends no CAN.
21 focused and 8777 full safety tests pass (932 existing skips); 45 RetroPilot,
53 CAN and 303 broader car checks pass (314 broader skips). New policy has
24/24 executable lines covered; debug/release C and Cereal C++ builds pass.
No Cereal source/DBC/model/firmware changes. Chimera is held; relays excluded.
Active policy limits, RX health/freshness and engagement remain unqualified.
Next: qualify those software/vehicle requirements without resuming held hardware.
Evidence: Ai/Evidence/retropilot-safety-20261103.json and report under
Ai/Reports/retropilot-safety-20261103/. This supersedes older "no policy file"
notes, not the remaining active-control limitations.

2026-11-03 owner scope: relay features are not wanted. Current discussion is
RetroPilot safety-mode selection and enforcement. Chimera work remains on hold.
Preserve existing offline reference code; do not add relay integration.

2026-11-03 owner direction: **Chimera work is on hold until the owner resumes it.**
Current discussion is the need for modern RetroPilot messages and why C2 changed
Cereal. Earlier next-step notes about Chimera acceptance are deferred.

## 2026-11-03 — Owner clarification: modern RetroPilot implementation

The objective is to make RetroPilot work on the existing Radxa Q8B running
current Sunnypilot, with Chimera providing the CAN interface and BeamNG as
the intended initial vehicle environment. C2 is a behavioral/protocol reference.
The owner requested examination of cereal, opendbc, panda, selfdrive,
third_party and tools to understand what the author achieved and why.
Those folders and commits are research inputs, not an implementation checklist.

Identify the required RetroPilot behavior and CAN/hardware contracts, then
implement only the missing pieces through current Sunnypilot APIs. Reuse
existing modern capabilities. Do not recreate the C2 integration or require
matching edits in every old folder. Old build fixes, schemas, engagement
shortcuts and tuning machinery are not requirements merely because C2 used
them. Evaluate any proposed change against the current Radxa goal and evidence.

This clarification changes the framing, not the tested runtime status. No
runtime code was changed for this clarification. Next remains actual Chimera
receive acceptance, then current board health/lifecycle and vehicle-data
contracts. Historical review is supporting evidence, not live validation.

## 2026-11-03 — 2025 commit guide

[Plain-English commit guide](../Reports/retropilot-c2-history-20261103/2025_COMMITS.md) covers all53dated2025commits in the
reviewed four-repository comparisons: application28, opendbc20, Panda2,
Cereal3; February6–August14.30older inherited/other-author commits remain
separate. All20individual2025opendbc patches retained and SHAs checked.
C2 branch freshly rechecked at b9a942efd3cb210127bb5efb5cf9ccf6a811c728.
This is history evidence, not proof of completed safety or our live control.

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

## 2026-11-03 — C2 controller migrated to modern offline replay

Owner requested implementation after comparing the small modern controller
with the linked C2 directory. Accepted increment: migrate portable control
calculation and provide parser-to-controller offline replay; preserve the
independent zero-live-output boundary until Chimera safety/profile qualification.
The previous11-line controller was a passive placeholder, not a completed
active migration. No physical/game actuation is qualified by this increment.

Fetched linked GitHub directory and c2 branch through the connected GitHub
plugin. Branch resolves to b9a942efd3cb210127bb5efb5cf9ccf6a811c728; all8retained
file Git blobs match. Read every C2 file and current interfaces/schema/parser.
Immutable teacher retropilot source and canonical DBC bytes were not edited.

Implemented modern normalized torque to two-channel steering, bounded speed
taper, asymmetric slew and zero-before-direction-change; separate lat/long
activation, gas/brake scaling and mutual exclusion;100Hz steering/brake and50Hz
gas/relay with immediate disable flush, per-message counters/CRC/hostbus2.
Preview reports held gas between sends. Nonfinite inputs, overrides, faults,
missing selected endpoints, ignition loss, non-monotonic steps/gaps over50ms
and stale accepted state disable candidates.100ms offline age uses the oldest
accepted tracked CAN arrival, not parser update time; empty/bad-CRC/unrelated
traffic cannot refresh it. Arrival age is not source acquisition age.

profiles.py validates immutable explicit calibration; default profile absent.
C2_REFERENCE is deliberately offline/unqualified (1510center,350counts, author
pedal slopes,7mm brake, implicit1m/s²-to-full-pedal slope).350counts yields700
channel difference versus local Core400check. No calibrated measured-torque
feedback limiter or driver-pedal authority is claimed. SSC/motor steering has
codecs but no selected normalized mapping. Zero live tunes/placeholder geometry,
unknown gear and no fake cruise engagement remain. C2 radar forcibly disabled;
no unused Toyota radar parser copied. docs/RETROPILOT.md maps all8C2files.

replay.py consumes timestamped canonical CAN hex and modern CarControl JSONL,
records candidate frames/actuators, actual zero feedback and empty transmitted
CAN. No USB/CAN device is opened. update() never forwards candidates, even with
mutated dashcamOnly. No allOutput, firmware flash, manager/game/model launch,
persistent owner setting, remote PC action or upstream integration performed.

Source: parentbase796059f3457315877ba8d42890d29d0a76ea131b; modern opendbc
baseaa9bff6f5442cef8cb8e25e143ef38865c276ce8, prior04a78352a9605a0e07342146fe8481b7d92ee7fd,
new9da9210adfa4dc213424f36945caccd40182c80d on radxa/retropilot. Canonical
DBC6b90fafe/SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce;
CD210/OpenCL/Thneed eb741641 unchanged. Historical Chimera de193215 observation
is not a current installed-image pin. Child/parent increments remain unpushed.

Validation:44RetroPilot tests,53CAN tests and303broader car tests pass
(314existing subtest skips), Ruff/whitespace pass. RED missing profile import
and expanded controller failures reproduced before implementation. Integration
tests exercise real CANParser -> CarState -> modern apply -> candidate CAN,
including bad CRC/staleness and unconditional zero actual output. CLI help and
notebook verification pass; no real-time/game/physical/MCU-safety test.
Receipt/logs: sunnypilot/Ai/Evidence/retropilot-controller-20261103.json.

Skills used: source-driven-development, interface design, TDD, incremental
implementation, Git and code-review-and-quality, with source-first routing.
Readable-source and offline execution evidence; no REA binary question/result.
Inbox: upstreama86979d2 unchanged,0related pending,8historical failed/blocked
records retained. No new owner question required for this code increment.

Next: implement the receive-only Chimera backend against its actual installed
USB/health format; qualify producer units, selected game/actuator/driver-input
profile and canonical telemetry gaps. Then shadow/game-only loop and enforced
MCU safety/limits before any live physical output. Do not promote C2 constants
or an offline preview to a tested Sunnypilot/Chimera integration.

# RetroPilot car platform — current implementation

## 2026-11-03 — RetroPilot car port implemented, receive-only

Owner explicitly requested RetroPilot as the car and Chimera as Panda. Modern
RETROPILOT_RETROFIT now registers in opendbc; canonical DBC/CRC/counters,
state/module parsing, button/override/stale handling and all8offline command
IDs implemented. Explicit selection suppresses OEM VIN/FW probes. Hostbus2;
no global car override, forced CAN validity or fake wheels/gear/torque.
Default speed scale0 marks sensors invalid; legacy km/h vs local Hall centi-km/h
must be qualified explicitly. CarController is unconditionally passive;
dashcamOnly/noOutput and placeholder geometry/tune do not establish control.

Submodule branch radxa/retropilot: codec eb64a22, platform649bbb6
(full649bbb632a020f155fc1eb16ae343f49a5c4bb50), baseaa9bff6f; parentbase dd29f00.
53CAN+22port tests pass;303broader car tests pass (314existing subtest skips),
490lateral-limit tests pass (31existing skips), Ruff/whitespace pass.
Compiled original CRC matches1600vectors across20canonical messages.
No devices/game/model/manager/firmware/CAN TX or actuation tested or enabled.
Next: receive-only Chimera backend + actual producer units/frames/hostbus2,
then full BeamNG telemetry/motion contract and optical shadow. Actual actuator
profile, live safety and endpoint calibration remain open. No owner question
needed to complete this code stage. Detailed topic/session/receipts below.

Guide: [RetroPilot](../../docs/RETROPILOT.md).
Code: [package](../../opendbc_repo/opendbc/car/retropilot/README.md).
Validation: [receipt](../Evidence/retropilot-port-20261103.json),
[native CRC](../Evidence/retropilot-native-crc-20261103.json).

Accepted scope: modern car platform and offline canonical codecs, using the
teacher C2 migration plan. Chimera remains the intended Panda-role device;
its backend, installed firmware safety and board health are not supplied or
fabricated by a car package. Normal CAN parser validity/timeouts retained.

Sources: C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728, canonical
RetroPilot/opendbc6b90fafe59e81822bfae58e4ecb080248e9de40d,
DBC SHAef6eef74021a00183729b53ba90f1c790792cfe5dcf72fe9bdfe2dcb3d6a5dce.
Packaged DBC bytes unchanged; checksum test enforces this pin. Current target
opendbc baseaa9bff6f5442cef8cb8e25e143ef38865c276ce8. Panda8a16e089 unchanged;
CD210/OpenCL GPU eb741641 retained, no new model/camera test. Historical
Chimera de193215/43-byte health observation stays historical; no USB opened.

Teacher source recovered a new implementation-critical discrepancy: saved
ocelot/firmware/chimera/main.c Hall speed computes kph*100, while C2 CarState
uses raw kph. SPEED.MODE uses a different config index in that source; it does
not establish a reliable units selector. CP.wheelSpeedFactor defaults0, and only
explicit1.0/0.01 scales qualify an isolated replay after producer confirmation.
Canonical unsigned steering-rate magnitude stays raw rather than pretending
it is signed rate. Gear/wheels/cruise-enabled/set-speed remain unavailable.
Actual Interceptor differential torque calibration and SSC status semantics
remain unknown. Optional module flags require exact bus/ID/DLC, are per-instance
observations, and never grant active capabilities.

The minimum platform geometry2.7m/ratio13 and 1m/s² bound are explicitly
non-driving computational placeholders; no actual vehicle has been tuned.
No active requests are encoded by CarController even if caller flags mutate.
Offline commands require endpoint targets, bus and counter; bit limits are not
physical actuator limits. Invalid/nonfinite values cannot silently wrap.

Changed owning subsystems: opendbc/can/dbc.py and new test_ocelot.py,
car/{values.py,car_helpers.py,torque_data/override.toml,retropilot/},
dbc/ocelot_controls.dbc. Parent pins submodule; guide/BeamNG guides/notebooks
and validation logs are tracked. Local commits are not pushed. Maintenance
configcdc20d4 registers the submodule and retains journaling/validation.

Workflow: source-driven-development, interface design, TDD, incremental
implementation, security, Git, documentation and self-review. Existing
teacher PORTING_PLAN used; no need for a second approval to execute owner's
explicit port instruction. REA binary analysis was not needed for this
readable-source migration. The native CRC crosscheck is an offline reference
execution, not REA/firmware or hardware verification.

## 2026-11-03 — Car-port checklist: identification and safety remain separate

Reconciled owner's pasted modern car-port checklist with actual source and
commaai/opendbc README (official current structure/safety sections). Added a
file/status matrix to docs/RETROPILOT.md. Existing modern package/state/codecs
and explicit selection are implemented; active controller mapping, automatic
identification, RetroPilot MCU policy and compiled safety tests are pending.
No invented fingerprints or radar/safety stubs added. Current noOutput request
is not proof of Chimera enforcement; CarController itself always emits nothing.
Teacher C2 safety header remains WIP (arbitrary RX enables controls, disabled
integrity checks, DLC mismatches and missing steering/brake limits). Host file
creation alone cannot wire that policy into Chimera's actual TX path.

Source pins unchanged: parentbase1a1cc4025c4233732bbbb86c061c4c54b35add5a,
opendbc649bbb632a020f155fc1eb16ae343f49a5c4bb50; canonical DBC/source/model
unchanged. Documentation/source review only; prior53CAN/22port/1600native CRC
results remain prior results, not new MCU safety tests. No code/device/network
PC/firmware/actuation change; no REA binary question. Next implementation stays
receive-only Chimera transport, producer units/profile, then qualified active
control and MCU policy. No new owner question needed for this clarification.
Skills: source-driven review, code-review-and-quality, interface design and
repository documentation/Git. Validation: notebook, real file-status/relative
link assertions and whitespace, captured in the checklist evidence receipt.

## 2026-11-03 — C2 RetroPilot identification mapped to modern selection

Owner asked why fingerprint registration was absent and requested teacher C2
comparison. Re-read immutable C2 values.py and selection/car_helpers.py:
values has placeholderIDs0..15/DLC8; selection hard-codes "RETROPILOT RETROFIT",
skipsFW queries and overwrites the matcher result. It did not identify the
retrofit through measured ECU/CAN fingerprints. Earlier explanation omitted
this distinction and compatibility with the old name was missing.

Implemented car/retropilot/fingerprints.py with C2-name MIGRATION and an empty
FINGERPRINTS map. Shared car/fingerprints.py merges that map; car_helpers
normalizes the old name before the RetroPilot no-diagnostic guard. Explicit
argument and FINGERPRINT environment accept both old/new names. Existing
Sunnypilot CarPlatformBundle migration now converts saved C2 names; tested
against actual native Params in caller-owned temporary directories. Other-car
MOCK selection stays unchanged. No global override or automatic matching added.

Source: C2b9a942efd3cb210127bb5efb5cf9ccf6a811c728; parentbasec6917544;
opendbc649bbb6→04a78352a9605a0e07342146fe8481b7d92ee7fd on radxa/retropilot.
27RetroPilot/5Params/53CAN tests and303broader car tests pass (314existing
subtest skips); Ruff and whitespace pass. Canonical DBC, noOutput/passive
controller, speed factor0, hostbus2, CD210GPU eb741641 and firmware unchanged.
No model/manager/game/hardware/CAN TX or persistent owner-settings action.
Next remains receive-only Chimera backend and producer/profile qualification;
automatic identity and active MCU safety remain unimplemented. No new question.

Current receipt: Ai/Evidence/retropilot-c2-selection-20261103.json; source hashes
and RED/GREEN/regression logs retained. Skills: source-driven-development,
interface design, TDD/incremental implementation, Git, documentation and
self-review. Source-first path; no REA artifact/runtime question. No upstream
merge; inbox had0related pending and8historical failed/blocked records retained.

2026-11-03 six-folder clarification: history report now maps cereal/opendbc/
panda/selfdrive/third_party/tools. Old third_party is compiler/libyuv work;
tools is joystick control. boardd edits are build fixes, not Chimera transport
validation. Runtime status/next action unchanged; see dated history session.

## Final software/GPU checkpoint; physical wire still unresolved

Post-start genuine capture492/492 samples over11.995s passed independent
decoder and actual passive CarInterface (canValidtrue/vehicleSensorsInvalidfalse,
noOutput,dashcamOnly,carNotReadytrue). Median19.835ms,p9547.902,max57.640,0gaps
>150ms. Actual throughput~41Hz, not guaranteed50Hz. Final genuine-game serial
TX attempt117samples/3s received0Chimera frames. Firmware/manager/control holds
unchanged. All bounded gateways/readers stopped; BeamNG remains open with the
temporary Bastion reference scene and read-only UDP producer. PC account now
has dialout access. Next measure termination/transceiver rails,confirm wiring/
bitrate and qualify ACK/silent behavior. Current hardware owner facts retained;
no invented powered-rail or installed silent-state conclusion.

2026-11-04 shutdown handoff: fresh165tests/source integrity pass; no functional change. Owner chose November5Chimera focus: resolve actual connector,USB-only rails,removed Waveshare termination and ACK/silent/bitrate before receive acceptance. Last0CANframes; noOutput/relay exclusion retained. Audit/publication/ordered shutdown report at Ai/Reports/beamng-shutdown-audit-20261104; actual remote/shutdown receipts follow before closeout.
