# Current Panda, legacy Panda contracts, and Chimera — November 5, 2026

## Scope and result

Owner requested an in-depth understanding of current Panda, legacy Panda and our
Chimera code, starting with the teacher. This review covers the host/firmware
boundary, discovery and process ownership, wire formats, status, safety,
heartbeat/ignition, CAN routing, configuration, firmware lifecycle and the current
Radxa adapter. It does not use simulator behavior as an explanation.

There is no single legacy Panda protocol. The retained mailbox-era host, the C2
host and current Panda have materially different contracts. Chimera reuses Panda
API names and USB IDs but is a sensor/gateway application with a different safety
and configuration implementation. A codec translation does not supply MCU safety.

This is an architecture and selected-function source review, backed by offline
checks. It is not an exhaustive review of every supported board, car safety mode,
peripheral, compiler path or every byte of firmware, and does not establish live
hardware behavior. Exact source hashes and coverage categories are in
[sources.json](sources.json); actual checks are in [validation.json](validation.json)
and [tests.txt](tests.txt). The verifier is [verify_contracts.py](verify_contracts.py).

## Teacher evidence retrieved first

Read central routers/resume/current task/update inbox, student router/handoff/state/
tasks, QA-20261105-08 through11, the Chimera transport and Ocelot topic notes,
retropilot/PANDA_CHIMERA.md, retained C2 host/layout provenance, the actuator-demo
host report, October recovery/config incident and existing November3REA evidence.
Earlier modern-source notes pin Panda74a0adce; current project pins8a16e089.
The source is rechecked here rather than treating the older pin as current.
The upstream-update hold remains; no fetch,merge,reference advance or timer resume.

## Source versions and meanings

| Layer | Pin and location | Meaning |
| --- | --- | --- |
| Current Radxa parent before review | ad7efa20849305682e99337fff4a710c91fb7c51 | Protected sunnypilot project on radxa/q8b; notebook changes follow |
| Current Panda submodule | 8a16e089b88593914823743df29e1c30b7dd3e00 | sunnypilot/panda; H7 firmware, USB/SPI Python library |
| Current CAN/safety submodule | 150f937198ceab43c43b39f94b9bdea63fcb633c | opendbc_repo: CANPacket type, safety dispatcher/modes and car code |
| C2 application reference | b9a942efd3cb210127bb5efb5cf9ccf6a811c728 | Retained retropilot/panda/c2_host files, not a full restored checkout |
| C2 Panda reference | 9e6d47f63675d5a45170ae7972c24412034dc136 | Retained health/CAN definitions and WIP RetroPilot hook |
| Older native mailbox host | RetroPilot/openpilot_demo e2ce83cb349d2f5ec442b004fdafac61099b052f | Retained source/selfdrive/boardd under steer_actuator_demo/openpilot_demo |
| Ocelot reference | d87892fa25ef2a2474110b97bfb5245ee818b534 plus existing dirty files | Chimera application, old Python client0.0.9 and desktop tools; dirty bytes hashed |
| Installed-nightly historical identity | v1.0.0-DEV-de193215-DEBUG | Historical read/signature match; exact source commit unavailable |

Current Panda Python identifies itself as0.0.10; this package version is not a
wire-version compatibility guarantee. The pinned remote Python blob9d562fc1ec1de4005049658cc8b7345bd4176df5
matches local git hash-object. [Remote check](remote-source-check.json) records
GitHub's read-only response and the exact nightly-source lookup404. This did not
fetch or advance any local repository.

## Ownership: four different jobs

1. Car code/DBC understands vehicle signals and constructs requested messages.
2. Host transport moves messages between Cereal and the selected board and manages
   identity,health,ignition,reconnect and lifecycle.
3. MCU transport/controllers move messages between host and physical CAN.
4. MCU safety permits/blocks commands and forwarding using the selected policy.

The DBC does not select a USB wire format. A Python API method name does not prove
that the firmware implements that operation. Publishing a safe-looking board
state cannot create an enforcement path that the board does not have.

## Current managed Sunnypilot path

The manager normally selects Python pandad; the alternate direct native _pandad
entry is disabled. pandad.py does startup health checks, internal-board reset/
recovery and a DFU sweep, selects a supported internal/SPI board, checks signatures,
flashes/recoveries when needed,then launches the native executable. Native
Panda::list and constructor use only PandaSpiHandle; SConscript compiles panda.cc
with spi.cc,not a native libusb backend. Python USB support alone therefore does
not give this daemon a Chimera USB path.

