# November 7, 2026 — Classic CAN scope and 0xDC clarification

Scope: owner excludes CAN FD and asks what DC does in each firmware. QA21
synchronized teacher/student; student CHIMERA_OLD_PANDAD topic records details.
Baseline ae145e4c58c9f154a46cff85b2d2d4b11742425b, radxa/q8b clean at start;
Panda8a16e089/opendbc150f9371. Source-first selected reads trace host control
request -> Panda safety hooks versus old relay request -> saved ignition loop.
Actual relay condition bypass and hard-coded health17 remain explicit.

Documentation/source skills applied; no REA artifact/runtime work necessary.
No code, firmware, FD cleanup, hardware, Params, update or push. Prior tests
not rerun; synchronized QA/notebook/whitespace checks only. Installed image and
physical relay semantics unverified. Next candidate remains native classic-only
old-Chimera observation adapter; implementation not resumed. Verified notebook
increment committed locally and validation journaled in maintenance.
