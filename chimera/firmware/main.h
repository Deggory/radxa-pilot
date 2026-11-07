// SPDX-License-Identifier: MIT
#pragma once
#include "boot_facts.h"

// Local debugger diagnostics, not USB health or an operational capability.
enum chimera_main_state {
  CHIMERA_BOOT_RESET = 0,
  CHIMERA_BOOT_CLOCK_READY = 1,
  CHIMERA_BOOT_CLOCK_FAILED = 2,
  CHIMERA_BOOT_FAULT = 3,
  CHIMERA_BOOT_FACTS_FAILED = 4,
  CHIMERA_BOOT_USB_HELD = 5,
  CHIMERA_BOOT_ARGUMENT_FAILED = 6
};

typedef struct {
  chimera_boot_facts facts;
  uint32_t facts_valid;
} chimera_boot_details;

// Call after RAM/IRQ/quiet-board setup. Serialized, separate non-aliasing state
// and trusted callbacks, valid F413 readable address space. No peripheral writes
// or delay calls. Clock failure performs no reads. Success captures facts and
// returns USB_HELD: power/VBUS/current recovery are still unqualified. Never ready.
// Every call revokes facts_valid before checking; failure retains old raw bytes
// for diagnosis, with facts_valid=0. This is not a concurrent publication API.
enum chimera_main_state chimera_main_prepare(volatile chimera_boot_details *details,
                                           const chimera_usb_io *io, bool clock_ready);
