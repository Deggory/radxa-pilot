// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "boot_facts.h"
#include "usb_ep0.h"

typedef struct { uint32_t uid[3], csr, opt, reads, uid_reads; int unstable; } fake;
static uint32_t rd(void *ctx,uint32_t addr) {
  fake *f=ctx;++f->reads;
  assert(f->reads<=8);
  if(addr>=0x1FFF7A10 && addr<=0x1FFF7A18 && addr%4==0) {
    unsigned index=(addr-0x1FFF7A10)/4;++f->uid_reads;
    return f->uid[index] ^ ((f->uid_reads>3 && f->unstable==(int)index) ? 1U:0U);
  }
  if(addr==0x40023874) return f->csr;
  if(addr==0x40023C14) return f->opt;
  assert(false);return 0;
}
static void wr(void *ctx,uint32_t addr,uint32_t value) { (void)ctx;(void)addr;(void)value;assert(false); }
int main(void) {
  fake f={.uid={0x0044003a,0x30335116,0x36363738},.csr=0xA8000003,.opt=0x0FFFAAED,.unstable=-1};
  chimera_usb_io io={.context=&f,.read32=rd,.write32=wr,.delay_us=NULL};
  struct { uint32_t before; chimera_boot_facts facts; uint32_t after; } output;
  memset(&output,0xA5,sizeof(output));
  assert(chimera_boot_read_facts(&io,&output.facts) && f.reads==8);
  assert(output.before==0xA5A5A5A5 && output.after==0xA5A5A5A5);
  assert(output.facts.reset_csr==f.csr && output.facts.option_control==f.opt);
  chimera_usb_ep0 ep0;
  assert(chimera_usb_ep0_init(&ep0,output.facts.uid,1,0));
  const char *serial="3a0044001651333038373636";
  for(unsigned i=0;i<24;++i) assert(ep0.serial[2+i*2]==(uint8_t)serial[i] && ep0.serial[3+i*2]==0);
  const chimera_boot_facts saved=output.facts;
  for(int word=0;word<3;++word) {
    f.reads=0;f.uid_reads=0;f.unstable=word;
    assert(!chimera_boot_read_facts(&io,&output.facts));
    assert(memcmp(&saved,&output.facts,sizeof(saved))==0);
  }
  f.unstable=-1;
  for(unsigned invalid=0;invalid<2;++invalid) {
    for(unsigned i=0;i<3;++i) f.uid[i]=invalid ? UINT32_MAX:0;
    f.reads=0;f.uid_reads=0;assert(!chimera_boot_read_facts(&io,&output.facts));
    assert(memcmp(&saved,&output.facts,sizeof(saved))==0);
  }
  for(unsigned i=0;i<65536;++i) {
    f.uid[0]=0x0044003aU^i;f.uid[1]=0x30335116U^(i<<16);f.uid[2]=0x36363738U;
    f.csr=(i<<16)|i;f.opt=~f.csr;f.reads=0;f.uid_reads=0;
    io.write32=NULL;assert(chimera_boot_read_facts(&io,&output.facts) && f.reads==8);
    assert(output.facts.reset_csr==f.csr && output.facts.option_control==f.opt);
    for(unsigned j=0;j<12;++j) assert(output.facts.uid[j]==(uint8_t)(f.uid[j/4]>>((j%4)*8)));
  }
  assert(!chimera_boot_read_facts(NULL,&output.facts));
  assert(!chimera_boot_read_facts(&io,NULL));
  io.read32=NULL;assert(!chimera_boot_read_facts(&io,&output.facts));
  puts("Boot facts: 65536 read-only snapshots, three UID instability faults, blank IDs, serial order and canaries passed; no writes");
}
