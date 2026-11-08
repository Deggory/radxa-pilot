#pragma once

#include "selfdrive/pandad/panda_usb_can.h"

// Original packed <8I7Bh2B report. All values are unqualified raw firmware
// reports, not current Panda safety enums or calibrated power measurements.
struct ChimeraHealth {
  uint32_t uptime, voltage_raw, current_raw, can_rx_errs, can_send_errs, can_fwd_errs, gmlan_send_errs, faults;
  uint8_t ignition_line_raw, ignition_can_raw, controls_allowed_raw, gas_interceptor_detected_raw;
  uint8_t car_harness_status_raw, usb_power_mode_raw, safety_model_raw;
  int16_t safety_param_raw;
  uint8_t fault_status_raw, power_save_enabled_raw;
};

std::optional<ChimeraHealth> decode_chimera_health(const uint8_t *data, size_t size);

// Original little-endian mailbox16, receive only. Validate metadata before
// filtering RTR/TX receipts. No checksum exists in this format. Only bus0..2
// is admitted; no resync or legacy GMLAN/bus3 substitution. Errors latch.
class ChimeraUsbCanStream {
public:
  std::optional<std::vector<PandaUsbCanFrame>> feed(const uint8_t *data, size_t size, uint64_t now_ns);
  void reset() { *this = ChimeraUsbCanStream{}; }
private:
  std::optional<std::vector<PandaUsbCanFrame>> fail() { failed_ = true; used_ = 0; return std::nullopt; }
  std::array<uint8_t, 16> bytes_{};
  size_t used_ = 0;
  bool failed_ = false;
  uint64_t last_ns_ = 0, partial_ns_ = 0;
};
