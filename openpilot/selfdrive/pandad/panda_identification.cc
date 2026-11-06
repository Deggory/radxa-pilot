#include "selfdrive/pandad/panda_identification.h"

#include <algorithm>
#include <stdexcept>

namespace {
std::vector<uint8_t> read_identity(PandaCommsHandle &handle, uint8_t request) {
  if (!handle.connected || !handle.comms_healthy) {
    throw std::runtime_error("Panda identification transport is not healthy");
  }
  std::vector<uint8_t> data(64);
  int length = handle.control_read(request, 0, 0, data.data(), data.size(), 1000);
  if (length <= 0 || length > static_cast<int>(data.size()) || !handle.connected || !handle.comms_healthy) {
    throw std::runtime_error("Panda identification read failed or returned an invalid length");
  }
  data.resize(length);
  return data;
}

uint32_t little_endian_u32(const uint8_t *data) {
  return static_cast<uint32_t>(data[0]) | (static_cast<uint32_t>(data[1]) << 8) |
         (static_cast<uint32_t>(data[2]) << 16) | (static_cast<uint32_t>(data[3]) << 24);
}

bool printable(const std::string &value) {
  return std::all_of(value.begin(), value.end(), [](unsigned char ch) { return ch >= 0x20 && ch <= 0x7e; });
}
}  // namespace

PandaIdentification identify_panda(PandaCommsHandle &handle, const PandaUsbIdentity &identity,
                                   const PandaIdentificationPin &pin) {
  if (pin.serial.empty() || pin.firmware_version.empty() || pin.firmware_version.size() > 64 ||
      !printable(pin.firmware_version) || identity.serial != pin.serial || handle.hw_serial != pin.serial ||
      identity.product_id != 0xddcc ||
      (identity.vendor_id != 0x3801 && identity.vendor_id != 0xbbaa) ||
      (identity.product == "Chimera" &&
       (identity.vendor_id != 0xbbaa || pin.firmware_version != "v1.0.0-DEV-de193215-DEBUG"))) {
    throw std::runtime_error("Panda identification requires a pinned normal-mode USB device");
  }

  const auto version_bytes = read_identity(handle, 0xd6);
  const std::string version(version_bytes.begin(), version_bytes.end());
  if (!printable(version) || version != pin.firmware_version) {
    throw std::runtime_error("Panda firmware version does not match the explicit pin");
  }

  PandaProtocol protocol;
  std::optional<uint8_t> hardware;
  size_t health_size;
  if (identity.product == "Chimera") {
    // Original Chimera has no C1/DD handlers. Retain its explicit descriptor,
    // serial/version and health43 contract instead of assuming Panda versions.
    protocol = PandaProtocol::CHIMERA_MAILBOX;
    health_size = 43;
  } else {
    const auto hardware_bytes = read_identity(handle, 0xc1);
    if (hardware_bytes.size() != 1) throw std::runtime_error("Panda hardware type must be one byte");
    hardware = hardware_bytes[0];
    const auto versions = read_identity(handle, 0xdd);
    const bool f4 = *hardware == 1 || *hardware == 2 || *hardware == 3 || *hardware == 5 || *hardware == 6;
    const bool current = *hardware == 7 || *hardware == 9 || *hardware == 10 || *hardware == 0xb1;
    if (f4 && versions == std::vector<uint8_t>{17, 4, 5}) {
      protocol = PandaProtocol::LEGACY_F4_V17;
      health_size = 59;
    } else if (current && versions.size() == 8 &&
               little_endian_u32(versions.data()) == PANDA_HEALTH_VERSION_HASH &&
               little_endian_u32(versions.data() + 4) == PANDA_CAN_VERSION_HASH) {
      protocol = PandaProtocol::CURRENT;
      health_size = 49;
    } else {
      throw std::runtime_error("Unsupported Panda hardware and protocol version combination");
    }
  }
  auto health = read_identity(handle, 0xd2);
  if (health.size() != health_size) throw std::runtime_error("Panda health length does not match its protocol");
  return {protocol, hardware, version, std::move(health)};
}
