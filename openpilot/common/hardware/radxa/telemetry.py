"""Read-only Q8B diagnostic sensors; independent of hardwared's health policy."""
from pathlib import Path
import threading
import time


def empty_health(sample_ns=0):
  return {'sample_ns': sample_ns, 'cpu_c': None, 'gpu_c': None, 'pwm': None, 'pwm_percent': None, 'fan_mode': None, 'fan_rpm': None}


def read_int(path):
  try:
    return int(path.read_text().strip())
  except (OSError, ValueError):
    return None


def read_health(sys_root=Path('/sys')):
  values = {'cpu': [], 'gpu': []}
  for zone in (sys_root / 'class/thermal').glob('thermal_zone*'):
    try:
      name = (zone / 'type').read_text().strip().lower()
    except OSError:
      continue
    group = 'cpu' if name.startswith(('cpu', 'cluster')) else 'gpu' if name.startswith('gpuss') else None
    if group is not None:
      temperature = read_int(zone / 'temp')
      if temperature is not None and -40000 <= temperature <= 150000:
        values[group].append(temperature / 1000.)
  sample = empty_health()
  for group, temperatures in values.items():
    sample[group + '_c'] = max(temperatures) if temperatures else None
  for name in (sys_root / 'class/hwmon').glob('hwmon*/name'):
    try:
      if name.read_text().strip() != 'radxa_svc_glink':
        continue
    except OSError:
      continue
    pwm = read_int(name.parent / 'pwm1')
    if pwm is not None and 0 <= pwm <= 255:
      sample.update(pwm=pwm, pwm_percent=pwm / 255. * 100.)
    sample['fan_mode'] = read_int(name.parent / 'pwm1_enable')
    rpm = read_int(name.parent / 'fan1_input')
    sample['fan_rpm'] = rpm if rpm is not None and 0 <= rpm <= 100000 else None
    break
  sample['sample_ns'] = time.monotonic_ns()
  return sample


class HealthSampler:
  """Sample once per second off the rendering thread; never write sysfs."""
  def __init__(self, sys_root=Path('/sys')):
    self.root = sys_root
    self.latest = empty_health()
    self.lock = threading.Lock()
    self.stop = threading.Event()
    self.thread = threading.Thread(target=self._run, name='q8b-ui-health', daemon=True)
    self.thread.start()

  def _run(self):
    while not self.stop.is_set():
      sample = read_health(self.root)
      with self.lock:
        self.latest = sample
      self.stop.wait(1.)

  def snapshot(self, now_ns=None):
    now_ns = time.monotonic_ns() if now_ns is None else now_ns
    with self.lock:
      sample = self.latest.copy()
    return sample if 0 <= now_ns - sample['sample_ns'] <= 3_000_000_000 else empty_health()

  def close(self):
    self.stop.set()
    self.thread.join(timeout=2.)
    if self.thread.is_alive():
      raise TimeoutError('Q8B UI sensor reader did not stop')
