## QA-20261108-24 — Which host file talks to a connected Panda?

**Date:** November 8, 2026 UTC.
**Owner question (faithful quote):** "when we connect panda to comma or rdxa which file does it tallk to ,is it pandad or any other file it connect".
**Answer:** Yes: pandad is the running host service responsible for communication. For a USB connection, compiled PandaUsbHandle code in panda_usb.cc uses libusb/the OS USB stack to open/claim and transfer data. The manager starts pandad.py, which starts native pandad; main.cc is its entry and session/protocol code handles the selected firmware. Normal pandad.cc coordinates CAN receive/sendcan, health, heartbeat and safety, and panda.cc implements device operations. card.py/car interfaces exchange internal can/sendcan messages, rather than owning the USB connection; model/UI do not talk directly to Panda. In our current Radxa branch the launcher enters --usb-status, accepts F4v17 only and publishes passive can/isolated diagnostics; normal transmit/pandaStates/control threads are not started. Original Chimera's native session remains proposed. Internal comma transport depends on hardware; diagnostic Python tools are an alternative client, not an extra stage required in native traffic.
**Evidence/source pins:** Sunnypilot baseline b9bbcbb096a30d6d7c05343b68d14235f541cb51; upstream reference8cf6ff9a33c94bdf2fcb02e228a9aef1a7e6dc7f. Eight current source hashes in student Ai/Evidence/panda-host-path-20261108.json; process_config.py, pandad.py, main.cc, panda_usb_status.cc, panda_usb.cc, panda.cc, pandad.cc and card.py traced. Existing comparison topic extended; normal reference launcher/main/thread entry read separately from local modifications.
**Status/limits:** Explanation and notebook update only; source/notebook/QA/whitespace checks. No runtime USB ownership test, hardware/device/flash/config/CAN action, build/test suite, upstream update or push. No active-control support or completed original-Chimera integration claimed. Rewrite remains halted; unanswered entries retained.

---

## QA-20261108-23 — Original Chimera, new rewrite and Panda capabilities

**Date:** November 8, 2026 UTC.
**Owner question (faithful quote):** "now use all the skill u learn ,tell me about chimera old and new panda ,wat new have that old dont have ,teacher tell wat u knw about panda".
**Answer:** Distinguished older black/F413 Panda, original F413 Chimera, modern red/H725 Panda and our unfinished halted F413 rewrite. Panda bridges host USB and CAN, enforces the configured firmware safety policy and reports hardware/bus state; the host runs driving AI. Current Panda adds a model-aware safety dispatcher, richer fault/per-bus diagnostics, layout identity and modern checksummed variable CAN framing relative to the preserved original Chimera. H725 adds hardware CAN FD, outside our project scope. Stock older Panda also had safety rules, so safety is not red-only. Original Chimera retains retrofit direct/analog/pulse inputs, config/JSON, relay and OBD-C; its TX path lacks modern safety hooks. Its DC handler only changes a request variable, while saved relay GPIO follows ignition; no heartbeat-driven physical cutoff is proven. The new rewrite has tested offline USB/codec/state foundations but actual startup stays held and full operational CAN/input/config/safety/board validation remains incomplete. Current native Radxa entry is passive F4v17; native old-Chimera session remains proposed. No implementation resumed.
**Evidence/source pins:** Baseline efe4e9c951ebd1a994cc04a31ef36533bda65e4d; Panda8a16e089b88593914823743df29e1c30b7dd3e00, opendbc150f937198ceab43c43b39f94b9bdea63fcb633c; student Ai/Knowledge/PANDA_CHIMERA_COMPARISON.md and Ai/Evidence/panda-chimera-comparison-20261108.json. Fresh current-source comparison,31inventory hashes and76preserved legacy files match; four rewrite hashes pinned. Official pinned Panda README, comma safety and Chimera hardware wiki reopened. Existing teacher graph node/neighborhood used only as a source route.
**Status/limits:** Explanation and synchronized notebook update only. Source/notebook/QA/whitespace verification; no fresh firmware/native tests/build, REA artifact/runtime claim, hardware/USB/CAN/relay/flash, model, upstream update or push. Installed legacy image/source equivalence remains unresolved; rewrite remains halted; classic CAN scope retained. Skill selection is task-relevant, not blanket activation of unrelated skills. Existing unanswered entries preserved.

---

## QA-20261108-22 — Audit the teacher, then shut down Radxa

**Date:** November 8, 2026 UTC.
**Owner request (faithful quote):** "audit the teacher wiht this skill if it learn this skill after that shutdown the rdxa".
**Answer:** Installed and adopted both pinned skill packages, added teacher/student operating instructions, then audited them with Understand Anything knowledge analysis and Unlazy. All five completion gates passed and were re-executed successfully: 565 pinned installed files, eight evidence-retrieval cases, a source-pinned 11-article graph with 41 nodes/45 edges, notebook/QA/reference preservation, and a committed clean handoff. Independent review found and fixed hook wording, stale update authorization and preview qualification; excerpt metadata was corrected. The native notebook format needs a labelled derived audit view. This verifies bounded tool use and durable instructions, not model training, the full archive or future compliance. The full TypeScript code graph/dashboard remains untested; pnpm is absent. The authorized shutdown follows saved closeout; its OS reply belongs in the receipt.
**Evidence/source pins:** Teacher Ai/Reports/teacher-skills-audit-20261108 (BASELINE.json, VIEW_SOURCES.json, derived teacher-view graph, independent BEHAVIOR_REVIEW.md, GATES.md and final AUDIT.json); student Ai/Reports/teacher-skills-audit-20261108/README.md. Same immutable tool pins as QA21. Actual outcomes and shutdown reply belong in the final receipt, not an invented physical power-off claim.
**Status/limits:** Bounded audit completed: 5 met, 0 unmet, 0 abandoned; all five reverified. Saved teacher/student records and local commit; no push. Host shutdown is authorized as the final action and recorded after the OS reply in the teacher AUDIT.json; physical power-off cannot be observed independently here. No application, firmware/model, CAN/vehicle, upstream update or resumed halted implementation. Existing unanswered entries preserved.
---

## QA-20261108-21 — Adopt skills and strengthen the teacher

**Date:** November 8, 2026 UTC.
**Owner requests (faithful quotes):** "okay use these skills ,teach our teacher to do this ,it have all the data about this project ,i"; "r teacher should act like a god ,".
**Answer:** Adopted Understand Anything and Unlazy as task-relevant workspace tools. Installed pinned packages with all supporting files and made the nine Understand Anything skills and Unlazy discoverable. Added a teacher operating guide and student copy: recover routed evidence before asking again, use focused maps and compact observable gates, complete authorized capabilities autonomously, keep scope and verification honest, and save durable handoffs. This is persisted instruction and tested tool use, not background model training or omniscience. The existing archive contains substantial evidence but does not prove every fact is current or that every conversation was saved.
**Evidence/source pins:** Understand Anything a6ea4024767df85ce4f99140d4f12ecfc5a81eb6 (plugin2.9.8); Unlazy16671491f6679ad9378f52604d3bc2415b4120c7 (source2.1.0). Teacher manifest Ai/Tools/teacher-skills-installation.json; both Ai/Knowledge/TEACHER_WORKFLOW.md copies, policy topics and AGENTS pointers. Baseline Sunnypilot c83e113b921dc8d000d02d312f54e5c2934e9a08.
**Status/limits:** Installation and instructions adopted; supersedes QA20 proposed-only status from earlier today. Actual knowledge/gate audit and results recorded separately in QA22. Full TypeScript code graph/dashboard runtime not built (pnpm missing); Python knowledge analysis and Node gate checker are the exercised paths. No automatic Stop/commit hooks, update changes, resumed Chimera implementation, firmware/model/vehicle work or push. Existing unanswered items retained.

---

## QA-20261108-20 — Understand Anything and Unlazy fit

**Date:** November 8, 2026 UTC.
**Owner question (faithful quote):** "can understand-anythiing and unlazy skill help our project".
**Answer:** Yes, selectively. Understand Anything could give us a browsable source architecture map for the camera/model/messages/UI path or a selected CAN subsystem. Unlazy could attach explicit observable acceptance checks to a substantial deliverable and expose unfinished work. They complement existing skills, Ai memory and source/REA evidence. Full workspace indexing and deep task trees could add cost and repeat our earlier fragmentation problem; prefer a small pilot and compact gates. Unlazy's Stop hook is Claude Code specific, and its checker proves only declared checks, not that the checks capture the intended outcome. Neither establishes working hardware or vehicle integration.
**Evidence/source pins:** Understand Anything `a6ea4024767df85ce4f99140d4f12ecfc5a81eb6`, pinned README and understand/SKILL.md; Unlazy `16671491f6679ad9378f52604d3bc2415b4120c7`, pinned README and SKILL.md. Teacher receipt: Ai/Reports/skills-fit-20261108/SOURCES.json; student topic: Ai/Knowledge/SKILLS.md. Compared with existing module maps, validation workflow and saved November 7 halt/delay explanation. Project baseline `b2bc9c24030454a3cd313a31928dc7ea9717f044`.
**Status/limits:** Source assessment and recommendation completed; adoption remains proposed. Neither candidate installed or executed; no hook, graph, gates, dependencies, application code, model, firmware, hardware, update or push changes. No Radxa/ARM64 runtime qualification or measured benefit. Notebook/QA/whitespace checks recorded in session. Existing unanswered entries preserved separately.

---

## QA-20261108-03 — See all the things Panda does

**Date:** November 8, 2026 UTC.
**Owner request (faithful quote):** "see all the thing panda does".
**Answer:** Inspected current Panda normal firmware, bootstub/flasher, board callbacks, Python API and local pandad, with historical black-board context. Functions include multi-bus CAN RX/TX, framing/queues/checksums/receipts, routing/multiplexing/bitrate/loopback, MCU safety and driver override, heartbeat/liveness, harness/ignition, health/per-bus statistics, watchdog/register/interrupt/fault diagnostics, identity/version/signatures, signed boot and flash/DFU recovery, power saving and board-specific peripherals. Host pandad translates CAN/cereal and manages status/config/heartbeat; MCU does not run driving AI. Red lacks several internal-board peripherals; historical GPS/serial functions are version-specific. Complete local source command inventory:35normal vendor cases,9flasher cases, plus ordinary USB/CAN bulk streams. Current local launcher still runs passive F4v17 observation only, not dormant normal send/control threads; old Chimera native session remains proposed. Found stale host command methods E0/E4/FB and Python F4 absent in the pinned normal firmware handler; existing dormant connect also requests FD-auto, which must stay out of our classic-only route. No compatibility fix was made. Old Chimera's own sensor/config/relay behavior and missing modern safety/status contract remain distinct.
**Evidence/source pins:** Sunnypilot560e3ea87c0961bb9da2cf550b154011ae985184; Panda8a16e089, opendbc150f9371; student Ai/Knowledge/PANDA_FUNCTIONS.md and Ai/Evidence/panda-functions-20261108.json retain31source hashes, command/method inventories and board/runtime limits. Fresh official pinned Panda README and comma safety docs read. Prior F4 study69a2d3be is reference, not an installed firmware claim.
**Status/limits:** Source inventory only, not exhaustive proof of every car mode/historical board/body target. Static command-count/comment-exclusion and notebook/QA/whitespace checks; no test-suite rerun, firmware/native build, hardware/USB/CAN/flash/config/update/push. Classic CAN only, old firmware preserved, new rewrite halted; native RX remains next proposed capability. Existing unanswered items preserved.

---

## QA-20261108-02 — Do black/red Panda and our project need these safety inputs?

**Date:** November 8, 2026 UTC.
**Owner question (labelled paraphrase):** Asks whether the preceding safety-input/check table applies to black or red Panda and whether these are the inputs we need; repeats the full table.
**Answer:** Yes, the general safety requirements apply to both black/F4 and red/H7 Panda when using compatible vehicle-specific safety firmware. Actual supported models, signals and checks depend on the firmware/model, not board color. For our project, active steering/gas/brake control requires verified feedback/driver override, message integrity/freshness, command limits and timing, heartbeat and MCU enforcement. This is classic-CAN work; CAN FD is not required. These are information/behavior requirements, not necessarily separate new sensors: existing CAN or qualified Chimera inputs can supply relevant facts, but absent signals must not be invented or supplied as healthy zero. Exact torque-versus-angle inputs depend on selected actuator/safety design. Receive-only monitoring needs valid identification/decoding/bus/freshness/error handling, but does not require an active actuator-control profile just to receive/display data. Old Chimera has no modern safety hook enforcement and local RetroPilot has no qualified active production profile; a USB adapter alone does not fill that gap. No active implementation or hardware action authorized/inferred from this explanation.
**Evidence/source pins:** Sunnypilot a9c6a3a45c4392b1af63483e3997534df36a929b; Panda8a16e089/opendbc150f9371 safety.h TX checks, retropilot.h NULL active-profile initializer, car/retropilot/interface.py noOutput/dashcamOnly, and original chimera_old can_send. Reviewed legacy F4 reference ajouatom/openpilot69a2d3be, student Ai/Reports/carrot-wip-panda-20261106/README.md; prior QA-20261108-01 safety input evidence. All are source/reference evidence, not installed-board tests.
**Status/limits:** Source explanation/notebook only; no code/build/device/vehicle/test-suite rerun/update/push. Notebook/QA/whitespace checks only. Vehicle feedback availability, actuator calibration and exact installed firmware remain unqualified. Preserve classic-only scope, old firmware and halted new rewrite. Existing unanswered items preserved.

---

## QA-20261108-01 — What Panda safety rules take as inputs and require

**Date:** November 8, 2026 UTC.
**Owner question (faithful quote):** "Panda safety rules wat doe it take".
**Answer:** Panda MCU rules take the selected model/parameter, live CAN-derived vehicle state (model-dependent speed, brake/gas, driver torque/angle, engagement/cancel), requested outgoing CAN frames, timestamps/history and host heartbeat. They check required received-message identity/integrity/counters/freshness and allowed outgoing ID/bus/DLC plus applicable command magnitude/rate/driver-override rules. Limits and signal definitions are generally compiled into the chosen firmware model; the USB parameter only selects model-defined options. The result permits or blocks a frame and updates control/fault state, not merely a relay switch; no camera/AI model input goes directly to these safety hooks. For our classic-CAN Chimera project, implementing this requires canonical DBC/bus mapping, measured/calibrated actuator and feedback limits, defined override/timeout behavior, and hooks actually enforced in MCU RX/TX paths with verification. Current local RetroPilot safety has a parameterized active engine, but its production initializer passes no qualified profile; the car interface remains noOutput/dashcam-only. It is not installed/enforced by old Chimera's current can_send path. USB adaptation alone cannot supply that enforcement.
**Evidence/source pins:** Sunnypilot8fde793454f5908e88f6210d9c56b3cd41858212; Panda8a16e089b88593914823743df29e1c30b7dd3e00 main.c heartbeat and drivers/can_common.h safety_tx_hook; opendbc150f937198ceab43c43b39f94b9bdea63fcb633c safety/{safety.h,declarations.h,modes/retropilot.h,modes/retropilot_active.h}, car/retropilot/interface.py. Official https://docs.comma.ai/SAFETY/ and commaai/opendbc README opened/searched November8 support driver override and bounded actuation concepts. Student CHIMERA_OLD_PANDAD topic extended.
**Status/limits:** Source/doc explanation only; no implementation, test rerun, native/firmware build, device/vehicle/relay/CAN action, update or push. Notebook/QA/whitespace checks only. No calibrated physical profile or installed-board safety qualification. Classic CAN only; old retained/new halted. Existing unanswered items preserved.

---

## QA-20261107-23 — Meaning of DC plus safety model and parameter

**Date:** November 7, 2026 UTC.
**Owner question (faithful quote):** "0xDC + safety-model number + model parameter wat does this means".
**Answer:** The plus signs mean three fields of one USB control request, not arithmetic: bRequest=0xDC identifies set-safety, wValue is a16-bit safety-rule-set ID, wIndex is a16-bit model-specific configuration value. This safety model is MCU firmware rules, not the AI driving model. Parameter meanings depend on the selected rules, often option bits; it is not a universal steering/torque value. Example DC/19/0 selects noOutput with parameter0 on compatible Panda firmware; model0 is silent, model2 is Toyota, model19 is noOutput in this pinned enum. Selecting a rule set is not an engagement or steering command. Saved old Chimera interprets19 by clearing relay_req_usb, ignores the model parameter in that handler and installs no Panda safety hooks; its ignition-driven relay caveat from QA21/22 remains. No USB request was sent.
**Evidence/source pin:** Sunnypilot6bcc5cd95484b3889bdf87399583742eda065c75; host openpilot/selfdrive/pandad/panda.cc:42, panda_usb.cc:121; Panda8a16e089 board/main_comms.h:225; opendbc150f9371 car/car.capnp SafetyModel and safety/modes/honda.h parameter flags; old chimera main.c:335. Local source reread; no REA artifact/runtime result needed.
**Status/limits:** Explanation/notebook only; no implementation, test rerun, USB/relay/device/config/build/flash/update/push. Classic CAN only; retained old firmware and halted rewrite unchanged. Existing unanswered items preserved.

---

## QA-20261107-22 — Does Chimera safety switch off a relay and disconnect?

**Date:** November 7, 2026 UTC.
**Owner question (faithful quote):** "so u mean the safety in chimera u say it turns the relay off and disconnect".
**Answer:** No automatic safety disconnect is established in the preserved source. DC and heartbeat expiry change relay_req_usb, but the operative loop ignores that request condition and sets PB0 relay_on according to ignition. Therefore DC0/noOutput or loss of host heartbeat cannot be claimed to switch this relay off while ignition remains on. Hardware documentation describes the onboard relay as switching12VR power on CAN0 ports1–3, not opening CANH/CANL or disconnecting USB; powering a connected Core off is a different effect, with device/installation-dependent behavior. Panda safety rules also gate CAN commands and are not merely relay switching. This clarifies QA21 and the owner's interpretation; no claim of tested physical disconnect.
**Evidence/source pin:** Sunnypilot c1b625eeb854d90bfd04ad082d0a36b8c4d3836a; chimera_old/firmware/chimera/main.c:335,722,1026–1044. Ocelot hardware/chimera/README.md and official https://wiki.retropilot.org/index/hardware/chimera freshly opened November7,2026: Power & IO, CAN0 and pinout12VR/CANH/CANL.
**Status/limits:** Source/doc explanation only; notebook validation, no test-suite rerun, hardware/relay/USB action, code change, update or push. Installed-image identity and actual wiring remain unverified. Classic CAN only; old firmware retained, new rewrite halted. Existing unanswered items preserved.

---

## QA-20261107-21 — Classic CAN only and exact 0xDC behavior

**Date:** November 7, 2026 UTC.
**Owner question/direction (faithful quote):** "we dont want can fd in our project ,Command `0xDC`Changes relay-request variableSets Panda safety policy tell me about his".
**Answer:** Owner scope is classic CAN only (0..8 payload bytes); CAN FD is not a project requirement. This records scope, not permission for unrelated source removal. 0xDC is a vendor USB command; firmware determines its meaning. Current host set_safety_model sends mode as wValue and parameter as wIndex. Panda calls set_safety_mode, installs/initializes safety hooks with fallback to SILENT on unsupported mode, configures intercept relay/CAN state and reinitializes CAN. The selected hooks check allowed TX and RX/forwarding behavior; limits are model-dependent and relevant to classic CAN. Old Chimera instead sets relay_req_usb=0 for values0,3,19 and1 for other values; it does not install a model or use wIndex in that handler. Crucially its saved main loop comments out the request-based condition and writes PB0 relay_on from ignition_line OR ignition_can. Thus changing relay_req_usb through DC is not a verified relay switch in this source. Missing-heartbeat handling clears that variable but cannot be assumed to drop an ignition-driven relay. Old health safety_mode=17 is hard-coded, not confirmation a modern safety policy was installed. Current native Chimera USB backend blocks DC and other OUT writes.
**Evidence/source pins:** Sunnypilot ae145e4c58c9f154a46cff85b2d2d4b11742425b, Panda8a16e089, opendbc150f9371; chimera_old/firmware/chimera/main.c:335,722,1026,129; openpilot/selfdrive/pandad/panda.cc:42 and panda_usb.cc:121; panda/board/main_comms.h:225, board/main.c:31, board/drivers/can_common.h safety_tx_hook; opendbc safety/safety.h and car/car.capnp enum0/3/19. Existing report Ai/Knowledge/CHIMERA_OLD_PANDAD.md extended with scope and exact semantics.
**Status/limits:** Source explanation and owner-scope recording only. No firmware/source implementation, relay/USB/device/CAN action, build, test-suite rerun, update or push. Notebook checks only. Exact installed-board image/source match and electrical relay behavior remain unverified. Original firmware preserved; new rewrite halted; native old-Chimera adapter still proposed. Existing unanswered items retained.

---

## QA-20261107-20 — USB protocol in old Chimera versus current Sunnypilot

**Date:** November 7, 2026 UTC.
**Owner question (faithful quote):** "see wat is the usb protocol old chimera and sunnypilot have now".
**Answer:** Both use a vendor-specific USB interface, endpoint0 control requests, CAN receive bulk-IN0x81 and CAN send bulk-OUT0x03. Old Chimera uses little-endian fixed16-byte CAN mailboxes:4-byte identifier/flags,4-byte DLC/bus/timer,8-byte payload storage. It carries0..8payload bytes with no additional per-record XOR byte (USB link integrity and CAN payload CRCs are distinct). Modern Panda wire format uses a6-byte header (FD/bus/DLC byte,4identifier/flag bytes,1XOR checksum byte) plus variable payload; an8-byte CAN message occupies14bytes versus Chimera16. The current format supports CAN FD payload lengths up to64, but our passive F4 parser deliberately admits classic CAN only. Health requestD2 returns43bytes for old Chimera,49for current Panda,59for our selected Carrot F4v17 profile. Shared D6 returns firmware version; Chimera lacks C1 hardware-type and DD protocol-version handlers, while current DD returns two32-bit health/CAN header hashes. DC changes relay_req_usb in old Chimera versus installing a safety model in Panda. Same endpoint or opcode does not imply identical semantics. Sunnypilot identification recognizes all three pinned profiles; actual native --usb-status currently admits F4v17 only, and the managed Panda constructor admits CURRENT only. Old Chimera Python decoder/monitor exists, but native Chimera session remains proposed.
**Evidence/source pins:** Sunnypilot56b073934605c7fe2e2e39b06a17ca0ee1704ec7; Panda8a16e089b88593914823743df29e1c30b7dd3e00; opendbc150f937198ceab43c43b39f94b9bdea63fcb633c. Inspected chimera_old/firmware/chimera/{usb.h,main.c}, host pandad/{chimera_protocol.py,panda_identification.cc,panda_usb.cc,panda_usb_can.cc,panda_usb_status.cc,panda.cc,panda_health.h}, panda/board/{health.h,main_comms.h}, opendbc safety/can.h. Student Ai/Knowledge/CHIMERA_OLD_PANDAD.md has the comparison.
**Status/limits:** Source explanation only; no implementation, device access, firmware build/flash, protocol change or new hardware qualification.22passing tests from QA19 are prior evidence, not rerun this turn. Notebook/link/whitespace and Q&A synchronization checks only. Installed image/source match still unresolved; preserve old firmware and halted rewrite. Existing unanswered items retained.

---

## QA-20261107-19 — Keep old Chimera and connect it to Sunnypilot pandad

**Date:** November 7, 2026 UTC.
**Owner question/direction (faithful quote):** "see we will keep chimera_old and later improve it ,see how we can connect this to sunnypilot pandad ,".
**Answer:** Keep original firmware and adapt native pandad on the host. Existing PandaUsbHandle already recognizes pinned original Chimera and permits D6/D2 plus CAN bulk-IN. Python chimera.py/chimera_protocol.py already decode its mailbox16/health43 and publish can. Native PandaUsbStatusSession currently accepts F4v17 only, and managed Panda accepts CURRENT only. Proposed next capability is a Chimera-specific native session/decoder and profile-aware raw diagnostics, followed by disconnect/reconnect and separately qualified managed status. No need to rewrite firmware for that observation path. Full control is separate: old 0xDC changes a relay request rather than installing modern safety policy; saved loop actually drives relay from ignition, and old can_send has no modern safety hook. Raw health placeholders/safety17 cannot become modern healthy status. Preserve bus numbers; local CAN1 sensor reports are not automatically a USB sensor feed or host2 data.
**Evidence/source pin:** Sunnypilot5722805f8aa185ab4cf19a438bdee771dca53b55; student Ai/Knowledge/CHIMERA_OLD_PANDAD.md and Ai/Evidence/chimera-old-pandad-route-20261107.json pin inspected host/firmware source hashes. Canonical and packaged DBC SHA b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67.
**Implemented/proposed:** Existing USB/Python pieces verified; native Chimera integration is proposed, not implemented this turn. Fresh22offline tests pass; all76legacy files match manifest. No live USB, firmware build/flash, CAN TX, manager launch, REA runtime result, update or push. Exact installed-image/source match, wiring and speed units remain open. New firmware rewrite stays halted; original improvement deferred. Existing unanswered items preserved.

---

## QA-20261107-18 — Older Panda, original Chimera and red Panda comparison

**Date:** November 7, 2026 UTC.
**Owner question (faithful quote):** "compare the old panda i chimmera and new panda ,i knw it is red panda ,compare".
**Answer:** Interpreted older Panda as black/F4 following QA17; other old colors/revisions need separate identification. Black Panda and original Chimera use STM32F413/Cortex-M4 and classic CAN; red Panda uses STM32H725/Cortex-M7 and supports classic CAN plus CAN FD. These are CAN interface MCUs, not the host running the driving model. Original Chimera adds its own analog/pulse/button inputs, persistent configuration and relay/OBD-C behavior; stock Panda harness behavior is different. All three have USB host paths, but USB alone does not make their firmware protocols interchangeable. Original Chimera retains mailbox16/health43; Panda protocol versions and status sizes depend on the installed firmware. Red H7 firmware cannot run on the F413. A firmware rewrite on the same F413 cannot add hardware CAN FD. Our new chimera/ is an unfinished, halted F413 rewrite, while chimera_old/ preserves the original; new source is not a red-Panda hardware upgrade. A host adapter for retained original firmware is a possible route, not a completed modern Sunnypilot integration.
**Evidence/source pins:** Sunnypilot ab07117573529c2e54d74f47eb3d66c0542f5506; Panda submodule 8a16e089b88593914823743df29e1c30b7dd3e00 README.md, SConscript and board/boards/red.h; chimera_old/firmware/SConscript, chimera/{main,can}.h (application main.c), drivers/clock.h, config.h, README.md and SOURCES.json; chimera/firmware/main.c and docs/LEGACY_PANDA_SUPPORT.md. Original source provenance Ocelot d87892fa plus saved local changes. QA17 retains saved black/F4 build evidence. Official pinned Panda README/red.h also opened on the web this turn.
**Status/limits:** Source comparison only; no firmware/host implementation, build, flash, device or vehicle test, REA runtime result, upstream change or push. Exact Jetson author's physical board/chip marking and exact C2 installed-image source remain unresolved. Modern Chimera stays halted. Notebook checks only; earlier firmware-test results were not rerun. Existing unanswered items preserved.

---

## QA-20261107-17 — Jetson Panda color/STM32 and Sunnypilot fork

**Date:** November7,2026 UTC.
**Owner question (faithful quote):** "can u see if he used black panda or red panda u check stm32  ic which he used ,and he used sunnypilot there rt".
**Answer:** The pinned overlay author specifies Panda H7 over USB-A and tooling
selects panda_h7.bin.signed. This points to the red/H7 Panda family. Official
Panda8a16e089 README specifies STM32H725, red.h identifies Red Panda(STM32H7),
and local official SConscript selects STM32H725xx for H7. His exact physical
PCB revision/chip marking is not shown by the inspected overlay sources, so
STM32H725 is the standard target identification, not a confirmed chip reading
from his particular board. The older black/F4 target uses STM32F413; saved
Carrot69a2d3be F4 board detection/build source corroborates that distinction.
Our original Chimera source selects STM32F413xx as well, but is its own board.
Yes: locklist names custom sunnypilot-cuda, AGXOrin branch. README labels its
September24 SP vehicle validation as an author claim. Multiple fork families
are supported; exact matched upstream Sunnypilot commit remains unresolved.
**Evidence/source pins:** feiyang2025/jetson-cuda-overlay076d73bf9a2e055c83fbe9b2a3c16a8383519ba4
USAGE.md:7, panda/env.py, tools/locklist/sunnypilot-cuda.txt:1, README.md:21;
commaai/panda8a16e089b88593914823743df29e1c30b7dd3e00 README.md:3,
board/boards/red.h:6 and SConscript H7 flags; saved Carrot SConscript/STM32F4 board.h.
Pinned author files and official Panda README/red.h were freshly reread via GitHub.
An inherited H735 linker comment is not stronger chip evidence than the explicit
H725 build flag/README, and is not an author-board identification.
**Status/limits:** Source explanation only, no implementation or hardware test;
modern Chimera stays halted, chimera_old/ unchanged. No exact physical chip/board
proof or fresh Jetson validation. Existing unanswered items preserved.

---

## QA-20261107-16 — How Jetson CUDA overlay used Panda USB

**Date:** November7,2026 UTC.
**Owner question (faithful quote):** "teacher there was a project jetson cuda tell me how he used panda usb there ,".
**Answer:** Identified feiyang2025/jetson-cuda-overlay, reviewed pin076d73bf.
Its author specifies an H7 Panda connected to AGX Orin over USB-A. Existing Panda/
pandad and vehicle interfaces carry CAN; CUDA/TensorRT run model computation.
patch_panda_spi.py gates SpiDevice opening behind PANDA_SPI_ENABLE=1 and widens
DFU SPI exception handling; default is USB-only, with an opt-in SPI escape hatch.
The author describes spidev permission/crash/hang reasons; these are source claims,
not reproduced hardware failures. repair_protocol.py aligns selected host/C header
and Python decoder fields to that rig's v17/57-byte health ABI and adjusts older
pandad fields/flashing gates only where its anchors match. sync_firmware.py copies
one selected H7 firmware artifact across fork board/obj files (backup first);
it does not itself flash hardware. It aims to prevent fork switching from selecting
different firmware; a target pandad can still flash according to its own logic.

