// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "main.h"

enum chimera_main_state chimera_main_prepare(volatile chimera_boot_details *details,
                                           const chimera_usb_io *io, bool clock_ready) {
  if (details == NULL) return CHIMERA_BOOT_ARGUMENT_FAILED;
  details->facts_valid = 0U;
  if (!clock_ready) return CHIMERA_BOOT_CLOCK_FAILED;
  if (io == NULL || io->read32 == NULL) return CHIMERA_BOOT_ARGUMENT_FAILED;
  chimera_boot_facts facts;
  if (!chimera_boot_read_facts(io, &facts)) return CHIMERA_BOOT_FACTS_FAILED;
  for (unsigned i = 0U; i < sizeof(facts.uid); ++i) details->facts.uid[i] = facts.uid[i];
  details->facts.reset_csr = facts.reset_csr;
  details->facts.option_control = facts.option_control;
  details->facts_valid = 1U;
  return CHIMERA_BOOT_USB_HELD;
}

// Native fixtures execute the actual preparation function above. ARM reset,
// memory/IRQ initialization and MMIO binding are checked in the real ARM image.
#ifndef CHIMERA_MAIN_NATIVE_TEST
#include "board.h"
#include "usb_time.h"

#define REG32(address) (*(volatile uint32_t *)(address))
#define RCC_CR REG32(0x40023800U)
#define RCC_CFGR REG32(0x40023808U)
#define RCC_AHB1ENR REG32(0x40023830U)
#define RCC_AHB2ENR REG32(0x40023834U)
#define RCC_APB1ENR REG32(0x40023840U)

extern uint32_t __data_load[], __data_start[], __data_end[], __bss_start[], __bss_end[];
extern const uint32_t chimera_vectors[];

// Debugger-readable only. No host protocol or operational health claim.
volatile uint32_t chimera_boot_magic = 0x4348494DU;
volatile uint32_t chimera_boot_state;
volatile chimera_boot_details chimera_boot_snapshot;
chimera_main_runtime chimera_boot_runtime;

static void quiet(void) {
  chimera_board_quiet((chimera_gpio *)0x40020000U, (chimera_gpio *)0x40020400U,
                      (chimera_gpio *)0x40020800U, &RCC_AHB1ENR);
  RCC_APB1ENR &= ~((1U << 25) | (1U << 26) | (1U << 27)); // CAN1/2/3 clocks off.
  RCC_AHB2ENR &= ~(1U << 7);                             // USB FS clock off.
  __asm__ volatile ("dsb" ::: "memory");
}

static bool wait_bits(volatile uint32_t *reg, uint32_t mask, uint32_t value) {
  // A bounded polling budget, not a calibrated time interval.
  for (uint32_t remaining = 1000000U; remaining != 0U; --remaining) {
    if ((*reg & mask) == value) return true;
  }
  return false;
}

static bool clock_hsi(void) {
  // Bootstub may hand off at PLL frequency: switch first, then remove divisors.
  RCC_CR |= 1U;
  if (!wait_bits(&RCC_CR, 1U << 1, 1U << 1)) return false;
  RCC_CFGR &= ~3U;
  if (!wait_bits(&RCC_CFGR, 3U << 2, 0U)) return false;
  RCC_CFGR &= ~((15U << 4) | (7U << 10) | (7U << 13));
  // Existing flash wait states remain conservative; no PLL/HSE or USB clock setup.
  return true;
}

static _Noreturn void park(void) {
  for (;;) __asm__ volatile ("wfi");
}

_Noreturn void chimera_fault(void) {
  quiet();
  chimera_boot_snapshot.facts_valid = 0U;
  chimera_boot_runtime.state = CHIMERA_BOOT_FAULT;
  chimera_boot_state = CHIMERA_BOOT_FAULT;
  park();
}

_Noreturn void chimera_reset(void) {
  uint32_t *source = __data_load;
  for (uint32_t *dest = __data_start; dest < __data_end; ++dest) *dest = *source++;
  for (uint32_t *dest = __bss_start; dest < __bss_end; ++dest) *dest = 0U;

  REG32(0xE000E010U) = 0U;  // Disable inherited SysTick.
  for (unsigned bank = 0U; bank < 4U; ++bank) {
    REG32(0xE000E180U + bank * 4U) = UINT32_MAX; // NVIC interrupt disable.
    REG32(0xE000E280U + bank * 4U) = UINT32_MAX; // NVIC pending clear.
  }
  REG32(0xE000ED04U) = (1U << 25) | (1U << 27); // Clear pending SysTick/PendSV.
  REG32(0xE000ED08U) = (uint32_t)chimera_vectors;
  __asm__ volatile ("dsb\n isb" ::: "memory");
  quiet();
  const bool clock_ready = clock_hsi();
  chimera_usb_io io;
  const chimera_usb_io *boot_io = NULL;
  // Binding has no MMIO side effects. NULL profile deliberately keeps this
  // board build held until power/VBUS/recovery qualification is complete.
  if (clock_ready && chimera_usb_mmio_bind(&io)) boot_io = &io;
  (void)chimera_main_start(&chimera_boot_runtime, &chimera_boot_snapshot, boot_io, clock_ready, NULL);
  chimera_boot_state = chimera_boot_runtime.state;
  while (chimera_boot_runtime.state == CHIMERA_BOOT_USB_DETACHED) {
    if (chimera_main_poll(&chimera_boot_runtime) < 0) break;
  }
  chimera_boot_state = chimera_boot_runtime.state;
  // PRIMASK remains set. All inputs are reserved, no acquisition/IRQ enabled.
  // USB_HELD records the unmet power/VBUS/recovery prerequisites. No attach.
  park();
}
#endif
