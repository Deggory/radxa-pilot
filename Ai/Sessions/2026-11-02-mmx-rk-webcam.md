# MM-X/RK3588 webcam prerequisites — 2026-11-02

Owner clarified full hardware checklist question applies to webcam mode and
requested MM-X master and RK3588 sources. Starting4bf50579fb590786ce1b0454258e0480bf83a978,
clean radxa/q8b. Read teacher/student MM-X references before fresh GitHub reads.
Applied source-driven-development and documentation/Git workflows; readable
source analysis, no REA runtime execution necessary or claimed.

Fresh branches: literal masterdb27a433fcbf5601a61aa7a03fbd5d0fa1ade036,
default master-ticib9b7f4885662f9d8a2bfc984e23bcda412399e4a,
master-rk35883ad69b20b2c38172ea24c8388354ee95eca8412a. Retained11selected
source bodies/metadata in optional workspace q8b/research/mm-x-webcam-20261102;
all11Git blob hashes match and9Python files AST-parse. No full clone/build.

RK selects Pc, empty thermal configuration, zero GPU/power, comma-only fan,
disabled physical sensord/GNSS. OS resource stats remain real. Localizer uses
carState-derived accel/yaw and skips actual sensor ingestion/accepts sensor
health; do not adopt that shortcut for physical Q8B support. Literal master
also has generic defaults but different newer registry/source layout.

Corrected earlier overbroad yes: full hardware checklist is not a prerequisite
for initial webcam demo. Current Q8B source still needs qualified camera/model/
process compatibility; OS cooling stays active. Full hardware plan is a separate
pending scope, not completed by webcam mode. No source, model, runtime, CAN or
hardware configuration changed; no camera/process/vehicle launch. No runtime
performance or safety conclusion. Save teacher/student clarification and
commit documentation with actual notebook/diff checks; no code copied.
