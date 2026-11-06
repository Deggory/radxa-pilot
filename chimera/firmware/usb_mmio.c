// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "usb_time.h"

static uint32_t read32(void *context, uint32_t address) {
  (void)context;
  __asm__ volatile ("dmb" ::: "memory");
  uint32_t value = *(volatile uint32_t *)(uintptr_t)address;
  __asm__ volatile ("dmb" ::: "memory");
  return value;
}
static void write32(void *context, uint32_t address, uint32_t value) {
  (void)context;
  *(volatile uint32_t *)(uintptr_t)address = value;
  __asm__ volatile ("dsb" ::: "memory");
}
static bool delay(void *context, uint32_t us) {
  (void)context;
  const chimera_usb_io io = {.context=NULL, .read32=read32, .write32=write32, .delay_us=NULL};
  return chimera_usb_delay16(&io, us);
}
bool chimera_usb_mmio_init(chimera_usb_io *out) {
  if (out == NULL) return false;
  out->context=NULL; out->read32=NULL; out->write32=NULL; out->delay_us=NULL;
  const chimera_usb_io io = {.context=NULL, .read32=read32, .write32=write32, .delay_us=delay};
  if (!chimera_usb_time16_init(&io)) return false;
  out->read32=read32; out->write32=write32; out->delay_us=delay;
  return true;
}
