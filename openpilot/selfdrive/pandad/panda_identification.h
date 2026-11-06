#pragma once

#include <optional>
#include <string>
#include <vector>

#include "selfdrive/pandad/panda_comms.h"

enum class PandaProtocol { CURRENT, LEGACY_F4_V17, CHIMERA_MAILBOX };

struct PandaUsbIdentity {
  uint16_t vendor_id;
  uint16_t product_id;
  std::string serial;
  std::string product;
};

struct PandaIdentificationPin {
  std::string serial;
  std::string firmware_version;
};

struct PandaIdentification {
  PandaProtocol protocol;
  std::optional<uint8_t> hardware_type;
  std::string firmware_version;
  std::vector<uint8_t> initial_health;
};

// The caller exclusively owns the transport and supplies descriptor identity
// from that same device plus an explicit serial/version pin. Performs bounded
// control IN reads only; throws on any mismatch. A result
// identifies a protocol, not permission to initialize, transmit, flash or drive.
PandaIdentification identify_panda(PandaCommsHandle &handle, const PandaUsbIdentity &identity,
                                   const PandaIdentificationPin &pin);
