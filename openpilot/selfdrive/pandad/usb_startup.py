"""Pure USB-only startup selection; no device client, environment writes or defaults."""
from collections.abc import Mapping


def usb_status_command(radxa: bool, environ: Mapping[str, str], executable: str) -> list[str] | None:
  keys = ('PANDAD_USB_SERIAL', 'PANDAD_USB_VERSION')
  if not radxa and not any(key in environ for key in keys):
    return None
  serial, version = (environ.get(key, '') for key in keys)
  if not 1 <= len(serial) <= 64 or not all('!' <= ch <= '~' for ch in serial):
    raise ValueError('USB startup requires PANDAD_USB_SERIAL (1..64 printable non-space ASCII characters)')
  if not 1 <= len(version) <= 64 or not all(' ' <= ch <= '~' for ch in version):
    raise ValueError('USB startup requires PANDAD_USB_VERSION (exact printable ASCII firmware version, at most64 bytes)')
  return [executable, '--usb-status', serial, version]
