# Teacher Thneed work recovered — 2026-11-02

Owner asks what teacher knows about our fast GPU Thneed model. At clean
b67031e3d6bc585fcba4123f188f070fca2ee1fb/radxa/q8b, followed teacher camera/Sunny
notes into Oct30 trial, Oct31 matched-camera and20minute-soak source reports.
Promoted methods, files, exact source/model/runtime pins and timing boundaries
to [Thneed reference](../Knowledge/THNEED_GPU_REFERENCE.md).

Fresh verification: existing99641029byte driving-02.thneed SHA256eb741641
matches saved full hash. Read actual accepted result.json/protocol.json:
100warmup,24101steady,19gates pass,20.000014Hz,11.724/12.348ms model p50/p95,
35.417/39.721ms capture→output. Generic20-warmup summary is separate.
No new inference/benchmark/driver/clocks/camera changes; archived results only.
Correction after direct comparison: oldCD210659727c4 and currentCD21065a08adc
have identical learned weights/checkpoint; history wrapper differs. Current
wrapper needs runtime integration/qualification. Portable OpenCL replay and resident buffers are reusable approach;
HIGH priority had no proven speed gain and max-clock context must stay explicit.

Recommendation remains bring current model into Sunny using teacher's proven
GPU/exporter approach after checking current graph/contracts and CPU parity.
No code/runtime integration begun; camera optimisation deferred, no actuation.
Agent Skills performance/documentation/Git, source-first review per REA fast path.
Project notebook/link/diff checks are fresh validation; old GPU runs not repeated.
Both memory layers updated; no upstream integration (inbox has0pending reviews).
