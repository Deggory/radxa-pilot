#!/usr/bin/env sh
set -e

PROJECT_NAME="${1:-panda}"

for arg in "$@"; do
    if [ "$arg" = "--clean" ]; then
        echo "Cleaning all projects..."
        cd firmware
        PROJECT=ALL scons -u --clean
        exit 0
    fi
done

cd firmware
PROJECT=$PROJECT_NAME scons -u