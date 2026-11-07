// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "usb_hw.h"

#define CR 0x40023800U
#define PLLCFGR 0x40023804U
#define CFGR 0x40023808U
#define AHB2RSTR 0x40023814U
#define AHB2ENR 0x40023834U
#define DCKCFGR2 0x40023894U
#define GOTGCTL 0x50000000U
#define GAHBCFG 0x50000008U
#define GUSBCFG 0x5000000CU
#define GRSTCTL 0x50000010U
#define GINTSTS 0x50000014U
#define GINTMSK 0x50000018U
#define GRXFSIZ 0x50000024U
#define TX0FSIZ 0x50000028U
#define GCCFG 0x50000038U
#define DCFG 0x50000800U
#define DCTL 0x50000804U
#define PCGCCTL 0x50000E00U
#define PLL_FIELDS 0x0F437FFFU
#define PLL_USB48 0x04401808U // HSE16 /M8 *N96 /Q4 =48MHz; P2 unselected96MHz.

static bool valid(const chimera_usb_io *io, uint32_t budget) {
  return io != NULL && io->read32 != NULL && io->write32 != NULL && io->delay_us != NULL &&
         budget != 0U && budget <= 1000000U;
}
static uint32_t read_reg(const chimera_usb_io *io, uint32_t address) {
  return io->read32(io->context, address);
}
static void write_reg(const chimera_usb_io *io, uint32_t address, uint32_t value) {
  io->write32(io->context, address, value);
}
static void update(const chimera_usb_io *io, uint32_t address, uint32_t clear, uint32_t set) {
  write_reg(io, address, (read_reg(io, address) & ~clear) | set);
}
static bool wait_reg(const chimera_usb_io *io, uint32_t address, uint32_t mask, uint32_t value, uint32_t budget) {
  for (uint32_t i = 0U; i < budget; ++i) if ((read_reg(io, address) & mask) == value) return true;
  return false;
}

bool chimera_usb_clock48(const chimera_usb_io *io, uint32_t poll_budget) {
  if (!valid(io, poll_budget)) return false;
  if ((read_reg(io, CR) & (3U | (1U << 18))) != 3U || (read_reg(io, CFGR) & 255U) != 0U ||
      (read_reg(io, AHB2ENR) & 128U) != 0U) return false; // No writes on ownership/precondition failure.
  update(io, AHB2RSTR, 0U, 128U); // Hold inherited core reset before enabling its new clock.
  if ((read_reg(io, AHB2RSTR) & 128U) == 0U) return false;
  update(io, CR, 1U << 24, 0U);
  if (!wait_reg(io, CR, 1U << 25, 0U, poll_budget)) return false;
  update(io, CR, 0U, 1U << 16);
  if (!wait_reg(io, CR, 1U << 17, 1U << 17, poll_budget)) return false;
  update(io, PLLCFGR, PLL_FIELDS, PLL_USB48);
  update(io, DCKCFGR2, 1U << 27, 0U); // CK48MSEL0: main PLLQ.
  update(io, CR, 0U, 1U << 24);
  if (!wait_reg(io, CR, 1U << 25, 1U << 25, poll_budget)) {
    update(io, CR, 1U << 24, 0U);
    return false;
  }
  update(io, AHB2ENR, 0U, 128U);
  return (read_reg(io, AHB2ENR) & 128U) != 0U;
}

static bool clock_ready(const chimera_usb_io *io) {
  const uint32_t ready = 3U | (3U << 16) | (3U << 24);
  return (read_reg(io, CR) & (ready | (1U << 18))) == ready &&
         (read_reg(io, CFGR) & 255U) == 0U && (read_reg(io, PLLCFGR) & PLL_FIELDS) == PLL_USB48 &&
         (read_reg(io, DCKCFGR2) & (1U << 27)) == 0U && (read_reg(io, AHB2ENR) & 128U) != 0U;
}
static bool core_failure(const chimera_usb_io *io) {
  write_reg(io, DCTL, 2U);
  write_reg(io, GAHBCFG, 0U);
  write_reg(io, GINTMSK, 0U);
  update(io, GOTGCTL, CHIMERA_USB_SESSION_OVERRIDE_MASK, 0U);
  update(io, GCCFG, 1U << 16, 0U);
  return false;
}

bool chimera_usb_core_detached(const chimera_usb_io *io, uint32_t poll_budget) {
  return chimera_usb_core_detached_mode(io, poll_budget, CHIMERA_USB_SESSION_UNFORCED);
}
bool chimera_usb_core_detached_mode(const chimera_usb_io *io, uint32_t poll_budget,
                                    enum chimera_usb_session_mode mode) {
  if (!chimera_usb_session_mode_valid(mode) || !valid(io, poll_budget) ||
      !clock_ready(io) || (read_reg(io, AHB2RSTR) & 128U) == 0U) return false;
  update(io, AHB2RSTR, 128U, 0U); // Reset defaults keep PHY off until SDIS is established below.
  if ((read_reg(io, AHB2RSTR) & 128U) != 0U) return false;
  write_reg(io, DCTL, 2U); // SDIS before touching/resetting the PHY.
  write_reg(io, GAHBCFG, 0U);
  write_reg(io, GINTMSK, 0U);
  update(io, GCCFG, 1U << 16, 0U);
  write_reg(io, PCGCCTL, 0U);
  write_reg(io, GUSBCFG, 1U << 6); // Internal FS PHY before core reset.
  if (!wait_reg(io, GRSTCTL, 1U << 31, 1U << 31, poll_budget)) return core_failure(io);
  write_reg(io, GRSTCTL, 1U);
  if (!wait_reg(io, GRSTCTL, 1U, 0U, poll_budget)) return core_failure(io);
  write_reg(io, DCTL, 2U); // Reset may have cleared SDIS; PHY is still off.
  write_reg(io, GUSBCFG, (1U << 6) | (1U << 30) | (13U << 10)); // ST HCLK16MHz TRDT.
  if (!io->delay_us(io->context, 50000U) || !wait_reg(io, GINTSTS, 1U, 0U, poll_budget)) return core_failure(io);
  update(io, GOTGCTL, CHIMERA_USB_SESSION_OVERRIDE_MASK, chimera_usb_session_override(mode));
  update(io, GCCFG, 1U << 21, 1U << 16);
  update(io, DCFG, (127U << 4) | 3U, 3U); // Address0, full-speed internal PHY.
  write_reg(io, GRXFSIZ, 128U);
  write_reg(io, TX0FSIZ, (64U << 16) | 128U);
  if (!wait_reg(io, GRSTCTL, 1U << 31, 1U << 31, poll_budget)) return core_failure(io);
  write_reg(io, GRSTCTL, 1U << 5);
  if (!wait_reg(io, GRSTCTL, 1U << 5, 0U, poll_budget)) return core_failure(io);
  if (!wait_reg(io, GRSTCTL, 1U << 31, 1U << 31, poll_budget)) return core_failure(io);
  write_reg(io, GRSTCTL, 1U << 4);
  if (!wait_reg(io, GRSTCTL, 1U << 4, 0U, poll_budget)) return core_failure(io);
  if ((read_reg(io, GOTGCTL) & CHIMERA_USB_SESSION_OVERRIDE_MASK) != chimera_usb_session_override(mode))
    return core_failure(io);
  return true; // Still disconnected; no interrupt, GPIO, endpoint or FIFO traffic.
}
