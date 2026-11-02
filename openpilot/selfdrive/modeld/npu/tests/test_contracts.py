import unittest
from openpilot.selfdrive.modeld.npu.contracts import validate_road_metadata


class TestRoadContract(unittest.TestCase):
  def records(self):
    return [{'frame_id': i, 'capture_ns': i * 50_000_000, 'image_sha256': f'{i:064x}'} for i in range(4)]

  def test_continuous_unique_frames(self):
    validate_road_metadata(self.records())

  def test_duplicate_image_rejected(self):
    rows = self.records()
    rows[2]['image_sha256'] = rows[1]['image_sha256']
    with self.assertRaises(ValueError):
      validate_road_metadata(rows)

  def test_gap_and_reverse_time_rejected(self):
    for field, value in [('frame_id', 4), ('capture_ns', 49_000_000), ('capture_ns', 160_000_000)]:
      rows = self.records()
      rows[2][field] = value
      with self.assertRaises(ValueError):
        validate_road_metadata(rows)


class TestArtifactContract(unittest.TestCase):
  def test_stale_dlc_rejected_after_receipt(self):
    from pathlib import Path
    import tempfile
    from unittest.mock import patch
    from openpilot.selfdrive.modeld.npu.contracts import float_receipt
    from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
    with tempfile.TemporaryDirectory() as temp:
      work = Path(temp)
      source = work / 'artifacts/graph-v1/quantization_source_fp32.onnx'
      dlc = work / 'artifacts/dlc-v1/float.dlc'
      source.parent.mkdir(parents=True)
      dlc.parent.mkdir(parents=True)
      source.write_bytes(b'controlled source fixture')
      dlc.write_bytes(b'fresh converted fixture')
      with patch('openpilot.selfdrive.modeld.npu.contracts.DERIVATIVE_SHA', digest(source)):
        float_receipt(work, create=True)
        float_receipt(work)
        dlc.write_bytes(b'old unrelated DLC')
        with self.assertRaises(ValueError):
          float_receipt(work)

  def test_native_input_changes_and_missing_diagnostics_rejected(self):
    from pathlib import Path
    import tempfile
    import json
    from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, verify_calibration
    from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      raw = root / 'input.raw'
      raw.write_bytes(b'reference input')
      input_list = root / 'input_list.txt'
      input_list.write_text(f'input:={raw}\n')
      report = {'reference_sha256': REFERENCE_SHA, 'derivative_sha256': DERIVATIVE_SHA, 'frames': 1,
                'input_list_sha256': digest(input_list), 'comparisons': [{'index': 0, 'packed': {'outside_atol_0p01_rtol_0p01': 0}}],
                'native_inputs': [{'file': raw.name, 'sha256': digest(raw)}]}
      receipt = root / 'reference-report.json'
      receipt.write_text(json.dumps(report))
      verify_calibration(input_list)
      raw.write_bytes(b'wrong state input')
      with self.assertRaises(ValueError):
        verify_calibration(input_list)
      report['comparisons'] = []
      receipt.write_text(json.dumps(report))
      with self.assertRaises(ValueError):
        verify_calibration(input_list)


class TestRoadVersion(unittest.TestCase):
  def test_camera_ordinal_manifest_rejected(self):
    from openpilot.selfdrive.modeld.npu.contracts import validate_road_manifest
    manifest = {'records': [{'frame_id': 5915, 'capture_ns': 1, 'image_sha256': 'a'}]}
    with self.assertRaises(ValueError):
      validate_road_manifest(manifest, 1)
    manifest.update(format_version=2, video_alignment='frameId mapped through fullHEVC encode-index segmentId')
    with self.assertRaises(ValueError):
      validate_road_manifest(manifest, 1)
    manifest['records'][0].update(narrow_video_index=3, wide_video_index=3)
    self.assertEqual(len(validate_road_manifest(manifest, 1)), 1)


