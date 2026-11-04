# 2026-11-04 — Explain dzid/ZSS DBC roles

Owner question only. Confirmed SSC0x22E5/0x22F8 layouts match retained dzid
source782676bc, but additive checksum differs from canonical CRC and current
Sunnypilot profile does not implement SSC actuation. Updated ZSSv0.2 uses
0x506 matching encoder/DBC; fresh schema script passes, original smartZSS0x23
is different. DBC/code unchanged, calibration and live integration unqualified.
No selection/flash/actuation or remote push. [Details](../Knowledge/RETROPILOT_CAR_PORT.md).
