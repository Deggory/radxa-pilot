#!/usr/bin/env bash
# Build Ocelot firmware locally. This script never opens a USB device.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: ./build_local.sh <project|ALL>" >&2
  echo "Examples: ./build_local.sh chimera; ./build_local.sh ALL" >&2
  exit 2
fi

project="$1"
firmware_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname -- "${firmware_dir}")"
tool_dir="${OCELOT_BUILD_TOOLS_DIR:-${HOME}/.local/ocelot-build-tools}"

# This Radxa has a user-local toolchain; other hosts can use tools in PATH.
if [ -x "${tool_dir}/usr/bin/scons" ] && [ -x "${tool_dir}/usr/bin/arm-none-eabi-gcc" ]; then
  export PATH="${tool_dir}/usr/bin:${PATH}"
  export PYTHONPATH="${tool_dir}/pylib:${tool_dir}/usr/lib/python3/dist-packages${PYTHONPATH:+:${PYTHONPATH}}"
  export CPATH="${tool_dir}/usr/include/newlib${CPATH:+:${CPATH}}"
fi

for program in scons arm-none-eabi-gcc arm-none-eabi-objcopy; do
  if ! command -v "${program}" >/dev/null 2>&1; then
    echo "Missing ${program}. See ${firmware_dir}/BUILDING.md for prerequisites." >&2
    exit 1
  fi
done
if ! python3 -c 'from Crypto.PublicKey import RSA' >/dev/null 2>&1; then
  echo "Missing Python pycryptodome (Crypto.PublicKey). See ${firmware_dir}/BUILDING.md." >&2
  exit 1
fi

cd "${firmware_dir}"
PROJECT="${project}" scons -u

if [ "${project}" = "ALL" ]; then
  echo "Signed applications: ${repo_dir}/firmware/obj/*.bin.signed"
else
  echo "Raw binary: ${repo_dir}/firmware/obj/${project}/${project}.bin"
  echo "Signed application: ${repo_dir}/firmware/obj/${project}.bin.signed"
fi
echo "No firmware was flashed."
