"""One bounded, isolated Q8B research replay; never starts vehicle processes."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA, REFERENCE_SHA, verify_native_inputs
from openpilot.selfdrive.modeld.npu.evaluate_outputs import output_contract
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest


def verify_files(root, files):
  root = root.resolve()
  for name, entry in files.items():
    path = (root / name).resolve()
    if not path.is_relative_to(root) or digest(path) != entry['sha256']:
      raise ValueError(f'private runtime identity changed: {name}')


def bounded_run(command, environment, log, lease, started):
  process = subprocess.Popen(command, env=environment, stdout=log, stderr=subprocess.STDOUT)
  try:
    while process.poll() is None:
      lease.check()
      if time.monotonic() - started > 120:
        raise TimeoutError('bounded QNN replay exceeded120s; no retry')
      time.sleep(.1)
  finally:
    if process.poll() is None:
      process.terminate()
      try:
        process.wait(timeout=5)
      except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
  return process.returncode


def main():
  from openpilot.common.hardware.radxa.performance import MaxPerformanceLease, pin_q8b_worker

  def terminate(_signum, _frame):
    raise KeyboardInterrupt('SIGTERM: stop the owned QNN child and restore clocks')
  signal.signal(signal.SIGTERM, terminate)
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--context-dir', type=Path, required=True)
  parser.add_argument('--reference-data', type=Path, required=True)
  parser.add_argument('--output', type=Path, required=True)
  args = parser.parse_args()
  if args.output.exists():
    parser.error('existing output preserved; use a fresh destination')
  npu = Path(__file__).resolve().parent
  runtime = npu / 'artifacts/runtime-2.37'
  verify_files(runtime, json.loads((npu / 'runtime-2.37.json').read_text())['files'])
  context_dir, dataset, output = args.context_dir.resolve(), args.reference_data.resolve(), args.output.resolve()
  context = context_dir / 'mountain_dew_v3_w8a8_research.bin'
  metadata = context_dir / 'context-info.json'
  receipt = json.loads((context_dir / 'context-receipt.json').read_text())
  if (receipt['source_sha256'] != DERIVATIVE_SHA or receipt['context_sha256'] != digest(context) or
      receipt['context_info_sha256'] != digest(metadata)):
    raise ValueError('context provenance changed')
  output_contract(json.loads(metadata.read_text()))
  reference = json.loads((dataset / 'reference-report.json').read_text())
  if (reference['start_frame'] != 500 or reference['frames'] != 200 or reference['reference_sha256'] != REFERENCE_SHA or
      reference['derivative_sha256'] != DERIVATIVE_SHA):
    raise ValueError('requires the separately reset heldout200 dataset')
  input_list = dataset / 'input_list.txt'
  verify_native_inputs(input_list, reference)
  cdsp = [p for p in Path('/sys/class/remoteproc').glob('remoteproc*') if (p / 'name').read_text().strip() == 'cdsp']
  if len(cdsp) != 1 or (cdsp[0] / 'state').read_text().strip() != 'running':
    raise RuntimeError('cDSP is not running; no recovery or retry is attempted')
  output.mkdir(parents=True)
  command = [str(runtime / 'qnn-net-run'), '--backend', str(runtime / 'libQnnHtp.so'), '--retrieve_context', str(context),
             '--input_list', str(input_list), '--output_dir', str(output), '--use_native_input_files',
             '--perf_profile', 'burst', '--profiling_level', 'basic', '--log_level', 'info']
  environment = os.environ | {'LD_LIBRARY_PATH': str(runtime), 'ADSP_LIBRARY_PATH': str(runtime)}
  pin_q8b_worker()
  started = time.monotonic()
  try:
    with MaxPerformanceLease() as lease, (output / 'execution.log').open('w') as log:
      exit_code = bounded_run(command, environment, log, lease, started)
  except BaseException as error:
    (output / 'failure.json').write_text(json.dumps({'error': f'{type(error).__name__}: {error}',
      'context_sha256': digest(context), 'input_list_sha256': digest(input_list),
      'qualification': 'failed/interrupted replay; no accuracy result or automatic retry'}) + '\n')
    raise
  result = {'context_sha256': digest(context), 'context_info_sha256': digest(metadata),
            'input_list_sha256': digest(input_list), 'command': command, 'exit_code': exit_code,
            'elapsed_s': time.monotonic() - started, 'cdsp_after': (cdsp[0] / 'state').read_text().strip(),
            'clock_guard_closed': True, 'qualification': 'unqualified teacher-forced research replay',
            'qnn_output_files': [{'file': str(p.relative_to(output)), 'sha256': digest(p)}
                                 for folder in sorted(output.glob('Result_*'), key=lambda p: int(p.name.split('_')[1]))
                                 for p in sorted(folder.glob('*.raw'))]}
  (output / 'run-receipt.json').write_text(json.dumps(result, indent=2) + '\n')
  if exit_code or result['cdsp_after'] != 'running':
    raise RuntimeError('QNN replay failed; inspect retained log/receipt, no retry')


if __name__ == '__main__':
  main()
