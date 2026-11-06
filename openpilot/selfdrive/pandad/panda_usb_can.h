#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <vector>

struct PandaUsbCanFrame {
  uint32_t address;
  uint8_t bus, length;
  bool extended;
  std::array<uint8_t, 8> data;
};

// Current six-byte/XOR classical format, RX only. Filter returned/rejected
// receipts, reject FD/bus3+/DLC9+/bad standard IDs/conflicting metadata. No TX or
// reset command. Errors latch, partials expire after500ms; timestamps are local
// monotonic receipt times, not ECU sample times. At most4096bytes/feed.
class PandaUsbCanStream {
public:
  std::optional<std::vector<PandaUsbCanFrame>> feed(const uint8_t *data, size_t size, uint64_t now_ns);
  void reset() { *this = PandaUsbCanStream{}; }
private:
  std::optional<std::vector<PandaUsbCanFrame>> fail() { failed_ = true; used_ = 0; return std::nullopt; }
  std::array<uint8_t, 14> bytes_{};
  size_t used_ = 0;
  bool failed_ = false;
  uint64_t last_ns_ = 0, partial_ns_ = 0;
};
