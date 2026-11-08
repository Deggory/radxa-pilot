# RetroPilot safety and canonical DBC — focused review, November 8, 2026

Baseline009ec3899c8cec85aefdd5cc094104be74022868; opendbc150f937198ceab43c43b39f94b9bdea63fcb633c;
Panda8a16e089b88593914823743df29e1c30b7dd3e00. [Actual result/source hashes](RESULTS.json).
This is a focused source/compiled-test review, not a complete safety audit or
installed-board qualification. No product code, DBC or firmware was changed.

## Findings

The modern opendbc/safety/modes/retropilot.h registers the hooks and defines
seven allowed command ID/bus/DLC combinations. Parameter0without a qualified
active profile permits only exact disabled packets with valid CRC; unknown
parameters permit no TX. Forwarding is disabled. RelayCore0x600is not allowed.
Normal retropilot_init calls retropilot_profile_init(NULL,param), so supplying
mode39or changing its parameter cannot enable active actuation.

retropilot_active.h implements a parameterized engine for steering interceptor
0x300, gas interceptor0x200 and iBooster position0x20E. Other allowed command
families remain disabled-only. Required RX is0x50/0x75/0x76/0x100/0x301/0x201/0x20F,
all on hostbus2 with matching DLC. It checks full CRC8J1850, modulo16counter
progression, metadata/status/quality, two clean samples and profile freshness.
Ignition, brake/gas/steering override, button edges and feedback envelopes gate
engagement. Active TX checks channel agreement, ranges, speed taper, slew and
250mssteering change, command timing/counters and gas/brake exclusion. Startup
requires a16-counter disabled cycle on each of the three engine axes; this
models acceptance, not physical delivery acknowledgement. Tests supply synthetic
limits via a debug-only harness; no qualified production vehicle profile exists.

The car interface remains dashcamOnly/noOutput and runtime CarController.update
returns no CAN. The new passive pandad path does not install these MCU hooks.
Preserved chimera_old can_send contains no modern safety_tx_hook and its relay
still follows ignition. Repository safety code therefore exists, but it is not
active-command safety enforcement on the attached old board.

The historical retropilot/safety/safety_retropilot.h is a separate C2 WIP
reference: bus0, commented RX/checksum validation and controls_allowed=1 in RX.
Do not confuse it with the modern restricted/parameterized header or copy its
weaker policy into the Radxa implementation.

## DBC checks and outstanding producer gaps

Canonical retropilot/dbc/ocelot_controls.dbc and the packaged opendbc copy match
SHA256b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67.
All28messages are present:20legacy retrofit messages plus8RP-SIM-1messages.
The first7363bytes match the preserved original C2 DBC. All7TX/7RX ID/DLC
pairs agree with the DBC; safety code explicitly chooses hostbus2 (the DBC
alone does not establish physical routing). Full CRC8/SAE-J1850 over bytes1..end
matches the host checksum function. Focused compiled tests exercise the packers
and hooks; this is not every producer/bit-layout/physical calibration proof.

Retained producer caveats remain material: local Ocelot differential.h183uses
lut_checksum(dat,6,...) while transmitting8bytes of0x301. The modern full8-byte
check disagrees for an explicit offline vector (partial245/full202). This source
is pre-existing dirty local firmware, not proof of the installed board image.
Saved old Chimera CRUISEADC writes are byte-aligned while canonical ADC fields
start at bits31/47; speed units/source mode and generatedCAN0versus parser/
safetybus2routing also require explicit qualification. No checks were weakened
and no firmware/DBC adaptation was made by this review.

## Verification

Fresh focused suites test_retropilot and test_retropilot_active:50tests passed
in2.605s, native C hooks rebuilt with the existing UBSan harness. Tests include
release fixture containment, disabled-command metadata/CRC/counter handling and
synthetic-profile active bounds/override/fault recovery. No full safety suite,
new coverage claim, ARM image build, device/USB/CAN/relay/vehicle test, config,
flash, update or push. Source-first readable files and compiled fixtures answer
this question; no unrelated REA binary/runtime claim. Code-review skill used
for the focused comparison; documentation/Git skills for durable closeout.

Next: keep host reception passive. Any active integration needs a separately
qualified endpoint/vehicle profile, resolved producer/DBC/bus differences,
MCU enforcement deployment and physical fault/override/cutoff verification.
New Chimera rewrite and upstream updates retain their saved holds.
