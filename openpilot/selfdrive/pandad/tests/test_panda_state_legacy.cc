#include <algorithm>
#include <cmath>
#include <fstream>
#include <limits>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_state_legacy.h"
#include "chimera/reference/carrot-f4-state-v17/panda/board/faults_declarations.h"

namespace {
LegacyF4StatusSample sample() {
  LegacyF4StatusSample s{};
  s.health.uptime = 123;
  s.health.safety_tx_blocked = 0xfffffffdU;
  s.health.safety_rx_invalid = 123456;
  s.health.tx_buffer_overflow = 123457;
  s.health.rx_buffer_overflow = 123458;
  s.health.power_save_enabled = s.health.heartbeat_lost = s.health.safety_rx_checks_invalid = true;
  s.health.fan_power = 88;
  s.health.voltage_mV = 0xffffffffU;
  s.health.current_mA = 0xfffffffeU;
  s.health.ignition_line = s.health.ignition_can = s.health.controls_allowed = true;
  s.health.safety_mode_raw = 19;
  s.health.safety_param = 0xffff;
  s.health.alternative_experience = 0x7fff;
  s.health.harness_status_raw = 2;
  s.health.fault_status_raw = 1;
  s.health.faults = FAULT_RELAY_MALFUNCTION | FAULT_HEARTBEAT_LOOP_WATCHDOG;
  s.health.interrupt_load = 0.375f;
  s.health.sbu1_voltage_mV = 3300;
  s.health.sbu2_voltage_mV = 1250;
  s.health.spi_checksum_error_count = 1234;  // Not a broader SPI error measurement.
  for (uint8_t i = 0; i < 3; ++i) {
    s.can[i].can_number = i;
    s.can[i].bus_off = s.can[i].error_warning = s.can[i].error_passive = true;
    s.can[i].last_stored_error = 5;
    s.can[i].last_data_error = 6;
    s.can[i].last_data_stored_error = 7;
    s.can[i].transmit_error_cnt = 254;
    s.can[i].can_data_speed_kbps = 0xffff;
    s.can[i].canfd_enabled = s.can[i].brs_enabled = s.can[i].canfd_non_iso = true;
    s.can[i].bus_off_cnt = 0xfffffffeU;
    s.can[i].total_error_cnt = 0xfffffffdU;
    s.can[i].total_tx_lost_cnt = 0xfffffffcU;
    s.can[i].total_rx_lost_cnt = 0xfffffffbU;
    s.can[i].total_tx_cnt = 0xfffffffaU;
    s.can[i].total_fwd_cnt = 0xfffffff9U;
    s.can[i].irq0_call_rate = 0xfffffff8U;
    s.can[i].irq1_call_rate = 0xfffffff7U;
    s.can[i].irq2_call_rate = 0xfffffff6U;
    s.can[i].can_core_reset_cnt = 0xfffffff5U;
    s.can[i].total_rx_cnt = 0xffffffffU - i;
    s.can[i].last_error = i + 1;
    s.can[i].receive_error_cnt = 255;
    s.can[i].can_speed_kbps = 500 + i;
    s.can[i].total_tx_checksum_error_cnt = 55;
  }
  return s;
}

void test_values() {
  MessageBuilder message;
  CHECK(build_legacy_f4_panda_state_preview(message, PandaProtocol::LEGACY_F4_V17, 3, sample(), 123) == LegacyF4StateError::NONE);
  auto bytes = message.toBytes();
  AlignedBuffer aligned;
  capnp::FlatArrayMessageReader reader(aligned.align(reinterpret_cast<const char *>(bytes.begin()), bytes.size()));
  auto e = reader.getRoot<cereal::Event>();
  CHECK(e.which() == cereal::Event::PANDA_STATES && !e.getValid() && e.getLogMonoTime() == 123);
  CHECK(e.getPandaStates().size() == 1);
  auto s = e.getPandaStates()[0];
  CHECK(s.getVoltage() == 0xffffffffU && s.getCurrent() == 0xfffffffeU && s.getUptime() == 123);
  CHECK(s.getIgnitionLine() && s.getIgnitionCan() && s.getControlsAllowed());
  CHECK(s.getPandaType() == cereal::PandaState::PandaType::BLACK_PANDA);
  CHECK(s.getSafetyModel() == cereal::CarParams::SafetyModel::NO_OUTPUT && s.getSafetyParam() == 0xffff);
  CHECK(s.getAlternativeExperience() == 32767 && s.getInterruptLoad() == 0.375f);
  CHECK(s.getHarnessStatus() == cereal::PandaState::HarnessStatus::FLIPPED);
  CHECK(s.getFaultStatus() == cereal::PandaState::FaultStatus::FAULT_TEMP);
  CHECK(s.getSbu1Voltage() == 3.3f && s.getSbu2Voltage() == 1.25f);
  CHECK(s.getFaults().size() == 2 && s.getFaults()[0] == cereal::PandaState::FaultType::RELAY_MALFUNCTION);
  CHECK(s.getFaults()[1] == cereal::PandaState::FaultType::HEARTBEAT_LOOP_WATCHDOG);
  CHECK(s.getSafetyTxBlocked() == 0xfffffffdU && s.getSafetyRxInvalid() == 123456);
  CHECK(s.getTxBufferOverflow() == 123457 && s.getRxBufferOverflow() == 123458);
  CHECK(s.getPowerSaveEnabled() && s.getHeartbeatLost() && s.getSafetyRxChecksInvalid() && s.getFanPower() == 88);
  CHECK(s.getSpiErrorCount() == 0);  // Placeholder is unavailable, never measured zero.
  CHECK(LEGACY_F4_UNAVAILABLE_PANDA_FIELDS.size() == 6);
  for (float load : {0.0f, 2.5f, std::numeric_limits<float>::max()}) {
    auto input = sample(); input.health.interrupt_load = load;
    MessageBuilder m;
    CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, input, 1) == LegacyF4StateError::NONE);
    CHECK(m.getRoot<cereal::Event>().asReader().getPandaStates()[0].getInterruptLoad() == load);
  }
  const auto buses = std::array{s.getCanState0(), s.getCanState1(), s.getCanState2()};
  for (unsigned i = 0; i < 3; ++i) {
    CHECK(buses[i].getBusOff() && buses[i].getErrorWarning() && buses[i].getErrorPassive());
    CHECK(buses[i].getLastStoredError() == cereal::PandaState::PandaCanState::LecErrorCode::BIT0_ERROR);
    CHECK(buses[i].getLastDataError() == cereal::PandaState::PandaCanState::LecErrorCode::CRC_ERROR);
    CHECK(buses[i].getLastDataStoredError() == cereal::PandaState::PandaCanState::LecErrorCode::NO_CHANGE);
    CHECK(buses[i].getBusOffCnt() == 0xfffffffeU && buses[i].getTotalErrorCnt() == 0xfffffffdU);
    CHECK(buses[i].getTotalTxLostCnt() == 0xfffffffcU && buses[i].getTotalRxLostCnt() == 0xfffffffbU);
    CHECK(buses[i].getTotalTxCnt() == 0xfffffffaU && buses[i].getTotalFwdCnt() == 0xfffffff9U);
    CHECK(buses[i].getIrq0CallRate() == 0xfffffff8U && buses[i].getIrq1CallRate() == 0xfffffff7U);
    CHECK(buses[i].getIrq2CallRate() == 0xfffffff6U && buses[i].getCanCoreResetCnt() == 0xfffffff5U);
    CHECK(buses[i].getTransmitErrorCnt() == 254 && buses[i].getCanDataSpeed() == 0xffff);
    CHECK(buses[i].getCanfdEnabled() && buses[i].getBrsEnabled() && buses[i].getCanfdNonIso());
    CHECK(buses[i].getTotalRxCnt() == 0xffffffffU - i && buses[i].getReceiveErrorCnt() == 255);
    CHECK(static_cast<unsigned>(buses[i].getCanSpeed()) == 500 + i && static_cast<unsigned>(buses[i].getLastError()) == i + 1);
  }
}