**Relevance/status:** The transferable approach is explicit USB plus an exact host
protocol adapter for retained firmware. H7 v17/57 is distinct from original Chimera
mailbox16/health43 and Carrot F4v17/health59. Its H7 firmware/patches are not a
Chimera implementation or proof of compatibility. Our two Chimera folders and host
source remain unchanged; modern work stays halted. This is explanation/source
review only; no patch execution, device access, installer, update or push.
**Evidence:** Teacher jetson/reports/PLATFORM_INTEGRATION.md, student
Ai/Knowledge/JETSON_HARDWARE_REFERENCE.md, and four pinned source files freshly
read via GitHub connector: USAGE.md, patch_panda_spi.py, panda/repair_protocol.py,
panda/sync_firmware.py. Source commit076d73bf9a2e055c83fbe9b2a3c16a8383519ba4.
No new physical Jetson test or REA result. Existing unanswered items retained.

---

## QA-20261107-15 — Copy original Chimera into chimera_old first

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "make new folder chimera_old we will keep the chimera from c2 ,copy wat is needed  in sunnypilot do this first".
**Answer:** Created sunnypilot/chimera_old/ with76byte-identical legacy source,
shared headers/drivers/CMSIS/startup/config/build references/public certificates
and selected historical Chimera/bootstub recovery files. Added README, instructions
and per-file source/SHA256 manifest. No modern firmware or host code changed.
**Evidence/source pin:** Baselinee71640be3; Ocelotd87892fa plus saved local changes,
matching19pinned sources and39dirty entries; recovery ZIP8158f29132e88bff946cbe23b72d269fa2e6aeb4d6ca5aba7b9539ac04ec043c;
Chimera imagee35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b.
See sunnypilot/chimera_old/SOURCES.json for all76verified files.
**Status/limits:** Copy completed only. C2-era is owner terminology; exact installed
image match and source for de193215490b4906aa74aae6aa426b8f4740f3fa remain unverified.
Source retains known local changes and differs from the historical image's source.
Restricted Atollic linker, private signing keys and generated objects excluded;
not a complete verified rebuild. No build/flash/device/host integration/update/
push. Modern chimera/ remains halted. Earlier unanswered items preserved. Next
host adaptation is not implemented or automatically started by this copy request.

---

## QA-20261107-14 — Halt Chimera and explain the delay

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "hault this ,this is is taking too uch time why".
**Answer:** Implementation halted. Work was split into too many small USB bring-up
increments, with excessive repeated auditing, documentation and handoffs. This
made visible progress toward actual CAN data exchange too slow. Tests establish
offline behavior; they have not completed board startup or the operational CAN
path. The workflow should have grouped larger useful capabilities earlier.
**Evidence/source pin:** e71640be3f15262670e38442ec28b3f5f5a7f823;
chimera/docs/USB_LIFECYCLE.md and its saved36-test/92-scenario receipt. The timing
explanation is an assessment of the work pattern, not a measured time breakdown.
**Status/limits:** Stopped at owner's request; earlier next steps are suspended.
No automatic resumption, new implementation/tests/hardware/update/push. Stop notes
only saved during this turn. Existing unanswered questions remain preserved.

---

## QA-20261107-13 — Deliver a larger USB capability beyond25%

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "Next: handle USB controller events, then implement controlled attachment and disconnect/reconnect behavior.
 we hvae ben doing this for long time ,we need to improve more thna 25%".

**Answer:** Implemented the complete offline USB control lifecycle through main,
service and packet driver: explicit checked attachment, enumeration, OTG causes,
suspend/resume, reset cancellation, session-end release and explicit fresh reconnect.
Suspend retains address/configuration/armed transfer; reset cancels old work.
Session end takes priority over reset/completion. Captured-only OTG ACK preserves
new causes arriving during acknowledgment. Attachment uses10ms bounded disconnect
hold, pristine EP0, pre/post power and mode/PHY/clock/gate/IRQ/DMA checks, including
an invariant check after event drain and before attachment. Errors release and
latch; failed cleanup retains ownership until explicit retry. Legacy physical
VBUS remains UNKNOWN; cable removal cannot be measured by this base circuit.
The default board startup still passes NULL profile and never attaches. New APIs
are retained in the ARM image and main polling accepts attached/suspended states.

**Evidence/source pin:** Baseline86c7349246eda89906bd37363e3979900c42f2ce;
ST HAL6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90 PCD/LL sources, local F413 CMSIS
V2.6.0 and original Ocelot USB. Actual sources, review and build/tests pinned in
sunnypilot/Ai/Evidence/chimera-usb-lifecycle-20261107.json and USB_LIFECYCLE.md.
36firmware tests pass incl92new ASan/UBSan composed scenarios and40reconnect cycles;
three copied-source mutations fail; independent final review approved and passed
the92scenario fixture. Raw9064/globals264, unsigned/unflashed, SHA
341ef240b4af887d74ae8a7800b892d116e8aca8ddf1af03640492d6ef83badd.

**Status/limits/correction:** Implemented and tested offline; stage100%.
Revised full-roadmap planning estimateabout30% complete/70% remaining, physical0%.
This dated estimate supersedes the earlier25% current estimate in QA12 because
an integrated capability is now complete; neither number measures time/effort or
physical readiness. T03 remains partial until board binding/qualification. No
physical enumeration, unplug deadline, continuous PLL health, bulk/CAN-controller
binding, normal status or actuator operation is proven. Next opt-in board USB
startup binding, then bulk/CAN RX and operational status; hostT08b2d remains queued.
No hardware/flash/config/actuation/upstream update/push. Existing unanswered items
preserved. Agent Skills/source/GNU ARM plus independent review used; no REA provider
result or unrelated binary analysis fabricated.

---

## QA-20261107-12 — Implement explicit legacy no-VBUS session mode

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "proceed".
**Context (labelled paraphrase):** Continue from the owner-identified Ocelot base
power trace, implementing an explicit no-sense USB policy without enabling the board.

**Answer:** Implemented validated UNFORCED(default) and explicit LEGACY_NO_VBUS
controller/service modes. Legacy sets the original B-session-valid override while
remaining soft-disconnected; it does not measure cable voltage. Main copies the
mode and requires no VBUS reader for legacy; physical VBUS remains UNKNOWN.
Legacy names controller session/power policy only; no old CAN/health format is
selected. Invalid/mixed/mismatched selections fail without choosing another mode.
Reset cancels old EP0 address/configuration/generation, exact mode bits and PHY/
VBDEN settings are checked around polling, faults invalidate the snapshot and
accessible cleanup clears overrides. Failed release retains ownership for explicit
retry. Actual main.c is unchanged and still passes NULL profile/reader, so no
physical USB connection or descriptor power profile is enabled.

**Evidence/source pin:** Baseline radxa/q8bb3ff3d26e4d71e9d7b68dd6a7b3a94310b5cfe7e;
new mode API in usb_hw.h/c, usb_service.h/c and main.h/main_runtime.c; driver rejects
unsupported OTG summary in addition to role/suspend faults. Original Ocelot source
and pinned ST F413 CMSIS V2.6.0 define the used bits. Actual sources/build/tests are
pinned in sunnypilot/Ai/Evidence/chimera-legacy-session-20261107.json.
34firmware tests pass, including61new real-component ASan/UBSan scenarios, ARM/
deterministic/linker checks and three caught mutations. The initial restart fixture
incorrectly expected success while leaving its injected suspend bit set; it now
asserts that refault, then removes the condition before healthy restart. No
production weakening or assertions suppressed. New raw8316/globals260/stack4096,
SHA745f66c5c408a8c046c6c7ed3f3c3edc576b9743b9a0b35d860770a1f24e8826.

**Status/limits/progress:** T03c3b100% implemented/tested offline; full rough roadmap
about25% complete/75% remaining, new-firmware hardware validation0%. No actual
VBUS/cable-loss detection, resume or host-activity deadline is claimed. OTG summary
causes are not yet decoded/acknowledged and even benign summary events currently
fault; that policy must be reviewed before attached operation. Next OTG cause
handling and controlled attached-state lifecycle offline. Actual power/profile/
pins/installed recovery/bench, bulk/CAN/health/inputs/Core Config/MCU TX remain
later work. HostT08b2d queued. No hardware/flash/config/actuation/update/push.
Earlier unanswered items retained; QA11's proposed mode is now implemented only
within the detached/offline scope above. No REA provider or live result fabricated.

---

## QA-20261107-11 — Continue using the Ocelot base schematic

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "proceed".
**Owner clarification (faithful quote):** "see on ovelot foldeer the sch is same onli i/o is added".
**Context:** In answer to our PCB/schematic question, the owner identifies the
saved Ocelot schematic as Chimera's base circuit, with added I/O. This supplies
the working baseline; it is not an independent physical measurement or a
numerical PCB revision. Do not repeat the same baseline question next session.

**Answer:** Traced gateway schematic and board, plus Pro source/original PDF.
USB VBUS connects through BAS40 to the shared5V rail; external regulator output
also joins that rail and3.3V is downstream. Neither drawing routes host VBUS to
an MCU input. Gateway PA9 is unconnected; Pro PA9 goes to header H5pin9, not VBUS.
All nine CAN RX/TX/enable MCU pins match. Existing original F4 firmware forces
B-session-valid through BVALOEN/BVALOVAL, explaining its no-sense USB architecture.
Historical raw descriptor bytes0xc0/0x32 are not measured consumption.

This corrects earlier wording treating the base drawing as inapplicable/missing.
Our new sensed-VBUS supervisor works in simulation but cannot sense an unwired
signal. Do not hardcode PRESENT or sacrifice retained analog/direct inputs.
Next is explicit opt-in legacy no-VBUS session handling tested offline, separate
from a sensed mode. It has not been implemented or enabled by this source audit.
The actual board build remains held; no firmware or host source changed.

**Evidence/source pin:** Baseline radxa/q8b4b6098789f86735a626c9e02c727202498cb748b;
Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 with unchanged39dirty entries and
working-file hashes. Gateway sch56ba4336a4e87670e27582f6b504ed0592036d8781d093bb9f2b476294282dcc,
board5787d0a7bb794082ddd12f9d176a144718d3873e6a43b6d257c769586ff32bd9;
ProSchDoc1f263c35e6b0d7b88fbec9868e5ba60d218f8a2880e939811051c0aeb3d6b4f9.
36source checks include17gateway net-pad comparisons. Pro selected-path replay
normalizes0.1unit fractional export geometry and was visually checked against
the original PDF; it is not full EDA/ERC. Structured data, replay and validation:
sunnypilot/chimera/hardware/ocelot-base-power-20261107.json and
sunnypilot/Ai/Evidence/chimera-base-power-20261107.json. No REA provider result
claimed. All25firmware inputs/8108-byte image preserved;33firmware tests remain
source-pinned to4b6098789, not rerun for this documentation/source-audit stage.

**Status/limits/progress:** T01b source audit100% complete; overallabout25% complete/
75% remaining, new-firmware hardware validation0%. No new physical power/current/
reverse-current/profile/recovery/attachment qualification. Full added-I/O routes,
operational USB/CAN/health/inputs/Core Config/MCU TX remain separate. No board,
flash/config/CAN/relay/OBD-C action, update or push. HostT08b2d stays queued.
Earlier unanswered items remain; QA08–10's missing-base/physical-reader next-step
assumptions are superseded by this dated owner clarification and trace.

---

## QA-20261107-10 — Continue and show percentages after every stage

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "proceed after each stage show in % were we reached".

**Answer:** Continued main-first work with observed VBUS supervision. Main polling
now requires fresh PRESENT before and after each bounded detached USB service
poll. Missing, unknown, invalid or absent observations stop the service, invalidate
the snapshot and latch a power failure. Cleanup ownership/errors are preserved;
no automatic sampling/retry/reconnect follows failure. Explicit stop/restart
requalifies observations. The board build still uses NULL power profile and NULL
reader, so it stays USB_HELD; no physical cable detector or attachment is claimed.

After each completed stage, report its result plus the full new-firmware-and-host
roadmap's approximate completion/remaining percentage and physical validation
separately. At this checkpoint: T03c3a100% implemented/tested offline; overall
about25% complete/75% remaining; new-firmware hardware validation0%. Overall is
subjective planning, consistent with QA06's20–25% estimate, not measured effort,
time or readiness. The same partial T03workstream remains open, so this small
slice does not justify an automatic percentage increase.

**Evidence/source pin:** Baseline radxa/q8b1dd5a7f63920c8e5a935c0a6fe3ce9a89baedd25;
main.c/main.h/main_runtime.c, USB_POWER_SUPERVISION.md and PROGRESS_EXPLAINED.md.
Receipt sunnypilot/Ai/Evidence/chimera-main-power-20261107.json pins actual sources,
33passing firmware tests (16new real-component ASan/UBSan power scenarios), ARM/
deterministic/linker checks and two caught power-guard mutations. Current raw
unsigned8108-byte image SHA256
b2c62ee6d05d5b6c720633daf4d34c2aecb3ca15166926a10257d54a9a7f7bb3.
Teacher source-first routing confirmed existing board photo/guide and separately
named schematics do not establish this revision's USB power/VBUS circuit. No
REA provider or physical reading fabricated. Earlier QA09 describes the T03c2
poll API; this dated increment adds the required observation argument.

**Implemented/proposed/limits:** T03c3a supervision is implemented and tested
simulated/offline. Actual VBUS reader/profile, electrical/current/installed
recovery qualification, attached-mode lifecycle and other operational firmware
remain pending. No device/flash/config/CAN/input/relay/OBD-C/host admission change,
upstream update or push. Host T08b2d stays queued. Earlier unanswered items retained.

---

## QA-20261107-09 — Proceed with the next main USB startup slice

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** "proceed".
**Context (labelled paraphrase):** Continue the new Chimera firmware/main-first
path after the explanation of checked startup and the power/VBUS/recovery hold.

**Answer:** Implemented a coordinator that main calls for checked startup,
bounded USB polling while detached, identity consistency and explicit cleanup/
stop/restart. It uses the existing real USB components. Failed cleanup keeps its
ownership/error recorded and is not silently retried. A supplied configuration
must pass argument checks; no configuration means USB stays held. The actual
board build still supplies no profile, so this increment does not establish USB
communication with Sunnypilot or qualify board power/recovery. Native tests use
synthetic configuration with simulated registers only.

**Evidence/source pin:** Baseline radxa/q8b6865244e73ef3a1cebb1356810b4fa4694467857;
main.c, main.h and new main_runtime.c; source hashes, new build report and actual
checks in sunnypilot/Ai/Evidence/chimera-main-runtime-20261107.json.32firmware tests
pass, including51new real-component startup/poll/fault/restart scenarios under
ASan/UBSan, ARM call checks, deterministic builds and two caught guard mutations.
Current unsigned8032-byte image SHA256
da43eb348399fcb05fe203a50d38aa95a9d69bf031e20695ab5ceb9a179427d7.
Source-first/GNU ARM inspection; no fabricated REA provider or live result.

**Status/limits:** T03c2 implemented/tested offline. No hardware opening, flash,
attachment, CAN/input operation, Core Config, relay/OBD-C or host admission change.
Board power/profile/VBUS, installed bootstub and restore path remain unqualified.
Next is evidence-backed attachment/cable-loss policy; host T08b2d still queued.
Updates held; no push. QA08's earlier unbound-service answer describes T03c1;
this dated increment adds conditional service composition, while board USB stays held.

---

## QA-20261107-08 — What main.c change adds, and why USB is held

**Date:** November7,2026 UTC.
**Owner question (faithful quote):** so wat have u done in main.c ,did u imrpove to to our new sunnypilot ,USB communication is still held pending power/VBUS/recovery qualification. Next is the qualified USB startup sequence and recovery handling.
 wat this means

**Answer:** The previous increment improves startup/diagnostics, not completed
USB/Sunnypilot communication. Actual reset now calls checked preparation after
the existing clock/quiet setup. That reads the UID, rejects blank/inconsistent
values, captures raw reset/option words, sets a validity flag and records explicit
clock/argument/facts/fault/held states. Faults revoke validity. Data is debugger-
visible RAM only; Sunnypilot does not receive this snapshot over USB. UID is a
future serial source, not chip-model authentication or current readiness proof.

USB_HELD is a deliberate software stop after successful preparation, not a
measurement that USB power failed. There is no runtime power-qualification
algorithm or condition that currently turns it into operational USB. Main still
parks without calling the USB service; the new image is offline/unflashed.
No USB protocol/CAN endpoint integration was added by this main.c increment.

Power qualification means establish whether this board is powered byUSB,
external/IGN/battery, or both and how the supplies interact. VBUS means the USB
cable's5V supply/presence; an externally powered board may remain alive after
unplug, so cable-loss detection/response must be established for that design.
Recovery means a verified bootloader/DFU/restore path with the correct image,
bootstub and settings preserved if a new application fails. Historical recovery
evidence exists; the new image/current installed state is not thereby qualified.
These are board/boot facts, not Sunnypilot configuration options.

Qualified USB startup means initialize/poll the existing USB components using
verified board power/session parameters and fault cleanup before live attachment.
Offline startup/service implementation and tests can progress while physical
qualification is pending; the gate is not a reason to invent settings or a claim
that no further software work is possible. Full USB/CAN communication remains
unfinished. No implementation was resumed by this explanatory answer.

**Evidence/source pin:** Cleanradxa/q8b228ed567e8eabdbb4f7c45735b9338fc1b87d842;
main.c5–18 and79–103, MAIN_STARTUP.md and USB_STARTUP_REQUIREMENTS.md. Source/
saved receipts only;30previous offline tests remain source-pinned, not freshly
rerun here. No REA provider/device/flash/runtime/config/CAN TX/upstream update/push.

**Status/limits:** Documentation-only clarification; no source/roadmap change.
Continue new firmware/main-first scope; next remains qualified main USB startup
and recovery/fault handling, with physical attachment prerequisites unresolved.
Host T08b2d still queued. Current snapshot does not prove the watchdog is stopped,
attest firmware or expose an operational USB capability.

---

## QA-20261107-07 — Continue new Chimera and work on main.c first

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** lets continue this path but i want u to work on main.c first

**Accepted scope/answer:** Continue the new-firmware path; prioritize main ahead
of the previously queued host status/reconnect task. T03c1 connects the read-only
boot snapshot to actual reset startup. Main now checks clock success before UID/
reset/option reads, exposes snapshot validity and named failure/USB_HELD states,
and revokes validity in the fault handler. MMIO callback binding is separate
from DWT initialization, so this new startup step adds no peripheral writes.
USB power/VBUS/current recovery remain unqualified; main does not choose invented
power descriptors, start USB service/attach, sample inputs or transmit CAN.

**Evidence/source pin:** Baseline03b89175b40483f3cce7bac6d2292e7dac9f5ed5 onradxa/q8b;
main.c/main.h, usb_mmio.c/usb_time.h, build source manifest and native/ARM tests.
30firmware tests pass with warnings as errors, including ASan/UBSan on actual
preparation/65536snapshots and existing register/codec suites. ARM ELF call graph
confirms reset→binder/preparation→real boot reader, no USB service call. Removing
the clock guard in a temporary copy makes the test abort. Initial RED and ARM
memset-link failure retained; final logic passes only fully bound callback data,
no shim/link relaxation/warning suppression. Raw7592bytes/globals32/stack4096,
SHAfbce0bfa171b2bedca369d9913f6e3b661cadfa8ccf8a69063e0b9935b1020d1.
Student receipt: Ai/Evidence/chimera-main-startup-20261107.json and contract
chimera/docs/MAIN_STARTUP.md. Source/GNU/native evidence, no REA provider or
subagent claim. Relevant incremental/TDD/API/Git/review/docs workflows used.

**Implemented versus proposed/limits:** This checked startup slice is implemented
and verified offline, not a complete operating main loop or physical board proof.
Original7448-byte build preserved ignored; historical receipts remain tied to old
sources.24current source/header hashes,19unchanged prior firmware sources; Ocelot
39dirty entries/19hashes, archive/DBC and Panda/opendbc pins preserved. No flash/
reset/config/CAN TX/managed daemon/upstream update/push. Raw reset/options do not
prove watchdog state or readiness. Next main increment: qualified USB startup
profile and recovery/fault handling before service initialization/attachment;
physical prerequisites remain. Host T08b2d stays queued. QA05's C2-era host-only
idea remains an alternative; no rollback to that firmware was selected.

---

## QA-20261107-06 — New Chimera progress as a percentage

**Date:** November7,2026 UTC.
**Owner question (faithful quote):** how far we implemented new chimera idea show in %

**Answer:** For the full new-firmware-plus-host T01–T20 roadmap, give a rough
planning estimate of20–25% implemented, with75–80% remaining. This is subjective
partial-credit estimation, not a measured effort/time fraction or a readiness
metric. The source roadmap has2offline building-block tasks complete(T04codec,
T06native transport),5partly implemented(T01/T02/T03/T05/T08),13pending(T07,
T09–T20). They are unequal in difficulty and have no agreed effort weights, so
10% of workstreams fully complete and25% partial does not itself determine an
exact overall completion percentage. Physical qualification of this new
implementation remains0%: no flash/physical USB/CAN/complete board proof.

Completed foundations include source/board map, F413 bootstrap/build, detached
USB libraries, CAN codec, host USB/identification and legacy status/consumer
checks. New firmware main remains parked. Operational attachment/bulk/controller
binding, status/reconnect, digital/pulse/analog acquisition, guarded TX, CoreConfig,
settings/recovery, relay/OBD-C and bench/release work remain. No percentage means
ready for use or predicts completion time. The earlier statement that there is
no reliable measured percentage remains true; this dated estimate answers the
owner's explicit request for a rough number, not a new factual metric.

**Evidence/source pin:** Cleanradxa/q8b9a7489f8c382c922b91842f0a46d8878b5a75f1b;
chimera/tasks/plan.md T01–T20 status table, PROGRESS_EXPLAINED.md and November6
saved audit. No fresh code/build/hardware tests or REA provider needed. Previous
152Python/10native audit evidence is offline and not the denominator of progress.

**Implemented versus proposed:** Explanation/notebook only, no firmware/host/
Chimera folder/roadmap changes, implementation resumption or route selection.
C2-era retained-firmware approach from QA05 remains an unselected option. No
flash/config/CAN TX/upstream update/push. Next technical task stays T08b2d passive
normal-status publication and disconnect/reconnect; hardware remains untested.

---

## QA-20261107-05 — Option: retain C2-era Chimera firmware, adapt Sunnypilot only

**Date:** November7,2026 UTC.
**Owner question/request (faithful quote):** can i ask u some thing ,wat if we keep the chimera folder same as of c2 and we work on sunnypilot only ,dont implement i want this option ,and later we can improve the safety of chimera

**Answer:** If C2 means retaining the original C2-era Chimera firmware, adapting
only Sunnypilot is a viable compatibility option. Keep the existing firmware's
USB/CAN/input/config/relay behavior and park the new bootstrap work; build a
pinned, separate original-Chimera protocol adapter in the host for CAN framing,
health/unsupported fields, bus/report mapping and connection lifecycle. Preserve
the canonical DBC via explicit translation where legacy reports differ. Existing
Python mailbox16/health43 receive code and native original-Chimera identification
are useful starting points; the managed native monitor currently accepts the
different F4v17/health59 profile, so this route still requires host integration.
It does not require making old firmware speak the current USB wire format.

**Safety tradeoff:** Delaying a firmware safety redesign can fit receive-only
integration and isolated bench work. Host checks cannot enforce output limits
when host software crashes/disconnects, or establish independent MCU safety.
Minimum device-side permission/limit/loss/override behavior needs qualification
before real actuator control; missing enforcement needs firmware/device work then.
Original Chimera reports constants/unqualified status, uses0xDC for relay request
rather than modern safety selection, and its shown PB0 loop follows ignition;
heartbeat-controlled actuator cutoff is not established. Existing defects remain
with the retained image. Updating host code alone does not repair them.

**Evidence/source pin:** Clean actual Sunnypilot
e8cd79f9008d9b566828fa0345cda2cc5a0addcc; old Ocelotd87892fa plus preserveddirty
main.c/chimera.h and the existing November5deep review. Selected actual source:
Chimera get_health_pkt/USB endpoint3/control0xDC/relay loop; host chimera.py and
chimera_protocol.py, LEGACY_PANDA_SUPPORT.md and FIRMWARE_SOURCE_MAP.md. C2 Panda
CAN5/health50, original Chimera mailbox16/health43 and CarrotF4 CAN6/health59 are
different profiles. C2 itself does not identify an exact board firmware image.
No installed-image/previous-working-compatibility claim or hardware test.

**Proposed versus implemented:** Option assessment only, as explicitly requested.
No firmware/host code, Chimera folder, roadmap, installed config or runtime changed;
no flash/CAN TX/upstream update/push. Exact intended C2/Chimera source/image remains
to pin if this option is chosen. New firmware work remains preserved. No route
selected and no safety weakening accepted. Current queued engineering remains
T08b2d until the owner explicitly selects a direction. Source-first migration/API/
documentation review; no REA provider or delegated analysis required.

---

## QA-20261107-04 — Why the new firmware main.c is small

**Date:** November7,2026 UTC.
**Owner question (faithful quote):** why our main.c is small

**Answer:** chimera/firmware/main.c is74lines because it is still the minimal
startup/bootstrap, and other logic lives in separate modules. It initializes
RAM, clears inherited interrupts, selects the internal16MHz clock, sets source-
defined inactive outputs/gates USB and CAN clocks, records a boot state and parks
in WFI. It does not start USB service, CAN controllers, input sampling, CoreConfig
or a working communications loop. USB driver/EP0/service/codec helpers exist
separately and are tested offline, but main does not call them. The short file
therefore reflects both modular structure and incomplete operational integration.
A future main can remain compact while initializing services and running their
polling/fault-handling loop; most implementation can stay in modules.

**Evidence/source pin:** Cleanradxa/q8b baseline
b32b0e9b953384349aa4696864d5b5919a23cb87; main.c20-25 quiet,47-49park,
57-74reset; firmware/README.md module map; usb_service.h detached-only contract.
Readable source/line counts only, no REA provider or new build/device test.

**Implemented/proposed/limits:** Explanation/notebook only. Existing bootstrap
and detached helpers implemented offline; startup attachment, bulk/controller
binding, inputs/status/TX policy and physical qualification remain pending.
No source edit/flash/config/CAN TX/upstream update/push. Next engineering task
still T08b2d passive normal-status publication/disconnect/reconnect on the host;
this question alone does not resume implementation or connect USB startup.

---

## QA-20261107-03 — Shut down now; continue this evening

**Date:** November7,2026 UTC.
**Owner request (faithful quote):** please  shutown now and  will see this in evening

**Answer:** Save the current clean project/explanation work and evening restart
point; request normal GNOME shutdown of the current Radxacomma host, respecting
application cleanup/inhibitors. No force/discard. Actual queued request/result is
recorded below and in the session receipt; physical poweroff not claimed in
advance. Resume T08b2d passive normal-status publication/disconnect/reconnect
this evening, with invalid/observation-only legacy status. No new engineering,
remote-PC shutdown, source update or push.

**Evidence/status:** Source baseline3ec39ebc2ed477309750727bf737d8020b8e4c70 on
cleanradxa/q8b. Normal desktop session active and gnome-session-quit available;
Code has a shutdown-delay cleanup inhibitor. Documentation-only notebook/QA/
whitespace validation; no application/hardware test rerun. Source-first/saved
normal shutdown method; no unrelated REA analysis.

Actual request: normal GNOME poweroff queued as chimera-evening-poweroff-20261107T061018Z.timer,
60second delay; readback active/waiting. No force/inhibitor override. Physical
poweroff unobserved. Evening restart point saved before request.

---

## QA-20261107-02 — Intended complete USB/CAN role for Chimera

**Date:** November7,2026 UTC.

**Owner question (faithful quote):** so we will be able to completery replace ,were chimera will be able to recieve and send data throuh chimera

**Answer:** The intended result is Chimera serving the Panda-style USB/CAN
interface role for this Radxa/Sunnypilot setup, with both directions: three
classical CAN buses into Chimera then USB to Sunnypilot, and Sunnypilot USB
commands through Chimera's MCU policy to the selected CAN bus/device. Retaining
ignition/brake/pulse/analog inputs, Core Config and board relay/OBD-C support
remains in scope. This is an intended outcome, not a tested complete replacement
or a promise of every current Panda/H7 feature; the board has classical CAN.

**Implemented versus proposed:** Host passive legacy CAN receive and isolated
status paths plus codecs/USB foundations are implemented/tested offline. The new
F413 bootstrap still parks with USB/CAN disabled; endpoint/controller binding,
MCU enforcement on every transmit path, permitted TX handling and physical bus
qualification remain pending. No operational TX path or actuation permission
comes from metadata/exact status reads. Next T08b2d remains passive normal-status
publication and disconnect/reconnect; TX integration follows in later slices.

**Evidence/source pin:** Cleanradxa/q8b6f788e922b8487e618702f0a795cdb4a526e1065;
chimera/tasks/plan.md T04/T08/T13/T20; BUS_INPUT_CONTRACT.md,
STATUS_CAPABILITY_CONTRACT.md, CAN_CODEC_CONTRACT.md; pandad/main.cc passive
can/customReservedRawData1 publishers and firmware/main.c parked startup. Local
source/saved audit only; no fresh application/hardware tests or REA provider.
This follow-up records the intended role, does not resume implementation, flash,
change runtime/DBC/config, update upstream or push.

---

## QA-20261107-01 — Explain field metadata and exact-length USB status

**Date:** November7,2026 UTC.

**Owner question (faithful quote):**
> 1. Metadata identifying the six unavailable legacy fields.
> 2. Exact-length USB status reads. wat is this

**Answer:** Both are host-side compatibility checks. Metadata is an explicit
label listing newer Panda status fields that the selected legacy F4 profile
cannot supply: spiErrorCount, soundOutputLevel, controlsAllowedLateral,
controlsAllowedLongitudinal, nmiReset and hardfaultReset. Unavailable means
unknown/unsupported, not measured zero/false. Separate lateral/longitudinal
permission cannot be inferred from the older combined controlsAllowed flag.
Consumers check required fields; legacy previews remain invalid/observation-only.
The SPI-named field is a protocol label, not an SPI backend.

