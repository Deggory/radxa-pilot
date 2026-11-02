"""Remove calibrated floating boundary adapters without recalibrating weights (SDK host only)."""
import argparse
import hashlib
import json
from pathlib import Path
import enum

import numpy as np

from openpilot.selfdrive.modeld.npu.contracts import HEADS
from openpilot.selfdrive.modeld.npu.evaluate_outputs import INPUT_SHAPES
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest

CALIBRATED_SHA = '6cca7b518b6aa7d557727833d589de8a93dfe253a13a0a14f55fa81a3d7e3343'


def normalized(value):
  if isinstance(value, np.ndarray):
    return {'dtype': str(value.dtype), 'shape': list(value.shape), 'sha256': hashlib.sha256(value.tobytes()).hexdigest()}
  if isinstance(value, np.generic):
    return value.item()
  if isinstance(value, dict):
    return {key: normalized(item) for key, item in value.items()}
  if isinstance(value, (list, tuple)):
    return [normalized(item) for item in value]
  if isinstance(value, enum.Enum) or hasattr(value, 'name'):
    return value.name
  if value is None or isinstance(value, (str, bool, int, float)):
    return value
  raise TypeError(f'unknown SDK attribute type: {type(value)}')


def graph_signature(graph, aliases=None, removed=(), old_boundary=()):
  aliases = aliases or {}
  def name(tensor):
    return aliases.get(tensor.name(), tensor.name())
  operations = {node.name: {'type': node.type, 'attributes': normalized(node.attrs_dict),
                           'inputs': [name(t) for t in node.inputs()], 'outputs': [name(t) for t in node.outputs()]}
                for node in graph.get_ops() if node.name not in removed}
  tensors = {name(t): {'shape': t.dims(), 'dtype': t.data_type().name, 'static': t.is_static_tensor()}
             for t in graph.get_tensor_map().values() if t.name() not in old_boundary}
  return {'operations': operations, 'tensors': tensors}


def static_signatures(graph):
  result = {}
  for tensor in graph.get_tensor_map().values():
    if tensor.is_static_tensor():
      data = tensor.get_data()
      result[tensor.name()] = {'dtype': str(data.dtype), 'shape': list(data.shape),
                              'sha256': hashlib.sha256(data.tobytes()).hexdigest()}
  return result


def verify_encodings(before, after, aliases):
  if before['param_encodings'] != after['param_encodings']:
    raise ValueError('calibrated parameter encodings changed')
  if len(set(aliases.values())) != len(aliases):
    raise ValueError('boundary aliases collide')
  activations = before['activation_encodings']
  for target in aliases.values():
    if target in activations and activations[target] != [{'bitwidth': 32, 'dtype': 'float'}]:
      raise ValueError('unexpected original boundary encoding')
  expected = {name: value for name, value in activations.items() if name not in aliases and name not in aliases.values()}
  expected.update({new: activations[old] for old, new in aliases.items()})
  if expected != after['activation_encodings']:
    raise ValueError('calibrated activation encodings changed beyond boundary aliases')


def verify_encoding_evidence(parent_actual, parent_sidecar, child_actual, child_sidecar, aliases):
  if parent_actual != parent_sidecar or child_actual != child_sidecar:
    raise ValueError('encoding sidecar does not match the actual saved DLC')
  verify_encodings(parent_actual, child_actual, aliases)


