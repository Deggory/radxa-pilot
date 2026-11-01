"""Platform identity without application imports, also usable by the build."""
import os
import platform
from pathlib import Path


def is_radxa_q8b(compatible_path: Path = Path('/sys/firmware/devicetree/base/compatible')) -> bool:
  if platform.system() != 'Linux' or platform.machine() != 'aarch64':
    return False
  try:
    return b'radxa,dragon-q8b' in compatible_path.read_bytes().split(b'\0')
  except OSError:
    return False


AGNOS = os.path.isfile('/AGNOS')
COMMA_HARDWARE = AGNOS
PC = not COMMA_HARDWARE
RADXA_Q8B = not COMMA_HARDWARE and is_radxa_q8b()
