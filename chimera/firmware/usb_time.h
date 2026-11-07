// SPDX-License-Identifier: MIT
#pragma once
#include "usb_hw.h"

// Exclusive DWT cycle-counter use at nominal HSI/HCLK16MHz. No timer IRQ or
// CYCCNT reset. Preserves unrelated debug bits; reject absent/stopped counters.
bool chimera_usb_time16_init(const chimera_usb_io *io);
// 0..50000us, wrap-safe cycle arithmetic and bounded read count even if stopped.
// Caller keeps the CPU clock fixed and counter enabled for the entire operation.
bool chimera_usb_delay16(const chimera_usb_io *io, uint32_t us);
// ARM-only ordered volatile-MMIO callbacks. Binding only writes *out; it performs
// no peripheral reads/writes or timing initialization. False only for NULL out.
bool chimera_usb_mmio_bind(chimera_usb_io *out);
// Bind and initialize DWT timing. Out must not alias any other state; invalid
// init clears it. Startup currently uses bind/read32 only, not this initializer.
bool chimera_usb_mmio_init(chimera_usb_io *out);
