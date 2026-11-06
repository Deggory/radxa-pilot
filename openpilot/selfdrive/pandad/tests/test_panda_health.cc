#include <array>
#include <cmath>
#include <cstring>
#include <limits>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_health.h"

namespace carrot_v17 {
#include "chimera/reference/carrot-f4-health-v17/health.h"
}

namespace {
using Wire = carrot_v17::health_t;
static_assert(sizeof(Wire) == 59);
static_assert(offsetof(Wire, ignition_line_pkt) == 32);
static_assert(offsetof(Wire, interrupt_load_pkt) == 45);
static_assert(offsetof(Wire, som_reset_triggered) == 58);
constexpr auto LEGACY = PandaProtocol::LEGACY_F4_V17;

Wire make_wire(uint8_t flags) {
  Wire w{};
  w.uptime_pkt = 0x12345678;
  w.voltage_pkt = 0xfedcba98;
  w.current_pkt = 0x87654321;
  w.safety_tx_blocked_pkt = 0x11223344;
  w.safety_rx_invalid_pkt = 0x55667788;
  w.tx_buffer_overflow_pkt = 0x99aabbcc;
  w.rx_buffer_overflow_pkt = 0xddeeff00;
  w.faults_pkt = 0x80000001;
  w.ignition_line_pkt = (flags >> 0) & 1;
  w.ignition_can_pkt = (flags >> 1) & 1;
  w.wake_on_can_pkt = (flags >> 2) & 1;
  w.controls_allowed_pkt = (flags >> 3) & 1;
  w.car_harness_status_pkt = 0xfe;  // Preserve unknown enum values as raw numbers.
  w.safety_mode_pkt = 0xfd;
  w.safety_param_pkt = 0xabcd;
  w.fault_status_pkt = 0xfc;
  w.power_save_enabled_pkt = (flags >> 4) & 1;
  w.heartbeat_lost_pkt = (flags >> 5) & 1;
  w.alternative_experience_pkt = 0xdef0;
  w.interrupt_load_pkt = 0.375f;
  w.fan_power = 0xfb;
  w.safety_rx_checks_invalid_pkt = (flags >> 6) & 1;
  w.spi_checksum_error_count_pkt = 0x9876;
  w.fan_stall_count = 0xfa;
  w.sbu1_voltage_mV = 0x7654;
  w.sbu2_voltage_mV = 0x3210;
  w.som_reset_triggered = (flags >> 7) & 1;
  return w;
}

std::array<uint8_t, 59> bytes(const Wire &wire) {
  std::array<uint8_t, 59> raw;
  std::memcpy(raw.data(), &wire, raw.size());
  return raw;
}

void check_fields(const Wire &w, const LegacyF4Health &h) {
  CHECK(h.uptime == w.uptime_pkt);
  CHECK(h.voltage_mV == w.voltage_pkt && h.current_mA == w.current_pkt);
  CHECK(h.safety_tx_blocked == w.safety_tx_blocked_pkt && h.safety_rx_invalid == w.safety_rx_invalid_pkt);
  CHECK(h.tx_buffer_overflow == w.tx_buffer_overflow_pkt && h.rx_buffer_overflow == w.rx_buffer_overflow_pkt);
  CHECK(h.faults == w.faults_pkt);
  CHECK(h.ignition_line == bool(w.ignition_line_pkt) && h.ignition_can == bool(w.ignition_can_pkt));
  CHECK(h.wake_on_can == bool(w.wake_on_can_pkt) && h.controls_allowed == bool(w.controls_allowed_pkt));
  CHECK(h.harness_status_raw == w.car_harness_status_pkt && h.safety_mode_raw == w.safety_mode_pkt);
  CHECK(h.safety_param == w.safety_param_pkt && h.fault_status_raw == w.fault_status_pkt);
  CHECK(h.power_save_enabled == bool(w.power_save_enabled_pkt) && h.heartbeat_lost == bool(w.heartbeat_lost_pkt));
  CHECK(h.alternative_experience == w.alternative_experience_pkt && h.interrupt_load == w.interrupt_load_pkt);
  CHECK(h.fan_power == w.fan_power && h.safety_rx_checks_invalid == bool(w.safety_rx_checks_invalid_pkt));
  CHECK(h.spi_checksum_error_count == w.spi_checksum_error_count_pkt && h.fan_stall_count == w.fan_stall_count);
  CHECK(h.sbu1_voltage_mV == w.sbu1_voltage_mV && h.sbu2_voltage_mV == w.sbu2_voltage_mV);
  CHECK(h.som_reset_triggered == bool(w.som_reset_triggered));
}

void test_layout_and_fields() {
  // Independently specified little-endian golden bytes, including high 32-bit measurements.
  const std::array<uint8_t, 59> golden = {
    0x78,0x56,0x34,0x12, 0x98,0xba,0xdc,0xfe, 0x21,0x43,0x65,0x87, 0x44,0x33,0x22,0x11,
    0x88,0x77,0x66,0x55, 0xcc,0xbb,0xaa,0x99, 0x00,0xff,0xee,0xdd, 0x01,0x00,0x00,0x80,
    1,1,1,1,0xfe,0xfd,0xcd,0xab,0xfc,1,1,0xf0,0xde,0,0,0xc0,0x3e,0xfb,1,0x76,0x98,0xfa,0x54,0x76,0x10,0x32,1,
  };
  CHECK(bytes(make_wire(255)) == golden);
  for (unsigned flags = 0; flags < 256; ++flags) {
    auto wire = make_wire(flags);
    auto raw = bytes(wire);
    const auto original = raw;
    auto decoded = decode_legacy_f4_health(LEGACY, raw.data(), raw.size());
    CHECK(decoded);
    check_fields(wire, *decoded);
    CHECK(raw == original);
    // Force unaligned input; output is a separate value with no retained pointer.
    std::array<uint8_t, 60> unaligned;
    std::memcpy(unaligned.data() + 1, raw.data(), raw.size());
    auto other = decode_legacy_f4_health(LEGACY, unaligned.data() + 1, raw.size());
    CHECK(other);
    check_fields(wire, *other);
  }
  auto wire = make_wire(0);
  for (uint32_t value : {0U, 1U, 65535U, 65536U, 0x7fffffffU, 0x80000000U, 0xffffffffU}) {
    wire.uptime_pkt = wire.voltage_pkt = wire.current_pkt = wire.safety_tx_blocked_pkt = value;
    wire.safety_rx_invalid_pkt = wire.tx_buffer_overflow_pkt = wire.rx_buffer_overflow_pkt = wire.faults_pkt = value;
    auto raw = bytes(wire);
    auto decoded = decode_legacy_f4_health(LEGACY, raw.data(), raw.size());
    CHECK(decoded);
    check_fields(wire, *decoded);
  }
  // Keep fractional/subnormal loads and finite values above one; no invented clamp.
  for (float load : {0.0f, 1.0f, 1.25f, std::numeric_limits<float>::denorm_min(), std::numeric_limits<float>::max()}) {
    wire.interrupt_load_pkt = load;
    auto raw = bytes(wire);
    auto decoded = decode_legacy_f4_health(LEGACY, raw.data(), raw.size());
    CHECK(decoded && decoded->interrupt_load == load);
  }
}

void test_rejection() {
  const auto valid = bytes(make_wire(0));
  for (size_t length = 0; length <= 128; ++length) {
    std::array<uint8_t, 128> data{};
    std::memcpy(data.data(), valid.data(), valid.size());
    if (length != 59) CHECK(!decode_legacy_f4_health(LEGACY, data.data(), length));
  }
  CHECK(!decode_legacy_f4_health(LEGACY, nullptr, 59));
  for (auto profile : {PandaProtocol::CURRENT, PandaProtocol::CHIMERA_MAILBOX}) {
    CHECK(!decode_legacy_f4_health(profile, valid.data(), valid.size()));
  }
  for (size_t offset : {32, 33, 34, 35, 41, 42, 50, 58}) {
    for (unsigned value = 2; value < 256; ++value) {
      auto raw = valid;
      raw[offset] = value;
      CHECK(!decode_legacy_f4_health(LEGACY, raw.data(), raw.size()));
    }
  }
  for (float value : {std::numeric_limits<float>::quiet_NaN(), std::numeric_limits<float>::infinity(),
                      -std::numeric_limits<float>::infinity(), -0.125f}) {
    auto wire = make_wire(0);
    wire.interrupt_load_pkt = value;
    auto raw = bytes(wire);
    CHECK(!decode_legacy_f4_health(LEGACY, raw.data(), raw.size()));
  }
}

class HealthHandle : public PandaCommsHandle {
public:
  int calls = 0;
  int forbidden = 0;
  int result = 59;
  bool lose_connection = false;
  bool lose_health = false;
  std::array<uint8_t, 59> raw = bytes(make_wire(255));

