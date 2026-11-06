// SPDX-License-Identifier: MIT
#include "board.h"

static void output(chimera_gpio *gpio, unsigned pin, uint32_t pull) {
  const unsigned shift = pin * 2U;
  gpio->OTYPER &= ~(1U << pin);
  gpio->OSPEEDR &= ~(3U << shift);
  gpio->PUPDR = (gpio->PUPDR & ~(3U << shift)) | (pull << shift);
  gpio->MODER = (gpio->MODER & ~(3U << shift)) | (1U << shift);
}

void chimera_board_quiet(chimera_gpio *a, chimera_gpio *b, chimera_gpio *c,
                         volatile uint32_t *ahb1enr) {
  *ahb1enr |= 7U;
  (void)*ahb1enr;  // Clock-enable readback before accessing GPIO.

  // Preload all output latches before changing any pin to output mode.
  a->BSRR = 1U;                         // PA0: CAN3 disabled (active low).
  c->BSRR = (1U << 1) | (1U << 13);     // PC1/PC13: CAN1/CAN2 disabled.
  b->BSRR = (1U << 16) | (1U << 1);     // PB0 relay low; PB1 OBD-C ignition off.
  output(a, 0U, 1U);
  output(c, 1U, 1U);
  output(c, 13U, 1U);
  output(b, 0U, 2U);
  output(b, 1U, 1U);

  // PA2 OBD-C request, PA3 IGN, PA4 VSS, PA5 CPS, PA6 brake: input/pull-up.
  a->MODER &= ~(0x3FFU << 4);
  a->PUPDR = (a->PUPDR & ~(0x3FFU << 4)) | (0x155U << 4);
  // PC2/PC3: analog mode, no pulls. No ADC conversions in this target.
  c->MODER |= 15U << 4;
  c->PUPDR &= ~(15U << 4);
}
