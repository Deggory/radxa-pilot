from pathlib import Path
import tempfile
import unittest

import numpy as np

from openpilot.selfdrive.modeld.npu.evaluate_outputs import INPUT_SHAPES, output_contract, read_outputs, verify_run
from openpilot.selfdrive.modeld.npu.contracts import HEADS, SIZES
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest


class TestCompiledOutputs(unittest.TestCase):
  def test_execution_receipt_rejects_substituted_context_and_outputs(self):
    with tempfile.TemporaryDirectory() as directory:
      paths = [Path(directory) / name for name in ['context', 'metadata', 'input_list']]
      for path in paths:
        path.write_bytes(path.name.encode())
      run = dict(zip(['context_sha256', 'context_info_sha256', 'input_list_sha256'], map(digest, paths), strict=True))
      run.update(exit_code=0, qnn_output_files=[{'file': 'Result_0/head.raw', 'sha256': 'abc'}])
      verify_run(run, *paths, run['qnn_output_files'])
      with self.assertRaises(ValueError):
        verify_run(run, *paths, [])
      paths[0].write_bytes(b'wrong context')
      with self.assertRaises(ValueError):
        verify_run(run, *paths, run['qnn_output_files'])

  def metadata(self):
    return {'info': {'numGraphs': 1, 'socModel': 37, 'contextMetadata': {'info': {'dspArch': 68}}, 'buildId': 'v2.37.1.250807093845_124904',
                     'graphs': [{'info': {'graphInputs': [
      {'info': {'name': name, 'dimensions': shape, 'dataType': 'QNN_DATATYPE_FLOAT_32'}} for name, shape in INPUT_SHAPES.items()],
                                         'graphOutputs': [
      {'info': {'name': 'q8b_' + head, 'dimensions': [1, size], 'dataType': 'QNN_DATATYPE_FLOAT_32'}}
      for head, size in reversed(list(zip(HEADS[:-1], SIZES[:-1], strict=True)))]}}]}}

  def test_reordered_heads_use_names_and_missing_constant_padding_is_zero(self):
    contract = output_contract(self.metadata())
    with tempfile.TemporaryDirectory() as directory:
      folder = Path(directory)
      for index, (head, size) in enumerate(zip(HEADS[:-1], SIZES[:-1], strict=True)):
        np.full(size, index + 1, np.float32).tofile(folder / f'q8b_{head}.raw')
      packed = read_outputs(folder, contract)
      self.assertEqual(packed.shape, (1, 18452))
      self.assertEqual(packed[0, 0], 1)
      self.assertEqual(packed[0, 528], 2)
      self.assertEqual(packed[0, -3], 14)
      self.assertTrue(np.array_equal(packed[0, -2:], [0, 0]))
      np.array([np.nan], np.float32).tofile(folder / 'q8b_action.raw')
      with self.assertRaises(ValueError):
        read_outputs(folder, contract)

  def test_old_model_and_wrong_dimensions_or_dtype_rejected(self):
    for field, value in [('name', 'old_packed_output'), ('dimensions', [1, 1]), ('dataType', 'QNN_DATATYPE_UFIXED_POINT_8')]:
      metadata = self.metadata()
      metadata['info']['graphs'][0]['info']['graphOutputs'][0]['info'][field] = value
      with self.subTest(field=field), self.assertRaises(ValueError):
        output_contract(metadata)

  def test_historical_soc39_and_quantized_io_are_rejected(self):
    metadata = self.metadata()
    metadata['info']['socModel'] = 39
    with self.assertRaises(ValueError):
      output_contract(metadata)
    metadata = self.metadata()
    metadata['info']['graphs'][0]['info']['graphInputs'][0]['info']['dataType'] = 'QNN_DATATYPE_UFIXED_POINT_8'
    with self.assertRaises(ValueError):
      output_contract(metadata)


if __name__ == '__main__':
  unittest.main()
