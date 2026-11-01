# Complete non-camera hardware checklist — 2026-11-01

Owner requested all sensors and other things Sunnypilot asks for beyond CPU/GPU
temperature, PWM, IMU and GPS. Startinga80afa88ea5ed141684c2e8a83901c042a99322a,
radxa/q8b clean. Read teacher first: known Adafruit LSM6DS3TR-C/I²C9/0x6a and
prior raw/schema proof; GNSS candidate research only. Current source headers
Sunny2026.003.000/COMMA0.11.3; no upstream integration.

Used source-driven-development/documentation-and-adrs skills to inspect Python/
C++ hardware APIs, DeviceState/Panda/Peripheral/USB schemas, current car schema,
hardwared, micd/soundd, UI brightness/power and service definitions. Added a
full checklist to Knowledge/NONCAMERA_HARDWARE, updated HANDOFF/WORKLOG. Fields
are grouped as real readings, controls, computed estimates or optional/car-
specific data. Do not imply all require physical sensors or new purchases.
Deprecated NVMe/battery schema fields are not mandatory current inputs. Camera
work remains deferred. Canonical CAN policy unchanged; no bus/port/hardware
reads/writes, no services/tests on physical devices, no application changes.

REA artifact/runtime analysis not applicable to readable source/schema checklist;
no such validation claimed. Validate notebook links/index/diff and saved source
hashes; prior sensor/runtime tests remain their dated evidence, not rerun.
Next implementation candidate stays read-only thermal mapping with real fault
tests, followed by explicit power-domain mapping and current IMU integration.

Documentation verification passed:30documents/68relative links,
workspace index/eight repository pins, standalone notebook copy,10source hash
readbacks and git diff --check. Application/build source unchanged. No new
hardware/managed runtime tests were run or claimed.
