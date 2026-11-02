"""Guarded Mountain Dew v3 derivatives; preserve original and record every rewrite."""
import argparse
import copy
import json
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.contracts import HEADS, SIZES

SOURCE_SHA = '35976b11be3904eb78e32f7dc55a6abf8e9433ac5aa391a1998f1e9ce001b199'
PARTS = ['linear_76', 'linear_77', 'linear_78', 'linear_79', 'linear_80', 'mul_36', 'linear_82', 'linear_81',
         'mul_41', 'mul_42', 'linear_120', 'linear_126', 'cat_4', 'view_60', 'model.pad']



def make_reference(model):
  result = copy.deepcopy(model)
  custom = [n for n in result.graph.node if n.domain]
  if len(custom) != 1 or custom[0].domain != 'org.tinygrad' or custom[0].op_type != 'Contiguous':
    raise ValueError('unexpected custom graph operations')
  custom[0].domain, custom[0].op_type = '', 'Identity'
  return result


def make_quantization_source(reference):
  model = copy.deepcopy(reference)
  arrays = {i.name: numpy_helper.to_array(i) for i in model.graph.initializer}
  values = {v.name: v for v in model.graph.value_info}
  nodes = {n.name: n for n in model.graph.node}
  concat = nodes['node_cat_5']
  if concat.op_type != 'Concat' or list(concat.input) != PARTS or list(concat.output) != ['cat_5']:
    raise ValueError('unexpected packed output graph')
  for name, count in zip(PARTS, SIZES, strict=True):
    dimensions = [d.dim_value for d in values[name].type.tensor_type.shape.dim]
    if dimensions != [1, count]:
      raise ValueError(f'output shape changed: {name} {dimensions}')
  rewrites = {'allowzero': [], 'gathernd': [], 'float16_initializers': 0, 'host_image_fifo': True,
              'head_outputs': dict(zip(HEADS, SIZES, strict=True))}
  for node in model.graph.node:
    if node.op_type == 'Reshape':
      for attr in list(node.attribute):
        if attr.name == 'allowzero' and attr.i == 1:
          if node.input[1] not in arrays or 0 in arrays[node.input[1]]:
            raise ValueError('unsafe dynamic/zero Reshape target')
          node.attribute.remove(attr)
          rewrites['allowzero'].append(node.name)
    if node.op_type == 'GatherND':
      if list(node.input) != ['val_545', 'val_551'] or arrays['val_551'].tolist() != [[i] for i in range(-9, 0)]:
        raise ValueError('unexpected GatherND index contract')
      dimensions = [d.dim_value for d in values['val_545'].type.tensor_type.shape.dim]
      if dimensions[0] != 33:
        raise ValueError('GatherND source dimension changed')
      replacement = arrays['val_551'] + 33
      next(i for i in model.graph.initializer if i.name == 'val_551').CopyFrom(numpy_helper.from_array(replacement, 'val_551'))
      rewrites['gathernd'].append(node.name)
  if len(rewrites['allowzero']) != 30 or len(rewrites['gathernd']) != 1:
    raise ValueError('graph rewrite counts changed')
  fifo = nodes['node_cat']
  if fifo.op_type != 'Concat' or list(fifo.input) != ['slice_1', 'unsqueeze'] or list(fifo.output) != ['next_state_img_q']:
    raise ValueError('image FIFO structure changed')
  for node in model.graph.node:
    if node is fifo:
      continue
    for index, name in enumerate(node.input):
      if name == 'next_state_img_q':
        node.input[index] = 'updated_state_img_q'
  model.graph.input.append(helper.make_tensor_value_info('updated_state_img_q', TensorProto.FLOAT, [2, 5, 6, 128, 256]))
  del model.graph.output[:]
  for name, head, size in zip(PARTS, HEADS, SIZES, strict=True):
    model.graph.node.append(helper.make_node('Cast', [name], ['q8b_' + head], name='q8b_export_' + head, to=TensorProto.FLOAT))
    model.graph.output.append(helper.make_tensor_value_info('q8b_' + head, TensorProto.FLOAT, [1, size]))
  # Keep only ancestors of exported heads. State FIFOs not needed by the neural
  # graph are maintained on the host, with reference checks before quantization.
  needed = {v.name for v in model.graph.output}
  kept = []
  for node in reversed(model.graph.node):
    if needed.intersection(node.output):
      kept.append(node)
      needed.update(node.input)
  del model.graph.node[:]
  model.graph.node.extend(reversed(kept))
  for field in ['initializer', 'input', 'value_info']:
    collection = getattr(model.graph, field)
    selected = [v for v in collection if v.name in needed]
    del collection[:]
    collection.extend(selected)
  for item in model.graph.initializer:
    if item.data_type == TensorProto.FLOAT16:
      item.CopyFrom(numpy_helper.from_array(numpy_helper.to_array(item).astype(np.float32), item.name))
      rewrites['float16_initializers'] += 1
  for value in list(model.graph.input) + list(model.graph.output) + list(model.graph.value_info):
    if value.type.tensor_type.elem_type in (TensorProto.FLOAT16, TensorProto.UINT8):
      value.type.tensor_type.elem_type = TensorProto.FLOAT
  for node in model.graph.node:
    for attr in node.attribute:
      if node.op_type == 'Cast' and attr.name == 'to' and attr.i == TensorProto.FLOAT16:
        attr.i = TensorProto.FLOAT
  return model, rewrites


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('source', type=Path)
  parser.add_argument('output', type=Path)
  args = parser.parse_args()
  if digest(args.source) != SOURCE_SHA:
    parser.error('wrong Mountain Dew v3 original source hash')
  if args.output.exists():
    parser.error('choose a fresh graph output directory; existing artifacts preserved')
  args.output.mkdir(parents=True)
  source = onnx.load(args.source)
  reference = make_reference(source)
  ref_path = args.output / 'reference_fp16.onnx'
  onnx.checker.check_model(reference, full_check=True)
  onnx.save(reference, ref_path)
  del source
  quant, rewrites = make_quantization_source(reference)
  onnx.checker.check_model(quant, full_check=True)
  quant_path = args.output / 'quantization_source_fp32.onnx'
  onnx.save(quant, quant_path)
  report = {'original_sha256': SOURCE_SHA, 'reference_sha256': digest(ref_path),
            'quantization_source_sha256': digest(quant_path), 'rewrites': rewrites,
            'heads': [{'name': h, 'source': n, 'size': size} for h, n, size in zip(HEADS, PARTS, SIZES, strict=True)],
            'limit': 'FP32 derivative removes FP16 arithmetic rounding; must compare against FP16 reference. No accuracy acceptance from checker success.'}
  (args.output / 'graph-rewrites.json').write_text(json.dumps(report, indent=2) + '\n')
  print(json.dumps(report, indent=2))


if __name__ == '__main__':
  main()
