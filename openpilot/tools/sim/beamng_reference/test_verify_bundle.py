"""Source-loss and metadata corruption regressions for the bundle verifier."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestVerifyBundle(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp.cleanup)
    self.root = Path(self.temp.name)
    shutil.copyfile(Path(__file__).with_name('verify_bundle.py'), self.root / 'verify_bundle.py')
    self.source = self.root / 'upstream/sample.py'
    self.source.parent.mkdir()
    self.source.write_bytes(b'')
    self.source.chmod(0o644)
    # Known Git empty-blob and SHA-256 empty-input identities.
    self.entry = {'path': 'upstream/sample.py', 'bytes': 0, 'source_mode': '100644',
                  'git_blob_sha1': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
                  'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
    self.manifest = {'repository': 'https://github.com/Caleb-J773/beampilot-drive',
                     'source_commit': '5435d67499f66eca58f95882cbe35e9c577e874c', 'files': [self.entry]}
    self.save_manifest()
    (self.root / 'SHA256SUMS').write_text(f"{self.entry['sha256']}  {self.entry['path']}\n")

  def save_manifest(self):
    (self.root / 'MANIFEST.json').write_text(json.dumps(self.manifest))

  def result(self):
    return subprocess.run([sys.executable, str(self.root / 'verify_bundle.py')], capture_output=True, text=True)

  def rejected(self):
    self.assertNotEqual(self.result().returncode, 0)

  def test_pristine_fixture_passes(self):
    result = self.result()
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)['files'], 1)

  def test_empty_snapshot_is_rejected(self):
    self.source.unlink()
    self.manifest['files'] = []
    self.save_manifest()
    (self.root / 'SHA256SUMS').write_text('')
    self.rejected()

  def test_missing_directory_is_rejected(self):
    shutil.rmtree(self.source.parent)
    self.manifest['files'] = []
    self.save_manifest()
    (self.root / 'SHA256SUMS').write_text('')
    self.rejected()

  def test_wrong_origin_is_rejected(self):
    self.manifest['repository'] = 'https://example.invalid/other'
    self.save_manifest()
    self.rejected()

  def test_wrong_pin_is_rejected(self):
    self.manifest['source_commit'] = '0' * 40
    self.save_manifest()
    self.rejected()

  def test_mismatched_checksum_list_is_rejected(self):
    (self.root / 'SHA256SUMS').write_text('')
    self.rejected()

  def test_changed_source_is_rejected(self):
    self.source.write_text('changed')
    self.rejected()

  def test_extra_source_is_rejected(self):
    self.source.with_name('extra.py').write_text('extra')
    self.rejected()

  def test_source_symlink_is_rejected(self):
    self.source.unlink()
    self.source.symlink_to(self.root / 'verify_bundle.py')
    self.rejected()

  def test_changed_mode_is_rejected(self):
    self.source.chmod(0o755)
    self.rejected()

  def test_duplicate_source_is_rejected(self):
    self.manifest['files'].append(self.entry)
    self.save_manifest()
    self.rejected()

  def test_escaped_manifest_path_is_rejected(self):
    self.entry['path'] = '../escape.py'
    self.save_manifest()
    self.rejected()


if __name__ == '__main__':
  unittest.main()
