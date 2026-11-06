// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "usb_time.h"

typedef struct { uint32_t cr, cfgr, demcr, ctrl, cycles, step, reads, writes; bool reject; } fake;
static uint32_t rd(void *ctx, uint32_t addr) {
  fake *f = ctx; ++f->reads;
  switch (addr) {
    case 0x40023800: return f->cr;
    case 0x40023808: return f->cfgr;
    case 0xE000EDFC: return f->demcr;
    case 0xE0001000: return f->ctrl;
    case 0xE0001004: f->cycles += f->step; return f->cycles;
    default: assert(false); return 0;
  }
}
static void wr(void *ctx, uint32_t addr, uint32_t value) {
  fake *f = ctx; ++f->writes;
  if (f->reject) return;
  if (addr == 0xE000EDFC) f->demcr = value;
  else if (addr == 0xE0001000) f->ctrl = value;
  else assert(false); // Never reset CYCCNT or touch USB/GPIO/CAN.
}
int main(void) {
  fake f = {.cr=3, .step=17, .demcr=0x20, .ctrl=0x100};
  chimera_usb_io io = {.context=&f, .read32=rd, .write32=wr, .delay_us=NULL};
  assert(chimera_usb_time16_init(&io));
  assert(f.demcr == 0x1000020 && f.ctrl == 0x101);
  for (uint32_t us=0; us<=50000; us+=1000) {
    const uint32_t start=f.cycles;
    assert(chimera_usb_delay16(&io, us));
    assert((uint32_t)(f.cycles-start) >= us*16);
  }
  f.cycles=UINT32_MAX-20; assert(chimera_usb_delay16(&io, 20));
  f.step=0; f.reads=0; assert(!chimera_usb_delay16(&io, 1)); assert(f.reads<100);
  f.reads=0; assert(!chimera_usb_time16_init(&io)); assert(f.reads<45);
  f.step=17; f.cfgr=4; f.writes=0;
  assert(!chimera_usb_time16_init(&io) && f.writes==0);
  assert(!chimera_usb_delay16(&io, 1));
  f.cfgr=0; f.ctrl=1U<<25; assert(!chimera_usb_time16_init(&io));
  f.ctrl=0; f.reject=true; assert(!chimera_usb_time16_init(&io));
  f.reject=false; f.ctrl=1; f.demcr=1U<<24;
  assert(!chimera_usb_delay16(&io, 50001));
  f.ctrl=0; assert(!chimera_usb_delay16(&io, 1));
  assert(!chimera_usb_time16_init(NULL) && !chimera_usb_delay16(NULL, 1));
  io.write32=NULL; assert(!chimera_usb_time16_init(&io));
  puts("USB time: 51 delay durations, wrap, stalled/absent counter and clock/ownership guards passed");
}