  int control_read(uint8_t request, uint16_t value, uint16_t index, unsigned char *data,
                   uint16_t length, unsigned int timeout) override {
    ++calls;
    CHECK(request == 0xd2 && value == 0 && index == 0 && length == 64 && timeout == 1000);
    if (result >= 0) std::memcpy(data, raw.data(), raw.size());
    if (lose_connection) connected = false;
    if (lose_health) comms_healthy = false;
    return result;
  }
  int control_write(uint8_t, uint16_t, uint16_t, unsigned int) override { ++forbidden; return -1; }
  int bulk_read(unsigned char, unsigned char *, int, unsigned int) override { ++forbidden; return -1; }
  int bulk_write(unsigned char, unsigned char *, int, unsigned int) override { ++forbidden; return -1; }
};

void test_bounded_read() {
  HealthHandle handle;
  auto h = read_legacy_f4_health(handle, LEGACY);
  CHECK(h);
  check_fields(make_wire(255), *h);
  CHECK(handle.calls == 1 && handle.forbidden == 0);
  // Every subsequent bad transfer fails without returning cached prior state or retrying.
  for (int length = -10; length <= 65; ++length) {
    if (length == 59) continue;
    handle.result = length;
    const auto before = handle.calls;
    CHECK(!read_legacy_f4_health(handle, LEGACY));
    CHECK(handle.calls == before + 1 && handle.forbidden == 0);
  }
  for (auto profile : {PandaProtocol::CURRENT, PandaProtocol::CHIMERA_MAILBOX}) {
    const auto before = handle.calls;
    CHECK(!read_legacy_f4_health(handle, profile));
    CHECK(handle.calls == before);
  }
  for (unsigned scenario = 0; scenario < 4; ++scenario) {
    HealthHandle broken;
    if (scenario == 0) broken.connected = false;
    if (scenario == 1) broken.comms_healthy = false;
    broken.lose_connection = scenario == 2;
    broken.lose_health = scenario == 3;
    CHECK(!read_legacy_f4_health(broken, LEGACY));
    CHECK(broken.calls == (scenario < 2 ? 0 : 1) && broken.forbidden == 0);
  }
  HealthHandle malformed;
  malformed.raw[35] = 2;
  CHECK(!read_legacy_f4_health(malformed, LEGACY));
  CHECK(malformed.calls == 1 && malformed.forbidden == 0);
}
}  // namespace

int main() {
  return run_native_test([] {
    test_layout_and_fields();
    test_rejection();
    test_bounded_read();
    std::cout << "Legacy F4 health59: exact source/golden layout, 256 flag combinations, 2032 invalid booleans, "
                 "integer/float/unaligned cases and bounded single-read failures passed; no hardware calls\n";
  });
}
