# Non-camera hardware and sensor map

Inspected 2026-11-01 at source5bcc0028c494e248e5d77f7f0cbea8877407415c,
branchradxa/q8b, headersSunny2026.003.000/COMMA0.11.3. Owner selected hardware
work and explicitly deferred cameras. This is a source/read-only host inventory,
not an implemented sensor adapter or a qualified running stack.

## Known IMU recovered from teacher memory — 2026-11-01 correction

Teacher [IMU record](/home/radxa/comma/Ai/Knowledge/Repos/imu.md) and retained
`imu/README.md`, `imu/SUNNYPILOT_IMU_TEST.md` and capture reports establish:

| Item | Recorded hardware/evidence |
| --- | --- |
| Module | Adafruit LSM6DS3TR-C six-axis IMU: accelerometer, gyroscope and temperature |
| Connection | Q8B I²C9, `/dev/i2c-9`, address `0x6a`; prior WHO_AM_I=`0x6a` |
| Wiring | VIN→header1, GND→6, SDA→3, SCL→5; four wires, no interrupt wire recorded |
| Bus setting | Prior live device-tree check:400kHz |
| Prior rate test |2026-10-16 uncapped fresh reads:3120 over30.555s,102.08Hz observed, maximum gap32.93ms |
| Prior message test |520 live samples/1040 in-memory Cereal round trips at102.26Hz; maximum message-creation age7.26ms |
| Integration limit |Tests used old sourcea5f44653; no IPC delivery, managed sensord/locationd acceptance or rigid-mount/vehicle-axis calibration demonstrated |

The standalone reader uses raw userspace I²C. No exposed IIO accel/gyro channel
is therefore consistent with this known sensor; the earlier IIO-only inventory
was insufficient to ask the owner for its model. This task also observes
`/dev/i2c-9` exists, but does not open it or repeat a live chip-ID/sample test.
The historical loose-board gyro bias and37.3° gravity tilt must not be applied
as installed vehicle calibration. Teacher evidence is the starting point for
current-source integration, not proof the newer runtime is already integrated.

The teacher's [GPS record](/home/radxa/comma/Ai/Knowledge/Repos/gps.md) says
receiver candidates were researched but none purchased/connected/tested in that
record. Do not infer GNSS from the CH341 USB Serial adapter. No buying advice
or new hardware absence/presence claim is made in this correction.

Owner reaffirmed: search teacher notes/reports before asking for project facts;
ask only about remaining missing/conflicting/stale details. These recovered
facts are copied into student knowledge so it can retain the hardware context.

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

1. Use the known Adafruit LSM6DS3TR-C/I²C9/address0x6a and existing raw reader
   reports as the starting point; search teacher evidence before asking. Recheck
   transport/current-source compatibility in a bounded scope. Do not substitute
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

## Complete non-camera hardware checklist — 2026-11-01

Source snapshot:a80afa88ea5ed141684c2e8a83901c042a99322a, application12e44fee.
This lists inputs, outputs and diagnostics across the current hardware API,
active schema and service consumers. **Not every field is mandatory on every
board/car.** Unsupported/absent and measured-zero are different facts. PWM is
an output, fan RPM is feedback, and battery capacity/energy may be estimates.

| Area | Readings / controls / state | Scope |
| --- | --- | --- |
| CPU thermals | Per-core CPU temperatures | Q8B health provider needed |
| GPU thermals | GPU temperature channels | Q8B health provider needed |
| Other thermals | RAM/memory, DSP and power-management chip temperatures | Use actual board zones; avoid inventing equivalent sensor locations |
| Board-specific thermals | Intake, exhaust, GNSS receiver, bottom-SoC and modem temperatures | Optional/layout-specific; current comma schema fields do not prove Q8B has each sensor |
| Cooling output | Desired fan percentage, actual board fan/PWM command and control mode | A PWM interface is exposed; correct controller/ownership still needed |
| Cooling feedback | Fan RPM/tachometer, cooling fault detection where supported | peripheralState supports RPM; no Q8B tach feedback established |
| Electrical input | Input voltage/current, power consumption, supply presence | Map actual power domains and units; USB/adapter/car supply are distinct |
| Compute power | Whole-device and SoM power reports, offroad energy use | Whole-board/SoM must be verified; energy/capacity reporting includes estimates |
| Vehicle power | Vehicle battery voltage, ignition from bridge/CAN, offroad battery-capacity/shutdown policy | Comes from the correct vehicle interface; never infer ignition from USB online |
| Compute load | Per-core CPU load, GPU utilization, RAM usage | Existing Linux/common paths plus Q8B-specific GPU telemetry |
| Storage | Available disk space and recording/storage readiness | Software/OS checks; current nvmeTempC field is deprecated, not a mandatory active DeviceState input |
| IMU acceleration | Three-axis acceleration in m/s², timestamp/source/validity | Known Adafruit LSM6DS3TR-C on I²C9/0x6a; service nominal104Hz |
| IMU rotation | Three-axis angular velocity in rad/s, timestamp/source/validity | Same IMU, nominal104Hz; mounting/gyro bias/current managed delivery still unqualified |
| IMU diagnostic | Sensor-chip temperature | Separate from CPU thermals; nominal2Hz temperatureSensor |
| Position/GNSS | Latitude/longitude/altitude, speed/course, fix, accuracy, satellites and receiver time | gpsLocation nominal1Hz or external nominal10Hz; no purchased/tested receiver in the last teacher record |
| Clocking/health | Monotonic sample/message time, wall-clock/UTC where needed, uptime, freshness/rate/validity | Must validate real timestamps; no synthetic timing to hide missing/stale data |
| Network | Connected transport (Wi-Fi/Ethernet/cellular), signal, metering, connection/operator state, data counters | Optional cellular fields only if a modem is actually used |
| Display/input | Screen brightness read/set, display on/off; host UI input/touch | Match actual Q8B display/input, not comma backlight sysfs paths |
| Audio output | Speaker/audio-device playback, alert volume and fault/availability | Actual alert output must be integrated/tested; no camera dependency assumed |
| Audio input | Microphone/raw audio and ambient sound-pressure estimate for adaptive alert volume | Existing micd/soundd consumer; depends on enabled feature/audio hardware |
| Identity/lifecycle | Board/device ID, OS version, serial/init metadata, boot readiness, initialization, power-save, shutdown/reboot/reset behavior | Identity implemented; real platform operations remain separate; IMEI/SIM/eSIM only for applicable cellular hardware |
| USB/peripherals | Attached devices, connection/link speed/errors and optional accessory state | Chestnut-specific GPU/USB/power/thermal contract only if that accessory is used |
| CAN/bridge health | Connection, firmware/type, CAN RX/TX health, counters/errors, heartbeat, ignition, safety checks/controls state | Vehicle-interface boundary, not HardwareRadxa temperature/IMU methods |
| Vehicle motion/steering | Ego/wheel speed, standstill, steering angle, optional steering rate and yaw rate, relevant driver/EPS torque, driver override and steering faults | Exact signals depend on selected car/actuator design; native CAN torque units are not automatically Nm |
| Vehicle controls/state | Accelerator/brake/regen/parking brake where used, gear, cruise/buttons, blinkers, doors/seatbelt | Required/optional behavior determined by actual car interface, not a new generic retrofit protocol |
| Conditional ADAS | Radar/object tracks, blindspot and OEM safety/assist status | Only for applicable enabled longitudinal/OEM features; not universally required for the selected lateral focus |

