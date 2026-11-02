#!/usr/bin/python3 -I
"""Root-owned, fixed-policy Q8B clock lease. No project imports or shell commands."""
import fcntl
import json
import os
from pathlib import Path
import select
import signal
import stat
import sys
import time

GPU_HZ = '690000000'
STOP_SIGNALS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT)
stop_requested = False


def emit(message, *, required=False):
  data = (json.dumps(message) + '\n').encode()
  try:
    if os.write(sys.stdout.fileno(), data) != len(data):
      raise RuntimeError('Incomplete performance status write')
  except BlockingIOError:
    if required:
      raise RuntimeError('Performance status pipe is full') from None



class Profile:
  def __init__(self, root=Path('/')):
    self.root = root
    compatible = (root / 'proc/device-tree/compatible').read_bytes().split(b'\0')
    if b'radxa,dragon-q8b' not in compatible:
      raise RuntimeError('This performance profile requires Radxa Dragon Q8B')
    self.gpu = root / 'sys/class/devfreq/3d00000.gpu'
    if GPU_HZ not in (self.gpu / 'available_frequencies').read_text().split():
      raise RuntimeError('Tested GPU 690 MHz frequency is unavailable')
    if 'userspace' not in (self.gpu / 'available_governors').read_text().split():
      raise RuntimeError('GPU userspace governor is unavailable')
    if int((self.gpu / 'max_freq').read_text()) < int(GPU_HZ):
      raise RuntimeError('Refusing to raise the existing GPU maximum limit')
    self.policies = sorted((root / 'sys/devices/system/cpu/cpufreq').glob('policy*'))
    if not self.policies:
      raise RuntimeError('No CPU frequency policies')
    self.original = {}
    self.desired = {}
    for p in self.policies:
      maximum = (p / 'cpuinfo_max_freq').read_text().strip()
      if maximum not in ('2438400', '2995200') or (p / 'scaling_max_freq').read_text().strip() != maximum:
        raise RuntimeError('CPU maximum differs from the tested profile; refusing to raise limits')
      if 'performance' not in (p / 'scaling_available_governors').read_text().split():
        raise RuntimeError('CPU performance governor unavailable')
      self.desired[p / 'scaling_governor'] = 'performance'
    self.desired.update({self.gpu / 'governor': 'userspace', self.gpu / 'max_freq': GPU_HZ, self.gpu / 'min_freq': GPU_HZ})
    for p in self.desired:
      self.original[p] = p.read_text().strip()

  def apply(self):
    for p, value in self.desired.items():
      p.write_text(value + '\n')
    self.verify()

  def verify(self):
    for p, value in self.desired.items():
      if p.read_text().strip() != value:
        raise RuntimeError(f'Clock policy mismatch: {p}')

  def restore(self):
    # Lower the minimum before restoring the maximum and governor.
    order = [self.gpu / 'min_freq', self.gpu / 'max_freq', self.gpu / 'governor']
    order += [p / 'scaling_governor' for p in self.policies]
    failures = []
    for p in order:
      try:
        p.write_text(self.original[p] + '\n')
        if p.read_text().strip() != self.original[p]:
          raise RuntimeError('readback mismatch')
      except OSError as e:
        failures.append(f'{p}: {e}')
      except RuntimeError as e:
        failures.append(f'{p}: {e}')
    if failures:
      raise RuntimeError('Clock restore failed; saved state retained: ' + '; '.join(failures))

  def temperatures(self):
    temperatures = []
    for p in (self.root / 'sys/class/thermal').glob('thermal_zone*/temp'):
      value = int(p.read_text())
      if value >= 85000:
        raise RuntimeError(f'Temperature limit reached at {p}: {value / 1000:.1f} C')
      temperatures.append(value)
    if not temperatures:
      raise RuntimeError('No thermal readings; refusing unattended maximum mode')
    return temperatures

  def telemetry(self):
    temperatures = self.temperatures()
    self.verify()
    return {'gpu_hz': int((self.gpu / 'cur_freq').read_text()),
            'cpu_khz': {p.name: int((p / 'scaling_cur_freq').read_text()) for p in self.policies},
            'hottest_mc': max(temperatures)}


def guard():
  if os.geteuid() != 0:
    raise RuntimeError('Install and invoke the root-owned helper with its restricted sudo rule')
  os.umask(0o077)
  os.set_blocking(sys.stdout.fileno(), False)
  fd = os.open('/run/sunnypilot-q8b-performance.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
  try:
    info = os.fstat(fd)
    if info.st_uid or not stat.S_ISREG(info.st_mode):
      raise RuntimeError('Unsafe performance lock')
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state = Path('/run/sunnypilot-q8b-performance.json')
    if state.exists():
      raise RuntimeError('Previous recovery state exists; inspect it before another run')
    profile = Profile()
    profile.temperatures()
    with state.open('x') as stream:
      json.dump({str(p): v for p, v in profile.original.items()}, stream)
      stream.flush()
      os.fsync(stream.fileno())
    try:
      if stop_requested:
        return
      profile.apply()
      readings = profile.telemetry()
      emit({'ready': True, 'profile': 'cpu-max-gpu690', **readings}, required=True)
      last_telemetry = time.monotonic()
      while not stop_requested:
        readable, _, _ = select.select([sys.stdin], [], [], .5)
        if readable and not os.read(sys.stdin.fileno(), 4096):
          break
        readings = profile.telemetry()
        if time.monotonic() - last_telemetry >= 1:
          emit({'telemetry': readings})
          last_telemetry = time.monotonic()
    finally:
      profile.restore()
      state.unlink()
  finally:
    os.close(fd)


def main():
  if sys.argv[1:] != ['guard']:
    raise RuntimeError('Only the fixed guard action is supported')
  def stop(_signal, _frame):
    global stop_requested
    stop_requested = True
  for sig in STOP_SIGNALS:
    signal.signal(sig, stop)
  guard()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
