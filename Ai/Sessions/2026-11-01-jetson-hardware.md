# Jetson teacher hardware review — 2026-11-01

Owner asked what the Jetson people did, explicitly referring to teacher memory.
Read central jetson-cuda-overlay/dp-agx-orin notes and retained platform/sensor
reports first. Starting current0205e38bf44014c6b57b5508352d924e26d041c8/radxa/q8b,
clean, Sunny2026.003.000/COMMA0.11.3. Cameras remain deferred. No branch/runtime
switch or implementation authorized by this reference lookup.

Reviewed pinned Deggory/dp_agx_orin d0c3a6e3e890ee9162109f7d932eca116f903289 and
feiyang2025/jetson-cuda-overlay076d73bf9a2e055c83fbe9b2a3c16a8383519ba4.
Fresh read-only GitHub fetches6source identities,4full Git blob checks/3Python
AST parses plus2selected ranges. No full checkout/mirror/source-body retention.
Used source-driven-development/code-review-and-quality workflows, reused actual
retained REA evidence rather than rerunning foreign code or hardware probes.
Verified19overlay/24DP retained files and result hashes against REA exit0/
quiesced receipts; prior48/55offline assertions remain historical scoped evidence,
including old camera-helper assertions, not new hardware qualification.

Saved student Knowledge/JETSON_HARDWARE_REFERENCE, links/current handoff/worklog
and this session; promoted facts to teacher. Dedicated DP Jetson class discovers
thermal/INA paths, reads GPU load, drives PWM and has NVIDIA power-mode code;
GPS/IMU still TICI-only and display setters incomplete. Overlay offers CH347/
LSM6DS3 Cereal publisher with documented calibration/freshness issues. Q8B uses
known native I²C9/LSM6DS3TR-C and its own thermal/power/PWM paths, not those
NVIDIA paths/modes/calibration. Canonical CAN policy unchanged, no physical
activity, installer or service launch. Next candidate still real read-only
thermal provider/tests; no camera/model work.

Documentation verification: `python3 Ai/verify_memory.py --workspace /home/radxa/comma`
passed33documents/73relative links/eight repository pins/4252indexentries;
standalone notebook-copy and git diff --check passed. Source identity/fullblob/
AST readback and frozen REA receipt integrity are recorded separately. No
application/build source change, new runtime test or hardware action occurred.
