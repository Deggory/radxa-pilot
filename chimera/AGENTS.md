# Chimera implementation instructions

Follow the project AGENTS.md, Ai/REPO_RULES.md and Ai/HANDOFF.md. Read the
Chimera topic and Q&A through Ai/ROUTER.md before starting. In the full Comma
workspace, consult the teacher evidence before declaring information missing.

This directory is the active implementation home. Keep firmware here and host
integration in the existing Sunnypilot modules. Do not add a nested Git repo or
depend on symlinks to workspace reference folders. Preserve the original dirty
Ocelot checkout and archived evidence; import only reviewed, attributed inputs.
Do not copy its restricted legacy linker script into the implementation.

Follow tasks/plan.md in small verified commits. Retain all three physical bus
identities, direct inputs, onboard relay and OBD-C interfaces. The canonical
RetroPilot CAN definition is workspace retropilot/dbc/; record its version and
explicit routing when importing required definitions. No silent protocol fork.

Keep board identity distinct from stock H7 Panda. Guard every eventual CAN TX
path with MCU policy, including generated reports and maintenance traffic.
Offline implementation does not authorize flashing, relay operation or vehicle
actuation. Record source pins, actual checks and limits in the project notebook.

Owner transport decision, November 6: Radxa connects to Chimera/selected legacy
Panda over USB only. Do not add SPI wiring, probing or automatic fallback to this
deployment. T08 must replace inherited SPI construction with qualified pinned USB
selection; refusal/disconnect must remain disconnected instead of trying SPI.
Owner correction, November6: remove SPI from pandad source, build, classes,
constructors, discovery and fallback paths. Earlier generic-SPI preservation
wording is superseded. Keep pinned USB as its only backend/entry on all platforms.
Retained source/firmware statistics named spi are protocol data, not a transport.
