# Big Tinygrad model and Q8B NPU — 2026-11-02

Owner asks whether big_driving_tinygrad.pkl will be easy to run on Radxa NPU.
Advisory investigation only; source HEAD b9d8af56deeca5411752a8b5887f2a428a84d197,
branch radxa/q8b, clean at start. No inference/conversion/camera/device writes.

## Current bundled artifact

openpilot/selfdrive/modeld/models/big_driving_tinygrad.pkl is 799941965 bytes
(about763MiB), SHA256 d4c7a3fcfc95813826ca871a80bea18df833aacb2eb6f5333e25a01e65b1a422.
Configured name Mountain Dew Model v3/ref1e219d7785cfb7b7343c7f2366347fc86e7ce5f2.
Read eight-byte length and820289-byte opcode section, then parsed138913opcodes
with standard-library pickletools. Found Tinygrad JIT, LLVM, AMD and model
input/output/state names. Never unpickled or executed the artifact.
helpers.load_oob explicitly selects USB+AMD:LLVM for Chestnut/big; this is not
a QNN context. No NPU switch is implemented by this research.
Tinygrad source pin92b742f711c7d216fd3ed7a46a30a959e3c43bd4 unchanged.

## Teacher evidence recovered: big NPU conversion already exists

Read teacher Jetlink note and actual Oct31 O3/shared report, not just earlier
small-model NPU failure. Historical big ONNX6fee5937923c74848df4a63f6239eb6331c6274dd4bdb7a5d6ec0388a8b543d5
is766018462bytes; separate W8A16 O3/4MiB context
afef0f879d85402ba432e5d37cd9884266789d10d07fe3988bdc9952b144616f is442757120bytes.
QAIRT/QNN2.37/v68, standalone runner095b20f / ELF6e5593ec; exact System library
SDK release still unidentified. Matched short replay: graph p50/p95
38.196/40.353ms; host request→reply41.515/44.191ms, excluding camera/UI/init.
488calls across two ABBA rounds; all480 recurrent vectors match the saved
quantized baseline bitwise,18452values each. This does not resolve differences
from unquantized reference or qualify sustained current Sunnypilot integration.

Current pickle-to-historical-ONNX identity is NOT established. Do not attach
these timings to Mountain Dew v3 without matching graph/weights/state/outputs.
Separate Oct23 small-model W8A8 tests failed accuracy; that failure is not proof
the big model cannot run. Prior mixed contexts crashed cDSP and were recovered;
do not rerun them or replace the proven runtime for this advisory question.

## Recommendation and remaining work

Possible, substantial port rather than direct pickle loading. First compare
the exact bundled graph/weights/metadata against retained historical big ONNX.
If different, obtain/export matching ONNX or original graph, then adapt/quantize
and compile for the matched Q8B v68 stack. Reuse verified conversion lessons.
Require floating-reference per-head/recurrent accuracy, exact image/state/parser
contracts, explicit HTP placement, and sustained camera→model publication20Hz
with latency/thermal checks. A20Hz frame period is50ms, not a measured timing.
Keep current CD210→Adreno as the recommended first integration route; owner has
not selected or authorized implementation of a new NPU backend in this turn.
Camera optimisation/calibration remain deferred; application defaults unchanged.

Primary online sources checked November2:
[Radxa NPU guide](https://docs.radxa.com/en/dragon/q8b/app-dev/npu-dev/qairt-sdk)
documents QAIRT formats and SC8280XP/v68; context binaries are chip-specific.
[Radxa Ubuntu example](https://docs.radxa.com/en/dragon/q8b/app-dev/npu-dev/quick-example)
demonstrates QNN HTP execution. Linux is not the fundamental blocker.
Current ONNX Runtime QNN documentation also lists LinuxARM64; that alone does
not qualify a newest SDK/runtime for this board's existing v68 firmware.

## Evidence and limits

Optional workspace evidence: Ai/Reports/sunnypilot-big-npu-review-20261102/evidence.json.
Teacher report: Ai/Reports/jetlink-o3-shared-test-20261031/REPORT.md;
binding: Jetlink/config/q8b-model-o3-experimental.json. Read preserved results,
no benchmark rerun. Fresh checks are static pickle-format parsing, artifact
SHA256, source routing and notebook integrity/diff checks. No current NPU-health,
model-inference or vehicle result claimed. Source-first/REA routing used bounded
format inspection; no native REA analysis or fabricated runtime result needed.
Skills: source-driven review, documentation and Git workflow. Daily inbox shows
no pending related upstream discussion; protected port not merged or rebased.
