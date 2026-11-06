# SPDX-License-Identifier: MIT
"""Pure decoder for the new Chimera bootstrap's A0/D6 replies.

This is discovery data, not Panda health or admission to managed pandad. No USB
access, measurements, configuration, readiness or safety authority is supplied.
Original Chimera mailbox16/health43 remains in chimera_protocol.py.
"""
from dataclasses import dataclass
import struct

_MANIFEST = struct.Struct('<4s4B3I4BH6s')
_VERSION = b'chimera-f413-bootstrap-v1'
_INTERFACES = ('IGN', 'VSS', 'CPS', 'BRAKE', 'ADC1', 'ADC2', 'RELAY', 'OBDC_REQUEST', 'OBDC_IGNITION')


@dataclass(frozen=True)
class ChimeraBootstrapIdentity:
  firmware_version: str
  physical_bus_count: int
  classical_payload_max: int
  physical_interfaces: tuple[str, ...]
  operational_capabilities: int
  active_can_layout_hash: int
  active_health_layout_hash: int


def decode_bootstrap_identity(manifest: bytes, version: bytes) -> ChimeraBootstrapIdentity:
  """Require this exact phase-zero contract; unknown/future profiles fail closed.

  Arguments are complete A0 and D6 response bytes with no padding/NUL. The caller
  owns descriptor/serial/transport checks. A decoded identity grants no operation
  and does not authenticate hardware, firmware or physical interface readiness.
  """
  if not isinstance(manifest, bytes) or not isinstance(version, bytes):
    raise TypeError('Chimera identity responses must be bytes')
  if len(manifest) != _MANIFEST.size:
    raise ValueError('Expected complete Chimera manifest32')
  if version != _VERSION:
    raise ValueError('Unsupported Chimera bootstrap version')
  (magic, schema, length, family, phase, capabilities, can_hash, health_hash,
   buses, payload_max, auto_update, config_abi, interfaces, reserved) = _MANIFEST.unpack(manifest)
  if (magic, schema, length, family) != (b'CHMR', 1, 32, 1):
    raise ValueError('Unsupported Chimera manifest identity/schema')
  if (phase, capabilities, can_hash, health_hash, auto_update, config_abi) != (0, 0, 0, 0, 0, 0):
    raise ValueError('Unsupported Chimera operational profile; bootstrap only')
  if (buses, payload_max, interfaces) != (3, 8, 0x01ff) or reserved != bytes(6):
    raise ValueError('Unsupported Chimera topology or reserved fields')
  return ChimeraBootstrapIdentity(version.decode('ascii'), buses, payload_max,
                                 tuple(name for bit, name in enumerate(_INTERFACES) if interfaces & (1 << bit)),
                                 capabilities, can_hash, health_hash)
