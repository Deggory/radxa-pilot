# Ocelot Panda Docker review — November 6, 2026

Owner supplied Deggory/Ocelot_Panda_docker and requested teacher research with
Agent Skills, explaining historical Panda use and retained analog/relay/OBD-C.
Accepted scope is source research and durable evidence, not new driver work or
physical actions. Baseline7d749a4125affa96f260c8059384ff9b823086f6 on radxa/q8b,
clean before research. Teacher/student routers/resume/handoff/state/tasks/Q&A,
source maps and update inbox consulted first. Upstream remains held sinceNov4.

GitHub connector read-only metadata, current commit/tree, selected files,20commit
history entries, branch and Actions collections inspected. Main04b56ba0145588d91ff70e1b35b47b7f2652d4db
(May14,2026) trims to panda-only; parent98de83bb54746d057e6e4bff707eab6cd8c179d9
retains separate panda and chimera targets. Current/parent panda selects F413
but removes GATEWAY; config then defines PANDA and stock hardware detection.
Parent Chimera retains GATEWAY and actual PC2/PC3,PA2–PA6,PB0/PB1 acquisition/
output behavior. Its main.c matches Ocelot committed HEADd87892fa exactly, not
our dirty working file. CAN/USB headers also match. No inference about exact
board-addition history, installed image or physical compatibility.

Panda source has actual safety dispatch, SILENT startup, mailbox16/health43,
C1/D6 identification. DD changes forwarding, unlike current version queries.
Manual forwarding bypasses TX hook. EON-only heartbeat fallback is not enabled
by supplied target. ALLOW_DEBUG exposes all-output17. Stock harness intercept
relay is not Chimera PB0; generic channel12 voltage scaling is not calibrated
external analog health. Parent loop's request gating and B4/B5 handlers are
commented; relay follows ignition. OBD-C request/ignition is source-level accessory
sequencing, not a diagnosed/qualified connector or actuator cutoff. Older config
header lacks local write/watchdog repairs; never replace current recovery evidence.

31selected exact original files retained under [the reference directory](../../chimera/reference/ocelot-panda-docker-20261106/PROVENANCE.md). Git blob/SHA256 manifest
pins each; complete tree and selected history/remote checks retained. No debug
private signing key, restricted linker or vendor SDK copied. These are selected
attributed reference inputs, not complete buildable source or production imports.
No blanket licensing permission inferred. PROVENANCE identifies exact originals
and separates our verifier/validation. Existing source whitespace preserved.

Actual checks from Sunnypilot root:

- python3 chimera/reference/ocelot-panda-docker-20261106/verify_reference.py
  —pass31Git blob/SHA256 files, target/flag AST assignments, config preprocessor,
  compiled health43/safety_param offset39,189actual sender/parser vectors over
  3024bytes and signedness fixture C-1/Python65535. Python3.12.3/native compiler;
  no Panda import/constructor, device enumeration or SCons execution.
- .venv/bin/ruff check chimera/reference/ocelot-panda-docker-20261106/verify_reference.py
  —pass. Initial macro fixture missed compiler trailing whitespace; corrected
  exact macro-name whitespace handling. Ruff string concatenation corrected.
- Ocelot dirty39/all19previous pinned hashes and clean archive verified unchanged;
  no tracked diff under active chimera/firmware/, native pandad or opendbc.

Source-driven development, documentation/ADRs, Git and review skills used; source
inspection via rg/selected ranges and host-only probes is appropriate. No new
REA provider/binary analysis claimed. Review and useful adaptation boundaries
saved in [the review](../../chimera/docs/OCELOT_PANDA_DOCKER_REVIEW.md). No unrelated VCDS finding from this source study.

Research does not complete another implementation task. Next T03b2 remains real
ordered MMIO/timing backend and event/FIFO/EP0 packets with cancellation/reset/
STALL/attach prerequisites. Follow with status/endpoints/admission; later inputs,
Core Config, policy, recovery and relay/OBD-C qualification. Canonical DBC/bus
identities unchanged. No Docker/full firmware build, hardware/flash/CAN/relay/
actuation/install/upstream reference update/push. Source snapshots are inactive
research evidence and do not enter firmware build. Teacher/student Q&A18 and
state/topic/worklog/roadmap synchronized; local research commit after checks.

Closeout: memory verifier passes138documents/428relative links/246optional
workspace links/8source repositories/4254indexed entries;57active Chimera/provenance
links resolve. Receipt Ai/Evidence/ocelot-panda-docker-20261106.json records exact
checks. Authored-file diff checks exclude byte-preserved original source inputs;
originals are checked against Git blob and SHA256 pins, not reformatted.
