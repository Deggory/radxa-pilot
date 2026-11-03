import io
import json
import struct
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import usb1

from openpilot.cereal import log
from opendbc.can import CANPacker
from opendbc.car import Bus, gen_empty_fingerprint, structs
from opendbc.car.retropilot.carcontroller import CarController
from opendbc.car.retropilot.interface import CarInterface
from opendbc.car.retropilot.profiles import C2_REFERENCE
from opendbc.car.retropilot.values import CAR, MODULES
from openpilot.selfdrive.pandad import can_capnp_to_list
from openpilot.selfdrive.pandad.chimera import ChimeraReceiver, main, open_chimera
from openpilot.selfdrive.pandad.chimera_protocol import can_event_bytes
from openpilot.selfdrive.pandad.tests.test_chimera_protocol import mailbox


VERSION = 'v1.0.0-DEV-de193215-DEBUG'


class FakeHandle:
  def __init__(self, serial='selected', version=VERSION):
    self.serial = serial
    self.version = version
    self.calls = []
    self.payload = mailbox(0x50, b'123456')
    self.health = struct.pack('<8I7Bh2B', *([0] * 8), 1, 0, 0, 0, 0, 0, 17, 0, 0, 0)
    self.error = None

  def getSerialNumber(self):
    return self.serial

  def getProduct(self):
    return 'Chimera'

  def claimInterface(self, index):
    self.calls.append(('claim', index))

  def releaseInterface(self, index):
    self.calls.append(('release', index))

  def close(self):
    self.calls.append(('close',))

  def controlRead(self, request_type, request, value, index, length, timeout):
    self.calls.append(('controlRead', request_type, request, value, index, length, timeout))
    return self.version.encode() if request == 0xd6 else self.health

  def bulkRead(self, endpoint, length, timeout):
    self.calls.append(('bulkRead', endpoint, length, timeout))
    if self.error is not None:
      raise self.error
    return self.payload

  def controlWrite(self, *args, **kwargs):
    raise AssertionError('No vendor writes permitted')

  def bulkWrite(self, *args, **kwargs):
    raise AssertionError('No CAN TX permitted')


class FakeDevice:
  def __init__(self, handle, pid=0xddcc):
    self.handle = handle
    self.pid = pid

  def getVendorID(self):
    return 0xbbaa

  def getProductID(self):
    return self.pid

  def open(self):
    return self.handle


class FakeContext:
  def __init__(self, devices):
    self.devices = devices

  def getDeviceIterator(self, skip_on_error=True):
    return iter(self.devices)


