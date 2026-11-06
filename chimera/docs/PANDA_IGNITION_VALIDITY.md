# Panda ignition validity prerequisite

November 6, 2026 — T08b2a. Source baseline
`bc99ae0d917a99b925840c31a11c3cb34ed5f7e0`.

The normal host consumes `pandaStates` to select ignition/startup and retain
harness context for battery shutdown. Previously hardwared accepted nonempty
updates without checking Event.valid. Empty updates also advanced receive time
without clearing the previous ignition state, potentially preventing timeout
from clearing it. Both defects reproduce against the baseline source branch.

## Implemented behavior

[hardwared](../../openpilot/system/hardware/hardwared.py) now routes every updated
pandaStates event through the pure
[panda_power_state](../../openpilot/system/hardware/panda_state.py) reducer.

| Input | Ignition | Primary harness context used for shutdown |
| --- | --- | --- |
| Updated invalid event | False immediately | Retain last valid value |
| Updated empty event | False immediately | Retain last valid value |
| Updated valid, only unknown types | False | Retain last valid value |
| Updated valid, non-unknown types | Either ignition flag on any non-unknown Panda | Update only from a non-unknown primary Panda |
| No updated event | Preserve until existing receive-age grace exceeds5seconds | Retain last valid value |

The helper receives the event's actual validity from SubMaster.valid; invalid
payload fields are not read. A later valid update can restore ignition. The
primary harness remains independent of ignition; secondary ignition still counts,
while secondary harness does not replace primary-board semantics. The existing
`pandaType != unknown` predicate is retained; this is not a new protocol/board
allowlist or firmware authentication mechanism.

Keeping the last valid harness context is deliberate: PowerMonitoring uses
in_car to permit delayed low-battery/offroad shutdown. Clearing that history on
an invalid/empty report could suppress battery protection. It does not assert
live connectivity or change current power measurements. Invalid reports cannot
establish a new harness state; a later valid primary disconnection can clear it.
No-update disconnect logging and the existing strict age>5s threshold are unchanged.

## Scope and evidence

12new tests use real Cereal builders/readers and cover invalid/empty/unknown,
either ignition flag, repeated invalid updates, primary/secondary semantics,
serialization, recovery and retained/cleared shutdown context.37focused Python
tests (these12plus existing USB/Chimera/Thneed25) and28power/fan regressions pass.
The37-test run treats warnings as errors. A Capnp test initially serialized one
builder twice; separate builders remove the warning without suppression.
A temporary helper with validity rejection removed fails3tests. Seven cases
execute the actual selected baseline/current hardwared AST branch with fake
SubMaster fields/clock, reproducing both defects and preserving the disconnect
deadline. This does not run hardware_thread, live messaging or hardware methods.
Ruff and Python compilation pass. [Receipt](../../Ai/Evidence/chimera-panda-validity-20261106.json)
contains source/version/hash pins and actual outputs. Native/firmware code and
artifacts are unchanged, so prior native/sanitizer results are retained evidence,
not fresh runs. Camera/model/Thneed, DBC, outputs and Ocelot/archive are preserved.

## Remaining integration

This fixes a prerequisite; it does not admit legacy operational status. The
[USB monitor](USB_PASSIVE_RECEIVE.md) still publishes only CAN and isolated
customReservedRawData1 diagnostics, with no pandaStates or TX/control threads.
No schema, USB profile, runtime pins or device configuration changes occur here.
A valid event alone is not proof of MCU safety policy or physical readiness.

T08b2b now adds the tested [offline legacy mapping](LEGACY_F4_PANDA_STATE.md),
with explicit unsupported fields and always-invalid previews. Next T08b2c is
ordinary admission/supported-field metadata and consumer review before publication.
Reconnect/backoff and full physical/firmware qualification remain later work.
USB only, no SPI fallback.
