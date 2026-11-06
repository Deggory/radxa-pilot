// SPDX-License-Identifier: MIT
#pragma once
#include "usb_hw.h"

typedef struct {
  uint8_t uid[12];
  uint32_t reset_csr;
  uint32_t option_control;
} chimera_boot_facts;

// Read-only F413 source-defined UID/reset/option snapshot. Only read32 is used;
// no flag clearing, option write, watchdog start/feed or USB operation. Trusted
// callback, valid readable F413 address space, serialized calls, separate state.
// Eight reads on success; blank/allFF or inconsistent UID rejects with output
// untouched. Read callback cannot report a bus fault. Raw CSR flags may already
// have been changed by the bootstub; neither raw word proves watchdog is stopped,
// verifies firmware identity, attests a device or authorizes USB attachment.
bool chimera_boot_read_facts(const chimera_usb_io *io, chimera_boot_facts *out);
