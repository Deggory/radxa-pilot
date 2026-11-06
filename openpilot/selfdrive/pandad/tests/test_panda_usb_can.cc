#include <algorithm>
#include <array>
#include <vector>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_usb_can.h"

namespace {
std::vector<uint8_t> wire(uint32_t address, uint8_t bus, uint8_t size, uint8_t receipt = 0, bool extended = false) {
  uint32_t word = (address << 3) | (extended ? 4 : 0) | receipt;
  std::vector<uint8_t> data{static_cast<uint8_t>((size << 4) | (bus << 1)),
                          static_cast<uint8_t>(word), static_cast<uint8_t>(word >> 8),
                          static_cast<uint8_t>(word >> 16), static_cast<uint8_t>(word >> 24), 0};
  for (unsigned i = 0; i < size; ++i) data.push_back(i * 17);
  uint8_t check = 0;
  for (uint8_t value : data) check ^= value;
  data[5] = check;
  return data;
}

void checksum(std::vector<uint8_t> &data) {
  data[5] = 0;
  uint8_t check = 0;
  for (uint8_t value : data) check ^= value;
  data[5] = check;
}

void test_frames_and_splits() {
  for (uint8_t bus = 0; bus < 3; ++bus) {
    for (uint8_t size = 0; size <= 8; ++size) {
      for (auto [address, extended] : std::vector<std::pair<uint32_t, bool>>{{0, false}, {0x7ff, false}, {0, true}, {0x1fffffff, true}}) {
        for (uint8_t receipt = 0; receipt < 3; ++receipt) {
          auto raw = wire(address, bus, size, receipt, extended);
          for (size_t split = 0; split <= raw.size(); ++split) {
            PandaUsbCanStream stream;
            auto first = stream.feed(raw.data(), split, 1);
            auto second = stream.feed(raw.data() + split, raw.size() - split, 2);
            CHECK(first && second);
            first->insert(first->end(), second->begin(), second->end());
            CHECK(first->size() == (receipt == 0 ? 1 : 0));
            if (receipt == 0) {
              auto &f = first->at(0);
              CHECK(f.address == address && f.bus == bus && f.length == size && f.extended == extended);
              CHECK(std::equal(raw.begin() + 6, raw.end(), f.data.begin()));
            }
          }
        }
      }
    }
  }
}

void test_failure_and_fragment_age() {
  const auto valid = wire(0x123, 2, 8);
  for (size_t offset = 0; offset < valid.size(); ++offset) {
    auto bad = valid;
    bad[offset] ^= 0x80;
    PandaUsbCanStream stream;
    CHECK(!stream.feed(bad.data(), bad.size(), 1));
    CHECK(!stream.feed(valid.data(), valid.size(), 2));
    stream.reset();
    CHECK(stream.feed(valid.data(), valid.size(), 3)->size() == 1);
  }
  for (auto bad : {wire(0x800, 0, 0), wire(1, 3, 0), wire(1, 0, 8, 3)}) {
    PandaUsbCanStream stream;
    CHECK(!stream.feed(bad.data(), bad.size(), 1));
  }
  for (uint8_t invalid : {1, 0x90, 0xf0}) {
    auto bad = valid;
    bad[0] = invalid;
    checksum(bad);
    PandaUsbCanStream stream;
    CHECK(!stream.feed(bad.data(), bad.size(), 1));
  }
  PandaUsbCanStream stream;
  CHECK(stream.feed(valid.data(), 3, 1)->empty());
  CHECK(stream.feed(nullptr, 0, 500000001)->empty());
  CHECK(!stream.feed(valid.data() + 3, valid.size() - 3, 500000002));
  stream.reset();
  CHECK(stream.feed(valid.data(), 3, 10)->empty());
  CHECK(!stream.feed(valid.data() + 3, valid.size() - 3, 9));
  stream.reset();
  CHECK(!stream.feed(nullptr, 1, 1));
  stream.reset();
  CHECK(!stream.feed(valid.data(), valid.size(), 0));
  stream.reset();
  std::array<uint8_t, 4097> oversized{};
  CHECK(!stream.feed(oversized.data(), oversized.size(), 1));
  stream.reset();
  auto batch = valid;
  auto bad = valid;
  bad.back() ^= 1;
  batch.insert(batch.end(), bad.begin(), bad.end());
  CHECK(!stream.feed(batch.data(), batch.size(), 1)); // Discard this transfer's valid prefix too.
}
}  // namespace

int main() {
  return run_native_test([] {
    test_frames_and_splits();
    test_failure_and_fragment_age();
    std::cout << "USB classical RX: 324 records/all split positions, receipt filtering, corruption/bounds/time latching pass\n";
  });
}
