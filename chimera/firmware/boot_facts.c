// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "boot_facts.h"

bool chimera_boot_read_facts(const chimera_usb_io *io, chimera_boot_facts *out) {
  if(io==NULL || io->read32==NULL || out==NULL) return false;
  uint32_t uid[3];
  uint32_t any=0U, all=UINT32_MAX;
  for(unsigned i=0;i<3U;++i) {
    uid[i]=io->read32(io->context,0x1FFF7A10U+i*4U);
    any|=uid[i];all&=uid[i];
  }
  if(any==0U || all==UINT32_MAX) return false;
  uint32_t csr=io->read32(io->context,0x40023874U);
  uint32_t opt=io->read32(io->context,0x40023C14U);
  for(unsigned i=0;i<3U;++i) if(io->read32(io->context,0x1FFF7A10U+i*4U)!=uid[i]) return false;
  for(unsigned i=0;i<12U;++i) out->uid[i]=(uint8_t)(uid[i/4U]>>((i%4U)*8U));
  out->reset_csr=csr;
  out->option_control=opt;
  return true;
}
