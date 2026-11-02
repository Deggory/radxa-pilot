#!/usr/bin/env bash
# Host-only conversion; never loads a context on the Q8B.
set -euo pipefail
[[ $# == 4 && $(uname -m) == x86_64 ]] || {
  echo 'Usage (x86_64): qairt_host.sh float|quantize|quantize-research|context-research|help TOOLCHAIN_WORK EXPERIMENT_WORK INPUT_LIST' >&2
  exit 2
}
mode="$1"
toolchain="$(realpath "$2")"
work="$(realpath "$3")"
input_list="$4"
sdk="$toolchain/qairt/2.37.1.250807"
[[ -x "$toolchain/python310/bin/python" && -f "$sdk/bin/envsetup.sh" ]] || exit 3
source "$toolchain/python310/bin/activate"
python_libdir="$(python -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')"
runtime_libdirs="$(find "$toolchain/local-runtime-root/usr/lib" \( -type f -o -type l \) \( -name 'libc++.so*' -o -name 'libc++abi.so*' -o -name 'libunwind.so*' \) -printf '%h\n' | sort -u | paste -sd:)"
export LD_LIBRARY_PATH="$sdk/lib/x86_64-linux-clang:$runtime_libdirs:$python_libdir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="${PYTHONPATH:-}"
source "$sdk/bin/envsetup.sh"
export PYTHONPATH="$work/source${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$work/logs" "$work/artifacts/dlc-v1"
source_model="$work/artifacts/graph-v1/quantization_source_fp32.onnx"
[[ $(sha256sum "$source_model" | cut -d ' ' -f 1) == eceadb809ada5462481cb343e643850e45c72cc4fdf55db0deb74b5718b9411d ]] || {
  echo 'Unexpected graph derivative; require a reviewed new source pin.' >&2; exit 3;
}
case "$mode" in
  help)
    qairt-quantizer --help > "$work/logs/quantizer-help.txt" 2>&1
    qnn-context-binary-generator --help > "$work/logs/context-generator-help.txt" 2>&1
    qnn-context-binary-utility --help > "$work/logs/context-utility-help.txt" 2>&1
    qairt-dlc-info --help > "$work/logs/dlc-info-help.txt" 2>&1
    ;;
  float)
    [[ ! -e "$work/artifacts/dlc-v1/float.dlc" ]] || { echo 'Choose a fresh output; existing DLC preserved.' >&2; exit 3; }
    /usr/bin/time -v qairt-converter --input_network "$source_model" --float_bitwidth 32 \
      --output_path "$work/artifacts/dlc-v1/float.dlc" 2>&1 | tee "$work/logs/float-conversion-v1.log"
    python -m openpilot.selfdrive.modeld.npu.contracts record-float "$work"
    ;;
  quantize|quantize-research)
    suffix=""
    verifier="verify-calibration"
    if [[ "$mode" == quantize-research ]]; then
      suffix="-research"
      verifier="verify-calibration-research"
    fi
    [[ -s "$input_list" && ! -e "$work/artifacts/dlc-v1/w8a8$suffix.dlc" ]] || exit 3
    python -m openpilot.selfdrive.modeld.npu.contracts verify-float "$work"
    python -m openpilot.selfdrive.modeld.npu.contracts "$verifier" "$input_list"
    /usr/bin/time -v qairt-quantizer --input_dlc "$work/artifacts/dlc-v1/float.dlc" \
      --output_dlc "$work/artifacts/dlc-v1/w8a8$suffix.dlc" --input_list "$input_list" \
      --act_bitwidth 8 --weights_bitwidth 8 --bias_bitwidth 32 --use_per_channel_quantization \
      --use_per_row_quantization --use_native_input_files --preserve_io_datatype \
      --target_backend HTP --dump_encoding_json 2>&1 | tee "$work/logs/quantization-v1$suffix.log"
    if [[ "$mode" == quantize-research ]]; then
      python -m openpilot.selfdrive.modeld.npu.contracts record-research "$work" --input-list "$input_list"
    fi
    ;;
  context-research)
    python -m openpilot.selfdrive.modeld.npu.contracts verify-research "$work" --input-list "$input_list"
    output="$work/artifacts/context-v68-soc37-v1"
    [[ ! -e "$output" ]] || { echo 'Choose a fresh context destination; existing evidence preserved.' >&2; exit 3; }
    mkdir "$output"
    printf '%s\n' '{"devices":[{"dsp_arch":"v68","soc_id":37}]}' > "$output/htp.json"
    python - "$sdk" "$output" <<'PY'
import json
import sys
from pathlib import Path
sdk, output = map(Path, sys.argv[1:])
(output / 'context.json').write_text(json.dumps({'backend_extensions': {
  'shared_library_path': str(sdk / 'lib/x86_64-linux-clang/libQnnHtpNetRunExtensions.so'),
  'config_file_path': str(output / 'htp.json')}}) + '\n')
PY
    /usr/bin/time -v qnn-context-binary-generator --model "$sdk/lib/x86_64-linux-clang/libQnnModelDlc.so" \
      --dlc_path "$work/artifacts/dlc-v1/w8a8-research.dlc" --backend "$sdk/lib/x86_64-linux-clang/libQnnHtp.so" \
      --config_file "$output/context.json" --binary_file mountain_dew_v3_w8a8_research --output_dir "$output" \
      --log_level info 2>&1 | tee "$work/logs/context-v68-soc37-v1.log"
    sha256sum "$output/mountain_dew_v3_w8a8_research.bin" > "$output/context.sha256"
    ;;
  *) echo 'Host stages are float or quantize.' >&2; exit 2 ;;
esac
