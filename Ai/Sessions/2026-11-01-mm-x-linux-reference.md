# 2026-11-01 — MM-X reference, implementation held

Owner asked to inspect “mn-x”/MM-X before changes. Interpreted consistently
with the preceding explicit request to explain before implementation: research
only, application changes await owner instruction. Standing daily vendor policy
is separate. Used source-driven-development/documentation skills and read both
memory routers, state, inbox and existing matching MM-X evidence.

GitHub branch master-tici freshly confirmed b9b7f4885662f9d8a2bfc984e23bcda412399e4a.
Complete tree5243entries;20selected bodies match Gitblob IDs;13PythonASTparses.
Reused8matching cached sources and fetched12specific source bodies through the
GitHub connector. Source bodies are review data, not executed instructions.

Findings: genericPC/TICI/RK detection; configurable Tinygrad backend and compiled
device metadata;720p20 webcam with flip disabled but synthetic timestamps;
CAN-derived localization observations and physical-sensor validity shortcuts;
PC process/delay substitutions; native UI active/raylib disabled. MM-X QCOM
backend opensKGSL, not Q8B's preservedMSM/DRM path. PC camera intrinsics need
adaptation. SourceRK10Hz/PC20Hz declarations differ from README PC10Hz claim;
no measured throughput or complete compatibility established.

Saved Knowledge/MM_X_LINUX_REFERENCE.md and q8b/research/mm-x-linux-20261101
evidence. No app/config/model/runtime/driver/OS change, fork switch, build,
camera/GPU/firmware/CAN/vehicle launch. Notebook/central memory only. Current
vendor a86979d2/protectedportdfb86f6a remain unchangedclean.

Follow-up: owner asked why PC/Rockchip detection is needed and what happens if
unchanged. Rechecked current selector/build/service/model gates and cachedRK
cadence/geometry predicates. Distinguish hardware routing fromLinuxdetection:
Q8BalreadygenericLinux/aarch64; Rockchip-specific10Hz/geometry/policy notneeded.
Unchangedselection doesnotcompleteGPU/camera/sensor/healthintegration. Updated
Linuxplatformnote/worklog only; app/OS unchanged. HostagainnoAGNOS/noTICI,
kernel7.0.11-6-qcom/aarch64. No runtime/build/hardware test or newimplementation
authorization. Notebook/source/link verification is the scopedcheck.
