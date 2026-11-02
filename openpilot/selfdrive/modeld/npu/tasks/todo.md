# Fresh NPU baseline checkpoint — 2026-11-02

- [x] Fresh matching source downloaded, hash/checkpoint verified.
- [x] Jetlink reference clones updated; relevant changes/pins saved.
- [x] Parameter/size/IO inventory completed;200 MB plain-INT8 target unmet.
- [x] Corrected encoder-index road700-v2; ordinal v1 rejected.
- [x]500 fresh source-state calibration frames independently replayed/audited.
- [x]200 heldout frames built with separate reset;132 warmup/68 evaluation.
- [x] Retain failed strict FP16 check; explicit owner-approved research gate.
- [x] Fresh W8A8 PTQ completed,400356844-byte DLC retained.
- [x] Prove integer-IO adapter removal preserves weights/graph/encodings.
- [x] Compile and inspect actual SDK2.37/v68/SoC37 context (444203008bytes).
- [x]200-call device replay and3-call native-byte conversion check exit0.
- [x] Measure per-head teacher-forced errors: **numerical acceptance FAIL**.
- [ ] Candidate self-feedback / parsed driving metrics (deferred after failure).
- [ ] Broad representative scene/night/weather/maneuver evaluation.
- [ ] Accuracy recovery with W8A16/mixed activation precision (next experiment).
- [ ] Qualify any candidate for modeld integration (not authorized by this test).

Current candidate remains unselected. Tooling checks do not override model
failure. See [results](../RESULTS.md). Teacher/student closeout, review evidence
and verified scoped commits accompany this checkpoint. Current CD210 GPU path
and camera calibration are unchanged; no vehicle actuation.
