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

## UI increment completed

## 2026-11-02 — Q8B live onroad statistics complete

Owner-requested panel is on the actual Sunny AugmentedRoadView, enabled by
Q8B road-only mode; Q8B_SHOW_STATS=0 hides it. Shows hottest readable CPU/GPU,
fan PWM percent/raw/mode (RPM unavailable), GPU inference/readback, full model,
modelHz, camera→model and camera→UI first draw. Read-only sensors1Hz on a worker;
2s timing medians, display4Hz, stale timing1s/sensors3s, unavailable as dashes.
76tests/Ruff pass. Complete65sUI:1293camera frames/1274model messages/33path
points,20.0048Hz; inference10.933/12.133ms and capture→model36.832/41.043ms
median/p95. Overlay samples match model benchmark exactly; UI endpoint precedes
benchmark draw-ready by0.781ms median. UI benchmark draw-ready45.390/58.292ms;
host EndDrawing74.590/88.904ms. Physical display latency remains unmeasured.
Full65s child exits0/0/0; outer command143 after completion remains unexplained.
Independent cleanup passes; final10s command/children exit0,179matching packets,
zero rejections. Camera/clocks restored, GPUfaults0, fan mode staysautomatic.
Model/native/root helper hashes unchanged; no new conversion/calibration/control
or vehicle/hardwared integration. Data helpers committed5e01a48; this UI increment
and exact validation are saved in Git/ledger and the portable UI receipt.
Next: normal preview --model shows the panel; owner selects later work.
[Details](../Knowledge/UI_TELEMETRY.md), [receipt](../Evidence/q8b-ui-telemetry-20261102.json).

Publisher primitive-Data initialization regression fixed and failure isolation
tested. source/model/native/helper pins, exact run results and anomaly limits
are preserved in UI_TELEMETRY and the portable receipt.
