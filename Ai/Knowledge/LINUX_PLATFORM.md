# AGNOS, Ubuntu/Linux and Q8B platform selection

## 2026-11-01 — Working project is sunnypilot; notebook is inside it

Owner clarified that `sunnypilot/` is the actual project and other workspace
folders are references/support. The existing radxa/q8b repository was moved
from q8b/sunnypilot-radxa into sunnypilot, preserving identity commit12e44fee,
all Git history, assets, submodule pins and IDE files. The clean upstream copy
is now q8b/sunnypilot-upstream and remains the only daily-updated checkout.
No upstream code was merged. The former project path is a compatibility link.

`Ai/` is now a real directory versioned with the project, copied from notebook
ed8afade without nested Git. The old notebook repository retains history only.
Active code, README and knowledge belong here; external references are optional
context and do not supply the new identity implementation at runtime.

See [README](../../readme_wat_we_did.md) from this Ai directory, or
[location session](../Sessions/2026-11-01-project-location.md). Earlier recorded
paths/roles below are historical and must be interpreted using their source
pins. This move does not qualify camera/model/UI/sensors or vehicle actuation.


## 2026-11-01 — Q8B identity implemented and checked

Owner authorized Ubuntu/Linux, ARM64 and Radxa Dragon Q8B identification.
Protected `radxa/q8b` commit `12e44feeff241334e184c86dc9daccdc7f9e4fa1` implements exact device-tree detection,
Python/C++ HardwareRadxa and local cereal enum `radxaQ8b @8`, preserving existing
ordinals and generic Linux `aarch64`, `COMMA_HARDWARE=False`, `PC=True` policy.
The read-only command reports actual Ubuntu24.04.5/ARM64/RadxaDragonQ8B. Dynamic
camera consumers explicitly reject missing Radxa calibration. No comma camera
calibration is claimed for this board.

11 Python tests, 4 actual C++→Python deviceState/initData message checks, SCons
profile detection, Ruff, syntax and diff checks passed. A detection mutation
was rejected by the tests. No full Sunnypilot build, camera/model/UI launch,
MSM runtime integration, hardware-health measurement or vehicle actuation was
performed. Generic hardware defaults remain unimplemented health providers.
Vendor stays clean at a86979d2; no upstream merge/push.

[What we did](/home/radxa/comma/q8b/sunnypilot-radxa/readme_wat_we_did.md) ·
[Evidence](/home/radxa/comma/Ai/Reports/radxa-board-identity-20261101/REPORT.md).

Earlier source-only explanations below retain their original scope and pins.

2026-11-01 explanation requested before implementation. Vendor source
`a86979d2b2b176413a7f3e5cccf8c807596a7def`; protected port
`dfb86f6a9b5161f323abc6312f1462fb946d39d8`. No application, build configuration,
environment or OS setting was changed. Memory updates only.

## AGNOS is a Linux distribution

Comma's official [agnos-builder README](https://github.com/commaai/agnos-builder)
describes AGNOS as its Ubuntu-based OS for comma 3X and comma four. Linux support
and comma hardware support are separate questions. Our board can use Ubuntu
while requiring different camera, GPU, sensor, power and display integrations.

Read-only host observations in this session:

- `/etc/os-release`: Ubuntu24.04.5LTS, versionID24.04, Noble.
- `uname -srm`: Linux7.0.11-6-qcom, aarch64.
- `/AGNOS`: absent.

These describe the current host, not the result of running Sunnypilot.

## This checkout already detects the generic Linux platform

[`openpilot/common/hardware/__init__.py`](/home/radxa/comma/sunnypilot/openpilot/common/hardware/__init__.py)
uses the presence of `/AGNOS` to set AGNOS/COMMA_HARDWARE; PC is its inverse.
Without that marker, Python selects HardwarePc. Here PC means the generic
non-comma platform; it includes ARM64 Linux boards, not only desktop x86 PCs.

[`SConstruct`](/home/radxa/comma/sunnypilot/SConstruct) reads uname and OS, selecting
comma_arm64 only for aarch64 plus /AGNOS. Otherwise aarch64 is explicitly accepted
as Linux PC ARM64. The C++ hardware selection follows the build's comma flag.
The launch script also guards comma-specific initialization with /AGNOS.
There is no need to set a new “Linux=true” flag just to identify this host.

Do not create `/AGNOS` to make Q8B inference use the comma path: that also selects
the comma board's GPIO/KGSL/power/modem/update assumptions. There is no existing
RADXA=1 switch that completes the port.

## What remains to implement, when requested

1. Keep generic Linux/ARM64 as the initial development platform and complete
   the protected-port dependency/model/message contract preflight.
2. Design explicit Q8B hardware capabilities/implementation in the protected
   clone. Resolve Python/C++ identity and cereal/camera lookup implications;
   provide real thermal/power/display/sensor behavior instead of base stubs.