Exact-length reads accept a board-status reply only when its size matches the
identified protocol: current D2health49bytes, legacy F4v17 D2health59bytes and
supported C2per-controller health64bytes. A59byte reply expected but40received
is rejected instead of filling19missing bytes with zeros and accepting it.
Timeouts/disconnects/unhealthy ownership also reject; status replies are distinct
from CAN data frames. Current/legacy formats stay separate.

**Evidence/source pin:** Read actual cleanradxa/q8b HEAD
dfd316d6554bbd39e221759c5637e648b8cd2cc3; pandad/panda_state_legacy.h,
panda_state.py, panda.cc get_state/get_can_state and panda_health.cc exact legacy
readers; chimera/docs/PANDA_STATE_AVAILABILITY.md and QA32/33 audit. Local
source evidence, no web/REA provider/device run needed. Existing offline test
receipts were read, not rerun for this explanation.

**Implemented/proposed/limits:** These checks are already implemented offline;
this answer changes notebook prose only. No new runtime/firmware/startup action,
upstream update or push. Metadata does not authenticate firmware or grant control
permission. Normal USB PandaState publication/reconnect and physical qualification
remain pending. Next technical task is still T08b2d passive normal-status
publication and disconnect/reconnect handling. Existing statsd teardown issue
and PC shutdown delivery limit remain recorded separately.

---

## QA-20261106-33 — Audit, save, publish and PC shutdown

**Date:** November6,2026 UTC.

**Owner request (faithful quote):** i knw chimera is not complete ,i want u to audit wat we did so far ,save it,i want u to update the github page if sunnypilt ,shutdown the pc ,we should continue wat we left tom ,Next: passive normal-status publication and disconnect/reconnect handling.

**Answer at audit checkpoint:** Audited33local commits since publishedc1811280;
all have latest passing validation. Saved component status, source/hash evidence,
limits and November7next step; updated main GitHub-facing README. Fresh56host+
68control assertions+28firmware tests (152total),10native checks and existing
sanitizer reruns pass. The bare control runner hangs during existing metrics
shared-context destruction; explicit after-suite socket cleanup gives clean exit0,
with all assertions preserved. Production stats teardown remains unresolved.
Earlier68pass reports did not establish process exit; correction is saved here.

**Evidence/source pin:** Implementation05a33eb1c556fd5d7bf489056ce1782330671e6f;
student Ai/Reports/chimera-audit-20261106/README.md, source-audit.json,
control-cleanup-diagnosis.json, control-clean-exit.json, preservation.json and
per-suite receipts. Full git refs and test commands retained. Teacher/student
logs synchronized; no REA provider/delegated/physical integration claim.

**Implemented/proposed/limits:** Audit and restart saved; authorized normal push
toDeggory/radxa-pilot:radxa/q8b follows and actual readback will be added. No master
update or upstream integration. Strict PCSSH to10.43.0.216 fails(no route),
10.42.0.216 times out,192.168.1.104 refuses; no PC shutdown delivered. Owner asked
whether already off/address changed. Radxacomma is separate. Hardware/new firmware
untested/unflashed; legacy observations remain nonoperational. Tomorrow T08b2d:
passive normal-status publication and disconnect/reconnect handling, retaining
pinned identity/exclusive ownership/no stale reuse/no SPI or control admission.


**Actual publication closeout, November6:** Audit148f77d272e81eccfb7b7f9a195ce9acb8a4f783
pushed normally toDeggory/radxa-pilot:radxa/q8b. Remote SHA matches; GitHub
connector README blobc0f96337cd2a3b1410d2096bc23f52580fd416f1 matches localGit.
Supporting opendbc ref150f9371 already matches. Defaultmaster/upstream preserved.
Final strict PC10.43.0.216 attempt again returns255/no route; alternate refusals/
timeout saved. No authenticated PC shutdown delivered, physical power unknown.
Owner's address/status question remains unanswered. No Radxa shutdown requested.
This follow-up saves actual publication and failed shutdown delivery; next remains
November7 T08b2d passive normal-status publication and disconnect/reconnect.

---

## QA-20261106-32 — Availability and consumer increment completed

**Date:** November6,2026 UTC.

**Owner request (faithful quote):** i already told we have to remove spi ,look into pandad ,Next: field-availability metadata and consumer checks before normal publication. Hardware remains untested.

**Context:** Second increment of the same request; QA31 records the SPI removal.

**Answer:** SPI source/build/class/discovery/implicit entry removal is committed
as0fedef7b0. Now statusAvailability metadata explicitly marks legacyF4v17,
observationOnly and all6missing current fields. A shared consumer guard rejects
invalid/stale/unknown/incomplete/observation data, preserving complete batch
indices. hardwared, manager, UI, core controls/replay and MADS lateral checks use
it. Current D2/C2 reads now reject partial status instead of returning zero-filled
values. Legacy preview remains invalid and USB emits no normal pandaStates.

**Evidence/status:** Implemented and verified offline: native pandad build,
10native programs,56focused+68control/MADS/power/fan Python tests, USB/current
read and converter ASan/UBSan, native-to-Python metadata and mutation checks.
Source pins: Panda8a16e089, opendbc150f9371, Carrot69a2d3be; source hashes and
commands in student Ai/Evidence/chimera-availability-20261106.json; contract
chimera/docs/PANDA_STATE_AVAILABILITY.md. Source/GNU/fake-USB/Cereal evidence;
no REA provider/delegated/full daemon/GUI/hardware claim. All23firmware sources,
7448-byte parked image, Ocelot39dirty entries/19hashes,5reference files,
archive/canonical DBC and camera/model/Thneed preserved.

**Limits/next:** No physical USB/flash/reset/config/CAN TX/live IPC/update/push.
Metadata describes declared field support, not authentication or controls
permission. Historical current messages without metadata keep their old contract.
Normal passive publication and disconnect/reconnect policy, other profiles, new
operational firmware and power/VBUS/recovery/bench work remain. Existing generic
current fault27/schema limitation remains source-only and unexposed. No completion
percentage or hardware readiness is claimed.

**Dated correction:** QA30 described33active PandaState fields and availability
outside Cereal at that checkpoint. The schema now has34active fields including
this metadata struct; the six unavailable values remain unavailable. The previous
SPI session had a broken self-link and its first saved notebook check failed;
this increment fixes the link and reruns the full notebook verifier. Native/
Python/SPI checks from QA31 remain independently recorded.

---

## QA-20261106-31 — Remove SPI from pandad; continue metadata checks

**Date:** November6,2026 UTC.

**Owner request (faithful quote):** i already told we have to remove spi ,look into pandad ,Next: field-availability metadata and consumer checks before normal publication. Hardware remains untested.

**Answer, first increment:** Corrected earlier retention: deleted spi.cc,
PandaSpiHandle, SPI buffers/build/listing; native/Python startup now requires
explicit USB pins on all platforms, no generic fallback/auto-recovery/flash.
Current Panda construction uses qualified USB only, performs no reset/config
and rejects legacy before writes; legacy stays passive. Associated obsolete
SPI/internal-auto-recovery hardware tests removed with their features, fully
preserved in Git17f933a8. Replacement fake-USB/startup coverage passes.10native/
42Python checks and strict ASan/UBSan pass. New short-header test reproduced an
old heap over-read in the retained CAN parser; bounds fixed and regression passes.

**Evidence/status:** Baseline17f933a82d1139738c8673ed9951f477cf29a1bc;
student Ai/Evidence/chimera-remove-spi-20261106.json, PANDAD_USB_ONLY.md. Source/
GNU symbols/archive, fake libusb and actual builds; no physical/REA provider
claim. No PandaSpiHandle symbol or spi.o member, five invalid CLI exits2. Paused
build resumed; normal vendored linking/includes restored, warnings corrected with
zero-init/unsigned positions, no suppressions. Firmware23hashes preserved.
Metadata/consumer step remains active with its new RED test uncommitted. No
normal publication, hardware/flash/reset/config/TX/upstream update/push. Earlier
permission to retain generic SPI is superseded by this explicit correction.

---

## QA-20261106-30 — Proceed with legacy PandaState mapping

**Date:** November6,2026 UTC.

**Owner request (faithful quote):** proceed

**Context:** Continue after the host ignition-validity prerequisite; USB-only,
teacher-first evidence and one verified increment at a time remain accepted.

**Answer:** T08b2b adds an offline source-backed legacy F4-to-Cereal PandaState
preview. It maps24common fields plus all25fields in each of3controller structs,
preserves UInt32 measurements, fractional loads, volts and raw firmware booleans.
All33active PandaState fields are accounted for;6are explicitly unavailable,
including the broader SPI error count and current-only sound/reset/lateral/
longitudinal fields. Every preview has Event.valid=false. Legacy safety25/26
mean STELLANTIS/FAW, conflicting with current volkswagenMlb/hongqi; converter
rejects them. Fault bit27=SOUND_DMA is absent from the schema; bits27..31 reject
the whole preview. alternativeExperience32768..65535 rejects instead of signed
truncation. Complete raw values remain isolated diagnostics. Validation failures
leave the builder untouched. No publisher or transport is called; managed pandad
has no converter symbol.10native programs,41Python tests, converter ASan/UBSan
and validity mutation pass. Native preview read by Python cannot enable ignition.

**Evidence/source pins:** Baseline faf1f8140fab872ee20225813e17e8d724ea8e7a;
Carrot69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7, Panda8a16e089,
opendbc150f9371. Exact seven read-only connected GitHub file queries at that ref,
5retained files/licenses and matching Git blobs/SHA256 are recorded in
student Ai/Evidence/chimera-legacy-state-20261106.json and
chimera/reference/carrot-f4-state-v17/SOURCES.json. Contract:
chimera/docs/LEGACY_F4_PANDA_STATE.md. Source-first/GNU/native/Cereal evidence;
no REA provider/delegated/fresh-context review claimed. Relevant incremental/TDD/
API/review/Git/docs skills used. Source checks cover name-matched safety IDs,
fault ordinals, complete field accounting and frozen bytes.

**Implemented versus proposed/limits:** Offline preview conversion complete;
ordinary PandaState publication/admission still pending. Six serialized default
placeholders are unavailable, not measured zero/false; availability metadata is
not embedded in the Event. Matching labels do not qualify hooks/params or control.
Current Panda also defines sound-DMA bit27; existing managed fault list allocates
from all bits but fills0..26, a separate source-level risk saved for later review,
not repaired here. ASan/UBSan instruments converter/test with existing unsanitized
support libraries; no USB/SPI source linked. No normal status/Params/schema/profile/
pin/USB/IPC/hardware/flash/reset/config/relay/CAN TX/SPI/actuation/update/push.
Physical recovery/board firmware still unqualified and parked.23firmware hashes/
7448-byte image, Ocelot39dirty entries/19hashes/archive/DBC and protected runtime/
camera/model/Thneed preserved. Exact pinned GitHub reads are research, not branch
updates/fetch/updater checks. Initial SCons dry-run option/generated-include issue
corrected without suppression. Next T08b2c supported-field admission metadata and
consumer review before publication; reconnect/backoff follows. Earlier unanswered
items remain intact.

**Closeout clarification:** The complete source import retains upstream trailing
spaces on safety.h line666. Authored code/docs pass whitespace checks excluding
that unchanged attributed reference; exact Git blob/hash checks cover its bytes.
The initial feature commit and a small provenance/verification correction commit
are retained, with no history rewrite or runtime/test suppression.

---

## QA-20261106-29 — Proceed with Panda ignition validity prerequisite

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue normal Panda status integration after passive USB reception;
teacher-first evidence, USB-only deployment and incremental verification persist.

**Answer:** Implemented T08b2a: hardwared now uses Event.valid for each updated
pandaStates event. Invalid/empty updates clear ignition immediately, preventing
invalid ignition acceptance and repeated-empty updates retaining old ignition.
The last valid primary harness context is retained because it permits delayed
battery/offroad shutdown; invalid/unknown reports cannot invent new harness data.
Either ignition flag on any non-unknown Panda and primary-board harness semantics
are preserved. Missing-message age>5s grace/logging remain.12new real-Cereal tests,
37focused USB/Chimera/Thneed tests plus28power/fan regressions (65total) pass;
Ruff/compile pass. Removing validity rejection fails3tests. Seven fake-clock cases
execute selected actual baseline/current hardwared branches, reproduce both bugs
and verify the existing deadline without running hardware_thread or sockets.

**Evidence/source pins:** Baseline bc99ae0d917a99b925840c31a11c3cb34ed5f7e0,
unchanged Panda8a16e089/opendbc150f9371/Carrot69a2d3be and firmware/source pins;
student Ai/Evidence/chimera-panda-validity-20261106.json and
chimera/docs/PANDA_IGNITION_VALIDITY.md record exact files, hashes, outputs and
limits. Source-first selected local source/fake-clock evidence, not a REA provider,
physical runtime or delegated review. Relevant incremental/TDD/API/review/Git/docs
skills used. Initial Capnp test serialization warning fixed with separate builders,
not suppression; final37-test run uses warnings-as-errors.

**Implemented versus proposed/limits:** Host validity prerequisite complete offline;
T08b2 overall remains partial. Dated correction to QA28: hardwared no longer trusts
Event.valid=false or retains ignition after fresh empty updates. USB monitor still
publishes only CAN/isolated diagnostics, no ordinary pandaStates. Non-unknown type
check is not a new firmware/profile allowlist; valid does not prove physical
readiness. Current-only missing fields, raw safety/fault translations and unsigned
alternativeExperience still need explicit semantics and tested conversion before
ordinary status admission. Reconnect/backoff follows. No device/flash/reset/config/
TX/new profile/schema/pins/SPI fallback or upstream update/fetch/push. Native and
firmware sources unchanged; prior9native/sanitizer/28firmware results retained,
not fresh runs. Firmware23hashes/7448-byte image, Ocelot39dirty entries/19hashes,
archive, DBC and protected camera/model/Thneed preserved. Earlier unanswered items
remain unchanged.

---

## QA-20261106-28 — Proceed with passive USB CAN and diagnostics

**Date:** November 6, 2026 UTC.

**Owner request (original):** proced

**Context:** Continue after T08a USB-only pinned status startup. Teacher-first
source evidence and USB-only/no SPI fallback remain accepted.

**Answer:** T08b1 adds bounded classical CAN RX, fragmented-frame handling and
normal Cereal CAN publication to the legacy F4v17 USB entry. Complete supported
health/controller reports publish on isolated customReservedRawData1 JSON schema1,
with exact pins, query timestamps, operational=false and explicit failed/closed
payloads. hardwared consumes ignition from nonempty pandaStates without checking
Event.valid, so we publish no pandaStates pending explicit admission/validity
policy. RawData0 belongs to Thneed and is unchanged. RX/parser/status failure
closes ownership, discards partials and exits without reset/retry/SPI fallback.
Native build/9native programs,25Python regressions (including Thneed), parser and
backend/session ASan/UBSan pass. Removing checksum rejection is detected.

**Evidence/source pins:** Baseline ca409374b1102233acc6ad99c108c628a4ffba9f;
Panda8a16e089, opendbc150f9371, Carrot69a2d3be; actual source/artifact/test pins
and results in student Ai/Evidence/chimera-usb-receive-20261106.json and
chimera/docs/USB_PASSIVE_RECEIVE.md. Selected local source/native/GNU evidence;
no new REA provider/network/fresh-context agent result claimed. Used incremental,
TDD, API/interface, code-review, Git and documentation skills.

**Implemented versus proposed/limits:** Passive host observation implemented and
tested offline, not physical/end-to-end integration. This dated extension
supersedes T08a's status-only/no-CAN description from its earlier commit. Only
legacy F4v17 admitted; no new Chimera/original/current Panda admission. CAN6 has
no RTR field; host cannot distinguish/filter legacy remote records. XOR has
collisions; timestamps are host reception, status sequential and can delay RX.
Abrupt death needs consumer liveness checks. No sendcan/TX/safety/heartbeat/reset/
config/flash/SPI fallback or real USB/IPC/vehicle session/pins installed. Firmware
23hashes/7448-byte retained artifact, Ocelot39dirty entries/19source hashes/archive/
DBC preserved. No updates/fetch/push. T08b2 pandaStates supported-field validity/
ignition and reconnect/backoff policy, operational firmware and bench qualification
remain proposed. Initial toolchain invocation/header issues corrected without
suppression; earlier unanswered entries preserved separately.

---

## QA-20261106-27 — Proceed with USB-only startup/status ownership

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue T08a, retaining USB-only/no SPI fallback.

**Answer:** Radxa launcher now requires explicit PANDAD_USB_SERIAL/PANDAD_USB_VERSION and execs native --usb-status before legacy device probes/reset/flash/DFU. Native Q8B entry rejects bare/legacy invocation. A new status-only session owns the pinned USB backend, qualifies typed legacy F4v17 initial health and samples health plus all3controllers; any failure/exception closes immediately, no stale-cache/retry/SPI fallback. Explicit reopen repeats identification.21Python tests (6new),7native executables, actual native build and strict ASan/UBSan pass. Five invalid native invocations exit2 before device access; main.o has no legacy-thread reference. Removing immediate failure cleanup is caught. Next T08b is passive CAN reception and validity-aware publication/exact-read/freshness/reconnect work.

**Evidence/source pins:** Baseline86678975460572b26a03af3354cb0fcc0f7f24c6; exact existing Radxa identity, wrapper/main/backend and prior health contracts. Saved actual source/artifact hashes/commands/results at student Ai/Evidence/chimera-usb-startup-20261106.json; startup contract chimera/docs/USB_ONLY_STARTUP.md. Real backend/session exercised with fake libusb, no SPI source linked into sanitizer fixture. No new REA provider/network result or fresh-context review claimed.

**Implemented versus proposed/limits:** T08a startup/status ownership complete offline, not full managed Sunnypilot integration. Session currently accepts legacy F4v17 only; current Panda/original Chimera/new bootstrap remain rejected. No CAN/pandaStates/Params publication, sendcan/safety/heartbeat threads, TX or firmware writes. Earlier answers saying Radxa entry still opens SPI are superseded by this dated implementation; generic Panda SPI constructor remains but Radxa entry bypasses it. Missing pins fail closed; no pins installed or historical defaults. Reviewed compatible firmware is required, since unknown older IN commands may have side effects; version match is not authentication. Sample is sequential, not atomic/freshness-qualified; active means ownership only. No valid session/hardware/flash/reset/config/actuation/install/update/push run. Firmware23hashes/7448-byte retained artifact, Ocelot39dirty entries/19hashes/archive/DBC preserved. Native test enum-list compile defect fixed explicitly without suppression. Earlier unanswered entries preserved.

---

## QA-20261106-26 — Proceed with per-controller CAN-health5

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue T05c after the progress summary; USB-only deployment/no SPI fallback remains accepted.

**Answer:** Added native LegacyF4CanHealth with all26wire fields plus the caller selector, exact64-byte profile-gated decoder and one bounded C2 reader for selectors0/1/2. All unsigned widths, checked flags/error codes, reported speeds/counters are retained without casting to current health or inferring physical bus roles/FD capability. Invalid selectors/profiles/unhealthy handles fail before IO; malformed/short/failed or unhealthy completed reads return no state, without retry/cache/writes. Current/legacy CAN-health layouts match at pinned sources; versions/main health/policies stay separate. Native pandad and seven native executables build/pass; strict ASan/UBSan passes new CAN health and existing health59. Removing the reader selector bound is caught. Next T08a is USB-only pinned session/startup ownership with no SPI probe/fallback; managed publication/exact-read hardening/reconnect remains.

**Evidence/source pins:** Baseline288479ccaad916286376fac6fc86ad7dd6c69e85; Carrot69a2d3be actual header/C2 producer/bxcan/Python mapping, current Panda8a16e089 health header, F413 CMSIS REC mask. Exact hashes/commands/output in student Ai/Evidence/chimera-can-health-20261106.json; contract chimera/docs/LEGACY_F4_CAN_HEALTH.md. Independent golden bytes, all26offset/type assertions against both headers,3x64flags aligned/unaligned,1524invalid booleans,1024LEC cases and65533invalid selectors checked. Source/CLI/GNU native evidence; no new REA provider/network result.

**Implemented versus proposed/limits:** T05c decoder/read helper complete offline, full T05 partial. Legacy bus_off_cnt increments on each producer update including C2 reads while bus-off, not distinct transitions; no rate/reset inference. F4 REC is8bits, not constrained by H7 comment. Selector has no reply echo, no role remap; FD fields are reports only. No new firmware/status producer, USB startup switch or managed-readiness claim. Firmware23source hashes/retained7448-byte artifact unchanged; no new ARM/28-test firmware or Python receiver run. Ocelot39dirty entries/19hashes, archive and canonical DBC preserved. No device/flash/reset/config/CAN/relay/install/update/push; power/VBUS/current recovery and watchdog still open. Prior unanswered entries preserved.

---

## QA-20261106-25 — Summarize progress and remaining work

**Date:** November 6, 2026 UTC.

**Owner question (original):** summrize wat we got done tillnow and how much is left

**Answer:** The offline software foundation is built, but most operational integration and all new-firmware physical qualification remain. Completed work includes in-project Chimera code/evidence/roadmap; source-backed F413 GPIO/flash/three-bus/input mapping; original standalone firmware build/startup; current classical CAN codec; distinct USB identity/read-only control replies, packet driver, timing/UID helpers and detached service; native Radxa USB backend/pinned identification; bootstrap decoder and legacy F4 health59 decoder/bounded reader. Saved validation is28firmware/discovery tests, native pandad build/six native executable tests, sanitizers and15existing Python receiver tests. These are offline/source/fake-register results, not physical USB-CAN operation. Current image is7448bytes, unsigned, unflashed; main parks with USB/CAN disabled. Host still has inherited SPI construction awaiting USB-only integration. USB only/no SPI fallback is the accepted deployment. Remaining stages: per-bus status, operational firmware health/bulk endpoints/CAN controller binding, USB-only managed startup/publication/reconnect/exact-read hardening, qualified power/VBUS/current recovery and safe image packaging/bench bring-up, input acquisition/calibration/reports, MCU TX policy, Core Config/read/write persistence/watchdog, relay/OBD-C electrical behavior and release/soak tests. Active driving is a separate later scope. There is no defensible percentage from unequal roadmap slices; most work needed to make this usable on the board is still ahead. Next is T05c per-bus CAN-health5, then USB-only managed integration alongside pending board work.

**Evidence/source pins:** Baseline3f0c75e99430f02ca7f3d0d7fa9b6343d9f3be1c, clean radxa/q8b; current chimera/tasks/plan.md and docs/PROGRESS_EXPLAINED.md; saved Ai/Evidence/chimera-status-contract-20261106.json, chimera-legacy-health-20261106.json and chimera-usb-only-20261106.json. main.c parks; panda.cc constructor/list select SPI. Saved validation ledger at baseline passes. Firmware SHA256d5f7a3f9d0299da28fa7c78c662cefd4deb60c5e748b7e553926c77b8e9c2698. Teacher/student notes read first.

**Implemented versus proposed/limits:** Status explanation and progress-guide refresh only; no new runtime/code/hardware work, percentage estimate, completion/physical readiness claim or repeated runtime tests. Existing inputs/relay/OBD-C are retained in design, not operationally reimplemented. Original Chimera43, F4health59 and new bootstrap stay separate. Power/recovery gaps, managed lifecycle and new MCU policy remain open. No flash/reset/actuation/install/update/push; upstream checks held. Earlier unanswered entries preserved.

---

## QA-20261106-24 — USB only; no SPI requirement

**Date:** November 6, 2026 UTC.

**Owner request (original):** no spi is needed since we will use usb only

**Answer:** The Radxa-to-Chimera/selected legacy Panda deployment is USB only. SPI wiring, probing and automatic fallback are excluded from the target. Updated active README, roadmap, compatibility/status docs and Chimera instructions. Existing decoders and USB backend remain useful. The inherited native Panda constructor/list still open SPI; replacing those with qualified pinned USB startup remains T08 implementation work. Earlier references to preserving SPI described inherited generic code, not a hardware requirement for this setup.

**Evidence/source pin:** Baselinec668f6757da3e6a693d9738e99bdc0b5b81b7529; native panda.cc constructor/list explicitly select PandaSpiHandle; panda_usb.h supplies separate pinned USB factory. Owner statement is the authority for USB-only scope. Exact source/doc hashes and validation in student Ai/Evidence/chimera-usb-only-20261106.json.

**Implemented versus proposed/limits:** Requirement and plan correction saved, not runtime startup switching or SPI-source deletion. No code/build/firmware/hardware changes or new runtime tests; documentation/link/memory checks only. T05c per-bus health remains next, T08 must test no SPI probe/fallback and remain disconnected on USB failure. Physical USB/recovery and managed compatibility remain unqualified. No update/push; earlier unanswered entries preserved. This dated correction supersedes any earlier implication that SPI support is needed for the owner's deployment.

---

## QA-20261106-23 — Proceed with legacy F4 health59 decoding

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue the T05b host status slice after QA22.

**Answer:** Added a distinct native LegacyF4Health type, pure exact59-byte decoder and one bounded D2 read helper. Full32-bit voltage/current/counters, fractional load, eight checked boolean bytes and legacy-only fields are preserved; unknown enum numbers stay raw. No cast to current health49 or current-only defaults. Reader requires the previously qualified legacy profile and healthy exclusive transport; it makes one64-byte/1000ms control-IN read and rejects non-exact, malformed or unhealthy results without retries, cache or writes. Native pandad and six test executables build/pass, ASan/UBSan passes,15existing receiver tests pass, and removing the decoder profile guard is caught. Next T05c is per-bus CAN-health5 qualification before managed selection/publication/reconnect.

**Evidence/source pins:** Baseline9ada248e6ba7160723623fb62ba07e1d6aa67d63; Carrot69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7 health17 header/producer/Python mapping. Exact header and MIT license copied into project test references with verified Git blobs/SHA256, no network. Sources/commands/output/artifact hashes in student Ai/Evidence/chimera-legacy-health-20261106.json and contract chimera/docs/LEGACY_F4_HEALTH.md. Tests compare all27fields with original header plus independent golden bytes;256flag combinations,2032invalid booleans, high integer/float/unaligned and bounded failure cases. Native GNU file/nm evidence; no new REA provider result.

**Implemented versus proposed/limits:** T05b typed decoding/read helper complete offline, T05 overall partial. Managed get_state/startup remains unchanged, per-bus health/publication/enum-command compatibility pending. Reader's profile is a caller contract after pinned identification, not authentication; caller serializes ownership. Transport exceptions propagate. Current get_state/get_can_state still accept non-exact nonnegative replies; future managed integration must harden them. Generic Ruff on SConscript reports injected-name F821 just as baseline; actual SCons build and syntax pass, no suppressions added. All23firmware source hashes and retained7448-byte artifact unchanged; prior28-test firmware result is historical, not rerun here. Ocelot39dirty entries/19hashes, archive and canonical DBC preserved. No hardware/flash/reset/CAN/config/relay/install/update/push; physical power/VBUS/current-recovery still open. Earlier unanswered entries retained.

---

## QA-20261106-22 — Proceed with bootstrap status/capability contract

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue T05a after the detached USB service in QA21.

**Answer:** Added a pure Radxa-side decoder for the new bootstrap's existing A0/D6 replies and documented exactly what they establish. It validates the complete version/schema/phase/topology, zero operational capabilities/layout hashes and reserved fields. Unknown or altered profiles fail; no measurement, ignition, controls-allowed or ready state is manufactured. A real C-handler fixture feeds its replies to Python and verifies health/safety requests remain unavailable. All28offline tests pass, including five new tests. Firmware sources and7448-byte ARM image are unchanged. Next is source-backed legacy F4health59 decoding/adaptation before managed use; new Chimera operational health/controller/bulk binding remain separate work.

**Evidence/source pins:** Baselinee586191ac39e663727aac2cbd453937477350ef8; current Panda8a16e089 health header, Sunnypilot native consumer/identifier and actual bootstrap protocol.c. Exact hashes,28-test output (16.253s), ARM build/hash and mutation check in student Ai/Evidence/chimera-status-contract-20261106.json. Decoder openpilot/selfdrive/pandad/chimera_identity.py; contract chimera/docs/STATUS_CAPABILITY_CONTRACT.md.8160manifest/6375version alterations,256incorrect lengths and12invalid-type arguments are rejected. Native ASan/UBSan interoperability passes. Removed reserved-byte validation is detected in a temporary mutation and restored. Source/CLI and GNU ARM artifact evidence used; no new REA provider result claimed.

**Implemented versus proposed/limits:** T05a bootstrap contract/decoder complete offline; not an operational health profile, authentication, admission or managed lifecycle. Descriptor/serial/transport qualification belongs to future callers. Original health43 and legacy59 stay separate. Main remains parked; no attachment, measurement acquisition, CAN/relay/OBD-C/config/flash/reset/device/install/update/push. Missing physical power/VBUS/current-recovery and watchdog qualifications remain. Ocelot39dirty entries/19hashes, archive and canonical DBC preserved. Upstream checks remain held; earlier unanswered entries retained.

---

## QA-20261106-21 — Proceed with detached startup/service composition

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue the detached startup/service composition after QA20; actual attachment remains subject to its power/VBUS/recovery requirements.

**Answer:** Combined the tested boot-facts, timing, USB48 clock/core and EP0 driver modules into one detached service library. Start performs argument/ownership checks and the real preparation sequence; polling checks detached and CPU-clock invariants before and after driver work. Failure disables polling, attempts owned USB disconnect/masking/PHY-off and holds reset/gates the clock with checked readbacks. Failed cleanup stays latched; explicit successful stop is required before restarting.23offline tests pass, including44real-component pipeline scenarios. The ARM image is7448bytes with8bytes global RAM. The library is not instantiated/called by main and no attachment API is added. Next board work is the exact status/capability contract and offline response fixtures, followed by operational endpoints/controller binding.

**Evidence/source pins:** Baseline10fbf46341d6acadc768cea296c7e36044416750 on radxa/q8b; same Panda8a16e089/opendbc150f9371/Ocelotd87892fa and pinned ST evidence underlying existing helpers. Exact source/test hashes, actual23-test output, ARM symbol/no-startup-call and ELF bounds/reproducibility results in Ai/Evidence/chimera-usb-service-20261106.json. API/lifecycle contract chimera/docs/USB_SERVICE.md; session2026-11-06-chimera-usb-service.md. Native ASan/UBSan exercises real composed C functions against register callbacks; no success stubs or physical MMIO execution. No new REA provider/compliance/manual result claimed.

