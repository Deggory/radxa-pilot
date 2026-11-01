# 2026-11-01 — Explain Linux platform selection before changes

Owner asked how to tell the Sunny checkout that Q8B runs Linux rather than
AGNOS, explicitly requesting explanation before changes. Used source-driven
development and documentation skills; read both routers, current state and
inbox. Existing historical02bf09e8 failed snapshot check remains corrected by
bdc0dfbf; no new pending related upstream commits were found.

Host read-only results: Ubuntu24.04.5LTS/Noble; Linux7.0.11-6-qcom/aarch64;
/AGNOS absent. Current vendor a86979d2, protected portdfb86f6a. Inspected Python
selector/HardwarePc/base/Paths, SConstruct architecture selection, launch guard,
manager service gating and stock/Sunny model backend selection. Official
commaai/agnos-builder README confirms AGNOS is Ubuntu-based.

Result: no flag or source edit is required to identify generic Linux/ARM64.
Without /AGNOS the code already chooses PC/HardwarePc; PC includes aarch64.
Q8B hardware readings/camera/model backend still need explicit integration.
Do not impersonate AGNOS or assume USE_WEBCAM enables the MSM runtime.
Saved Knowledge/LINUX_PLATFORM.md; proposed steps are not implementation approval.

Checks: source/platform predicates inspected without importing manager/hardware
modules; documentation links checked and source checkout states retained. No
build/runtime/camera/model/GPU/firmware/CAN/vehicle launch, environment change,
application patch or OS operation. Only notebook/central memory records changed.

Follow-up: owner asked conditionally how Sunny could know this is a Radxa board.
Read device-tree modelRadxaDragonQ8B and compatible tokensradxa,dragon-q8b/
qcom,sc8280xp. CurrentInitData.DeviceType has noRadxa, DeviceState uses thatenum;
C++HardwarePC returnsPC andcamera lookuphasPC/comma keys. Proposed detector +
explicit Q8B hardware identity/capability layer, retainingLinux/aarch64 and
non-comma classification; update sharedidentitycontract ifpublishingnewenum.
Do notsimplyreturnunknownstring orflipPCfalse globally. No app/config/OS change
or implementationapproval; only source/hostinspection andmemorydocumentation.

Ownerthenaskedthemeaningofthreesteps. Clarifiedrecognitionversushardwaremethod
implementationversussharedidentity/schema/cameralookup. No newdesignapproval,
source/runtime/OS changes orhardwarequalification; memoryexplanationonly.
