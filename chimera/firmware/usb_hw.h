// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>

typedef struct {
  void *context;
  uint32_t (*read32)(void *context, uint32_t address);
  void (*write32)(void *context, uint32_t address, uint32_t value);
  bool (*delay_us)(void *context, uint32_t us);
} chimera_usb_io;

// Caller owns the clocks/controller exclusively. Backend must provide real
// ordered MMIO and a calibrated delay when eventually bound to hardware.
// Poll budgets are bounded read counts, not elapsed-time guarantees.
// Clock preconditions: HSI SYSCLK/AHB16MHz, HSE crystal (not bypass), USB gated.
// HSE16MHz is a source-defined board assumption, not measured by these routines.
// Success enables the clock with the USB peripheral held in reset.
bool chimera_usb_clock48(const chimera_usb_io *io, uint32_t poll_budget);
// Requires the verified clock register profile above and held peripheral reset.
// Leaves PHY powered and
// core configured but soft-disconnected, with interrupts masked and no endpoints
// armed. Failure after entry disconnects/masks/powers down the PHY. No attach API.
bool chimera_usb_core_detached(const chimera_usb_io *io, uint32_t poll_budget);
