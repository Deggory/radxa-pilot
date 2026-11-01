# Existing Sunnypilot changes explained — 2026-11-01

Owner requested a plain-language account of changes inside sunnypilot. Read
current Git/source/README at b7fff5360aebb15d774c2146e5de1415022db160,
branch radxa/q8b; working tree clean before this documentation closeout.
Confirmed implementation12e44fee and location/notebook commits7c208a33/b7fff536.
No new application change, upstream integration or service launch was requested.

Explained exact Linux/aarch64/Q8B device-tree detection, HardwareRadxa identity
in Python/C++, retained generic Linux build/service policy, append-only
radxaQ8b schema identity, explicit unconfigured-camera guards, read-only
identity CLI, existing11 Python/4 native checks, tracked project Ai and README.
Power/thermal/sensor methods still inherit generic PC defaults. No camera,
GPU inference, full managed runtime or lateral/actuator integration is established.
Existing test results are prior verified evidence, not tests rerun for this
explanation. The daily updater protects the project and updates only the
external upstream reference. Inbox: no pending related commits or missing local
validation; retained02bf09e8 failure is historical stale notebook evidence.

Next implementation remains stock-contract/runtime preflight. Source headers
2026.003.000/COMMA0.11.3; main identity application source unchanged. Used the
documentation-and-adrs workflow to keep the explanation and limits consistent
with actual source. This task changes memory documentation only.
