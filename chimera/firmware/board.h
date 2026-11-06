// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>

// STM32F413 GPIO offsets, checked against ST's stm32f413xx.h V2.6.0.
typedef struct {
  volatile uint32_t MODER, OTYPER, OSPEEDR, PUPDR, IDR, ODR, BSRR, LCKR, AFR[2];
} chimera_gpio;

// Source-defined inactive levels only; this does not qualify an electrical cutoff.
// Arguments permit native register-state tests without accessing a device.
void chimera_board_quiet(chimera_gpio *a, chimera_gpio *b, chimera_gpio *c,
                         volatile uint32_t *ahb1enr);
