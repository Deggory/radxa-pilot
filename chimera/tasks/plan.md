# Incremental Chimera implementation

November 6, 2026. Active project location: `sunnypilot/chimera/`.
The existing T01–T20 task identities are retained. Each slice gets appropriate
checks, a local commit and a notebook handoff before expanding the scope.

November7 owner priority: deliver a larger working capability beyond the25%
checkpoint. T03c4 now implements explicit attach/OTG/suspend/resume/reset/session-end
and fresh reconnect through the main/service/driver path.36firmware tests pass,
including92new composed scenarios/40reconnect cycles. Stage100% offline; revised
full-roadmap estimate30%/70% remaining, physical0%. Default startup stays held.
Next opt-in board USB startup binding, then bulk/CAN RX and operational status;
hostT08b2d remains queued. [Current contract](../docs/USB_LIFECYCLE.md).

T03c4 completed capability — USB control lifecycle (offline):
- [x] Explicit checked attachment with disconnect delay, pristine EP0 and pre/post power/session/clock invariants.
- [x] Captured OTG acknowledgment, session-end priority, retained suspend/resume and reset cancellation.
- [x] Explicit fresh reconnect, cleanup/retry, full firmware/ARM tests, mutation checks and independent review.

T03c3b completed slice — explicit legacy no-VBUS session (offline):
- [x] Add validated unforced(default)/legacy modes to detached core/service preparation; legacy selects only B-session override, no VBDEN/attachment, no silent fallback.
- [x] Main config copies explicit mode; legacy polling keeps VBUS UNKNOWN and rejects a supplied reader. Preserve mode invariants, reset/suspend/OTG-fault cleanup and explicit restart without retaining overrides.
- [x] Real-component sanitizer/fault tests, full firmware/ARM checks, docs, percentage checkpoint and local commit. Actual main profile remains NULL; no hardware/flash.

T03c3a completed slice — observed VBUS supervision (offline):
- [x] Main polling requires a fresh PRESENT observation before and after each service poll; missing/unknown/invalid/absent observations stop the detached service and revoke the snapshot.
- [x] Failure retains cleanup ownership and initiating error, with no automatic sampling/restart after failure; explicit stop/restart requalifies observations.
- [x] Native real-component fault tests, full firmware suite, ARM build, documentation and percentage checkpoint saved. Board profile/reader remain NULL; no attach or electrical qualification.

Owner clarification, November6: Radxa-to-Chimera/selected legacy Panda is USB only.
T08 must select pinned USB explicitly, never probe/fall back to SPI, and remain
disconnected on USB failure. Existing generic SPI source is not a deployment
requirement. Pandad SPI source/build/classes/discovery and generic entries are now removed.
All platforms require pinned USB startup; no implicit transport fallback.

Additional November6 source evidence: [Ocelot Panda Docker review](../docs/OCELOT_PANDA_DOCKER_REVIEW.md).
Pinned current/parent targets distinguish stock Panda selection from Chimera
GPIO/acquisition. DD forwarding/version collision and health43 signedness feed
future T02/T05/T08 fixtures; no new firmware integration or task completion.

