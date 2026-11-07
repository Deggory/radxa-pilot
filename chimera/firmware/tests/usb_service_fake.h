// SPDX-License-Identifier: MIT
#pragma once
#include <assert.h>
#include <string.h>
#include "usb_service.h"
#include "usb_time.h"

typedef struct { uint32_t address,value; } reg;
typedef struct {
  reg regs[48];unsigned count,reads,writes,uid_reads,failure,resets,rx_flush;
  bool cleanup_stuck,clock_gate_stuck,attach_during_poll,identity_changed_after_snapshot;
  bool clear_session_during_poll,session_write_stuck;
} fake;
static uint32_t *cell(fake *f,uint32_t address) {
  for(unsigned i=0;i<f->count;++i) if(f->regs[i].address==address) return &f->regs[i].value;
  assert(f->count<48);f->regs[f->count]=(reg){address,0};return &f->regs[f->count++].value;
}
static uint32_t rd(void *ctx,uint32_t address) {
  fake *f=ctx;++f->reads;
  if(address>=0x50000000 && address<0x50010000) assert((*cell(f,0x40023834)&128) && !(*cell(f,0x40023814)&128));
  if(address>=0x1FFF7A10 && address<=0x1FFF7A18) {
    ++f->uid_reads;if(f->failure==1) return 0;
    if(f->failure==2 && f->uid_reads==4) return *cell(f,address)^1;
    if(f->identity_changed_after_snapshot && f->uid_reads>6) return *cell(f,address)^1;
  }
  uint32_t *v=cell(f,address);
  if(address==0xE0001004 && f->failure!=5) *v+=16000;
  if(address==0x40023800) {
    if((*v&(1U<<16)) && f->failure!=7) *v|=1U<<17;
    if(*v&(1U<<24)) { if(f->failure!=8) *v|=1U<<25; }
    else if(f->failure!=6) *v&=~(1U<<25);
  }
  if(address==0x50000010) {
    if(f->failure!=12) *v|=1U<<31;
    if(f->failure!=13) *v&=~1U;
    if(f->failure!=16) *v&=~(1U<<5);
    if(f->failure!=17) *v&=~(1U<<4);
  }
  if(address==0x50000014 && f->failure==15) return 1;
  if(address==0x50000014 && f->attach_during_poll) *cell(f,0x50000804)=0;
  if(address==0x50000014 && f->clear_session_during_poll) *cell(f,0x50000000)&=~0xC0U;
  if(address==0x50000800 && f->failure==18 && f->rx_flush==1) return 0;
  return *v;
}
static void wr(void *ctx,uint32_t address,uint32_t value) {
  fake *f=ctx;++f->writes;
  const uint32_t allowed[]={0xE000EDFC,0xE0001000,0x40023800,0x40023804,0x40023814,0x40023834,0x40023894,
    0x50000000,0x50000008,0x5000000C,0x50000010,0x50000014,0x50000018,0x50000024,0x50000028,
    0x50000038,0x50000800,0x50000804,0x50000810,0x50000814,0x5000081C,0x50000834,
    0x50000900,0x50000908,0x50000B00,0x50000B08,0x50000B10,0x50000E00};
  bool known=false;for(unsigned i=0;i<sizeof(allowed)/sizeof(allowed[0]);++i) known|=address==allowed[i];
  assert(known); // No GPIO/CAN/watchdog/flash/config/UID writes.
  if(address>=0x50000000 && address<0x50010000) assert((*cell(f,0x40023834)&128) && !(*cell(f,0x40023814)&128));
  if(address==0x50000000 && f->session_write_stuck) return;
  if(address==0x40023814 && ((f->failure==9 || f->cleanup_stuck) && (value&128))) return;
  if(address==0x40023814 && f->failure==11 && !(value&128)) return;
  if(address==0x40023834 && f->failure==10 && (value&128)) return;
  if(address==0x40023834 && f->clock_gate_stuck && !(value&128)) return;
  if(address==0xE0001000 && f->failure==4) return;
  if(address==0x50000038 && (value&(1U<<16))) assert(*cell(f,0x50000804)&2);
  if(address==0x50000804) assert(value&2); // This increment cannot attach.
  if(address==0x50000014 || address==0x50000908 || address==0x50000B08) *cell(f,address)&=~value;
  else *cell(f,address)=value;
  if(address==0x50000018 && f->failure==19 && value!=0) *cell(f,0x50000804)=0;
  if(address==0x50000010) {
    if(value&1) { ++f->resets;*cell(f,0x50000804)=0;*cell(f,0x50000038)=0; }
    if(value&16) ++f->rx_flush;
  }
}
static bool delay(void *ctx,uint32_t us) {
  fake *f=ctx;if(f->failure==14) return false;
  chimera_usb_io io={ctx,rd,wr,NULL};return chimera_usb_delay16(&io,us);
}
static void base(fake *f,unsigned failure) {
  memset(f,0,sizeof(*f));f->failure=failure;
  *cell(f,0x40023800)=3|(1U<<24)|(1U<<25);
  *cell(f,0x40023814)=0x200;*cell(f,0x40023834)=0x100;
  *cell(f,0x1FFF7A10)=0x0044003a;*cell(f,0x1FFF7A14)=0x30335116;*cell(f,0x1FFF7A18)=0x36363738;
  *cell(f,0x40023874)=0x28000003;*cell(f,0x40023C14)=0x0FFFAAED;
  if(failure==3) *cell(f,0xE0001000)=1U<<25;
}
