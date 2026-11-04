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
