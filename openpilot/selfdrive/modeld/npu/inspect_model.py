"""Record ONNX source identity, IO contracts and initializer storage estimates."""
import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

from onnx import TensorProto
import onnx

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest


def inventory(model):
  def spec(value):
    tensor = value.type.tensor_type
    return {'name': value.name, 'dtype': TensorProto.DataType.Name(tensor.elem_type),
            'shape': [d.dim_value if d.HasField('dim_value') else d.dim_param or None for d in tensor.shape.dim]}
  types = defaultdict(lambda: {'tensors': 0, 'elements': 0, 'storage_bytes': 0})
  floating = 0
  for item in model.graph.initializer:
    name = TensorProto.DataType.Name(item.data_type)
    count = math.prod(item.dims)
    types[name]['tensors'] += 1
    types[name]['elements'] += count
    types[name]['storage_bytes'] += count * onnx.helper.tensor_dtype_to_np_dtype(item.data_type).itemsize
    if item.data_type in (TensorProto.FLOAT, TensorProto.FLOAT16, TensorProto.DOUBLE, TensorProto.BFLOAT16):
      floating += count
  return {'graph_name': model.graph.name, 'inputs': [spec(v) for v in model.graph.input],
          'outputs': [spec(v) for v in model.graph.output], 'initializer_types': dict(types),
          'floating_initializer_elements': floating,
          'floating_initializer_int8_payload_estimate_bytes': floating,
          'estimate_limit': ('One byte per floating initializer element, excluding scales, bias precision, alignment and compiler overhead. ' +
                             'Includes floating constants; not a measured compiled size or peak RAM.'),
          'operators': dict(Counter(f'{n.domain or "ai.onnx"}::{n.op_type}' for n in model.graph.node)),
          'metadata': {v.key: v.value for v in model.metadata_props},
          'opsets': {v.domain or 'ai.onnx': v.version for v in model.opset_import}}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('model', type=Path)
  parser.add_argument('--expected-sha256', required=True)
  parser.add_argument('--report', type=Path, required=True)
  args = parser.parse_args()
  sha = digest(args.model)
  if sha != args.expected_sha256:
    parser.error(f'model hash mismatch: {sha}')
  result = inventory(onnx.load(args.model))
  result.update(path=str(args.model), sha256=sha, bytes=args.model.stat().st_size)
  args.report.parent.mkdir(parents=True, exist_ok=True)
  args.report.write_text(json.dumps(result, indent=2) + '\n')
  print(json.dumps({k: result[k] for k in ['sha256', 'bytes', 'inputs', 'outputs', 'initializer_types', 'floating_initializer_elements']}, indent=2))


if __name__ == '__main__':
  main()
