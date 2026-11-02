# Conversion progress

- [x] Fresh matching source downloaded/hash/checkpoint verified.
- [x] Jetlink clones updated and relevant changes recorded.
- [x] Parameter/size/IO inventory completed.
- [x] Initial floating/FP32 diagnostics and fresh floating DLC conversion pass; full spread-out checks continue with fresh states.
- [ ] Fresh recurrent calibration and held-out data built.
- [ ] Fresh INT8 PTQ conversion completed with preserved logs.
- [ ] Per-head and recurrent accuracy measured.
- [ ] Target/runtime verified, context compiled and inspected.
- [ ] Isolated NPU execution passes accuracy/health checks.
- [ ] Teacher/student closeout and verified commits recorded.

Corrected road700-v2 is complete:700unique images, encode-index frame mapping,
20Hz continuity checked. Initial ordinal-based data/native v1 are rejected.
Fresh calibration500-v2 is running on the x86 host; no quantization yet.
12focused tests/Ruff/shell/notebook checks pass. Scoped checkpoint is in Git.
