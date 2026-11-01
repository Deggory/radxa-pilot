"""Print platform identity without initializing hardware or starting services."""
import platform

from openpilot.common.hardware import HARDWARE, PC


def main():
  machine = platform.machine()
  architecture = f'ARM64 ({machine})' if machine == 'aarch64' else machine
  board = HARDWARE.get_name() if hasattr(HARDWARE, 'get_name') else HARDWARE.get_device_type()
  print(f'Operating system: {HARDWARE.get_os_version() or platform.system()} ({platform.system()})')
  print(f'CPU architecture: {architecture}')
  print(f'Board: {board}')
  print(f'Device type: {HARDWARE.get_device_type()}')
  print(f'Linux development policy (PC): {PC}')


if __name__ == '__main__':
  main()
