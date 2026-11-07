// SPDX-License-Identifier: MIT
#pragma once
#include "boot_facts.h"
#include "usb_service.h"

// Local debugger diagnostics, not USB health or an operational capability.
enum chimera_main_state {
  CHIMERA_BOOT_RESET = 0,
  CHIMERA_BOOT_CLOCK_READY = 1,
  CHIMERA_BOOT_CLOCK_FAILED = 2,
  CHIMERA_BOOT_FAULT = 3,
  CHIMERA_BOOT_FACTS_FAILED = 4,
  CHIMERA_BOOT_USB_HELD = 5,
  CHIMERA_BOOT_ARGUMENT_FAILED = 6,
  CHIMERA_BOOT_USB_DETACHED = 7,
  CHIMERA_BOOT_USB_FAILED = 8,
  CHIMERA_BOOT_USB_STOPPED = 9
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

enum chimera_main_usb_error {
  CHIMERA_MAIN_USB_NONE, CHIMERA_MAIN_USB_ARGUMENT, CHIMERA_MAIN_USB_START,
  CHIMERA_MAIN_USB_IDENTITY, CHIMERA_MAIN_USB_POLL, CHIMERA_MAIN_USB_STOP
};
typedef struct {
  uint8_t self_powered, max_power_2ma;
  uint32_t poll_budget;
  unsigned event_budget;
} chimera_main_usb_config;
typedef struct {
  chimera_usb_service usb;
  volatile chimera_boot_details *details;
  chimera_main_usb_config config;
  enum chimera_main_state state;
  enum chimera_main_usb_error error;
  enum chimera_usb_service_error service_error;
  uint8_t cleanup_ok;
} chimera_main_runtime;

// Zero-initialize before first use; serialize calls, never copy/move live state.
// State, details, IO and config must not alias. Details and trusted IO context
// remain alive; config and callback members are copied. Same quiet-board/clock
// ownership preconditions as usb_service.h. NULL config captures facts only and
// leaves USB held. Explicit config permits DETACHED operation only, never attach.
// Start accepts RESET/USB_STOPPED only. Failures latch; explicit stop is required
// before retry. This lifecycle is not flashing/DFU or proven hardware recovery.
bool chimera_main_start(chimera_main_runtime *runtime, volatile chimera_boot_details *details,
                        const chimera_usb_io *io, bool clock_ready, const chimera_main_usb_config *config);
// Returns service poll result (0 idle, 1 progress, 2 budget exhausted), or -1.
// Non-detached states perform no I/O. Failure revokes the external facts snapshot.
int chimera_main_poll(chimera_main_runtime *runtime);
// Explicit cleanup/retry; success invalidates facts and permits a fresh start.
// Successful stop retains prior diagnostics until next start; failed stop records
// USB_STOP and the service release error. Already stopped is I/O-free.
bool chimera_main_stop(chimera_main_runtime *runtime);
