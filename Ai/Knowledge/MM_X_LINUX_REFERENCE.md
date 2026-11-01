# MM-X's PC/Linux approach: reference for Q8B

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
