from typing import cast

from openpilot.common.hardware.base import HardwareBase
from openpilot.common.hardware.comma.hardware import HardwareComma
from openpilot.common.hardware.pc.hardware import HardwarePc
from openpilot.common.hardware.radxa.hardware import HardwareRadxa
from openpilot.common.platform import AGNOS as AGNOS, PC as PC
from openpilot.common.platform import COMMA_HARDWARE, RADXA_Q8B

if COMMA_HARDWARE:
  HARDWARE = cast(HardwareBase, HardwareComma())
elif RADXA_Q8B:
  HARDWARE = cast(HardwareBase, HardwareRadxa())
else:
  HARDWARE = cast(HardwareBase, HardwarePc())
