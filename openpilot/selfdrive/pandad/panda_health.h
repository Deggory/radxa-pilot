#pragma once

#include <cstddef>
#include <cstdint>
#include <optional>

#include "selfdrive/pandad/panda_identification.h"

// Carrot F4 health17 (59 bytes), not the current packed health_t. Preserve
// full-width measurements, fractional load and legacy-only fields. Unknown enum
// numbers stay raw; no current-only NMI/hardfault/temperature/sound/lateral state
// is fabricated. This value reports firmware claims, not readiness or authority.
struct LegacyF4Health {
  uint32_t uptime;
  uint32_t voltage_mV;
  uint32_t current_mA;
  uint32_t safety_tx_blocked;
  uint32_t safety_rx_invalid;
  uint32_t tx_buffer_overflow;
  uint32_t rx_buffer_overflow;
  uint32_t faults;
  bool ignition_line;
  bool ignition_can;
  bool wake_on_can;
  bool controls_allowed;
  uint8_t harness_status_raw;
  uint8_t safety_mode_raw;
  uint16_t safety_param;
  uint8_t fault_status_raw;
  bool power_save_enabled;
  bool heartbeat_lost;
  uint16_t alternative_experience;
  float interrupt_load;
  uint8_t fan_power;
  bool safety_rx_checks_invalid;
  uint16_t spi_checksum_error_count;
  uint8_t fan_stall_count;
  uint16_t sbu1_voltage_mV;
  uint16_t sbu2_voltage_mV;
  bool som_reset_triggered;
};

// Caller supplies the qualified identify_panda profile, not a guess from length.
// Exact health59, canonical boolean bytes and finite nonnegative load required.
// No IO/retained pointers; nullopt on unsupported/malformed input. Data may be
// unaligned but must cover size bytes. See chimera/docs/LEGACY_F4_HEALTH.md.
std::optional<LegacyF4Health> decode_legacy_f4_health(PandaProtocol profile, const uint8_t *data, size_t size);

// One bounded D2 IN read (64-byte buffer, 1000ms timeout), no retries, writes or
// cache. Requires exclusive transport ownership and prior pinned identification.
// Unsupported profile/unhealthy transport returns nullopt without IO; failed,
// non-exact or unhealthy completed reads return nullopt, never prior state.
// Transport exceptions propagate. Not connected to managed Panda/get_state yet.
std::optional<LegacyF4Health> read_legacy_f4_health(PandaCommsHandle &handle, PandaProtocol profile);

// CAN-health5 has 26 wire fields plus the caller's C2 selector. Selector0/1/2
// is not proof of physical routing. FD fields are firmware reports, not F4 FD
// capability; no inferred speed, counter semantics or current-profile admission.
struct LegacyF4CanHealth {
  uint8_t can_number;
  bool bus_off;
  uint32_t bus_off_cnt;
  bool error_warning;
  bool error_passive;
  uint8_t last_error;
  uint8_t last_stored_error;
  uint8_t last_data_error;
  uint8_t last_data_stored_error;
  uint8_t receive_error_cnt;
  uint8_t transmit_error_cnt;
  uint32_t total_error_cnt;
  uint32_t total_tx_lost_cnt;
  uint32_t total_rx_lost_cnt;
  uint32_t total_tx_cnt;
  uint32_t total_rx_cnt;
  uint32_t total_fwd_cnt;
  uint32_t total_tx_checksum_error_cnt;
  uint16_t can_speed_kbps;
  uint16_t can_data_speed_kbps;
  bool canfd_enabled;
  bool brs_enabled;
  bool canfd_non_iso;
  uint32_t irq0_call_rate;
  uint32_t irq1_call_rate;
  uint32_t irq2_call_rate;
  uint32_t can_core_reset_cnt;
};

// Qualified legacy profile only; exact64 bytes, canonical booleans, LEC0..7.
// Full u8 REC/TEC and u16/u32 fields preserved. Nullopt on malformed/profile/bus
// mismatch. No IO or retained pointer; controller selector is supplied by caller.
std::optional<LegacyF4CanHealth> decode_legacy_f4_can_health(PandaProtocol profile, uint16_t can_number,
                                                         const uint8_t *data, size_t size);

// One C2 IN request (value=selector0..2, index0, length64, timeout1000ms).
// Same ownership/failure/no-cache/exception contract as the D2 reader above.
// No SPI selection/fallback or managed publication. See LEGACY_F4_CAN_HEALTH.md.
std::optional<LegacyF4CanHealth> read_legacy_f4_can_health(PandaCommsHandle &handle, PandaProtocol profile,
                                                       uint16_t can_number);