Magnetometer, barometer, proximity and light variants occur in broad historical
sensor schema, but current sensord creates accel/gyro/temp only. Do not buy or
emulate every old schema sensor. Camera/IR hardware and its driver monitoring
are intentionally deferred under current owner scope. GPU/NPU model execution
is a separate compute-backend integration, not supplied by temperature/load
readings or board identity.

Relevant ownership split: HardwareRadxa handles board/platform methods;
sensord/provider publishes IMU; a GNSS provider publishes position; common OS
code supplies resource statistics; audio/UI manage user I/O; vehicle/bridge
services supply CAN/vehicle/actuator feedback. Some requests only occur when
the feature/process is enabled, and some values are computed rather than sensed.

Q8B evidence already available: named thermal zones, power monitors and PWM
interface, plus the existing raw-I²C Adafruit IMU. These are not all connected
to current managed Sunnypilot yet. Planned first bounded change stays real
read-only thermal reporting, then explicit power mapping and the actual IMU
provider. Existing teacher raw/schema IMU tests are historical proof, not new
IPC/locationd acceptance. No camera or vehicle action is included.

Primary current sources: common/hardware/base.py, base.h and comma/hardware.py;
cereal/log.capnp DeviceState/PandaState/PeripheralState/UsbState and services.py;
system/hardware/hardwared.py, micd.py; selfdrive/ui/soundd.py and ui_state.py;
opendbc_repo/opendbc/car/car.capnp. Canonical RetroPilot DBC policy remains
unchanged; this checklist is not proof of any physical bus/protocol compatibility.


MM-X follow-up: the [non-camera comparison](MM_X_LINUX_REFERENCE.md) shows
empty PC thermal config, zero power/GPU usage, TICI-only fan control and
carState-derived IMU observations. Real OS CPU/RAM/disk statistics remain.
These are reference policies, not Q8B sensor/health implementations; none copied.


Jetson follow-up: [teacher-derived hardware comparison](JETSON_HARDWARE_REFERENCE.md)
separates DragonPilot's actual thermal/INA-power/GPU/fan backend from Feiyang's
external LSM6DS3/CH347 publisher overlay. Keep Q8B's own providers/native I²C9;
no NVIDIA profile, calibration constants or sensor shortcut copied.

## 2026-11-02 — Available temperature channels, read-only inventory

Fresh inventory confirms55readable thermal zones and58hwmon temperature
attributes;55hwmon names mirror thermal-zone names. Additional hwmon readings:
NVMe Composite and smb2351_0_temp/smb2351_1_temp. This is channel availability,
not58independent physical sensors or qualified physical placements.
CPU0..7 each have2channels pluscluster0/1(18total); gpuss0..7(8); mem0/1(2);
aoss0..3(4); nsp0 channels0..2(3); smss0/1(2); camss0/1(2); pcie0/1(2);
audio/video(1each); PMIC-labelled pm8280-1/-2,pmc8280c,pmr735a(4); smb2351(1);
eeprom,led,vbat(1each); top-left/top-right/left-edge/left-edge-2(4).
Current UI shows hottest readable CPU/cluster and GPU values only. Other
channels are readable but not added to UI/hardwared. Do not equate mem-labelled
SoC channels with measured RAM-die temperature, CAMSS with the USB-camera
sensor, or VBAT with car-battery temperature without board mapping evidence.
Snapshot values change with workload and were read sequentially. No thermal
stress test, new model/UI run, PWM write or application change performed.
Sourcece7b047; raw snapshot: central ui-telemetry report/temperature-inventory.json.
Git/source-first workflow used; REA binary analysis not applicable.
