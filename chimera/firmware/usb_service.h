// SPDX-License-Identifier: MIT
#pragma once
#include "boot_facts.h"
#include "usb_driver.h"

enum chimera_usb_service_phase {
  CHIMERA_USB_SERVICE_STOPPED, CHIMERA_USB_SERVICE_DETACHED, CHIMERA_USB_SERVICE_FAILED
};
enum chimera_usb_service_error {
  CHIMERA_USB_SERVICE_OK, CHIMERA_USB_SERVICE_ARGUMENT, CHIMERA_USB_SERVICE_OWNERSHIP,
  CHIMERA_USB_SERVICE_FACTS, CHIMERA_USB_SERVICE_TIMING, CHIMERA_USB_SERVICE_CLOCK,
  CHIMERA_USB_SERVICE_CORE, CHIMERA_USB_SERVICE_DRIVER, CHIMERA_USB_SERVICE_INVARIANT,
  CHIMERA_USB_SERVICE_POLL, CHIMERA_USB_SERVICE_RELEASE
};
typedef struct {
  chimera_usb_io io;
  chimera_boot_facts facts;
  chimera_usb_driver driver;
  enum chimera_usb_service_phase phase;
  enum chimera_usb_service_error error;
  uint8_t owns_usb, facts_valid, cleanup_ok;
} chimera_usb_service;

// Zero-initialize before first use; never reset/copy/move a live context. Inputs
// must not alias state; callbacks/context remain trusted and alive. IO methods
// are copied, driver points into this stable context. Calls must be serialized.
// Caller owns a quiet board at HSI/HCLK16, main PLL and USB; USB starts gated.
// Profile values are caller-supplied, not qualified by this detached-only API.
// No main/IRQ/GPIO/attach/watchdog call. Failure latches until explicit stop.
bool chimera_usb_service_start(chimera_usb_service *state, const chimera_usb_io *io,
                              uint8_t self_powered, uint8_t max_power_2ma, uint32_t poll_budget);
// Same event-budget semantics as driver; invalid budget/phase does no I/O.
// Invariants are checked before/after polling; no connection is permitted.
int chimera_usb_service_poll(chimera_usb_service *state, unsigned event_budget);
// Explicitly release owned USB: soft-disconnect/mask/PHY-off when accessible,
// hold reset and gate clock; check readbacks. Failure leaves context latched.
// No restoration of PLL/HSE/debug settings. Already stopped is an I/O-free no-op.
bool chimera_usb_service_stop(chimera_usb_service *state);