- [x] T08USB Remove pandad SPI backend/source/classes/build/discovery and generic entry; pinned USB on all platforms.
- [x] S00 Create the in-project home, retain source map/provenance and establish the sequence.
- [x] T06a Transport interface extracted and tested offline; original SPI backend subsequently removed by T08USB.
- [x] T02a Pinned read-only native identification and profile selection; exact versions/health lengths and negative fixtures checked offline.
- [x] T06b Native USB factory/backend, exclusive pinned selection, bounded I/O and cleanup; fake USB and real-library link checks pass.
- [x] T01a Source-backed board GPIO/flash/RAM contract; physical recovery and electrical qualification remain open.
- [x] T01b Owner-identified Ocelot base power trace:17gateway schematic/board nets, Pro/source/PDF comparison and36source checks. No MCU VBUS sense net; no electrical or recovery qualification.
- [x] T03a Original minimal F413 startup/linker/build, inactive outputs, nine offline tests and deterministic raw image.
- [x] T02b Distinct bootstrap identity/manifest, read-only request handler/matrix and source bus/input contract; twelve offline tests pass.
- [x] T04 Pure current six-byte/XOR classical CAN codec; fourteen-test suite, source interoperability and bounded stream/error fixtures pass offline.
- [x] T03b1 Backend-driven USB clock/detached-core preparation and pure descriptor/EP0 model; sixteen offline tests pass. No packet driver/startup attachment yet.
- [x] T03b2 Ordered ARM MMIO/DWT timing backend and polling EP0 event/FIFO driver; nineteen offline tests pass. Startup/attachment and physical qualification pending.
- [x] T03b3a Power/VBUS/UID/watchdog/recovery requirements and read-only UID/reset/option snapshot helper; twenty-one offline tests pass. No startup/attachment.
- [x] T03b3b Composed detached preparation/poll/release service; twenty-three tests/44integration scenarios pass. Not called by main; physical attachment unqualified.
- [x] T03c1 Main calls checked boot snapshot preparation; explicit clock/facts/error/USB_HELD diagnostics and30offline firmware tests. No USB service/attachment or CAN/input startup.
- [x] T03c2 Main detached USB lifecycle coordinator, UID continuity, bounded polling, cleanup/explicit restart;32offline tests/51new integration scenarios pass. Board NULL profile stays held; physical qualification remains open.
- [x] T03c3a Observed VBUS supervision before/after bounded poll, unknown/lost cleanup and explicit restart;33offline tests/16new scenarios pass. Physical reader/profile/attachment remain unbound.
- [x] T03c3b Explicit legacy no-VBUS session mode, exact invariants, truthful UNKNOWN status, reset/fault/cleanup/restart behavior;34offline tests/61new scenarios. No attachment or hardware qualification.
- [x] T05a Bootstrap status/capability contract and strict pure decoder; response interoperability/rejection fixtures pass offline. No operational health/profile admission.
- [x] T08b2c Typed field-availability metadata and normal consumer guards;124Python/10native/sanitizer/mutation checks pass offline. No ordinary USB status publication.
- [x] T08b2b Offline source-backed legacy PandaState preview, explicit unavailable fields and strict conflict/fault/width validation; no publication/admission.
- [x] T08b2a Normal host ignition validity gate, invalid/empty update revocation and retained shutdown context; 65Python tests pass. No USB PandaState admission.
- [x] T08b1 Passive classical CAN RX plus isolated customReservedRawData1 diagnostics; strict fragment/error handling and offline tests. No pandaStates admission.
- [x] T08a Radxa USB-only pinned status startup/session; bypass legacy reset/flash/SPI, legacy F4 typed sampling with immediate failure release; no CAN/pandaStates publication.
- [x] T05c Legacy F4 CAN-health5/64 typed decoder and bounded selector0..2 reader; exact layouts, golden data, sanitizer and rejection fixtures pass offline. No managed publication.
- [x] T05b Legacy F4 health59 typed native decoder and bounded read helper; exact retained header/golden bytes, sanitizer and failure tests pass offline. No managed publisher/startup.