3. Connect actual camera/VisionIPC timing/layout and the chosen MSM/Adreno
   model backend. USE_WEBCAM only selects a camera service. Stock non-comma
   model compilation uses CPU:LLVM, and Sunny modeld_v2 selects CPU outside
   comma hardware; OS detection alone does not activate our existing GPU work.
4. Qualify actual sensors, native UI and process lifecycle with bounded tests.

HardwarePc inherits defaults/no-op methods for many hardware operations.
Selecting it proves platform selection, not a functioning or thermally qualified
Q8B integration. An eventual Q8B backend should not blindly turn off meaningful
health/startup checks or impersonate comma hardware. No implementation was
approved or performed in this explanation task.

## Follow-up: why detection exists, and what happens if it is unchanged

The selector routes hardware behavior; it is not simply a Linux/not-Linux test.
Comma and our board both run Linux, but their device nodes, camera interfaces,
GPIO, display/power controls and compute runtimes differ. PC is the generic
non-comma route. Changing its name or predicate does not implement those drivers.

In MM-X's b9b7f488 reference, RK is an extra Rockchip predicate within this
platform scheme. It selects10Hz model scheduling, alternate-frame skipping,
conditional camera geometry and service policy. Those are Rockchip-specific
choices, not required Linux support. Q8B's inspected kernel containsqcom rather
thanrockchip; leavingRKfalse is consistent with that observation. Do not force
the RK path to make a Qualcomm board appear supported.

For our a86979d2 vendor/dfb86f6a protected source, leaving detection unchanged:

| Area | Source-selected behavior |
| --- | --- |
| OS/build target | Generic Linux/aarch64 remains recognized; this is not proof all build dependencies are available |
| Hardware abstraction | HardwarePc remains selected without /AGNOS |
| Model compute | Stock Linux model build selectsCPU:LLVM; Sunny modeld_v2 explicitly choosesCPU off comma, pending our runtime integration |
| Camera | Native camerad remains the default; USE_WEBCAM selects the example publisher, not our existing measured Q8B capture/preparation integration |
| Motion/GNSS services | sensord and comma-specific GNSS/modem entries are gated off by PC/comma conditions; actual Q8B providers remain to be connected |
| Device health | Generic base defaults/no-op methods do not supply qualified Q8B power/thermal/display control |

Therefore no detection change is needed now. Keeping this selection permits
Linux development but does not complete the managed Q8B camera/model/sensor/UI
pipeline. Later, an explicit Q8B implementation/capability design can provide
real interfaces and compute choice without impersonating comma or Rockchip.
No application or OS changes were made for this follow-up.

## Follow-up: explicitly identify this board as Radxa Q8B

Read-only Linux device-tree identity observed2026-11-01:

```text
/sys/firmware/devicetree/base/model       = Radxa Dragon Q8B
/sys/firmware/devicetree/base/compatible  = radxa,dragon-q8b; qcom,sc8280xp
```

The files contain NUL-terminated strings; compatible is a list of exact tokens.
This provides a concrete automatic board detector without inventing a marker
file or inferring board identity from the Linux kernel name alone.

Proposed, not implemented: recognize the radxa,dragon-q8b compatible token,
select an explicit HardwareRadxa/Q8B implementation, and retain the existing
Linux/aarch64 build target and COMMA_HARDWARE=False. An internal Q8B capability
flag can initially coexist with the generic PC classification; do not globally
set PC=False just to change the displayed board name, since existing consumers
also use it to gate services, paths and hardware operations.

If deviceState/route logs are to publish a new radxaQ8b device type, the current
InitData.DeviceType enum in cereal/log.capnp has no such value. Extend schema,
Python/C++ hardware identity and relevant camera lookup/consumers consistently.
Simply returning an unregistered string from get_device_type is insufficient.
The current C++ HardwarePC returns the PC enum, and DEVICE_CAMERAS contains PC/
comma keys; both are part of the identity contract. New schema numbering and
actual calibration/capability design remain decisions for implementation.

Identification can be a first small change when requested; it does not by
itself implement camera, MSM/Adreno, sensor or health support. Owner asked a
conditional follow-up, not to apply changes. App/source/OS remain unchanged.

Plain-language clarification of the three proposed jobs:

1. Recognition: read Linux's existing board label to answer “which board am I
   on?” Ubuntu is the OS, ARM64 is the CPU architecture, Radxa Q8B is the board.
2. Hardware implementation: a HardwareRadxa object would translate general
   requests such as “read temperature” into the correct Q8B interfaces. Creating
   or selecting the class does not supply working drivers by itself; unsupported
   capabilities must remain explicit until implemented and tested.
3. Shared identity: message formats and Python/C++ code must agree on the new
   board name. Camera lookups must accept that identity and use the actual
   calibrated camera configuration. This is compatibility work, not automatically
   enabling a camera or inventing calibration from the board name.

This explanation is about the proposal's meaning; implementation remains held.