def main():
  from qti.aisw.converters.common.dlc_quantizer import DLCQuantizer, encodings_json_serializer

  def actual_encodings(graph):
    serializer = encodings_json_serializer.IrEncodingsJsonSerializer('', False)
    serializer.serialize(graph)
    return json.loads(serializer.get_graph_json())
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('source', type=Path)
  parser.add_argument('output', type=Path)
  parser.add_argument('--audit-existing', action='store_true', help='Independently validate an already-written derivative without reserializing')
  args = parser.parse_args()
  if (digest(args.source) != CALIBRATED_SHA or args.output.exists() != args.audit_existing or
      args.output.with_suffix('.json').exists()):
    parser.error('requires pinned completed calibration and a fresh output DLC')
  quantizer = DLCQuantizer(str(args.source), output_dlc=str(args.output), dump_encoding_json=True)
  graph = quantizer.ir_graph
  original_encodings = actual_encodings(graph)
  before = static_signatures(graph)
  aliases, removed = {}, []
  inputs, outputs = list(graph.get_input_tensors_to_graph()), list(graph.get_output_tensors_of_graph())
  boundary_names = [t.name() for t in inputs + outputs]
  # Capture the unmodified graph while the SDK owner/reader remains alive.
  original = graph_signature(graph)
  if {t.name() for t in inputs} != set(INPUT_SHAPES) or {t.name() for t in outputs} != {'q8b_' + h for h in HEADS[:-1]}:
    raise ValueError('unexpected calibrated graph IO')
  for tensor, is_input in [(t, True) for t in inputs] + [(t, False) for t in outputs]:
    if tensor.data_type().name != 'QNN_DATATYPE_FLOAT_32':
      raise ValueError('unexpected floating boundary type')
    neighbors = list(tensor.get_consumers()) if is_input else [tensor.get_producer()]
    if len(neighbors) != 1 or neighbors[0].type != 'Convert':
      raise ValueError('boundary is not one isolated Convert')
    node = neighbors[0]
    if len(node.inputs()) != 1 or len(node.outputs()) != 1:
      raise ValueError('unexpected boundary arity')
    native = node.outputs()[0] if is_input else node.inputs()[0]
    if native.data_type().name != 'QNN_DATATYPE_UFIXED_POINT_8' or tensor.shape() != native.shape():
      raise ValueError('unexpected native boundary contract')
    aliases[native.name()] = tensor.name()
    tensor.set_encoding(native.data_type(), native.get_encoding())
    removed.append(node.name)
    graph.squash(node, node.inputs()[0].name(), False)
  if len(removed) != 20 or static_signatures(graph) != before:
    raise ValueError('unexpected graph/static-buffer change')
  expected = {'operations': {name: value for name, value in original['operations'].items() if name not in removed},
              'tensors': {aliases.get(name, name): value for name, value in original['tensors'].items() if name not in boundary_names}}
  for value in expected['operations'].values():
    for field in ['inputs', 'outputs']:
      value[field] = [aliases.get(name, name) for name in value[field]]
  if graph_signature(graph) != expected:
    raise ValueError('retained operations/attributes/connectivity/tensor contracts changed')
  graph.validate_graph()
  # No call to quantize(): calibrated weights and ranges are reused exactly.
  if not args.audit_existing:
    quantizer.save('Research integer IO: remove20 boundary Converts; no recalibration or weight changes')
  reloaded = DLCQuantizer(str(args.output))  # Keep the owner alive: IrGraph is a borrowed SDK object.
  if static_signatures(reloaded.ir_graph) != before or graph_signature(reloaded.ir_graph) != expected:
    raise ValueError('static buffers changed during serialization')
  before_encoding = args.source.with_name(args.source.stem + '_encoding.json')
  after_encoding = args.output.with_name(args.output.stem + '_encoding.json')
  reloaded_encodings = actual_encodings(reloaded.ir_graph)
  verify_encoding_evidence(original_encodings, json.loads(before_encoding.read_text()),
                           reloaded_encodings, json.loads(after_encoding.read_text()), aliases)
  report = {'parent_dlc_sha256': CALIBRATED_SHA, 'dlc_sha256': digest(args.output), 'dlc_bytes': args.output.stat().st_size,
            'removed_boundary_converts': removed, 'activation_aliases': aliases, 'static_buffer_count': len(before),
            'static_buffers_unchanged': True, 'parameter_and_activation_encodings_unchanged': True,
            'retained_graph_signature_sha256': hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest(),
            'retained_operations_attributes_connectivity_unchanged': True,
            'roundtrip_encodings_unchanged': True,
            'encoding_sha256': digest(after_encoding), 'qualification': 'unqualified integer-boundary derivative; not recalibrated'}
  args.output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
  print(json.dumps(report, indent=2))


if __name__ == '__main__':
  main()