The native loop targets100Hz for CAN reception/publication. It processes peripheral
control at20Hz,board state/heartbeat/safety configuration at10Hz and peripheralState
publication at2Hz. A separate sendcan thread drops events older than1second and
passes fresh requests to the board; that age gate is not vehicle safety validation.
It publishes can,pandaStates and peripheralState. Board disconnection ends the
process; communication faults can trigger a later reconnect. The current native
host manages one board; C2 managed multiple boards with four-bus offsets.

PandaSafety configures ELM327 for initial diagnostic/fingerprint traffic,manages
OBD multiplexing,waits for FirmwareQueryDone/ControlsReady and CarParams/CarParamsSP,
then sets alternative-experience/SP parameters and the requested safety mode.
Offroad/unstarted handling requests noOutput. A silent board is switched to
noOutput to allow CAN acknowledgement without host command permission. These
Panda mode semantics must not be presumed for Chimera0xDC.

## Current Python client: connection has side effects

Panda.__init__ calls connect. connect opens USB first,then SPI,reads packet versions,
and sends configuration operations. By default disable_checks=True adds heartbeat-
disable and power-save-off requests. Independently of that flag,it resets comms,
disables automatic CAN-FD switching on all3buses and sets all3bitrates(default500k).

The extracted actual methods were exercised against fake handles returning no
0xDD response. get_packets_versions returns(0,0),but connection setup still emits:

| Setting | Vendor OUT writes observed in fake-handle check |
| --- | --- |
| disable_checks=True(default) | 9: F8,E7,C0,E8×3,DE×3 |
| disable_checks=False | 7: C0,E8×3,DE×3 |

No actual Panda object,USB device or SPI endpoint was opened by this check.
Version checks are decorators on health/CAN methods; they do not gate all connection
writes. The wrapper's startup health loop and support-selection path instantiate
Panda before rejecting external devices. Its DFU sweep also precedes internal
selection. Correction to any earlier shorthand: late filtering is not a guarantee
that no external-device action occurs first. No actual external write/flash during
this review is claimed. Do not use generic Panda() as a passive Chimera probe.

There is a distinct Sunnypilot Rivian external-F4 flash helper, gated on a Rivian
platform and external black-Panda type. It is not Chimera support. Current Python
SUPPORTED_DEVICES lists H7 red/tres/cuatro/body; INTERNAL_DEVICES is tres/cuatro.
F4 address/DFU constants remain in the library,but they do not establish generic
F4 runtime support in this managed daemon.

## CAN wire formats

| Contract | Frame representation | Integrity/chunk handling | Health |
| --- | --- | --- | --- |
| Ocelot mailbox Python/native demo; Chimera | Fixed16bytes: RIR u32,RDTR u32,payload8 | No extra per-record XOR; USB link CRC is separate; mailbox alignment matters | 43bytes |
| Retained C2 host/Panda | 5-byte header plus payload | Counter at start of each64-byte USB packet; no modern frame-XOR byte | 50bytes,health version3/CAN version2 |
| Current Panda | 6-byte header plus0..64payload | XOR over header+payload must total0; partial-frame buffers survive chunk boundaries; reset viaC0 | 49bytes,hash-based versions |
| Current Sunnypilot Chimera adapter | Reads16-byte mailbox,produces modern Cereal can | Rejects malformed batches; filters returned/remote from vehicle receive | Requires exactly43bytes,keeps safety raw |

Mailbox metadata: RIR bit2 is extended,bit1 remote; address is shifted3for extended
or21for standard. RDTR low nibble is payload length,next bus field includes
returned bit0x80; upper16bits are firmware bus_time. That timer is not a calibrated
ECU/host sample time. Chimera hardware path is classical CAN,maximum8payload bytes.
The old Python client returns(address,busTime,data,bus); modern Panda Python uses
(address,data,bus). Changing tuple shape is separate from changing wire format.

Modern header: byte0has FD bit0,bus bits1–3,DLC bits4–7; bytes1–4contain
(address<<3)|(extended<<2)|(returned<<1)|rejected; byte5is XOR checksum. DLC maps
0..8,12,16,20,24,32,48,64. Current native header calls bit0reserved but retains the
6-byte representation; do not infer tested FD metadata preservation from that
name. Returned/rejected are represented to host consumers using bus offsets0x80/
0xC0. A classical mailbox cannot be handed directly to either variable-header host.

C2's USB packet counter is transport framing,not a vehicle payload counter.
Current native unpacking buffers partial messages and resets communication state
on XOR error; retained C2 parsing clears its transfer assembly each call and does
not provide the same defensive partial-frame handling. Offline transcoding tests
prove representations,not complete device lifecycle or installed compatibility.

