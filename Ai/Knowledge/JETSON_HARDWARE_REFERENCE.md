## November 7 — Panda / Chimera comparison (QA18)

Compared older black/F413 Panda, original F413 Chimera and red/H725 Panda.
Red adds H7/CAN FD; original Chimera has custom inputs/config/relay behavior.
USB transport is shared but installed firmware protocols differ (original
mailbox16/health43). The new chimera/ remains an unfinished, halted F413 rewrite;
chimera_old/ remains preserved. No integration or physical test claimed.
Baseline ab07117573529c2e54d74f47eb3d66c0542f5506; Panda8a16e089.
Source-only explanation; notebook checks only, no source/build/hardware/update/push.
Next: await owner-selected scope; no automatic resumption. See QA-20261107-18.

## November7 — Jetson Panda identity follow-up

QA17: author says H7 USB; official red/H7 target is STM32H725, legacy black/F4
STM32F413. Author-specific PCB/chip marking remains unconfirmed. Custom
sunnypilot-cuda AGXOrin branch explicitly named; exact upstream base unresolved.
Source-only follow-up on076d73bf and official Panda8a16e089, no source/hardware
change. Modern Chimera remains halted and chimera_old preserved.

## November7 — Jetson Panda USB explanation (read-only)

QA-20261107-16 records H7 USB-A, default SPI gating, rig-specific v17/57 health
repair and cross-fork expected firmware synchronization. Four pinned076d73bf
files reread via GitHub connector; no scripts executed or hardware claim. Pattern
is relevant to host adaptation, not direct Chimera compatibility. Original Chimera
mailbox16/health43 differs. Modern Chimera remains halted; chimera_old/ preserved;
no firmware/host implementation resumed. Baseline591683739.

# Jetson hardware approaches: teacher evidence for Q8B

2026-11-01 follow-up to the owner's non-camera hardware checklist. Teacher
already holds two distinct2026-10-27 source studies. They are different projects,
not one verified Jetson/Sunnypilot implementation. This note reads that evidence
first and checks selected original source at the same immutable pins. It does
not claim the branch tips are unchanged or that either port runs correctly here.

## 1. DragonPilot full-port reference

Repository Deggory/dp_agx_orin, orin-port source
`d0c3a6e3e890ee9162109f7d932eca116f903289`, DragonPilot0.10.3. The code carries
Xavier support plus an Orin adaptation. This differs from our Sunny2026.003.000/
COMMA0.11.3. Historical benchmarks refer to their stated device/conditions.

| Hardware job | What this code implements | Limit relevant to Q8B |
| --- | --- | --- |
| Platform identity | /JETSON selects Python Jetson and C++ HardwareJetson, with a Jetson build/profile | Serialized enum remains pc; NVIDIA profile is not our Radxa profile |
| Temperatures | Discovers thermal-zone type names; chooses CPU/GPU/memory/PMIC candidates | Missing zones become empty; verify actual physical meaning rather than copy names |
| Power | Discovers INA3221/ina3221x hwmon directories; multiplies channel voltage/current and sums channels1..3 | Board rails can overlap; get_som_power_draw returns the same aggregate, not independently qualified SoM measurement |
| GPU load | Reads /sys/devices/gpu.0/load and scales by10 | NVIDIA-specific path, failure returns0; not Q8B load implementation |
| Fan output | JetsonFanController computes desired speed and writes0..255 to /sys/devices/pwm-fan/target_pwm | No Q8B hwmon PWM mapping or RPM proof; write errors can be swallowed |
| Power modes | nvpmodel, jetson_clocks, core4..7 online changes, DFS/clock-watchdog/hugepage initialization | NVIDIA/board-specific behavior; no direct Q8B transfer or qualification |
| Network | Checks sysfs interface operational state and Ethernet/Wi-Fi name prefixes | Heuristic detection, not complete modem/default-route health |
| Display | Brightness setter is a no-op and getter returns0 | A dedicated backend does not mean every operation is implemented |
| IMU/GNSS services | Stock sensord/qcomgpsd/ubloxd/pigeond enabled only on TICI | Dedicated Jetson identity alone supplies no external IMU/GNSS producer |
| Vehicle transport | Existing Panda/card/ignition path remains | Not a new compatible RetroPilot transport or permission for actuation |

