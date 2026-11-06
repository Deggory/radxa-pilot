#pragma once

#include "cereal/messaging/messaging.h"
#include "selfdrive/pandad/panda_usb_status.h"

enum class UsbObservationState { OBSERVING, FAILED, CLOSED };

// Host receive timestamps, not ECU timestamps. No pandaStates/control admission.
void build_usb_can_message(MessageBuilder &message, const std::vector<PandaUsbCanFrame> &frames,
                           uint64_t stamp, bool valid);
void build_usb_status_message(MessageBuilder &message, const PandaIdentificationPin &pin,
                              const LegacyF4StatusSample *sample, uint64_t start, uint64_t end,
                              UsbObservationState state);
