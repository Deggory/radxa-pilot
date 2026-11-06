# Chimera audit and restart checkpoint — November 6, 2026

Owner requested an audit, saved handoff, Sunnypilot GitHub update and PC shutdown.
Implementation baseline: `05a33eb1c556fd5d7bf489056ce1782330671e6f` on
`radxa/q8b`. The saved remote branch was `c1811280466b2eb410db03599e24350003060d0e`:
33 local commits, 234 changed paths, 231 existing-file hashes. Every one of those
33 commits has a latest passing validation record. This audit changes project
documentation and evidence only; it does not implement the next stage.

## Work accounted for

| Area | Completed and checked | Still outstanding |
| --- | --- | --- |
| Evidence | Source map, original firmware/wiki/history and Ocelot Panda Docker/Carrot references pinned; board buses, inputs and reserved flash recorded | Installed image, electrical measurements and physical recovery qualification |
| Firmware | Independent F413 bootstrap, layout checks, inactive GPIO, distinct identity/read-only manifest, current CAN codec, detached USB clock/core/EP0/packet driver/service and UID/reset snapshots | Main does not call USB service; operational CAN/health binding, actual attachment and input acquisition |
| Native host | Explicit USB serial/version selection, ownership/cleanup, current versus legacy identification, exact F4 health59/CAN-health64 decoders | Other managed profiles and reconnect/backoff policy |
| SPI removal | Source, backend class/buffers, build target, discovery and implicit startup/fallback removed from pandad; native binary/archive checked | Historical wire statistics with spi in their names remain measurements, not a backend |
| Passive legacy monitor | CAN reception on `can`, complete isolated JSON on `customReservedRawData1`; strict parser and failure release | Normal `pandaStates` publication and lifecycle policy |
| Status preparation | Offline legacy PandaState preview; typed profile/observation/unavailable-field metadata; validity/liveness/field guards in hardwared, manager, UI, selfdrived and MADS | Preview remains invalid and observation-only; no operational ignition/control admission |
| Board features | CAN0/Cores→host0, CAN1/ADAS→host1, CAN2/vehicle→host2 and direct input/relay/OBD-C interfaces retained in contracts | Digital/pulse/analog acquisition, MCU TX policy, Core Config, persistent settings, relay/OBD-C and bench/release work |

The unsigned bootstrap remains7448bytes, SHA256
`d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698`,
parked/unflashed. Hardware remains untested for this implementation. Existing
older board observations are not qualification of the new firmware.

## Audit evidence and limits

Fresh runs pass56focused host tests,68control/MADS/power/fan assertions and
28firmware/discovery tests:152Python tests total. Ten native test programs pass.
The two previously built strict USB/current-read and converter sanitizer binaries
pass again; their recipes/source hashes are in the availability receipt. Firmware
tests also rebuild their native sanitizer fixtures and verify ARM/layout limits.
These are offline tests with fake/register inputs or selected production branches,
not full managed daemon/GUI/physical USB or vehicle integration.

**Audit finding:** the bare control-suite process printed68tests/OK but hung at
interpreter exit. A bounded reproduction dumps a stack in `StatLog.__del__`,
called by `StatLogSP.__del__`: the parent terminates a shared ZMQ context while
the child still owns a socket. The source is unchanged since the previous remote
checkpoint. Three agent-owned completed/stuck test processes were terminated;
the original outputs and exit status are retained. The first bounded diagnostic
selected four modules/61tests; the final runner selects all five/68tests.

The [audit runner](run_control_regressions.py) preserves all assertions and closes
both metrics sockets **after the suite**, before terminating their shared context.
That run passes68tests and exits0. Production stats teardown remains an open
issue; this audit does not claim to fix it. Earlier notes reporting68passes refer
to successful assertions and did not establish clean interpreter exit. The new
receipt corrects that limit rather than overwriting historical evidence.

Metadata describes support, not authentication or control authorization.
Metadata-absent historical current producers retain their old contract. Six legacy
fields are unavailable; safety25/26 name conflicts, fault27+ and signed alternative
overflow remain rejected. The generic current fault-list/schema27 limitation
remains unexposed and unresolved. No failure or test assertion was suppressed.

Preservation checks cover all23firmware-source hashes, the image, Ocelot39dirty
entries/19source hashes, five attributed reference files, clean archive
`224cfa645134db91103c55d8188d87e7976b0ba4`, Panda
`8a16e089b88593914823743df29e1c30b7dd3e00`, opendbc
`150f937198ceab43c43b39f94b9bdea63fcb633c` and the canonical RetroPilot DBC
SHA256 `b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67`.
Camera/model/Thneed source and artifacts remain outside this audit's changes.
A limited credential-signature scan of the tracked publication delta found no
matches; this is not a comprehensive secret audit.

Source-first review covered startup/session ownership, exact reads, passive
publication, preview validity, shared field admission and the new teardown
finding. Existing source/artifact receipts were reused; no REA provider or
delegated review was performed. Applicable Git, review, documentation and
debugging skills guided the audit. No firmware/device/reset/configuration/CAN TX,
managed stack, upstream update or merge was performed.

## Publication, shutdown and tomorrow

Publish this source/history and README to the existing owner repository
`Deggory/radxa-pilot:radxa/q8b` by normal push. Its default branch remains `master`
under the owner's saved preference. Supporting opendbc remote ref already matches
the submodule. The GitHub connector can inspect metadata but cannot upload local
Git objects; Git handles that transfer. Actual push and remote-SHA readback are
recorded in a later closeout receipt, not asserted in advance here.

PC preflight: strict trusted-host SSH cannot reach10.43.0.216 (no route),
10.42.0.216 times out, and historical192.168.1.104 refuses SSH. No authenticated
PC shutdown command has been delivered. The owner was asked whether the PC is
already off or has a new address. Radxa is the current `comma` host; only the
separate PC was named for shutdown in this request. Physical power state is
unobserved. Any later result belongs in the shutdown receipt.

**Resume November 7, T08b2d: passive normal-status publication and
disconnect/reconnect handling.** Read both handoffs and live Git/status/validation.
Specify publication validity and required fields, invalidation on disconnect,
bounded retry/backoff with fresh pinned identification, exclusive ownership and
no stale sample reuse/SPI fallback. Keep legacy observations nonoperational and
verify lifecycle failure cases offline before any hardware step. Do not resume
active driving or flash the parked bootstrap from this handoff.

[Source/commit audit](source-audit.json), [preservation](preservation.json),
[focused tests](focused_python.json), [control clean exit](control-clean-exit.json),
[cleanup diagnosis](control-cleanup-diagnosis.json), [firmware tests](firmware.json),
[availability implementation receipt](../../Evidence/chimera-availability-20261106.json),
[roadmap](../../../chimera/tasks/plan.md).
