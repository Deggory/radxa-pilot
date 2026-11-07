// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "main.h"

typedef struct {
  uint32_t uid[3], csr, opt, reads, uid_reads;
  int unstable;
} fake;

static uint32_t rd(void *context, uint32_t address) {
  fake *f = context;
  assert(++f->reads <= 8U);
  if (address >= 0x1FFF7A10U && address <= 0x1FFF7A18U && address % 4U == 0U) {
    unsigned i = (address - 0x1FFF7A10U) / 4U;
    ++f->uid_reads;
    return f->uid[i] ^ ((f->uid_reads > 3U && f->unstable == (int)i) ? 1U : 0U);
  }
  if (address == 0x40023874U) return f->csr;
  if (address == 0x40023C14U) return f->opt;
  assert(false);
  return 0U;
}

static void wr(void *context, uint32_t address, uint32_t value) {
  (void)context; (void)address; (void)value;
  assert(false);  // Startup snapshot must never write a peripheral.
}

static bool delay(void *context, uint32_t us) {
  (void)context; (void)us;
  assert(false);
  return false;
}

int main(void) {
  fake f = {.uid = {0x0044003aU, 0x30335116U, 0x36363738U}, .unstable = -1};
  chimera_usb_io io = {.context = &f, .read32 = rd, .write32 = wr, .delay_us = delay};
  struct { uint32_t before; chimera_boot_details details; uint32_t after; } output;
  memset(&output, 0xa5, sizeof(output));

  assert(CHIMERA_BOOT_CLOCK_READY == 1 && CHIMERA_BOOT_CLOCK_FAILED == 2 && CHIMERA_BOOT_FAULT == 3);
  assert(chimera_main_prepare(&output.details, &io, false) == CHIMERA_BOOT_CLOCK_FAILED);
  assert(f.reads == 0U && output.details.facts_valid == 0U);
  const chimera_boot_facts untouched = output.details.facts;
  assert(chimera_main_prepare(NULL, &io, true) == CHIMERA_BOOT_ARGUMENT_FAILED);
  assert(chimera_main_prepare(&output.details, NULL, true) == CHIMERA_BOOT_ARGUMENT_FAILED);
  io.read32 = NULL;
  assert(chimera_main_prepare(&output.details, &io, true) == CHIMERA_BOOT_ARGUMENT_FAILED);
  assert(f.reads == 0U && memcmp(&untouched, &output.details.facts, sizeof(untouched)) == 0);
  io.read32 = rd;

  for (unsigned i = 0U; i < 65536U; ++i) {
    f.uid[0] = 0x0044003aU ^ i;
    f.csr = (i << 16) | i;
    f.opt = ~f.csr;
    f.reads = f.uid_reads = 0U;
    assert(chimera_main_prepare(&output.details, &io, true) == CHIMERA_BOOT_USB_HELD);
    assert(f.reads == 8U && output.details.facts_valid == 1U);
    assert(output.details.facts.reset_csr == f.csr && output.details.facts.option_control == f.opt);
    for (unsigned j = 0U; j < 12U; ++j) {
      assert(output.details.facts.uid[j] == (uint8_t)(f.uid[j / 4U] >> ((j % 4U) * 8U)));
    }
    assert(output.before == 0xa5a5a5a5U && output.after == 0xa5a5a5a5U);
  }

  // A later failed preparation revokes validity; no stale snapshot becomes ready.
  const chimera_boot_facts saved = output.details.facts;
  for (int i = 0; i < 3; ++i) {
    f.unstable = i; f.reads = f.uid_reads = 0U;
    assert(chimera_main_prepare(&output.details, &io, true) == CHIMERA_BOOT_FACTS_FAILED);
    assert(output.details.facts_valid == 0U && memcmp(&saved, &output.details.facts, sizeof(saved)) == 0);
  }
  f.unstable = -1;
  for (unsigned invalid = 0U; invalid < 2U; ++invalid) {
    for (unsigned j = 0U; j < 3U; ++j) f.uid[j] = invalid ? UINT32_MAX : 0U;
    f.reads = f.uid_reads = 0U;
    assert(chimera_main_prepare(&output.details, &io, true) == CHIMERA_BOOT_FACTS_FAILED);
    assert(output.details.facts_valid == 0U && f.reads == 3U);
    assert(memcmp(&saved, &output.details.facts, sizeof(saved)) == 0);
  }
  f.uid[0] = 1U; f.reads = f.uid_reads = 0U;
  assert(chimera_main_prepare(&output.details, &io, true) == CHIMERA_BOOT_USB_HELD);
  assert(output.details.facts_valid == 1U);
  assert(output.before == 0xa5a5a5a5U && output.after == 0xa5a5a5a5U);
  puts("Main startup: 65536 snapshots, clock/argument/UID failures, validity revocation and canaries pass; USB held, zero writes/delays");
}
