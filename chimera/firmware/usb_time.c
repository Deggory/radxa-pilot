// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "usb_time.h"

#define DEMCR 0xE000EDFCU
#define DWT_CTRL 0xE0001000U
#define CYCCNT 0xE0001004U

static bool clock16(const chimera_usb_io *io) {
  return io != NULL && io->read32 != NULL &&
    (io->read32(io->context, 0x40023800U) & 3U) == 3U &&
    (io->read32(io->context, 0x40023808U) & 255U) == 0U;
}
bool chimera_usb_time16_init(const chimera_usb_io *io) {
  if (!clock16(io) || io->write32 == NULL) return false;
  uint32_t ctrl = io->read32(io->context, DWT_CTRL);
  if ((ctrl & (1U << 25)) != 0U) return false;
  io->write32(io->context, DEMCR, io->read32(io->context, DEMCR) | (1U << 24));
  io->write32(io->context, DWT_CTRL, ctrl | 1U);
  if ((io->read32(io->context, DEMCR) & (1U << 24)) == 0U ||
      (io->read32(io->context, DWT_CTRL) & 1U) == 0U) return false;
  uint32_t start = io->read32(io->context, CYCCNT);
  for (unsigned i=0U; i<32U; ++i) if (io->read32(io->context, CYCCNT) != start) return true;
  return false;
}
bool chimera_usb_delay16(const chimera_usb_io *io, uint32_t us) {
  if (us > 50000U || !clock16(io) || (io->read32(io->context, DEMCR) & (1U << 24)) == 0U ||
      (io->read32(io->context, DWT_CTRL) & ((1U << 25) | 1U)) != 1U) return false;
  uint32_t cycles = us * 16U;
  uint32_t start = io->read32(io->context, CYCCNT);
  for (uint32_t i=0U; i<cycles+64U; ++i)
    if ((uint32_t)(io->read32(io->context, CYCCNT)-start) >= cycles) return true;
  return false;
}
