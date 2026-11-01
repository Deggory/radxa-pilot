# Q8B non-camera hardware plan

Proposed implementation order, 2026-11-01. Planning baseline: radxa/q8b
1dd194f1aa42cfac8cac0f83e73a2f4ecefe1684; identity implementation12e44fee,
Sunny2026.003.000/COMMA0.11.3. Task status: [checklist](todo.md).
No driver implemented by this plan.

## Goal and evidence

Extend the existing HardwareRadxa with real measurements in small, tested
increments. Retain Linux/ARM64 and device identity. Start with read-only
temperatures: the board exposes thermal zones, while PC defaults have no real
thermal configuration. Use the [hardware map](../Ai/Knowledge/NONCAMERA_HARDWARE.md),
[Jetson comparison](../Ai/Knowledge/JETSON_HARDWARE_REFERENCE.md) and
[MM-X comparison](../Ai/Knowledge/MM_X_LINUX_REFERENCE.md).
Jetson pins d0c3a6e3/076d73bf and MM-X b9b7f488 are references, not Q8B drivers.

## First slice: temperatures

Read current zone types and qualify CPU/GPU/memory/PMIC meanings using available
board/kernel evidence. Discover by stable type rather than fixed zone number.
Implement qualified categories in HardwareRadxa.get_thermal_config. Review the
actual consumer and choose explicit missing/error behavior: ThermalZone.read
can return zero on a missing file, which must not silently become valid health.
Preserve other platforms.

Acceptance: correct domains/units; meaningful discovery, conversion and
missing/malformed/unreadable-path tests; isolated read-only Q8B readback and
actual current-schema thermal-message encoding; existing identity checks pass.
Record exact commands, samples and limits; commit and journal verification.
This needs no manager launch, fan writes or OS tuning.

## Following slices

1. Power: qualify rail domains and units before reporting measurements. Avoid
   overlapping sums or presenting SoM power as total board/vehicle power.
   Test conversions, failures and isolated live readback. GPU utilization is
   a separate measured backend task; existing zero is a generic default.
2. Physical IMU: reuse known Adafruit LSM6DS3TR-C/I²C9/0x6a and teacher reports.
   Qualify fixed mount, axes, SI units, acquisition timestamps and freshness;
   test bounded live sampling, IPC, consumers and faults. Historical ~102Hz
   raw polling/schema round trips do not establish current integration. Keep
   unrelated stock comma I²C1/GPIO84 wiring disabled on Q8B.
3. Cooling: after thermal reporting, qualify PWM automatic/manual ownership
   and any feedback before changing control. Preserve existing automatic mode
   until a tested policy is ready. PWM does not prove RPM. NVIDIA paths and
   performance modes are not Q8B settings.
4. Remaining platform services: qualify network/display/audio/lifecycle as
   required by current consumers. Identify actual GNSS hardware before its
   provider; existing serial devices are not established GPS receivers.

Each slice gets focused verification, review, commit, validation journal and
teacher/student checkpoint. Reorder only for concrete consumer dependencies.

## Owner preparation and scope

No immediate purchase or rewiring is needed for temperatures. Confirm secure
IMU mounting before final axis/bias calibration; prior loose-board readings
are not mounting calibration. Cameras remain deferred. Model/runtime and
custom steering/CAN are separate later work; shared CAN follows canonical
RetroPilot DBC. This plan does not establish managed-stack readiness or
authorize vehicle actuation. Daily reference updates stay separate from the
protected project.
