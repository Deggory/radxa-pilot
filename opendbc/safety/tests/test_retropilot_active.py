"""Compiled policy engine with artificial limits, never a vehicle calibration."""
import os
import unittest

from opendbc.car.retropilot import commands
from opendbc.car.structs import CarParams
from opendbc.safety.tests import common
from opendbc.safety.tests.libsafety import libsafety_py
from opendbc.safety.tests.test_retropilot import DISABLED, packet


class TestRetroPilotActive(common.SafetyTestBase):
  SAFETY_MODEL = CarParams.SafetyModel.retropilot
  DBC = 'ocelot_controls'
  RX = {
    'STEER_ANGLE_SENSOR': {'STATE': 1},
    'ENGINE': {'IGNITION_ON': 1},
    'SPEED': {'CAN_SPEED': 1000},
    'INTERCEPTOR_STEERING_SENSOR': {},
    'PEDAL_GAS_SENSOR': {},
    'IBOOSTER_BRAKE_STATUS': {'BRAKE_OK': 1},
    'CRUISE': {},
  }

  def setUp(self):
    super().setUp()
    # Only the native debug harness can supply this synthetic profile.
    self.assertTrue(self.safety.set_retropilot_test_profile(0))
    self.now = 0
    self.rx_counters = dict.fromkeys(self.RX, 0)
    self.tx_counters = dict.fromkeys(('steer', 'gas', 'brake'), 0)

  def rx_msg(self, name, **values):
    data = dict(self.RX[name], **values, COUNTER=self.rx_counters[name])
    self.rx_counters[name] = (self.rx_counters[name] + 1) % 16
    return self.packer.make_can_msg_safety(name, 2, data)

  def cycle(self, changes=None, skip=(), dt=50000):
    self.now = (self.now + dt) & 0xFFFFFFFF
    self.safety.set_timer(self.now)
    for name in self.RX:
      if name not in skip:
        self._rx(self.rx_msg(name, **(changes or {}).get(name, {})))

  def engage(self):
    # A full modulo16 cycle reaches an unknown endpoint counter even when
    # the decoder does NOT seed its counter from rejected sequences.
    for counter in range(16):
      for addr in (0x300, 0x200, 0x20E):
        data = bytearray(DISABLED[addr])
        data[1 if addr == 0x20E else 5] |= counter
        self.assertTrue(self._tx(packet(addr, data)))
    self.cycle()
    self.cycle()
    self.cycle({'CRUISE': {'ON_OFF': 1}})
    self.cycle()
    self.cycle({'CRUISE': {'SET_DOWN': 1}})
    self.cycle()
    self.assertTrue(self.safety.get_controls_allowed())

  def command(self, kind, value=0, counter=None, **overrides):
    cnt = self.tx_counters[kind] if counter is None else counter
    self.tx_counters[kind] = (cnt + 1) % 16
    if kind == 'steer':
      args = dict(bus=2, enabled=True, channel1=1000 + value, channel2=1000 - value, counter=cnt)
      func = commands.steering_interceptor
    elif kind == 'gas':
      args = dict(bus=2, enabled=True, channel1=10 + value, channel2=20 + 2 * value, counter=cnt)
      func = commands.gas
    else:
      args = dict(bus=2, mode=2, position_mm=value / 64, relative_command=0, counter=cnt, ibooster=True)
      func = commands.brake
    addr, data, bus = func(self.packer, **dict(args, **overrides))
    return common.make_msg(bus, addr, dat=data)

  def test_valid_active_commands(self):
    for kind, value in (('steer', 5), ('gas', 20), ('brake', 16)):
      with self.subTest(kind=kind):
        self.setUp()
        self.engage()
        self.assertTrue(self._tx(self.command(kind, value)))

  def test_forced_controls_cannot_bypass_startup(self):
    self.safety.set_controls_allowed(True)
    for kind in self.tx_counters:
      self.assertFalse(self._tx(self.command(kind)))

  def test_set_alone_and_held_startup_buttons_do_not_engage(self):
    for button in ('SET_DOWN', 'RES_UP', 'ON_OFF'):
      self.setUp()
      for _ in range(6):
        self.cycle({'CRUISE': {button: 1}})
        self.assertFalse(self.safety.get_controls_allowed())
      self.cycle()
      self.cycle({'CRUISE': {'SET_DOWN': 1}})
      self.assertFalse(self.safety.get_controls_allowed())

  def test_cancel_requires_new_edge(self):
    self.engage()
    self.cycle({'CRUISE': {'CANCEL': 1, 'SET_DOWN': 1}})
    self.assertFalse(self.safety.get_controls_allowed())
    self.cycle({'CRUISE': {'SET_DOWN': 1}})
    self.assertFalse(self.safety.get_controls_allowed())
    self.cycle()
    self.cycle({'CRUISE': {'RES_UP': 1}})
    self.assertTrue(self.safety.get_controls_allowed())

  def test_on_off_disengages(self):
    self.engage()
    self.cycle({'CRUISE': {'ON_OFF': 1}})
    self.assertFalse(self.safety.get_controls_allowed())

  def test_driver_takeover_and_faults(self):
    cases = [('ENGINE', {'BRAKE_PRESSED': 1}), ('ENGINE', {'IGNITION_ON': 0}),
             ('PEDAL_GAS_SENSOR', {'PED_GAS': 101}), ('PEDAL_GAS_SENSOR', {'PED_GAS2': 101}),
             ('IBOOSTER_BRAKE_STATUS', {'DRIVER_BRAKE_APPLIED': 1}),
             ('INTERCEPTOR_STEERING_SENSOR', {'OVERRIDE': 1}),
             ('INTERCEPTOR_STEERING_SENSOR', {'STATE': 1}), ('PEDAL_GAS_SENSOR', {'STATE': 1}),
             ('IBOOSTER_BRAKE_STATUS', {'BRAKE_OK': 0}), ('IBOOSTER_BRAKE_STATUS', {'STATUS': 1}),
             ('IBOOSTER_BRAKE_STATUS', {'EXT_STATUS1': 1}), ('STEER_ANGLE_SENSOR', {'STATE': 0}),
             ('STEER_ANGLE_SENSOR', {'STEER_ANGLE': 100.1}), ('STEER_ANGLE_SENSOR', {'STEER_RATE': 501}),
             ('SPEED', {'CAN_SPEED': 5001}), ('ENGINE', {'MODE': 5}), ('CRUISE', {'MODE': 5}),
             ('SPEED', {'MODE': 1})]
    for name, values in cases:
      with self.subTest(name=name, values=values):
        self.setUp()
        self.engage()
        self.cycle({name: values})
        self.assertFalse(self.safety.get_controls_allowed())
        self.assertFalse(self._tx(self.command('steer')))
        self.cycle()
        self.assertFalse(self.safety.get_controls_allowed())

  def test_own_brake_status_does_not_mean_driver_takeover(self):
    self.engage()
    self.cycle({'IBOOSTER_BRAKE_STATUS': {'BRAKE_APPLIED': 1}})
    self.assertTrue(self.safety.get_controls_allowed())

  def test_each_missing_or_stale_message_blocks_output(self):
    for name in self.RX:
      with self.subTest(name=name):
        self.setUp()
        self.engage()
        for _ in range(3):
          self.cycle(skip=(name,))
        self.assertFalse(self._tx(self.command('steer')))
        self.assertFalse(self.safety.get_controls_allowed())

  def test_stale_input_checked_at_tx_without_rx_or_tick(self):
    self.engage()
    self.safety.set_timer(self.now + 100001)
    self.assertFalse(self._tx(self.command('steer')))
    self.assertFalse(self.safety.get_controls_allowed())

  def test_late_frame_cannot_hide_its_own_timeout(self):
    self.engage()
    for _ in range(2):
      self.cycle(skip=('SPEED',))
    self.safety.set_timer(self.now + 1)
    self._rx(self.rx_msg('SPEED'))
    self.assertFalse(self._tx(self.command('steer')))

  def test_bad_checksum_counter_and_metadata(self):
    for name in self.RX:
      for fault in ('crc', 'counter', 'fd', 'extended', 'returned', 'rejected'):
        with self.subTest(name=name, fault=fault):
          self.setUp()
          self.engage()
          if fault == 'counter':
            self.rx_counters[name] = (self.rx_counters[name] - 1) % 16
          msg = self.rx_msg(name)
          if fault == 'crc':
            msg[0].data[0] ^= 1
          elif fault != 'counter':
            setattr(msg[0], fault, 1)
          self._rx(msg)
          self.assertFalse(self._tx(self.command('steer')))

  def test_corrupt_rx_latches_fault_even_if_shared_flag_is_forced(self):
    self.engage()
    self.rx_counters['SPEED'] = (self.rx_counters['SPEED'] - 1) % 16
    bad = self.rx_msg('SPEED')
    bad[0].data[0] ^= 1
    self.assertFalse(self._rx(bad))
    self.safety.set_controls_allowed(True)
    self._rx(self.rx_msg('SPEED'))
    self.cycle()
    self.safety.set_controls_allowed(True)
    self.assertFalse(self._tx(self.command('steer', 5)))

  def test_wrong_bus_and_dlc_do_not_refresh_rx(self):
    for fault in ('bus', 'dlc'):
      for name in self.RX:
        self.setUp()
        self.engage()
        for _ in range(3):
          self.cycle(skip=(name,))
          msg = self.rx_msg(name)
          if fault == 'bus':
            msg[0].bus = 0
          else:
            msg[0].data_len_code = 4
          self._rx(msg)
        self.assertFalse(self._tx(self.command('steer')))

  def test_invalid_command_disengages_and_disabled_release_is_allowed(self):
    for kind, values in (('steer', {'value': 6}), ('gas', {'value': 21}), ('brake', {'value': 17}),
                         ('steer', {'channel2': 999}), ('gas', {'channel2': 23}),
                         ('brake', {'mode': 1}), ('brake', {'relative_command': 1})):
      self.setUp()
      self.engage()
      self.assertFalse(self._tx(self.command(kind, **values)), (kind, values))
      self.assertFalse(self.safety.get_controls_allowed())
      for addr, data in DISABLED.items():
        self.assertTrue(self._tx(packet(addr, data)))

  def test_steering_ramp_real_time_limit_and_speed_taper(self):
    self.engage()
    for val in (5, 10, 15, 20):
      self.assertTrue(self._tx(self.command('steer', val)))
      self.cycle(dt=10000)
    self.assertFalse(self._tx(self.command('steer', 25)))  # 250ms delta max20
    self.setUp()
    self.engage()
    for val in range(5, 31, 5):
      self.cycle(dt=50000)
      self.assertTrue(self._tx(self.command('steer', val)))
    self.cycle({'SPEED': {'CAN_SPEED': 5000}})
    self.assertFalse(self._tx(self.command('steer', 30)))  # high-speed max25

  def test_command_min_interval_and_counter_progress(self):
    for kind in self.tx_counters:
      for fault in ('early', 'repeat', 'skip'):
        self.setUp()
        self.engage()
        self.assertTrue(self._tx(self.command(kind)))
        if fault != 'early':
          self.cycle()
        counter = {'early': 1, 'repeat': 0, 'skip': 2}[fault]
        self.assertFalse(self._tx(self.command(kind, counter=counter)), (kind, fault))

  def test_counter_and_timer_wrap(self):
    self.now = 0xFFFB0000
    self.engage()
    for _ in range(20):
      self.cycle(dt=20000)
      for kind in self.tx_counters:
        self.assertTrue(self._tx(self.command(kind)), kind)

  def test_pedal_interlock_and_release_order(self):
    for first, second in (('gas', 'brake'), ('brake', 'gas')):
      self.setUp()
      self.engage()
      self.assertTrue(self._tx(self.command(first, 1)))
      self.assertFalse(self._tx(self.command(second, 1)))
      self.setUp()
      self.engage()
      self.assertTrue(self._tx(self.command(first, 1)))
      self.cycle()
      self.assertTrue(self._tx(self.command(first, 0)))
      self.assertTrue(self._tx(self.command(second, 1)))

  def test_blocked_release_does_not_erase_outstanding_pedal(self):
    self.engage()
    self.assertTrue(self._tx(self.command('gas', 1)))
    self.safety.set_relay_malfunction(True)
    self.assertFalse(self._tx(packet(0x200, DISABLED[0x200])))
    self.assertFalse(self.safety.get_controls_allowed())
    self.safety.set_relay_malfunction(False)
    # Fault recovery must retain the previously accepted gas until a release
    # actually passes the complete framework, even after fresh ON and SET.
    self.cycle()
    self.cycle({'CRUISE': {'ON_OFF': 1}})
    self.cycle()
    self.cycle({'CRUISE': {'SET_DOWN': 1}})
    self.assertFalse(self._tx(self.command('brake', 1)))

  def test_replayed_or_skipped_release_does_not_credit_pedal_release(self):
    for first, second, addr in (('gas', 'brake', 0x200), ('brake', 'gas', 0x20E)):
      for counter in (0, 2, 15):
        self.setUp()
        self.engage()
        self.assertTrue(self._tx(self.command(first, 1)))
        data = bytearray(DISABLED[addr])
        data[1 if first == 'brake' else 5] |= counter
        self.assertFalse(self._tx(packet(addr, data)))
        self.assertFalse(self._tx(self.command(second, 1)))

  def test_startup_requires_full_counter_cycle_before_engagement(self):
    for count in (0, 1, 2, 15):
      self.setUp()
      for counter in range(count):
        for addr in (0x300, 0x200, 0x20E):
          data = bytearray(DISABLED[addr])
          data[1 if addr == 0x20E else 5] |= counter
          self.assertTrue(self._tx(packet(addr, data)))
      self.cycle()
      self.cycle()
      self.cycle({'CRUISE': {'ON_OFF': 1}})
      self.cycle()
      self.cycle({'CRUISE': {'SET_DOWN': 1}})
      self.assertFalse(self.safety.get_controls_allowed())

  def test_active_limits_after_gradual_ramp(self):
    for kind, limit, step in (('gas', 1000, 20), ('brake', 128, 16)):
      self.setUp()
      self.engage()
      for value in range(step, limit + 1, step):
        self.cycle()
        self.assertTrue(self._tx(self.command(kind, value)), (kind, value))
      self.cycle()
      self.assertFalse(self._tx(self.command(kind, limit + 1)))

  def test_steering_negative_ramp_unwind_and_sign_change(self):
    self.engage()
    for value in (-5, -10, -15, -20):
      self.cycle(dt=10000)
      self.assertTrue(self._tx(self.command('steer', value)))
    self.cycle(dt=10000)
    self.assertFalse(self._tx(self.command('steer', -9)))  # unwind max10
    self.setUp()
    self.engage()
    self.assertTrue(self._tx(self.command('steer', -5)))
    self.cycle(dt=10000)
    self.assertTrue(self._tx(self.command('steer', 5)))

  def test_fault_recovery_needs_release_then_new_buttons(self):
    self.engage()
    self.assertTrue(self._tx(self.command('steer', 5)))
    self.cycle({'INTERCEPTOR_STEERING_SENSOR': {'OVERRIDE': 1}})
    self.cycle()
    self.cycle({'CRUISE': {'ON_OFF': 1}})
    self.cycle()
    self.cycle({'CRUISE': {'SET_DOWN': 1}})
    self.assertFalse(self.safety.get_controls_allowed())
    data = bytearray(DISABLED[0x300])
    data[5] = 1  # Sequential release after the accepted active counter0.
    self.assertTrue(self._tx(packet(0x300, data)))
    self.cycle()
    self.cycle({'CRUISE': {'RES_UP': 1}})
    self.assertTrue(self.safety.get_controls_allowed())

  def test_tx_metadata_and_reserved_bits(self):
    for kind in self.tx_counters:
      for fault in ('fd', 'extended', 'returned', 'rejected', 'crc', 'reserved'):
        self.setUp()
        self.engage()
        msg = self.command(kind)
        if fault == 'crc':
          msg[0].data[0] ^= 1
        elif fault == 'reserved':
          data = bytearray(bytes(msg[0].data)[:6])
          data[5 if kind != 'brake' else 1] |= 0x40
          msg = packet(msg[0].addr, data)
        else:
          setattr(msg[0], fault, 1)
        self.assertFalse(self._tx(msg), (kind, fault))
        self.assertFalse(self.safety.get_controls_allowed())

  def test_nonselected_endpoints_remain_disabled_only(self):
    self.engage()
    for addr in (0x10E, 0x12E, 0x22E, 0x400):
      data = bytearray(DISABLED[addr])
      data[1 if addr in (0x10E, 0x12E, 0x22E) else 5] |= 0x10 if addr != 0x400 else 0x80
      self.assertFalse(self._tx(packet(addr, data)))

  def test_invalid_profiles_fail_closed(self):
    for invalid_case in range(1, 10):
      self.assertFalse(self.safety.set_retropilot_test_profile(invalid_case))
      self.safety.set_controls_allowed(True)
      self.assertFalse(self._tx(self.command('steer')))

  def test_mode_switch_clears_profile_and_engagement(self):
    self.engage()
    for param in (0, 1, 0xFFFF):
      self.safety.set_safety_hooks(CarParams.SafetyModel.noOutput, 0)
      self.safety.set_safety_hooks(self.SAFETY_MODEL, param)
      self.safety.set_controls_allowed(True)
      self.assertFalse(self._tx(self.command('steer')))

  def test_fixture_is_absent_from_release_build(self):
    path = libsafety_py._build_libsafety(release=True)
    try:
      release = libsafety_py.ffi.dlopen(path)
      with self.assertRaises(AttributeError):
        release.set_retropilot_test_profile(0)
    finally:
      os.unlink(path)


if __name__ == '__main__':
  unittest.main()