## SPI is another layer,not another CAN format

Current native SPI uses /dev/spidev0.0,mode0,8bits and configured50MHz. Requests
contain endpoint,u32ID,u16TXlen,u16RXlen,payload,CRC32. Responses contain ACK/NACK,
sameID,u16length,payload,CRC32. Ready=3C,ACK=C3,NACK=5A; host poll bytes areFF.
Repeated requests preserve an ID so firmware can replay a cached response without
running the operation twice. NACK indicates congestion/backpressure; retries use
a new ID. CRC32 and response-ID checks protect this transport layer. The CAN
records inside still use the6-byte/XOR format. None of this establishes a matching
SPI peripheral or50MHz qualification on Radxa/Chimera.

## Status layouts and identity

Measured source layout sizes: mailbox-era demo43,Chimera43,C2Panda50,currentPanda49.
Current per-bus can_health_t is64bytes. The verifier records each field offset.
Current health version hash=0xCA8F9EAF; CAN layout hash=0x75ABF276 for these exact
files. Current0xDD returns two32-bit values; absent/short responses are not a
compatible old numeric version. Hashes change with the source header bytes.

Old43health has separate ignition/controls bytes,u32voltage/current and legacy
error counts. C2adds heartbeat_lost,unsafe_mode and blocked-message count. Current
49health uses16-bit voltage/current,a16-bit flags bitmap,explicit safety-blocked/
invalid/overflow counts,alternative-experience,interrupt/fan/SPI/SBU/sound/temperature
and lateral/longitudinal permission fields. Equal-looking field names do not
permit casting layouts. Current native get_state and C2get_state accept any
nonnegative read length into a zero-initialized struct; a future adapter must
validate exact lengths rather than rely on that convenience behavior.

Reviewed Chimera health hardcodes voltage/current0,safety17,param0,and exposes a
controls_allowed variable initializedfalse with no normal enabling assignment
found in its application. These are not voltage measurements or proof that Panda
allOutput policy was installed. Historical Chimera customC1type/D0provisioning
reads returned empty; the USB descriptor serial remains a usable distinct identity.
The dedicated receiver pins VID/PID,productChimera,serial and expected version.

## Control API: same number can mean different behavior

| Request | Current Panda | Reviewed Chimera |
| --- | --- | --- |
| B6/E0 | Firmware/Python debug read isB6; native serial_read still sendsE0 | E0reads UART ring; no B6handler found |
| C0 | Reset CAN fragment-assembly state | No active handler found |
| C1/C2/C3 | Board type/per-bus health/MCU UID | No active handlers found |
| D0 | Provisioned serial/secret information | No active handler found; USB descriptor serial is separate |
| D1/D8 | Enter loader/reset | Loader/reset implemented,subject to debug/hardwired guards |
| D2 |49-byte health |43-byte health |
| D3/D4 | Application signature halves | Signature halves |
| D6 | Version text | Version text |
| D7 | No handler in reviewed currentmain | Local patched config capability marker; not proof of installed support |
| DC | set_safety_mode→set_safety_hooks | Changes relay_req_usb using numeric modes; no safety dispatcher |
| DD | Health/CAN version hashes | No active handler found |
| DE | Validated bitrate for each of3buses | Only value/bus0accepted; no persistent startup-speed loading |
| DF | Alternative-experience/SP settings | No active handler found |
| E5 | Loopback/reinitialize | Loopback/reinitialize; uses can_silent mask |
| E6 | Custom clock-source timing; older Ocelot Python calls this USB-power control | No active handler found |
| E7/E8/F8 | Power save/FD auto/heartbeat-disable | No active handlers found |
| F1 | Clear RX/all or selected TX queue | Local handler clears RX for value0orFFFF; not the full current TX-queue API |
| F3 | Heartbeat with engagement/MADS state | Resets heartbeat counter only |
| F9/FC | FD data bitrate/non-ISO mode | FCis JSON command input; F9not handled |
| FB | No currentmain handler; dormant native helper still names deepsleep | JSON response read |
| FD/FE/FF | Not Chimera config APIs | Format/write entry/chunked config read |

Commented-out B4/B5relay blocks are not active capabilities. The legacy Python
library also exposes functions for requests its firmware may ignore. Static API
presence and successful USB transfer completion are not physical readback.
The native host's E0log-read helper and dormant FBdeep-sleep helper do not match
the inspected current firmware's B6debug-read/B5debug-stop handlers. SPI forwards
the request unchanged. These are additional source-level API gaps in the current
pair,not measured runtime failures or reasons to substitute Chimera commands.

