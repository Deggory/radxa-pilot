# Native original-Chimera passive acceptance

Owner: "lets mdify pandad to accept the chimera_old  ,use all the skill of teacher awat it learnd".

Deliver one complete offline-verified native receive/diagnostic capability in
existing pandad. Retain exact USB identity, serial/version pins and exclusive
ownership. Dispatch CHIMERA_MAILBOX separately from F4v17, keeping current/new
bootstrap refused. Decode little-endian mailbox16 and health43 from preserved
source and literal/historical fixtures. Preserve standard/extended IDs, bus0..2,
DLC0..8 and payload. Validate/filter RTR and returned receipts. Reject unsupported
bus3+, reserved/DLC corruption, oversized input, time reversal and expired partial
records; failure latches and discards that feed. Bound pending data to one16-byte
record; use the existing500ms partial expiry and4096-byte feed bounds.

Only D6/D2 reads and bulk-IN81 for original Chimera. No C1/DD/C2 or any OUT,
reset/config/heartbeat/flash operation. Native can messages and separate labelled
chimeraOldMailbox16 raw diagnostics; preserve raw safety17 and zero placeholders
without mapping to modern safety or measured voltage/current. Mark observation
only/nonoperational; no normal pandaStates, sendcan or control threads. Failure
or close emits invalid empty CAN/diagnostics where graceful delivery is possible.
Release ownership and clear fragments; explicit reopen reidentifies, with no
old data replay. No automatic reconnect requirement or active-control admission.

Keep F4 public sample behavior and JSON unchanged. New profile uses its own
codec, health type and publication. Main dispatch must use the fixed identified
profile, including failure labels. USB transport protections, canonical DBC,
old firmware and halted new rewrite remain unchanged. No physical run is included.

Threat boundary: device-owned USB descriptors/bytes -> bounded host parser and
messages. Pins constrain identity but are not authentication. The old protocol
has no extra record checksum; this cannot manufacture payload integrity or ECU
sample freshness. Host monotonic timestamps are receive times. Bus3 is outside
our three-controller native route despite the broader legacy Python decoder.

Verification: test-first native codec + fake USB/session/publication fixtures,
Python literal/parity/CarState regression, real native target build, ASan/UBSan,
request trace proving no writes/C2, old/F4/current rejection regressions and
preservation/notebook checks. Independent review before closeout.
