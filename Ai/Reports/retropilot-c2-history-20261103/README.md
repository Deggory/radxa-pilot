# RetroPilot C2 history and adaptation to current Sunnypilot

Target confirmed by owner: **existing Radxa Q8B**, not physical comma4.
Parentbase35d46c1e179d0f6a541e32e5669ee0c879b408b1, current upstream reference
a86979d2b2b176413a7f3e5cccf8c807596a7def (GitHub master rechecked this session).
Use its current APIs; preserve the tested CD210/OpenCL/Thneed path.

## Scope and chronology

The [C2 branch](https://github.com/RetroPilot/retropilot/tree/b9a942efd3cb210127bb5efb5cf9ccf6a811c728)
has35commits beyond the retained2022base
da2ea41241f16c4b0e80a52fdc40ed57becd185b.28are dated May15–August14,2025;
7are older upstream commits. Its opendbc ancestry includes work from2021,
2022and2025. This evidence does not support describing all of it as one year
of new work by one author. The important requirement is to recover the full
integration, including work outside the car folder.

Fetched every included parent commit's changed files/patches, the complete
parent comparison and all3modified submodule comparisons through GitHub.
The final parent delta has50paths; the history touches64including transient
changes. Panda has2additional commits/2changed files, Cereal3/6, opendbc43/10.
[Timeline](TIMELINE.md) lists every parent commit with its upstream link.
[Plain-English 2025 guide](2025_COMMITS.md) explains all53dated2025commits across
the application, CAN library, Panda and Cereal, with direct patch links.
[Coverage](coverage.json) assigns all82parent/submodule paths an explicit
disposition. This is complete path coverage, not a claim of line-by-line review
of unrelated kernels/binaries or tested live integration. Relevant transport,
state/control, schema, checksum, lifecycle and safety patches were inspected;
unrelated upstream/build work is attributed separately.

## What the author changed and what we do now

| C2 work | Current adaptation or disposition |
| --- | --- |
| May15: repoint Panda/opendbc/Cereal forks; Ubuntu24 build fixes | Keep current UV/Python3.12/Linux/C++/FFmpeg APIs. Current FFmpeg encoder already uses send-frame/receive-packet. No old Pipenv, Qt, libyuv binary or Cython restoration. |
| June10: new retrofit car interface/controller/state, hard-coded selection and ECU defaults | Modern RetroPilot platform, explicit selection/name migration and per-instance ID/DLC observations implemented. No global override or fabricated module presence. |
| June–July: signed steering angle, speed/engine/cruise ADC signals, counters/CRC and override bit | Canonical final DBC and SAE-J1850 CRC/counters already adapted to Python CAN. Source-state bug corrected here: angle STATE1 means enabled, STATE0 disabled in reviewed Chimera/ZSS producers. |
| Panda safety hooks and Cereal safety enum26 | C2 hook is WIP: arbitrary RX enables controls, integrity checks disabled, DLC mismatches and missing steering/brake limits. Do not copy that policy or numeric enum into modern occupied slots. Live MCU policy/tests remain required. |
| Boardd/USB path | Add Chimera's actual mailbox16/health43 receive adapter and Cereal CAN serialization. C2's retained Panda host uses a different CAN5/health50 contract; modern stock pandad is SPI/CAN6 and has a flash/recovery lifecycle. Do not treat them as interchangeable. |
| Cereal bodycontrol.relayCoreCMD and joystick buttons | Modern commands/profile preview supports an explicit raw relay mask. C2's8-bit joystick mapping is not a qualified owner relay map; canonical wire field is16bits. No new schema ordinals or enabled-state bypass. |
| July: local cruise state machine and engagement changes | Modern button events/available indicator implemented. Modern selfdrived owns engagement; retain unknown gear and carNotReady until actual profile/telemetry is qualified. No fake drive gear or synthetic cruise engagement. |
| Gas, iBooster, steering, relay command mapping | Modern torque/accel preview, separate lat/long activity, slew/speed taper,100/50Hz scheduling and counters implemented. Author constants are labelled offline references;700count steering channel difference conflicts with local Core400limit. |
| PID tune and inactive JSON reload | Current PIDController has a different API and speed-dependent gain arrays. Keep this implementation. C2 kp=.05,ki=.05,kf=.00003 is vehicle-specific reference, not a measured Q8B/game/car tune. No global hot reload from /data/tune_pid.json. |
| controlsd communication/model/GPS event suppression and joystick enable toggle | Preserve modern communication, model, GPS, safety and engagement checks. Resolve missing data at its producer/adapter rather than suppressing events. |
| UI forced restart | Retain modern process enabled/not_run/should_run ownership. C2 special case could start UI before those checks; it is not carried over. |
| NEOS20 OTA URLs and Android setup | Not applicable to the confirmed Linux Radxa target. No legacy phone OS or AGNOS flash. |
| Thneed optimizer/kernels, navigation/OEM updates and old replay pins | Separate inherited2022upstream work, including George Hotz's optimizer commit. Keep current tested model/runtime and current modern navigation/OEM behavior. No old model/kernel replacement. |

Complete exact-path mappings and commit attribution are retained in JSON,
including transient files that do not appear in the final branch diff.

## REA evidence and source limits

Selected retained Chimera ELF, not a new build or installed-device dump:
ocelot/firmware/obj/chimera/chimera.elf,
SHA2565ae9b4f6ea99e569028d271c4ec9c2ce59cd11375b5482adbd0781f3480e20b8.
REA open_binary identified ARM ELF. GNU objdump symbol/disassembly operations
completed without truncation or a changed artifact digest. Relevant functions:

- get_health_pkt at0x080077b0 returns43 and stores raw safety17 at offset38.
- usb_cb_ep1_in at0x080079b8 uses16byte stride and at most4records per callback.
- can_send at0x08006e60 visibly calls can_push/process_can without a safety hook
  in that function body. Source corroborates this; it is not a whole-firmware
  safety proof or proof of what is installed on a board.
- usb_cb_control_msg at0x08007aa8 includes health/version and mutation paths;
  the new receiver exposes only vendor-IN D6/D2 and bulk-IN81.

Full REA Evidence is retained in the symbols/disassembly JSON. Native provider
analysis was unavailable (Ghidra/Hopper/IDA not configured); pwntools layout
profile only supports Linuxx64. Those failed capabilities are recorded rather
than presented as decompilation. GNU provider version/formats were not reliably
probed and remain unknown as its Evidence states. Firmware was never executed.

The read-only sysfs check found bbaa:ddcc product "Interceptor DAC Bench",
serial440048001251333133333633, at bus3/device8. This differs from the
historically probed Chimera3a0044001651333038373636. No USB handle was opened,
CAN consumed or paused Interceptor experiment resumed. Matching VID/PID does
not establish Chimera identity; the adapter also requires product/serial pins.

## Implemented increment and remaining work

The adapter has exact DLC/classical-CAN/bus/reserved-bit validation, raw health
decoding, timeout-byte preservation, explicit cleanup on errors and optional
modern CAN publication. Returned/RTR records remain diagnostic metadata and
cannot refresh vehicle reception. It does not import Panda, flash, subscribe
to sendcan, send CAN, send heartbeats/config/relay/bitrate commands or fabricate
pandaStates. It is a standalone monitor, not an installed manager replacement.

Tests use fake USB with real Cereal and real RetroPilot state/controller code,
plus literal firmware-layout and historical health vectors. They exercise the
path into candidate commands while actual output remains zero. They do not
establish USB timing, bus load, wiring, installed firmware or managed readiness.

Remaining ordered work: identify actual Chimera and collect its pinned receive
data; qualify producer units/source ages/profile; integrate truthful board
health/ignition and exclusive manager ownership/reconnect; complete missing
gear/wheel/motion/driver-input contract; shadow/game-only loop; calibrated
actuator limits and enforced MCU safety before physical output. These gaps
are not resolved by copying C2 bypasses or adding empty safety files.

## Verification

```bash
.venv/bin/python Ai/Reports/retropilot-c2-history-20261103/verify_history.py
.venv/bin/python -m unittest openpilot.selfdrive.pandad.tests.test_chimera \
  openpilot.selfdrive.pandad.tests.test_chimera_protocol -v
.venv/bin/python -m unittest discover -s opendbc_repo/opendbc/car/retropilot/tests -v
```

Actual commands/results and source hashes are captured in
../../Evidence/retropilot-history-adaptation-20261103.json. No live USB/game/CAN
transmission or physical actuation test is included.
