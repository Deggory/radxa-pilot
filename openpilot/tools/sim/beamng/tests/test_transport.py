import errno
import os
from pathlib import Path
import pty
import select
import socket
import subprocess
import sys
import time
import unittest

from openpilot.tools.sim.beamng.pc.gateway import FLOAT_FIELDS, PACKET, adapter_config, write_serial
from opendbc.car.retropilot.simulation import SimulationReceiver
from test_gateway import sample


class TestTransport(unittest.TestCase):
  def test_real_cli_udp_to_serial_pty_and_radxa_decode(self):
    master, slave = pty.openpty()
    path = os.ttyname(slave)
    os.close(slave)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reservation:
      reservation.bind(('127.0.0.1', 0))
      port = reservation.getsockname()[1]
    gateway = Path(__file__).resolve().parents[1]/'pc/gateway.py'
    proc = subprocess.Popen([sys.executable, str(gateway), '--serial', path, '--transmit',
                             '--port', str(port), '--duration', '0.4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
      self.assertTrue(select.select([proc.stderr], [], [], 5)[0], 'CLI did not become ready')
      self.assertIn(b'waiting_for_beamng', proc.stderr.readline())
      s = sample(wall_time=time.clock_gettime(time.CLOCK_REALTIME))
      raw = PACKET.pack(b'RPT1', s.session, s.wall_time, s.sim_time, s.sequence, s.valid,
                        *[getattr(s, name) for name in FLOAT_FIELDS], s.buttons)
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        sender.sendto(raw, ('127.0.0.1', port))
      wire = bytearray()
      deadline = time.monotonic()+2
      while proc.poll() is None and time.monotonic() < deadline:
        if select.select([master], [], [], 0.05)[0]:
          try:
            wire.extend(os.read(master, 4096))
          except OSError as error:
            if error.errno != errno.EIO:
              raise
            break
      stdout, stderr = proc.communicate(timeout=2)
      self.assertEqual(proc.returncode, 0, stderr)
      self.assertEqual(stdout, b'')
      self.assertIn(b'"samples": 1', stderr)
      self.assertEqual(wire[:20], adapter_config(500000))
      pending = wire[20:]
      receiver = SimulationReceiver()
      count = 0
      while pending:
        self.assertEqual(pending[0], 0xaa)
        size = 5+(pending[1] & 15)
        self.assertEqual(pending[size-1], 0x55)
        address = int.from_bytes(pending[2:4], 'little')
        receiver.feed(address, pending[4:size-1], 2, 1_000_000_000)
        pending = pending[size:]
        count += 1
      self.assertEqual(count, 12)
      self.assertAlmostEqual(receiver.current(1_000_000_000)['speed_mps'], 10)
    finally:
      if proc.poll() is None:
        proc.terminate()
        proc.communicate(timeout=2)
      os.close(master)

  def test_blocked_serial_write_has_a_deadline(self):
    master, slave = pty.openpty()
    os.set_blocking(slave, False)
    try:
      start = time.monotonic()
      with self.assertRaises(TimeoutError):
        write_serial(slave, b'a'*1_000_000)
      self.assertLess(time.monotonic()-start, 0.5)
    finally:
      os.close(slave)
      os.close(master)


if __name__ == '__main__':
  unittest.main()
