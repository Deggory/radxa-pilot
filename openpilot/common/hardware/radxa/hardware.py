"""Q8B identity; hardware operations retain generic Linux defaults for now."""
import platform

from openpilot.common.hardware.pc.hardware import HardwarePc


class HardwareRadxa(HardwarePc):
  def get_device_type(self):
    return 'radxaQ8b'

  def get_name(self):
    return 'Radxa Dragon Q8B'

  def get_os_version(self):
    try:
      return platform.freedesktop_os_release().get('PRETTY_NAME', platform.system())
    except OSError:
      return platform.system()
