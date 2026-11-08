# Original Chimera: native passive USB support

Implemented November 8, 2026 in existing pandad. The retained chimera_old
firmware and halted chimera rewrite are unchanged. This capability receives
classic CAN and publishes labelled raw diagnostics; normal managed Panda status,
vehicle control and firmware programming are outside this increment.

## Entry and identity

The existing pandad.py launcher requires PANDAD_USB_SERIAL and
PANDAD_USB_VERSION and execs pandad --usb-status SERIAL VERSION. There is no
new command, default serial, device-client probe or updater. Existing F4v17
support remains. Session admission now also accepts the separately identified
original Chimera: VID bbaa/PID ddcc, product Chimera, exact serial and firmware
version v1.0.0-DEV-de193215-DEBUG, and exact health43. CURRENT and the new
bootstrap profile remain refused by this observation entry.

Example for a separately qualified matching board (replace the serial):

```sh
PANDAD_USB_SERIAL='REPLACE_WITH_EXACT_SERIAL' \
PANDAD_USB_VERSION='v1.0.0-DEV-de193215-DEBUG' \
.venv/bin/python openpilot/selfdrive/pandad/pandad.py
```

This command is documentation, not an action performed by this change. Pins
constrain selection; they do not authenticate firmware or establish an exact
source/installed-image match. The retained source includes saved local changes.
The exact historical de193215 source and current physical board equivalence
remain unresolved. Do not run a second CAN publisher alongside pandad.

## Native path

panda_usb.cc retains exclusive ownership and original-Chimera write protections.
Identification uses D6/D2 only. PandaUsbStatusSession fixes its protocol for the
connection, dispatches original mailbox16 to ChimeraUsbCanStream, and reads
separately typed ChimeraHealth using D2 only. No C1/DD/C2, control OUT, bulk OUT,
heartbeat, safety setup, reset, config write or flash operation is added.

Mailbox decode is little-endian. Preserve standard/extended ID, DLC0..8, payload
and original host bus0/1/2. The native frame retains its extended flag; Cereal
CAN exposes address/bus/payload but has no separate extended-ID flag. Validate
before filtering RTR/returned TX receipts.
Reject bus3+, reserved RDTR bits, malformed standard-ID bits and TXRQ bit0 on
non-receipts. Returned TIR-origin records may carry bit0 and are filtered. The
existing Python reference is broader for bus3/TXRQ; native behavior is deliberately
restricted to the reviewed three-controller RX contract. No bus remapping or DBC
change is made. CAN0/Cores=host0, CAN1/ADAS=host1, CAN2/vehicle=host2 remain source
roles, not verified current wiring.

Read at most4096bytes per poll with the inherited10ms USB timeout. Retain at most
one16-byte record across transfers/timeouts; an incomplete record older than500ms
or a backwards/zero host timestamp fails closed. Any malformed record discards
all staged frames from that feed and latches failure. No resynchronization.
Mailbox16 has no extra record checksum: structurally valid payload corruption
is not detectable here. Host monotonic publication time is receive time, not
qualified ECU sample time or end-to-end freshness.

## Publications and failure

Main still publishes only can and customReservedRawData1. The latter retains
kind panda-usb-status/schema1 with profile chimeraOldMailbox16, exact identity,
operational:false and observationOnly:true. rawHealth contains all18 reported
values, with raw suffixes for unqualified state/enum/power fields. No modern
safety enum translation, voltage/current calibration, per-controller health or
heartbeat-loss value is invented. Seven fields hardcoded in preserved source
are listed under availability.preservedSourcePlaceholders. controllers is empty,
perBusHealth/heartbeatLost/pandaStates are false availability capabilities.
The F4v17 diagnostic builder/layout is unchanged.

Failure or close releases USB, clears both codecs and prevents further IO from
that session. Identified protocol remains available after close for correct
failure labels. On orderly failure/exit, main attempts invalid empty can and
failed/closed raw diagnostics; abrupt power/process loss cannot guarantee a final
message, so consumers still need liveness checks. Explicit reopen reidentifies
and starts with empty state. No in-session reconnect/fallback is added; an external
supervisor may restart the existing process. D2 sampling is sequential with CAN
polling and can block up to its control timeout; no whole-loop deadline/throughput
claim is made.

Receive-only host policy does not change original firmware behavior. In the
preserved source PB0 follows ignition rather than the USB relay-request variable.
This implementation supplies neither a relay cutoff guarantee nor MCU safety.

## Verification and limits

The real native target and11offline native programs are checked, including fake
USB ownership, exact request traces, failure/partial/reopen isolation, unchanged
F4 and refused CURRENT/bootstrap profiles, and Capnp/JSON publications. Native
codec covers432record combinations at every split plus literal/historical health
fixtures and malformed/time/size cases. Python compares432native mailbox vectors
and5health vectors with the independent existing decoder. Startup, protocol,
consumer/availability and Thneed telemetry regressions run without daemons/devices.
ASan/UBSan and copied-source negative controls test parser/session behavior.

Exact commands, red/green evidence, independent review and result receipts are
in Ai/Reports/chimera-native-passive-20261108. Its verify.py has native, python,
sanitizers and preservation modes. Local repeated output goes into ignored run/;
the coordinating teacher owns the single active Unlazy gate ledger. No real
USB/device/CAN/relay/vehicle session or firmware build/flash was performed.
Physical qualification and later managed/active integration remain separate.
