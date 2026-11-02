"""Separate FP16 promotion error from graph/FIFO/head rewrite error."""
import argparse
import json
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, numpy_helper

from openpilot.selfdrive.modeld.npu.prepare_graph import SOURCE_SHA, make_reference
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('source', type=Path)
  parser.add_argument('output', type=Path)
  args = parser.parse_args()
  if digest(args.source) != SOURCE_SHA or args.output.exists():
    parser.error('requires original source and a fresh output path')
  model = make_reference(onnx.load(args.source))
  promoted = 0
  for item in model.graph.initializer:
    if item.data_type == TensorProto.FLOAT16:
      item.CopyFrom(numpy_helper.from_array(numpy_helper.to_array(item).astype(np.float32), item.name))
      promoted += 1
  for value in list(model.graph.input) + list(model.graph.output) + list(model.graph.value_info):
    if value.type.tensor_type.elem_type == TensorProto.FLOAT16:
      value.type.tensor_type.elem_type = TensorProto.FLOAT
  for node in model.graph.node:
    for attr in node.attribute:
      if node.op_type == 'Cast' and attr.name == 'to' and attr.i == TensorProto.FLOAT16:
        attr.i = TensorProto.FLOAT
  onnx.checker.check_model(model, full_check=True)
  onnx.save(model, args.output)
  report = {'original_sha256': SOURCE_SHA, 'semantic_reference_sha256': digest(args.output),
            'promoted_initializers': promoted, 'preserved': 'original seven inputs/four outputs and all FIFO/head graph operations',
            'changes': 'Contiguous to Identity and FP16 to FP32 only; no safe-Reshape/negative-GatherND/head-split/host-FIFO rewrite',
            'limit': 'Same-precision graph check only; does not erase FP16 precision-drift failures or establish INT8 accuracy.'}
  args.output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
  print(json.dumps(report, indent=2))


if __name__ == '__main__':
  main()
