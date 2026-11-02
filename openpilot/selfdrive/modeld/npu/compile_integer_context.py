"""Compile only the independently checked integer-boundary DLC for v68/SoC37."""
import argparse
import json
from pathlib import Path
import subprocess

from openpilot.selfdrive.modeld.npu.contracts import DERIVATIVE_SHA
from openpilot.selfdrive.modeld.npu.evaluate_outputs import INPUT_SHAPES, IO_MODE, output_contract
from openpilot.selfdrive.modeld.npu.integer_io import CALIBRATED_SHA
from openpilot.selfdrive.modeld.npu.prepare_road_inputs import digest
from openpilot.selfdrive.modeld.npu.contracts import HEADS


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('sdk', type=Path)
  parser.add_argument('dlc', type=Path)
  parser.add_argument('output', type=Path)
  parser.add_argument('--audit-existing', action='store_true', help='Reinspect an existing binary after stronger provenance checks')
  args = parser.parse_args()
  sdk, dlc, output = args.sdk.resolve(), args.dlc.resolve(), args.output.resolve()
  proof_path = dlc.with_suffix('.json')
  proof = json.loads(proof_path.read_text())
  if (output.exists() != args.audit_existing or (output / 'context-receipt.json').exists() or
      proof['parent_dlc_sha256'] != CALIBRATED_SHA or digest(dlc) != proof['dlc_sha256'] or
      not all(proof.get(key) is True for key in ['static_buffers_unchanged', 'parameter_and_activation_encodings_unchanged',
                                               'retained_operations_attributes_connectivity_unchanged', 'roundtrip_encodings_unchanged'])):
    parser.error('requires proved derivative and a fresh context output')
  enc_path = dlc.with_name(dlc.stem + '_encoding.json')
  if digest(enc_path) != proof['encoding_sha256']:
    raise ValueError('integer IO encodings changed')
  activation_encodings = json.loads(enc_path.read_text())['activation_encodings']
  names = list(INPUT_SHAPES) + ['q8b_' + head for head in HEADS[:-1]]
  if any(len(activation_encodings[name]) != 1 for name in names):
    raise ValueError('expected per-tensor IO calibration')
  encodings = {name: activation_encodings[name][0] for name in names}
  output.mkdir(parents=True, exist_ok=args.audit_existing)
  host = sdk / 'lib/x86_64-linux-clang'
  if not args.audit_existing:
    (output / 'htp.json').write_text(json.dumps({'devices': [{'dsp_arch': 'v68', 'soc_id': 37}]}) + '\n')
    (output / 'config.json').write_text(json.dumps({'backend_extensions': {
      'shared_library_path': str(host / 'libQnnHtpNetRunExtensions.so'), 'config_file_path': str(output / 'htp.json')}}) + '\n')
  binary = output / 'mountain_dew_v3_w8a8_research.bin'
  command = [str(sdk / 'bin/x86_64-linux-clang/qnn-context-binary-generator'), '--model', str(host / 'libQnnModelDlc.so'),
             '--dlc_path', str(dlc), '--backend', str(host / 'libQnnHtp.so'), '--config_file', str(output / 'config.json'),
             '--binary_file', binary.stem, '--output_dir', str(output), '--log_level', 'info']
  if not args.audit_existing:
    (output / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    with (output / 'compile.log').open('w') as log:
      subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
  metadata = output / 'context-info.json'
  inspected = output / 'context-info-reinspection.json' if args.audit_existing else metadata
  with (output / ('inspect-revalidation.log' if args.audit_existing else 'inspect.log')).open('w') as log:
    subprocess.run([str(sdk / 'bin/x86_64-linux-clang/qnn-context-binary-utility'), '--context_binary', str(binary),
                    '--json_file', str(inspected)], stdout=log, stderr=subprocess.STDOUT, check=True)
  if json.loads(inspected.read_text()) != json.loads(metadata.read_text()):
    raise ValueError('reinspected context metadata changed')
  output_contract(json.loads(metadata.read_text()), encodings)
  receipt = {'source_sha256': DERIVATIVE_SHA, 'context_sha256': digest(binary), 'context_info_sha256': digest(metadata),
             'context_bytes': binary.stat().st_size, 'dlc_sha256': proof['dlc_sha256'], 'integer_io_receipt_sha256': digest(proof_path),
             'io_mode': IO_MODE, 'io_encodings': encodings, 'target': 'SDK2.37/v68/SoC37 and exact calibrated IO scales verified',
             'qualification': 'unqualified research; device execution and INT8 accuracy unmeasured'}
  (output / 'context-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
  (output / 'integer-io-proof.json').write_bytes(proof_path.read_bytes())
  print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
  main()
