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

// Software controller policy, not a physical VBUS observation or wire ABI.
// Zero/default preserves the original unforced detached preparation.
enum chimera_usb_session_mode {
  CHIMERA_USB_SESSION_UNFORCED = 0,
  CHIMERA_USB_SESSION_LEGACY_NO_VBUS = 1
};
// STM32F413 GOTGCTL A/B session override fields (CMSIS V2.6.0 bits4..7).
#define CHIMERA_USB_SESSION_OVERRIDE_MASK 0xF0U
static inline bool chimera_usb_session_mode_valid(enum chimera_usb_session_mode mode) {
  return mode == CHIMERA_USB_SESSION_UNFORCED || mode == CHIMERA_USB_SESSION_LEGACY_NO_VBUS;
}
// Caller must first validate mode. Legacy enables only BVALOEN/BVALOVAL.
static inline uint32_t chimera_usb_session_override(enum chimera_usb_session_mode mode) {
  return mode == CHIMERA_USB_SESSION_LEGACY_NO_VBUS ? 0xC0U : 0U;
}

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
// Same detached-only contract. Invalid mode fails before IO. Explicit legacy
// mode forces B-session-valid as the original F413 code does, without claiming
// cable/power detection. VBDEN remains off; SDIS remains set in both modes.
bool chimera_usb_core_detached_mode(const chimera_usb_io *io, uint32_t poll_budget,
                                    enum chimera_usb_session_mode mode);
