# Temporary Chimera CAN2 500 kbit/s test — 2026-11-08

## Actual outcome

The owner authorized the previously proposed test with “lets test it”. One
narrowly guarded temporary runtime command completed over USB, but **CAN
reception did not recover**. No persistent configuration or firmware was changed.

| Observation | Duration | USB reads / native batches | Received CAN |
| --- | --- | --- | --- |
| Direct raw USB before command | 4.000403058s | 2000reads | 0bytes /0records |
| Direct raw USB after command | 12.001264853s | 5883reads | 0bytes /0records |
| Native pandad after command | 20.115466715s | 1895batches,20health | 0frames on every bus0/1/2 |

Native profile was chimeraOldMailbox16, exit0. The raw probe counts actual
libusb transfer lengths before decoding; all returns were0and all payload
lengths0. Empty valid native batches do not mean CAN frames were received.
There are no sensor0x25frames or other received IDs in these captures.

## Exactly what changed

Selected original Chimera bbaa:ddcc/productChimera/serial
3a0044001651333038373636 at USB003/021. Version
v1.0.0-DEV-de193215-DEBUG and all128application signature bytes matched saved
nightly e35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b.
The separate Interceptor DAC Bench was not opened by the exact-address probe.

Sent exactly one application OUT: vendor type0x40, request0xDE, wValue2,
wIndex5000, zero payload. In this fingerprinted nightly, the handler supports
buses0..2and interprets5000as500kbit/s. The command status stage completed;
its internal can_init result is not returned by that API. Therefore this proves
USB acknowledgement, **not BTR register readback or measured wire timing**.
The guard permits only that one OUT after identity/signature/config validation;
an exclusive attempt file prevents accidental mutation replay in this report.

Printed CAN2is MCUCAN3/USBbus2. Sensor wiring stayed there. Separate sensor
supply/common ground are previously owner-confirmed, not newly measured.
No CAN data frame was sent by the host; controller operation may acknowledge
traffic. No Save/Format/reset/flash/heartbeat or command to another bus/device.
The narrow authorization does not lift other firmware/config/upstream holds.

The last requested runtime CAN2rate is500k. We did not reboot or send a rate
restore command; the pre-test live register value was not read. Restarting this
nightly is expected to reapply saved CAN2zero/default250kboot behavior. No
restart was performed as part of this test.

## Interpretation and next step

QA56's artifact finding remains: matching nightly uses250kdefaults and nonzero
saved-rate overrides, unlike the preserved source. However, the authorized
500kcommand alone did not restore reception. Do not mark the failure solved or
claim bitrate is conclusively eliminated: internal initialization/currentBTR
were not measured. The controller handler can acknowledge even if initialization
fails. No further rate sweep, firmware rewrite or saved-config change follows
from this negative result.

Next useful evidence: verify CAN2actual controller initialization/timing and
transceiver VCC/STB/RXD/waveform, plus current sensor transmission/termination.
Earlier CANH/L1..1.15V and labelled5Vrail4.5V remain historical leads, not current
measurements. Zero placeholder health voltage/current and sparse error counters
cannot qualify those electrical or register states. Keep the known-working
Waveshare sensor evidence distinct from this negative Chimera test.

## Preservation and evidence

Before/after flash reads both776bytes, valid CRC and identical SHA256
4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22.
Saved speeds remain500/500/0/0kbit/s; no permanent repair applied. Health uptime
increased23287..23303during the raw test, then23321on native entry, consistent
with no observed reset. Per-controller register health remains unavailable.

All76legacy manifest files, native executable SHAe9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84,
and canonical DBC SHAb4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67
preserved. Panda8a16e089/opendbc150f9371and existing ocelot/steering dirty sets
unchanged. Started projectab38419b89ab3725ba6cb0af39e0e5f33a19ea5a clean.
Native/source/firmware unchanged. Only teacher/student Ai documentation changes.

Both reader handles/processes closed; final target USB owner list empty.
Existing Core Config GUI left open/disconnected. No new compiler/unit test run
was needed because product code did not change. The live bounded captures,
request whitelist/count, matching fingerprints, flash readback and preservation
checks are the actual validation. Earlier23Python/5native results are historical.
Used debugging and Unlazy solo verification with documentation/git discipline;
reused pinned QA56artifact/REA fallback evidence, no new REA decompilation claim.

Central report retains test_runtime_speed.py, RUNTIME_TEST.json, before/after
USB bytes and frameJSONL, native log/summary/canJSONL, config-before/after.bin,
BASELINE.json and PRESERVATION_CLEANUP.json. Student evidence summarizes these
without requiring an outside source to understand the result.
