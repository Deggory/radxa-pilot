// SPDX-License-Identifier: MIT
#include "protocol.h"

const char chimera_usb_product[] = "Chimera F413";
const char chimera_firmware_version[] = "chimera-f413-bootstrap-v1";

// Explicit wire bytes avoid packing, alignment and native-endian dependencies.
// See ../docs/USB_IDENTITY_CONTRACT.md for offsets and capability semantics.
const uint8_t chimera_manifest[CHIMERA_MANIFEST_SIZE] = {
  'C', 'H', 'M', 'R', 1U, 32U, 1U, 0U, // Schema/length/local board family/phase.
  0U, 0U, 0U, 0U,                      // Operational capabilities: none.
  0U, 0U, 0U, 0U,                      // Active CAN layout hash: unavailable.
  0U, 0U, 0U, 0U,                      // Active health layout hash: unavailable.
  3U, 8U, 0U, 0U,                      // Buses/classical max/auto-update/config ABI.
  0xFFU, 1U, 0U, 0U,                   // Physical interface mask; reserved.
  0U, 0U, 0U, 0U,                      // Reserved.
};

int chimera_control_read(const uint8_t *setup, size_t setup_size, uint8_t *reply, size_t capacity) {
  if (setup == NULL || reply == NULL || setup_size != 8U) return CHIMERA_CONTROL_STALL;
  // Exact vendor/device/IN request; direction alone is insufficient protection.
  if (setup[0] != 0xC0U || setup[2] != 0U || setup[3] != 0U ||
      setup[4] != 0U || setup[5] != 0U) return CHIMERA_CONTROL_STALL;

  const uint8_t *data;
  size_t size;
  switch (setup[1]) {
    case CHIMERA_REQUEST_MANIFEST:
      data = chimera_manifest;
      size = sizeof(chimera_manifest);
      break;
    case CHIMERA_REQUEST_VERSION:
      data = (const uint8_t *)chimera_firmware_version;
      size = sizeof(chimera_firmware_version) - 1U; // No trailing NUL on wire.
      break;
    default:
      return CHIMERA_CONTROL_STALL;
  }
  const uint16_t requested = (uint16_t)setup[6] | ((uint16_t)setup[7] << 8);
  // This vendor ABI requires a complete reply, with a bounded EP0 query size.
  if (requested < size || requested > 64U || capacity < size) return CHIMERA_CONTROL_STALL;
  for (size_t i = 0U; i < size; ++i) reply[i] = data[i];
  return (int)size;
}
