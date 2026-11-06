#pragma once

#include "cereal/messaging/messaging.h"
#include "selfdrive/pandad/panda_usb_status.h"

// These current PandaState placeholders are unavailable, not measured zero/false.
using UnavailableField = cereal::PandaState::StatusAvailability::Field;
struct LegacyF4UnavailableField { const char *name; UnavailableField field; };
inline constexpr std::array<LegacyF4UnavailableField, 6> LEGACY_F4_UNAVAILABLE_PANDA_FIELDS{{
  {"spiErrorCount", UnavailableField::SPI_ERROR_COUNT},
  {"soundOutputLevel", UnavailableField::SOUND_OUTPUT_LEVEL},
  {"controlsAllowedLateral", UnavailableField::CONTROLS_ALLOWED_LATERAL},
  {"controlsAllowedLongitudinal", UnavailableField::CONTROLS_ALLOWED_LONGITUDINAL},
  {"nmiReset", UnavailableField::NMI_RESET},
  {"hardfaultReset", UnavailableField::HARDFAULT_RESET},
}};

inline void set_legacy_f4_availability(cereal::PandaState::Builder state) {
  auto info = state.initStatusAvailability();
  info.setProfile(cereal::PandaState::StatusAvailability::Profile::LEGACY_F4V17);
  info.setObservationOnly(true);
  auto missing = info.initUnavailableFields(LEGACY_F4_UNAVAILABLE_PANDA_FIELDS.size());
  for (size_t i = 0; i < LEGACY_F4_UNAVAILABLE_PANDA_FIELDS.size(); ++i) {
    missing.set(i, LEGACY_F4_UNAVAILABLE_PANDA_FIELDS[i].field);
  }
}

enum class LegacyF4StateError {
  NONE, PROFILE, HARDWARE, TIMESTAMP, SAFETY_MODEL, HARNESS, FAULT_STATUS,
  FAULT_BITS, ALTERNATIVE_EXPERIENCE, INTERRUPT_LOAD, CAN_SELECTOR, CAN_LEC,
};

// Offline preview only, never operational admission. Fresh builder required;
// validation failure leaves it untouched. Success builds one PandaState with
// Event.valid=false, even if firmware reports controls/ignition true. Unavailable
// current fields stay placeholders; retain the complete raw diagnostic separately.
// No transport, publisher, Params, firmware or control operations.
LegacyF4StateError build_legacy_f4_panda_state_preview(MessageBuilder &message, PandaProtocol profile,
    uint8_t hardware, const LegacyF4StatusSample &sample, uint64_t timestamp);
