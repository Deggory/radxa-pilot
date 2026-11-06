// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "usb_driver.h"

#define EN (1U<<31)
typedef struct { uint32_t status; uint8_t bytes[64]; } packet;
typedef struct {
  uint32_t r[0x1004/4], gint, writes, reads, fifo_reads, tx[16], tx_count;
  packet q[8]; unsigned head, tail, word; bool stuck, disable_stuck, clock_off, reset_held;
} fake;
static uint32_t rd(void *ctx, uint32_t addr) {
  fake *f=ctx; ++f->reads;
  if(addr==0x40023834) return f->clock_off ? 0:128;
  if(addr==0x40023814) return f->reset_held ? 128:0;
  assert(addr>=0x50000000 && addr<=0x50001000 && addr%4==0);
  unsigned off=addr-0x50000000;
  if(off==0x14) return f->gint | (f->head<f->tail ? 16U:0U) |
    (f->r[0x908/4]&f->r[0x810/4] ? 1U<<18:0U) | (f->r[0xB08/4]&f->r[0x814/4] ? 1U<<19:0U);
  if(off==0x818) return (f->r[0x908/4]&f->r[0x810/4] ? 1U:0U) |
    (f->r[0xB08/4]&f->r[0x814/4] ? 1U<<16:0U);
  if(off==0x20) {
    assert(f->head<f->tail); f->word=0;
    uint32_t status=f->q[f->head++].status;
    if(((status>>17)&15)==6) {
      f->r[0xB08/4]|=8; f->r[0xB00/4]&=~EN;
    }
    return status;
  }
  if(off==0x1000) {
    assert(f->head && f->word<16); ++f->fifo_reads;
    const packet *p=&f->q[f->head-1]; uint32_t v=0;
    for(unsigned i=0;i<4;++i) v|=(uint32_t)p->bytes[f->word*4+i]<<(8*i);
    ++f->word; return v;
  }
  return f->r[off/4];
}
static void wr(void *ctx, uint32_t addr, uint32_t value) {
  fake *f=ctx; ++f->writes;
  assert(addr>=0x50000000 && addr<=0x50001000 && addr%4==0);
  unsigned off=addr-0x50000000;
  switch(off) {
    case 0x14: assert((value&~((1U<<12)|(1U<<13)))==0); f->gint &= ~value; return;
    case 0x908: case 0xB08: f->r[off/4]&=~value; return;
    case 0x10:
      f->r[off/4]=(1U<<31) | (f->stuck ? value:0U);
      if((value&16) && !f->stuck) f->head=f->tail;
      return;
    case 0x1000: assert(f->tx_count<16); f->tx[f->tx_count++]=value; return;
    case 0x900:
      if((value&(1U<<30)) && !f->disable_stuck) { value&=~(EN|(1U<<30)); f->r[0x908/4]|=2; }
      break;
    case 0x804: assert(value&2); break; // Driver never attaches.
    case 0x8: assert(value==0); break;
    case 0x18: case 0x38: case 0x800: case 0x810: case 0x814: case 0x81C:
    case 0x834: case 0x910: case 0xB00: case 0xB10: break;
    default: assert(false); // No nonzero endpoints or unrelated peripherals.
  }
  f->r[off/4]=value;
}
static bool delay(void *ctx,uint32_t us) { (void)ctx;(void)us;assert(false);return false; }
static void base(fake *f) {
  memset(f,0,sizeof(*f)); f->r[0x804/4]=2; f->r[0x800/4]=3;
  f->r[0xC/4]=(1U<<30)|(1U<<6)|(13U<<10); f->r[0x38/4]=1U<<16;
  f->r[0x10/4]=1U<<31; f->r[0x918/4]=64; f->r[0x808/4]=6;
}
static void queue(fake *f,unsigned kind,const uint8_t *data,unsigned length,unsigned ep) {
  assert(f->tail<8 && length<=64);
  packet *p=&f->q[f->tail++]; p->status=(kind<<17)|(length<<4)|ep;
  if(data) memcpy(p->bytes,data,length);
}
static void pump(chimera_usb_driver *d) { assert(chimera_usb_driver_poll(d,32)>=0); }
static void setup(fake *f,chimera_usb_driver *d,unsigned type,unsigned req,unsigned value,unsigned index,unsigned len) {
  f->head=f->tail=0; f->tx_count=0;
  uint8_t b[]={type,req,value,value>>8,index,index>>8,len,len>>8};
  queue(f,6,b,8,0);pump(d);
}
static void in_done(fake *f,chimera_usb_driver *d) {
  f->r[0x900/4]&=~EN; f->r[0x910/4]=0; f->r[0x908/4]|=1; pump(d);
}
static void status_out(fake *f,chimera_usb_driver *d) {
  f->head=f->tail=0;queue(f,2,NULL,0,0);pump(d);
  f->r[0xB00/4]&=~EN;f->r[0xB08/4]|=1;pump(d);
}
int main(void) {
  fake f; base(&f); chimera_usb_driver d;
  const uint8_t uid[]={1,2,3,4,5,6,7,8,9,10,11,12};
  chimera_usb_io io={.context=&f,.read32=rd,.write32=wr,.delay_us=delay};
  assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
  assert(d.active && d.ep0.address==0 && f.r[0xB10/4]==((3U<<29)|(1U<<19)|24));
  f.gint=1U<<13;pump(&d);assert(f.gint==0);
  setup(&f,&d,0x80,6,0x100,0,64);
  assert(f.tx_count==5 && (f.r[0x910/4]&127)==18 && f.tx[0]==0x02000112);
  assert((f.tx[4]&0xFFFF0000)==0); // Tail word zero padded, no source overread.
  in_done(&f,&d);assert(d.ep0.phase==CHIMERA_EP0_STATUS_OUT);
  status_out(&f,&d);assert(d.ep0.phase==CHIMERA_EP0_IDLE);
  setup(&f,&d,0,5,23,0,0);assert(d.ep0.address==0 && f.tx_count==0);
  in_done(&f,&d);assert(d.ep0.address==23 && (f.r[0x800/4]&(127U<<4))==23U<<4);
  setup(&f,&d,0,9,1,0,0);assert(d.ep0.configuration==0);
  in_done(&f,&d);assert(d.ep0.configuration==1);
  setup(&f,&d,0xC0,0xA0,0,0,32);assert(f.tx_count==8 && f.tx[0]==0x524D4843);
  in_done(&f,&d);status_out(&f,&d);
  setup(&f,&d,0x40,0xDC,17,0,0);assert(d.ep0.phase==CHIMERA_EP0_STALL && f.tx_count==0);
  setup(&f,&d,0x80,8,0,0,1);assert(d.ep0.phase==CHIMERA_EP0_DATA_IN && (f.tx[0]&255)==1);
  in_done(&f,&d);status_out(&f,&d);
  // Replacement SETUP must stop/flush an active IN and discard its completions.
  setup(&f,&d,0x80,6,0x100,0,18);uint32_t old=d.ep0.generation;
  setup(&f,&d,0x80,6,0x300,0,4);assert(d.ep0.generation!=old && f.tx_count==1 && f.tx[0]==0x04090304);
  assert(!chimera_usb_ep0_in_complete(&d.ep0,old));
  in_done(&f,&d);status_out(&f,&d);
  f.gint=1U<<12;pump(&d);assert(d.ep0.address==0 && d.ep0.configuration==0);
  // Malformed endpoint and excessive status count disconnect without FIFO reads.
  const unsigned before=f.fifo_reads;f.head=f.tail=0;queue(&f,6,uid,8,1);
  assert(chimera_usb_driver_poll(&d,1)==-1 && !d.active && f.fifo_reads==before);
  unsigned headers=0;
  for(unsigned ep=0;ep<16;++ep) for(unsigned kind=0;kind<16;++kind) for(unsigned size=0;size<128;++size) {
    base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
    f.q[0].status=(kind<<17)|(size<<4)|ep;f.tail=1;
    bool valid=ep==0 && ((kind==6 && size==8) || (kind==2 && size<=64) ||
                        ((kind==1 || kind==3 || kind==4) && size==0));
    int result=chimera_usb_driver_poll(&d,1);
    assert((result>=0)==valid && d.active==valid);
    if(!valid) assert(f.fifo_reads==0);
    assert(f.reads<200 && f.writes<60);++headers;
  }
  // Descriptor lengths include zero, truncated replies and non-word tails.
  const unsigned values[]={0x100,0x200,0x300,0x301,0x302,0x303};unsigned descriptors=0;
  for(unsigned which=0;which<6;++which) for(unsigned len=0;len<=64;++len) {
    base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));d.ep0.address=23;d.ep0.configuration=1;
    setup(&f,&d,0x80,6,values[which],which>=3 ? 0x409:0,len);
    assert(d.reply_size>=0 && f.tx_count==((unsigned)d.reply_size+3)/4);
    for(unsigned i=0;i<f.tx_count*4;++i)
      assert(((f.tx[i/4]>>((i%4)*8))&255)==(i<(unsigned)d.reply_size ? d.reply[i]:0));
    in_done(&f,&d);if(len) status_out(&f,&d);
    assert(d.ep0.phase==CHIMERA_EP0_IDLE);++descriptors;
  }
  unsigned faults=0;
  for(unsigned fault=0;fault<14;++fault) {
    base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
    switch(fault) {
      case 0: f.gint=1;break;
      case 1: f.gint=1U<<11;break;
      case 2: f.gint=1U<<13;f.r[0x808/4]=0;break;
      case 3: f.r[0x908/4]=8;break;
      case 4: f.gint=1U<<12;f.stuck=true;break;
      case 5: f.gint=1U<<12;f.r[0x10/4]=0;break;
      case 6: f.gint=1U<<12;f.r[0xB00/4]=EN;break;
      case 7: f.clock_off=true;break;
      case 8: f.reset_held=true;break;
      case 9: f.q[0].status=(6U<<17)|(2047U<<4);f.tail=1;break;
      case 10: f.r[0xB08/4]=8;break; // STUP without a received SETUP.
      case 11:
        setup(&f,&d,0x80,6,0x100,0,18);f.disable_stuck=true;
        f.head=f.tail=0;queue(&f,6,uid,8,0);break;
      case 12:
        setup(&f,&d,0x80,6,0x100,0,18);f.r[0x908/4]=1;break; // False XFRC before transfer end.
      case 13: f.r[0x908/4]=1U<<8;break; // A standalone FIFO underrun must be observed.
      default:assert(false);
    }
    unsigned writes=f.writes;
    assert(chimera_usb_driver_poll(&d,32)==-1 && !d.active);
    if(fault==7 || fault==8) assert(f.writes==writes);
    else assert(f.r[0x804/4]&2);
    writes=f.writes;assert(chimera_usb_driver_poll(&d,1)==-1 && f.writes==writes);
    assert(f.reads<400);++faults;
  }
  base(&f);f.r[0x918/4]=4;assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
  uint8_t descriptor[]={0x80,6,0,1,0,0,18,0};queue(&f,6,descriptor,8,0);
  assert(chimera_usb_driver_poll(&d,32)==-1 && !d.active);++faults;
  // A status completion already observed before a queued new SETUP must commit.
  base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));d.ep0.address=23;
  setup(&f,&d,0,9,1,0,0);f.r[0x900/4]&=~EN;f.r[0x910/4]=0;f.r[0x908/4]|=1;
  setup(&f,&d,0xC0,0xA0,0,0,32);assert(d.ep0.configuration==1 && f.tx[0]==0x524D4843);
  // Back-to-back received SETUPs retain only the last request, then one STUP.
  base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
  queue(&f,6,descriptor,8,0);uint8_t lang[]={0x80,6,0,3,0,0,4,0};queue(&f,6,lang,8,0);
  pump(&d);assert(f.tx_count==1 && f.tx[0]==0x04090304);
  in_done(&f,&d);status_out(&f,&d);
  // A canceled SET_ADDRESS must never publish its address.
  setup(&f,&d,0,5,7,0,0);setup(&f,&d,0x80,6,0x100,0,18);
  in_done(&f,&d);status_out(&f,&d);assert(d.ep0.address==0);
  // Malformed OUT status is drained and stalled, next SETUP recovers.
  setup(&f,&d,0x80,6,0x100,0,18);in_done(&f,&d);
  f.head=f.tail=0;queue(&f,2,uid,1,0);pump(&d);assert(d.ep0.phase==CHIMERA_EP0_STALL);
  setup(&f,&d,0x80,6,0x300,0,4);in_done(&f,&d);status_out(&f,&d);
  unsigned reads=f.reads;assert(chimera_usb_driver_poll(&d,0)==-1 && f.reads==reads);
  assert(chimera_usb_driver_poll(&d,33)==-1 && f.reads==reads);
  assert(chimera_usb_driver_poll(NULL,1)==-1 && !chimera_usb_driver_init(NULL,&io,uid,1,0,8));
  for(unsigned fault=0;fault<6;++fault) {
    base(&f);
    if(fault==0) f.r[0x804/4]=0;
    if(fault==1) f.r[8/4]=32;
    if(fault==2) f.r[0x800/4]=0;
    if(fault==3) f.r[0xC/4]=0;
    if(fault==4) f.r[0x38/4]=0;
    if(fault==5) f.clock_off=true;
    assert(!chimera_usb_driver_init(&d,&io,uid,1,0,8) && f.writes==0);
  }
  base(&f);assert(!chimera_usb_driver_init(&d,&io,uid,1,0,0) && f.writes==0);
  assert(!chimera_usb_driver_init(&d,&io,uid,2,0,8) && f.writes==0);
  assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
  for(unsigned i=0;i<8;++i) queue(&f,1,NULL,0,0);
  assert(chimera_usb_driver_poll(&d,1)==2 && f.head==1);
  pump(&d);assert(f.head==8);
  for(unsigned phase=0;phase<3;++phase) {
    base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
    if(phase==0) setup(&f,&d,0,5,7,0,0);
    else {
      setup(&f,&d,0x80,6,0x100,0,18);
      if(phase==2) in_done(&f,&d);
    }
    uint32_t canceled=d.ep0.generation;
    f.head=f.tail=0;queue(&f,6,descriptor,8,0);
    // The hardware USB reset clears active endpoints before reporting USBRST.
    f.r[0x900/4]&=~EN;f.r[0xB00/4]&=~EN;f.gint=1U<<12;pump(&d);
    assert(f.head==f.tail && d.ep0.address==0 && d.ep0.configuration==0 &&
           d.ep0.phase==CHIMERA_EP0_IDLE && !d.in_armed && !d.out_armed);
    assert(!chimera_usb_ep0_in_complete(&d.ep0,canceled));
  }
  base(&f);assert(chimera_usb_driver_init(&d,&io,uid,1,0,8));
  d.ep0.generation=UINT32_MAX;f.head=f.tail=0;queue(&f,6,descriptor,8,0);
  assert(chimera_usb_driver_poll(&d,32)==-1 && !d.active);
  printf("USB packet matrix: %u RX headers, %u descriptor-length transfers, %u controller faults passed\n",headers,descriptors,faults);
  puts("USB packet driver: reset/enumeration, descriptors, address/config, vendor query, STALL recovery and SETUP cancellation passed");
}
