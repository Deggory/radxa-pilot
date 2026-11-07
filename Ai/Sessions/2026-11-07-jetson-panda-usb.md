## November7 — Jetson Panda USB explanation (read-only)

QA-20261107-16 records H7 USB-A, default SPI gating, rig-specific v17/57 health
repair and cross-fork expected firmware synchronization. Four pinned076d73bf
files reread via GitHub connector; no scripts executed or hardware claim. Pattern
is relevant to host adaptation, not direct Chimera compatibility. Original Chimera
mailbox16/health43 differs. Modern Chimera remains halted; chimera_old/ preserved;
no firmware/host implementation resumed. Baseline591683739.

Sources: https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/USAGE.md ; https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/patch_panda_spi.py ; https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/panda/repair_protocol.py ; https://github.com/feiyang2025/jetson-cuda-overlay/blob/076d73bf9a2e055c83fbe9b2a3c16a8383519ba4/panda/sync_firmware.py

Source-first research only; existing pinned study reused. No firmware/tests rerun
or runtime analysis needed. Historical source findings kept separate from proof
of physical compatibility. No model/camera/DBC/source change.
