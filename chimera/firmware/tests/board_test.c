// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include "board.h"

static void check(uint32_t initial) {
  chimera_gpio a, b, c;
  volatile uint32_t *ports[] = {(volatile uint32_t *)&a, (volatile uint32_t *)&b, (volatile uint32_t *)&c};
  for (unsigned p = 0; p < 3; ++p) {
    for (unsigned i = 0; i < sizeof(a) / sizeof(uint32_t); ++i) ports[p][i] = initial;
  }
  uint32_t clock = 0x80000000U;
  chimera_board_quiet(&a, &b, &c, &clock);
  assert(clock == 0x80000007U);
  // Active-low transceiver enables high; relay low; OBD-C ignition high/off.
  assert(a.BSRR == 1U);
  assert(c.BSRR == ((1U << 1) | (1U << 13)));
  assert(b.BSRR == ((1U << 16) | (1U << 1)));
  const uint32_t mask_a = 3U | (0x3FFU << 4);
  assert((a.MODER & mask_a) == 1U);
  assert((a.PUPDR & mask_a) == (1U | (0x155U << 4)));
  assert((a.MODER & ~mask_a) == (initial & ~mask_a));
  assert((a.PUPDR & ~mask_a) == (initial & ~mask_a));
  assert((b.MODER & 15U) == 5U);
  assert((b.PUPDR & 15U) == 6U);
  const uint32_t mask_c = (3U << 2) | (15U << 4) | (3U << 26);
  assert((c.MODER & mask_c) == ((1U << 2) | (15U << 4) | (1U << 26)));
  assert((c.PUPDR & mask_c) == ((1U << 2) | (1U << 26)));
  assert((c.MODER & ~mask_c) == (initial & ~mask_c));
  assert((c.PUPDR & ~mask_c) == (initial & ~mask_c));
  assert((b.MODER & ~15U) == (initial & ~15U));
  assert((b.PUPDR & ~15U) == (initial & ~15U));
  assert(a.OTYPER == (initial & ~1U));
  assert(b.OTYPER == (initial & ~3U));
  assert(c.OTYPER == (initial & ~((1U << 1) | (1U << 13))));
  assert(a.OSPEEDR == (initial & ~3U));
  assert(b.OSPEEDR == (initial & ~15U));
  assert(c.OSPEEDR == (initial & ~((3U << 2) | (3U << 26))));
  // No alternate functions, input data or direct output-data writes.
  for (unsigned p = 0; p < 3; ++p) {
    assert(ports[p][4] == initial && ports[p][5] == initial);
    assert(ports[p][7] == initial && ports[p][8] == initial && ports[p][9] == initial);
  }
}

int main(void) {
  _Static_assert(offsetof(chimera_gpio, BSRR) == 0x18, "GPIO register layout");
  check(0U);
  check(UINT32_MAX);
  check(0xA5963C69U);
  return 0;
}
