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