**Implemented versus proposed/limits:** T03b3b unbound detached service complete offline; whole T03/startup/physical qualification and Sunnypilot integration remain partial. Caller must zero-initialize/stabilize context, serialize calls and exclusively own a quiet board/PLL/affected clock domain; callbacks/context are trusted and live. Copied IO methods do not extend callback-context lifetime. Descriptor values are caller test inputs, not a qualified board supply profile. Cleanup checks register intent/readback, not physical cutoff, and leaves PLL/HSE/debug settings. No GPIO/IRQ/CAN/watchdog/flash/config or native host change; capabilities/hashes0. Actual power/VBUS/current-recovery, inherited watchdog, scheduling/resume/session/reconnect and physical timing remain open. No board read/write/flash/reset, actuation, install, upstream update or push; originals/DBC preserved. QA20's6608-byte artifact remains its historical result; current7448bytes. Earlier unanswered entries preserved.

---

## QA-20261106-20 — Explain the work and establish startup prerequisites

**Date:** November 6, 2026 UTC.

**Owner request (original):** can u sumrise wat we did ,since i dont wat u have done ,please expian and proceed Next: establish power/VBUS, UID and recovery requirements before wiring USB into startup. to this

**Answer:** We are building two cooperating programs: firmware on Chimera and USB host support inside Sunnypilot on the Radxa. So far we have source/board/flash evidence, a standalone F413 build with inactive output initialization, modern classical CAN byte encoding, USB identity/control requests, ordered register/timing access and a polling EP0 packet driver. Host USB/identification libraries also exist, but managed startup still uses SPI. These are offline-tested pieces; the new image has never been flashed and its startup still parks with USB/CAN disabled. Direct inputs/relay/OBD-C are preserved in the design; acquisition, Core Config, operational status/bulk endpoints, managed host admission and MCU TX policy remain unfinished. Added a plain-language guide. For this next slice, established the power/VBUS/UID/watchdog/recovery requirements and added a read-only helper for UID and raw reset/option registers.21offline tests pass, including65536snapshot vectors; image6608bytes. VBUS means host USB power, UID provides a stable serial, and recovery means verified rollback/bootstub/settings and an independent way back. Exact VBUS routing and supply/current profile remain unknown; old code forces session-valid rather than proving detection. Next software work can compose a detached startup/service module while attachment waits for the recorded electrical/current-recovery qualifications.

**Evidence/source pins:** Baselinef75b1e831e4190e7f62eb21f70bf0f7606976015; Ocelotd87892fa plus preserved dirty source; ST F413 CMSIS UID/CSR/OPTCR fields; ST HAL flash_ex.h6ef30cf0, bloba8217d36; official Chimera wiki recheckedNovember6. Historical October4 recovery session, exact nightly bundle/application/bootstub hashes and17archived config file hashes verified without device access. Current code/docs at chimera/firmware/boot_facts.c and chimera/docs/PROGRESS_EXPLAINED.md, USB_STARTUP_REQUIREMENTS.md; exact21-test output/build/source pins in Ai/Evidence/chimera-usb-prerequisites-20261106.json. No REA provider result claimed.

**Implemented versus proposed/limits:** T03b3a contract/helper complete offline; no startup/attachment enabled. UID helper has eight reads on success, rejects blank/unstable IDs and never calls write32; real MCU reads are untested. Raw flags may have been changed by bootstub and cannot prove software-started watchdog is stopped. The saved bundle bootstub is a build, not the installed16KiB-region dump. Historical restore/readback is not current board qualification. New raw image still lacks legacy length/VERS/signature packaging; no loading permitted by code availability. Main/driver/host/board/input/DBC sources unchanged; old archive/Ocelot preserved. No board read/write, flash, reset, option/config migration, actuation, install, upstream update or push. QA19's6420bytes remains its historical image; current6608bytes. Unanswered items below preserved.

---

## QA-20261106-19 — Continue Chimera's next USB stage

**Date:** November 6, 2026 UTC.

**Owner request (original):** lets continue with chimera next stage

**Context:** Continue T03b2 after the USB foundation and owner-supplied Ocelot Panda Docker source study.

**Answer:** Implemented the ordered ARM MMIO backend, bounded DWT cycle-counter delays at nominal HCLK16 and a polling control-endpoint packet driver. It connects the existing model to SETUP reception, FIFO replies, address/configuration status completion, reset and STALL recovery. Transfer cancellation waits for active IN disable, flushes old FIFO contents and clears old event flags before rearming.19offline tests pass, including32768RX headers,390descriptor-length transfers,15controller faults and51delay durations. The raw ARM image is6420bytes; global RAM remains8bytes. Startup remains parked and USB stays disconnected. Next T03b3 is the power/VBUS/UID and watchdog/recovery prerequisites, followed by separately reviewed startup/service/attachment integration.

**Evidence/source pins:** Sunnypilot baseline6b83b2e632bc95c53ec58fda748ee87d93b50be6; Panda8a16e089/opendbc150f9371/Ocelotd87892fa with original dirty sources preserved. ST HAL PCD/LL USB6ef30cf0, middleware2df324bd, ST CMSIS core_cm4/F413 register definitions and retained Ocelot Panda Docker source used. Exact source/test hashes, actual19-test output and ARM build/tool pins in Sunnypilot Ai/Evidence/chimera-usb-driver-20261106.json; contract chimera/docs/USB_PACKET_DRIVER.md and session2026-11-06-chimera-usb-driver.md. Native ASan/UBSan and real ARM symbol/barrier/link/vector/bounds/reproducibility checks; no REA provider/hardware runtime analysis claimed.

**Implemented versus proposed/limits:** T03b2 packet/backend library complete offline; full T03 and Sunnypilot compatibility remain partial. No GPIO/IRQ/startup attachment, physical UID read, qualified supply/VBUS behavior or real USB enumeration. Delay accuracy uses nominal16MHz; real oscillator, scheduling, endpoint/address/status timing and event ordering remain unmeasured. Suspend disconnects; wake/session end/watchdog/recovery still unqualified. Event/read budgets bound operations, not elapsed service deadlines. Current phase0 capabilities/hashes stay zero; no bulk/health/CAN binding, host profile admission, Core Config/input sampling or MCU TX policy added. Main/board/protocol/codec/USB model/linker and original references/DBC unchanged. No hardware/flash/config/actuation/install/upstream update/push. QA17's4060-byte image remains its historical artifact; current image6420bytes. Earlier unanswered entries remain preserved.

---

## QA-20261106-18 — Learn from Ocelot Panda Docker

**Date:** November 6, 2026 UTC.

