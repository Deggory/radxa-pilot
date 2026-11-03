from opendbc.car.crc import CRC8J1850


def ocelot_checksum(address: int, sig, data: bytearray) -> int:
  """RetroPilot/opendbc 6b90fafe: CRC-8/SAE-J1850, excluding byte zero."""
  crc = 0xFF
  for byte in data[1:]:
    crc = CRC8J1850[crc ^ byte]
  return crc ^ 0xFF