## Current Panda safety path

Current firmware includes opendbc/safety/safety.h. set_safety_mode calls the
registry; unknown modes fall back to silent. Silent and noOutput both reject
host actuation under their policies,but silent disables CAN acknowledgement
whereas noOutput permits a live receive/ACK controller. Car mode handling also
sets harness interception and bus configuration.

Host messages enter comms_can_write,then can_send. can_send invokes safety_tx_hook
unless this is an explicitly approved forwarding path. Rejected frames are marked,
checksummed and queued back to the host with a blocked counter. The controller
TX path verifies transport XOR. On receive,the firmware constructs the CAN packet,
uses safety_fwd_hook to select approved forwarding,invokes safety_rx_hook,updates
ignition and queues the observed frame to the host. RX invalidity is recorded;
raw logging and authorization are distinct. safety_tick checks timing/quality.

Heartbeat arrives from managed host nominally10Hz. MCU checks its age at1Hz and
uses5-count threshold while ignition/start is true,2while off; on loss it enters
silent,power save and changes peripheral behavior. Separate engagement mismatch,
watchdog,register and fault paths exist. Threshold counts are source behavior,
not exact measured end-to-end shutdown latency. Physical transceiver/harness
behavior still needs board-specific tests.

## Legacy RetroPilot safety and our current files

The C2RetroPilot hook is labelledWIP. Its RXvalidation/checksum code is commented,
it sets controls_allowed on arbitrary receive,and has no qualified steering/brake
limit engine. Its RX0x301length6differs from the retained DBC8. Treat it as historical
behavior to understand,not a policy to install unchanged.

Our modern opendbc registry adds RetroPilot mode39. Parameter0production init
supplies NULLactive limits: disabled/release command patterns only on explicit
bus2; unknown parameters have noTX,forwarding disabled. retropilot_active.h has
an engine for qualified measured profiles,with freshness,counters,CRC,driver
intervention,engagement,amplitude/slew and gas/brake exclusion checks. Artificial
profiles are native-test fixtures; no production initializer selects one. The
current car interface still requests noOutput and runtime controller emits noCAN.

Mode39's presence in source and compilation into this review's native fixture do
not install it on Chimera or prove an existing H7firmware image includes it.
Existing November3safety evidence remains historical and separately linked in the
student topic. This review reran communications/adapter tests,not the full vehicle
safety suite or H7ARM/MISRA/hardware acceptance.

## Chimera firmware path and gaps

Local startup selectsGATEWAY,asserts transceiver enable pins PC1/PC13/PA0active-low,
sets normal pins and initializes all3controllers500k/non-silent. can.halso declares
can_silent=FF,but only reinitialization uses that mask. Reading the variable alone
cannot establish the installed board's state. A generic DEbus0/E5operation can
reach that different reinitialization path; this consequence is source-derived,
not a measured change performed here.

USBIN81drains fixed16-byte records; OUT03queues TX. Raw RX on all3buses feeds USB.
The local can_send does not invoke safety_tx_hook; its skip_tx_hook flag controls
the opposite queue branch rather than installing Panda safety. Forwarding tables/
setters exist,but raw can_rx does not use them to implement current safety-gated
forwarding. Periodic generated sensor messages write MCUCAN1mailboxes directly,
so adding a hook only to hostcan_send would not cover every board-generated TX.

Direct IGN,VSS,CPS,BRAKE,ADC1/2and configuredCAN2angle/rate/speed/ignition/RPM/brake
feed generated boardCAN0reports50/75/76/100. Configured CANcruise11–14is absent in
RXcode; ADCbutton matching exists. endian_type ignored,CANRPMmasked&1,no generic
OEMintegrity/freshness checks,wrong speed-mode configindex3and some null-config
accesses remain. See the previous native-input record for exact fields. These
findings do not prove corresponding defects in unavailable nightly source.

F3timeout only clears relay_req_usb. Main relay logic follows ignition and has
request gating commented out; neither current Panda heartbeat failure behavior
nor physical relay dropout is established by this source. No relay action here.

## Persistent configuration and firmware lifecycle

Chimera config is776bytes: magicDEADBEEF,32entries×24bytes,CRC32over entries.
Local main stores integer CANscale/offset; retained json_api source stores floats
at a different layout. The desktop site's encoder does not prove which one the
nightly uses. SYSoutput groups are a bitmask1/2/4/8; stored bitrate fields are not
read by local startup. HALLandADCcalibration remain producer/hardware contracts.