Source links: [Python hardware](https://github.com/Deggory/dp_agx_orin/blob/d0c3a6e3e890ee9162109f7d932eca116f903289/system/hardware/jetson/hardware.py),
[C++ hardware](https://github.com/Deggory/dp_agx_orin/blob/d0c3a6e3e890ee9162109f7d932eca116f903289/system/hardware/jetson/hardware.h),
[fan controller](https://github.com/Deggory/dp_agx_orin/blob/d0c3a6e3e890ee9162109f7d932eca116f903289/system/hardware/jetson/fan_controller.py),
[process selection](https://github.com/Deggory/dp_agx_orin/blob/d0c3a6e3e890ee9162109f7d932eca116f903289/system/manager/process_config.py).

The teacher's earlier study found Python INA discovery but C++ still hardcoded
an older Xavier INA path. Power-mode IDs and clock/thermal assumptions also
needed device-specific qualification. Retained pure-helper tests exposed DFS
behavior issues; those were synthetic source tests, not real Jetson failures.
Do not create /JETSON on Radxa or run its initialization/power scripts.

## 2. Feiyang hardware/model overlay

Repository feiyang2025/jetson-cuda-overlay, source
`076d73bf9a2e055c83fbe9b2a3c16a8383519ba4`. This overlay patches an existing
openpilot-family tree, rather than supplying the same full hardware backend
as the DragonPilot reference above.

The useful non-camera component is a native external-IMU daemon, ch347t:

- CH347 USB-to-I²C transport for an LSM6DS3-family physical IMU; direct I²C is
  available only with explicit bus selection in the reviewed code.
- Publishes standard accelerometer, gyroscope and temperatureSensor Cereal
  messages. This is an actual physical-sensor producer design, distinct from
  MM-X's PC carState-derived motion observations.
- Build/launcher support and a process_config patch register sensord_ch347 on
  the PC path. Its third-party library/build/message dependencies still matter.
- Adds sensor bias/mount/calibration tools, but the teacher's earlier source
  study and retained synthetic tests found inverted ellipsoid scaling, frame
  mismatches, repeated correction of cached readings and stale-data/timestamp
  concerns. These are reasons to validate each contract before reusing code.

[Publisher helpers](https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/openpilot/system/sensord/ch347t.cc#L739) set sensor time
from publication logMonoTime; that is not proof of hardware acquisition time.
[Manager patch](https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/patch_ch347_manager.py) describes auto-exit without hardware,
but the teacher's fuller source review found a retry loop; do not rely on that
comment as a tested lifecycle guarantee. Earlier platform review also found
PC compile stubs; the overlay does not establish complete thermal/power/GNSS
coverage. Camera and CUDA/TensorRT implementation details stay outside this task.

## Our Q8B application

Take the separation of responsibilities: real board-health methods behind
HardwareRadxa, separate physical-IMU/GNSS publishers, standard messages and
explicit manager ownership. Retain our working board identity and generic
Linux path policy; broad PC=False/JETSON switches are not a capability audit.

Known physical IMU is Adafruit LSM6DS3TR-C/I²C9/address0x6a, four-wire header
1VIN/6GND/3SDA/5SCL with prior ~102Hz raw and in-memory schema proof. It already
has native Q8B I²C access; no CH347 is needed merely to follow the architectural
pattern. Reuse the existing reader/driver knowledge, not Jetson axes/calibration.

Use Q8B's named thermal zones, actual power-domain monitors and radxa_svc_glink
PWM interface. Do not import INA/Xavier paths, NVIDIA power profiles, mode IDs,
fan targets or old calibration constants. Preserve current automatic fan
ownership until a deliberate tested control change. Current source read-only
thermal mapping remains the first bounded implementation candidate; power
mapping/current IMU service follows. Cameras remain deferred.

## Evidence and verification limits

Started local0205e38bf44014c6b57b5508352d924e26d041c8/radxa/q8b, clean;
application identity12e44fee unchanged. Fresh pinned GitHub reads:6 source IDs
match original teacher manifests;4 full bodies match Git blob SHA;3 Python AST
parses;2 selected ranges checked against their file IDs. No source body retained
as a new checkout/mirror, no foreign import/installer/hardware execution.

Reused retained REA evidence from2026-10-27. Integrity readback verified19overlay
and24DP study files, result hashes and actual REA receipts (exit0/quiesced):
48overlay and55DP offline/synthetic assertions. The55 include camera checks in
the old study; none were rerun here. Those are not new device/runtime benchmarks.
Current local source snapshots differ from old October27 references, so the
old all-in-one verifiers' former local-baseline checks were not applied as
claims about today's fresh project. Historical evidence remains unchanged.

Optional workspace sources: teacher Knowledge/Repos/jetson-cuda-overlay.md and
dp-agx-orin.md; jetson/reports and jetson/dp_agx_orin/reports. New metadata and
readback evidence: Ai/Reports/jetson-hardware-20261101. This follow-up changes
only student/teacher documentation, not runtime providers or vehicle behavior.
