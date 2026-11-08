#include <algorithm>
#include <array>
#include <iomanip>
#include <sstream>
#include <vector>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/chimera_usb.h"

namespace {
std::vector<uint8_t> mailbox(uint32_t address, uint8_t bus, uint8_t length,
                             bool extended = false, bool remote = false, bool returned = false) {
  const uint32_t rir = (address << (extended ? 3 : 21)) | (extended ? 4U : 0U) | (remote ? 2U : 0U);
  const uint32_t rdtr = length | ((static_cast<uint32_t>(bus) | (returned ? 128U : 0U)) << 4) | 0xabcd0000U;
  std::vector<uint8_t> raw(16);
  for (unsigned i = 0; i < 4; ++i) { raw[i] = rir >> (i * 8); raw[4 + i] = rdtr >> (i * 8); }
  for (unsigned i = 0; i < 8; ++i) raw[8 + i] = i * 17;
  return raw;
}

void test_mailboxes() {
  const std::vector<uint8_t> golden{0, 0, 0x20, 0x60, 0x26, 0, 0, 0, 1, 2, 3, 4, 5, 6, 0, 0};
  ChimeraUsbCanStream literal;
  auto decoded = literal.feed(golden.data(), golden.size(), 1);
  CHECK(decoded && decoded->size() == 1);
  CHECK(decoded->at(0).address == 0x301 && decoded->at(0).bus == 2 && decoded->at(0).length == 6);
  CHECK(decoded->at(0).data[0] == 1 && decoded->at(0).data[5] == 6);
  for (uint8_t bus = 0; bus < 3; ++bus) for (uint8_t length = 0; length <= 8; ++length) {
    for (auto [id, extended] : std::vector<std::pair<uint32_t, bool>>{{0, false}, {0x7ff, false}, {0, true}, {0x1fffffff, true}}) {
      for (unsigned flags = 0; flags < 4; ++flags) {
        const auto raw = mailbox(id, bus, length, extended, flags & 1, flags & 2);
        for (size_t split = 0; split <= 16; ++split) {
          ChimeraUsbCanStream stream;
          auto first = stream.feed(raw.data(), split, 1);
          auto last = stream.feed(raw.data() + split, raw.size() - split, 2);
          CHECK(first && last); first->insert(first->end(), last->begin(), last->end());
          CHECK(first->size() == (flags ? 0 : 1));
          if (!flags) {
            const auto &f = first->at(0);
            CHECK(f.address == id && f.bus == bus && f.length == length && f.extended == extended);
            CHECK(std::equal(raw.begin() + 8, raw.begin() + 8 + length, f.data.begin()));
          }
        }
      }
    }
  }
}

void test_invalid_and_lifecycle() {
  const auto good = mailbox(0x123, 2, 8);
  std::vector<std::vector<uint8_t>> bad{mailbox(1, 3, 0), mailbox(1, 4, 0), mailbox(1, 0, 9)};
  auto reserved = good; reserved[1] |= 8; bad.push_back(reserved);
  reserved = good; reserved[5] |= 0x10; bad.push_back(reserved);
  reserved = good; reserved[0] |= 1; bad.push_back(reserved);
  reserved = mailbox(0x123, 0, 0, true); reserved[0] |= 1; bad.push_back(reserved);
  bad.push_back(mailbox(1, 3, 0, false, true));
  bad.push_back(mailbox(1, 3, 0, false, false, true));
  for (const auto &raw : bad) {
    ChimeraUsbCanStream stream;
    auto batch = good; batch.insert(batch.end(), raw.begin(), raw.end());
    CHECK(!stream.feed(batch.data(), batch.size(), 1));
    CHECK(!stream.feed(good.data(), good.size(), 2));
    stream.reset(); CHECK(stream.feed(good.data(), good.size(), 3)->size() == 1);
  }
  ChimeraUsbCanStream stream;
  CHECK(stream.feed(good.data(), 15, 10)->empty());
  CHECK(stream.feed(nullptr, 0, 500000010)->empty());
  CHECK(!stream.feed(good.data() + 15, 1, 500000011));
  stream.reset(); CHECK(stream.feed(good.data(), 1, 100)->empty());
  CHECK(!stream.feed(nullptr, 0, 99));
  stream.reset(); CHECK(!stream.feed(nullptr, 1, 1));
  stream.reset(); CHECK(!stream.feed(nullptr, 0, 0));
  std::array<uint8_t, 4097> oversized{};
  stream.reset(); CHECK(!stream.feed(oversized.data(), oversized.size(), 1));
  std::vector<uint8_t> maximum;
  for (unsigned i = 0; i < 256; ++i) maximum.insert(maximum.end(), good.begin(), good.end());
  stream.reset(); CHECK(stream.feed(maximum.data(), maximum.size(), 1)->size() == 256);
  // Restart clears fragments: a fresh complete record must decode independently.
  stream.reset(); CHECK(stream.feed(good.data(), 7, 2)->empty());
  stream.reset(); CHECK(stream.feed(good.data(), good.size(), 3)->size() == 1);
  auto receipt = mailbox(0x123, 2, 8, false, false, true); receipt[0] |= 1;
  stream.reset(); CHECK(stream.feed(receipt.data(), receipt.size(), 4)->empty());
}

void test_health() {
  std::array<uint8_t, 43> raw{};
  raw[0] = 0xf9; raw[1] = 0x6f; raw[38] = 17;  // Historical 2026-10-17 probe.
  auto h = decode_chimera_health(raw.data(), raw.size());
  CHECK(h && h->uptime == 28665 && h->safety_model_raw == 17 && h->controls_allowed_raw == 0);
  raw.fill(0xff);
  h = decode_chimera_health(raw.data(), raw.size());
  CHECK(h && h->uptime == 0xffffffffU && h->voltage_raw == 0xffffffffU);
  CHECK(h->safety_param_raw == -1 && h->ignition_line_raw == 255);
  raw[39] = 0; raw[40] = 0x80;
  CHECK(decode_chimera_health(raw.data(), raw.size())->safety_param_raw == -32768);
  raw[39] = 0xff; raw[40] = 0x7f;
  CHECK(decode_chimera_health(raw.data(), raw.size())->safety_param_raw == 32767);
  for (size_t size : {0U, 42U, 44U, 49U, 59U}) CHECK(!decode_chimera_health(raw.data(), size));
  CHECK(!decode_chimera_health(nullptr, 43));
  std::array<uint8_t, 44> unaligned{}; std::copy(raw.begin(), raw.end(), unaligned.begin() + 1);
  CHECK(decode_chimera_health(unaligned.data() + 1, 43)->safety_param_raw == 32767);
}

std::string hex(const std::vector<uint8_t> &bytes) {
  std::ostringstream out;
  out << std::hex << std::setfill('0');
  for (auto byte : bytes) out << std::setw(2) << static_cast<unsigned>(byte);
  return out.str();
}

// Test-only vector interface for comparison with the independently implemented
// Python decoder. No device client or live publisher is involved.
void vectors() {
  for (uint8_t bus = 0; bus < 3; ++bus) for (uint8_t length = 0; length <= 8; ++length) {
    for (auto [id, extended] : std::vector<std::pair<uint32_t, bool>>{{0, false}, {0x7ff, false}, {0, true}, {0x1fffffff, true}}) {
      for (unsigned flags = 0; flags < 4; ++flags) {
        auto raw = mailbox(id, bus, length, extended, flags & 1, flags & 2);
        ChimeraUsbCanStream stream;
        auto frames = stream.feed(raw.data(), raw.size(), 1);
        CHECK(frames);
        std::cout << "M|" << hex(raw) << '|';
        if (!frames->empty()) {
          const auto &f = frames->at(0);
          std::cout << f.address << ',' << static_cast<unsigned>(f.bus) << ',' << f.extended << ','
                    << hex(std::vector<uint8_t>(f.data.begin(), f.data.begin() + f.length));
        }
        std::cout << '\n';
      }
    }
  }
  for (unsigned offset : {0U, 1U, 127U, 128U, 255U}) {
    std::vector<uint8_t> raw(43);
    for (unsigned i = 0; i < raw.size(); ++i) raw[i] = offset + i;
    const auto h = decode_chimera_health(raw.data(), raw.size()); CHECK(h);
    std::array<int64_t, 18> values{h->uptime, h->voltage_raw, h->current_raw, h->can_rx_errs,
      h->can_send_errs, h->can_fwd_errs, h->gmlan_send_errs, h->faults,
      h->ignition_line_raw, h->ignition_can_raw, h->controls_allowed_raw,
      h->gas_interceptor_detected_raw, h->car_harness_status_raw, h->usb_power_mode_raw,
      h->safety_model_raw, h->safety_param_raw, h->fault_status_raw, h->power_save_enabled_raw};
    std::cout << "H|" << hex(raw) << '|';
    for (size_t i = 0; i < values.size(); ++i) std::cout << (i ? "," : "") << values[i];
    std::cout << '\n';
  }
}
}  // namespace

int main(int argc, char **argv) {
  return run_native_test([&] {
    if (argc == 2 && std::string(argv[1]) == "--vectors") vectors();
    else { test_mailboxes(); test_invalid_and_lifecycle(); test_health(); }
  });
}
