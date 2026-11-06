#include <array>
#include <cstring>
#include <type_traits>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_health.h"

namespace carrot_v17 {
#include "chimera/reference/carrot-f4-health-v17/health.h"
}
namespace current_panda {
#include "panda/board/health.h"
}

namespace {
using Wire = carrot_v17::can_health_t;
constexpr auto LEGACY = PandaProtocol::LEGACY_F4_V17;
static_assert(sizeof(Wire) == 64 && sizeof(current_panda::can_health_t) == 64);

Wire make_wire(unsigned flags, uint32_t count = 0x87654321) {
  Wire w{};
  w.bus_off = (flags >> 0) & 1;
  w.bus_off_cnt = count;
  w.error_warning = (flags >> 1) & 1;
  w.error_passive = (flags >> 2) & 1;
  w.last_error = 1;
  w.last_stored_error = 2;
  w.last_data_error = 3;
  w.last_data_stored_error = 7;
  w.receive_error_cnt = 255;  // bxCAN REC is eight bits, unlike the H7 comment.
  w.transmit_error_cnt = 254;
  w.total_error_cnt = count + 1;
  w.total_tx_lost_cnt = count + 2;
  w.total_rx_lost_cnt = count + 3;
  w.total_tx_cnt = count + 4;
  w.total_rx_cnt = count + 5;
  w.total_fwd_cnt = count + 6;
  w.total_tx_checksum_error_cnt = count + 7;
  w.can_speed = 0xabcd;
  w.can_data_speed = 0xdef0;
  w.canfd_enabled = (flags >> 3) & 1;
  w.brs_enabled = (flags >> 4) & 1;
  w.canfd_non_iso = (flags >> 5) & 1;
  w.irq0_call_rate = count + 8;
  w.irq1_call_rate = count + 9;
  w.irq2_call_rate = count + 10;
  w.can_core_reset_cnt = count + 11;
  return w;
}

std::array<uint8_t, 64> bytes(const Wire &w) {
  std::array<uint8_t, 64> raw;
  std::memcpy(raw.data(), &w, raw.size());
  return raw;
}

void check_fields(const Wire &w, const LegacyF4CanHealth &h, unsigned selector) {
  CHECK(h.can_number == selector);
  CHECK(h.bus_off == bool(w.bus_off) && h.bus_off_cnt == w.bus_off_cnt);
  CHECK(h.error_warning == bool(w.error_warning) && h.error_passive == bool(w.error_passive));
  CHECK(h.last_error == w.last_error && h.last_stored_error == w.last_stored_error);
  CHECK(h.last_data_error == w.last_data_error && h.last_data_stored_error == w.last_data_stored_error);
  CHECK(h.receive_error_cnt == w.receive_error_cnt && h.transmit_error_cnt == w.transmit_error_cnt);
  CHECK(h.total_error_cnt == w.total_error_cnt && h.total_tx_lost_cnt == w.total_tx_lost_cnt);
  CHECK(h.total_rx_lost_cnt == w.total_rx_lost_cnt && h.total_tx_cnt == w.total_tx_cnt);
  CHECK(h.total_rx_cnt == w.total_rx_cnt && h.total_fwd_cnt == w.total_fwd_cnt);
  CHECK(h.total_tx_checksum_error_cnt == w.total_tx_checksum_error_cnt);
  CHECK(h.can_speed_kbps == w.can_speed && h.can_data_speed_kbps == w.can_data_speed);
  CHECK(h.canfd_enabled == bool(w.canfd_enabled) && h.brs_enabled == bool(w.brs_enabled));
  CHECK(h.canfd_non_iso == bool(w.canfd_non_iso));
  CHECK(h.irq0_call_rate == w.irq0_call_rate && h.irq1_call_rate == w.irq1_call_rate);
  CHECK(h.irq2_call_rate == w.irq2_call_rate && h.can_core_reset_cnt == w.can_core_reset_cnt);
}

void test_layout_and_values() {
  // Pin every field's position against both independently retained schemas.
#define OFFSET(member, offset) \
  static_assert(offsetof(Wire, member) == offset && offsetof(current_panda::can_health_t, member) == offset && \
                std::is_same_v<decltype(Wire::member), decltype(current_panda::can_health_t::member)>)
  OFFSET(bus_off, 0); OFFSET(bus_off_cnt, 1); OFFSET(error_warning, 5); OFFSET(error_passive, 6);
  OFFSET(last_error, 7); OFFSET(last_stored_error, 8); OFFSET(last_data_error, 9); OFFSET(last_data_stored_error, 10);
  OFFSET(receive_error_cnt, 11); OFFSET(transmit_error_cnt, 12); OFFSET(total_error_cnt, 13);
  OFFSET(total_tx_lost_cnt, 17); OFFSET(total_rx_lost_cnt, 21); OFFSET(total_tx_cnt, 25);
  OFFSET(total_rx_cnt, 29); OFFSET(total_fwd_cnt, 33); OFFSET(total_tx_checksum_error_cnt, 37);
  OFFSET(can_speed, 41); OFFSET(can_data_speed, 43); OFFSET(canfd_enabled, 45); OFFSET(brs_enabled, 46);
  OFFSET(canfd_non_iso, 47); OFFSET(irq0_call_rate, 48); OFFSET(irq1_call_rate, 52);
  OFFSET(irq2_call_rate, 56); OFFSET(can_core_reset_cnt, 60);
#undef OFFSET
  const std::array<uint8_t, 64> golden = {
    1,0x21,0x43,0x65,0x87,1,1,1,2,3,7,255,254,
    0x22,0x43,0x65,0x87, 0x23,0x43,0x65,0x87, 0x24,0x43,0x65,0x87,
    0x25,0x43,0x65,0x87, 0x26,0x43,0x65,0x87, 0x27,0x43,0x65,0x87, 0x28,0x43,0x65,0x87,
    0xcd,0xab,0xf0,0xde,1,1,1,
    0x29,0x43,0x65,0x87, 0x2a,0x43,0x65,0x87, 0x2b,0x43,0x65,0x87, 0x2c,0x43,0x65,0x87,
  };
  CHECK(bytes(make_wire(63)) == golden);
  for (unsigned selector = 0; selector < 3; ++selector) {
    for (unsigned flags = 0; flags < 64; ++flags) {
      auto wire = make_wire(flags);
      auto raw = bytes(wire);
      auto original = raw;
      auto h = decode_legacy_f4_can_health(LEGACY, selector, raw.data(), raw.size());
      CHECK(h);
      check_fields(wire, *h, selector);
      CHECK(raw == original);
      std::array<uint8_t, 65> unaligned;
      std::memcpy(unaligned.data() + 1, raw.data(), raw.size());
      h = decode_legacy_f4_can_health(LEGACY, selector, unaligned.data() + 1, raw.size());
      CHECK(h);
      check_fields(wire, *h, selector);
    }
  }
  for (uint32_t counter : {0U, 65535U, 65536U, 0x80000000U, 0xffffffffU}) {
    auto wire = make_wire(0, counter);
    auto raw = bytes(wire);
    auto h = decode_legacy_f4_can_health(LEGACY, 2, raw.data(), raw.size());
    CHECK(h);
    check_fields(wire, *h, 2);
  }
}

void test_malformed() {
  const auto valid = bytes(make_wire(0));
  CHECK(!decode_legacy_f4_can_health(LEGACY, 0, nullptr, 64));
  std::array<uint8_t, 128> buffer{};
  std::memcpy(buffer.data(), valid.data(), valid.size());
  for (size_t size = 0; size <= 128; ++size) {
    if (size != 64) CHECK(!decode_legacy_f4_can_health(LEGACY, 0, buffer.data(), size));
  }
  for (auto profile : {PandaProtocol::CURRENT, PandaProtocol::CHIMERA_MAILBOX}) {
    CHECK(!decode_legacy_f4_can_health(profile, 0, valid.data(), 64));
  }
  for (unsigned selector = 3; selector <= 65535; ++selector) {
    CHECK(!decode_legacy_f4_can_health(LEGACY, selector, valid.data(), 64));
  }
  for (size_t offset : {0, 5, 6, 45, 46, 47}) {
    for (unsigned value = 2; value < 256; ++value) {
      auto raw = valid;
      raw[offset] = value;
      CHECK(!decode_legacy_f4_can_health(LEGACY, 0, raw.data(), 64));
    }
  }
  for (size_t offset : {7, 8, 9, 10}) {
    for (unsigned value = 0; value < 256; ++value) {
      auto raw = valid;
      raw[offset] = value;
      CHECK(bool(decode_legacy_f4_can_health(LEGACY, 0, raw.data(), 64)) == (value <= 7));
    }
  }
}

class CanHealthHandle : public PandaCommsHandle {
public:
  int calls = 0, forbidden = 0, length = 64;
  uint16_t expected_selector = 0;
  bool disconnect = false, unhealthy = false, corrupt = false;
  int control_read(uint8_t request, uint16_t value, uint16_t index, unsigned char *data,
                   uint16_t capacity, unsigned int timeout) override {
    ++calls;
    CHECK(request == 0xc2 && value == expected_selector && index == 0 && capacity == 64 && timeout == 1000);
    auto raw = bytes(make_wire(0, value));
    if (corrupt) raw[5] = 2;
    std::memcpy(data, raw.data(), raw.size());
    if (disconnect) connected = false;
    if (unhealthy) comms_healthy = false;
    return length;
  }
  int control_write(uint8_t, uint16_t, uint16_t, unsigned int) override { ++forbidden; return -1; }
  int bulk_read(unsigned char, unsigned char *, int, unsigned int) override { ++forbidden; return -1; }
  int bulk_write(unsigned char, unsigned char *, int, unsigned int) override { ++forbidden; return -1; }
};

void test_bounded_reads() {
  CanHealthHandle h;
  for (uint16_t selector = 0; selector < 3; ++selector) {
    h.expected_selector = selector;
    auto result = read_legacy_f4_can_health(h, LEGACY, selector);
    CHECK(result);
    check_fields(make_wire(0, selector), *result, selector);
  }
  h.expected_selector = 0;
  for (int length = -10; length <= 65; ++length) {
    if (length == 64) continue;
    h.length = length;
    const int before = h.calls;
    CHECK(!read_legacy_f4_can_health(h, LEGACY, 0));
    CHECK(h.calls == before + 1 && h.forbidden == 0);
  }
  h.length = 64;
  const int before = h.calls;
  for (unsigned selector = 3; selector <= 65535; ++selector) CHECK(!read_legacy_f4_can_health(h, LEGACY, selector));
  for (auto profile : {PandaProtocol::CURRENT, PandaProtocol::CHIMERA_MAILBOX}) CHECK(!read_legacy_f4_can_health(h, profile, 0));
  CHECK(h.calls == before && h.forbidden == 0);
  for (unsigned scenario = 0; scenario < 5; ++scenario) {
    CanHealthHandle broken;
    if (scenario == 0) broken.connected = false;
    if (scenario == 1) broken.comms_healthy = false;
    broken.disconnect = scenario == 2;
    broken.unhealthy = scenario == 3;
    broken.corrupt = scenario == 4;
    CHECK(!read_legacy_f4_can_health(broken, LEGACY, 0));
    CHECK(broken.calls == (scenario < 2 ? 0 : 1) && broken.forbidden == 0);
  }
}
}  // namespace

int main() {
  return run_native_test([] {
    test_layout_and_values();
    test_malformed();
    test_bounded_reads();
    std::cout << "Legacy F4 CAN-health5: 26 fields/64 bytes, 3 selectors x 64 flag combinations, "
                 "1524 invalid booleans, 1024 LEC cases, 65533 invalid selectors and bounded reads pass; no hardware calls\n";
  });
}
