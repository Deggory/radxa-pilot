# Post-RESET BeamNG / Chimera handoff — November 8, 2026

The bounded test is finished; physical CAN acceptance remains blocked.
400/400 genuine source samples decoded, 391 moving; game body max21.034km/h.
602 samples submitted over12s; native32.115s/3032batches/32health, zero raw
frames on each USBbus0/1/2. Independent978polls/19health also zero during301
submitted samples over6s. Both readers/gateway stopped; game AI disabled and
pause acknowledged, frozen sim time/position verified. This is pause, not a
verified zero-speed/parkingbrake state: sampled wheelspeed nonzero, parkingbrake0.
Waveshare500kstandard/silent config written, serial closed; no mode readback.

Next isolate actual Waveshare electrical TX/ACK using a known-good independent
receiver or qualified measurement, then Chimera CAN2 supply/enable/termination.
Do not infer TX from USB writes, sensor RX, or placeholder Chimera health fields.
No product/firmware/DBC/source change;76legacy entries and binary hashes match.
New firmware rewrite and upstream updates stay held. Do not resume game/control
or flash/configure Chimera automatically. See RESULTS.json and raw logs here.
