#include "selfdrive/pandad/chimera_usb.h"

namespace {
uint32_t u32(const uint8_t *data) {
  return static_cast<uint32_t>(data[0]) | (static_cast<uint32_t>(data[1]) << 8) |
         (static_cast<uint32_t>(data[2]) << 16) | (static_cast<uint32_t>(data[3]) << 24);
}
}  // namespace

std::optional<ChimeraHealth> decode_chimera_health(const uint8_t *data, size_t size) {
  if (data == nullptr || size != 43) return std::nullopt;
  const int32_t param = data[39] | (static_cast<uint16_t>(data[40]) << 8);
  return ChimeraHealth{
    u32(data), u32(data + 4), u32(data + 8), u32(data + 12), u32(data + 16),
    u32(data + 20), u32(data + 24), u32(data + 28),
    data[32], data[33], data[34], data[35], data[36], data[37], data[38],
    static_cast<int16_t>(param >= 32768 ? param - 65536 : param), data[41], data[42],
  };
}

std::optional<std::vector<PandaUsbCanFrame>> ChimeraUsbCanStream::feed(const uint8_t *data, size_t size, uint64_t now_ns) {
  if (failed_ || (data == nullptr && size != 0) || size > 4096 || now_ns == 0 || now_ns < last_ns_ ||
      (used_ != 0 && now_ns - partial_ns_ > 500000000ULL)) return fail();
  last_ns_ = now_ns;
  std::vector<PandaUsbCanFrame> frames;
  for (size_t i = 0; i < size; ++i) {
    if (used_ == 0) partial_ns_ = now_ns;
    bytes_[used_++] = data[i];
    if (used_ != bytes_.size()) continue;
    const uint32_t rir = u32(bytes_.data()), rdtr = u32(bytes_.data() + 4);
    const bool extended = (rir & 4U) != 0, remote = (rir & 2U) != 0;
    const uint8_t source = (rdtr >> 4) & 255U;
    const bool returned = (source & 128U) != 0;
    const uint8_t bus = source & 127U, length = rdtr & 15U;
    if (length > 8 || bus >= 3 || (rdtr & 0xf000U) != 0 ||
        (!extended && (rir & 0x1ffff8U) != 0) || (!returned && (rir & 1U) != 0)) return fail();
    if (!remote && !returned) {
      PandaUsbCanFrame frame{rir >> (extended ? 3 : 21), bus, length, extended, {}};
      for (unsigned k = 0; k < length; ++k) frame.data[k] = bytes_[8 + k];
      frames.push_back(frame);
    }
    used_ = 0;
  }
  return frames;
}
