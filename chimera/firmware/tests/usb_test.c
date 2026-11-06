// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "usb_hw.h"
#include "usb_ep0.h"

typedef struct { uint32_t address, value; } reg;
typedef struct {
  reg regs[24];
  unsigned count, reads, writes, delay, failure, core_resets;
} fake_hw;
static unsigned hw_cases, setup_cases;

static uint32_t *cell(fake_hw *hw, uint32_t address) {
  for (unsigned i = 0; i < hw->count; ++i) if (hw->regs[i].address == address) return &hw->regs[i].value;
  assert(hw->count < 24);
  hw->regs[hw->count] = (reg){address, 0};
  return &hw->regs[hw->count++].value;
}
static uint32_t read32(void *context, uint32_t address) {
  fake_hw *hw = context;
  ++hw->reads;
  if (address >= 0x50000000U) {
    assert((*cell(hw, 0x40023834U) & 128U) && !(*cell(hw, 0x40023814U) & 128U));
  }
  uint32_t *value = cell(hw, address);
  if (address == 0x40023800U) {
    if ((*value & (1U << 16)) && hw->failure != 1) *value |= 1U << 17;
    if (*value & (1U << 24)) {
      if (hw->failure != 3) *value |= 1U << 25;
    } else if (hw->failure != 2) *value &= ~(1U << 25);
  }
  if (address == 0x50000010U) {
    if (hw->failure == 10 && hw->core_resets != 0) *value &= ~(1U << 31);
    else if (hw->failure != 4) *value |= 1U << 31;
    if (hw->failure != 5) *value &= ~1U;
    if (hw->failure != 8) *value &= ~(1U << 5);
    if (hw->failure != 9) *value &= ~(1U << 4);
  }
  if (address == 0x50000014U && hw->failure == 6) return 1;
  return *value;
}
static void write32(void *context, uint32_t address, uint32_t value) {
  fake_hw *hw = context;
  ++hw->writes;
  const uint32_t allowed[] = {0x40023800U, 0x40023804U, 0x40023814U, 0x40023834U, 0x40023894U,
    0x50000000U, 0x50000008U, 0x5000000CU, 0x50000010U, 0x50000018U, 0x50000024U,
    0x50000028U, 0x50000038U, 0x50000800U, 0x50000804U, 0x50000E00U};
  bool known = false;
  for (unsigned i = 0; i < sizeof(allowed) / sizeof(allowed[0]); ++i) known |= address == allowed[i];
  assert(known); // No GPIO/CAN or unrelated peripheral writes.
  if (address >= 0x50000000U) {
    assert((*cell(hw, 0x40023834U) & 128U) && !(*cell(hw, 0x40023814U) & 128U));
  }
  if (address == 0x40023834U && (value & 128U)) assert(*cell(hw, 0x40023814U) & 128U);
  if (address == 0x40023814U && hw->failure == 11) return; // Reset hold did not latch.
  if (address == 0x40023814U && hw->failure == 12 && (value & 128U) == 0U) return; // Reset release stuck.
  if (address == 0x50000038U && (value & (1U << 16))) {
    assert(*cell(hw, 0x50000804U) & 2U); // Never power the PHY while connected.
  }
  *cell(hw, address) = value;
  if (address == 0x50000010U && (value & 1U)) {
    ++hw->core_resets;
    *cell(hw, 0x50000804U) = 0; // Model reset clearing device controls.
    *cell(hw, 0x50000038U) = 0;
  }
}
static bool delay_us(void *context, uint32_t us) {
  fake_hw *hw = context;
  assert(us == 50000U);
  hw->delay += us;
  return hw->failure != 7;
}
static void hardware(void) {
  for (unsigned failure = 0; failure <= 11; ++failure) {
    fake_hw hw = {.failure = failure};
    *cell(&hw, 0x40023800U) = 3U | (1U << 24) | (1U << 25);
    *cell(&hw, 0x40023804U) = 0x20000000U;
    *cell(&hw, 0x40023894U) = 0xFFFFFFFFU;
    chimera_usb_io io = {&hw, read32, write32, delay_us};
    bool clock = chimera_usb_clock48(&io, 4);
    assert(clock == (failure == 0 || (failure >= 4 && failure <= 10)));
    if (clock) {
      assert(*cell(&hw, 0x40023814U) & 128U); // Core held reset while clocks change.
      assert((*cell(&hw, 0x40023804U) & 0x0F437FFFU) == 0x04401808U);
      assert(*cell(&hw, 0x40023804U) & 0x20000000U); // Preserve unrelated PLLR.
      assert(!(*cell(&hw, 0x40023894U) & (1U << 27)));
      assert(chimera_usb_core_detached(&io, 4) == (failure == 0));
      assert(*cell(&hw, 0x50000804U) & 2U);
      assert(*cell(&hw, 0x50000008U) == 0 && *cell(&hw, 0x50000018U) == 0);
      if (failure == 0) {
        assert((*cell(&hw, 0x5000000CU) & (15U << 10)) == (13U << 10));
        assert(*cell(&hw, 0x50000024U) == 128U);
        assert(*cell(&hw, 0x50000028U) == ((64U << 16) | 128U));
        assert(hw.delay == 50000U);
      }
    } else assert(!(*cell(&hw, 0x40023834U) & 128U));
    assert(hw.reads < 150 && hw.writes < 60);
    ++hw_cases;
  }
  for (unsigned bad = 0; bad < 5; ++bad) {
    fake_hw hw = {0};
    *cell(&hw, 0x40023800U) = 3U;
    if (bad == 0) *cell(&hw, 0x40023808U) = 8; // PLL selected.
    if (bad == 1) *cell(&hw, 0x40023808U) = 0x80; // Divided AHB.
    if (bad == 2) *cell(&hw, 0x40023834U) = 128; // Already active USB owner.
    if (bad == 3) *cell(&hw, 0x40023800U) |= 1U << 18; // HSE bypass.
    chimera_usb_io io = {&hw, read32, write32, delay_us};
    assert(!chimera_usb_clock48(&io, bad == 4 ? 0 : 4));
    assert(hw.writes == 0);
    ++hw_cases;
  }
  fake_hw hw = {0};
  chimera_usb_io io = {&hw, read32, write32, delay_us};
  assert(!chimera_usb_core_detached(&io, 4) && hw.writes == 0);
  assert(!chimera_usb_clock48(NULL, 4));
  assert(!chimera_usb_clock48(&io, 1000001U) && hw.writes == 0);
  io.delay_us = NULL;
  assert(!chimera_usb_clock48(&io, 4));
  io.delay_us = delay_us;
  io.write32 = NULL;
  assert(!chimera_usb_clock48(&io, 4));
  io.write32 = write32;
  io.read32 = NULL;
  assert(!chimera_usb_clock48(&io, 4));
  ++hw_cases;
  fake_hw stuck = {.failure = 12};
  *cell(&stuck, 0x40023800U) = 3U;
  chimera_usb_io stuck_io = {&stuck, read32, write32, delay_us};
  assert(chimera_usb_clock48(&stuck_io, 4));
  assert(!chimera_usb_core_detached(&stuck_io, 4) && (*cell(&stuck, 0x40023814U) & 128U));
  ++hw_cases;
}

