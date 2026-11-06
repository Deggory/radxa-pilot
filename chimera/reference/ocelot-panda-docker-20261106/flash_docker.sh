#! /usr/bin/env bash
set -e

PROJECT_NAME="${1:-panda}"

# if [ $# -eq 0 ]; then
#     echo "Usage: $0 <project>"
#     exit 1
# fi

docker run --rm \
  -v $(pwd):/ocelot \
  -w /ocelot \
  ocelot-builder ./build_project.sh $PROJECT_NAME

./recover.sh $PROJECT_NAME

# docker run -it --rm ocelot-builder $1
# docker run --rm --device /dev/bus/usb --privileged  ocelot-builder $1