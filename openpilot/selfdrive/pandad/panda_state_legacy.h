#pragma once

#include "cereal/messaging/messaging.h"
#include "selfdrive/pandad/panda_usb_status.h"

// These current PandaState placeholders are unavailable, not measured zero/false.
inline constexpr std::array<const char *, 6> LEGACY_F4_UNAVAILABLE_PANDA_FIELDS{
  "spiErrorCount", "soundOutputLevel", "controlsAllowedLateral",
  "controlsAllowedLongitudinal", "nmiReset", "hardfaultReset",
};

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
