#!/usr/bin/env bash
# Isolated installed SDK interpreter for host-side artifact inspection.
set -euo pipefail
[[ $# -ge 2 && $(uname -m) == x86_64 ]] || exit 2
toolchain="$(realpath "$1")"
shift
q8b_python_args=("$@")
set --
sdk="$toolchain/qairt/2.37.1.250807"
source "$toolchain/python310/bin/activate"
python_libdir="$(python -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')"
runtime_libdirs="$(find "$toolchain/local-runtime-root/usr/lib" \( -type f -o -type l \) \( -name 'libc++.so*' -o -name 'libc++abi.so*' -o -name 'libunwind.so*' \) -printf '%h\n' | sort -u | paste -sd:)"
export LD_LIBRARY_PATH="$sdk/lib/x86_64-linux-clang:$runtime_libdirs:$python_libdir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="${PYTHONPATH:-}"
source "$sdk/bin/envsetup.sh"
exec python "${q8b_python_args[@]}"
