# Ocelot Panda Docker source review

November 6, 2026. Owner supplied
[Deggory/Ocelot_Panda_docker](https://github.com/Deggory/Ocelot_Panda_docker)
as evidence that the board previously served as an older Panda while preserving
analog inputs, relay and OBD-C. This is useful legacy implementation evidence.
The reviewed source does not establish a working physical Chimera installation
or current Sunnypilot compatibility.

## Two applications, two board selections

Current main is pinned at
[04b56ba0145588d91ff70e1b35b47b7f2652d4db](https://github.com/Deggory/Ocelot_Panda_docker/commit/04b56ba0145588d91ff70e1b35b47b7f2652d4db),
May 14, 2026, “Trim workspace to panda-only docker flash workflow.” Its parent is
[98de83bb54746d057e6e4bff707eab6cd8c179d9](https://github.com/Deggory/Ocelot_Panda_docker/tree/98de83bb54746d057e6e4bff707eab6cd8c179d9).
The current Git tree is complete (not truncated); the branch query returned only
main and the Actions query returned zero workflow runs. This does not establish
whether somebody previously built or ran the board elsewhere.

| Source target | Selection | What the source establishes |
| --- | --- | --- |
| Current panda | F413, panda/main.c, explicitly removes -DGATEWAY | config.h defines PANDA; board.h probes white/grey/black/UNO/DOS board variants |
| Parent panda | Same main.c and same flag exclusion | Separate legacy Panda application already existed before the trim |
| Parent chimera | F413, chimera/main.c, retains -DGATEWAY | Gateway board selection plus direct inputs, generated reports, configuration and onboard outputs |

Verified by evaluating only flag/project assignments and preprocessing config.h
with a temporary empty MCU include. No SCons project or firmware was executed.
Selected original source:
[current SConscript](../reference/ocelot-panda-docker-20261106/firmware/SConscript),
[config.h](../reference/ocelot-panda-docker-20261106/firmware/config.h),
[board.h](../reference/ocelot-panda-docker-20261106/firmware/board.h) and
[parent SConscript](../reference/ocelot-panda-docker-20261106/parent-98de83bb/firmware/SConscript).

The retained gateway abstraction has the expected three CAN controller pin maps
and active-low transceiver enables, but its ignition callback returns zero and
its harness configuration says has_harness=false. Stock Panda harness intercept
relay calls are separate from Chimera's PB0 onboard output. Changing a target
name or enabling PANDA is insufficient to preserve Chimera's board behavior.

## Analog, digital, relay and OBD-C code recovered from the parent

The parent
[Chimera main.c](../reference/ocelot-panda-docker-20261106/parent-98de83bb/firmware/chimera/main.c)
is byte-identical to committed ocelot/firmware/chimera/main.c at d87892fa.
It differs from our preserved dirty working file. Parent Chimera USB/CAN headers
also match our Ocelot files exactly. This corroborates earlier source recovery;
it is not a newly discovered electrical pinout or proof of when hardware was added.

| Interface | Source mapping | Behavior/limit |
| --- | --- | --- |
| Analog 1/2 | PC2/PC3, ADC12/13 | Actual adc_get(12)/adc_get(13) acquisition; no measured calibration here |
| Ignition/brake | PA3/PA6 | Active-low digital inputs |
| Speed/crank | PA4/PA5 | Pulse inputs and interrupt handling |
| Onboard relay | PB0 | Starts low; loop follows line-or-CAN ignition |
| OBD-C relay request | PA2 | Active-low input read into relay_req_obdc |
| OBD-C ignition output | PB1 | Starts high/off; loop writes inverse ignition_on |
| CAN0 / host0 | CAN1, PB8/PB9, enable PC1 | Cores/controlled devices under the existing board contract |
| CAN1 / host1 | CAN2, PB5/PB6, enable PC13 | Radar/ADAS role under the existing board contract |
| CAN2 / host2 | CAN3, PA8/PA15, enable PA0 | Vehicle/retrofit sensors under the existing board contract |

Parent main.c lines743–744 read ADCs; lines1010–1028 implement digital inputs and
outputs; lines1171–1193 set GPIO modes/pulls/startup outputs. The condition using
relay_req_obdc or relay_req_usb is commented out. B4/B5 direct-output handlers
are inside a block comment. The heartbeat clears relay_req_usb, but that value
does not control PB0 in the shown loop. Therefore neither heartbeat-driven power
cutoff nor actuator disabling is established. Physical relay contacts/load paths
remain an electrical qualification item.

The source uses OBD-C as an accessory request/ignition interface. It does not
define an OBD diagnostic protocol through those two signals, nor prove a
particular accessory or harness is compatible. Stock Panda board_has_obd()
and CAN_MODE_OBD_CAN2 refer to a separate board-specific CAN routing feature.

ADC channel12 is labeled voltage sense in the inherited generic ADC helper,
where adc_get_voltage() applies a stock divider conversion. The Chimera main
instead uses channels12/13 as its external analog inputs. Do not publish a
stock Panda voltage/current conversion as measured Chimera supply health.

The parent configuration header is older than our local working header: it lacks
local watchdog-window/write-repair changes and the local motor config extension.
It is historical reference, not a reason to replace our recovery/config evidence.

## The separate legacy Panda protocol and policy

Reviewed
[Panda main.c](../reference/ocelot-panda-docker-20261106/firmware/panda/main.c),
[CAN driver](../reference/ocelot-panda-docker-20261106/firmware/drivers/can.h),
[safety registry](../reference/ocelot-panda-docker-20261106/firmware/panda/safety.h),
[USB driver](../reference/ocelot-panda-docker-20261106/firmware/drivers/usb.h) and
[Python host](../reference/ocelot-panda-docker-20261106/firmware/python/__init__.py).

| Property | This older Panda application | Modernization implication |
| --- | --- | --- |
| Application USB ID | bbaa:ddcc | Shared IDs do not uniquely identify Chimera or a protocol |
| Bootstub USB ID | bbaa:ddee | Keep recovery separate from normal-mode selection |
| CAN | Fixed16-byte STM32 mailbox records, IN1/OUT3; max four records per64-byte IN packet | Matches the legacy framing family, not modern six-byte/XOR records |
| Health | Packed43 bytes, safety_param signed int16 at offset39 | Neither modern49-byte nor Carrot59-byte health |
| C1 / D6 | Hardware byte / firmware version | Available here; original Chimera's command set differs |
| DC | Selects actual safety hooks and changes CAN silent/live state | Different from original Chimera's relay-request semantics |
| DD | Sets/clears CAN forwarding | Conflicts with modern Panda's version-query request; never probe before profile qualification |
| Startup | Calls SAFETY_SILENT | Source intent only; no physical silence/driver operation measured |
| Host TX | Calls can_send(..., false), which invokes the selected TX hook | Useful policy placement, not an approved policy for this board |
| Forwarding | Manual forwarding precedes hook selection; can_send(..., true) bypasses TX hook | Do not inherit this bypass; guard every future outgoing path |
| Heartbeat loss handling | Fallback block is under EON; supplied target does not define EON | Do not assume a compiled timeout interlock from reading the block alone |

The debug build enables ALLOW_DEBUG and exposes safety17/all-output. Its TX hook
permits everything. That old number must not be interpreted as our RetroPilot
policy. None of the old vehicle safety policies was audited or approved here.

One concrete host mismatch: old Python health uses unsigned H for safety_param,
while C declares int16_t. A synthetic -1 is decoded as65535 by that Python format.
Our existing signed health43 decoder remains distinct; exact size alone does
not prove semantic equivalence or authorize native profile admission.

The old endpoint3 loop also assumes whole16-byte records. It does not supply our
new codec's strict size/DLC/header/error contract. Queue/USB/timer techniques are
reference inputs to review against the new driver tests, not production imports.

## How this helps the current plan

1. Keep Chimera's explicit board/pin map and acquisition separate from the Panda
   transport/status/policy layer. The parent provides a direct comparison of both.
2. Use the retained USB callbacks/FIFO/reset/timer implementation as an additional
   source for T03b2; retain our ST-backed bounded operations and cancellation tests.
3. Carry the DD collision and signed health field into future T02/T05/T08 profile
   fixtures. This oldest Panda43/mailbox16 family is not admitted by today's host
   selector; current support targets remain explicit and unchanged.
4. Use real safety dispatch as historical architecture evidence for T13, while
   requiring policy on host, generated, forwarded and maintenance transmissions.
5. Preserve PC2/PC3, PA2–PA6, PB0/PB1 through T09/T10/T14/T17/T18. Do not replace
   their configuration, calibration or output behavior with stock Panda helpers.

No task is newly declared complete. Next implementation remains T03b2; operational
status/endpoints, inputs/Core Config, MCU policy and physical qualification remain
open. Canonical RetroPilot DBC and bus identities are unchanged.

## Retained evidence and actual verification

[Source receipt](../reference/ocelot-panda-docker-20261106/retrieval.json) retains
the complete current tree and selected commit history, plus Git blob/SHA256 pins
for31 exact original text files (current and selected parent files). Includes
attribution/provenance; no private debug key, restricted linker or vendor SDK copy.
Selected snapshots are not a complete buildable distribution. Repository licensing
was not resolved into a permission to import implementation into our MIT target.

Reproduce offline:
`python3 chimera/reference/ocelot-panda-docker-20261106/verify_reference.py`.
[Actual output](../reference/ocelot-panda-docker-20261106/validation.json):31source
hashes, both project/flag tables, preprocessor selection, compiled packed health
size/offset, signedness fixture and189actual sender/parser vectors pass. The sender
uses an in-memory sink; only selected AST functions run, no Panda imports or USB
constructors. Ruff passes for the new verifier. An initial macro assertion did
not allow compiler trailing whitespace; corrected the verifier's comparison and
reran successfully. No reference source normalized or behavior changed.

Ocelot's39dirty entries/all19pinned source hashes, the clean evidence archive and
all active firmware/host code remain unchanged. No Docker build, full legacy
firmware build, device access, flash, relay operation, CAN traffic, install,
Sunnypilot upstream/reference update or push. The repository's recover.sh writes
both application at0x08004000 and bootstub at0x08000000; it was read only.
