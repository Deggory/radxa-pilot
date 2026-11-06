#include "selfdrive/pandad/panda_health.h"

#include <array>
#include <cmath>
#include <cstring>
#include <limits>

namespace {
uint16_t read_u16(const uint8_t *data) {
  return static_cast<uint16_t>(data[0]) | (static_cast<uint16_t>(data[1]) << 8);
}

uint32_t read_u32(const uint8_t *data) {
  return static_cast<uint32_t>(data[0]) | (static_cast<uint32_t>(data[1]) << 8) |
         (static_cast<uint32_t>(data[2]) << 16) | (static_cast<uint32_t>(data[3]) << 24);
}
}  // namespace

std::optional<LegacyF4Health> decode_legacy_f4_health(PandaProtocol profile, const uint8_t *data, size_t size) {
  if (profile != PandaProtocol::LEGACY_F4_V17 || data == nullptr || size != 59) return std::nullopt;
  for (size_t offset : {32, 33, 34, 35, 41, 42, 50, 58}) {
    if (data[offset] > 1) return std::nullopt;
  }
  static_assert(sizeof(float) == sizeof(uint32_t) && std::numeric_limits<float>::is_iec559);
  const uint32_t load_bits = read_u32(data + 45);
  float load;
  std::memcpy(&load, &load_bits, sizeof(load));
  if (!std::isfinite(load) || load < 0.0f) return std::nullopt;

  // Explicit offsets avoid native packing, byte order and unaligned loads.
  return LegacyF4Health{
    read_u32(data), read_u32(data + 4), read_u32(data + 8),
    read_u32(data + 12), read_u32(data + 16), read_u32(data + 20), read_u32(data + 24), read_u32(data + 28),
    data[32] != 0, data[33] != 0, data[34] != 0, data[35] != 0,
    data[36], data[37], read_u16(data + 38), data[40], data[41] != 0, data[42] != 0,
    read_u16(data + 43), load, data[49], data[50] != 0, read_u16(data + 51), data[53],
    read_u16(data + 54), read_u16(data + 56), data[58] != 0,
  };
}

std::optional<LegacyF4Health> read_legacy_f4_health(PandaCommsHandle &handle, PandaProtocol profile) {
  if (profile != PandaProtocol::LEGACY_F4_V17 || !handle.connected || !handle.comms_healthy) return std::nullopt;
  // Request up to EP0's bound so an overlong reply is detected, not truncated to59.
  std::array<uint8_t, 64> data{};
  const int length = handle.control_read(0xd2, 0, 0, data.data(), data.size(), 1000);
  if (length != 59 || !handle.connected || !handle.comms_healthy) return std::nullopt;
  return decode_legacy_f4_health(profile, data.data(), length);
}

std::optional<LegacyF4CanHealth> decode_legacy_f4_can_health(PandaProtocol profile, uint16_t can_number,
                                                         const uint8_t *data, size_t size) {
  if (profile != PandaProtocol::LEGACY_F4_V17 || can_number >= 3 || data == nullptr || size != 64) return std::nullopt;
  for (size_t offset : {0, 5, 6, 45, 46, 47}) {
    if (data[offset] > 1) return std::nullopt;
  }
  for (size_t offset : {7, 8, 9, 10}) {
    if (data[offset] > 7) return std::nullopt;
  }
  return LegacyF4CanHealth{
    static_cast<uint8_t>(can_number), data[0] != 0, read_u32(data + 1), data[5] != 0, data[6] != 0,
    data[7], data[8], data[9], data[10], data[11], data[12],
    read_u32(data + 13), read_u32(data + 17), read_u32(data + 21), read_u32(data + 25),
    read_u32(data + 29), read_u32(data + 33), read_u32(data + 37),
    read_u16(data + 41), read_u16(data + 43), data[45] != 0, data[46] != 0, data[47] != 0,
    read_u32(data + 48), read_u32(data + 52), read_u32(data + 56), read_u32(data + 60),
  };
}

std::optional<LegacyF4CanHealth> read_legacy_f4_can_health(PandaCommsHandle &handle, PandaProtocol profile,
                                                       uint16_t can_number) {
  if (profile != PandaProtocol::LEGACY_F4_V17 || can_number >= 3 ||
      !handle.connected || !handle.comms_healthy) return std::nullopt;
  std::array<uint8_t, 64> data{};
  const int length = handle.control_read(0xc2, can_number, 0, data.data(), data.size(), 1000);
  if (length != 64 || !handle.connected || !handle.comms_healthy) return std::nullopt;
  return decode_legacy_f4_can_health(profile, can_number, data.data(), length);
}