static const uint8_t uid[12] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
static void init(chimera_usb_ep0 *s) { assert(chimera_usb_ep0_init(s, uid, 1, 50)); }
static bool in_done(chimera_usb_ep0 *s) { return chimera_usb_ep0_in_complete(s, s->generation); }
static bool out_done(chimera_usb_ep0 *s, size_t size) { return chimera_usb_ep0_out_complete(s, s->generation, size); }
static int request(chimera_usb_ep0 *s, unsigned bm, unsigned req, unsigned value,
                   unsigned index, unsigned length, uint8_t *data, size_t capacity) {
  uint8_t setup[8] = {bm, req, value, value >> 8, index, index >> 8, length, length >> 8};
  ++setup_cases;
  return chimera_usb_ep0_setup(s, setup, 8, data, capacity);
}
static void configure(chimera_usb_ep0 *s) {
  assert(request(s, 0, 5, 7, 0, 0, NULL, 0) == 0 && s->address == 0);
  assert(in_done(s) && s->address == 7);
  assert(request(s, 0, 9, 1, 0, 0, NULL, 0) == 0 && s->configuration == 0);
  assert(in_done(s) && s->configuration == 1);
}
static void endpoint_zero(void) {
  chimera_usb_ep0 s;
  init(&s);
  assert(s.serial[0] == 50 && s.serial[1] == 3);
  const char *hex = "000102030405060708090a0b";
  for (unsigned i = 0; i < 24; ++i) assert(s.serial[2 + i * 2] == hex[i] && s.serial[3 + i * 2] == 0);
  uint8_t data[80];
  // Address/configuration changes commit only after status-IN completion.
  assert(request(&s, 0, 5, 9, 0, 0, NULL, 0) == 0);
  assert(request(&s, 0x80, 6, 0x100, 0, 8, data, 64) == 8); // New SETUP cancels it.
  assert(in_done(&s));
  assert(out_done(&s, 0) && s.address == 0);
  assert(request(&s, 0, 5, 8, 0, 0, NULL, 0) == 0);
  uint32_t canceled = s.generation;
  assert(request(&s, 0, 5, 9, 0, 0, NULL, 0) == 0);
  assert(!chimera_usb_ep0_in_complete(&s, canceled) && s.address == 0);
  assert(!chimera_usb_ep0_out_complete(&s, canceled, 0) && s.phase == CHIMERA_EP0_STATUS_IN);
  chimera_usb_ep0_reset(&s);
  configure(&s);
  const uint8_t expected_device[] = {18, 1, 0, 2, 0, 0, 0, 64, 0xAA, 0xBB, 0xCC, 0xDD, 0, 1, 1, 2, 3, 1};
  assert(request(&s, 0x80, 6, 0x100, 0, 64, data, 64) == 18 && memcmp(data, expected_device, 18) == 0);
  const char *strings[] = {"RetroPilot", "Chimera F413", "000102030405060708090a0b"};
  for (unsigned i = 0; i < 3; ++i) {
    size_t size = strlen(strings[i]);
    assert(request(&s, 0x80, 6, 0x301 + i, 0x409, 64, data, 64) == (int)(2 * size + 2));
    assert(data[0] == 2 * size + 2 && data[1] == 3);
    for (size_t j = 0; j < size; ++j) assert(data[2 + j * 2] == strings[i][j] && data[3 + j * 2] == 0);
  }
  assert(request(&s, 0x80, 6, 0x200, 0, 255, data, 64) == 18);
  assert(data[2] == 18 && data[7] == 0xC0 && data[8] == 50 && data[13] == 0); // No bulk endpoints.
  assert(request(&s, 0x80, 0, 0, 0, 2, data, 64) == 2 && data[0] == 1 && data[1] == 0);
  assert(request(&s, 0x80, 8, 0, 0, 1, data, 64) == 1 && data[0] == 1);
  assert(request(&s, 0x81, 10, 0, 0, 1, data, 64) == 1 && data[0] == 0);
  assert(request(&s, 1, 11, 0, 0, 0, NULL, 0) == 0 && in_done(&s));
  assert(request(&s, 0x82, 0, 0, 0x81, 2, data, 64) == -1);
  assert(request(&s, 0, 5, 10, 0, 0, NULL, 0) == -1 && s.address == 7);
  // All request types/numbers, with a configured device and zero parameters.
  for (unsigned bm = 0; bm < 256; ++bm) for (unsigned req = 0; req < 256; ++req) {
    memset(data, 0xA5, sizeof(data));
    int expected = bm == 0xC0 && req == 0xA0 ? 32 : bm == 0xC0 && req == 0xD6 ? 25 : -1;
    assert(request(&s, bm, req, 0, 0, 64, data + 8, 64) == expected);
    if (expected < 0) for (unsigned i = 0; i < sizeof(data); ++i) assert(data[i] == 0xA5);
  }
  const unsigned descriptors[] = {0x100, 0x200, 0x300, 0x301, 0x302, 0x303};
  const unsigned sizes[] = {18, 18, 4, 22, 26, 50};
  for (unsigned d = 0; d < 6; ++d) for (unsigned length = 0; length <= 65535; ++length) {
    const unsigned index = d >= 3 ? 0x409 : 0;
    const unsigned size = length < sizes[d] ? length : sizes[d];
    memset(data, 0xA5, sizeof(data));
    assert(request(&s, 0x80, 6, descriptors[d], index, length, data + 8, 64) == (int)size);
    for (unsigned i = 0; i < sizeof(data); ++i) if (i < 8 || i >= 8 + size) assert(data[i] == 0xA5);
  }
  assert(request(&s, 0xC0, 0xA0, 0, 0, 64, data, 31) == -1);
  assert(request(&s, 0x80, 6, 0x303, 0x409, 64, data, 49) == -1);
  assert(request(&s, 0x80, 6, 0x303, 0, 64, data, 64) == -1);
  uint8_t setup[8] = {0xC0, 0xD6, 0, 0, 0, 0, 64, 0};
  for (size_t size = 0; size <= 16; ++size) {
    ++setup_cases;
    memset(data, 0xA5, sizeof(data));
    assert(chimera_usb_ep0_setup(&s, setup, size, data, 64) == (size == 8 ? 25 : -1));
    if (size != 8) for (unsigned i = 0; i < sizeof(data); ++i) assert(data[i] == 0xA5);
  }
  assert(request(&s, 0, 9, 0, 0, 0, NULL, 0) == 0 && s.configuration == 1);
  assert(in_done(&s) && s.configuration == 0 && s.address == 7);
  assert(request(&s, 0xC0, 0xD6, 0, 0, 64, data, 64) == -1);
  assert(request(&s, 0, 5, 128, 0, 0, NULL, 0) == -1);
  chimera_usb_ep0_reset(&s);
  assert(!in_done(&s) && s.address == 0 && s.configuration == 0);
  assert(chimera_usb_ep0_setup(&s, NULL, 0, data, 64) == -1);
  assert(chimera_usb_ep0_init(&s, uid, 0, 100));
  configure(&s);
  assert(request(&s, 0x80, 6, 0x200, 0, 64, data, 64) == 18 && data[7] == 0x80 && data[8] == 100);
  assert(request(&s, 0x80, 0, 0, 0, 2, data, 64) == 2 && data[0] == 0);
  assert(in_done(&s) && !out_done(&s, 1));
  s.generation = UINT32_MAX;
  assert(request(&s, 0, 9, 0, 0, 0, NULL, 0) == -1 && !s.initialized);
  uint8_t blank[12] = {0};
  assert(!chimera_usb_ep0_init(&s, blank, 0, 50));
  assert(!chimera_usb_ep0_init(&s, uid, 2, 50));
  assert(!chimera_usb_ep0_init(&s, uid, 1, 251));
}
int main(void) {
  hardware();
  endpoint_zero();
  printf("USB fake-register scenarios=%u SETUP cases=%u; no hardware calls\n", hw_cases, setup_cases);
  return 0;
}
