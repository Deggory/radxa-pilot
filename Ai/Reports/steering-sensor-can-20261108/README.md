# Steering sensor / original Chimera CAN observation — November 8, 2026

Owner connected a steering-angle sensor and requested CAN3 output observation.
Initially only a different Interceptor DAC Bench enumerated; it was not probed
with the Chimera protocol. Owner confirmed Radxa connection, then reconnected
Chimera USB. The exact original serial/version returned and capture ran.

Native receive-only observation: **20.114 s, 1,886 CAN batches, 20 health replies,
zero raw CAN frames on each USB bus 0/1/2**, normal exit and reader stopped.
MCU CAN3 = printed CAN2 = USB bus2. No raw ID filter; no Toyota0x25 frame or any
other frame observed. The saved teacher Toyota89245-0K020 reference is not a
fresh confirmation of this installed sensor model. No angle decoding possible.

Owner says sensor power comes from Chimera IGN. That connector pin previously
measured0V, so verify voltage at the connected sensor before treating this as a
powered-sensor test. If still0V, the sensor lacks its intended supply and cannot
transmit. No new meter reading, external power, wiring change or firmware fix
was performed. Correctly rated sensor supply/pinout must be verified before a
power change. Previous CAN voltage/standby/termination unknowns remain.

Owner describes direct USB reconnect, but fresh sysfs still places Chimera at
3-4.1 behind VIA2109:2812hub3-4. Reconnect restored discovery; hub bypass is not
established. Initial USB absence is superseded by successful current capture.

Baseline4d689db69985326b44e5402a7c586efd37bd40ad; native SHA256
`e9e692b6bfaf67d4c9061f4645a89d8337fc938bd857cf03e03f6a3454f81a84`.
All76legacy manifest hashes match. Product/firmware/DBC/model unchanged; no
Interceptor/MCU OUT/config/relay/heartbeat/reset/flash, simulator/Waveshare
transmission, drive, upstream update or push. Source-first debugging and saved
native runtime evidence used; no unrelated binary analysis/build performed.

RESULTS.json is portable; central same-named report additionally holds raw
capture/helper/log/USB/watch evidence and final validation receipt. The capture
completed; sensor CAN acceptance remains blocked by zero observed frames and
unverified sensor power. Next measure sensor IGN-to-sensor-GND supply, qualify
power/wiring, then repeat receive-only capture under an explicitly powered setup.
