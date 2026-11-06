import ast
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from openpilot.selfdrive.pandad.usb_startup import usb_status_command


class ReplacedProcess(BaseException):
  pass


class UsbStartupTests(unittest.TestCase):
  def test_requires_both_pins_on_every_platform(self):
    for env in ({}, {'PANDAD_USB_SERIAL': 'selected'}, {'PANDAD_USB_VERSION': 'version'},
                {'PANDAD_USB_SERIAL': '', 'PANDAD_USB_VERSION': 'version'}):
      with self.subTest(env=env), self.assertRaises(ValueError):
        usb_status_command(env, '/native/pandad')

  def test_exact_arguments_without_shell_or_historical_defaults(self):
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned version $(literal)'}
    expected = ['/native/pandad', '--usb-status', 'selected', 'pinned version $(literal)']
    self.assertEqual(usb_status_command(env, expected[0]), expected)
    for field in env:
      for invalid in ('', 'x' * 65, 'bad\nvalue', 'bad\x00value', '\u00e9'):
        with self.subTest(field=field, invalid=invalid), self.assertRaises(ValueError):
          usb_status_command({**env, field: invalid}, expected[0])
    with self.assertRaises(ValueError):
      usb_status_command({**env, 'PANDAD_USB_SERIAL': 'has space'}, expected[0])

  def test_wrapper_executes_only_explicit_usb_command(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned'}
    with patch.dict(os.environ, env, clear=True), patch.object(wrapper.os, 'execv', side_effect=ReplacedProcess) as execute:
      with self.assertRaises(ReplacedProcess):
        wrapper.main()
      command = execute.call_args.args[1]
      self.assertEqual(command[1:], ['--usb-status', 'selected', 'pinned'])
      self.assertEqual(execute.call_args.args[0], command[0])

  def test_wrapper_rejects_missing_pins_without_exec(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    with patch.dict(os.environ, {}, clear=True), patch.object(wrapper.os, 'execv') as execute:
      with self.assertRaises(ValueError):
        wrapper.main()
      execute.assert_not_called()

  def test_exec_failure_and_return_never_start_another_backend(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned'}
    with patch.dict(os.environ, env, clear=True), patch.object(wrapper.os, 'execv', side_effect=OSError('exec failed')):
      with self.assertRaises(OSError):
        wrapper.main()
    with patch.dict(os.environ, env, clear=True), patch.object(wrapper.os, 'execv'):
      with self.assertRaises(RuntimeError):
        wrapper.main()

  def test_wrapper_cannot_import_legacy_device_or_recovery_clients(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    tree = ast.parse(Path(wrapper.__file__).read_text())
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    imported |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    self.assertEqual(imported, {'os', 'openpilot.common.basedir', 'openpilot.selfdrive.pandad.usb_startup'})

  def test_no_spi_backend_source_class_or_build_target(self):
    root = Path(__file__).resolve().parents[1]
    self.assertFalse((root / 'spi.cc').exists())
    self.assertNotIn('PandaSpiHandle', (root / 'panda_comms.h').read_text())
    self.assertNotIn("'spi.cc'", (root / 'SConscript').read_text())
    self.assertNotIn('PandaSpiHandle', (root / 'panda.cc').read_text())
    self.assertNotIn('Panda::list()', (root / 'panda.cc').read_text())


if __name__ == '__main__':
  unittest.main()
