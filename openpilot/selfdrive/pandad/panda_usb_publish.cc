#include "selfdrive/pandad/panda_usb_publish.h"

#include <stdexcept>
#include "json11/json11.hpp"

namespace {
using json11::Json;
template <typename T> Json number(T value) { return static_cast<double>(value); }
Json health_json(const LegacyF4Health &h) {
  return Json::object{
    {"uptime", number(h.uptime)},
    {"voltage_mV", number(h.voltage_mV)},
    {"current_mA", number(h.current_mA)},
    {"safety_tx_blocked", number(h.safety_tx_blocked)},
    {"safety_rx_invalid", number(h.safety_rx_invalid)},
    {"tx_buffer_overflow", number(h.tx_buffer_overflow)},
    {"rx_buffer_overflow", number(h.rx_buffer_overflow)},
    {"faults", number(h.faults)},
    {"ignition_line", h.ignition_line},
    {"ignition_can", h.ignition_can},
    {"wake_on_can", h.wake_on_can},
    {"controls_allowed", h.controls_allowed},
    {"harness_status_raw", number(h.harness_status_raw)},
    {"safety_mode_raw", number(h.safety_mode_raw)},
    {"safety_param", number(h.safety_param)},
    {"fault_status_raw", number(h.fault_status_raw)},
    {"power_save_enabled", h.power_save_enabled},
    {"heartbeat_lost", h.heartbeat_lost},
    {"alternative_experience", number(h.alternative_experience)},
    {"interrupt_load", number(h.interrupt_load)},
    {"fan_power", number(h.fan_power)},
    {"safety_rx_checks_invalid", h.safety_rx_checks_invalid},
    {"spi_checksum_error_count", number(h.spi_checksum_error_count)},
    {"fan_stall_count", number(h.fan_stall_count)},
    {"sbu1_voltage_mV", number(h.sbu1_voltage_mV)},
    {"sbu2_voltage_mV", number(h.sbu2_voltage_mV)},
    {"som_reset_triggered", h.som_reset_triggered}
  };
}
Json can_json(const LegacyF4CanHealth &c) {
  return Json::object{
    {"can_number", number(c.can_number)},
    {"bus_off", c.bus_off},
    {"bus_off_cnt", number(c.bus_off_cnt)},
    {"error_warning", c.error_warning},
    {"error_passive", c.error_passive},
    {"last_error", number(c.last_error)},
    {"last_stored_error", number(c.last_stored_error)},
    {"last_data_error", number(c.last_data_error)},
    {"last_data_stored_error", number(c.last_data_stored_error)},
    {"receive_error_cnt", number(c.receive_error_cnt)},
    {"transmit_error_cnt", number(c.transmit_error_cnt)},
    {"total_error_cnt", number(c.total_error_cnt)},
    {"total_tx_lost_cnt", number(c.total_tx_lost_cnt)},
    {"total_rx_lost_cnt", number(c.total_rx_lost_cnt)},
    {"total_tx_cnt", number(c.total_tx_cnt)},
    {"total_rx_cnt", number(c.total_rx_cnt)},
    {"total_fwd_cnt", number(c.total_fwd_cnt)},
    {"total_tx_checksum_error_cnt", number(c.total_tx_checksum_error_cnt)},
    {"can_speed_kbps", number(c.can_speed_kbps)},
    {"can_data_speed_kbps", number(c.can_data_speed_kbps)},
    {"canfd_enabled", c.canfd_enabled},
    {"brs_enabled", c.brs_enabled},
    {"canfd_non_iso", c.canfd_non_iso},
    {"irq0_call_rate", number(c.irq0_call_rate)},
    {"irq1_call_rate", number(c.irq1_call_rate)},
    {"irq2_call_rate", number(c.irq2_call_rate)},
    {"can_core_reset_cnt", number(c.can_core_reset_cnt)}
  };
}
}  // namespace

void build_usb_can_message(MessageBuilder &message, const std::vector<PandaUsbCanFrame> &frames,
                           uint64_t stamp, bool valid) {
  if (stamp == 0 || (!valid && !frames.empty())) throw std::invalid_argument("invalid CAN observation");
  for (const auto &f : frames) {
    if (f.length > 8 || f.bus > 2 || f.address > 0x1fffffff || (!f.extended && f.address > 0x7ff)) {
      throw std::invalid_argument("invalid classical CAN frame");
    }
  }
  auto event = message.initEvent(valid);
  event.setLogMonoTime(stamp);
  auto can = event.initCan(frames.size());
  for (size_t i = 0; i < frames.size(); ++i) {
    can[i].setAddress(frames[i].address);
    can[i].setSrc(frames[i].bus);
    can[i].setDat(kj::ArrayPtr<const capnp::byte>(frames[i].data.data(), frames[i].length));
  }
}

void build_usb_status_message(MessageBuilder &message, const PandaIdentificationPin &pin,
                              const LegacyF4StatusSample *sample, uint64_t start, uint64_t end,
                              UsbObservationState state) {
  const bool observing = state == UsbObservationState::OBSERVING;
  if (start == 0 || end < start || (sample != nullptr) != observing) {
    throw std::invalid_argument("invalid USB diagnostic observation");
  }
  Json::array controllers;
  if (sample) for (const auto &can : sample->can) controllers.push_back(can_json(can));
  const auto payload = Json(Json::object{
    {"kind", "panda-usb-status"}, {"schema", 1}, {"profile", "legacyF4v17"},
    {"serial", pin.serial}, {"version", pin.firmware_version}, {"operational", false},
    {"state", observing ? "observing" : state == UsbObservationState::FAILED ? "failed" : "closed"},
    {"startNanos", std::to_string(start)}, {"endNanos", std::to_string(end)},
    {"health", sample ? health_json(sample->health) : Json()}, {"controllers", controllers},
  }).dump();
  auto event = message.initEvent(observing);
  event.setLogMonoTime(end);
  event.setCustomReservedRawData1(kj::ArrayPtr<const capnp::byte>(
    reinterpret_cast<const capnp::byte *>(payload.data()), payload.size()));
}
