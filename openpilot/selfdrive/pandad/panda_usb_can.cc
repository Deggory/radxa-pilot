#include "selfdrive/pandad/panda_usb_can.h"

std::optional<std::vector<PandaUsbCanFrame>> PandaUsbCanStream::feed(const uint8_t *data, size_t size, uint64_t now_ns) {
  if (failed_ || (data == nullptr && size != 0) || size > 4096 || now_ns == 0 || now_ns < last_ns_ ||
      (used_ != 0 && now_ns - partial_ns_ > 500000000ULL)) return fail();
  last_ns_ = now_ns;
  std::vector<PandaUsbCanFrame> frames;
  for (size_t i = 0; i < size; ++i) {
    if (used_ == 0) partial_ns_ = now_ns;
    bytes_[used_++] = data[i];
    if (used_ < 6) continue;
    const uint8_t length = bytes_[0] >> 4, bus = (bytes_[0] >> 1) & 7, receipt = bytes_[1] & 3;
    const bool extended = (bytes_[1] & 4) != 0;
    const uint32_t address = (static_cast<uint32_t>(bytes_[1]) | (static_cast<uint32_t>(bytes_[2]) << 8) |
                             (static_cast<uint32_t>(bytes_[3]) << 16) | (static_cast<uint32_t>(bytes_[4]) << 24)) >> 3;
    if ((bytes_[0] & 1) || length > 8 || bus >= 3 || receipt == 3 || (!extended && address > 0x7ff)) return fail();
    if (used_ != 6U + length) continue;
    uint8_t check = 0;
    for (size_t k = 0; k < used_; ++k) check ^= bytes_[k];
    if (check != 0) return fail();
    if (receipt == 0) {
      PandaUsbCanFrame frame{address, bus, length, extended, {}};
      for (unsigned k = 0; k < length; ++k) frame.data[k] = bytes_[6 + k];
      frames.push_back(frame);
    }
    used_ = 0;
  }
  return frames;
}
