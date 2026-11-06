# Incremental Chimera implementation

November 6, 2026. Active project location: `sunnypilot/chimera/`.
The existing T01–T20 task identities are retained. Each slice gets appropriate
checks, a local commit and a notebook handoff before expanding the scope.

- [x] S00 Create the in-project home, retain source map/provenance and establish the sequence.
- [x] T06a Shared native USB/SPI transport interface; existing SPI backend retained, native build and offline ownership/codec checks pass.
- [x] T02a Pinned read-only native identification and profile selection; exact versions/health lengths and negative fixtures checked offline.
- [x] T06b Native USB factory/backend, exclusive pinned selection, bounded I/O and cleanup; fake USB and real-library link checks pass.

| Task | Next deliverable | Status |
| --- | --- | --- |
| T01 | Board GPIO/reset behavior, flash/config partitions and recovery boundaries | Next; known GPIO/build facts already recovered |
| T02 | Distinct identity, legacy/current protocol profiles, RPC matrix and explicit bus/input source contracts | Partial: T02a selector complete; full RPC/new Chimera identity and source contracts pending |
| T03 | Minimal F413 target, reviewed support/linker and offline image budget | Pending |
| T04 | Modern six-byte/XOR classical CAN USB codec with stream/vector checks | Pending |
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

Next slice: T01 source-backed board/flash contract. Electrical unknowns block
claims or hardware loading that depend on them; they do not erase known source
assignments or prevent bounded offline engineering.

Owner added legacy Panda compatibility on November 6. The independent host
transport boundary was extracted first; it does not depend on a flashed Chimera
image. See [the compatibility slices](../docs/LEGACY_PANDA_SUPPORT.md). T06a/b and
T02a are checked offline; legacy status, managed lifecycle and physical testing
still follow. Next host slice: exact legacy status decoding before managed use.
