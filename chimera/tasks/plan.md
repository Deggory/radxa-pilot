# Incremental Chimera implementation

November 6, 2026. Active project location: `sunnypilot/chimera/`.
The existing T01–T20 task identities are retained. Each slice gets appropriate
checks, a local commit and a notebook handoff before expanding the scope.

Additional November6 source evidence: [Ocelot Panda Docker review](../docs/OCELOT_PANDA_DOCKER_REVIEW.md).
Pinned current/parent targets distinguish stock Panda selection from Chimera
GPIO/acquisition. DD forwarding/version collision and health43 signedness feed
future T02/T05/T08 fixtures; no new firmware integration or task completion.

- [x] S00 Create the in-project home, retain source map/provenance and establish the sequence.
- [x] T06a Shared native USB/SPI transport interface; existing SPI backend retained, native build and offline ownership/codec checks pass.
- [x] T02a Pinned read-only native identification and profile selection; exact versions/health lengths and negative fixtures checked offline.
- [x] T06b Native USB factory/backend, exclusive pinned selection, bounded I/O and cleanup; fake USB and real-library link checks pass.
- [x] T01a Source-backed board GPIO/flash/RAM contract; physical recovery and electrical qualification remain open.
- [x] T03a Original minimal F413 startup/linker/build, inactive outputs, nine offline tests and deterministic raw image.
- [x] T02b Distinct bootstrap identity/manifest, read-only request handler/matrix and source bus/input contract; twelve offline tests pass.
- [x] T04 Pure current six-byte/XOR classical CAN codec; fourteen-test suite, source interoperability and bounded stream/error fixtures pass offline.
- [x] T03b1 Backend-driven USB clock/detached-core preparation and pure descriptor/EP0 model; sixteen offline tests pass. No packet driver/startup attachment yet.
- [x] T03b2 Ordered ARM MMIO/DWT timing backend and polling EP0 event/FIFO driver; nineteen offline tests pass. Startup/attachment and physical qualification pending.

| Task | Next deliverable | Status |
| --- | --- | --- |
| T01 | Board GPIO/reset behavior, flash/config partitions and recovery boundaries | T01a source contract complete; installed bootstub/recovery and electrical qualification pending |
| T02 | Distinct identity, legacy/current protocol profiles, RPC matrix and explicit bus/input source contracts | T02a/b complete offline; operational health/capability/config ABI and new-profile host admission remain pending |
| T03 | Minimal F413 target, reviewed support/linker and offline image budget | T03a/b1/b2 offline complete; T03b3 power/VBUS/UID/recovery prerequisites and reviewed startup/attachment next; physical qualification pending |
| T04 | Modern six-byte/XOR classical CAN USB codec with stream/vector checks | Complete offline; no endpoint/CAN-controller binding or TX permission |
| T05 | Exact identity/version/health responses, legacy F4 status adaptation and fail-disabled state | Pending |
| T06 | Native Sunnypilot USB transport and offline failure tests | Offline transport implemented (T06a/b); managed use remains T08 |
| T07 | Isolated passive receive qualification on each physical bus | Pending separate bench scope |
| T08 | Protected current/F4/Chimera managed passive lifecycle, reconnect and exclusive ownership | Pending |
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

Next board slice: T03b3 source-backed power/VBUS/UID and watchdog/recovery prerequisites,
then separately reviewed startup/service/attachment integration. See
[the packet driver](../docs/USB_PACKET_DRIVER.md). Status/capability and endpoint
binding follow. Electrical unknowns block
claims or hardware loading that depend on them; they do not erase known source
assignments or prevent bounded offline engineering.

Owner added legacy Panda compatibility on November 6. The independent host
transport boundary was extracted first; it does not depend on a flashed Chimera
image. See [the compatibility slices](../docs/LEGACY_PANDA_SUPPORT.md). T06a/b and
T02a are checked offline; legacy status, managed lifecycle and physical testing
still follow. Next host slice: exact legacy status decoding before managed use.