void test_errors() {
  const auto reject = [](const LegacyF4StatusSample &s, LegacyF4StateError expected,
                         PandaProtocol protocol = PandaProtocol::LEGACY_F4_V17, uint8_t hardware = 3, uint64_t time = 1) {
    MessageBuilder msg;
    msg.initEvent().initCan(0);  // Failure must not partially overwrite a prior message.
    CHECK(build_legacy_f4_panda_state_preview(msg, protocol, hardware, s, time) == expected);
    CHECK(msg.getRoot<cereal::Event>().asReader().which() == cereal::Event::CAN);
  };
  reject(sample(), LegacyF4StateError::PROFILE, PandaProtocol::CURRENT);
  reject(sample(), LegacyF4StateError::PROFILE, PandaProtocol::CHIMERA_MAILBOX);
  reject(sample(), LegacyF4StateError::TIMESTAMP, PandaProtocol::LEGACY_F4_V17, 3, 0);
  for (uint8_t hardware : {1,2,3,5,6}) {
    MessageBuilder m;
    CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, hardware, sample(), 1) == LegacyF4StateError::NONE);
    CHECK(static_cast<unsigned>(m.getRoot<cereal::Event>().asReader().getPandaStates()[0].getPandaType()) == hardware);
  }
  {
    MessageBuilder m;
    auto s = sample(); s.health.faults = 0;
    CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, s, 1) == LegacyF4StateError::NONE);
    CHECK(m.getRoot<cereal::Event>().asReader().getPandaStates()[0].getFaults().size() == 0);
  }
  for (unsigned value = 0; value < 256; ++value) {
    if (value != 1 && value != 2 && value != 3 && value != 5 && value != 6) {
      reject(sample(), LegacyF4StateError::HARDWARE, PandaProtocol::LEGACY_F4_V17, value);
    }
  }
  for (unsigned value = 0; value <= 0xffff; ++value) {
    auto s = sample(); s.health.alternative_experience = value;
    if (value > 32767) reject(s, LegacyF4StateError::ALTERNATIVE_EXPERIENCE);
    else {
      MessageBuilder m;
      CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, s, 1) == LegacyF4StateError::NONE);
      CHECK(m.getRoot<cereal::Event>().asReader().getPandaStates()[0].getAlternativeExperience() == static_cast<int>(value));
    }
  }
  for (uint32_t bit = 0; bit < 32; ++bit) {
    auto s = sample(); s.health.faults = 1U << bit;
    if (bit > 26) reject(s, LegacyF4StateError::FAULT_BITS);
    else {
      MessageBuilder m;
      CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, s, 1) == LegacyF4StateError::NONE);
      auto f = m.getRoot<cereal::Event>().asReader().getPandaStates()[0].getFaults();
      CHECK(f.size() == 1 && static_cast<uint32_t>(f[0]) == bit);
    }
  }
  for (unsigned value = 3; value < 256; ++value) {
    auto s = sample(); s.health.harness_status_raw = value; reject(s, LegacyF4StateError::HARNESS);
    s = sample(); s.health.fault_status_raw = value; reject(s, LegacyF4StateError::FAULT_STATUS);
  }
  for (float value : {std::numeric_limits<float>::infinity(), std::numeric_limits<float>::quiet_NaN(), -1.0f}) {
    auto s = sample(); s.health.interrupt_load = value; reject(s, LegacyF4StateError::INTERRUPT_LOAD);
  }
  for (unsigned bus = 0; bus < 3; ++bus) {
    auto s = sample(); s.can[bus].can_number = (bus + 1) % 3; reject(s, LegacyF4StateError::CAN_SELECTOR);
    for (auto field : {&LegacyF4CanHealth::last_error, &LegacyF4CanHealth::last_stored_error,
                       &LegacyF4CanHealth::last_data_error, &LegacyF4CanHealth::last_data_stored_error}) {
      s = sample(); s.can[bus].*field = 8; reject(s, LegacyF4StateError::CAN_LEC);
    }
  }
}