The prior watchdog/flash erase incident,patched candidates and successful original-
nightly restore remain separate evidence. The float-layout candidate failed boot;
watchdog-off SYSwrites later passed exact776-byte readback. This review did not
repeat writes or lift the serial quarantine. SourcepatchD7marker is not a current
installed capability claim.

Modern H7default application address is08020000; legacy F4/Chimera application is
08004000,bootstub08000000. Bootstubs verify a signed length/body,VERSminimum2and
RSA/SHA signature before jumping; debug-key acceptance depends on bootstub build.
Matching signatures/API names do not make H7images suitable for F4. Modern wrapper
and DFU recovery are active write-capable flows; Ocelot's legacy flash_docker also
writes the bootstub. None were executed. The known saved nightly image hash and
historical signature match identify a retained artifact,not recovered source.

## Our current dedicated Chimera receiver

chimera.pyopens only normal-mode Chimera identity with explicit serial/version,
reads D6and exact-layoutD2,then reads81. It preserves bytes received before timeout,
rejects partial mailboxes and cleans up the claimed interface on errors. It has
no controlOUT,bulkOUT,heartbeat,relay,bitrate/config/flash operation or sendcan
subscription. Optional canpublication uses host monotonic receipt times and ends
with an invalid empty event. Returned/remote frames are excluded from vehicle
reception. Health remains a raw observation; it does not publish pandaStates or
grant managed readiness. It owns no automatic reconnect/firmware lifecycle.

That boundary is a useful validated receive component,but not a finished replacement
for managed pandad. The read-only desktop bridge is another distinct tool; its
lower-level USBhelper drops partial data on timeout while this receiver retains it.
Only one managed owner/publisher must be selected when integration is implemented.

## Bus contract still needs an explicit adaptation

Our physical RetroPilot car/safety source selects hostbus2. Local Chimera's vehicle
extraction listens on boardCAN2/host2,but its synthesized reports transmit on
boardCAN0/host0. The receiver preserves tags; it does not remap0to2or publish
Chimera's internal variables as CarState. A generated hardwareTXis also not
automatically an unreturned vehicleRX; returned receipts are explicitly filtered.
Thus native sensor synthesis,physical bus routing and the current car parser do
not form a proven automatic chain merely because both mention RetroPilot. Route
and source authority must be deliberately qualified; no remap was implemented.

## Validation and evidence limits

Fresh checks used189mailbox cases and336modern packets across3buses,7addresses
(standard/extended boundaries)and supported lengths. Modern checks exercise every
split point and every single-bit corruption position: incomplete changed-length
packets may remain buffered,but no corrupt frame may be accepted. Health layouts
and offsets are source-derived. Two fake-connect cases prove9/7vendor OUTwrites
without hardware. A fresh native libpanda fixture was compiled withGCC13.3.0from
current Panda communications and current opendbc safety includes in a temporary
directory; no on-disk existing library was replaced.

21existing tests passed,0failures/errors/skips: modern Pythoncodec1,native firmware
comms5and Chimeraadapter15. The comms suite includes60000TXand50000RXmessages,
chunking,queue and reset checks; these are native fake-controller operations.
The initial verifier had a missing fakePanda global; corrected in the harness,
with [initial note](initial-harness-limit.txt) retained. No product failure was
hidden and no functional source was patched.

Existing REA GNU symbols/disassembly evidence for local Chimera ELF SHA256
5ae9b4f6ea99e569028d271c4ec9c2ce59cd11375b5482adbd0781f3480e20b8still matches the
on-disk artifact. Selected saved get_health_pktreturns43and endpoint/can_send
sections were inspected. This reuses matching historical analysis; it is not a
new REA run or disassembly of installedde193215. [REA reuse](rea-reuse.json).

Unresolved: exact nightly source and build provenance,actual current board health/
configuration,physical routing/rails/ACK/bitrate/traffic,complete managed bridge,
truthful health capability mapping,qualified MCU enforcement and endpoint limits.
No USB/SPI/DFU/device discovery or live CAN,firmware/config/relay/output action was
performed. No push or upstream update. No claim to know every unobserved behavior.

## Next engineering boundaries

Keep the dedicated receiver as the passive baseline. Resolve actual installed
identity/capabilities and physical receive first. Then design explicit managed
ownership/reconnect/ignition/health behavior around supported facts. A future TX
path must separately qualify all host and generated MCUtransmissions,board safety
semantics and endpoint release/failure behavior. Do not blindly transplant C2
framing,safety rules,stock startup writes or updater assumptions into Chimera.
