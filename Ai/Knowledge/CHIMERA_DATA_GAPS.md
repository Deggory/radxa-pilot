# Chimera data completeness — November 6, 2026

We have enough source/reference evidence to begin bounded offline engineering;
we do not have a complete verified hardware/installed-firmware dataset. Review
QA-20261106-03 before repeating a claim that all board data is available.

Saved references include selected Ocelot/current Panda/C2/Carrot F413 and native
USB code, Core Config source, canonical DBC context, input/bus source maps,
original nightly image and historical recovery/config evidence. These snapshots
are not complete buildable source distributions or tested managed integration.

A collection gap was closed today: 17 historical Core Config backup/quarantine
files still existed outside the new board folder. They were copied unchanged to
`/home/radxa/comma/chimera/recovery/legacy-core-config-20261106/`, with origin and
SHA-256 manifest. Eight configuration blocks have valid magic/CRC; one all-FF
block is incident evidence. Valid bytes can still represent empty/unsafe/unknown
settings. No restore, quarantine-policy activation or current hardware read.

Remaining facts/decisions:

- Exact owner-board revision/MCU marking, full schematic/power tree and connector
  mapping, input conditioning, relay contacts/load paths and OBD-C levels.
- Exact source/build provenance for the saved de193215 nightly; its original
  image and historical application restore proof already exist.
- A verified complete current recovery set, including installed bootstub and
  current configuration/signature consistency. Local bootstub builds are not dumps.
- Full new F413 build inputs/toolchain/board definition and signed partition budget.
- Measured physical reception on all three buses and calibrated direct inputs.
- Actual vehicle/sensor CAN IDs, layout, units, integrity and freshness.
- Explicit bus/source authority, generated-report delivery, modern status and
  versioned configuration contracts; remaining implementation is not missing data.
- Measured relay/fault/endpoint release and later active-control qualification.

OBD-C can remain disabled during initial Radxa USB reception. Exact old source
is useful to reproduce old behavior but is not an absolute barrier to a new
known-source implementation with explicit migration/recovery limits. Full ST
manual reading/archive remains incomplete in the new folder; earlier teacher
notes preserve selected flash/watchdog facts.

Next T01/T02: board/partition/recovery evidence plus identity/RPC/bus contracts.
No firmware/application/DBC change, hardware operation or push. The detailed
[board gap checklist](/home/radxa/comma/chimera/docs/DATA_GAPS.md) is an optional
workspace reference; this note remains self-contained in a standalone clone.
