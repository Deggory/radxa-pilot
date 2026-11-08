# 2026-11-08 — Chimera CAN deep audit and nightly boot correction

Scope: owner requested all-bus/detection/code/read-path/root-cause investigation.
Accepted no device/config/firmware changes; sensor stays printedCAN2. Started
radxa/q8b1d5b9cc7clean; panda8a16e089/opendbc150f9371clean. See report README and
EVIDENCE.json for exact source/runtime hashes, durations, raw probes and limits.

Completed: fresh exact identity/signature/config/debug reads; native all-bus20s,
independent pre-parser10s capture;23Python/5native suites; existing ARM objdump
analysis found250kdefault and saved-speed overrides, predicting500/500/250k.
No CAN frames/USB bytes received; physical failure not repaired. REA open worked,
overview provider unavailable, target closed. Official ST HAL fetched; RM0430
fetch failed/timeout; exact nightly GitHub commit422/unrecovered. Debug ring read
consumed1023buffered bytes; INIT/watchdogoff/absent mappings, no complete log proof.

Changed only student Ai/ and teacher Ai/.76legacy hashes/nativebinary/canonical
DBC remain unchanged; existing ocelot/steering dirty sets retained. Reader/USB
cleanup verified; Core Config GUI left open/disconnected. No physical movement,
OUT/flash/reset/config/host source change, upstream advance, or push.

Next: separately authorized temporary runtime CAN2=500k via actual nightly DE
handler (bus2/index5000), then capture0x25, with source/signature/ownership guards.
No automatic write; currentBTR/VCC/STB/termination/waveforms unmeasured. If timing
matched but capture stays empty, qualify electrical/RXD and controller/filter
state. Full-source identity and vehicle/control integration remain unqualified.

Skills: debugging, Unlazy solo gates, REA artifact workflow, focused source/graph
explanation, git/documentation. Teacher graph insufficient/stale; source/artifact
pins used. QA56synchronized; corrections precede historical source-only notes.
