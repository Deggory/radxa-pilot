"""Run existing assertions, then close both shared metrics sockets before term.

Audit harness only. The production StatLogSP destructor currently terminates its
shared ZMQ context before closing the child socket, hanging interpreter exit.
This explicit after-suite cleanup does not fix or bypass production behavior.
"""
import json
from pathlib import Path
import unittest

from openpilot.sunnypilot.system.statsd import statlog


def main():
  receipt = json.loads(Path('Ai/Evidence/chimera-availability-20261106.json').read_text())
  modules = receipt['commands']['control_regressions'][5:-1]
  assert len(modules) == 5
  result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
  contexts = {}
  for logger in (statlog, statlog.comma_statlog):
    if logger is not None:
      if logger.sock is not None:
        logger.sock.close(linger=0)
        logger.sock = None
      if logger.zctx is not None:
        contexts[id(logger.zctx)] = logger.zctx
        logger.zctx = None
  for context in contexts.values():
    context.term()
  print(f'Explicit after-suite metrics cleanup: {len(contexts)} context(s); assertions unchanged', flush=True)
  return int(not result.wasSuccessful())


if __name__ == '__main__':
  raise SystemExit(main())