class TestChimeraReceiver(unittest.TestCase):
  def test_only_version_health_and_bulk_in_are_used(self):
    handle = FakeHandle()
    receiver = ChimeraReceiver(handle, VERSION)
    self.assertEqual(receiver.version, VERSION)
    self.assertEqual(receiver.read_health()['safety_model_raw'], 17)
    self.assertEqual(receiver.read_can()[0].bus, 2)
    self.assertEqual({call[2] for call in handle.calls if call[0] == 'controlRead'}, {0xd6, 0xd2})
    self.assertTrue(all(call[1] == 0xc0 for call in handle.calls if call[0] == 'controlRead'))
    self.assertEqual([call[1] for call in handle.calls if call[0] == 'bulkRead'], [0x81])

  def test_wrong_version_and_health_shape_fail_before_can_read(self):
    for handle in (FakeHandle(version='other'), FakeHandle()):
      if handle.version == VERSION:
        handle.health = bytes(50)
      with self.assertRaises(ValueError):
        ChimeraReceiver(handle, VERSION)
      self.assertFalse(any(c[0] == 'bulkRead' for c in handle.calls))

  def test_timeout_preserves_transferred_bytes_and_disconnect_propagates(self):
    handle = FakeHandle()
    receiver = ChimeraReceiver(handle, VERSION)
    error = usb1.USBErrorTimeout()
    error.received = handle.payload
    handle.error = error
    self.assertEqual(receiver.read_can()[0].address, 0x50)
    error.received = b''
    self.assertEqual(receiver.read_can(), [])
    error.received = handle.payload[:8]
    with self.assertRaises(ValueError):
      receiver.read_can()
    handle.error = usb1.USBErrorNoDevice()
    with self.assertRaises(usb1.USBErrorNoDevice):
      receiver.read_can()

  def test_discovery_pins_serial_ignores_bootstub_and_releases_on_error(self):
    other, selected, bootstub = FakeHandle('other'), FakeHandle(), FakeHandle('bootstub')
    context = FakeContext([FakeDevice(other), FakeDevice(bootstub, pid=0xddee), FakeDevice(selected)])
    with self.assertRaisesRegex(RuntimeError, 'simulated disconnect'):
      with open_chimera(context, 'selected', VERSION) as receiver:
        self.assertIs(receiver.handle, selected)
        raise RuntimeError('simulated disconnect')
    self.assertEqual(other.calls, [('close',)])
    self.assertEqual(bootstub.calls, [])
    self.assertEqual(selected.calls[-2:], [('release', 0), ('close',)])

  def test_wrong_serial_never_claims_or_reads_control(self):
    handle = FakeHandle('other')
    with self.assertRaisesRegex(RuntimeError, 'serial'):
      with open_chimera(FakeContext([FakeDevice(handle)]), 'selected', VERSION):
        self.fail('Wrong device selected')
    self.assertEqual(handle.calls, [('close',)])

  def test_shared_vid_pid_does_not_select_interceptor_bench(self):
    handle = FakeHandle()
    with patch.object(handle, 'getProduct', return_value='Interceptor DAC Bench'):
      with self.assertRaises(RuntimeError):
        with open_chimera(FakeContext([FakeDevice(handle)]), 'selected', VERSION):
          self.fail('A matching VID/PID is not a Chimera identity')
    self.assertEqual(handle.calls, [('close',)])

  def test_main_publishes_only_can_and_ends_session_on_unplug(self):
    handle = FakeHandle()
    handle.error = usb1.USBErrorNoDevice()
    context = FakeContext([FakeDevice(handle)])
    args = ['chimera', '--serial', 'selected', '--expected-version', VERSION, '--seconds', '0.1', '--publish-can']
    with patch('sys.argv', args), patch('usb1.USBContext') as factory, \
         patch('openpilot.cereal.messaging.PubMaster') as pub, redirect_stdout(io.StringIO()):
      factory.return_value.__enter__.return_value = context
      with self.assertRaises(usb1.USBErrorNoDevice):
        main()
    pub.assert_called_once_with(['can'])
    topic, payload = pub.return_value.send.call_args.args
    self.assertEqual(topic, 'can')
    with log.Event.from_bytes(payload) as event:
      self.assertFalse(event.valid)
      self.assertEqual(len(event.can), 0)
    self.assertEqual(handle.calls[-2:], [('release', 0), ('close',)])

  def test_main_default_monitor_serializes_trace_without_publisher(self):
    handle = FakeHandle()
    context = FakeContext([FakeDevice(handle)])
    args = ['chimera', '--serial', 'selected', '--expected-version', VERSION, '--seconds', '0.025']
    output = io.StringIO()
    with patch('sys.argv', args), patch('usb1.USBContext') as factory, \
         patch('openpilot.cereal.messaging.PubMaster') as pub, redirect_stdout(output):
      factory.return_value.__enter__.return_value = context
      main()
    pub.assert_not_called()
    rows = [json.loads(line) for line in output.getvalue().splitlines()]
    self.assertEqual(rows[0]['event'], 'connected')
    self.assertFalse(rows[0]['live_output'])
    self.assertEqual(rows[1]['mailboxes'][0]['data'], b'123456'.hex())

  def test_usb_to_cereal_to_modern_controller_candidates_without_live_output(self):
    packer = CANPacker('ocelot_controls')
    signals = {'STEER_ANGLE_SENSOR': {'STATE': 1}, 'ENGINE': {'IGNITION_ON': 1}, 'SPEED': {'CAN_SPEED': 36}, 'CRUISE': {},
               'INTERCEPTOR_STEERING_SENSOR': {}, 'ACTUATOR_GAS_SENSOR': {}, 'IBOOSTER_BRAKE_STATUS': {'BRAKE_OK': 1}}
    handle = FakeHandle()
    handle.payload = b''.join(mailbox(address, data, bus) for address, data, bus in
                              (packer.make_can_msg(name, 2, values) for name, values in signals.items()))
    receiver = ChimeraReceiver(handle, VERSION)
    packets = can_capnp_to_list([can_event_bytes(receiver.read_can(), 1_000_000_000)])
    fingerprint = gen_empty_fingerprint()
    fingerprint[2] = {address: size for flag, (_, address, size) in MODULES.items() if C2_REFERENCE.modules & flag}
    cp = CarInterface.get_params(CAR.RETROPILOT_RETROFIT, fingerprint, [], False, False, False)
    cp.wheelSpeedFactor = 1
    cp_sp = CarInterface.get_non_essential_params_sp(cp, CAR.RETROPILOT_RETROFIT)
    ci = CarInterface(cp, cp_sp)
    ci.CC = CarController({Bus.main: 'ocelot_controls'}, cp, cp_sp, profile=C2_REFERENCE)
    ci.update(packets)
    cc = structs.CarControl(enabled=True, latActive=True, longActive=True, actuators={'torque': 1, 'accel': 0.5})
    actual, sends = ci.apply(cc, structs.CarControlSP(), 1_000_000_000)
    self.assertTrue(ci.CC.last_preview.lateral_active)
    self.assertEqual(ci.CC.last_preview.actuators.torqueOutputCan, 5)
    self.assertEqual(ci.CC.last_preview.actuators.gas, 0.5)
    self.assertEqual(actual.torque, 0)
    self.assertEqual(sends, [])


if __name__ == '__main__':
  unittest.main()
