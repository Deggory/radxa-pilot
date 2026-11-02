# Q8B UI telemetry — 2026-11-02

## 2026-11-02 — Live Q8B diagnostics panel in progress

Owner requests CPU/GPU temperatures, fan PWM, model speed, camera→model and
camera→UI timings on the actual Sunny UI. Accepted scope: read-only sensors,
small onroad panel, exact monotonic endpoints, missing/stale values shown as
unavailable, and no fan/control/calibration/model change. Source basec744d99.
First increment: named sensor reader/background sampler and bounded versioned
model timing/window helpers;5new tests/Ruff and real read-only sensors pass.
No publisher or visible UI is active yet. Next connect Q8B modeld and onroad
panel, run live UI/latency/staleness/cleanup checks, then commit the UI increment.
[Contract and source evidence](../Knowledge/UI_TELEMETRY.md).

Teacher desktop_ui source/named sysfs checked; initial read-only health receipt
retained centrally. Tests first failed for missing helpers, then5passed; Ruff
pass. Source/runtime model and saved maximum-clock helper unchanged.
