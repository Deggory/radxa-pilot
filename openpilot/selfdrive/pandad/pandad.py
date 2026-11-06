#!/usr/bin/env python3
"""Pinned USB launcher. Device initialization belongs to the native USB session."""
import os

from openpilot.common.basedir import BASEDIR
from openpilot.selfdrive.pandad.usb_startup import usb_status_command


def main() -> None:
  command = usb_status_command(os.environ, os.path.join(BASEDIR, 'openpilot/selfdrive/pandad/pandad'))
  os.execv(command[0], command)
  raise RuntimeError('USB startup exec returned without replacing the process')


if __name__ == '__main__':
  main()