**Owner request (original):** “[https://github.com/Deggory/Ocelot_Panda_docker](https://github.com/Deggory/Ocelot_Panda_docker) teacher i want you to learn about this ,the same board was ones made to work as old panda ,but he added the anlog input to this ,and relay and obdc ,maybe this can help use agnet skills”

**Answer:** Reviewed the supplied repository and its parent using source-driven/documentation skills. It helps: the parent contains both a real older Panda application and the separate Chimera application with PC2/PC3 analog inputs, PA3 ignition, PA4 speed, PA5 crank, PA6 brake, PB0 relay, PA2 OBD-C request and PB1 OBD-C ignition output. Parent Chimera main.c matches our committed Ocelot source exactly. Current main04b56ba0 removed the Chimera application; its panda target removes GATEWAY and uses stock Panda board detection. Thus we can reuse evidence about legacy USB/policy architecture while keeping our explicit Chimera board support. The Panda application uses mailbox16/health43 and actual safety-hook selection; DD changes forwarding rather than reading modern protocol versions. The parent PB0 loop follows ignition with request gating commented out, so heartbeat-controlled actuator cutoff is not established. OBD-C is a source-level accessory request/ignition interface; physical load paths remain unknown.

**Evidence/source pins:** Deggory/Ocelot_Panda_docker04b56ba0145588d91ff70e1b35b47b7f2652d4db and parent98de83bb54746d057e6e4bff707eab6cd8c179d9, retrieved via GitHub connector.31exact original selected files/tree/history/Git blob/SHA256 receipts in sunnypilot/chimera/reference/ocelot-panda-docker-20261106/. Review chimera/docs/OCELOT_PANDA_DOCKER_REVIEW.md and session2026-11-06-ocelot-panda-docker.md. Offline source verifier passes189sender/parser vectors, both target/flag tables, config preprocessing, compiled health43/signed-field offset39 and C-versus-Python signedness fixture. Current application baseline7d749a412; Ocelotd87892fa plus original dirty files preserved. No REA provider/runtime analysis claimed.

**Implemented versus proposed/limits:** Research, retained attributed sources, reproducible offline verifier and both notebook updates only. No active MCU/host/safety/config implementation changed or task marked newly complete. No proof of the owner's historic physical board operation or exact hardware-addition chronology, no full Docker/legacy firmware build, CI runs or physical test. New code remains our offline USB foundation; next T03b2 unchanged. Stock ADC supply scaling/harness relay/EON-only heartbeat fallback and forwarding bypass must not silently replace Chimera behavior. Core Config/acquisition/relay/OBD-C and modern profile admission still require implementation/qualification. Canonical DBC/Ocelot/archive unchanged; no hardware/flash/actuation/install/upstream update/push. Earlier unanswered entries remain preserved. “Learn” here means durable project notebooks and pinned evidence, not background model training.

---

## QA-20261106-17 — Proceed with USB clock and endpoint zero

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue after QA16 with the USB clock/controller/endpoint-zero foundation, using teacher evidence and offline verification before physical attachment.

**Answer:** Added original firmware libraries for USB48 clock preparation, detached USB core initialization and a pure endpoint-zero request/state model. The clock uses the source-defined16MHz HSE and M8/N96/Q4 while the CPU remains HSI16. EP0 supplies bootstrap descriptors and UID-derived serial formatting, strict standard requests and configured-only A0/D6 queries. Address/configuration changes wait for status completion; generation tokens reject canceled-transfer completions.16offline tests pass, including19fake-register scenarios and458797SETUP cases. The ARM image is4060bytes, with8bytes global RAM. Nothing calls these libraries from startup yet. Next is the real timing/MMIO and controller event/FIFO packet driver, followed by status and operational endpoints.

**Evidence/source pins:** Baselinefcdbecdd6f706d21074363b8cca869ce85dace40; Ocelotd87892fa original clock/USB/board sources and ST CMSIS header; official ST LL USB6ef30cf0 and device middleware2df324bd. Exact URLs/hashes, actual16-test output and tool/artifact pins in Sunnypilot Ai/Evidence/chimera-usb-bootstrap-20261106.json; design/limits in chimera/docs/USB_BOOTSTRAP.md and session2026-11-06-chimera-usb-bootstrap.md. GCC13.2.1/binutils2.42, native ASan/UBSan and ARM link/symbol checks used. No unrelated REA provider analysis claimed.

**Implemented versus proposed/limits:** T03b1 complete offline; T03 remains partial. No hardware MMIO/timer adapter, GPIO USB setup, interrupts, FIFO packet pump, physical UID read, VBUS qualification or connection. Caller must supply a qualified power profile and UID. Generation tokens require the future driver to cancel/drain stale hardware events. Physical clock/address-status timing and USB compliance remain unqualified; full ST manual/USB specification review is not claimed. No bulk endpoints, operational status, host admission, CAN/input acquisition or MCU actuation policy enabled. Main/startup, phase0 capabilities, DBC/Ocelot/archive unchanged. No device/flash/config/actuation/install/update/push. QA16's1840-byte artifact remains its historical result; current image4060bytes. Unanswered entries below are preserved.

---

## QA-20261106-16 — Proceed with modern classical CAN framing

**Date:** November 6, 2026 UTC.

**Owner request (original):** procceedd

**Context:** Continue the next board slice after QA15: modern classical CAN framing before USB endpoint wiring.

**Answer:** Implemented the pure firmware CAN codec: current six-byte/XOR encoding, strict host-TX decoding and a bounded streaming decoder that retains partial records across chunks. It preserves buses0/1/2, accepts0..8payload bytes and standard/extended IDs, rejects FD/invalid headers/host return flags, and latches detected stream failures until explicit reset.14offline tests pass:648RX records and189TX packing vectors match the current Panda source, with4536split/chunk scenarios,17280fixed-size bit-flip rejections,65536header cases and10000random streams. The image is1840bytes. No codec is called from the parked application; USB/CAN wiring and operational health remain unfinished. Next is USB clock/controller/endpoint-zero work.

**Evidence/source pins:** Baselinef65ab3639119f9a3e006aa76547d531310e56552; Panda8a16e089/opendbc150f9371. Current packed CAN header, Panda can_comms.h/Python wire functions/native panda.cc; source and test hashes plus actual output in Sunnypilot Ai/Evidence/chimera-can-codec-20261106.json. Contract chimera/docs/CAN_CODEC_CONTRACT.md; session2026-11-06-chimera-can-codec.md. GCC13.2.1/binutils2.42/native sanitizers, ARM artifact and copied-tree build checks. No REA provider analysis claimed.

**Implemented versus proposed/limits:** T04 complete offline. Explicit tests show XOR can miss balanced data changes and a changed DLC can form a valid shorter stream prefix. Checksum validity is not authentication or MCU TX permission; independent policy/message integrity remains mandatory. Main/GPIO/protocol sources and zero capability/hash advertisement unchanged; canonical DBC/Ocelot/archive preserved. No actual USB/CAN traffic, hardware/flash/config/DBC/actuation/install/upstream/push action. Previous QA15's1240-byte image is its historical snapshot; current raw image1840bytes. Physical qualification, USB/status/host lifecycle, input acquisition/Core Config and MCU policy remain pending. Unanswered items below are preserved.

---

## QA-20261106-15 — Continue the board identity and request contract

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue after QA14 with the distinct USB identity/request and bus/input source contract, then implement the next testable firmware piece.

**Answer:** Added a distinct Chimera F413 bootstrap identity, a32-byte versioned manifest and a pure read-only firmware request handler. D6 returns the bootstrap version and A0 returns the manifest; all other vendor requests, control OUT and malformed queries are rejected without changing the reply buffer. The manifest preserves the three-bus/nine-interface source topology but advertises zero operational capabilities/layout hashes. Request and bus/input source contracts explain the future selection, freshness, Core Config and MCU policy boundaries. The handler is compiled and retained in the ARM image;12offline tests pass, including458920sanitized request cases. The raw image is now1240bytes. USB enumeration/EP0/endpoints and native host admission are still unimplemented. Next is the modern classical CAN codec.

**Evidence/source pins:** Baseline0bc14bcfda34a5d087278737fe6293efbfaeac24; Panda8a16e089/opendbc150f9371; original Ocelot dirty sources preserved. Exact hashes, commands/results and source pins in Sunnypilot Ai/Evidence/chimera-identity-contract-20261106.json and session2026-11-06-chimera-identity-contract.md. New contracts in chimera/docs/USB_IDENTITY_CONTRACT.md and BUS_INPUT_CONTRACT.md. GCC13.2.1/binutils2.42; ARM disassembly exposed an alignment dependency, now corrected/tested with -mno-unaligned-access. Official libusb SETUP/type docs support wire interpretation; A0/manifest and rejection policy are new design choices.

**Implemented versus proposed/limits:** T02b pure handler/metadata and source contracts implemented offline; operational health/capability/hash/config ABI and USB wiring/host selection remain pending. ABI version strings are not cryptographic binary attestation. No sampling, relay/OBD-C operation, CAN TX, physical qualification, hardware/flash/config/DBC write, install, upstream update or push. Earlier QA14's1064-byte image describes its original snapshot; this increment is1240bytes. Full T02/T05/T08 and hardware readiness are not complete. Preserve unanswered items below.

---

## QA-20261106-14 — Proceed with the first board firmware increment

**Date:** November 6, 2026 UTC.

**Owner request (original):** let proceed

**Context:** Continue the board-side step explained after QA13; actual firmware belongs inside Sunnypilot, with teacher evidence and incremental checks.

**Answer:** Implemented the first F413 application under sunnypilot/chimera/firmware/: original startup, board GPIO initialization, minimal parked application, linker, offline builder and tests. The build preserves the original bootstub/config boundaries and boot flag, budgets the legacy signing envelope, and explicitly loads the stack before C. It reserves all existing bus/input/relay/OBD-C interfaces; this target sets source-defined inactive output levels and input modes only. Nine offline tests pass and the deterministic unsigned image is1064bytes. This is the first board code, not modern USB compatibility yet; next are the distinct identity/request/bus-source contracts and USB/CAN implementation. Host status adaptation and managed USB use remain pending.

**Evidence/source pins:** Baseline9fa1f81108d2102830d13c0fc03c22b9db6e73d0; Ocelotd87892fa with preserved dirty working-file hashes, ST headerV2.6.0 and source bootstub/signer. Source contract chimera/docs/BOARD_FLASH_CONTRACT.md; exact tests/tool/source hashes in Sunnypilot Ai/Evidence/chimera-f413-bootstrap-20261106.json; detailed session2026-11-06-chimera-f413-bootstrap.md. Existing GCC13.2.1/binutils2.42, native sanitizer tests and ARM artifact inspection used. No REA provider result claimed.

**Implemented versus proposed/limits:** T01a/T03a complete offline and saved locally. Dated status update to QA12/13: those earlier answers accurately described a README-only firmware directory; real source/build now exists. GPIO fixtures/build checks do not prove power-on/electrical states or runtime operation. Installed bootstub/signature identity, recovery/watchdog and physical qualification remain unresolved. No flash, hardware/actuation, config/DBC write, upstream update or push. Unanswered questions below remain untouched.

---

## QA-20261106-13 — Is README completion required before Chimera code?

**Date:** November 6, 2026 UTC.

**Owner question (original):** so after readme is done only then we make it in chimera suynny

**Answer:** The README/folder setup is already done; it is not a remaining gate or a substitute for implementation. Actual Radxa-side USB/identification code has already been written in Sunnypilot's existing pandad module. The new code that runs on the Chimera MCU belongs in sunnypilot/chimera/firmware/ and has not started yet. That firmware step needs the source-backed board/flash/build contract, not more README completion. Documentation is kept alongside verified code increments. Host and MCU work are two parts of the same Sunnypilot project.

**Evidence/source pin:** Fresh folder/README/roadmap inventory at f8cd9177b9e37bfc656b72aeaa61acf59f0440f5; firmware contains README.md only, while pandad has committed panda_usb and panda_identification sources. See QA11/12 for actual implementation and validation limits.

**Implemented versus proposed/limits:** Explanation and notebook only; no runtime source/build/device/update/push action. Existing host backend and offline tests remain as saved; MCU firmware T01/T03 and host status/managed integration remain pending. No new scope or automatic flashing inferred from this question.

---

## QA-20261106-12 — Where the Chimera code is being written

**Date:** November 6, 2026 UTC.

**Owner question (original):** i dont see the chimera codes in sunnypilot were r u making it

**Answer:** All new implementation is inside the actual Sunnypilot project. The Radxa-side USB/backend code is in openpilot/selfdrive/pandad/panda_usb.cc/.h; identification in panda_identification.cc/.h; shared interface in panda_comms.h and Panda's handle declaration in panda.h. Existing chimera.py/chimera_protocol.py provide the separate original-board Python receiver/decoder. sunnypilot/chimera/ currently holds the plan, source map, provenance and a firmware README; no new STM32F413 application source/build target has been written there yet. Recent work prioritized shared host compatibility after the legacy Panda request. The original firmware remains in preserved workspace ocelot/firmware/chimera/. Added direct in-repository code links and explicit firmware status to chimera/README.md; files were not moved or duplicated.

**Evidence/source pins:** Fresh rg inventory and Git show at cd62e21d6757662ef16b86418157fd50966e85d7 confirm code/tests are committed under Sunnypilot, branch radxa/q8b. Firmware directory inventory contains README.md only. Existing source pins/checks remain those in QA11.

**Implemented versus proposed/limits:** Documentation/navigation clarification only. Host backend exists and is tested offline; managed startup and legacy status adaptation are still pending. New MCU firmware remains unimplemented. No product source, build, device, update or push action. Next planned host slice stays T05; board T01/T03 remains separate pending work.

---

## QA-20261106-11 — Proceed with native USB connection and failure handling

**Date:** November 6, 2026 UTC.

**Owner request (original):** proceed

**Context:** Continue the next agreed native USB connection increment after T02a identification; retain teacher-first evidence and incremental checks.

**Answer:** Implemented PandaUsbHandle and an explicit pinned open factory. It discovers only supported normal-mode VIDs/PID, reads actual descriptors, requires a unique matching serial/configuration1 and exclusive interface0, and runs the identification selector before returning. Every failure cleans up its list/handle/context/claim. It does not change USB configuration, detach drivers, reset devices or invoke flash/update paths. Transfers are serialized, capped at1second and not retried; timeout bulk reads retain actual partial bytes, while uncertain/short writes and other I/O errors become unhealthy. Disconnect closes the usable transport state. Original Chimera is read-only: OUT denied and IN restricted to D6/D2 zero-parameter observations, because direction alone does not establish absence of legacy command side effects. Current/F4 transport operations are available only after identification; this is not a safety-profile authorization.

**Actual verification:** Native pandad builds with the existing vendored libusb1.0.29.post103.33fake-USB scenario groups pass, including descriptor/serial/config/claim/identity failures, duplicate serials, all three profile families, partial/timeout/short/unplug/overflow, cleanup and original Chimera command denial. Strict AddressSanitizer/UndefinedBehaviorSanitizer fake suite passes. A real-vendored-library link test exercises only empty-pin rejection before initialization. Existing443identification cases, native interface/CAN codec tests and15Chimera Python tests pass. Initial test compile mixed int/enum initializer types; corrected the fixture type. First fake run leaked an injected error between cases; diagnosed group6 and reset that fixture state. Neither required relaxing product behavior. gdb was unavailable; test diagnostics supplied the location, without installation.

**Evidence/source pins:** Baseline96ea6bd7960374bbf4ebcb23e1cad9bc4b81b864; current Panda8a16e089/opendbc150f9371; Carrot69a2d3be USB reference and teacher reports; Ocelotd87892fa dirty main/USB sources preserve old direction/command dispatch evidence. Installed libusb header and official synchronous/device docs checked (online docs1.0.30; used API matches installed1.0.29). New panda_usb.h/.cc, fake USB and real-library link tests, native build/ignore updates; roadmap/compatibility status and both memory layers saved. Receipt Ai/Evidence/chimera-usb-20261106.json.

**Implemented versus proposed/limits:** T06b offline transport/factory completed. Existing Panda construction/listing and managed startup still select SPI; new USB factory is not enabled there yet. Exact legacy status decoding (T05), protected managed selection/lifecycle (T08), physical USB/CAN/input/relay qualification and Chimera firmware T01/T03 remain pending. No real USB API initialization/enumeration/device access, daemon run, firmware/DBC/config/CAN/relay action, upstream update, install or push. Next host slice: exact legacy status decoding before managed use. Offline tests do not establish live compatibility or guaranteed hardware success.

---

## QA-20261106-10 — Proceed reliably and keep using teacher evidence

**Date:** November 6, 2026 UTC.

**Owner request (original):** see u hvae to make this happen it should not fail ,prced ,take teachers help all the time

**Answer:** Proceeded with the next agreed code increment, consulting the teacher's source reports throughout. Implemented T02a, a native identification/profile selector requiring an explicit serial/version pin, matching descriptor and transport serial, supported normal-mode identity, exact reported versions and exact initial health length. Current Panda, reviewed Carrot F4 and original Chimera have separate branches. Chimera uses its descriptor/D6/health43 contract and is not sent unsupported C1/DD requests. All identification operations are bounded control-IN reads; failures throw without initialization, reset, CAN, configuration or flash writes. Current protocol hashes are derived during the native build from the same source headers used by firmware. Caller must exclusively own the transport and supply descriptors from that device.

**Actual validation:** Test first failed because the new header/API did not exist. Native pandad and identification/interface/CAN codec test binaries build. Identification tests accept19 source-based fixtures, reject421 malformed/incompatible fixtures and reject3 invalid transports; fake transport forbids all OUT and bulk operations and reports zero writes. Address/undefined-behavior-sanitized strict build/run passes the same cases. Existing native transport/CAN tests and15 Chimera Python tests pass. Tests cover descriptor/pin mismatch, bootstub/DFU, short/overlong/failed reads, hash/numeric-version mismatch, disconnect and unsupported board types. This is source/CPU validation, not a guarantee of hardware success.

**Evidence/source pins:** Baseline b76db53c3ea69da38d55bc0056c32c325f0329b3; Panda8a16e089/opendbc150f9371, Carrot69a2d3be and Ocelotd87892fa dirty references. Used teacher November5 deep review and November6 Carrot/source map; no new REA artifact analysis was needed. Native sources panda_identification.h/.cc, focused native test and pandad SConscript/ignore. Compatibility doc and roadmap retain incomplete task status. Receipt Ai/Evidence/chimera-identification-20261106.json.

**Implemented versus proposed/limits:** T02a completed; T02 overall remains partial. Selector is in the native library but not yet used by startup. Existing generic Panda/updater behavior is unchanged and must not be described as protected by this new helper. Next USB transport/factory must provide real descriptor identity and call this selector before initialization; status decoding and protected managed selection remain pending. T01/T03 board/flash/build remains separate. No device/daemon/USB enumeration, firmware/DBC/config/relay/actuation, upstream update or push. Teacher-first use is reaffirmed; reported firmware text is not cryptographic image attestation and live compatibility remains unqualified.

---

## QA-20261106-09 — Meaning of keeping SPI and how to complete legacy USB

**Date:** November 6, 2026 UTC.

**Owner question (labelled paraphrase):** What does keeping the current SPI backend mean, and how do we proceed with device/protocol identification, USB backend and legacy status decoding?

**Answer:** SPI is the existing direct-hardware transport used for integrated Panda hardware. Keeping it preserves that connection option; our Radxa-to-Chimera link will use USB. The completed common interface exposes control/bulk operations, but the native constructor/list still choose SPI, so it cannot yet connect through USB. Next define and test read-only device/protocol identification against pinned current/F4/Chimera replies; add bounded libusb control/bulk transport with fake short-read/timeout/unplug/cleanup tests; decode each supported status layout into host state with exact-length/version checks; then integrate protected selection and managed passive RX. Current health49, reviewed Carrot F4 health59 and original Chimera health43/mailbox16 are separate profiles. Existing chimera_protocol.py serves the old separate Python receiver, not the new native USB driver or F4 status decoder. A hardware family alone does not identify installed firmware. Initial identification must not perform generic initialization/flash writes, and no H7 automatic update path may select an F4/Chimera device. Real-device passive qualification follows the offline pieces.

**Evidence/source pins:** Sunnypilot538e46a89, native panda.cc constructor/list, panda_comms.h interface, Python Panda.connect setup writes, chimera_protocol.py decoder and the compatibility document. Carrot69a2d3be profile59/numeric17/4/5; current Panda8a16e089/opendbc150f9371 profile49/hash versions; Ocelotd87892fa dirty source profile43/mailbox16. Actual T06a checks remain in Ai/Evidence/chimera-legacy-transport-20261106.json.

**Implemented versus proposed/limits:** This turn explains and documents the sequence; it does not implement a USB backend, identify a device or decode new status. T06a remains complete, the other slices pending. Immediate next implementation is read-only identification/profile validation with fake replies; board flash/build T01/T03 remains a separate stream. No hardware/build/firmware/DBC/update/push action.

---

## QA-20261106-08 — Build Sunnypilot to support legacy Panda alongside Chimera

**Date:** November 6, 2026 UTC.

**Owner request (original):** build in a way our sunnypilot supoort the legency panda

**Answer:** Made legacy Panda support an explicit host design requirement alongside Chimera. Initial legacy target is the reviewed Carrot F4 hardware family (white/grey/black/UNO/DOS), with firmware-specific protocol profiles rather than assuming every old Panda uses one layout. Current native pandad is SPI-only; current status49/hash versions, Carrot status59/numeric17/4/5 and original Chimera mailbox16/status43 are distinct. First implemented T06a: a shared native PandaCommsHandle interface, current PandaSpiHandle implements it, and Panda owns the interface. This allows a later USB backend without tying host logic to SPI. Current constructor/listing, SPI wire implementation, buffer limits, firmware updater and safety behavior are unchanged. A compatibility matrix and remaining USB/status/discovery/lifecycle slices are saved in chimera/docs/LEGACY_PANDA_SUPPORT.md.

**Actual verification:** Native interface test first failed because the shared type did not exist, then passed after implementation. ARM64 SCons build of pandad and both native tests passed; native interface and CAN codec tests passed; 15 existing Chimera Python tests passed. Initial build attempts used an unsupported --extras flag and then missed capnpc on PATH; reading the project options and activating the existing venv resolved those invocation errors. No tool installation, compiler suppression or product workaround. No daemon/device was opened by these tests.

**Evidence/source pins:** Baseline Sunnypilot1120411362fd52b462ddee656061f23b78422b58, Panda8a16e089/opendbc150f9371; Carrot source69a2d3be provides reference transport structure/F4 contracts; Ocelotd87892fa dirty source remains unchanged. New native changes: pandad/panda_comms.h, panda.h, SConscript, .gitignore and tests/test_panda_comms.cc. Existing reports and explicit compatibility doc retain the source distinctions. Validation receipt Ai/Evidence/chimera-legacy-transport-20261106.json.

**Implemented versus proposed/limits:** T06a shared host boundary completed; full T06 stays partial. No USB backend, legacy59-byte decoder, automatic profile selection or managed legacy support is implemented yet. Unknown/other old firmware is not declared compatible. T01/T02/T03 board/flash/contracts/build work remains pending; next freeze read-only identity/protocol contracts and implement bounded USB transport before managed external selection. No firmware/DBC edit, flash/config/CAN/GPIO/relay action, upstream update or push. This is an incremental support foundation, not a live legacy-Panda or vehicle qualification.

---

## QA-20261106-07 — What do board/flash layout and minimal F413 build mean?

**Date:** November 6, 2026 UTC.

**Owner question (labelled paraphrase):** What will we actually do in the proposed board/flash-layout and minimal F413-build steps?

**Answer:** First turn the already known Chimera GPIO assignments into the new board definition and specify which flash regions belong to startup/recovery, application and saved settings. The legacy source reserves the first16KiB for the bootstub, starts the application at0x08004000 and stores configuration in sector5 at0x08020000. A new linker/build must keep the complete signed application within its selected space and preserve configuration; exact total MCU capacity/installed-image proof remain separate. Then add a small STM32F413 startup/build target inside sunnypilot/chimera/firmware/, configure the CPU/clocks/vector table and defined initial GPIO behavior, compile it into ELF/binary, and inspect its addresses/size. This proves our new project can produce a correctly laid-out F413 image; it does not yet implement modern USB or Sunnypilot compatibility. The existing Ocelot build is already known to exist. USB codec/status and native host support come in later verified increments. This question requests an explanation; no firmware implementation or flashing was performed.

**Evidence/source pins:** Project0834e890f, chimera/tasks/plan.md T01–T03, chimera/firmware/README.md; Ocelotd87892fa dirty reference, firmware/stm32_flash.ld (_app_start and MEMORY), firmware/bootstub.c and firmware/chimera/chimera.h (sector5/config address). Existing GPIO/build facts retained by QA04/05. These addresses describe the legacy intended layout, not a freshly verified installed flash dump.

**Implemented versus proposed/limits:** Explanation and notebook only. S00 folder remains complete; T01–T03 still pending. No build, source/DBC behavior change, device action, update or push. Next remains T01 then T02 contracts and T03 minimal offline target; no modern communication compatibility claim.

---

## QA-20261106-06 — Create Chimera inside Sunnypilot and build incrementally

**Date:** November 6, 2026 UTC.

**Owner request (original):** let first make chimera folder inside sunnypilot ,lets build one by one

**Answer:** Created the regular tracked directory `sunnypilot/chimera/` as the active implementation home, using Sunnypilot's existing Git history. It contains a README, local instructions, firmware destination, incremental T01–T20 roadmap, exact copied firmware source map/hash receipt and starting provenance. The original workspace `chimera/` archive and dirty Ocelot source remain preserved. Required implementation inputs will be imported with provenance as needed; the new implementation will not require outside workspace folders at runtime.

**Evidence/source pins:** Sunnypilot baseline044772ac169069105763c2547484324a372fbead, workspace Chimera224cfa645134db91103c55d8188d87e7976b0ba4; source map retains Ocelotd87892fa plus dirty bytes. Current Panda8a16e089/opendbc150f9371 and Carrot69a2d3be references remain unchanged. See project `chimera/docs/PROVENANCE.md` and `chimera/tasks/plan.md`.

**Implemented versus proposed/limits:** S00 folder setup completed. No new firmware/build target or host behavior, flash/config/device/relay action, upstream update or push. Next slice T01 records source-backed GPIO/reset and flash/config/recovery boundaries, then T02 identity/RPC/bus-source contracts and T03 minimal offline F413 target. The original detailed roadmap remains evidence; active implementation now belongs inside Sunnypilot. Folder checks verify real directories, local links, copied-byte equality and ignore rules; they are not firmware/hardware tests.

---

## QA-20261106-05 — Why were already recorded firmware facts missed?

**Date:** November 6, 2026 UTC.

**Owner question (original):** see techeer alreasy knw about it ,then why it didn tdo the first time

**Answer:** The teacher notes already contained the information. The November 5 Ocelot note records the direct-input pins and transceiver controls; October 4 entries record the local build helper, toolchain and successful Chimera builds. The agent failed to reconcile those existing facts with the new completeness checklist and used wording that conflated unverified electrical/modern-build qualification with missing source definitions/build infrastructure. This was an evidence-retrieval and synthesis failure in the answer, not missing owner information. The owner should not have needed to point back to the firmware folder. The latest source map consolidates existing knowledge and freshly checked details; it must not be presented as all newly discovered knowledge.

**Evidence/source pin:** `Ai/Knowledge/Repos/ocelot.md`, sections “2026-11-05 — Chimera native input and CAN contract”, “2026-11-05 — Direct Ocelot Chimera source review” and October 4 build/location follow-ups. Historical build source94efc673 and current reference d87892fa plus dirty bytes remain distinct. QA-20261106-04 corrects the broader gap wording.

**Implemented versus proposed/limits:** Logged this accountability explanation and corrected the handoff. No firmware/host/hardware action or push. Before declaring evidence missing, follow teacher entries into their original reports/source and reconcile known versus unverified facts. This is a documented correction, not a guarantee against future retrieval mistakes or a claim of new hardware validation.

---

## QA-20261106-04 — Inspect Ocelot Chimera firmware as the board baseline

**Date:** November 6, 2026 UTC.

**Owner question (original):** see the firmware folder insdie the ocelot ,chimera  this will give an idea

**Answer:** Yes. The four Chimera files plus shared gateway/common board files define the existing implementation: STM32F413/Cortex-M4, MCU CAN1/2/3 on host buses 0/1/2, transceiver enables, PA3 ignition, PA4 speed pulses, PA5 crank pulses, PA6 brake, PC2/PC3 analog inputs, PB0 relay, PA2 OBD-C request and PB1 OBD-C ignition. The code also supplies legacy USB mailbox/status handlers, 776-byte flash configuration and input/report timing. The existing local build helper and toolchain are present. We should use these board assignments and acquisition paths as the preservation baseline while adapting USB/status/host support and explicit MCU safety policy.

**Dated correction to QA-20261106-03:** Logical source pin assignments and a legacy build path are known, not missing. Earlier gap wording was too broad. Complete electrical connector/conditioning/load-path evidence, a reproducible modern image and proof that installed nightly matches these dirty local sources remain unresolved. Relay follows ignition; USB/OBD-C request gating is commented out. Do not equate preserving this circuit with already implemented heartbeat cutoff.

**Evidence/source pin:** Ocelot d87892fa25ef2a2474110b97bfb5245ee818b534 plus preserved dirty source/local helpers. Selected source map is saved as `chimera/docs/FIRMWARE_SOURCE_MAP.md` and student `Ai/Knowledge/CHIMERA_FIRMWARE_SOURCE_MAP.md`. `chimera/evidence/firmware-source-map-20261106.json` hashes 19 source/dependency files; all 94 original entries and 93 frozen copies match, and Ocelot's 39-line dirty state is unchanged. GCC13.2.1, objcopy2.42 and SCons4.5.2 version checks passed. Direct SCons initially lacked its local PYTHONPATH; rerun with build_local.sh's library directories passed without installation.

**Implemented versus proposed/limits:** Source inspection, documented mapping and corrected gaps only. No firmware/application/DBC change, build, device handle, flash/config/CAN/GPIO/relay operation, new REA run, upstream update or push. Modern implementation tasks remain pending. Next use the recovered board baseline for T01/T02 and offline target design; physical/installed verification remains a distinct qualification step.

---

## QA-20261106-03 — Do we have all Chimera data, or is anything missing?

**Date:** November 6, 2026 UTC.

**Owner question (original):** so we have all the data for chimera right ,did we miss somrthing

**Answer:** We have a substantial source/reference base, enough to begin bounded offline engineering, but not all verified board or installed-firmware data. Missing/unverified items include the exact owner-board schematic/revision/power and OBD-C map; exact source/build provenance for the saved nightly; a complete current installed bootstub/configuration recovery set; full reproducible new F413 build inputs and signed partition budget; measured three-bus receive behavior, input calibration and actual vehicle signal definitions; relay/load/fault measurements; and final protocol/source/configuration decisions. Existing original nightly and past application restoration evidence are present, so recovery is not wholly absent. Local build bootstubs are not installed bootstub dumps. Selected source snapshots and offline codec checks are not a finished firmware/managed integration.

**Collection gap found and closed:** The host still held 17 historical Core Config backup/quarantine files outside the new Chimera folder. Copied exact bytes and provenance to `chimera/recovery/legacy-core-config-20261106/`; eight config blocks have valid magic/CRC32 and one erased-flash block is retained as incident evidence. Originals are unchanged. These are historical backups, not a fresh current-board read or authorization to restore/watchdog-enable/clear quarantine.

**Evidence/source pins:** Local audit against `chimera/SPEC.md`, roadmap/checklist, hardware/research/config notes, earlier teacher recovery records and Core Config user-data directory. Audit receipt `chimera/evidence/completeness-20261106.json`; gap checklist `chimera/docs/DATA_GAPS.md`; student `Ai/Knowledge/CHIMERA_DATA_GAPS.md`. Prior source pins remain current Panda8a16e089/opendbc150f9371, Ocelotd87892fa plus preserved dirty bytes and Carrot69a2d3be. Local Chimera ELF still matches retained REA hash5ae9b4f6; no new REA or installed-image claim.

**Saved archive/gap checkpoint:** Local Chimera commit `603ea76aceaa17e75adeb57cd498f974cf0333c8`; not pushed.

**Implemented versus proposed/limits:** Documentation and local archival only. No device handle, USB/CAN/config write/restore, flash, GPIO/relay/actuator action, runtime source change, install or push. Next T01/T02 resolves board/partition/recovery and identity/RPC/bus-source contracts; OBD-C and active-control qualification are later gates. Exact old source helps reproduction but need not block all new known-source offline work. Existence, completeness and tested integration remain separate.

---

## QA-20261106-02 — Where Chimera evidence and references are saved

**Date:** November 6, 2026 UTC.

**Owner question (original):** were is chimera evidence and refercne saved?

**Answer:** The dedicated board home is `/home/radxa/comma/chimera/`. Verification results and scripts are in `chimera/evidence/`; frozen source/reference data in `chimera/reference/`; the latest CarrotPilot snapshot in `chimera/reference/carrot-wip-20261106/`; board documents/photo/connector drawing in `chimera/hardware/`; original nightly bundle in `chimera/recovery/`; roadmap in `chimera/tasks/plan.md`. Selected original workspace sources are under `reference/workspace/`, and the earlier deep review under `reference/prior-review/`. Sunnypilot also retains portable reports under `sunnypilot/Ai/Reports/carrot-wip-panda-20261106/` and `panda-chimera-deep-review-20261105/`.

**Evidence/status/limits:** Each listed path was freshly checked to exist. Files were already saved; this answer only clarifies their locations. No firmware/application/hardware change or push. Source pins, test coverage and integration limits remain those in QA-20261106-01 and the report manifests.

---

## QA-20261106-01 — Fetch CarrotPilot carrot-wip and inspect older Panda support

**Date:** November 6, 2026 UTC.

**Owner question (original):** see fetch data of carriotpilot-wp ,see it is suing legacy panda ,see its code

**Answer (plain-English record):** Interpreted the spelling as CarrotPilot's carrot-wip branch in ajouatom/openpilot,consistent with the teacher's earlier reference; exact-name repository searches did not find carriotpilot-wp/carrotpilot-wp. Fetched31selected files at69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7. Yes,the source retains older F4 Panda support: an STM32F413/Cortex-M4 build with app0x08004000,white/grey/black/UNO/DOS board definitions and F4/H7 Python support. It also retains a native libusb USB backend alongside SPI,unlike our current SPI-only native host. However,older hardware support does not mean the earliest USB wire format: Carrot uses6-byte/XOR CAN headers,not Chimera's16-byte mailbox format. Its status protocol is59-byte health/version17,64-byte CAN-health/version5 and CAN version4 returned as3bytes by DD; our current Panda has49-byte health and8-byte hash-version response.189classical frame encodings match our current Panda exactly. Native Carrot USB accepts3801:ddcc only,so it would not directly select our historicalbbaa:ddcc Chimera. Its automatic reset/flash/recovery flow and Panda board GPIO/harness behavior cannot be applied unchanged. F413 HAL/bxCAN and native USB transport are concrete T03/T06source candidates,with Chimera-specific identity,input/relay/config/safety and current status adaptation still required.

**Evidence/source pins:** Carrot branch69a2d3be,commit time2026-11-06T10:27:29Z; prior November1 Carrot4a555c75 remains historical lateral evidence. `/home/radxa/comma/chimera/reference/carrot-wip-20261106/` contains the source and manifest; student `Ai/Reports/carrot-wip-panda-20261106/README.md` contains the self-contained report. All31Git blobs/SHA256 match the pinned,non-truncated7,319-entry tree; no root.gitmodules or legacy_panda path at this pin. Key files:panda/SConscript,board/SConscript,stm32f4/board.h,board/drivers/bxcan.h,board/health.h,python/__init__.py,andopenpilot/selfdrive/pandad/{panda.cc,panda_comms.cc,pandad.py}. Protected Sunnypilot baselinec1811280/Panda8a16e089/opendbc150f9371; Chimera77464e0before this research; Ocelotdirty reference unchanged.

**Actual verification:**189classical frames across3buses/7addresses/lengths0–8 match both encoders;4,158two-decoder split checks and378checksum-corruption rejections pass. Native C++ structure fixture using unchanged headers measures59/64/6/49/64bytes and matches Python formats. This does not import Panda,open a device,build ARM firmware or qualify FD/managed hardware. Bulk source-save argument-limit and initial pragma-once fixture errors were corrected in tooling,without compiler suppression or changing fetched/product source; limits retained in the report.

**Saved board reference:** Local Chimera commit `ea2651cb7c3576350e61c16ed79f525d10fd6736`; not pushed.

**Implemented versus proposed/status:** Source snapshot,research report and roadmap candidate note saved; no firmware/application/DBC change,flash/config/CAN/relay action,full clone,install,push or upstream update. Existing tasks remain pending; this is a reusable source lead,not a drop-in Chimera image or evidence of live compatibility. Next review F413/USB components during T01/T02identity/partition/bus-source contracts before implementing T03/T06. Exact intended spelling remains inferred rather than owner-confirmed,but the earlier teacher source and branch name corroborate it.

---

## QA-20261105-14 — Audit, update GitHub and shut down both computers

**Date:** November 5, 2026 UTC.

**Owner question (original):** audit update gituhb shutdon pc and radxa

**Answer (plain-English record):** Audited the saved Chimera/Sunnypilot work and published all nine previously unpushed notebook/research commits plus the fresh audit to Deggory/radxa-pilot, branch radxa/q8b, at967082679a2b3f96cef5c92c24df1457c218574e. Created the private Deggory/chimera repository and published the board evidence/roadmap at initial evidence306c0c8e1fc073d12af9f6d4f6c2d93c90a0a2a7 and closeout77464e015d60b873bb6101350a43fef14708ea43, default planning/modern-usb, with Actions disabled. The public audit README blob independently matches GitHub; private backup REST/Git readback matches. Fresh21software tests,189mailbox/336modern vectors,94source entries/93copies and recovery-image checks pass. Ocelot dirty work and Panda/opendbc pins are preserved; runtime source is unchanged. Initial audit runs used the wrong Python/import context; retained errors were resolved by using the existing project venv,without product changes. PC is reachable through its saved trusted host alias. Original normal PC shutdown started and SSH became unreachable; the attempted no-prompt retry could not connect and was not delivered. Radxa normal GNOME poweroff is queued with a120-second timer,read back active/waiting. No force or inhibitor override; physical poweroff is not directly observed. Final request receipt is published with this handoff.

**Evidence/source pin:** Student `Ai/Reports/chimera-shutdown-audit-20261105/` contains tests/layouts/native-build/hash/scan/publication evidence; notebook checks and final local commit validation follow. Teacher `/home/radxa/comma/Ai/Reports/chimera-shutdown-audit-20261105/shutdown.json` and `final-publication.json` record actual shutdown request/readbacks and final branch SHA. Public master932ff06d/defaultmaster and support150f9371 are preserved. Private GitHub app access returned404; authenticated gh REST/Git verified the backup.157selected files passed a narrow credential-signature scan; not a complete secret audit.

**Implemented versus pending/limits:** Audit and initial publication completed. PC shutdown initiated/SSH unreachable; Radxa shutdown timer queued and confirmed waiting. This final notebook/request receipt is published next; final remote SHA is in teacher final-publication.json. No forced shutdown,discard,firmware/config/CAN/relay/vehicle action,upstream update or active-control implementation. Local editor autosaveafterDelay/backups0; explicit SaveAll/physical poweroff not independently verified. Next restart remains Chimera roadmap review followed by T01/T02partition/recovery/identity/RPC/bus-source contracts. Onboard relay preservation is in scope; actuation remains unqualified.

---

## QA-20261105-13 — Roadmap for modern USB Chimera on Radxa Sunnypilot

**Date:** November 5, 2026 UTC.

**Owner question (labelled paraphrase):** Make Chimera hardware work over USB with our new Sunnypilot on Radxa, using the latest accepted Panda USB protocol. Preserve CAN0 Cores/control = MCU CAN1/host0, CAN1 ADAS = MCU CAN2/host1, CAN2 vehicle/retrofit = MCU CAN3/host2; keep ignition, speed/crank pulse, brake, two analog inputs and the onboard actuator power relay. Retain RetroPilot Core Config usability, explain OBD-C and existing code, create a chimera folder, deeply research and explain what/why in a roadmap before changing firmware.

**Answer (plain-English record):** Created `/home/radxa/comma/chimera/` with a proposed capability map, requirements, source-pinned research, hardware/OBD-C evidence, frozen selected references, original nightly recovery bundle and20ordered implementation tasks. Firmware alone is insufficient: our managed native pandad is SPI-only, so add a protected native USB host transport/lifecycle alongside F413 firmware modernization. Use the pinned modern six-byte/XOR classical CAN stream, exact validated status/version responses and a distinct Chimera identity; reject CAN-FD and prevent stock H7 auto-update/recovery. Preserve physical buses0/1/2 and all direct inputs. Current generated reports are onbus0 while physical host parser selectsbus2; explicitly select signal sources/delivery rather than silently remapping. Update Core Config's legacy16-byte transport and separate Chimera USB settings from attached Core typed-CAN transactions, with exclusive offroad USB ownership and transactional/watchdog-qualified writes. OBD-C is a comma power/CAN/sideband accessory connector, while Radxa normally uses USB Type-B; local code already reads PA2 relay request and drives PB1 ignition, but exact Chimera connector routing is unverified. Preserve onboard PB0 relay circuit; wiki documents cutoff of only three CAN0 12VR ports, and current code follows ignition with request gating commented out, so it does not prove all actuator power is removed. First resolve partitions/recovery/identity, then offline implementation, isolated passive receive, managed lifecycle, inputs/source routing, all-TX MCU policy, safe configuration and measured relay/accessory behavior. Active profiles/vehicle actuation are separate future qualification.

**Dated scope correction:** The latest owner instruction explicitly includes preservation and later qualification of Chimera's onboard power relay. Earlier “relays excluded” scope is superseded for this circuit in the roadmap only. It does not select external Relay Core work or authorize operating/energizing relays during research.

**Evidence/source pins:** Sunnypilot research baseline e888f9393537c45c50c2a18a13573a989aef5617; Panda8a16e089b88593914823743df29e1c30b7dd3e00; opendbc150f937198ceab43c43b39f94b9bdea63fcb633c; Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 with pre-existing dirty state. `/home/radxa/comma/chimera/reference/SOURCES.json` has94entries,93copied; all75prior source hashes match. Roadmap `/home/radxa/comma/chimera/tasks/plan.md`; technical research `/home/radxa/comma/chimera/docs/RESEARCH.md`. Official wiki/ST family datasheet and comma harness connector drawing; drawing blob2d4033ff6040586950069881d6f53f998a5fcbf8. Prior hash-matching REA artifact analysis reused, not a new run or installed-image proof. Primary-source receipt distinguishes successful web/drawing reads from failed ST local downloads/RM0430 read.

**Board-folder checkpoint:** Local commit `306c0c8e1fc073d12af9f6d4f6c2d93c90a0a2a7` on `planning/modern-usb`; no remote/push.

**Status and limits:** Folder/evidence/roadmap implemented; all firmware/host modernization tasks proposed and pending owner roadmap review. No firmware/application source edits, build/flash, device handle, config write, CAN TX, relay/actuator operation, push or upstream update. Existing dirty Ocelot preserved. Fresh checks cover copied-file hashes/ZIP member, documentation links, Q&A sync and project scope; earlier189/336codec vectors and21software tests are retained historical evidence, not rerun here. Exact installed-nightly source, board electrical/OBD-C/power map, calibration, all-load cutoff and managed hardware qualification remain unresolved. Next T01/T02 evidence and interface contracts before implementation.

---

## QA-20261105-12 — Understand current Panda, legacy Panda and Chimera in depth

**Date:** November 5, 2026 UTC.

**Owner question (original):** i want u to about current panda ,legecy ,panda and our chimera code in depth ,you shuld knw everything about it ,ask teacher wat it knw

**Answer (plain-English record):** Read the coordinating teacher first,then traced the principal host/firmware/safety/lifecycle paths and saved a detailed source-pinned reference. Current project Panda8a16e089 uses an H7 firmware and a Python USB/SPI client; managed native pandad is SPI-only and adds ignition/health/heartbeat/safety/firmware orchestration. Older mailbox-era Ocelot/demo uses16-byte CAN records/43-byte health; retained C2uses5-byte headers,64-byte USB packet counters and50-byte health; current Panda uses6-byte XOR-protected headers and49-byte health,plus64-byte per-bus health. They cannot be interchanged by sharing a USB ID or method name. Current MCUcalls safety TX/RX/forwarding hooks; reviewed Chimera TXdoes not,and C2RetroPilot safety is WIP. Our mode39is source-registered but production init has no active profile; its presence does not install enforcement on Chimera. Our dedicated receiver pins identity/version,decodes exact mailbox/health layout and publishes CANonly,without writes/readiness/lifecycle. Local Chimera synthesizes onCAN0while our physical parser selectsbus2; raw reception/returned receipts do not automatically resolve that route. The exact installed-nightly source remains unavailable; full knowledge of unobserved installed behavior cannot honestly be claimed.

**New dated correction:** Current Python Panda connection itself sends configuration writes before later support filtering: fake-handle execution observed9vendor OUTwrites by default and7even with disable_checks=False. Missing version response becomes(0,0)without preventing those setup writes. Managed wrapper's startup health/support loops construct Panda before rejecting external devices,and DFUsweep precedes selection. Earlier shorthand that external filtering protects Chimera from all stock-startup actions is incomplete. No actual write/flash was performed here. Current pin8a16e089supersedes older teacher74a0adceas a description of this checkout; older source observations remain dated evidence. Current native E0log-read/dormantFBsleep helpers also differ from firmware B6/B5handlers; source-level gap,not a new runtime failure.

**Implemented versus proposed:** A detailed engineering reference,75-file source hash/coverage inventory,remote source receipt,reused matching REA excerpts and offline verification script/results are saved in student Ai/Reports/panda-chimera-deep-review-20261105/. Production application,firmware,DBC,safety and transport sources unchanged; no device handle/discovery,daemon start,USB/SPI/CAN action,flash/config/relay output,push or upstream update. No simulator explanation used.

**Evidence/tests:** Parentbeforead7efa20849305682e99337fff4a710c91fb7c51; Panda8a16e089b88593914823743df29e1c30b7dd3e00; opendbc150f937198ceab43c43b39f94b9bdea63fcb633c; Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534/pre-existing39status lines preserved. C2parentb9a942e/Panda9e6d47f and mailbox-demoe2ce83cb retained. GitHub pinned Python blob9d562fc1matches local; exactde193215ref lookup still404. Offline189mailbox/336modern packet vectors,all split points/single-bit positions,43/43/50/49health layouts,64-byte CANhealth,and fake constructor9/7writes pass. Fresh GCC13.3native communications fixture plus21existing modern/Chimera tests pass0failures/errors/skips. Matching historical REA ELF SHA5ae9b4f6/selected GNUdisassembly reused,not installed nightly or new REArun. Initial verifier missing fake-class global and lint issues corrected in report tooling,not product source. Documentation/source/status/QA validation follows in session/ledger. Exact nightly implementation,physical current state,complete managed bridge and MCU/endpoint safety remain unresolved; no claim every board/car mode or line was audited. Source-driven,documentation,Git,code-review and verifier-debugging workflows used.

## QA-20261105-11 — Chimera’s own inputs and expected CAN data

**Date:** November 5, 2026 UTC.

**Owner question (original):** okay lets see wat are the input and can bus data chimera expect ,dont bring beamng reference here

**Answer:** Chimera accepts direct ignition,VSSspeed pulses,CPScrank pulses,brake-switch and two external0–5Vanalog inputs. Saved HALL calibration selects pulses per distance for speed and reluctor/missing-tooth parameters for RPM; analog reference/tolerance mappings detect four cruise buttons. The local parser extracts vehicle CAN on boardCAN2(host2/MCUCAN3),using configurable IDs/bit fields/scaling for steering angle main/fraction/rate,speed,ignition,RPM and brake(entries1–7); there is no universal fixed OEM input-ID list or automatic OBD polling implemented by that parser. CAN0 is the Core/control-side bus,CAN1the ADAS-side bus; all3buses have a raw USB receive path. The menu advertises CAN cruise buttons11–14but this handler does not implement them; ADC buttons are implemented. The generated reports go out boardCAN0:0x50angle/DLC6,0x75engine/DLC8,0x76speed/DLC8,0x100cruise/DLC8; they are output definitions, not required incoming OEM IDs. Source timer scheduling implies nominal20Hz per enabled group,not a measured rate.

**Limits:** Local integer CAN extractor ignores endian_type,does not verify actual DLC/OEM integrity/freshness,and masks CAN RPM toonebit. Some generated-output paths dereference missing configs; speed mode reads config3instead of4; CRUISE ADC placement does not prove canonical compatibility. ADC/menu and installed-image gaps remain. Source findings are not measured behavior of installedde193215. Scope stays on Chimera’s own hardware/protocol; no external simulator framing used in the answer.

**Implemented versus proposed:** Read-only source/wiki explanation and durable notes. No code/config/source mapping change,device access,build,flash,CAN output or push. No new integration or physical calibration claimed.

**Evidence/source pin:** Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 with pre-existing dirty main.c/chimera.h preserved; parentc67074b7a10149f84747358ace59d8b1f8f15d16. Student Ai/Evidence/chimera-native-inputs-20261105.json hashes8selected source files and records mappings/status. main.c520–560configured input,603–711generated reports,759–774ADC buttons,832–930pulse routines,1026–1056direct/HALL selection; chimera.h362extractor; stm_flash_config.py17menu. Official https://wiki.retropilot.org/index/hardware/chimera checkedNovember5for inputs,bus roles and config intent. Original20-message prefix in canonical retropilot/dbc compared as reference; source implementation differences retained. Source-driven/documentation/Git skills reused; no REA binary question or new runtime result. Documentation validation recorded in session/ledger; upstream hold unchanged.

## QA-20261105-10 — Which Chimera bus connects to the car CAN/OBD?

**Date:** November 5, 2026 UTC.

**Owner question (original):** see his wiki page were did he connect the obd of car i mean which can bus

**Answer:** The Chimera wiki’s Installation example connects the car’s CAN High and CAN Low to Chimera CAN2. This is board/host bus2, corresponding to MCU CAN3 in the reviewed local source. The wiki does not specify the car-side OBD connector pins or prove a particular vehicle’s OBD port exposes the required signals. Chimera’s separate OBD-C connector is described as the connection to comma devices. Thus CAN2 is the vehicle-side bus in that example; the physical label still matters when interpreting the owner’s earlier “CAN3”.

**Evidence/source pin:** Official https://wiki.retropilot.org/index/hardware/chimera checked November5,2026; Installation lines103–110 explicitly lists CANH/CANL on CAN2; features/ports lines27/55 describes OBD-C. Local ocelot/firmware/chimera/can.h142–146 maps MCUCAN3 to hostbus2; reviewed referenceHEADd87892fa with pre-existing dirty work, parent0f045d5b914233c4d7a102f597331760118fa93d. Source/documentation/Git workflow reused; no REA artifact question.

**Implemented versus proposed/limits:** Documentation clarification only; no wiring,source,USB/CAN,firmware/config change or push. No vehicle-specific OBD pinout, harness compatibility or signal availability established. Prior zero-frame issue and upstream-update hold remain. Next confirm actual board connector label and qualify physical receive path.

## QA-20261105-09 — Inspect Chimera inside ocelot

**Date:** November 5, 2026 UTC.

**Owner question (original):** see inside ocelot folder about it

**Answer:** Inspected the actual Ocelot firmware, board support, Python host, desktop bridge, hardware guide and retained image/candidate files. Chimera main.c owns USB/health/config/sensor processing and startup; can.h owns raw mailboxes/queues; gateway.h owns CAN GPIO and transceiver-enable pins. The GATEWAY build enables all3transceivers via PC1/PC13/PA0 and initializes controllers at500kbit/s/non-silent. All3RX handlers call can_rx, which queues raw frames for USB endpoint0x81 independently of stored sensor mappings. Thus empty sensor configuration alone does not suppress raw USB CAN in this source. Health voltage/current and safety17 are hardcoded, so zero voltage/current are not power measurements and17is not modern enforcement proof. Actual can_send lacks safety_tx_hook and0xDCchanges relay request. Stored speed fields do not set startup bitrate;0xDEacts only on bus0. The default Core Config is a native read-only WebKit/site window; the guarded Tk tool is separate. Its lower-level USB helper drops partial data on timeout, unlike the Sunnypilot receiver that preserves timeout bytes; this is a desktop diagnostic limitation, not a proven cause of the previous capture. hardware/chimera contains a photo/guide, no dedicated schematic; ocelot-gateway design files are a separate reference and do not prove the actual Chimera power tree.

**Implemented versus proposed:** Read-only local investigation and memory update only. Ocelot pre-existing tracked/untracked changes preserved. No device script imported/executed, USB handle, build, CAN action, patch, flash or push. test_relay_chimera.py sends a safety request and repeated heartbeats and was not run. Next resolve actual installed-nightly behavior and physical receive path before any targeted implementation.

**Evidence/source pin:** Ocelotd87892fa25ef2a2474110b97bfb5245ee818b534 with pre-existing dirty Chimera main.c/chimera.h; Sunnypilot5c5785872cd05857c0ca828b0c60ad6b7e53c848. Student Ai/Evidence/chimera-ocelot-source-review-20261105.json hashes16selected source files and records exact Git status. Saved nightly ZIP SHA8158f29132e88bff946cbe23b72d269fa2e6aeb4d6ca5aba7b9539ac04ec043c contains Chimera image27976bytes/SHAe35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b. Exactde193215commit is absent from local Git objects; local source is not proven installed code. Existing failed-float-candidate/recovery records remain applicable. Source-driven/documentation/Git workflow reused; no new REA result or hardware compatibility claim. Documentation/source-hash checks recorded in session/ledger. Upstream updates remain paused; this does not resolve measured rails/ACK/bitrate/connector state.

## QA-20261105-08 — Resume Chimera and explain teacher knowledge

**Date:** November 5, 2026 UTC.

**Owner question (original):** lets work on chimera ,ask teacher,tell everything u  knw about it

**Answer:** Teacher evidence identifies Chimera as the intended USB/CAN and direct-sensor bridge for modern Sunnypilot on Radxa Q8B; Interceptor Core and Actuator Core remain selected parts. Three logical buses are CAN0/1/2, with MCU CAN1/2/3 mapping to host0/1/2. The owner’s earlier “CAN3” wording still needs physical-label confirmation. USB now enumerates the same serial3a0044001651333038373636 as RetroPilot Chimera bbaa:ddcc; the last read firmware was de193215, with mailbox16/health43. The standalone reader pins identity/version and decodes CAN into modern Cereal, but managed lifecycle/health/ignition and MCU safety remain unfinished. Yesterday492/492 genuine game samples passed software replay, while117 serial-submitted game samples produced0 physical Chimera frames. USB-only power, removed Waveshare resistor, actual termination/rails/bitrate/ACK remain unresolved. The original nightly was restored after an October candidate failed to boot; watchdog-off SYS_CFG writes passed full-block readback, but signal writes/watchdog-on behavior remain unqualified. The active safety header is software-tested and has no production profile or installed-Chimera enforcement. Next qualify physical receive, then managed passive integration.

**Dated correction:** Earlier silent-mode lead is incomplete: can.h declares can_silent=0xFF, but main.c startup calls llcan_set_speed for all three controllers with silent=false. The mask is used in reinitialization paths. Neither fact establishes installed nightly state or the zero-frame cause. The old hardware README’s empty-config wording predates the documented successful SYS_CFG recovery; last verified recovery used watchdog off, not a new configuration read today.

**Implemented versus proposed:** Knowledge recovery and notebook update only. This request resumes Chimera discussion/receive investigation; firmware changes, relays and physical actuation remain outside this increment. Current USB enumeration is fresh; November4 traffic/results and October recovery are historical. No USB handle opened, CAN send/read test, runtime source change, flash, push or automatic update.

**Evidence/source pin:** Parent9376a7f3794b34e036884f527e458bab881c7bd5; child150f937198ceab43c43b39f94b9bdea63fcb633c. Ocelot reference HEADd87892fa25ef2a2474110b97bfb5245ee818b534 has pre-existing dirty source; selected byte hashes are in student Ai/Evidence/chimera-teacher-review-20261105.json. Teacher Chimera transport note, October4isolated-recovery session and November4BeamNG receive/shutdown reports; current source main.c1134–1151/can.h46,162 and receive adapter reviewed. Official Chimera wiki and TI SLAAET4A sections5.1/5.3 checked November5. Existing REA symbol/disassembly evidence is historical, not analysis of the installed nightly; no new REA run needed for source/documentation review. Source-driven,documentation and Git skills used. Notebook/whitespace checks recorded in dated session/ledger; no new runtime qualification. Upstream hold remains; the inbox predates November5master932ff06d and the already-discussed low-speed curvature change.

## QA-20261105-07 — What is rednose_repo?

**Date:** November 5, 2026 UTC.

**Owner question (faithful paraphrase):** rednose_repo @28d4a7f https://github.com/commaai/rednose/tree/28d4a7f69e80e1c3e0d24ca0733d7daeaeade3d0 wat is this

**Answer:** Keep rednose_repo. It is Sunnypilot's mathematical estimation library, using Kalman filters to combine noisy readings into steadier estimates. The pose filter combines IMU readings and camera motion estimates for orientation, velocity, rotation and acceleration estimates. The car filter helps estimate steering ratio/offset and vehicle response from vehicle data. Radxa needs this software too. @28d4a7f is the pinned external submodule version. Transporting our BeamNG IMU data does not by itself integrate it into these filters.

**Implemented/evidence:** Source explanation only; no update/deletion, code change, push or runtime test. Parent4d6b4c87eee71150c76c5c1684c9071d39d631de. Local rednose, parent gitlink and GitHub match28d4a7f69e80e1c3e0d24ca0733d7daeaeade3d0. Inspected README, SConstruct build/rednose_filter tool and pyproject editable dependency; locationd/SConscript generates pose/car filters; models/pose_kf.py and car_kf.py import Rednose; locationd.py and paramsd.py use those estimators.

**Limits:** This is required dependency/source evidence, not a new Radxa sensor-fusion test or a measured steering calibration. BeamNG IMU provider/localization integration remains unfinished. Git/documentation skills and source-first routing reused; no REA artifact question or runtime claim. Upstream updates stay paused.

## QA-20261105-06 — What is msgq_repo?

**Date:** November 5, 2026 UTC.

**Owner question (original):** msgq_repo @ e7396e7 https://github.com/sunnypilot/msgq/tree/e7396e76dadbb49e374d4b664ff6bbb43a39bcb0 wat is this foder

**Answer:** Keep msgq_repo. It provides Sunnypilot's internal message delivery between programs, including vehicle-state/model messages. Its VisionIPC component transfers camera frames between camera, model and display processes. Cereal defines message structures; msgq provides transport. It is needed on Radxa as well. The GitHub @e7396e7 label is the exact external submodule version pinned by this project, not an extra backup.

**Implemented versus proposed:** Explanation/source inspection only. No msgq update, removal, code edit, push or runtime/hardware action.

**Evidence/source pin:** Parent3a4e97135fa2e80c1e273ba7f6bb0f15f1cff5e1; msgq gitlink, local checkout and GitHub all match e7396e76dadbb49e374d4b664ff6bbb43a39bcb0. Checked msgq README/SConscript/package exports, root .gitmodules and pyproject editable dependency; SConstruct includes/builds msgq; cereal/messaging imports it; webcam/camerad.py uses VisionIpcServer; modeld.py uses VisionIpcClient.

**Limits:** Source dependency review, not new full build/runtime testing or proof of the complete camera/model/BeamNG integration. No REA binary question needed; Git/documentation and source-first workflow reused. Keep upstream updates paused and continue owner-selected folder explanations.

## QA-20261105-05 — What every docs file does and which to keep

**Date:** November 5, 2026 UTC.

**Owner question (original):** https://github.com/Deggory/radxa-pilot/tree/radxa/q8b/docs tell me wat to keep ,wat eacg file do

**Answer:** Keep our README/RETROPILOT/GITHUB_RADXA guides, safety/limitations/integration references, AI/contribution policies, car-port/log/replay and safety-debugging guides. CARS.md is an optional generated supported-car catalogue. Comma-device connection and speed-color tutorials, upstream feedback/roadmap, the empty architecture page and website-only files are optional/removal candidates for Radxa-only docs. The safety concepts page links to SAFETY.md. Keep website logo/favicon with the website, star/video icons with CARS.md and three-back.svg with the comma connection guide. Full29entry explanation is saved in the existing cleanup topic/inventory.

**Implemented versus proposed:** Inspected source and dependencies, provided per-file recommendations; no docs deletion or content edit, no push. Remote Radxa matches local sourcec93bd4197e3b0a45249be12638fb410f7e4474f1.29tracked paths,390999logical bytes following the safety symlink. Removal choices remain proposed; nothing from the docs folder was removed by this question.

**Evidence/limits:** Student Ai/Evidence/docs-cleanup-review-20261105.json and Ai/Knowledge/REPOSITORY_CLEANUP.md. tools/op.sh, serve.py/template.html, docs/repo-maintenance workflows and car-doc generator checked for consumers. Not a full website implementation/security or whole-project runtime dependency audit. Older RETROPILOT sections need status refresh; inherited feature descriptions are not Radxa capability proof. No runtime test required for this read-only review and notebook update. Upstream updates stay paused.

## QA-20261105-04 — Remove JetBrains folders locally and on GitHub Q8B

**Date:** November 5, 2026 UTC.

**Owner request (original):** Removing `.idea` and `.run` saves only about **6 KB**. from our and github also in q8b

**Answer:** Removed .idea and .run from our local Sunnypilot project and published the deletion to GitHub radxa/q8b. Six editor-settings files removed,6251logical bytes. .github and .vscode stay intact. master and the RetroPilot support branch were unchanged.

**Implemented/evidence:** Cleanup commit52afd7a3bc64634a6fd1334f420f9a0ecdbc10d0; normal dry-run/actual push passed. GitHub REST and git ls-remote independently verify Radxa52afd7a3, master932ff06d and support150f9371. Folder absence, authorized deletion list, retained .github/.vscode hashes and whitespace pass. Student Ai/Evidence/editor-folder-removal-20261105.json records the actual result. Three previously local documentation commits also published in the fast-forward, as disclosed during work.

**Correction/limits:** Supersedes QA-20261105-03's proposed-only cleanup status: deletion is now complete. No functional source, model, DBC, safety, firmware or runtime setting changed. No runtime tests needed for these six editor-config deletions. Historical commits retain the original files; master retains official source. No history rewrite or automatic-update resume. Current closeout documentation follows the deletion commit.

## QA-20261105-03 — Explain development folders before minimizing the project

**Date:** November 5, 2026 UTC.

**Owner question/request (original):** see i want to minimise the folder ,delete wat is not needed ,si i want toknw wat is the puspose of these folder or file one by one.  .github , .idea ,.run ,.vscode

**Answer:** These are development/GitHub settings. .github holds automated test/build/release/documentation workflows and issue templates; keep for future GitHub maintenance, though it is not needed for local driving runtime. .idea stores JetBrains/CLion build-tool settings; .run stores JetBrains debug/release and big/small UI run shortcuts. Those two are removable candidates for a VS Code-only setup. .vscode has the VS Code formatting/search settings, recommended extensions and debugging shortcuts; keep because this is the owner's editor. All four total171350logical bytes (about167KiB); .idea+.run total6251bytes (about6KiB).

**Implemented versus proposed:** Inspected existing files and release exclusions; saved factual inventory and recommendations. No folder deletion/move/hiding, editor-config edit, source change or push. Current request is handled as explanation first; deletion candidates are recommendations, not completed cleanup.

**Evidence/source pin:** Projecte9275765d9eb8bc2670b1f453589213c353fe28e/child150f937198ceab43c43b39f94b9bdea63fcb633c. Student Ai/Evidence/editor-folder-audit-20261105.json records file hashes/sizes; .idea/customTargets.xml, .idea/tools/External Tools.xml, four .run/*.xml, .vscode/{settings,extensions,launch}.json and selected .github workflows inspected. tools/release/release_files.py already excludes .idea/.run/.github/workflows from its stripped file selection.

**Limits/next:** This is not a full repository pruning or deployment dependency audit. No runtime test or performance benefit claimed. Do not remove other code directories based on their names. Continue explaining the owner's next selected folders; Chimera diagnostics remain a separate pending task. Upstream updates stay paused.

## QA-20261105-02 — Compare Radxa against master on GitHub

**Date:** November 5, 2026 UTC.

**Owner question (faithful paraphrase):** GitHub says master is3commits ahead and113behind radxa/q8b. Shouldn't that comparison appear on q8b against master?

**Answer:** Yes. master is now the default branch. When viewing radxa/q8b, GitHub compares against master and shows113commits ahead and3behind. Previously radxa/q8b was the default, so viewing master showed the reverse. No branch code was merged or changed.

**Implemented/evidence:** Changed only the default-branch setting using gh repo edit Deggory/radxa-pilot --default-branch master. Exit0 and independent GitHub repository readback verified master. Compare base master/head radxa/q8b returned ahead113/behind3. Remote tips remain master932ff06d9316e4351d6b6b9f1dd422d5b639badf, Radxaf193a3cbaa0c5abcad971a34e7b754929ba0e907, support150f937198ceab43c43b39f94b9bdea63fcb633c. See student Reports/github-master-sync-20261105/default-branch.json.

**Correction/limits:** Supersedes the earlier November5answer that the default is radxa/q8b. Counts reflect commit identities; two upstream changes already have separate cherry-picked commits67876efc/a009818b in Radxa, so3behind does not mean all three features are absent. Latest modeld_v2 fix932ff06d remains unapplied to Radxa. Automatic updates remain paused; local notebook commits are not pushed. No runtime/hardware test was needed for repository metadata.

## QA-20261105-01 — Keep GitHub master equal to official Sunnypilot

**Date:** November 5, 2026 UTC.

**Owner question/request (original):** see can we make the master in github same as real sunnypilot

**Answer:** Done: the master branch in Deggory/radxa-pilot now matches official Sunnypilot exactly at932ff06d9316e4351d6b6b9f1dd422d5b639badf. Our camera, Thneed and RetroPilot work remains on radxa/q8b. Automatic updates are still paused. GitHub still opens the Radxa branch by default; select master to see the official source.

**Implemented versus proposed:** Implemented a normal fast-forward of GitHub master only, from8cf6ff9a. GitHub compare, local ancestry, push dry-run, actual push and independent readbacks passed. Remote Radxa branch remainsf193a3cbaa0c5abcad971a34e7b754929ba0e907; support branch remains150f937198ceab43c43b39f94b9bdea63fcb633c. Documentation checkpoint is local only.

**Evidence/source pin:** https://github.com/sunnypilot/sunnypilot/commit/932ff06d9316e4351d6b6b9f1dd422d5b639badf and the dated github-master-sync-20261105 report/receipt in the student notebook. This corrects the historical November4master8cf6ff9a status for today's GitHub branch only.

**Limits/next step:** New upstream commit fixes low-speed modeld_v2 curvature; it has not been integrated or runtime-tested on Radxa. No camera/model/DBC/firmware/hardware change. Future updates and Radxa integration still require owner approval. Continue Chimera receive diagnostics when the owner resumes that work.

# New owner Q&A after the two-day backfill — 2026-11-04

## QA-20261104-08 — BeamNG shared-CAN telemetry

**Owner question/request (original):** like we discused before will be using beam ng to usb to can ,which chimera will read ,so i want u to work on beamng on pc ,were it will be able to send steering angle ,speed ,imu ,brake ,cruise control if any ,see our current dbc ,so the beamng should use wat is there in our dbc ,if some thing is not there add it to our dbc ,teacher please help use agnet skill  edit the beamng file in pc and radxa accordinly

**Answer/status at this increment:** Implemented and deployed read-only PC telemetry/gateway,RP-SIM-1 canonical additions,independent Radxa decoder/monitor and explicit passive simulator profile. Steering,speed,IMU,pedals,wheels,gear and optional actual cruise status have defined availability/units. Existing20message layouts remain unchanged.16focused software checks and existing regressions pass; the deployed PC synthetic fixture decodes on Radxa. Live game/CAN acceptance is blocked by the PC graphics driver; no actuator output or localization fusion enabled.

## QA-20261104-09 — Waveshare connection clarification

**Owner reply (original):** yes waveshare is connected

**Answer/status:** Confirmed on the PC as CH3401a86:7523,ttyUSB0 and its by-id alias. Software is prepared for that Linux serial-framed adapter. Enumeration and synthetic/PTY tests are not electrical CAN delivery proof; no physical CAN transmission performed at this checkpoint.

## QA-20261104-10 — Diagnose and repair BeamNG graphics

**Owner question/request (original):** can see wat was the error ,can u repair it ,then finsifh our can file ,till last week beamng was working

**Answer/status:** BeamNG reports no usable Vulkan GPU; nvidia-smi fails because current kernel7.0.0-38has no NVIDIA module. Only31has a module, and installed next kernel42also lacks one. Prepared/reviewed Ubuntu595-open module/library repair for38and42; owner authenticated in the PC terminal and package downloads started. Driver/game success is not yet verified. No automatic PC restart. CAN source work is saved while live tests wait for graphics recovery.

## QA-20261104-11 — Local repair authentication

**Owner reply (original):** password given

**Answer/status:** Confirmed the root repair log started; 382MB NVIDIA package downloads are in progress. Authentication happened locally; no secret was requested or retained in chat. Next verify installation,module versions,nvidia-smi,Vulkan and genuine game telemetry.

**Evidence for this increment:** [source/test/runtime checkpoint](Reports/beamng-can-20261104/README.md). Source child150f9371; parent base4709073d7. Historical backfill and unresolved items below are unchanged. Append completion/corrections after repair and live validation.

## QA-20261104-12 — CAN adapter access authentication

**Owner reply (original):** i givenn password

**Answer/status:** Fresh PC SSH login confirms pc is now in dialout and can open Waveshare. A bounded synthetic telemetry test then sent20samples via the physical adapter; Chimera USB reads succeeded but reported0CAN frames. This proves adapter access and attempted wire transmission, not end-to-end CAN delivery. Asked whether CAN-H/L/signal-ground are actually wired to Chimera CAN2; no bitrate/firmware/configuration changes made. NVIDIA downloads still in progress.

## QA-20261104-13 — Chimera port clarification

**Owner reply (original):** connected to can 3 of chimera

**Answer/status:** Recorded as supplied. Saved source maps the third MCU controller CAN3 to softwarebus2/connectorCAN2; actual board label is not independently verified. The raw reader monitored every bus and received0frames, so a parser bus filter alone does not explain it. Power, termination and ACK participation remain unresolved.

## QA-20261104-14 — Resistor change

**Owner reply (original):** i removed the resisitro see now

**Answer/status:** Repeated the bounded20sample telemetry attempt after this physical change; Waveshare serial writes completed and Chimera again received0frames. Saved before/after captures separately. Asked which end's resistor was removed and whether external power is present; neither fact can be inferred from the zero result. NVIDIA packages have finished downloading and are installing.

## QA-20261104-15 — Physical wiring state

**Owner reply (original):** waveshare resitr ,chimea is powered by usb only

**Answer/status:** Recorded Waveshare resistor removed and USB-only Chimera power. Both before/after20sample attempts received0CAN frames. This does not prove powered transceiver rails, correct total termination, active bitrate or an ACK participant. No external power instruction or firmware change was issued without resolving these facts. PC GPU repair meanwhile passed: GTX1650/595.99.02, current38/next42modules, clean dpkg audit and successful BeamNG Vulkan startup; no reboot.

### Completion update for QA-20261104-08/10/11 — 2026-11-04

The original GPU repair finished successfully without reboot: GTX1650/595.99.02, matching modules for kernels38/42, clean package audit, and BeamNG running on NVIDIA Vulkan. All1480genuine game samples in a42s capture decoded on Radxa after file transfer; an additional12s capture had0gaps over150ms. Steering/speed/IMU/pedals/wheels/gear/optional cruise are present; generic cruise buttons unavailable. This proves real game generation/encoding/decoding, not physical CAN delivery: both bounded Waveshare/Chimera attempts still received0frames. Teacher/student retain USB-only Chimera power, Waveshare resistor removed and source-only silent-mode lead as unresolved electrical/firmware facts.

### Final answer update for this BeamNG/repair request

NVIDIA/BeamNG is repaired without reboot. CAN files and shared DBC extension are complete;17new focused tests and existing regressions pass. Real running-game492/492samples produced valid passive Sunnypilot car state in replay. Steering/speed/IMU/pedals/wheels/gear/cruise status are available; buttons and IMU localization remain unqualified/unavailable as documented. A genuine117sample serial-CAN attempt still received0Chimera frames. The remaining next step is electrical/ACK/bitrate qualification with the recorded USB-only power/resistor state, not a claim the entire CAN chain works. Source implementation parent880a0adb/child150f9371 saved locally; no push.


## QA-20261104-16 — Additional requirements and opening the Waveshare sender

**Owner question/request (original):** for sunnypilot to work wat are the things neeeded ,steering angle, speed, IMU, pedals, wheels and available cruise status. other than these ,and can u open beamng folder where it send waveshare can data

**Answer:** For this BeamNG setup, additionally need gear/ignition readiness (raw gear index is already transported but Drive/Reverse/Park mapping is pending), an explicit engage/cancel input (current cruise status is not button presses), driver override and actuator-ready/fault feedback appropriate to the selected control method, calibrated vehicle/steering parameters, aligned road-camera/model and simulator IMU integration, reliable timely CAN with enforced safety/fault shutdown, and a return path mapping final Sunnypilot CAN commands to game steering/throttle/brake. Real-vehicle doors/seatbelts/parking-brake conditions apply where appropriate; this does not require inventing simulator signals or bypassing checks. Radar is not mandatory for this current radarUnavailable simulator profile. Current runtime remains noOutput/dashcamOnly and live controller TX is empty; previous physical CAN attempt received0frames. No new CAN test or activation this turn.

**Action/evidence:** PC10.43.0.216 is reachable again using the pinned prior host key. PC desktop gio open returned0 for /home/pc/beamng-q8b/retropilot-can/pc; gateway.py exists. Radxa code --reuse-window --goto opened openpilot/tools/sim/beamng/pc/gateway.py:234; xdg-open for its containing folder returned0. Lua mod reads game state and sends loopback UDP49160; gateway.py uses the shared DBC to encode and write Waveshare serial CAN telemetry. Also completed the previously pending PC README copy; no executable or firmware change.

**Scope:** Source/read-only explanation and folder opening, using project4cc6d67195c20f1edf19a38d703c58ffff6418b0 and child150f937198ceab43c43b39f94b9bdea63fcb633c. No new runtime/safety/transport success is claimed.


## QA-20261104-17 — What the PC sends over CAN

**Owner question (original):** wat all data does pc send through can bus to chimera

**Answer:** With physical TX explicitly enabled, gateway.py sends12CAN frames per sample: measured steering angle and unsigned steering-rate magnitude (0x050); ignition,RPM if available,and driver-brake pressed derived from input>0.05(0x075); speed magnitude in centi-km/h(0x076); cruise button frame0x100 currently zero/unavailable; XYZ acceleration0x702; XYZ angular velocity0x703; four independent wheel-speed magnitudes0x704; driver accelerator input,driver brake input,applied brake,raw gear index,ignition and validity flags0x705; available/enabled/target game-cruise status0x706. Begin0x700/clock0x701/end0x707 add protocol/session/sample metadata,simulation milliseconds,validity flags; each frame has counter/CRC. Nominal maximum50updates/s,not a guaranteed measured rate.

wall_time is used on the PC to reject old UDP samples and is NOT transmitted on CAN; sim_time is transmitted in milliseconds. The full PC session/sequence/valid fields are mapped into bounded CAN metadata rather than copied verbatim. Missing optional fields are explicitly unavailable. Gear is not yet mapped to a complete P/R/N/D selector; IMU axes remain game-frame/unqualified for device localization. Generic cruise button presses are unavailable. Current gateway carries telemetry; command return remains unfinished. Last physical wire test received0frames, so outgoing definitions/serial submission are distinct from proven Chimera reception.

**Evidence/scope:** Read current gateway.py Encoder.encode,game Lua producer,shared CAN_CONTRACT.md and prior active-game receipt at parenta27c269c097c3937fc7877d491877de509e1272a / child150f937198ceab43c43b39f94b9bdea63fcb633c. No executable/DBC/device change, CAN transmission, upstream update, or new runtime test this turn.


## QA-20261104-18 — Is our DBC updated for this data?

**Owner question (original):** so is our dbc updated with this data

**Answer:** Yes. Canonical retropilot/dbc/ocelot_controls.dbc, Sunnypilot packaged copy and deployed PC pc/ocelot_controls.dbc all match RP-SIM-1/SHA256b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67. Count28messages:20original unchanged plus8sim additions. Existing angle/speed/RPM/ignition definitions reused; new IMU,wheels,separate pedals/gear,actual cruise status and sample/time/validity metadata cover the outgoing telemetry. wall_time is intentionally PC-local; button definitions exist but the current game producer marks presses unavailable. DBC coverage does not assert physical reception; last0-frame result remains historical.

**Actual verification:** Current local byte hashes and28BO_ count; original reference byte-prefix assertion; fresh pinned-host SSH sha256sum of deployed PC DBC. Source parent7f924e81add86045442a3d2562b97ea8d24e9f88/child150f937198ceab43c43b39f94b9bdea63fcb633c. No DBC/code/device change or CAN transmission.


## QA-20261104-19 — Canonical DBC meaning and opendbc changes

**Owner question (original):** Canonical RetroPilot DBC wat it means , and i saw u have updated opendbc folder wat u did

**Answer:** Canonical means the owner-selected master/reference copy at retropilot/dbc/ocelot_controls.dbc; Sunnypilot and PC carry matching working copies so all projects use the same IDs,bit layouts,scales and meaning. RP-SIM-1 is our local versioned extension; this does not claim upstream publication. opendbc is Sunnypilot's CAN/vehicle-support library. Latest BeamNG child commit150f9371 changed9files: dbc/ocelot_controls.dbc(add8sim messages); car/retropilot/simulation.py(new coherent/CRC/counter/session/time/availability decoder); carstate.py(map readings into Sunny state); values.py and interface.py(explicit passive RETROPILOT_BEAMNG and simulator speed units); car/car_helpers.py(skip OEM firmware/VIN probes for explicit sim selection); car/torque_data/override.toml(passive required placeholder,not a measured tune); README.md and SOURCES.json(documentation/provenance). This describes the latest BeamNG increment, not all historical port work. Profile stays noOutput,dashcamOnly,carNotReady and controller runtime TX empty.

**Evidence:** Actual git show --stat and selected diff671f8c4..150f9371, current interface/controller docs, owner CAN_DBC_POLICY. Parent basea644f949a95906adce28493048c0c940a7979eed; child150f937198ceab43c43b39f94b9bdea63fcb633c. Documentation/source-only explanation; no source/DBC/firmware/runtime/upstream change or new hardware test.


## QA-20261104-20 — What the updated Ocelot DBC contains

**Owner question (original):** can u tell wat all now new coelot hvae

**Interpretation/answer:** In the current conversation this refers to updated ocelot_controls.dbc, not newly flashed Ocelot/Chimera firmware. It contains28message definitions:20originals plus8local RP-SIM-1 additions. Original coverage: measured angle/rate,speed,ignition/RPM/brake-pressed,cruise buttons/ADC; command/status pairs for brake actuator,steering actuator,gas pedal interceptor,iBooster,SSC stepper,steering interceptor,throttle actuator,and historical RelayCore definitions. Relay control remains outside this project scope. New0x700..0x707:sample begin,simulation clock,XYZacceleration,XYZgyro,fourwheel speeds,driver accelerator/driver brake/applied brake/raw gear/ignition/validity,actual cruise available/enabled/target,coherent sample end. Missing optional values are marked unavailable; current generic button presses unavailable,gear selector mapping pending. Hardware operation requires matching firmware/wiring; these definitions do not establish working physical control. Current gateway emits12telemetry frames, not all28definitions.

**Evidence:** Direct BO_/SG_ inventory, canonical SHA256b4079670b8118fe63c6a7710ca1158afaabfec7df881ef902e43d70d70a36b67, packaged byte equality,28message count and preserved20message original-prefix assertion. Source parent9e3b896fb9a6f564acbce42aef3845994cad5eea / child150f937198ceab43c43b39f94b9bdea63fcb633c. Documentation/source-only; no DBC/code/firmware/runtime change or hardware test.


## QA-20261104-21 — Audit, publish and ordered shutdown

**Owner request (original):** audit wat we did ,tom onwards we will work on chimera ,update the githu page ,and close pc ,then vscode and this radxa

**Accepted scope/status:** Audit/save both memories, publish verified parent and child to Deggory/radxa-pilot with visible Radxa status and preserved master, prepare November5Chimera receive-diagnostics handoff, then power off PC first and close VS Code/Radxa normally last. Fresh165tests and source/DBC checks pass. Last physical CAN0frames remains unresolved. Publication/physical shutdown are not yet claimed at preparation time; append actual readbacks. No flash,relays or actuation.

**Evidence:** Ai/Reports/beamng-shutdown-audit-20261104 and the dated audit-publication-shutdown session.

### QA21 publication completion update

Audit165fresh tests passed. Updated Deggory/radxa-pilot front page and both source branches; fresh source downloads match, original master preserved, Actions disabled. Teacher/student handoff for November5Chimera saved. Final action is normal PC shutdown first, then VS Code/Radxa cleanup and poweroff; actual shutdown request receipt is central, not a premature claim of physical completion.

---

# Owner Q&A recovered for November 3–4, 2026

This dated backfill expands the earlier seven-entry summary below. It covers all
**62 owner turns found in the retained local conversations**: **47 on November 3**
and **15 on November 4**, through the 18:38:08 UTC request, including clarification
replies and requests for action. The 58 original completed answers are preserved
verbatim in [the exact-text archive and source manifest](Evidence/owner-qa-20261103-04.json).
Three requests continued after an owner reply; their entries link to the answer.
The current request has a separately labelled new closeout, not an invented old answer.

Below, answers are faithful plain-English summaries. Questions under 500 characters
are quoted; long pasted checklists are labelled paraphrases with full originals in
the archive. Historical answers describe the state **at that time**. Later changes
are called out separately; old commit IDs remain historical and can be resolved
with the commit-topic map. Existing earlier Q&A and unanswered questions are preserved.

Coverage excludes deleted/unsent chats, other devices/accounts and later turns.
Scanning 247 local session files found two relevant owner conversations. Only visible
owner/final-answer text was retained, without raw tools or reasoning. All recovered
questions in this window concern Sunnypilot or its supporting references; copying
Ocelot/dzid reference findings here does not establish a tested Sunnypilot integration.

Current source: project before this backfill `762842752843e204cc854c4c49728582e5d3ea40`,
opendbc `671f8c450fc74f5b8b90b2ee53124394108651ce`.
Live RetroPilot remains `noOutput`; Chimera is held and relays are excluded.
Upstream updates remain paused. This backfill is local documentation, with no push.

## Find a question

| Date (UTC) | Record | Topic |
| --- | --- | --- |
| 2026-11-03 06:56 | [CHAT-20261103-001](#chat-20261103-001) | BeamNG bridge audit in simple English |
| 2026-11-03 07:42 | [CHAT-20261103-002](#chat-20261103-002) | Webcam, Waveshare, Chimera and later bench actuators |
| 2026-11-03 09:50 | [CHAT-20261103-003](#chat-20261103-003) | What the hidden project folders do |
| 2026-11-03 09:59 | [CHAT-20261103-004](#chat-20261103-004) | Do we need docs and comma-specific files? |
| 2026-11-03 10:07 | [CHAT-20261103-005](#chat-20261103-005) | What Sunnypilot needs from the BeamNG PC |
| 2026-11-03 13:50 | [CHAT-20261103-006](#chat-20261103-006) | Port RetroPilot using Chimera |
| 2026-11-03 15:06 | [CHAT-20261103-007](#chat-20261103-007) | Modern car-port files checklist |
| 2026-11-03 15:13 | [CHAT-20261103-008](#chat-20261103-008) | Where is fingerprints.py? |
| 2026-11-03 15:16 | [CHAT-20261103-009](#chat-20261103-009) | Is RetroPilot in fingerprints.py? |
| 2026-11-03 15:17 | [CHAT-20261103-010](#chat-20261103-010) | Why no fingerprint? Compare C2 selection |
| 2026-11-03 17:09 | [CHAT-20261103-011](#chat-20261103-011) | Will incoming Chimera CAN detect the car? |
| 2026-11-03 17:13 | [CHAT-20261103-012](#chat-20261103-012) | Why is our controller smaller than C2? Fix it |
| 2026-11-03 17:40 | [CHAT-20261103-013](#chat-20261103-013) | Review the year of C2 work for modern Radxa |
| 2026-11-03 17:42 | [CHAT-20261103-014](#chat-20261103-014) | Target clarification: existing Radxa Q8B |
| 2026-11-03 18:03 | [CHAT-20261103-015](#chat-20261103-015) | Which files changed in the latest adaptation? |
| 2026-11-03 18:28 | [CHAT-20261103-016](#chat-20261103-016) | Explain the port plainly; did we add a DBC? |
| 2026-11-03 18:40 | [CHAT-20261103-017](#chat-20261103-017) | What does simulated testing mean? |
| 2026-11-03 18:43 | [CHAT-20261103-018](#chat-20261103-018) | Are the DBC and car folder enough? What about Panda? |
| 2026-11-03 18:45 | [CHAT-20261103-019](#chat-20261103-019) | Show all the C2 commits from that year |
| 2026-11-03 18:53 | [CHAT-20261103-020](#chat-20261103-020) | What changed in Cereal, opendbc, Panda, selfdrive, third_party and tools? |
| 2026-11-03 19:05 | [CHAT-20261103-021](#chat-20261103-021) | Understand C2 rather than copy its old integration |
| 2026-11-03 19:07 | [CHAT-20261103-022](#chat-20261103-022) | Changes outside RetroPilot and Panda? |
| 2026-11-03 19:12 | [CHAT-20261103-023](#chat-20261103-023) | What do chimera.py and chimera_protocol.py do? |
| 2026-11-03 19:22 | [CHAT-20261103-024](#chat-20261103-024) | Does current Sunnypilot have Cereal? |
| 2026-11-03 19:40 | [CHAT-20261103-025](#chat-20261103-025) | Do we need changes in current Sunnypilot/Cereal? |
| 2026-11-03 19:41 | [CHAT-20261103-026](#chat-20261103-026) | Hold Chimera; do we need Cereal changes? |
| 2026-11-03 19:41 | [CHAT-20261103-027](#chat-20261103-027) | Why did C2 change Cereal? |
| 2026-11-03 19:43 | [CHAT-20261103-028](#chat-20261103-028) | No relays; explain the custom safety mode |
| 2026-11-03 20:07 | [CHAT-20261103-029](#chat-20261103-029) | What safety changes do we need now? |
| 2026-11-03 20:25 | [CHAT-20261103-030](#chat-20261103-030) | Does safety go in opendbc/safety? |
| 2026-11-03 20:25 | [CHAT-20261103-031](#chat-20261103-031) | What safety did he put in Cereal? |
| 2026-11-03 20:26 | [CHAT-20261103-032](#chat-20261103-032) | Check whether current Sunnypilot needs changes |
| 2026-11-03 20:28 | [CHAT-20261103-033](#chat-20261103-033) | Are the identifier and safety rules already done? |
| 2026-11-03 20:30 | [CHAT-20261103-034](#chat-20261103-034) | Teacher, do we need these safety pieces? |
| 2026-11-03 20:58 | [CHAT-20261103-035](#chat-20261103-035) | Do we need the identifier and test file? |
| 2026-11-03 21:00 | [CHAT-20261103-036](#chat-20261103-036) | Fix the missing safety pieces |
| 2026-11-03 21:19 | [CHAT-20261103-037](#chat-20261103-037) | What did retropilot.h and the 21 tests do? |
| 2026-11-03 21:35 | [CHAT-20261103-038](#chat-20261103-038) | Is our retropilot.h the C2 file? |
| 2026-11-03 21:39 | [CHAT-20261103-039](#chat-20261103-039) | What means C2 safety implementation? |
| 2026-11-03 21:53 | [CHAT-20261103-040](#chat-20261103-040) | Why are other safety headers longer? Show the old file |
| 2026-11-03 21:59 | [CHAT-20261103-041](#chat-20261103-041) | Why not fix the missing active checks? |
| 2026-11-03 22:06 | [CHAT-20261103-042](#chat-20261103-042) | Which BeamNG car did the bridge author choose? |
| 2026-11-03 22:22 | [CHAT-20261103-043](#chat-20261103-043) | Why two RetroPilot files in safety/modes? |
| 2026-11-03 22:23 | [CHAT-20261103-044](#chat-20261103-044) | Is modes the Panda safety? |
| 2026-11-03 22:25 | [CHAT-20261103-045](#chat-20261103-045) | Are car/retropilot, DBC and safety modes all that is needed? |
| 2026-11-03 22:26 | [CHAT-20261103-046](#chat-20261103-046) | How does ours differ from C2? |
| 2026-11-03 22:28 | [CHAT-20261103-047](#chat-20261103-047) | Audit, save teacher/student, close VS Code and shut down |
| 2026-11-04 14:22 | [CHAT-20261104-001](#chat-20261104-001) | What is Ocelot in C2? |
| 2026-11-04 14:25 | [CHAT-20261104-002](#chat-20261104-002) | Do we need that DBC? Compare old and current |
| 2026-11-04 14:29 | [CHAT-20261104-003](#chat-20261104-003) | Rename it retropilot.dbc? |
| 2026-11-04 14:32 | [CHAT-20261104-004](#chat-20261104-004) | Required hardware: Chimera, Interceptor Core, Actuator Core |
| 2026-11-04 14:34 | [CHAT-20261104-005](#chat-20261104-005) | Label camera, Thneed and RetroPilot commits |
| 2026-11-04 16:02 | [CHAT-20261104-006](#chat-20261104-006) | Any upstream master updates? Ask before updating |
| 2026-11-04 16:09 | [CHAT-20261104-007](#chat-20261104-007) | Apply only those two; preserve camera, Thneed/model and RetroPilot |
| 2026-11-04 16:20 | [CHAT-20261104-008](#chat-20261104-008) | Create radxa-pilot, preserve master and our branch/commits |
| 2026-11-04 16:34 | [CHAT-20261104-009](#chat-20261104-009) | Publication clarification: public Sunnypilot history |
| 2026-11-04 17:57 | [CHAT-20261104-010](#chat-20261104-010) | All data our DBC can get |
| 2026-11-04 18:12 | [CHAT-20261104-011](#chat-20261104-011) | Does it include dzid stepper control and ZSS angle? |
| 2026-11-04 18:20 | [CHAT-20261104-012](#chat-20261104-012) | Are these analog inputs converted to CAN? |
| 2026-11-04 18:21 | [CHAT-20261104-013](#chat-20261104-013) | Can Sunnypilot read OEM CAN using a second DBC? |
| 2026-11-04 18:33 | [CHAT-20261104-014](#chat-20261104-014) | Are teacher and student saving my questions and answers? |
| 2026-11-04 18:38 | [CHAT-20261104-015](#chat-20261104-015) | Save all questions from today and yesterday |

## CHAT-20261103-001

**Topic:** BeamNG bridge audit in simple English

**Asked (UTC):** 2026-11-03T06:56:22.827Z

**Owner question/request (labelled paraphrase of long pasted text):** BeamNG bridge audit in simple English. Full original in the exact-text archive.

**Answer (summary):** The reference files were intact, but API compatibility, stale-data handling and the camera/network path still needed adaptation. The original curvature-to-steering route did not test our final motor torque controller.

**Status/limits at backfill:** BeamNG proposal at that time; the next request replaced network images with a webcam aimed at the monitor.

**Evidence:** exact archive record `CHAT-20261103-001`, session `01a196e8-3c9c-70f3-ad57-90846ae6d90b`, owner line 13300, final-answer line(s) 13305.

## CHAT-20261103-002

**Topic:** Webcam, Waveshare, Chimera and later bench actuators

**Asked (UTC):** 2026-11-03T07:42:19.786Z

**Owner question/request (labelled paraphrase of long pasted text):** Webcam, Waveshare, Chimera and later bench actuators. Full original in the exact-text archive.

**Answer (summary):** Saved the hardware-in-the-loop design: monitor to Radxa webcam, PC telemetry through Waveshare/CAN/Chimera, and return commands to BeamNG. Split PC/Radxa/shared instructions. The bridge itself and missing wheel-speed/IMU messages were still pending.

**Status/limits at backfill:** Design/documentation, not a working live loop.

**Evidence:** exact archive record `CHAT-20261103-002`, session `01a196e8-3c9c-70f3-ad57-90846ae6d90b`, owner line 13312, final-answer line(s) 13499.

## CHAT-20261103-003

**Topic:** What the hidden project folders do

**Asked (UTC):** 2026-11-03T09:50:26.848Z

**Owner question/request (original):**

> tell me wat are these folder  .github ,.idea .install bauck-uo, .ruff_cahce, ,.run .

**Answer (summary):** .github contains GitHub automation; .idea and .run contain JetBrains settings; .install-backup-20261102 holds five original compiled libraries; .ruff_cache is disposable checking cache. Their contents were left unchanged.

**Status/limits at backfill:** Explanation only; no deletion authorized or performed by that answer.

**Evidence:** exact archive record `CHAT-20261103-003`, session `01a196e8-3c9c-70f3-ad57-90846ae6d90b`, owner line 13506, final-answer line(s) 13544.

## CHAT-20261103-004

**Topic:** Do we need docs and comma-specific files?

**Asked (UTC):** 2026-11-03T09:59:30.991Z

**Owner question/request (original):**

> see docs folder ,do we need it ,see why i am asking is i want to remove all the thing which are not needed for sunnypilot folder  make it simiple ,siince we are working on radxa ,there will be some thing we dont need which belong to comma 4

**Answer (summary):** Recommended retaining car/CAN/safety and development references. The docs were about 440 KB, so removal would not improve model speed. Added a Radxa docs starting page; deleting imported comma hardware code would need dependency checks.

**Status/limits at backfill:** Documentation changed; no source folders deleted.

**Evidence:** exact archive record `CHAT-20261103-004`, session `01a196e8-3c9c-70f3-ad57-90846ae6d90b`, owner line 13551, final-answer line(s) 13631.

## CHAT-20261103-005

**Topic:** What Sunnypilot needs from the BeamNG PC

**Asked (UTC):** 2026-11-03T10:07:10.030Z

**Owner question/request (original):**

> see i have connected the pc with beamng ,lets work on this ,now pc beamng will act as a real car ,wat are the things we need by sunnypilot to make it work

**Answer (summary):** Needs the webcam road view, truthful vehicle and motion data, selected-car parameters, compatible CAN transport, and translated return controls with timeout handling. Proposed receiving and displaying data first. The actual game/car/mods and full loop remained unverified.

**Status/limits at backfill:** Checklist, not live integration acceptance.

**Evidence:** exact archive record `CHAT-20261103-005`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 12, final-answer line(s) 81.

## CHAT-20261103-006

**Topic:** Port RetroPilot using Chimera

**Asked (UTC):** 2026-11-03T13:50:30.883Z

**Owner question/request (original):**

> see in order for can to work we need to port a new car ,we wll be using chimera as panda ,and retropilot as car ,so port retropilot as car ,use agnet skill read Ai teacher

**Answer (summary):** Added the receive-only RETROPILOT_RETROFIT platform, canonical DBC/integrity checks, vehicle parsing, explicit selection and offline command encoders. Reported 53 CAN tests, 22 RetroPilot tests and 1,600 CRC vectors. The live controller sent nothing.

**Status/limits at backfill:** Historical implementation checkpoint; later entries add alias support, adapter and safety software.

**Evidence:** exact archive record `CHAT-20261103-006`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 88, final-answer line(s) 380.

## CHAT-20261103-007

**Topic:** Modern car-port files checklist

**Asked (UTC):** 2026-11-03T15:06:49.561Z

**Owner question/request (labelled paraphrase of long pasted text):** Modern car-port files checklist. Full original in the exact-text archive.

**Answer (summary):** Mapped the checklist to modern opendbc: values/interface/state/DBC were present; controller output was disabled. Automatic identification, a completed safety policy and compiled policy tests were pending at that point.

**Status/limits at backfill:** Historical status: safety software was added later on November 3; live output is still disabled.

**Evidence:** exact archive record `CHAT-20261103-007`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 387, final-answer line(s) 437.

## CHAT-20261103-008

**Topic:** Where is fingerprints.py?

**Asked (UTC):** 2026-11-03T15:13:46.783Z

**Owner question/request (original):**

> `fingerprints.py` werer is this file

**Answer (summary):** Pointed to the shared opendbc/car/fingerprints.py and the Hyundai example. RetroPilot initially had no separate fingerprints.py and required explicit RETROPILOT_RETROFIT selection.

**Status/limits at backfill:** Historical absence; corrected by the later C2-name compatibility change.

**Evidence:** exact archive record `CHAT-20261103-008`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 444, final-answer line(s) 458.

## CHAT-20261103-009

**Topic:** Is RetroPilot in fingerprints.py?

**Asked (UTC):** 2026-11-03T15:16:01.987Z

**Owner question/request (original):**

> is retropilot added to `fingerprints.py`

**Answer (summary):** At that time, no: the platform was registered in car/values.py but had no fingerprint entry; automatic CAN/ECU identification was absent.

**Status/limits at backfill:** Later alias registration does not add automatic identification.

**Evidence:** exact archive record `CHAT-20261103-009`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 465, final-answer line(s) 469.

## CHAT-20261103-010

**Topic:** Why no fingerprint? Compare C2 selection

**Asked (UTC):** 2026-11-03T15:17:57.086Z

**Owner question/request (original):**

> why this is not added ,teacher see retopilot C2 wat he did to port retropilo to c2 comma ,but see wat to do in new comma

**Answer (summary):** C2 forced RETROPILOT RETROFIT and skipped firmware queries; its placeholder table did not identify a real car. Added the modern fingerprints.py alias/migration so old and new names select the port. Kept the automatic database empty pending measured evidence.

**Status/limits at backfill:** Alias support implemented and tested; automatic identification remains unqualified.

**Evidence:** exact archive record `CHAT-20261103-010`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 476, final-answer line(s) 594.

## CHAT-20261103-011

**Topic:** Will incoming Chimera CAN detect the car?

**Asked (UTC):** 2026-11-03T17:09:26.561Z

**Owner question/request (original):**

> so whn the chimera get the can message ,will the sunnypilot detect teh car ,after i fixed the chimera

**Answer (summary):** CAN arriving alone will not automatically identify RetroPilot. Explicit selection plus valid base messages on host bus 2 lets the interface parse data. Chimera transport, speed scaling and disabled controller output remained barriers to control.

**Status/limits at backfill:** Host bus 2 is the source convention, not proof of physical wiring.

**Evidence:** exact archive record `CHAT-20261103-011`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 601, final-answer line(s) 605.

## CHAT-20261103-012

**Topic:** Why is our controller smaller than C2? Fix it

**Asked (UTC):** 2026-11-03T17:13:45.632Z

**Owner question/request (original):**

> [https://github.com/RetroPilot/retropilot/tree/c2/selfdrive/car/retropilot](https://github.com/RetroPilot/retropilot/tree/c2/selfdrive/car/retropilot)   if u see the code here and ours is very small ,this was made in C2 ,now we are in new so fix it

**Answer (summary):** Added adapted steering limits, pedal calculations, counters/scheduling, legacy relay command calculations and offline replay. Reported 44 RetroPilot, 53 CAN and 303 broader car tests. Live output stayed disabled.

**Status/limits at backfill:** Historical offline code; the owner subsequently excluded relays. No live relay use or calibrated vehicle tune follows from this answer.

**Evidence:** exact archive record `CHAT-20261103-012`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 612, final-answer line(s) 802.

## CHAT-20261103-013

**Topic:** Review the year of C2 work for modern Radxa

**Asked (UTC):** 2026-11-03T17:40:19.943Z

**Owner question/request (original):**

> see this was done on c2 of openpilot ,[https://github.com/RetroPilot/retropilot/tree/c2](https://github.com/RetroPilot/retropilot/tree/c2) ,see all thethings he did in one year ,but now we have c4 ,so use rea and sgnet skill to adapte retropilot to work on our latest sunnypilot ,fous on wat he did one one year

**Answer (summary):** Work continued after the owner clarified the target as the existing Radxa Q8B. The completed answer is attached to the next clarification record.

**Status/limits at backfill:** No separate final answer between this request and the clarification; follow the continuation link in the archive.

**Answer continuation:** [CHAT-20261103-014](#chat-20261103-014).

**Evidence:** exact archive record `CHAT-20261103-013`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 809; continuation/new-closeout status above.

## CHAT-20261103-014

**Topic:** Target clarification: existing Radxa Q8B

**Asked (UTC):** 2026-11-03T17:42:51.128Z

**Clarification asked by agent (original):** When you say C4, is the target our existing Radxa Q8B running modern Sunnypilot, or a physical comma 4? I’m continuing with the Radxa project and Chimera USB architecture saved in teacher Ai.

**Owner reply (original):** Existing Radxa Q8B project

**Answer (summary):** Owner selected the existing Q8B project. The completed response reported review of 35 C2 commits and three submodule histories, a receive-only Chimera adapter, correct steering STATE=1 handling, and firmware-layout REA evidence. Reported 15 adapter, 45 RetroPilot, 53 CAN and 303 broader car tests.

**Status/limits at backfill:** Source/artifact and CPU-test evidence; actual Chimera integration, health/ignition and calibration remained unfinished.

**Continues:** [CHAT-20261103-013](#chat-20261103-013).

**Evidence:** exact archive record `CHAT-20261103-014`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 925, final-answer line(s) 1129.

## CHAT-20261103-015

**Topic:** Which files changed in the latest adaptation?

**Asked (UTC):** 2026-11-03T18:03:27.507Z

**Owner question/request (original):**

> see i waant to knw wat are the thing file u chnaged

**Answer (summary):** Latest code changes were new chimera.py and chimera_protocol.py, plus carstate.py and values.py for angle validity. Four test files, reports, documentation, notebooks and the child revision were also updated. Other open car files came from earlier increments.

**Status/limits at backfill:** Scope of that adaptation, not a complete all-time changed-file inventory.

**Evidence:** exact archive record `CHAT-20261103-015`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1139, final-answer line(s) 1159.

## CHAT-20261103-016

**Topic:** Explain the port plainly; did we add a DBC?

**Asked (UTC):** 2026-11-03T18:28:29.889Z

**Owner question/request (original):**

> see i have no idea in coding i wam using vibe coding only ,so tell me plain english wat u did to port retropilot to work ,have u added dbc file also

**Answer (summary):** Yes: packaged the canonical ocelot_controls.dbc. Added the modern vehicle definition, CAN readers, offline command calculations and a standalone Chimera USB reader, with fake-input tests. The complete BeamNG/Chimera/control loop had not been demonstrated.

**Status/limits at backfill:** Software foundation; active steering, accelerator and brake output remain disabled.

**Evidence:** exact archive record `CHAT-20261103-016`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1166, final-answer line(s) 1186.

## CHAT-20261103-017

**Topic:** What does simulated testing mean?

**Asked (UTC):** 2026-11-03T18:40:54.491Z

**Owner question/request (original):**

> 1. **Added message readers** to turn incoming CAN messages into information Sunnypilot understands.
> 2. **Added command calculations** for steering, accelerator and brakes, currently used in simulated tests.
> 3. **Tested those pieces together with simulated inputs**, including missing messages, bad data and disconnection.
>
> &#x20;simulated wat u men by it

**Answer (summary):** Software generated pretend CAN data and checked parsing/calculations, damaged or missing messages and fake USB disconnects. These tests did not use a running BeamNG game or a real Chimera connection.

**Status/limits at backfill:** Passing test examples are not hardware or full-system acceptance.

**Evidence:** exact archive record `CHAT-20261103-017`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1193, final-answer line(s) 1198.

## CHAT-20261103-018

**Topic:** Are the DBC and car folder enough? What about Panda?

**Asked (UTC):** 2026-11-03T18:43:28.260Z

**Owner question/request (original):**

> we adeed dbc ,we made retropilot folder and files  is this enough any other files is chnages ,i saw panda also u did soe thing

**Answer (summary):** Also changed shared platform registration, selection/name migration, checksum support and a provisional torque-data entry. Added computer-side pandad adapter files and tests. Panda firmware itself was not modified or flashed.

**Status/limits at backfill:** The provisional entry is not measured tuning. pandad host code and Panda firmware are different.

**Evidence:** exact archive record `CHAT-20261103-018`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1205, final-answer line(s) 1222.

## CHAT-20261103-019

**Topic:** Show all the C2 commits from that year

**Asked (UTC):** 2026-11-03T18:45:59.356Z

**Owner question/request (original):**

> show me all the things c2 did in one year his commit

**Answer (summary):** Saved a 53-commit guide for the reviewed 2025 history: 28 application, 20 CAN/DBC, two Panda and three Cereal commits, spanning February through August. The author's July 16 “op drives” claim is historical, not evidence for our hardware.

**Status/limits at backfill:** The original answer and all commit descriptions/links are retained in the exact-answer archive and the C2 history report.

**Evidence:** exact archive record `CHAT-20261103-019`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1229, final-answer line(s) 1353.

## CHAT-20261103-020

**Topic:** What changed in Cereal, opendbc, Panda, selfdrive, third_party and tools?

**Asked (UTC):** 2026-11-03T18:53:36.654Z

**Owner question/request (original):**

> see wat he did ,cereal ,opendbc,paanda,selfdrive,thirdparty ,tools

**Answer (summary):** Explained schema/safety-mode and relay fields, CAN layouts/integrity, unfinished firmware rules, car/control/engagement changes, old compiler/video fixes and joystick behavior. These describe old architecture; modern Sunnypilot needs only relevant missing functions adapted.

**Status/limits at backfill:** Source comparison, not a requirement to transplant all six areas.

**Evidence:** exact archive record `CHAT-20261103-020`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1360, final-answer line(s) 1396.

## CHAT-20261103-021

**Topic:** Understand C2 rather than copy its old integration

**Asked (UTC):** 2026-11-03T19:05:19.655Z

**Owner question/request (original):**

> see i dont want his intergratin ,since c2 was 5 or 6 odl comma 2 device over the yearss c4 evolved ,see we dont need to add all the things he did ,i want u to understande wat he did ,i dont want to bring c2 to comma 4 or rdxa our goal is to make retorpilot to work on rdxa latest sunny pilot ,why i asked to look to 4 folder s is to understand wat he did

**Answer (summary):** Accepted the correction: the target is RetroPilot on current Sunnypilot/Radxa. Study old CAN/sensors/commands/hardware behavior and implement only current gaps. Folder counts do not define the work.

**Status/limits at backfill:** Owner scope correction; no runtime code changed by this clarification.

**Evidence:** exact archive record `CHAT-20261103-021`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1403, final-answer line(s) 1427.

## CHAT-20261103-022

**Topic:** Changes outside RetroPilot and Panda?

**Asked (UTC):** 2026-11-03T19:07:39.098Z

**Owner question/request (original):**

> so did u make any chnages other than retorpilot and pands

**Answer (summary):** Listed shared checksum, registration, selection, alias, provisional torque entry and packaged DBC changes, plus the standalone pandad reader. Clarified that Panda firmware, Cereal and third-party code had not been changed for the port at that stage.

**Status/limits at backfill:** Historical checkpoint before the later modern opendbc safety changes.

**Evidence:** exact archive record `CHAT-20261103-022`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1434, final-answer line(s) 1458.

## CHAT-20261103-023

**Topic:** What do chimera.py and chimera_protocol.py do?

**Asked (UTC):** 2026-11-03T19:12:58.103Z

**Owner question/request (original):**

> I also added **`chimera.py` and `chimera_protocol.py` under `selfdrive/pandad/`**, plus tests and documentation.
> wat does this do

**Answer (summary):** The first checks USB identity/version and receives CAN/health; the second decodes mailbox and health packets. The car parser interprets the CAN values. It is a separate receive-only tool, not an automatically managed control backend.

**Status/limits at backfill:** Fake USB/packet tests only; actual device operation still needs verification. Chimera work was later held.

**Evidence:** exact archive record `CHAT-20261103-023`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1465, final-answer line(s) 1469.

## CHAT-20261103-024

**Topic:** Does current Sunnypilot have Cereal?

**Asked (UTC):** 2026-11-03T19:22:40.139Z

**Owner question/request (original):**

> `cereal` does this exit in our current sunnypilot

**Answer (summary):** Yes, under openpilot/cereal. It carries messages between processes. Vehicle definitions such as CarState/CarControl are now in opendbc/car/car.capnp; no RetroPilot edit to the Cereal repository was needed.

**Status/limits at backfill:** Modern schema location is distinct from the process messaging library.

**Evidence:** exact archive record `CHAT-20261103-024`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1476, final-answer line(s) 1504.

## CHAT-20261103-025

**Topic:** Do we need changes in current Sunnypilot/Cereal?

**Asked (UTC):** 2026-11-03T19:40:17.284Z

**Owner question/request (original):**

> do we need to chnage in current sunnypilot

**Answer (summary):** Existing Cereal messages suffice for receiving CAN and vehicle data. Managed Chimera startup/health and the full BeamNG loop still need integration. A new schema field is needed only for a requirement the current messages cannot express.

**Status/limits at backfill:** Receive-only-stage answer; later safety-mode identifier work belongs in modern opendbc.

**Evidence:** exact archive record `CHAT-20261103-025`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1511, final-answer line(s) 1515.

## CHAT-20261103-026

**Topic:** Hold Chimera; do we need Cereal changes?

**Asked (UTC):** 2026-11-03T19:41:19.694Z

**Owner question/request (original):**

> lets hold chimera for now ,so do we need change in cereal

**Answer (summary):** Accepted the Chimera hold. Existing Cereal messages were sufficient for the RetroPilot work then implemented.

**Status/limits at backfill:** Hold remains active; this did not say all future active-control work was complete.

**Evidence:** exact archive record `CHAT-20261103-026`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1522, final-answer line(s) 1525.

## CHAT-20261103-027

**Topic:** Why did C2 change Cereal?

**Asked (UTC):** 2026-11-03T19:41:53.799Z

**Owner question/request (original):**

> tell why c2 made chnage\

**Answer (summary):** For three reasons: a RetroPilot safety-mode identifier, relay-control requests, and Ubuntu 24.04 build compatibility. Current vehicle definitions live in modern opendbc, so old edits are not automatically required.

**Status/limits at backfill:** Relay work was excluded by the following owner direction.

**Evidence:** exact archive record `CHAT-20261103-027`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1532, final-answer line(s) 1551.

## CHAT-20261103-028

**Topic:** No relays; explain the custom safety mode

**Asked (UTC):** 2026-11-03T19:43:46.992Z

**Owner question/request (original):**

> i dont wan relay ,**RetroPilot safety mode:** Added the name `retropilot` so his openpilot could request his custom Panda safety mode. this i wnt to knw more

**Answer (summary):** The schema name/number selects board-enforced rules; it does not itself check steering or brakes. C2 used 26, now occupied by Hongqi/FAW. Our interface requests noOutput. Future active control needs matching identifier, rules and firmware enforcement.

**Status/limits at backfill:** Relays excluded. The earlier “no Cereal change” statement was scoped to receive-only operation.

**Evidence:** exact archive record `CHAT-20261103-028`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1558, final-answer line(s) 1600.

## CHAT-20261103-029

**Topic:** What safety changes do we need now?

**Asked (UTC):** 2026-11-03T20:07:21.825Z

**Owner question/request (original):**

> so in our current sunny ,do we need to chnage anything

**Answer (summary):** For a custom active mode: add an unused identifier to car.capnp, implement/register/test the rules in opendbc/safety, and request it only after qualification. The actual board must enforce those rules.

**Status/limits at backfill:** Plan at that point; later code added local ID39 and rules/tests, but the live interface still uses noOutput.

**Evidence:** exact archive record `CHAT-20261103-029`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1607, final-answer line(s) 1611.

## CHAT-20261103-030

**Topic:** Does safety go in opendbc/safety?

**Asked (UTC):** 2026-11-03T20:25:27.647Z

**Owner question/request (original):**

> so u mean we will put here `opendbc/safety/`

**Answer (summary):** Yes: modes/retropilot.h and tests/test_retropilot.py, plus dispatcher and schema registration. At the time of this answer those files had not yet been implemented.

**Status/limits at backfill:** Historical absence, superseded by the later “fix it then” increment.

**Evidence:** exact archive record `CHAT-20261103-030`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1618, final-answer line(s) 1621.

## CHAT-20261103-031

**Topic:** What safety did he put in Cereal?

**Asked (UTC):** 2026-11-03T20:25:56.001Z

**Owner question/request (original):**

> see wat is the safety he did in cereal

**Answer (summary):** Only the selection identifier retropilot @26 in car.capnp. The actual steering/brake checks belonged in Panda's safety_retropilot.h.

**Status/limits at backfill:** Old C2 number only; do not use 26 for the modern port.

**Evidence:** exact archive record `CHAT-20261103-031`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1628, final-answer line(s) 1632.

## CHAT-20261103-032

**Topic:** Check whether current Sunnypilot needs changes

**Asked (UTC):** 2026-11-03T20:26:57.858Z

**Owner question/request (original):**

> so can u check and tell we dont neeed to make change in sunnypilot

**Answer (summary):** Checked Cereal compatibility: vehicle definitions are imported from opendbc, so no edit under openpilot/cereal is needed for the name. Active mode still needs schema/rules/interface qualification. A noOutput encode/decode check passed.

**Status/limits at backfill:** Messaging round trip is not completed active control.

**Evidence:** exact archive record `CHAT-20261103-032`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1639, final-answer line(s) 1675.

## CHAT-20261103-033

**Topic:** Are the identifier and safety rules already done?

**Asked (UTC):** 2026-11-03T20:28:47.674Z

**Owner question/request (original):**

> 1. **[\`opendbc/car/car.capnp\`](/home/radxa/comma/sunnypilot/opendbc_repo/opendbc/car/car.capnp)** — define the new safety identifier.
> 2. **[\`opendbc/safety/\`](/home/radxa/comma/sunnypilot/opendbc_repo/opendbc/safety/)** — implement and register its rules, with tests. see if this is doe

**Answer (summary):** Checked and found neither identifier nor rules/registration nor test_retropilot.py present at that moment. The interface still requested noOutput.

**Status/limits at backfill:** Historical November 3 check; all three software pieces were added later.

**Evidence:** exact archive record `CHAT-20261103-033`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1682, final-answer line(s) 1700.

## CHAT-20261103-034

**Topic:** Teacher, do we need these safety pieces?

**Asked (UTC):** 2026-11-03T20:30:19.244Z

**Owner question/request (original):**

> **I checked: neither is done yet.**
>
> | Required piece                                  | Current status      |
> | ----------------------------------------------- | ------------------- |
> | RetroPilot safety identifier in `car/car.capnp` | **Not added**       |
> | Safety rules and registration under `safety/`   | **Not implemented** |
> | `safety/tests/test_retropilot.py`               | **Does not exist**  |
>
> &#x20;see i told i dont knw codeing ,teacher do we need to do this

**Answer (summary):** Yes for completing custom active control. They check commands before they reach the vehicle. The agent should handle this coding work; the owner need not write it.

**Status/limits at backfill:** Explained remaining work; Chimera held and relays excluded.

**Evidence:** exact archive record `CHAT-20261103-034`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1707, final-answer line(s) 1711.

## CHAT-20261103-035

**Topic:** Do we need the identifier and test file?

**Asked (UTC):** 2026-11-03T20:58:25.922Z

**Owner question/request (original):**

> RetroPilot safety identifier in `car/car.capnp` ,`safety/tests/test_retropilot.py` question is do e need it

**Answer (summary):** Yes for our planned custom mode: the identifier selects the policy; the tests verify it. Actual safety rules are also required. Sunnypilot does not execute this development test file while driving.

**Status/limits at backfill:** Development tests and runtime enforcement have different jobs.

**Evidence:** exact archive record `CHAT-20261103-035`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1718, final-answer line(s) 1722.

## CHAT-20261103-036

**Topic:** Fix the missing safety pieces

**Asked (UTC):** 2026-11-03T21:00:44.920Z

**Owner question/request (original):**

> fix it then

**Answer (summary):** Added the modern identifier, registered retropilot.h and test_retropilot.py. Reported 21 focused native safety tests and the full suite passing with existing skips. This first version allowed only disabled commands and blocked active output, malformed frames and relays.

**Status/limits at backfill:** Implemented software; no firmware flash. Active limits and engagement rules came in the later offline engine.

**Evidence:** exact archive record `CHAT-20261103-036`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1729, final-answer line(s) 1961.

## CHAT-20261103-037

**Topic:** What did retropilot.h and the 21 tests do?

**Asked (UTC):** 2026-11-03T21:19:41.498Z

**Owner question/request (original):**

> **21 focused safety tests passed**, and the full native safety suite passed with its existing skips.
> ,wat is this ,/home/radxa/comma/sunnypilot/opendbc_repo/opendbc/safety/modes/retropilot.h wat did we do

**Answer (summary):** retropilot.h checked command address/bus/length/checksum, allowed only disabled commands and blocked active commands, relays and forwarding. Native C tests fed artificial frames into compiled code on Radxa; none were sent to a board, game or car.

**Status/limits at backfill:** Historical disabled-policy checkpoint; test success did not establish active control.

**Evidence:** exact archive record `CHAT-20261103-037`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1970, final-answer line(s) 1974.

## CHAT-20261103-038

**Topic:** Is our retropilot.h the C2 file?

**Asked (UTC):** 2026-11-03T21:35:02.623Z

**Owner question/request (original):**

> `retropilot.h` is the code give in c2

**Answer (summary):** No. Ours was newly written for modern opendbc using the shared message definitions. The old C2 policy attempted active commands but left important checks unfinished.

**Status/limits at backfill:** Not a copied or completed C2 firmware installation.

**Evidence:** exact archive record `CHAT-20261103-038`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1981, final-answer line(s) 1985.

## CHAT-20261103-039

**Topic:** What means C2 safety implementation?

**Asked (UTC):** 2026-11-03T21:39:23.588Z

**Owner question/request (original):**

> C2 safety implementation wat it mean

**Answer (summary):** The old author's actual rule code, linked to the schema identifier and selected by his car interface. It was intended to check outgoing commands, but important checks were unfinished.

**Status/limits at backfill:** Explains the old implementation; does not qualify either platform for driving.

**Evidence:** exact archive record `CHAT-20261103-039`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 1992, final-answer line(s) 1995.

## CHAT-20261103-040

**Topic:** Why are other safety headers longer? Show the old file

**Asked (UTC):** 2026-11-03T21:53:18.549Z

**Owner question/request (original):**

> our files and other real car h file is short wat we missed can u show safety_retropilot.h

**Answer (summary):** Opened the complete retained safety_retropilot.h and compared it with our then-62-line file and the 187-line Rivian file. Missing active features included incoming integrity/health, feedback, engagement/override, steering and pedal limits. C2 itself enabled controls on receipt and had commented-out receive validation.

**Status/limits at backfill:** Line counts describe that checkpoint only; line count is not a safety measure.

**Evidence:** exact archive record `CHAT-20261103-040`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2002, final-answer line(s) 2029.

## CHAT-20261103-041

**Topic:** Why not fix the missing active checks?

**Asked (UTC):** 2026-11-03T21:59:51.655Z

**Owner question/request (original):**

> why not fix it

**Answer (summary):** Work continued with a question about the actual BeamNG vehicle/limits. The completed response is attached to the owner's next reply asking what the bridge author used.

**Status/limits at backfill:** No separate final before the clarification; see linked continuation.

**Answer continuation:** [CHAT-20261103-042](#chat-20261103-042).

**Evidence:** exact archive record `CHAT-20261103-041`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2036; continuation/new-closeout status above.

## CHAT-20261103-042

**Topic:** Which BeamNG car did the bridge author choose?

**Asked (UTC):** 2026-11-03T22:06:29.867Z

**Clarification asked by agent (original):** Which BeamNG vehicle and configuration are you using? I couldn’t find a selected vehicle in the saved notes. I can build the message and shutdown checks while you reply; the final active limits need a concrete target.

**Owner reply (original):** see thre was beamng-openlit guy rt which car did he chose

**Answer (summary):** The saved guide showed an Ibishu Covet example and discussed ETK 800; the bridge uses the spawned car. Its HONDA_CIVIC_2022 CAN identity did not identify the game model. Also reported completing the profile-gated safety engine with 50 focused tests and the broader suite passing.

**Status/limits at backfill:** Owner's actual vehicle/configuration and calibrated limits remain unconfirmed; live output stayed disabled.

**Continues:** [CHAT-20261103-041](#chat-20261103-041).

**Evidence:** exact archive record `CHAT-20261103-042`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2115, final-answer line(s) 2437.

## CHAT-20261103-043

**Topic:** Why two RetroPilot files in safety/modes?

**Asked (UTC):** 2026-11-03T22:22:28.329Z

**Owner question/request (original):**

> why ew have 2 refetropilot files in modes

**Answer (summary):** retropilot.h is the entry/disabled-command policy; retropilot_active.h contains additional incoming-data, engagement, steering and pedal checks and is included by the first. Together they are one implementation.

**Status/limits at backfill:** Active profile remains unqualified; splitting files did not enable live control.

**Evidence:** exact archive record `CHAT-20261103-043`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2447, final-answer line(s) 2451.

## CHAT-20261103-044

**Topic:** Is modes the Panda safety?

**Asked (UTC):** 2026-11-03T22:23:40.601Z

**Owner question/request (original):**

> so modes is the saafet to panda

**Answer (summary):** Yes: Panda firmware uses these source rules to permit or block CAN transmissions. Sunnypilot requests a mode and the board enforces it. Our tested source had not been installed into Chimera.

**Status/limits at backfill:** Chimera would need compatible firmware and actual enforcement; no flash performed.

**Evidence:** exact archive record `CHAT-20261103-044`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2458, final-answer line(s) 2461.

## CHAT-20261103-045

**Topic:** Are car/retropilot, DBC and safety modes all that is needed?

**Asked (UTC):** 2026-11-03T22:25:02.975Z

**Owner question/request (original):**

> so cars/retropilot folfder ,dc and this modes retro files are only needed to port the new car

**Answer (summary):** They are the three main parts, but shared registration/selection, correct physical parameters/tuning and compatible CAN hardware/firmware are also required. Software registrations exist; live integration/calibration remain unfinished.

**Status/limits at backfill:** Chimera held; output disabled.

**Evidence:** exact archive record `CHAT-20261103-045`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2468, final-answer line(s) 2472.

## CHAT-20261103-046

**Topic:** How does ours differ from C2?

**Asked (UTC):** 2026-11-03T22:26:24.707Z

**Owner question/request (original):**

> ours and c2 wat is the difference

**Answer (summary):** Modern opendbc layout, canonical messages, adapted/offline command calculations and tested integrity/engagement/limit checks, with no live output. C2 could transmit using historical settings and unfinished safety. Our Chimera/BeamNG loop was still unproven.

**Status/limits at backfill:** No claim that newer software tests alone establish working hardware.

**Evidence:** exact archive record `CHAT-20261103-046`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2479, final-answer line(s) 2483.

## CHAT-20261103-047

**Topic:** Audit, save teacher/student, close VS Code and shut down

**Asked (UTC):** 2026-11-03T22:28:15.584Z

**Owner question/request (original):**

> auidt wat we did let teh teacher and student learn it ,save and shut down vscod and pc last

**Answer (summary):** The historical response reported 168 passing checks, saved teacher/student notes, clean repositories and commit ec53967. Radxa shutdown was scheduled with desktop cleanup; the BeamNG PC was left running.

**Status/limits at backfill:** Historical action on November 3; this saved request is not a new shutdown instruction.

**Evidence:** exact archive record `CHAT-20261103-047`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2490, final-answer line(s) 2607.

## CHAT-20261104-001

**Topic:** What is Ocelot in C2?

**Asked (UTC):** 2026-11-04T14:22:03.722Z

**Owner question/request (original):**

> can u tell me about ocelot memyion in c2

**Answer (summary):** Ocelot is the hardware/firmware family: Chimera, Interceptor Core, Actuator Core and iBooster firmware. Old ocelotcan.py built commands and the DBC described them. Our commands.py fills the modern command-building role.

**Status/limits at backfill:** Board firmware remains separate; hardware integration is unfinished.

**Evidence:** exact archive record `CHAT-20261104-001`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2620, final-answer line(s) 2652.

## CHAT-20261104-002

**Topic:** Do we need that DBC? Compare old and current

**Asked (UTC):** 2026-11-04T14:25:35.750Z

**Owner question/request (original):**

> so dont we need this dbc right ,compare our old and this one

**Answer (summary):** Yes, already included. Canonical retropilot/dbc/ocelot_controls.dbc and the packaged copy were byte-identical: 7,363 bytes, 20 messages, 120 fields. Surrounding modern code was adapted; no extra Ocelot DBC was missing.

**Status/limits at backfill:** Definition match does not establish that all installed producers match.

**Evidence:** exact archive record `CHAT-20261104-002`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2659, final-answer line(s) 2685.

## CHAT-20261104-003

**Topic:** Rename it retropilot.dbc?

**Asked (UTC):** 2026-11-04T14:29:03.508Z

**Owner question/request (original):**

> shouls we chnage it to retropilot.dbc?

**Answer (summary):** Recommended keeping ocelot_controls.dbc to match the canonical shared protocol and its provenance. A rename would require coordinated configuration/checksum/test updates without improving function.

**Status/limits at backfill:** Recommendation only; no rename performed.

**Evidence:** exact archive record `CHAT-20261104-003`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2692, final-answer line(s) 2696.

## CHAT-20261104-004

**Topic:** Required hardware: Chimera, Interceptor Core, Actuator Core

**Asked (UTC):** 2026-11-04T14:32:06.703Z

**Owner question/request (labelled paraphrase of long pasted text):** Required hardware: Chimera, Interceptor Core, Actuator Core. Full original in the exact-text archive.

**Answer (summary):** Saved all three as owner-selected required hardware in both notebooks: computer/CAN and signals, analog pedal/steering interface, and custom actuator motors respectively.

**Status/limits at backfill:** Selection documented, not proof of installed or qualified hardware; no relay requirement added.

**Evidence:** exact archive record `CHAT-20261104-004`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2703, final-answer line(s) 2723.

## CHAT-20261104-005

**Topic:** Label camera, Thneed and RetroPilot commits

**Asked (UTC):** 2026-11-04T14:34:21.916Z

**Owner question/request (original):**

> see beofre we worked on camera ,all the commit relate to it should be mention camera, all the things we did for running thneed model should mention,thneed in commit,all the things we did for retorpilot give commit name this  update it

**Answer (summary):** Updated 64 historical commit subjects with camera/thneed/retropilot labels, retaining original history and an old/new SHA map. File trees were unchanged. Future related commits should use these labels.

**Status/limits at backfill:** Owner-authorized history operation at that time; not permission for further rewriting.

**Evidence:** exact archive record `CHAT-20261104-005`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2730, final-answer line(s) 2849.

## CHAT-20261104-006

**Topic:** Any upstream master updates? Ask before updating

**Asked (UTC):** 2026-11-04T16:02:56.062Z

**Owner question/request (original):**

> is there any update in this master in github,do not update yet without asking

**Answer (summary):** Found two newer upstream commits: MICI steering-arc visibility and predictive acceleration boost. Neither was then applied to the protected Radxa project. The separate reference had refreshed earlier; automatic updates were paused on this instruction.

**Status/limits at backfill:** Later approval applied exactly those two. Future upstream updates remain held.

**Evidence:** exact archive record `CHAT-20261104-006`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2856, final-answer line(s) 2931.

## CHAT-20261104-007

**Topic:** Apply only those two; preserve camera, Thneed/model and RetroPilot

**Asked (UTC):** 2026-11-04T16:09:43.417Z

**Owner question/request (original):**

> update these 2 ,not camer ,thneed model and retropilot do not touch

**Answer (summary):** Applied both approved changes, preserving protected work. Reported 217 passing CPU tests and one existing skip. Teacher/student notes saved; automatic updates remained paused.

**Status/limits at backfill:** Completed scoped integration, not general permission for further updates or live driving.

**Evidence:** exact archive record `CHAT-20261104-007`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 2938, final-answer line(s) 3156.

## CHAT-20261104-008

**Topic:** Create radxa-pilot, preserve master and our branch/commits

**Asked (UTC):** 2026-11-04T16:20:33.397Z

**Owner question/request (original):**

> i want to to make a repo for me radxa-pilot inside by github ,keep the master sunnypilot and this repo as its branch ,copy only the sunnypilot folder in comma ,make sure the commit is there wat we chnaged

**Answer (summary):** Publication continued after the owner selected the public-history option. The completed repository answer is attached to that clarification.

**Status/limits at backfill:** No separate final before the reply; see continuation.

**Answer continuation:** [CHAT-20261104-009](#chat-20261104-009).

**Evidence:** exact archive record `CHAT-20261104-008`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3163; continuation/new-closeout status above.

## CHAT-20261104-009

**Topic:** Publication clarification: public Sunnypilot history

**Asked (UTC):** 2026-11-04T16:34:42.238Z

**Clarification asked by agent (original):** GitHub rejected the independent private copy because its old history references thousands of model files. Which should I use for radxa-pilot?

**Owner reply (original):** Public Sunnypilot fork — preserves the original history and our commits

**Answer (summary):** Created public Deggory/radxa-pilot: master for original Sunnypilot, radxa/q8b for our work, and opendbc/retropilot for child history. Uploaded the Sunnypilot project/assets and verified a fresh clone and hashes. It is a standalone public copy; the existing sunnypilot-pc network fork was untouched.

**Status/limits at backfill:** Publication complete at 40a0c9f8. Later notebook commits are local; this task does not push them.

**Continues:** [CHAT-20261104-008](#chat-20261104-008).

**Evidence:** exact archive record `CHAT-20261104-009`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3353, final-answer line(s) 3525.

## CHAT-20261104-010

**Topic:** All data our DBC can get

**Asked (UTC):** 2026-11-04T17:57:55.992Z

**Owner question/request (original):**

> I WANT U TO tell wat all data our dbc can get

**Answer (summary):** Inventoried 20 messages/120 fields including readings, commands, checksums and counters. Readings cover angle/rate, engine/ignition/brake, speed/pulses, buttons, interceptors and actuators, plus legacy SSC/iBooster/relay entries. It lacks gear, individual wheel speeds, GPS/IMU, radar and several factory statuses.

**Status/limits at backfill:** Only matching producers supply data; not every field is consumed by current CarState. Relays remain excluded.

**Evidence:** exact archive record `CHAT-20261104-010`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3535, final-answer line(s) 3571.

## CHAT-20261104-011

**Topic:** Does it include dzid stepper control and ZSS angle?

**Asked (UTC):** 2026-11-04T18:12:00.395Z

**Owner question/request (original):**

> does it have dzid dbc to contronl stepper motor ,then Zss  steering angle

**Answer (summary):** Yes as wire definitions: dzid SSC commands/status at 0x22E/0x22F and updated ZSS angle at 0x50. Reviewed dzid firmware uses a different checksum and is not integrated for active control. Updated ZSS v0.2 source matches the shared schema/CRC; old smartZSS 0x23 differs.

**Status/limits at backfill:** Physical calibration/testing and dzid checksum/profile adaptation remain pending. Motor encoder angle is not automatically steering-wheel angle.

**Evidence:** exact archive record `CHAT-20261104-011`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3578, final-answer line(s) 3616.

## CHAT-20261104-012

**Topic:** Are these analog inputs converted to CAN?

**Asked (UTC):** 2026-11-04T18:20:28.988Z

**Owner question/request (original):**

> so this bascially anglog inputs right which converted to can t

**Answer (summary):** For analog sensors, MCU firmware reads voltage and packs CAN values. ZSS instead reads a digital encoder. Commands travel the reverse direction through the actuator controller. Firmware performs conversions; the DBC describes encoding.

**Status/limits at backfill:** Architecture explanation, not a new hardware test.

**Evidence:** exact archive record `CHAT-20261104-012`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3623, final-answer line(s) 3627.

## CHAT-20261104-013

**Topic:** Can Sunnypilot read OEM CAN using a second DBC?

**Asked (UTC):** 2026-11-04T18:21:56.028Z

**Owner question/request (original):**

> wat if i connect to cars can bus to get data ,can sunnypilot can take input from 2 dbc files

**Answer (summary):** Yes: independent DBC parsers can feed one combined CarState. An OEM DBC could supply available factory data while RetroPilot supplies retrofit feedback. Our current port only has its RetroPilot parser; OEM mapping, health, units/source priority and ID conflicts still need explicit implementation.

**Status/limits at backfill:** Supported architecture, not already-added OEM support. Separate channels or translation may be necessary for conflicting IDs.

**Evidence:** exact archive record `CHAT-20261104-013`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3634, final-answer line(s) 3662.

## CHAT-20261104-014

**Topic:** Are teacher and student saving my questions and answers?

**Asked (UTC):** 2026-11-04T18:33:59.864Z

**Owner question/request (original):**

> is teh Ai teacher and student keeping note of questin i ask ,later it shouls knw wat i aske dand its answer

**Answer (summary):** Saved seven recent explicit Q&A entries in both existing logs and added startup/closeout instructions to read relevant answers and record new ones, with evidence and limits. Committed locally without pushing.

**Status/limits at backfill:** That first backfill covered only recent questions. The current request expands coverage to both days.

**Evidence:** exact archive record `CHAT-20261104-014`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3669, final-answer line(s) 3711.

## CHAT-20261104-015

**Topic:** Save all questions from today and yesterday

**Asked (UTC):** 2026-11-04T18:38:08.214Z

**Owner question/request (original):**

> all the question today and yesterd ,

**Answer (summary):** Recovered and saved all 62 owner questions/requests/clarification replies found in the local November 3–4 conversations: 47 from November 3 and 15 from November 4, including this request. Retained 58 original completed answers, linked three requests to their clarification continuations, and recorded this closeout separately.

**Status/limits at backfill:** Documentation only. Scope is the locally retained conversations through 18:38:08 UTC on November 4, not deleted/unsent/other-device chats or future questions.

**Evidence:** exact archive record `CHAT-20261104-015`, session `01a1a0de-8fab-7b30-b9c6-3c6df8c05146`, owner line 3718; continuation/new-closeout status above.

---

# Answered owner questions — 2026-11-04

This section records actual questions/requests and the answers given. Existing
unresolved questions remain below. Earlier answers also live in topic/session
notes; this backfill covers the recent visible conversation, not every past
chat message. Labels distinguish completed work, source findings and proposals.
At later sessions, read the relevant entries before asking the owner to repeat
information. Append dated corrections when facts change; do not erase history.

## QA-20261104-01 — updates

**Owner question/request:** update these 2 ,not camer ,thneed model and retropilot do not touch

**Answer:** Applied exactly upstream a86979d2 (Sunnylink steering-arc visibility) and8cf6ff9a (predictive acceleration boost) as67876efc/a009818b. Camera,Thneed/model and RetroPilot source were preserved.217distinct CPU tests passed,1existing skip at that task. Future upstream updates and timer remain on hold.

**Status/limits:** Completed implementation; validation is scoped historical evidence, not live driving proof.

**Evidence:** [source/topic/session](Reports/upstream-approved-20261104/README.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-02 — github

**Owner question/request:** I want a radxa-pilot repository on my GitHub, original Sunnypilot master plus our Radxa branch, only the Sunnypilot folder and our existing commits. [Faithful paraphrase; later owner explicitly chose public.]

**Answer:** Created public Deggory/radxa-pilot:master8cf6ff9a,radxa/q8b,opendbc/retropilot671f8c4. Existing commit IDs preserved;290LFS objects uploaded, fresh recursive clone and3downloaded asset hashes verified. It is a standalone public copy; existing sunnypilot-pc network fork untouched. Public branch last published40a0c9f8; later explanatory notebook commits are local only.

**Status/limits:** Publication complete; no assumption that subsequent notes have been pushed.

**Evidence:** [source/topic/session](Reports/github-publication-20261104/README.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-03 — dbc-data

**Owner question/request:** I WANT U TO tell wat all data our dbc can get

**Answer:** ocelot_controls.dbc defines20messages/120fields:12sensor-status reports and8commands, including repeated CRC/counter fields. Readings cover speed,RPM/ignition/brake switch,angle/rate,buttons,pedal/interceptor and actuator feedback. Legacy SSC/iBooster/relay entries also exist; relays remain excluded. Gear,individual wheel speeds,GPS/IMU and other absent fields are not created by this DBC. Definition does not mean every signal is transmitted or mapped into CarState.

**Status/limits:** Source inventory confirmed; producer units/calibration and current mapping limits remain.

**Evidence:** [source/topic/session](Evidence/retropilot-dbc-inventory-20261104.json). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-04 — dzid-zss

**Owner question/request:** does it have dzid dbc to contronl stepper motor ,then Zss steering angle

**Answer:** Yes as definitions:SSC command0x22E(5bytes)/status0x22F(8bytes) for dzid, and separate STEER_ANGLE_SENSOR0x50(6bytes) for updated ZSSv0.2. dzid firmware782676bc has additive CAN-ID checksum versus canonical CRC8J1850; current Sunnypilot profile excludes active SSC. Updated ZSS code matches schema/CRC but physical calibration is pending; original smartZSS0x23 differs. Motor encoder angle is not automatically steering-wheel angle.

**Status/limits:** Wire definitions/source comparison, not a tested live dzid or ZSS installation.

**Evidence:** [source/topic/session](Sessions/2026-11-04-dzid-zss-dbc.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-05 — analog-can

**Owner question/request:** so this bascially anglog inputs right which converted to can t

**Answer:** Yes for analog sources:sensor voltage is read by MCU firmware and encoded into CAN. Some inputs are digital; our ZSS designs read digital encoders and publish angle. Motor control goes Sunnypilot request→CAN→controller→motor. Firmware performs conversion; DBC describes packing. This explains the architecture, not proof of installed hardware or working live transport.

**Status/limits:** Conceptual explanation consistent with pinned source; no new test.

**Evidence:** [source/topic/session](Knowledge/RETROPILOT_CAR_PORT.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-06 — two-dbcs

**Owner question/request:** wat if i connect to cars can bus to get data ,can sunnypilot can take input from 2 dbc files

**Answer:** Yes:separate CANParser instances can use different DBCs and CarState combines explicitly selected readings. Existing Honda code demonstrates two DBCs. OEM DBC could supply available factory data while canonical RetroPilot DBC supplies retrofit/ZSS feedback. Current RetroPilot is single-parser and still expects its base messages; adding OEM input needs parser/mapping/health changes. Bus routing,ID collisions,units and source authority must be resolved; no new car or wiring selected.

**Status/limits:** Supported architecture; OEM+RetroPilot integration is not implemented.

**Evidence:** [source/topic/session](Sessions/2026-11-04-oem-retropilot-dbc.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

## QA-20261104-07 — memory

**Owner question/request:** is teh Ai teacher and student keeping note of questin i ask ,later it shouls knw wat i aske dand its answer

**Answer:** Yes through persistent workspace files. Earlier replies were retained in topic/session notes; today explicit dated question-and-answer entries were added to teacher QUESTION_LOG and student QUESTIONS. Startup and closeout rules now require reading relevant prior answers and recording new owner project questions, actual answers,evidence,status and corrections. This is file-based context for later sessions, not automatic model training or a guaranteed full chat transcript.

**Status/limits:** Standing owner requirement recorded and implemented in both memory layers.

**Evidence:** [source/topic/session](Sessions/2026-11-04-owner-question-memory.md). Source application40a0c9f8/child671f8c4 unless the linked report pins another historical version.

---

## 2026-11-03 — Game car/configuration still unconfirmed

Asked which BeamNG vehicle/configuration is selected. Owner referred to the
BeamNG-openpilot author instead of naming the currently loaded vehicle. Saved
Caleb5435d674 source does not force one model: user spawns a car; Covet is an
example, ETK800 appears in geometry examples. Do not silently select either
as the owner's car. Native algorithm tests use artificial limits; final game
profile/command mapping remains unresolved. Continue independent software work
without resuming held Chimera or physical Interceptor tasks.

2026-11-03 identification update: C2-name compatibility is implemented at04a7835.
Remaining identification question is measured automatic CAN/ECU identity, not
fixed selection. Teacher C2 used a forced name and placeholder fingerprint.
No owner question needed for the completed alias/migration increment.

## 2026-11-03 — RetroPilot live-integration facts still needed

Car code stage implemented; no question pending for this completed increment.
Before live integration: confirm installed Chimera image/health/bus route,
producer speed units (C2rawkm/h vs saved Hall*100 and ambiguous MODE), actual
vehicle geometry/dynamics, endpoint calibration and MCU safety. Wheel/gear/
cruise-status/IMU/session gaps remain in the shared contract. Teacher evidence
was recovered first; do not ask the owner to repeat already retained facts.

## 2026-11-03 — BeamNG optical webcam + Waveshare/Chimera CAN design

Open implementation facts: canonical wheel/IMU/session/gear and cruise-status mapping, speed units/MODE, selected game actuator family, installed Chimera behavior/routing, timeouts/bus load. Later bench: measured angle authority, endpoint types/calibration and physical stop behavior. Teacher evidence recovered before any owner questions; no new question pending.

# Unknowns and limits

Owner deferred automatic calibration2026-11-02, choosing temporary MM-X
fixed intrinsics in Q8B road-only mode. Future replacement options: target-assisted collection/solve
and measured vehicle-frame target pose, or target-free estimation with
independent validation/alignment. Existing guided capture is not autosave.

These remain open; the notebook must not silently fill them in.

- Current stock model/runtime/parser compatibility with the preserved MSM
  Adreno execution path. Older measured model results concern a different
  model identity and runtime contract.
- Identity is implemented at12e44fee; actual Q8B camera calibration and external
  reader/future-upstream compatibility for local enum ordinal8 remain open.
- IMU model/connection are known:Adafruit LSM6DS3TR-C/I²C9/0x6a. Current
  managed IMU/GNSS providers, installed mounting axes, units, rates and clock
  alignment; comma I²C/GPIO paths are not compatibility evidence.
- Q8B road-only720pVisionIPC layout/source IDs/timestamp pairing and model copy
  now tested; current CPU-warp synthetic parity matches ONNX input. Remaining
  inference/recording/native-UI buffer contracts and Adreno execution are open.
- Actual lens K/distortion, stable optical/focus state and camera mount remain
  unmeasured. Owner selected printable target/tool; candidates are never
  automatically installed. Current continuous autofocus1needs explicit review.
- Real thermal/power/fan behavior, host display/input and recording backend.
- Managed startup, dead-child restart, stale-data and shutdown qualification.
- Later custom steering feedback, car interface, bus routing and safety. A
  copied controller cannot establish measured actuator behavior.
- Deep algorithm-level review outside inspected paths. All tracked paths can
  be indexed while substantial behavior remains unreviewed and untested.

Use [coverage](Knowledge/COVERAGE.md) and the
[workspace question log](/home/radxa/comma/Ai/QUESTION_LOG.md) for related evidence.

2026-11-02 — Open evidence question (no owner answer needed yet): does bundled
Mountain Dew v3/1e219d77 match historical big ONNX6fee5937 graph and weights?
Compare retained source/export/contracts first; NPU38.196ms timing cannot be
assigned to bundled pickle before that. [Review](Sessions/2026-11-02-big-model-npu.md).
