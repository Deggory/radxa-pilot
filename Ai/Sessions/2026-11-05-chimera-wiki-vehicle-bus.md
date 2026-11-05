# Chimera wiki vehicle bus — November 5, 2026 UTC

Owner asked which bus the wiki connects the car OBD/CAN to. Rechecked official
Chimera page: Installation lines103–110 explicitly identifies CAN2 for car CANH/
CANL. This is hostbus2/MCUCAN3 in the already-reviewed local source. The page’s
OBD-C port is for comma devices; no car-side OBD pinout or vehicle compatibility
established. Saved synchronized QA-20261105-10 and topic/state/handoff records.
Parent before0f045d5b914233c4d7a102f597331760118fa93d,child150f9371 unchanged;
Ocelot reference d87892fa/pre-existing dirty source preserved. Source/documentation/
Git workflows reused,no new REA artifact analysis needed. No source change,wiring,
USB/CAN action,firmware/config write or push. Upstream updates remain paused;
next confirm actual board label and physical receive path. Documentation link/
layout,QA equality and whitespace validation recorded with local commit.

Source: https://wiki.retropilot.org/index/hardware/chimera (Installation and Ports).
