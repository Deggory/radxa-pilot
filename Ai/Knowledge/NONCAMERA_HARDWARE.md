# Non-camera hardware and sensor map

Inspected 2026-11-01 at source5bcc0028c494e248e5d77f7f0cbea8877407415c,
branchradxa/q8b, headersSunny2026.003.000/COMMA0.11.3. Owner selected hardware
work and explicitly deferred cameras. This is a source/read-only host inventory,
not an implemented sensor adapter or a qualified running stack.

## Motion sensors: a separate service from HardwareRadxa

| Input | Meaning / use | Current source contract |
| --- | --- | --- |
| 3-axis accelerometer | Acceleration including gravity; localization motion/orientation estimation | `accelerometer`, `SensorEventData.acceleration.v`, m/s², nominal104Hz |
| 3-axis gyroscope | Rotation rates, including turning/yaw; localization motion estimation | `gyroscope`, `SensorEventData.gyroUncalibrated.v`, rad/s, nominal104Hz |
| IMU temperature | Temperature of the motion sensor chip; logged diagnostic | `temperatureSensor`, °C, nominal2Hz; distinct from CPU/GPU thermal monitoring |
| GNSS/GPS | Geographic position, speed, course, fix/accuracy/time for position-dependent consumers | `gpsLocation` nominal1Hz or `gpsLocationExternal` nominal10Hz; provider-specific |

The stock `system/sensord/sensord.py` instantiates LSM6DS3-family accel/gyro/temp
on I²C1 with GPIOchip0/line84 and comma-specific IRQ/affinity behavior. Drivers
convert native measurements to SI units and use their own mounting convention
`[y,-x,z]`; locationd further transforms to its device frame. Neither mapping
can be copied without knowing the physical Q8B sensor mounting/orientation.

The Q8B retains PC=True, so the stock sensord process is disabled. Its GPIO/I²C
paths must not be enabled unchanged. A real Q8B IMU provider needs supported
transport/driver, actual samples, correct scale/axes, acquisition timestamps,
source identity, rate and dropout/fault tests. Generic HardwareRadxa methods
do not produce accelerometer/gyroscope messages.

`selfdrive/locationd/locationd.py` explicitly consumes accel/gyro with carState,
extrinsics calibration and model odometry. It checks nanosecond sample timestamps
against message time with a100ms limit and tracks live sample freshness below
100ms. Missing/fake motion data cannot be assumed to form a valid localizer.
The current pose estimator does not list GPS among those main subscriptions;
other navigation/position consumers and selfdrived's noGps handling still exist.
GPS is therefore not a replacement for the IMU. This scope leaves camera/model
work deferred; full localization still depends on that later interface.

Magnetic/light/pressure variants exist in the broad schema, but the inspected
current sensord constructs only accel/gyro/temp. Do not treat every historical
schema field as a mandatory active device or invent an installed magnetometer.

## Board health: HardwareRadxa and hardwared

| Reading/interface | Why Sunnypilot uses it | Current Q8B status |
| --- | --- | --- |
| CPU/GPU/memory/PMIC temperatures | hardwared publishes deviceState and computes thermal status | Linux exposes named thermal zones; HardwareRadxa currently returns empty ThermalConfig |
| Power consumption and voltage/current | Hardware power reporting and energy accounting | Readable Linux telemetry exists; backend currently returns0, not a measured0W |
| Fan/cooling | Desired cooling output and actual physical cooling control | A radxa_svc_glink PWM interface is exposed; no Sunnypilot fan integration or RPM proof |
| CPU load, RAM and disk | Device utilization/storage monitoring | Existing common/Linux code paths; managed hardwared not run in this inspection |
| Network/display/platform operations | Connectivity, brightness, shutdown/lifecycle | Generic defaults; need real supported providers if used |

`system/hardware/hardwared.py` calls `HARDWARE.get_thermal_config()` and power/GPU
methods, publishes deviceState nominal2Hz, and separately computes desired fan
percent. That desired percentage is not proof a Q8B fan is driven. Do not write
PWM, change automatic fan mode or copy comma fan settings during this inventory.
Unsupported capabilities must not silently look like valid measured telemetry.

## What Linux exposed on this Q8B

Read-only observations on Ubuntu24.04.5/aarch64/Linux7.0.11-6-qcom:

- 55 thermal zones, including cpu0..7 with two sets of per-core zones, gpuss,
  mem-0/mem-1 and PMIC/board names. Readings were accessible. Counts/numbers are
  observations for this boot; future providers should discover stable names.
- Two exposed IIO devices: PMIC ADC `c440000.spmi:pmic@0:adc@3100` and
  `voltage-divider-adp12v`. Neither exposed in_accel/in_anglvel/in_magn channels.
  This establishes no visible IIO motion channels, not proof the physical board
  or an external module cannot supply an IMU through another interface.
- hwmon names include system_power, typec_port0/typec_port1, adp12v_hwmon and
  radxa_svc_glink. Voltage/current/power attributes and PWM mode/duty were read.
  Their physical domains, accuracy/calibration and final application mapping
  remain unqualified. Raw values are recorded outside the repo in the report.
- No /dev/gnss* node observed. /dev/ttyUSB0 identifies only as CH341 USB Serial;
  /dev/ttyMSM0 also exists. No ports were opened and neither is identified as
  GNSS/IMU by this inventory. No device serial numbers were collected.

Do not label an input-rail ADC as car-battery voltage or infer vehicle ignition
from a USB supply's online flag. Board/USB/SOM/car supply domains need explicit
mapping. A hwmon `power` directory alone is not a power reading.

## Vehicle feedback is another boundary

Later lateral work also needs the selected vehicle/actuator feedback, such as
speed, steering angle and appropriate torque/driver override signals. These
come through the vehicle/actuator interface, not CPU sensors or generic IMU
methods. Requirements depend on the selected control/interface design.
Canonical shared RetroPilot definitions remain the workspace retropilot/dbc;
no CAN IDs, bus routing, DBC, firmware or actuator behavior changed here.

## Next non-camera steps

1. Identify the actual IMU model/connection. An asynchronous question was sent
   to the owner; no model was confirmed at this checkpoint. Do not substitute
   car yaw-rate or synthetic readings for a physical sensor without a separate,
   explicitly validated design.
2. First bounded board-health implementation candidate: read-only Q8B thermal
   configuration using actual zone names, with missing/malformed sensor tests.
   Preserve real failure reporting and existing generic Linux selection.
3. Verify power-domain/units against the installed driver/official ABI, then
   implement measured power reporting separately; do not claim whole-board/SOM
   equivalence from the filename. Fan control is a separate later change.
4. Build/test the IMU provider after transport, axes, rate and timing are known.
   GNSS provider follows actual receiver/protocol requirements. No camera work.

This task only explains/maps prerequisites; it does not change hardware drivers
or launch hardwared/sensord/GPS/vehicle services. Source-first inspection and
Linux sysfs reads were appropriate; no REA binary/runtime tracing was needed.

Primary local sources: `openpilot/common/hardware/base.py` and radxa/hardware.py;
`openpilot/system/hardware/hardwared.py`; `openpilot/system/sensord/` drivers;
`openpilot/selfdrive/locationd/locationd.py`; `openpilot/cereal/services.py` and
log.capnp; `openpilot/system/manager/process_config.py`. Full hashes/source pins
and host snapshots are in the optional workspace report directory
`Ai/Reports/sunnypilot-noncamera-hardware-20261101/`.
