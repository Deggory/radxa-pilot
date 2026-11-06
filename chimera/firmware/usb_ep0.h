// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum chimera_ep0_phase { CHIMERA_EP0_IDLE, CHIMERA_EP0_DATA_IN, CHIMERA_EP0_STATUS_OUT,
                         CHIMERA_EP0_STATUS_IN, CHIMERA_EP0_STALL };
typedef struct {
  uint32_t generation;
  uint8_t serial[50];
  uint8_t address, configuration, phase, pending_kind, pending_value;
  uint8_t initialized, self_powered, max_power_2ma;
} chimera_usb_ep0;

// Pure control-transfer model, no MMIO. Caller supplies the real 12 UID bytes
// and a separately qualified power profile; no physical power state is inferred.
// Invalid init disables the context. All buffers/state must be separate.
// Initialize before calling reset, SETUP or completion functions.
bool chimera_usb_ep0_init(chimera_usb_ep0 *state, const uint8_t *uid,
                          uint8_t self_powered, uint8_t max_power_2ma);
void chimera_usb_ep0_reset(chimera_usb_ep0 *state);
// Exact8-byte SETUP; returns reply length or -1/STALL with reply untouched.
// New SETUP aborts any pending previous transfer. Replies fit a single FS64-byte
// data packet. The future controller driver must obey phase and commit hardware
// address/config changes only after successful status completion.
int chimera_usb_ep0_setup(chimera_usb_ep0 *state, const uint8_t *setup, size_t setup_size,
                          uint8_t *reply, size_t capacity);
// Save generation when arming a transfer, never substitute the current value for
// an old completion. Backend must also cancel/clear stale hardware events before
// rearming. Generation exhaustion disables context and requires full reinit.
bool chimera_usb_ep0_in_complete(chimera_usb_ep0 *state, uint32_t generation);
bool chimera_usb_ep0_out_complete(chimera_usb_ep0 *state, uint32_t generation, size_t size);
