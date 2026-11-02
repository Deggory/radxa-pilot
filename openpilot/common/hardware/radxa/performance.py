"""User-side lease for the fixed, root-owned Q8B clock guard."""
import json
from pathlib import Path
import select
import subprocess
import time

HELPER = '/usr/local/libexec/sunnypilot-q8b-performance'
INSTALLER = 'sudo /usr/bin/python3 -I tools/q8b/install_performance.py'


class MaxPerformanceLease:
  def __init__(self):
    if not Path(HELPER).is_file():
      raise RuntimeError(f'Q8B Thneed requires the tested maximum profile. One-time local setup: {INSTALLER}')
    self.process = subprocess.Popen(['sudo', '-n', '--', HELPER, 'guard'], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    self.last_telemetry = None
    try:
      if not select.select([self.process.stdout], [], [], 10)[0]:
        raise RuntimeError('Timed out acquiring Q8B performance lease')
      ready = self.process.stdout.readline()
      if not ready:
        raise RuntimeError('Cannot acquire Q8B performance lease: ' + self.process.stderr.read().strip())
      self.last_telemetry = {**json.loads(ready), 'received_ns': time.monotonic_ns()}
      if self.last_telemetry.get('ready') is not True:
        raise RuntimeError('Performance helper did not confirm the maximum profile')
    except BaseException as e:
      try:
        self.close()
      except Exception as restore_error:
        e.add_note(str(restore_error))
      raise

  def check(self):
    if self.process.poll() is not None:
      raise RuntimeError('Q8B performance lease stopped; refusing lower-clock model execution: ' + self.process.stderr.read().strip())
    while select.select([self.process.stdout], [], [], 0)[0]:
      line = self.process.stdout.readline()
      if not line:
        break
      message = json.loads(line)
      if 'telemetry' in message:
        self.last_telemetry = {**message['telemetry'], 'received_ns': time.monotonic_ns()}

  def close(self):
    if self.process.stdin and not self.process.stdin.closed:
      self.process.stdin.close()  # EOF restores clocks even after the model process dies.
    try:
      self.process.wait(timeout=10)
    except subprocess.TimeoutExpired as e:
      # Never kill a root guard in the middle of hardware restoration.
      raise RuntimeError('Performance restoration did not finish; inspect the root recovery state') from e
    finally:
      for stream in (self.process.stdout, self.process.stderr):
        stream.close()
    if self.process.returncode:
      raise RuntimeError('Performance helper exited with an error; inspect /run/sunnypilot-q8b-performance.json')

  def __enter__(self):
    return self

  def __exit__(self, *_):
    self.close()
