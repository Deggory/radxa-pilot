# Non-camera hardware and sensor assessment — 2026-11-01

Owner requested hardware/sensor details and explicitly deferred cameras.
Starting source5bcc0028c494e248e5d77f7f0cbea8877407415c/radxa/q8b, clean;
identity application12e44fee unchanged; sourceSunny2026.003.000/COMMA0.11.3.
Read source-driven-development/planning-and-task-breakdown skills and existing
source notes, hardware interfaces, sensord drivers, message schemas/rates,
locationd/selfdrived consumers and manager gates. Used readonly Linux sysfs and
serial product/driver metadata; no serial ports/buses/services opened or started.

Created Knowledge/NONCAMERA_HARDWARE.md and updated current handoff/state/tasks,
router/decision/worklog/README. Motion IMU is a sensord provider, separate from
HardwareRadxa health methods. Source nominal accel/gyro104Hz, sensor temp2Hz;
GPS services1/10Hz. Pose estimator expects accel/gyro with valid timing and
calibration/model odometry; GPS does not substitute for IMU. PC=True gates off
stock comma sensord, whose I²C1/GPIO0:84 wiring is not a Radxa adapter.

Read-only inventory:55 thermal zones,2 IIO devices (PMIC ADC and voltage divider)
with no motion channels, hwmon system_power/typec/adp12v/PWM interfaces. No GNSS
node; CH341 USB Serial is unidentified as GNSS/IMU and was not opened. No absence
claim about physical/unbound sensors. Power domains/calibration/units remain
unqualified; no fan writes or fake health. Vehicle feedback/CAN remains separate
and canonical RetroPilot DBC unchanged. Owner was asked actual IMU model/interface
asynchronously; answer pending at this checkpoint.

REA artifact/binary tracing was not applicable to readable source/sysfs checks;
no such validation is claimed. Source hashes/host raw/summary snapshots are in
central Ai/Reports/sunnypilot-noncamera-hardware-20261101. No runtime tests
performed; validate documentation links/index/diff, then commit/document outcome.
Next candidate read-only Q8B thermal mapping/tests, then power and actual IMU;
cameras/model work deferred. Update teacher resume as well as student HANDOFF.

Validation completed: `python3 Ai/verify_memory.py --workspace /home/radxa/comma`
passed29documents/67relative links/236optional external links/eight source
repositories/4252 indexed entries. Standalone copied-notebook check passed.
All13 recorded source hashes match readback; application/build source unchanged.
`git diff --check` passed. These verify documentation/evidence integrity, not
working sensor/GNSS/fan integration. Host snapshots are read-only observations.

## Teacher-memory correction — owner steering during this task

Owner said consult teacher first and only ask if details cannot be found. Found
Ai/Knowledge/Repos/imu.md, retained reader/README, schema smoke JSON and dated
capture reports:Adafruit LSM6DS3TR-C on I²C9/0x6a, physical1VIN/6GND/3SDA/5SCL,
400kHz prior bus,102.08Hz raw/3120samples and102.26Hz/520samples/1040 in-memory
schema round trips. These were2026-10-16/a5f44653 tests, not a new managed test.
Mount/offset/FIFO/current-source IPC/locationd remain unqualified. Known raw-I²C
path explains absent IIO motion channels; /dev/i2c-9 exists today, not opened.
GPS teacher record has unpurchased/untested candidates, no confirmed receiver.

Initial model-pending handoff/question was incomplete because teacher lookup
was missed. Recorded factual cross-check failure againstb62481cc separately from
its passing document-link checks; preserve history. Corrected current map,
HANDOFF/state/tasks/router/README/questions and both agent-rule layers. New
standing rule: search teacher/reports/read-only sources before asking; ask only
about a remaining material gap/conflict/stale detail. No hardware changes or
new runtime integration tests. Source/report hashes recorded in
teacher-hardware-recovery.json. Camera scope stays deferred.

Corrected verification: documentation links/layout/index and standalone copy
passed; preserved raw JSON cross-check matches520samples/1040roundtrips at
102.2621Hz. Thirteen current-source hashes unchanged. This is evidence readback,
not new live hardware/managed runtime tests. Teacher-first correction resolves
the IMU-model question; future questions are reserved for actual remaining gaps.