| Task | Next deliverable | Status |
| --- | --- | --- |
| T01 | Board GPIO/reset behavior, flash/config partitions and recovery boundaries | T01a/b board/flash contract and owner-identified base power trace complete; no MCU VBUS detector in base; installed recovery/electrical qualification pending |
| T02 | Distinct identity, legacy/current protocol profiles, RPC matrix and explicit bus/input source contracts | T02a/b complete offline; operational health/capability/config ABI and new-profile host admission remain pending |
| T03 | Minimal F413 target, reviewed support/linker and offline image budget | Through T03c4 integrated USB control lifecycle complete offline; board startup binding, physical power/current/recovery and bench qualification pending |
| T04 | Modern six-byte/XOR classical CAN USB codec with stream/vector checks | Complete offline; no endpoint/CAN-controller binding or TX permission |
| T05 | Exact identity/version/health responses, legacy F4 status adaptation and fail-disabled state | T05a bootstrap, T05b health59 and T05c CAN-health5 decode/read helpers complete offline; publication and new Chimera operational health pending |
| T06 | Native Sunnypilot USB transport and offline failure tests | Offline transport implemented (T06a/b); managed use remains T08 |
| T07 | Isolated passive receive qualification on each physical bus | Pending separate bench scope |
| T08 | USB-only current/F4/Chimera managed passive lifecycle, pinned selection, reconnect and exclusive ownership; no SPI probe/fallback | T08a legacy F4 USB status startup/session complete offline; CAN/status publication, other profiles and reconnect policy pending |
| T09 | Preserve digital/pulse acquisition and qualify invalid/stopped states | Pending |
| T10 | Preserve ADC acquisition, calibration and button handling | Pending |
| T11 | Configured vehicle CAN extraction, integrity and freshness | Pending |
| T12 | Canonical reports and explicit host delivery/source selection | Pending |
| T13 | MCU policy guarding host/generated/forwarded/maintenance TX | Pending before bench TX |
| T14 | Core Config modern read/monitor transport | Pending |
| T15 | Recoverable persistent settings and watchdog/power-loss behavior | Pending |
| T16 | Exclusive maintenance and qualified board/Core configuration writes | Pending |
| T17 | Onboard relay power/fault qualification | Pending separate bench scope |
| T18 | Qualified OBD-C accessory support, or explicitly disabled capability | Pending |
| T19 | Reproducible passive release and managed fault/soak evidence | Pending |
| T20 | Separate active-control scope and production profile qualification | Future |

The detailed original roadmap remains pinned in the optional workspace archive
at `../chimera/tasks/plan.md`, relative to the Sunnypilot repository root.
This sequence carries the implementation forward without requiring that archive
at runtime. Slice boundaries may split a task; a partial task stays pending.

T05a [status/capability contract](../docs/STATUS_CAPABILITY_CONTRACT.md) and pure
bootstrap decoder and T05b legacy F4 health59 decoder/read helper are complete
offline, along with T05c [CAN-health5](../docs/LEGACY_F4_CAN_HEALTH.md).
T08a/b1 are implemented for pinned legacy F4 passive CAN and isolated diagnostics.
T08b2a adds normal host ignition validity. T08b2b adds tested source-backed PandaState preview conversion. T08b2c adds
supported-field metadata and consumer checks. Passive normal-status publication,
explicit operational admission policy, reconnect and
physical qualification remain pending, retaining no SPI probing/fallback. New Chimera
operational health and bulk CAN/controller binding remain pending.
[Detached service](../docs/USB_SERVICE.md) now composes existing modules.
[Requirements](../docs/USB_STARTUP_REQUIREMENTS.md) retain missing physical power/
VBUS/current-recovery evidence. Qualified startup/attachment follows those gates.
Electrical unknowns block
claims or hardware loading that depend on them; they do not erase known source
assignments or prevent bounded offline engineering.

Owner added legacy Panda compatibility on November 6. The independent host
transport boundary was extracted first; it does not depend on a flashed Chimera
image. See [the compatibility slices](../docs/LEGACY_PANDA_SUPPORT.md). T06a/b and
T02a/T05b/T05c are checked offline; publication, managed lifecycle and
physical testing still follow. See the [health59 contract](../docs/LEGACY_F4_HEALTH.md).

Next per November7 main-first priority: opt-in board USB startup binding, then bulk/CAN RX and operational status; physical qualification remains separate. Host T08b2d passive normal-status publication/disconnect/reconnect remains queued; keep legacy observations nonoperational. [Availability contract](../docs/PANDA_STATE_AVAILABILITY.md). [Mapping contract](../docs/LEGACY_F4_PANDA_STATE.md). [Contract](../docs/USB_PASSIVE_RECEIVE.md).
