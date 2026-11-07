// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "main.h"

static void revoke(chimera_main_runtime *r) {
  if (r->details != NULL) r->details->facts_valid = 0U;
}

static bool fail(chimera_main_runtime *r, enum chimera_main_usb_error error) {
  r->error = error;
  r->service_error = r->usb.error;
  r->state = CHIMERA_BOOT_USB_FAILED;
  revoke(r);
  // A failed service has already attempted release. Do not retry implicitly.
  if (r->usb.phase == CHIMERA_USB_SERVICE_DETACHED) {
    (void)chimera_usb_service_stop(&r->usb);
  }
  r->cleanup_ok = r->usb.cleanup_ok;
  return false;
}

bool chimera_main_start(chimera_main_runtime *r, volatile chimera_boot_details *details,
                        const chimera_usb_io *io, bool clock_ready, const chimera_main_usb_config *config) {
  if (r == NULL || (r->state != CHIMERA_BOOT_RESET && r->state != CHIMERA_BOOT_USB_STOPPED)) return false;
  r->details = details;
  r->error = CHIMERA_MAIN_USB_NONE;
  r->service_error = CHIMERA_USB_SERVICE_OK;
  r->vbus = CHIMERA_VBUS_UNKNOWN;
  r->cleanup_ok = 1U;
  revoke(r);
  if (details == NULL || (config != NULL &&
      (io == NULL || io->read32 == NULL || io->write32 == NULL || io->delay_us == NULL ||
       config->self_powered > 1U || config->max_power_2ma > 250U ||
       config->poll_budget == 0U || config->poll_budget > 1000000U ||
       config->event_budget == 0U || config->event_budget > 32U))) {
    r->state = CHIMERA_BOOT_ARGUMENT_FAILED;
    r->error = CHIMERA_MAIN_USB_ARGUMENT;
    return false;
  }
  r->state = chimera_main_prepare(details, io, clock_ready);
  if (r->state != CHIMERA_BOOT_USB_HELD || config == NULL) return false;
  r->config.self_powered = config->self_powered;
  r->config.max_power_2ma = config->max_power_2ma;
  r->config.poll_budget = config->poll_budget;
  r->config.event_budget = config->event_budget;
  if (!chimera_usb_service_start(&r->usb, io, r->config.self_powered,
                                 r->config.max_power_2ma, r->config.poll_budget)) {
    return fail(r, CHIMERA_MAIN_USB_START);
  }
  for (unsigned i = 0U; i < sizeof(r->usb.facts.uid); ++i) {
    if (r->usb.facts.uid[i] != details->facts.uid[i]) return fail(r, CHIMERA_MAIN_USB_IDENTITY);
  }
  r->state = CHIMERA_BOOT_USB_DETACHED;
  return true;
}

static bool present(chimera_main_runtime *r, const chimera_vbus_io *vbus) {
  enum chimera_vbus_state observed = CHIMERA_VBUS_UNKNOWN;
  if (vbus != NULL && vbus->sample != NULL) observed = vbus->sample(vbus->context);
  r->vbus = (observed == CHIMERA_VBUS_PRESENT || observed == CHIMERA_VBUS_ABSENT) ?
    observed : CHIMERA_VBUS_UNKNOWN;
  return r->vbus == CHIMERA_VBUS_PRESENT;
}

int chimera_main_poll(chimera_main_runtime *r, const chimera_vbus_io *vbus) {
  if (r == NULL || r->state != CHIMERA_BOOT_USB_DETACHED) return -1;
  if (!present(r, vbus)) {
    (void)fail(r, CHIMERA_MAIN_USB_POWER);
    return -1;
  }
  int result = chimera_usb_service_poll(&r->usb, r->config.event_budget);
  if (result < 0) {
    (void)fail(r, CHIMERA_MAIN_USB_POLL);
    return -1;
  }
  if (!present(r, vbus)) {
    (void)fail(r, CHIMERA_MAIN_USB_POWER);
    return -1;
  }
  return result;
}

bool chimera_main_stop(chimera_main_runtime *r) {
  if (r == NULL) return false;
  r->vbus = CHIMERA_VBUS_UNKNOWN;
  revoke(r);
  if (!chimera_usb_service_stop(&r->usb)) {
    r->state = CHIMERA_BOOT_USB_FAILED;
    r->error = CHIMERA_MAIN_USB_STOP;
    r->service_error = r->usb.error;
    r->cleanup_ok = r->usb.cleanup_ok;
    return false;
  }
  r->cleanup_ok = 1U;
  r->state = CHIMERA_BOOT_USB_STOPPED;
  return true;
}
