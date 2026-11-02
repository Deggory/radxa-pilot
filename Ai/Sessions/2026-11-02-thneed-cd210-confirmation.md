# Thneed CD210 confirmation — 2026-11-02

Owner asks whether the tested Thneed model wasCD210. Yes: source/metadata/content
chain supports CD210 learned core with older host-history interface. Prior
452cb3e8 documentation incorrectly said weights were different; corrected now.
Source start452cb3e8a8c4fbe5d787bfd70960ffb24af5cac7/radxa/q8b, clean.

Followed teacher October30 q8b-0113-performance report before fresh checks:
- Exporter/provenance binds original659727c4d4839adc4992a254409a54259a8756a743f2d567bf5fdc6579f8009b
  to derivativeee8ca6b3 and driving-02.thneedeb741641 (full pins in GPU reference).
- Preserved source model_name.py labels defaultCD210/ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391,
  matching current configured default.
- Fresh official ONNX parser/checker on retained60881999byte old model and current
  60918562byte65a08adc model passes exact expected SHA256, identical checkpoint,
  identical60Conv/82Gemm/8MatMul constant-RHS sequences, all old constant-content
  multiplicities retained. Eleven extra constants belong to new history wrapper.
- Old351nodes uses host img/big_img/features/desire history; new377nodes adds
  new_img/state queues and next-state outputs. Same learned network is not an
  interchangeable runtime interface. Earlier six mapped CPU checks passed exact
  outputs; those are preserved tests, not a new inference in this task.

Corrected student topic/handoff/state/tasks/router and teacher current summaries.
Old performance results remain valid for their tested profile; current wrapper
integration/timing still needs verification. Camera optimisation remains deferred.
No source/runtime/weights/backend/device action. Failed oldGit lookup is not
identity evidence; preserved files plus fullhash/content/provenance supplied proof.

Fresh report: optional workspace
Ai/Reports/sunnypilot-thneed-cd210-confirmation-20261102/identity.json.
Static format/tensor parsing only, no output_slices pickle executed, inference or
unrelated REA analysis. Skills: source-driven review, documentation, Git. Notebook
and diff checks are fresh validation. No upstream merge or vehicle action.
