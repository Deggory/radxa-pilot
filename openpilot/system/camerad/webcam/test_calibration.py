import tempfile
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import cv2 as cv
import numpy as np

from openpilot.system.camerad.webcam.calibrate import detect, object_points, solve, solve_directory, write_target


class TestLensCalibration(unittest.TestCase):
  @staticmethod
  def projected_views():
    k = np.array([[900., 0, 635.], [0, 890., 355.], [0, 0, 1.]])
    views = []
    for i in range(16):
      rotation = np.array([.15 * (i % 4 - 1.5), .12 * (i // 4 - 1.5), .03 * (i % 3 - 1)])
      translation = np.array([-100. + 50 * (i % 4 - 1.5), -60. + 40 * (i // 4 - 1.5), 650. + 40 * (i % 3)])
      corners, _ = cv.projectPoints(object_points(25), rotation, translation, k, np.zeros(5))
      views.append(corners.astype(np.float32))
    return k, views

  def test_detector_reads_the_9_by_6_grid(self):
    image = np.full((720, 1280, 3), 255, dtype=np.uint8)
    for y in range(7):
      for x in range(10):
        if (x + y) % 2 == 0:
          image[100 + y * 60:100 + (y + 1) * 60, 300 + x * 60:300 + (x + 1) * 60] = 0
    corners = detect(image)
    self.assertIsNotNone(corners)
    self.assertEqual(corners.shape, (54, 1, 2))
    self.assertIsNone(detect(np.full_like(image, 255)))

  def test_target_has_exact_a4_and_25mm_squares(self):
    with tempfile.TemporaryDirectory() as tmp:
      svg, pdf = write_target(Path(tmp))
      tree = ET.parse(svg)
      self.assertEqual(tree.getroot().attrib['width'], '297mm')
      self.assertEqual(tree.getroot().attrib['height'], '210mm')
      squares = [node for node in tree.getroot().iter() if node.attrib.get('class') == 'square']
      self.assertEqual(len(squares), 35)
      self.assertTrue(all(node.attrib['width'] == node.attrib['height'] == '25' for node in squares))
      self.assertTrue(pdf.read_bytes().startswith(b'%PDF-1.4'))
      with self.assertRaises(FileExistsError):
        write_target(Path(tmp))

  def test_solver_recovers_known_camera_from_diverse_projected_views(self):
    k, views = self.projected_views()
    result = solve(views, (1280, 720), 25)
    np.testing.assert_allclose(result['camera_matrix'], k, atol=.1)
    self.assertLess(result['rms_px'], .01)
    self.assertEqual(result['status'], 'candidate_not_installed')
    self.assertEqual(len(result['per_view_rms_px']), 16)

  def test_high_error_calibration_is_rejected_without_deleting_views(self):
    _, views = self.projected_views()
    rng = np.random.default_rng(123)
    noisy = [v + rng.normal(0, 5, v.shape).astype(np.float32) for v in views]
    with self.assertRaisesRegex(ValueError, 'Reprojection error too high'):
      solve(noisy, (1280, 720), 25)

  def test_solve_preserves_existing_output_and_rejects_changed_images(self):
    with tempfile.TemporaryDirectory() as tmp:
      directory = Path(tmp)
      output = directory / 'candidate.json'
      output.write_text('keep')
      with self.assertRaises(FileExistsError):
        solve_directory(directory, output, 25)
      self.assertEqual(output.read_text(), 'keep')
      image = directory / 'frame-000.jpg'
      image.write_bytes(b'changed')
      manifest = {'profile': {'width': 1280, 'height': 720, 'format': 'MJPG', 'capture_fps': 60},
                  'images': [{'file': image.name, 'sha256': 'original_hash'}]}
      (directory / 'manifest.json').write_text(json.dumps(manifest))
      with self.assertRaisesRegex(ValueError, 'Image hash changed'):
        solve_directory(directory, directory / 'new.json', 25)
      manifest['error'] = 'camera disconnected'
      (directory / 'manifest.json').write_text(json.dumps(manifest))
      with self.assertRaisesRegex(ValueError, 'Capture ended with an error'):
        solve_directory(directory, directory / 'new.json', 25)

  def test_insufficient_and_repeated_views_are_rejected(self):
    view = np.zeros((54, 1, 2), dtype=np.float32)
    for views in [[view] * 3, [view] * 12]:
      with self.assertRaises(ValueError):
        solve(views, (1280, 720), 25)
    with self.assertRaises(ValueError):
      object_points(0)


if __name__ == '__main__':
  unittest.main()