void test_safety_codes() {
  // Independent expectations cross-checked against retained source constants.
  const std::vector<unsigned> compatible{0,1,2,3,4,5,6,8,9,10,11,13,14,15,17,18,19,20,21,22,23,24,27,28,33,34};
  for (unsigned code = 0; code < 256; ++code) {
    auto s = sample(); s.health.safety_mode_raw = code;
    MessageBuilder m;
    const bool expected = std::find(compatible.begin(), compatible.end(), code) != compatible.end();
    CHECK((build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, s, 1) == LegacyF4StateError::NONE) == expected);
    if (expected) {
      auto e = m.getRoot<cereal::Event>().asReader();
      CHECK(!e.getValid() && static_cast<unsigned>(e.getPandaStates()[0].getSafetyModel()) == code);
    }
  }
  // Former meanings conflict with today's IDs25/26; never blind-cast them.
  for (uint8_t code : {25,26}) {
    auto s = sample(); s.health.safety_mode_raw = code;
    MessageBuilder m;
    CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, s, 1) == LegacyF4StateError::SAFETY_MODEL);
  }
}
}  // namespace

int main(int argc, char **argv) {
  return run_native_test([&] {
    test_values(); test_errors(); test_safety_codes();
    if (argc == 2) {
      MessageBuilder m;
      CHECK(build_legacy_f4_panda_state_preview(m, PandaProtocol::LEGACY_F4_V17, 3, sample(), 123) == LegacyF4StateError::NONE);
      auto bytes = m.toBytes();
      std::ofstream f(argv[1], std::ios::binary);
      f.write(reinterpret_cast<const char *>(bytes.begin()), bytes.size());
      CHECK(f.good());
    }
    std::cout << "Legacy F4 state preview: full-width/fractional values, all65536 alternative masks, 32fault bits, 256safety/hardware codes and invalid enums/selectors pass; always invalid, no device IO\n";
  });
}
