import unittest

from onnx import TensorProto, helper

from openpilot.selfdrive.modeld.npu.inspect_model import inventory


class TestInventory(unittest.TestCase):
  def test_precision_budget_and_static_io(self):
    weights = helper.make_tensor('w', TensorProto.FLOAT16, [3, 4], [1.] * 12)
    graph = helper.make_graph([helper.make_node('MatMul', ['x', 'w'], ['y'])], 'test',
                             [helper.make_tensor_value_info('x', TensorProto.FLOAT16, [1, 3])],
                             [helper.make_tensor_value_info('y', TensorProto.FLOAT16, [1, 4])], [weights])
    result = inventory(helper.make_model(graph))
    self.assertEqual(result['floating_initializer_elements'], 12)
    self.assertEqual(result['floating_initializer_int8_payload_estimate_bytes'], 12)
    self.assertEqual(result['initializer_types']['FLOAT16']['storage_bytes'], 24)
    self.assertEqual(result['inputs'][0]['shape'], [1, 3])

  def test_dynamic_dimension_is_reported(self):
    model = helper.make_model(helper.make_graph([], 'dynamic', [helper.make_tensor_value_info('x', TensorProto.FLOAT, ['batch', 2])], []))
    self.assertEqual(inventory(model)['inputs'][0]['shape'], ['batch', 2])
