# MM-X's PC/Linux approach: reference for Q8B

## 2026-11-02 — RK camera intrinsics versus automatic mounting calibration

Owner asked how MM-X configured cameras without our checkerboard step. Inspected
the actual master-rk3588 pin3ad69b20b2c38172ea24c8388354ee95eca8412a, rather
than assuming default master-tici describes RK. Its README camera section says
to obtain intrinsics with software such as GMLCCalibration, then edit geometry
and UI constants. It does not document the author's physical target/procedure
or prove that he avoided a checkerboard.

| File at the RK pin | Observed behavior |
| --- | --- |
| common/transformations/camera.py | Road CameraConfig(1280,720,900.0); K has fx=fy=900,cx=640,cy=360; PC maps to this configuration |
| selfdrive/ui/ui.h | FCAM_INTRINSIC_MATRIX repeats the same road K for UI projection |
| tools/webcam/camera.py | CameraMJPG requests MJPG1280x720/20FPS; not an intrinsic-calibration solver |
| tools/webcam/camerad.py | Uses CameraMJPG and a20Hz publisher loop; no lens calibration performed here |
| selfdrive/locationd/calibrationd.py | Uses cameraOdometry/carState to estimate mounting pitch/yaw and other alignment/height state; roll assumed zero; does not estimate K or lens distortion |

The intrinsic class represents a centered pinhole with equal focal lengths;
these camera/geometry paths do not supply a measured distortion profile for
our AK lens. Provenance/accuracy of his focal900 is not established by these
files. His camera constants cannot be treated as measurements of our camera.

Our printable target is one supported measurement method, not a mandatory
Sunnypilot mechanism. Verified manufacturer calibration matching resolution,
crop and focus, or a suitable alternative calibration method, could supply
intrinsics. An FOV-derived K is only an estimate unless independently verified.
The saved70degree visual estimate is not promoted to measured calibration.
No selection of an alternative or activation of estimated geometry was requested.
Next resolve the AK lens-parameter source before capture/installation; the
prepared target/tool remains available if the owner chooses that route.

Sources: [RK README](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/README.md),
[geometry](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/common/transformations/camera.py),
[UI](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/selfdrive/ui/ui.h),
[online calibration](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/selfdrive/locationd/calibrationd.py).
Fresh GitHub retrieval:5 exact Git blobs,4 Python AST parses; source-only.
Optional evidence:q8b/research/mm-x-camera-20261102/verification.json in the
workspace. No REA binary analysis needed for readable source. Runtime remains
d273823b4ae08eb51cce8042eea424b9dea062d9; stock model65a08adc/current runtime
unchanged, Q8B calibration guard active, no hardware or vehicle action.

## 2026-11-02 — Webcam bring-up is a smaller scope than complete hardware support

Owner specifically asked whether the full hardware checklist must be implemented
for webcam mode, using MM-X master and RK3588 as references. Earlier blanket
yes was too broad for that scope. **No: complete board telemetry is not a
prerequisite for an initial webcam demonstration.** This is distinct from a
qualified full Q8B/vehicle integration.

Fresh GitHub branch check distinguishes literal master db27a433fcbf5601a61aa7a03fbd5d0fa1ade036,
default master-tici b9b7f4885662f9d8a2bfc984e23bcda412399e4a and
master-rk3588 3ad69b20b2c38172ea24c8388354ee95eca8412a. The default is not
literal master. Inspected11pinned full files,11Git blobs matched/9Python AST
parses; existing master-tici review remains separately pinned evidence.

| Area | What the RK3588 reference actually implements |
| --- | --- |
| Hardware selection | Non-/TICI systems use Pc; no dedicated RK thermal/fan backend in this selection |
| Temperature reporting | Pc inherits empty ThermalConfig from base |
| Power/GPU utilization | PC getters return0; these are defaults, not measurements |
| Cooling | hardwared constructs the comma fan controller only under TICI; OS cooling is a separate responsibility |
| CPU/RAM/disk | Actual psutil/free-space readings remain |
| IMU | Stock sensord disabled on PC; localizer instead derives accel from carState.aEgo and optionally gyro from carState.yawRate; physical sensor ingestion commented and sensors_valid forced true |
| GNSS | Inspected registry gates comma GNSS processes on TICI |
| Webcam | USE_WEBCAM selects tools.webcam.camerad; README asks for camera configuration/calibration and compute setup |
| Vehicle | README still requires a Panda/car connection; derived motion needs real carState data |

