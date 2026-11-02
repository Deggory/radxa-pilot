#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p build
g++ -std=gnu++17 -O2 -g -fPIC -shared -Wl,-z,defs \
  -DCL_TARGET_OPENCL_VERSION=300 -Ivendor/include -Ivendor \
  bridge.cc vendor/selfdrive/modeld/thneed/thneed_common.cc \
  vendor/selfdrive/modeld/thneed/thneed_pc.cc \
  vendor/selfdrive/modeld/thneed/serialize.cc vendor/third_party/json11/json11.cpp \
  -l:libOpenCL.so.1 -o build/libq8b_thneed.so
