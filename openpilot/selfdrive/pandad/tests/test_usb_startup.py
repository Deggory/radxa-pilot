import os
import unittest
from unittest.mock import patch

from openpilot.selfdrive.pandad.usb_startup import usb_status_command


class ReplacedProcess(BaseException):
  pass


class UsbStartupTests(unittest.TestCase):
  def test_requires_both_pins_for_radxa_or_any_usb_request(self):
    self.assertIsNone(usb_status_command(False, {}, '/native/pandad'))
    for env in ({}, {'PANDAD_USB_SERIAL': 'selected'}, {'PANDAD_USB_VERSION': 'version'},
                {'PANDAD_USB_SERIAL': '', 'PANDAD_USB_VERSION': 'version'}):
      with self.subTest(env=env), self.assertRaises(ValueError):
        usb_status_command(True, env, '/native/pandad')
    for key in ('PANDAD_USB_SERIAL', 'PANDAD_USB_VERSION'):
      with self.assertRaises(ValueError):
        usb_status_command(False, {key: ''}, '/native/pandad')

  def test_exact_arguments_without_shell_or_historical_defaults(self):
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned version $(literal)'}
    expected = ['/native/pandad', '--usb-status', 'selected', 'pinned version $(literal)']
    self.assertEqual(usb_status_command(True, env, expected[0]), expected)
    self.assertEqual(usb_status_command(False, env, expected[0]), expected)
    for field in env:
      for invalid in ('', 'x' * 65, 'bad\nvalue', 'bad\x00value', '\u00e9'):
        with self.subTest(field=field, invalid=invalid), self.assertRaises(ValueError):
          usb_status_command(True, {**env, field: invalid}, expected[0])
    with self.assertRaises(ValueError):
      usb_status_command(True, {**env, 'PANDAD_USB_SERIAL': 'has space'}, expected[0])

  def test_wrapper_executes_usb_before_any_legacy_probe_or_recovery(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned'}
    with patch.dict(os.environ, env, clear=True), patch.object(wrapper, 'RADXA_Q8B', True), \
         patch.object(wrapper.os, 'execv', side_effect=ReplacedProcess) as execute, \
         patch.object(wrapper, 'Panda') as panda, patch.object(wrapper, 'PandaDFU') as dfu, \
         patch.object(wrapper, 'HARDWARE') as hardware, patch.object(wrapper.subprocess, 'Popen') as popen:
      with self.assertRaises(ReplacedProcess):
        wrapper.main()
      command = execute.call_args.args[1]
      self.assertEqual(command[1:], ['--usb-status', 'selected', 'pinned'])
      self.assertEqual(execute.call_args.args[0], command[0])
      self.assertEqual(panda.mock_calls + dfu.mock_calls + hardware.mock_calls + popen.mock_calls, [])

  def test_wrapper_never_falls_through_on_missing_pins_or_exec_failure(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    for env in ({}, {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned'}):
      with patch.dict(os.environ, env, clear=True), patch.object(wrapper, 'RADXA_Q8B', True), \
           patch.object(wrapper.os, 'execv', side_effect=OSError('exec failed')), \
           patch.object(wrapper, 'Panda') as panda, patch.object(wrapper, 'PandaDFU') as dfu, \
           patch.object(wrapper, 'HARDWARE') as hardware:
        with self.assertRaises((ValueError, OSError)):
          wrapper.main()
        self.assertEqual(panda.mock_calls + dfu.mock_calls + hardware.mock_calls, [])

  def test_returning_exec_is_an_error_and_never_enters_legacy_path(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    env = {'PANDAD_USB_SERIAL': 'selected', 'PANDAD_USB_VERSION': 'pinned'}
    with patch.dict(os.environ, env, clear=True), patch.object(wrapper, 'RADXA_Q8B', True), \
         patch.object(wrapper.os, 'execv'), patch.object(wrapper, 'Panda') as panda:
      with self.assertRaises(RuntimeError):
        wrapper.main()
      self.assertEqual(panda.mock_calls, [])

  def test_non_radxa_without_usb_pins_retains_legacy_entry(self):
    from openpilot.selfdrive.pandad import pandad as wrapper
    with patch.dict(os.environ, {}, clear=True), patch.object(wrapper, 'RADXA_Q8B', False), \
         patch.object(wrapper.os, 'execv') as execute, patch.object(wrapper.signal, 'signal'), \
         patch.object(wrapper.Panda, 'list', side_effect=ReplacedProcess):
      with self.assertRaises(ReplacedProcess):
        wrapper.main()
      execute.assert_not_called()


if __name__ == '__main__':
  unittest.main()
