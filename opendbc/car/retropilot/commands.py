"""Offline canonical encoders. No device access or normalized-control calibration.

These helpers are intentionally not called by the receive-only CarController.
Explicit channels, physical targets, modes, counters and host buses are required.
"""
import math


def _command(packer, name, bus, counter, values, zero_fields=()):
  if packer.dbc.name != 'ocelot_controls':
    raise ValueError('RetroPilot commands require the canonical ocelot_controls DBC')
  if not isinstance(bus, int) or not 0 <= bus <= 3:
    raise ValueError('Host CAN bus must be an integer from 0 to 3')
  if not isinstance(counter, int) or not 0 <= counter < 16:
    raise ValueError('Counter must be an integer from 0 to 15')
  if 'ENABLE' in values and type(values['ENABLE']) is not bool:
    raise ValueError('Enable must be an explicit boolean')
  # CANPacker intentionally wraps fields. Reject invalid engineering inputs
  # before packing, including disabled requests, instead of wrapping them.
  for field, value in values.items():
    sig = packer.dbc.name_to_msg[name].sigs[field]
    if not math.isfinite(value):
      raise ValueError(f'{field} must be finite')
    raw = math.floor((value - sig.offset) / sig.factor + 0.5)
    lower = -(1 << (sig.size - 1)) if sig.is_signed else 0
    upper = (1 << (sig.size - int(sig.is_signed))) - 1
    if not lower <= raw <= upper:
      raise ValueError(f'{field} exceeds its canonical encoded range')
  values = dict(values, COUNTER=counter)
  for field in zero_fields:
    values[field] = 0
  return packer.make_can_msg(name, bus, values)


def steering_interceptor(packer, bus, enabled, channel1, channel2, counter):
  """Raw two-channel request; no assumed 1510-center or torque-to-ADC law."""
  values = {'ENABLE': enabled, 'TORQUE_COMMAND1': channel1, 'TORQUE_COMMAND2': channel2}
  return _command(packer, 'INTERCEPTOR_STEERING_COMMAND', bus, counter, values,
                  () if enabled else ('TORQUE_COMMAND1', 'TORQUE_COMMAND2'))


def steering_actuator(packer, bus, mode, torque_nm, angle_deg, counter):
  """The caller supplies the endpoint's confirmed raw mode; zero disables."""
  if not isinstance(mode, int) or not 0 <= mode <= 3:
    raise ValueError('Steering mode must fit its two-bit field')
  values = {'STEER_MODE': mode, 'REQUESTED_STEER_TORQUE': torque_nm, 'REQUESTED_STEER_ANGLE': angle_deg}
  return _command(packer, 'ACTUATOR_STEERING_COMMAND', bus, counter, values,
                  () if mode else ('REQUESTED_STEER_TORQUE', 'REQUESTED_STEER_ANGLE'))


def steering_ssc(packer, bus, mode, torque_nm, angle_deg, counter):
  if not isinstance(mode, int) or not 0 <= mode <= 3:
    raise ValueError('Steering mode must fit its two-bit field')
  values = {'STEER_MODE': mode, 'STEER_TORQUE': torque_nm, 'STEER_ANGLE': angle_deg}
  return _command(packer, 'STEERING_COMMAND_SSC', bus, counter, values,
                  () if mode else ('STEER_TORQUE', 'STEER_ANGLE'))


def gas(packer, bus, enabled, channel1, channel2, counter, *, actuator=False):
  name = 'ACTUATOR_GAS_COMMAND' if actuator else 'PEDAL_GAS_COMMAND'
  fields = ('THROTTLE_REQ', 'THROTTLE_REQ2') if actuator else ('GAS_COMMAND', 'GAS_COMMAND2')
  values = {'ENABLE': enabled, fields[0]: channel1, fields[1]: channel2}
  return _command(packer, name, bus, counter, values, () if enabled else fields)


def brake(packer, bus, mode, position_mm, relative_command, counter, *, ibooster=False):
  if not isinstance(mode, int) or mode not in (0, 1, 2):
    raise ValueError('Brake mode must be disabled, relative or position; 3 is reserved')
  name = 'IBOOSTER_BRAKE_COMMAND' if ibooster else 'ACTUATOR_BRAKE_COMMAND'
  fields = ('BRAKE_POSITION_COMMAND', 'BRAKE_RELATIVE_COMMAND')
  values = {'BRAKE_MODE': mode, fields[0]: position_mm, fields[1]: relative_command}
  return _command(packer, name, bus, counter, values, () if mode else fields)


def relay(packer, bus, enabled, relay_bits, counter):
  return _command(packer, 'RELAY_CORE_COMMAND', bus, counter,
                  {'ENABLE': enabled, 'RELAY_COMMAND': relay_bits}, () if enabled else ('RELAY_COMMAND',))