Literal master also retains generic PC thermal/power/GPU defaults and switches
camera services with USE_WEBCAM. Its modern manager registry still gates
sensord on not PC and comma GNSS on COMMA_HARDWARE; not the same process policy
or source layout as the older RK branch. RK README documents OpenCL/camera/UI
adaptations, not a complete Rockchip hardware-health implementation.

For an initial Q8B webcam demo, leave unsupported telemetry at current defaults,
reuse OS resource stats and preserve existing OS automatic cooling. First qualify
the camera/message/calibration contract, actual Qualcomm GPU/model backend and
selected process dependencies. USE_WEBCAM alone does not supply those changes
in current Sunnypilot. No need to port every temperature/modem/power/fan entry
before that demonstration. Full real hardware reporting can be implemented
separately. Do not copy MM-X's fabricated sensor-health acceptance or mistake
carState-derived planar observations for our known physical IMU integration.

Sources: [RK hardware](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/system/hardware/pc/hardware.py),
[RK base](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/system/hardware/base.py),
[RK registry](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/system/manager/process_config.py),
[RK localizer](https://github.com/MM-X/sunnypilot-pc/blob/3ad69b20b2c38172ea24c8388354ee95eca8412a/selfdrive/locationd/locationd.py),
[literal-master base](https://github.com/MM-X/sunnypilot-pc/blob/db27a433fcbf5601a61aa7a03fbd5d0fa1ade036/openpilot/common/hardware/base.py).
Readable source only; no build, runtime, camera, sensor or vehicle tests and no
application changes. Camera work remains unimplemented. This answer clarifies
prerequisites, not permission to launch/engage a vehicle stack.

## Non-camera hardware comparison — 2026-11-01

Owner asked what MM-X did for the hardware/sensor checklist. Rechecked the
master-tici branch through GitHub: still `b9b7f4885662f9d8a2bfc984e23bcda412399e4a`,
commit2026-08-20. Verified9 selected Git blob identities and parsed8 Python
files:5 newly fetched source files plus4 exact cached bodies from this pin.
Local project at review start:f12882e96c6388dc72dcd434a4de33955595e5b4. Camera
work remains excluded. This describes behavior in the branch, not authorship
of every line or a measured working/safe PC/Q8B deployment.

| Topic | What the inspected MM-X PC path does | Consequence for our Q8B |
| --- | --- | --- |
| CPU/GPU/RAM/PMIC temperatures | Pc inherits base get_thermal_config returning an empty ThermalConfig | No real PC/Q8B thermal-zone mapping supplied here |
| CPU/RAM/disk usage | hardwared uses psutil.cpu_percent/percpu, psutil.virtual_memory and free-disk helper | Real OS statistics, separate from chip temperature/power telemetry |
| GPU utilization | Pc.get_gpu_usage_percent returns0 | Placeholder telemetry; does not mean GPU inference itself cannot execute |
| Device/SoM power | Pc power methods return0; normal power-monitor code otherwise remains | No measured PC input-rail/SoM power implementation; zero is not calibrated0W |
| Fan/PWM | hardwared creates TiciFanController only for TICI with a peripheral present | No Q8B PWM/control-mode/tach adapter on normal PC path |
| IMU | PC localizer creates accel[aEgo,0,-9.81] and gyro[0,0,-yawRate] from carState | Derived planar observations; not our physical3-axis accel/gyro measurement |
| Sensor health | PC skips physical accel/gyro subscriptions/critical checks and sets sensor validation true | A policy shortcut, not proof actual motion sensors are healthy |
| GPS | qcomgpsd/ubloxd/pigeond enabled only for TICI | No general external-PC/Q8B GNSS provider established by this registry |
| Network/modem | Pc reports Wi-Fi, unknown signal/no network info, absent SIM and empty modem temperatures | Assumed/default state, not complete host network/modem discovery |
| Display/lifecycle | Brightness/power-save/init methods are no-ops; reboot/shutdown print messages | Does not implement Q8B backlight, power policy or real shutdown controls |
| Process selection | micd/timed/sensord/torqued/lagd and several hardware functions gated away from PC | Each disabled service's consumers/fallbacks need deliberate review |
| Audio/interface | soundd runs on ordinary PC but not RK; native UI selected and raylib UI disabled | Different branch/interface policy; not our current Python raylib adaptation |
| Vehicle interface | Existing card/pandad supplies carState/CAN; pandad disabled in FILLBACK mode | Valid speed/yaw feedback still depends on actual car/bridge, not PC identity |

Physical IMU replacement details are in his locationd.handle_log carState branch.
He also avoids physical sensor sockets on PC and treats sensor_all_checks as
true; these are substantive estimator assumptions. Our custom steering-angle
sensor does not by itself supply a measured yaw rate or complete3D motion. Our
known Adafruit LSM6DS3TR-C/I²C9/0x6a has prior raw/schema evidence; retain its
real sensor path and qualify current-source publication/mount/bias instead of
copying this shortcut. No sensor bypass or car-derived IMU was adopted.

His hardwared still exists and publishes generic device status; it does not
make every hardware reading real. Inherited empty thermal configuration and
zero methods can still produce default-looking state. Existing CPU/RAM/disk
statistics should not be described as fake merely because other fields are
placeholders. Likewise GPU-usage telemetry is separate from the chosen model
execution backend. No Rockchip/PC thermal monitoring was proven elsewhere by
this focused file review; do not infer OS-level cooling is disabled either.

Useful pattern: isolate generic Linux and board/feature-specific services.
For Q8B we still need actual thermal/power reads, deliberate fan ownership,
physical IMU publisher and supported network/display/GNSS providers as required.
No fork switch, copied patch, upstream merge, camera/GPU/model/sensor/CAN/vehicle
run or hardware configuration change was made by this study.

Primary source links:

- [PC backend](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/hardware/pc/hardware.py) and
  [base thermal configuration](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/hardware/base.py).
- [Hardware monitor and fan selection](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/hardware/hardwared.py).
- [PC IMU observations and validation](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/selfdrive/locationd/locationd.py).
- [Process and GNSS policy](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/manager/process_config.py).

Evidence: optional workspace q8b/research/mm-x-hardware-20261101 and central
Ai/Reports/mm-x-hardware-20261101. Source-only checks are not runtime integration.

Earlier study below retains the recorded local checkout state at its date.


2026-11-01. Owner asked to inspect MM-X before making changes. This is reference
research only; implementation waits for the owner's instruction. The standing
daily vendor update policy remains separate. No application code/configuration,
driver, runtime, model or OS settings were changed for this study.

## Exact source

Repository: [MM-X/sunnypilot-pc](https://github.com/MM-X/sunnypilot-pc).
GitHub's current default master-tici still points to
`b9b7f4885662f9d8a2bfc984e23bcda412399e4a`, dated 2026-08-20.
The complete tree response contains5243entries and is not truncated. Checked20
selected source bodies against their Git blob IDs; parsed13Python files without
importing or running them. Sources/evidence are retained in
[q8b research](/home/radxa/comma/q8b/research/mm-x-linux-20261101/README.md).

This branch declares openpilot0.11.2, but is not the official Sunny release or
our source snapshot. Current vendor is a86979d2; protected port is dfb86f6a atop
6f7a2c94. Different layouts, schemas, model artifacts and runtime APIs need an
explicit adaptation. The following describes behavior present in his branch;
it does not establish who originally authored every line or a full upstream diff.

## 1. Platform detection remains a generic PC route

[`system/hardware/__init__.py`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/hardware/__init__.py)
uses /TICI for comma hardware, PC = not TICI and a separate /AGNOS flag. RK is
true when the kernel release contains rockchip. SConstruct treats aarch64 with
/TICI as larch64; aarch64 without it is an explicitly supported LinuxPC target.

There is no requirement to make ordinary Linux pretend to be AGNOS. His Pc
backend still supplies assumed Wi-Fi, placeholder identity, zero power/GPU
readings and no-op power/display methods. It is not a complete hardware-health
implementation. Our current host has neither /TICI nor /AGNOS and its kernel
release is7.0.11-6-qcom, so the inspected MM-X predicates would treat it as PC,
not Rockchip. Our newer official source instead uses /AGNOS for comma selection.

**Useful:** preserve a generic Linux entry and isolate platform behavior.
**Needs our design:** real Q8B capabilities, readings and Python/C++ identity.

## 2. Model backend is selected independently of PC/comma identity

His [`selfdrive/modeld/SConscript`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/selfdrive/modeld/SConscript)
probes available Tinygrad devices in a subprocess. MODELD_TG_BACKEND can override
selection; otherwise the inspected priority is CUDA → QCOM → CL → CPU, with
CPU:LLVM on Linux. The CL branch carries Mali-specific flags. Device choices
are written into tg_input_devices.json and read by modeld/helpers at runtime
for the warp and input queue devices. Source contains USB AMD-specific handling
as a separate path. README platform claims are not independent performance tests.

The compiler creates Tinygrad JIT warp/model artifacts and adds a1280×720 camera
configuration for PC. The main modeld uses driving_supercombo; legacy split-model
modeld098 remains registered but disabled for normal manager startup. Current
official Sunny's modeld_v2 and artifact pipeline differ.

**Useful:** explicit backend/configuration selection and matching compiler/runtime
contracts, rather than treating every non-comma system as CPU-only.
**Not established:** Q8B MSM compatibility. The actual
[`ops_qcom.py`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/tinygrad_repo/tinygrad/runtime/ops_qcom.py#L342)
opens /dev/kgsl-3d0 and uses KGSL ioctls. That is not our preserved Linux MSM/DRM
Adreno runtime. A QCOM label alone is not a driver/API compatibility guarantee.
Q8B Adreno and RK3588 Mali also require different implementations/qualification.

## 3. Webcam capture and publishing are adapted

[`tools/webcam/camera.py`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/tools/webcam/camera.py)
requests1280×720/20FPS through OpenCV, leaves the180degree flip commented out,
and converts BGR to NV12. Camerad defaults ROAD_CAM to11, with optional wide and
driver devices; it publishes pixels over VisionIPC and frame metadata messages.

The example still generates SOF/EOF from frame_id×0.05seconds instead of device
acquisition time. Its compiler/model path expects get_nv12_info padding, whereas
the webcam publisher uses default create_buffers. That is a contract to inspect
and measure, not proof the layouts agree. The camera table also requires actual
intrinsics: the inspected PC default retains a1928×1208/focal2648 configuration;
1280×720/focal900 is conditional on RK and no FILLBACK. Merely compiling720p does
not calibrate a PC webcam or our Q8B camera.

Older names include roadCameraState/driverCameraState and VISION_STREAM_ROAD/
DRIVER; our newer tree uses narrowRoadCameraState/cabinCameraState and the
corresponding new stream names. Code cannot be copied without schema adaptation.

**Useful:** camera-provider-to-standard-message organization and orientation/FPS
configuration. **For Q8B:** retain measured acquisition timestamps, calibration,
frame IDs, buffer layout/lifetime and our existing capture/preparation work.

## 4. PC localization synthesizes sensor observations from vehicle data

His [`locationd.py`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/selfdrive/locationd/locationd.py#L149)
uses carState on PC to construct acceleration[aEgo,0,-9.81] and gyro[0,0,-yawRate]
observations. It retains some sanity/camera-yaw comparisons but skips physical
accelerometer/gyro sockets on PC and treats their sensor-validity checks as
satisfied. Camera-odometry time uses the message log clock on PC rather than
timestampEof. These are substantive localization assumptions, not Linux detection.

**Do not adopt as established Q8B behavior:** our required actual vehicle yaw,
acceleration, timing, axes and physical-motion coverage have not been qualified.
A CAN-derived planar approximation is not a complete3D IMU measurement. Custom
steering angle feedback also does not by itself supply vehicle yaw rate.

## 5. Process policy is changed for PC and Rockchip

His [`process_config.py`](https://github.com/MM-X/sunnypilot-pc/blob/b9b7f4885662f9d8a2bfc984e23bcda412399e4a/system/manager/process_config.py)
selects webcamerad with USE_WEBCAM; gates encoderd, microphone, sensord, torqued,
lagd and other hardware services away from PC. Dmonitoring model/policy entries
are commented out in the inspected registry, as are updated/uploader entries.
The active UI is native C++; Python raylib_ui is registered disabled.

Modeld uses CP.steerActuatorDelay+0.2 on PC when lagd is absent. These gates and
delay values change behavior; they are not a tested Q8B service or safety policy.
Our current UI is Python raylib and our pipeline needs its actual contracts.

**Useful:** explicit per-platform process selection. **Needs separate review:**
each removed service, its consumers, fallback quality, alerting and lifecycle.

## 6. Cadence claims need care

README advertises10Hz PC/RK inference. Inspected source sets DT_MDL=0.1 and
MODEL_RUN_FREQ=10 only for RK, and0.05/20 otherwise. Modeld explicitly skips
alternate frames only on RK. Effective sustained PC throughput was not measured
here; do not report universal PC10Hz or proven Q8B20Hz from these declarations.

## What to take forward when changes are requested

Use MM-X as a design reference for explicit compute-backend selection, webcam
publication and platform-specific process wiring. Keep our current official
source and real Q8B runtime/geometry contracts. Review the real IMU/localization
and model/message/UI interfaces explicitly rather than copying disabled checks,
CAN-derived observations, fixed delays, old schemas or KGSL assumptions.

No fork switch, copied implementation, install, build, camera/model/GPU/CAN test
or actuation occurred. The reference supports a proposal, not tested integration.
