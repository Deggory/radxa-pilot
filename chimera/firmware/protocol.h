// SPDX-License-Identifier: MIT
#pragma once
#include <stddef.h>
#include <stdint.h>

#define CHIMERA_MANIFEST_SIZE 32U
#define CHIMERA_REQUEST_MANIFEST 0xA0U
#define CHIMERA_REQUEST_VERSION 0xD6U
#define CHIMERA_CONTROL_STALL (-1)

#ifdef __cplusplus
extern "C" {
#endif
extern const uint8_t chimera_manifest[CHIMERA_MANIFEST_SIZE];
extern const char chimera_firmware_version[];
extern const char chimera_usb_product[];

// Pure vendor-request handler; no USB controller or hardware access. SETUP is
// exactly eight wire bytes, including little-endian wValue/wIndex/wLength.
// Returns a complete response length or STALL. Failure leaves reply untouched.
// The future EP0 driver must translate STALL and handle standard USB requests
// separately. Source and destination buffers must not overlap.
int chimera_control_read(const uint8_t *setup, size_t setup_size, uint8_t *reply, size_t capacity);
#ifdef __cplusplus
}
#endif
