#!/usr/bin/env bash
# One-off owner-authorized Ubuntu PC repair. Never reboots or restarts the desktop.
set -euo pipefail
if [[ $EUID -ne 0 ]]; then
  echo 'Run this repair with sudo in the PC terminal.' >&2
  exit 1
fi
running_kernel=$(uname -r)
case "$running_kernel" in
  7.0.0-38-generic|7.0.0-42-generic) ;;
  *) echo "Stop: this repair was reviewed for PC kernels 7.0.0-38 and 7.0.0-42, not $running_kernel" >&2; exit 1 ;;
esac
repair_log=/home/pc/beamng-q8b/retropilot-can/nvidia-repair-20261104.log
exec > >(tee -a "$repair_log") 2>&1
printf 'Repair started: %s\n' "$(date -u --iso-8601=seconds)"
printf 'Running kernel: %s\n' "$running_kernel"
packages=(linux-modules-nvidia-595-open-7.0.0-38-generic
          linux-modules-nvidia-595-open-7.0.0-42-generic
          linux-modules-nvidia-595-open-generic-hwe-24.04 nvidia-driver-595-open)
# Ubuntu repository packages for the current and already-installed next kernel.
# APT simulation was reviewed: 16 NVIDIA upgrades, 3 new packages, removal of
# the obsolete 7.0.0-31 NVIDIA module package. No kernel removal or autoremove.
apt-get --simulate install "${packages[@]}"
DEBIAN_FRONTEND=noninteractive apt-get --yes install "${packages[@]}"
modprobe nvidia
modprobe nvidia_modeset
modprobe nvidia_drm
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
modinfo -k 7.0.0-38-generic -F version nvidia
modinfo -k 7.0.0-42-generic -F version nvidia
printf 'Repair finished: %s\n' "$(date -u --iso-8601=seconds)"
echo 'No reboot or desktop restart was requested by this script.'
