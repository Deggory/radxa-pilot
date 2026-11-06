// SPDX-License-Identifier: MIT
#pragma once
#include "usb_hw.h"
#include "usb_ep0.h"

typedef struct {
  const chimera_usb_io *io;
  chimera_usb_ep0 ep0;
  uint32_t poll_budget, in_generation, out_generation;
  uint8_t reply[64];
  int reply_size;
  uint8_t active, setup_wait, in_armed, out_armed, out_seen;
} chimera_usb_driver;

// Caller owns prepared/detached non-DMA USB core exclusively. io/context must
// remain valid and unchanged, calls serialized, buffers/state nonoverlapping.
// Initializes EP0 only; no attachment, IRQ enable or startup call. UID/power
// profile qualification remains caller's responsibility. Register waits bounded.
bool chimera_usb_driver_init(chimera_usb_driver *state, const chimera_usb_io *io,
                             const uint8_t *uid, uint8_t self_powered,
                             uint8_t max_power_2ma, uint32_t poll_budget);
// Process at most1..32 events: -1=invalid call or latched failure,0=idle,1=progress,
// 2=budget exhausted (call again). No elapsed-time or service-latency guarantee.
// Unsupported power/mode faults disconnect; reprepare detached core to recover.
int chimera_usb_driver_poll(chimera_usb_driver *state, unsigned event_budget);