class TestResearchGate(unittest.TestCase):
  def test_research_receipt_binds_dlc_and_calibration(self):
    import json
    from pathlib import Path
    import tempfile
    from unittest.mock import patch
    from openpilot.selfdrive.modeld.npu.contracts import research_receipt
    with tempfile.TemporaryDirectory() as directory:
      work = Path(directory)
      artifacts = work / 'artifacts/dlc-v1'
      artifacts.mkdir(parents=True)
      (artifacts / 'float-receipt.json').write_text('{}')
      dlc = artifacts / 'w8a8-research.dlc'
      dlc.write_bytes(b'new quantized graph')
      input_list = work / 'input_list.txt'
      input_list.write_text('input fixture')
      calibration = work / 'reference-report.json'
      calibration.write_text(json.dumps({'frames': 500, 'comparisons': [{'packed': {'outside_atol_0p01_rtol_0p01': 1}}]}))
      with patch('openpilot.selfdrive.modeld.npu.contracts.float_receipt'), patch('openpilot.selfdrive.modeld.npu.contracts.verify_calibration'):
        research_receipt(work, input_list, create=True)
        research_receipt(work, input_list)
        result = json.loads(dlc.with_suffix('.json').read_text())
        self.assertEqual(result['retained_fp16_failure_count'], 1)
        self.assertTrue(result['qualification'].startswith('unqualified'))
        with self.assertRaisesRegex(ValueError, 'existing research receipt preserved'):
          research_receipt(work, input_list, create=True)
        original = dlc.read_bytes()
        dlc.write_bytes(b'wrong compiled model')
        with self.assertRaisesRegex(ValueError, 'provenance changed'):
          research_receipt(work, input_list)
        dlc.write_bytes(original)
        calibration.write_text(calibration.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'provenance changed'):
          research_receipt(work, input_list)

  def test_explicit_research_retains_failure_and_requires_provenance(self):
    from pathlib import Path
    import tempfile
    import json
    from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, SEMANTIC_SHA, verify_calibration
    from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      raw = root / 'input.raw'
      raw.write_bytes(b'reference input')
      input_list = root / 'input_list.txt'
      input_list.write_text(f'input:={raw}\n')
      report = {'reference_sha256': REFERENCE_SHA, 'derivative_sha256': DERIVATIVE_SHA, 'frames': 1,
                'semantic_reference_sha256': SEMANTIC_SHA, 'reference_recurrence_verified_frames': 1,
                'input_list_sha256': digest(input_list), 'comparisons': [{'index': 0, 'packed': {'outside_atol_0p01_rtol_0p01': 1}}],
                'same_precision_comparisons': [{'index': 0, 'packed': {'max_abs': 0, 'bitwise_equal': True}}],
                'native_inputs': [{'file': raw.name, 'sha256': digest(raw)}]}
      receipt = root / 'reference-report.json'
      receipt.write_text(json.dumps(report))
      with self.assertRaisesRegex(ValueError, 'diagnostics failed'):
        verify_calibration(input_list)
      verify_calibration(input_list, research=True)
      for field, wrong in [('semantic_reference_sha256', 'wrong'), ('reference_recurrence_verified_frames', 0),
                           ('same_precision_comparisons', []),
                           ('same_precision_comparisons', [{'index': 1, 'packed': {'max_abs': 0, 'bitwise_equal': True}}]),
                           ('same_precision_comparisons', [{'index': 0, 'packed': {'max_abs': 0.1, 'bitwise_equal': False}}]),
                           ('same_precision_comparisons', [{'index': 0, 'packed': {'max_abs': 0, 'bitwise_equal': False}}]),
                           ('native_inputs', [])]:
        receipt.write_text(json.dumps(report | {field: wrong}))
        with self.subTest(field=field, value=wrong), self.assertRaises(ValueError):
          verify_calibration(input_list, research=True)
      receipt.write_text(json.dumps(report))
      raw.write_bytes(b'altered state')
      with self.assertRaisesRegex(ValueError, 'native calibration file changed'):
        verify_calibration(input_list, research=True)
