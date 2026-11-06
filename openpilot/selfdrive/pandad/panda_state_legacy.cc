#include "selfdrive/pandad/panda_state_legacy.h"

#include <cmath>
#include <limits>

namespace {
using Safety = cereal::CarParams::SafetyModel;
std::optional<Safety> safety_model(uint8_t code) {
  // Name-matched source IDs only:25=Stellantis and26=FAW conflict with current
  // volkswagenMlb/hongqi. These labels do not qualify compatible control hooks.
  switch (code) {
    case 0: return Safety::SILENT;
    case 1: return Safety::HONDA_NIDEC;
    case 2: return Safety::TOYOTA;
    case 3: return Safety::ELM327;
    case 4: return Safety::GM;
    case 5: return Safety::HONDA_BOSCH_GIRAFFE;
    case 6: return Safety::FORD;
    case 8: return Safety::HYUNDAI;
    case 9: return Safety::CHRYSLER;
    case 10: return Safety::TESLA;
    case 11: return Safety::SUBARU;
    case 13: return Safety::MAZDA;
    case 14: return Safety::NISSAN;
    case 15: return Safety::VOLKSWAGEN;
    case 17: return Safety::ALL_OUTPUT;
    case 18: return Safety::GM_ASCM;
    case 19: return Safety::NO_OUTPUT;
    case 20: return Safety::HONDA_BOSCH;
    case 21: return Safety::VOLKSWAGEN_PQ;
    case 22: return Safety::SUBARU_PREGLOBAL;
    case 23: return Safety::HYUNDAI_LEGACY;
    case 24: return Safety::HYUNDAI_COMMUNITY;
    case 27: return Safety::BODY;
    case 28: return Safety::HYUNDAI_CANFD;
    case 33: return Safety::RIVIAN;
    case 34: return Safety::VOLKSWAGEN_MEB;
    default: return std::nullopt;
  }
}

void fill_can(cereal::PandaState::PandaCanState::Builder state, const LegacyF4CanHealth &can) {
  using Lec = cereal::PandaState::PandaCanState::LecErrorCode;
  state.setBusOff(can.bus_off);
  state.setBusOffCnt(can.bus_off_cnt);
  state.setErrorWarning(can.error_warning);
  state.setErrorPassive(can.error_passive);
  state.setLastError(Lec(can.last_error));
  state.setLastStoredError(Lec(can.last_stored_error));
  state.setLastDataError(Lec(can.last_data_error));
  state.setLastDataStoredError(Lec(can.last_data_stored_error));
  state.setReceiveErrorCnt(can.receive_error_cnt);
  state.setTransmitErrorCnt(can.transmit_error_cnt);
  state.setTotalErrorCnt(can.total_error_cnt);
  state.setTotalTxLostCnt(can.total_tx_lost_cnt);
  state.setTotalRxLostCnt(can.total_rx_lost_cnt);
  state.setTotalTxCnt(can.total_tx_cnt);
  state.setTotalRxCnt(can.total_rx_cnt);
  state.setTotalFwdCnt(can.total_fwd_cnt);
  state.setCanSpeed(can.can_speed_kbps);
  state.setCanDataSpeed(can.can_data_speed_kbps);
  state.setCanfdEnabled(can.canfd_enabled);
  state.setBrsEnabled(can.brs_enabled);
  state.setCanfdNonIso(can.canfd_non_iso);
  state.setIrq0CallRate(can.irq0_call_rate);
  state.setIrq1CallRate(can.irq1_call_rate);
  state.setIrq2CallRate(can.irq2_call_rate);
  state.setCanCoreResetCnt(can.can_core_reset_cnt);
}
}  // namespace

LegacyF4StateError build_legacy_f4_panda_state_preview(MessageBuilder &message, PandaProtocol profile,
    uint8_t hardware, const LegacyF4StatusSample &sample, uint64_t timestamp) {
  using Error = LegacyF4StateError;
  if (profile != PandaProtocol::LEGACY_F4_V17) return Error::PROFILE;
  if (hardware != 1 && hardware != 2 && hardware != 3 && hardware != 5 && hardware != 6) return Error::HARDWARE;
  if (timestamp == 0) return Error::TIMESTAMP;
  const auto &health = sample.health;
  const auto safety = safety_model(health.safety_mode_raw);
  if (!safety) return Error::SAFETY_MODEL;
  if (health.harness_status_raw > 2) return Error::HARNESS;
  if (health.fault_status_raw > 2) return Error::FAULT_STATUS;
  // Current schema has fault0..26 only; legacy sound-DMA bit27 must not disappear.
  if ((health.faults & 0xf8000000U) != 0) return Error::FAULT_BITS;
  if (health.alternative_experience > std::numeric_limits<int16_t>::max()) return Error::ALTERNATIVE_EXPERIENCE;
  if (!std::isfinite(health.interrupt_load) || health.interrupt_load < 0) return Error::INTERRUPT_LOAD;
  for (size_t i = 0; i < sample.can.size(); ++i) {
    const auto &can = sample.can[i];
    if (can.can_number != i) return Error::CAN_SELECTOR;
    if (can.last_error > 7 || can.last_stored_error > 7 || can.last_data_error > 7 || can.last_data_stored_error > 7) return Error::CAN_LEC;
  }

  auto event = message.initEvent(false);
  event.setLogMonoTime(timestamp);
  auto state = event.initPandaStates(1)[0];
  set_legacy_f4_availability(state);
  state.setPandaType(cereal::PandaState::PandaType(hardware));
  state.setSafetyModel(*safety);
  state.setHarnessStatus(cereal::PandaState::HarnessStatus(health.harness_status_raw));
  state.setFaultStatus(cereal::PandaState::FaultStatus(health.fault_status_raw));
  state.setVoltage(health.voltage_mV);
  state.setCurrent(health.current_mA);
  state.setUptime(health.uptime);
  state.setSafetyTxBlocked(health.safety_tx_blocked);
  state.setSafetyRxInvalid(health.safety_rx_invalid);
  state.setIgnitionLine(health.ignition_line);
  state.setIgnitionCan(health.ignition_can);
  state.setControlsAllowed(health.controls_allowed);
  state.setTxBufferOverflow(health.tx_buffer_overflow);
  state.setRxBufferOverflow(health.rx_buffer_overflow);
  state.setSafetyParam(health.safety_param);
  state.setPowerSaveEnabled(health.power_save_enabled);
  state.setHeartbeatLost(health.heartbeat_lost);
  state.setAlternativeExperience(health.alternative_experience);
  state.setInterruptLoad(health.interrupt_load);
  state.setFanPower(health.fan_power);
  state.setSafetyRxChecksInvalid(health.safety_rx_checks_invalid);
  state.setSbu1Voltage(health.sbu1_voltage_mV / 1000.0f);
  state.setSbu2Voltage(health.sbu2_voltage_mV / 1000.0f);
  // The validated low27 fault ordinals match the retained declarations/current schema.
  size_t count = 0;
  for (unsigned bit = 0; bit <= 26; ++bit) if ((health.faults & (1U << bit)) != 0) ++count;
  auto faults = state.initFaults(count);
  size_t index = 0;
  for (unsigned bit = 0; bit <= 26; ++bit) {
    if ((health.faults & (1U << bit)) != 0) faults.set(index++, cereal::PandaState::FaultType(bit));
  }
  fill_can(state.initCanState0(), sample.can[0]);
  fill_can(state.initCanState1(), sample.can[1]);
  fill_can(state.initCanState2(), sample.can[2]);
  return Error::NONE;
}
