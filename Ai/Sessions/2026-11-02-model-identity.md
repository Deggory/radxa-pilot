# Bundled model identity — 2026-11-02

Owner asks which model is in our folder and what it does. Source base
576cdc6b3a166a2fdea5c9876ee6cba10ddcac15 on radxa/q8b, clean at start.

Confirmed CD210 configured default/ref5b6436a90cf6902b8aaa71c2b6f3d7164d8ae391.
Main ONNX path:openpilot/selfdrive/modeld/models/driving_supercombo.onnx,
60918562bytes,SHA25665a08adc31d5c456219687d99b7bf5e44d61dae2d49ea67850e76105c7248cce.
Actual bytes/name/ref combined fingerprint matches tracked models/tests/model_hash.
Official GitHub name file at6f7a2c94 also matches (blobbd8e9ac2650c5aa6e5ae207791ef2d58d9782567).

ONNX protobuf metadata read safely, no embedded output_slices pickle executed.
Exporter PyTorch2.13.0+cu130; graph new_img[2,6,128,256]uint8 plus desire,
traffic convention,action timing and temporal queues; outputs[1,2576]float
and next temporal queues. Source parser/fill_model_msg describes planned path,
motion/speed/acceleration, lane lines, road edges, leads and camera pose.
Lateral control uses path/curvature calculated from model output plus control/
vehicle logic, not direct actuator commands from the ONNX file. Target20Hz
from current ModelConstants, not a new measured inference performance result.

Separate configured big model:Mountain Dew Model v3,ref1e219d7785cfb7b7343c7f2366347fc86e7ce5f2,
stored as big_driving_tinygrad.pkl for Chestnut. Not another name for CD210;
big pickle not loaded/analyzed. Driver-monitoring model remains separate.
Do not infer this graph needs NVIDIA hardware merely from exporter cu130 text.
Actual current Q8B inference remains the recommended next work, not started.

Evidence:optional central Ai/Reports/sunnypilot-model-identity-20261102/identity.json.
ONNX metadata/source/hash review only; no model conversion/driver/camera/vehicle
run. Tinygrad92b742f7/msgqe7396e76/stock weights unchanged. Camera optimisation
remains deferred. No upstream merge or catalog/default-model change performed.

Skills:source-driven development, documentation and Git workflow; source-first
local metadata/schema/parser inspection and pinned official GitHub source.
No unrelated REA native/managed binary analysis needed for this identification.
Community search found discussion but no driving-performance anecdotes adopted
as technical validation. No release-date or training-architecture claim made.
