# Pinned legacy F4 status mapping inputs

Selected unchanged files from `ajouatom/openpilot`, carrot-wip commit
`69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7`, read November6,2026 using the
connected GitHub file reader at that exact ref. This is source research, not a
Sunnypilot/upstream update or evidence of firmware installed on a device.

- [Fault declarations](panda/board/faults_declarations.h): status0/1/2 and fault bits0..27.
- [Harness declarations](panda/board/drivers/harness_declarations.h): NC/normal/flipped0/1/2.
- [Safety source](opendbc_repo/opendbc/safety/safety.h): selected ID definitions reviewed. Full file retained unchanged for provenance/standalone checks, not an every-line hook audit.
- [Panda license](panda/LICENSE) and [opendbc license](opendbc_repo/LICENSE): original MIT notices.

[SOURCES.json](SOURCES.json) records exact upstream paths/URLs, Git blobs, SHA256
and byte counts, checked against the earlier saved nontruncated tree at this ref.
Panda license reused from the already verified in-project health fixture. The
related health17/CAN-health5 [fixture](../carrot-f4-health-v17/README.md) and
producer/host source review remain separate evidence. No imported file is compiled
into the runtime converter or used as an active MCU policy.

Legacy safety25=STELLANTIS and26=FAW conflict with current25=volkswagenMlb and
26=hongqi. The converter rejects them.26other IDs have matching source labels
(with current volkswagen corresponding to the explicit MQB declaration at15);
matching labels do not prove equivalent hooks/parameters or permit control.
Fault bit27=SOUND_DMA has no current Cereal enum entry and is rejected, together
with any higher bit. Current Panda also defines bit27; the schema limit is not
unique to legacy firmware. See the [mapping contract](../../docs/LEGACY_F4_PANDA_STATE.md).
