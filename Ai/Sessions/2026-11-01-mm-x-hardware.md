# MM-X non-camera hardware comparison — 2026-11-01

Owner asked what MM-X did for the hardware checklist. Teacher-first context:
existing MM-X repo note and student Linux-reference study, plus known Q8B IMU
and hardware map. Local sourcef12882e96c6388dc72dcd434a4de33955595e5b4/radxa/q8b
clean; sourceheadersSunny2026.003.000/COMMA0.11.3, identity12e44fee unchanged.
GitHub branch master-tici freshly rechecked at
b9b7f4885662f9d8a2bfc984e23bcda412399e4a,2026-08-20. Used GitHub plugin read-only
fetch,5 new selected files and4 exact cached bodies;9 Gitblob matches/8 Python
AST parses. Nothing imported/executed from the external repository.

Findings in Knowledge/MM_X_LINUX_REFERENCE: PC empty thermal config; zero
power/GPU-utilization placeholders; fan and GNSS initialization gated to TICI;
actual OS CPU/RAM/disk stats; assumed Wi-Fi/no modem; no-op display/platform
functions; PC locationd uses vehicle-derived accel/gyro and skips physical
sensor health checks; process selection differs. Describe branch behavior,
not authorship of all code or an exact release baseline. GPU telemetry does
not decide inference-backend compatibility. Source-only, no runtime claim.

For Q8B retain real Adafruit LSM6DS3TR-C/I²C9/0x6a and measured telemetry;
no new hardware/runtime/vehicle test, copied patch or upstream integration.
Camera work remains deferred. Next bounded implementation stays read-only
thermal provider with fault tests. Evidenceq8b/research/mm-x-hardware-20261101;
central reportAi/Reports/mm-x-hardware-20261101. Source-driven-development and
code-review-and-quality workflows; REA binary/runtime analysis not applicable
for selected readable Python/C++ sources. Documentation-only memory closeout.

Verification passed:9 exact Git blob matches/8 external Python AST parses;
31notebook documents/70relative links, source-index/pin checks,
standalone notebook copy and git diff --check. These are source/documentation
checks, not imported code, a working PC port or a Q8B integration test.
