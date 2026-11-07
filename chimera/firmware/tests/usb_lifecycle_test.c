// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "main.h"
#include "usb_service_fake.h"

#define EN (1U<<31)
#define GINT 0x50000014U
#define OTG 0x50000004U
#define DCTL 0x50000804U
#define DSTS 0x50000808U
#define SUSPEND (1U<<11)
#define WAKE (1U<<31)
static const chimera_main_usb_config CONFIG = {1, 0, 8, 8, CHIMERA_USB_SESSION_LEGACY_NO_VBUS};
typedef struct {
  fake f; uint8_t setup[8]; bool queued; unsigned word,tx_count,power_samples;
  uint32_t tx[16],power_drop_at;
  unsigned inject_on_attach,inject_during_delay;
  uint32_t late_otg,first_otg_ack;
  unsigned otg_acks;
} fixture;
static uint32_t read_life(void *ctx,uint32_t addr) {
  fixture *l=ctx; fake *f=&l->f;
  uint32_t value=rd(f,addr); // Keep shared clock/access assertions for every read.
  if(addr==OTG && l->late_otg) { *cell(f,OTG)|=l->late_otg; l->late_otg=0; }
  if(addr==GINT) return value | (l->queued ? 16U:0U) |
    ((*cell(f,0x50000908)&*cell(f,0x50000810)) ? 1U<<18:0U) |
    ((*cell(f,0x50000B08)&*cell(f,0x50000814)) ? 1U<<19:0U);
  if(addr==0x50000818) return (*cell(f,0x50000908)&*cell(f,0x50000810) ? 1U:0U) |
    (*cell(f,0x50000B08)&*cell(f,0x50000814) ? 1U<<16:0U);
  if(addr==0x50000020) {
    assert(l->queued); l->queued=false; l->word=0;
    *cell(f,0x50000B08)|=8; *cell(f,0x50000B00)&=~EN;
    return (6U<<17)|(8U<<4);
  }
  if(addr==0x50001000) {
    assert(l->word<2); uint32_t word=0;
    for(unsigned i=0;i<4;++i) word|=(uint32_t)l->setup[l->word*4+i]<<(i*8);
    ++l->word; return word;
  }
  return value;
}
static void write_life(void *ctx,uint32_t addr,uint32_t value) {
  fixture *l=ctx; fake *f=&l->f;
  if(addr==OTG) { if(!l->otg_acks) l->first_otg_ack=value; ++l->otg_acks; }
  if(addr==0x50001000) {
    // FIFO is the only extra write beyond the shared strict whitelist.
    assert((*cell(f,0x40023834)&128) && !(*cell(f,0x40023814)&128));
    assert(l->tx_count<16); l->tx[l->tx_count++]=value; ++f->writes; return;
  }
  if(addr==0x50000900 && (value&(1U<<30))) {
    value&=~(EN|(1U<<30)); *cell(f,0x50000908)|=2;
  }
  if(addr==0x50000010 && (value&16)) l->queued=false;
  wr(f,addr,value);
  if(addr==DCTL && !(value&2) && l->inject_on_attach) *cell(f,0x50000008)=32;
}
static bool delay_life(void *ctx,uint32_t us) {
  fixture *l=ctx;
  bool ok=delay(&l->f,us);
  if(us==10000 && l->inject_during_delay) *cell(&l->f,0x50000E00)=1;
  return ok;
}
static enum chimera_vbus_state power(void *ctx) {
  fixture *l=ctx; ++l->power_samples;
  return l->power_samples==l->power_drop_at ? CHIMERA_VBUS_ABSENT:CHIMERA_VBUS_PRESENT;
}
static void init(fixture *l,chimera_main_runtime *r,chimera_boot_details *facts,
                 enum chimera_usb_session_mode mode) {
  memset(l,0,sizeof(*l)); base(&l->f,0); l->f.allow_attach=true;
  *cell(&l->f,0x50000918)=64; *cell(&l->f,DSTS)=6;
  memset(r,0,sizeof(*r)); memset(facts,0,sizeof(*facts));
  chimera_usb_io io={l,read_life,write_life,delay_life};
  chimera_main_usb_config config=CONFIG; config.session_mode=mode;
  assert(chimera_main_start(r,facts,&io,true,&config));
}
static int pump(chimera_main_runtime *r,fixture *l) {
  chimera_vbus_io v={l,power};
  return chimera_main_poll(r,r->config.session_mode==CHIMERA_USB_SESSION_LEGACY_NO_VBUS ? NULL:&v);
}
static void setup(fixture *l,chimera_main_runtime *r,unsigned type,unsigned request,unsigned value,unsigned length) {
  l->setup[0]=type; l->setup[1]=request; l->setup[2]=value; l->setup[3]=value>>8;
  l->setup[4]=0; l->setup[5]=0; l->setup[6]=length; l->setup[7]=length>>8;
  l->queued=true; l->tx_count=0; assert(pump(r,l)>=0);
}
static void complete_in(fixture *l,chimera_main_runtime *r) {
  *cell(&l->f,0x50000900)&=~EN; *cell(&l->f,0x50000910)=0;
  *cell(&l->f,0x50000908)|=1; assert(pump(r,l)>=0);
}
static void host_reset(fixture *l,chimera_main_runtime *r,uint32_t coalesced) {
  *cell(&l->f,0x50000900)&=~EN; *cell(&l->f,0x50000B00)&=~EN;
  *cell(&l->f,GINT)=(1U<<12)|coalesced; assert(pump(r,l)>=0);
  assert(!r->usb.driver.ep0.address && !r->usb.driver.ep0.configuration && !r->usb.driver.suspended);
}
static void attach(fixture *l,chimera_main_runtime *r) {
  chimera_vbus_io v={l,power};
  assert(chimera_main_attach(r,r->config.session_mode==CHIMERA_USB_SESSION_LEGACY_NO_VBUS ? NULL:&v));
  assert(r->state==CHIMERA_BOOT_USB_ATTACHED && !(*cell(&l->f,DCTL)&2));
}
static void quiet(fixture *l,chimera_main_runtime *r,chimera_boot_details *facts) {
  assert(chimera_main_stop(r));
  assert(!facts->facts_valid && !r->usb.owns_usb && !r->usb.driver.active &&
         !r->usb.driver.attached && !r->usb.driver.suspended);
  // A previously gated core is inaccessible; quiet is proved by reset + gate,
  // not by reading stale USB cells that cleanup correctly refused to access.
  assert((*cell(&l->f,0x40023814)&128) && !(*cell(&l->f,0x40023834)&128));
}
int main(void) {
  unsigned scenarios=0;
  fixture l; chimera_main_runtime r; chimera_boot_details facts;
  for(unsigned mode=0;mode<2;++mode) {
    init(&l,&r,&facts,(enum chimera_usb_session_mode)mode); attach(&l,&r);
    assert(l.f.attaches==1 && l.f.attach_delays==1);
    assert(r.vbus==(mode ? CHIMERA_VBUS_UNKNOWN:CHIMERA_VBUS_PRESENT));
    host_reset(&l,&r,0);
    *cell(&l.f,GINT)=1U<<13; assert(pump(&r,&l)>=0);
    setup(&l,&r,0x80,6,0x100,18); assert(l.tx_count==5 && l.tx[0]==0x02000112);
    host_reset(&l,&r,0); // Cancels descriptor status and starts fresh enumeration.
    setup(&l,&r,0,5,23,0); complete_in(&l,&r); assert(r.usb.driver.ep0.address==23);
    setup(&l,&r,0,9,1,0); complete_in(&l,&r); assert(r.usb.driver.ep0.configuration==1);
    setup(&l,&r,0xC0,0xA0,0,32); assert(l.tx_count==8 && l.tx[0]==0x524D4843);
    uint32_t generation=r.usb.driver.ep0.generation;
    *cell(&l.f,DSTS)=7; *cell(&l.f,GINT)=SUSPEND;
    assert(pump(&r,&l)>=0 && r.state==CHIMERA_BOOT_USB_SUSPENDED);
    assert(r.usb.driver.ep0.address==23 && r.usb.driver.ep0.configuration==1 &&
           r.usb.driver.ep0.generation==generation && r.usb.driver.in_armed);
    // No endpoint completion is processed during suspend, including coalesced XFRC.
    *cell(&l.f,0x50000900)&=~EN; *cell(&l.f,0x50000910)=0; *cell(&l.f,0x50000908)|=1;
    assert(pump(&r,&l)==0 && r.usb.driver.in_armed);
    *cell(&l.f,DSTS)=6; *cell(&l.f,GINT)=WAKE;
    assert(pump(&r,&l)>=0 && r.state==CHIMERA_BOOT_USB_ATTACHED && !r.usb.driver.in_armed);
    assert(r.usb.driver.ep0.generation==generation && r.usb.driver.ep0.configuration==1);
    // Reset while suspended cancels the old address/configuration and all work.
    *cell(&l.f,DSTS)=7; *cell(&l.f,GINT)=SUSPEND; assert(pump(&r,&l)>=0);
    host_reset(&l,&r,SUSPEND|WAKE);
    assert(!chimera_usb_ep0_in_complete(&r.usb.driver.ep0,generation));
    // Current DSTS resolves coalesced or stale suspend/wake events.
    for(unsigned suspended=0;suspended<2;++suspended) {
      *cell(&l.f,DSTS)=6|suspended; *cell(&l.f,GINT)=SUSPEND|WAKE;
      assert(pump(&r,&l)>=0 && r.usb.driver.suspended==suspended); ++scenarios;
    }
    *cell(&l.f,DSTS)=6; *cell(&l.f,GINT)=WAKE; assert(pump(&r,&l)>=0);
    // Benign OTG changes acknowledged exactly; SEDET dominates reset/completion.
    *cell(&l.f,OTG)=(1U<<18)|(1U<<19); assert(pump(&r,&l)>=0 && !*cell(&l.f,OTG));
    setup(&l,&r,0,5,7,0); generation=r.usb.driver.ep0.generation;
    *cell(&l.f,0x50000900)&=~EN; *cell(&l.f,0x50000910)=0; *cell(&l.f,0x50000908)|=1;
    *cell(&l.f,OTG)=4; *cell(&l.f,GINT)|=1U<<12;
    assert(pump(&r,&l)==3 && r.state==CHIMERA_BOOT_USB_STOPPED && !facts.facts_valid);
    assert(!r.usb.driver.ep0.address && !r.usb.driver.active && !r.usb.owns_usb);
    assert(!chimera_usb_ep0_in_complete(&r.usb.driver.ep0,generation));
    // No implicit restart; explicit start must provide the full profile again.
    unsigned reads=l.f.reads,writes=l.f.writes;
    assert(pump(&r,&l)==-1 && !chimera_main_attach(&r,NULL));
    assert(l.f.reads==reads && l.f.writes==writes);
    chimera_usb_io io={&l,read_life,write_life,delay_life};
    chimera_main_usb_config config=CONFIG; config.session_mode=(enum chimera_usb_session_mode)mode;
    for(unsigned cycle=0;cycle<20;++cycle) {
      assert(chimera_main_start(&r,&facts,&io,true,&config)); attach(&l,&r);
      host_reset(&l,&r,0); quiet(&l,&r,&facts); ++scenarios;
    }
    scenarios+=8;
  }
  // Failed delay, SDIS write/readback, pre/post attachment invariants and refusal
  // of a synthetic pre-attach transfer must all release and revoke facts.
  for(unsigned fault=0;fault<11;++fault) {
    init(&l,&r,&facts,CHIMERA_USB_SESSION_LEGACY_NO_VBUS);
    switch(fault) {
      case 0:l.f.attach_delay_stuck=true;break;
      case 1:l.f.attach_write_stuck=true;break;
      case 2:l.f.gate_on_attach=true;break;
      case 3:*cell(&l.f,0x50000E00)=1;break;
      case 4:l.inject_during_delay=1;break;
      case 5:l.inject_on_attach=1;break;
      case 6:r.usb.driver.ep0.address=17;break;
      case 7:r.usb.driver.ep0.phase=CHIMERA_EP0_STATUS_IN;break;
      case 8:*cell(&l.f,OTG)=1U<<9;break;
      case 9:*cell(&l.f,OTG)=1U<<1;break;
      case 10:l.f.clear_session_during_poll=true;break;
      default:assert(false);
    }
    assert(!chimera_main_attach(&r,NULL) && r.state==CHIMERA_BOOT_USB_FAILED && !facts.facts_valid);
    assert(!r.usb.owns_usb && !r.usb.driver.active && (*cell(&l.f,DCTL)&2));
    if(fault==10) assert(!l.f.attaches); // Post-drain validation precedes SDIS clear.
    unsigned reads=l.f.reads,writes=l.f.writes;
    assert(pump(&r,&l)==-1 && !chimera_main_attach(&r,NULL));
    assert(l.f.reads==reads && l.f.writes==writes); quiet(&l,&r,&facts); ++scenarios;
  }
  // Fresh power required on both sides of attachment in sensed mode.
  for(unsigned drop=1;drop<=2;++drop) {
    init(&l,&r,&facts,CHIMERA_USB_SESSION_UNFORCED); l.power_drop_at=drop;
    chimera_vbus_io v={&l,power};
    assert(!chimera_main_attach(&r,&v) && r.error==CHIMERA_MAIN_USB_POWER && !facts.facts_valid);
    assert(l.f.attaches==(drop==2)); quiet(&l,&r,&facts); ++scenarios;
  }
  init(&l,&r,&facts,CHIMERA_USB_SESSION_LEGACY_NO_VBUS);
  chimera_vbus_io v={&l,power}; assert(!chimera_main_attach(&r,&v) && !l.power_samples && !l.f.attaches);
  quiet(&l,&r,&facts); ++scenarios;
  // A session end arriving after the first GOTGINT snapshot must survive its
  // acknowledgment and dominate an already completed SET_ADDRESS on next poll.
  init(&l,&r,&facts,CHIMERA_USB_SESSION_LEGACY_NO_VBUS); attach(&l,&r);
  setup(&l,&r,0,5,7,0);
  *cell(&l.f,0x50000900)&=~EN; *cell(&l.f,0x50000910)=0; *cell(&l.f,0x50000908)|=1;
  *cell(&l.f,OTG)=1U<<18; l.late_otg=4;
  assert(pump(&r,&l)==3 && l.first_otg_ack==(1U<<18) && l.otg_acks==2);
  assert(!r.usb.driver.ep0.address && !facts.facts_valid); quiet(&l,&r,&facts); ++scenarios;
  // Session-end cleanup failure remains owned/error-latched until explicit retry.
  init(&l,&r,&facts,CHIMERA_USB_SESSION_LEGACY_NO_VBUS); attach(&l,&r);
  l.f.cleanup_stuck=true; l.f.clock_gate_stuck=true; *cell(&l.f,OTG)=4;
  assert(pump(&r,&l)==-1 && r.state==CHIMERA_BOOT_USB_FAILED && r.usb.owns_usb && !facts.facts_valid);
  assert(!chimera_main_stop(&r)); l.f.cleanup_stuck=false; l.f.clock_gate_stuck=false;
  quiet(&l,&r,&facts); ++scenarios;
  // Every running invariant is checked while attached and while suspended.
  for(unsigned suspended=0;suspended<2;++suspended) for(unsigned fault=0;fault<8;++fault) {
    init(&l,&r,&facts,CHIMERA_USB_SESSION_LEGACY_NO_VBUS); attach(&l,&r);
    if(suspended) { *cell(&l.f,DSTS)=7; *cell(&l.f,GINT)=SUSPEND; assert(pump(&r,&l)>=0); }
    switch(fault) {
      case 0:*cell(&l.f,DCTL)|=2;break;
      case 1:*cell(&l.f,0x50000008)=32;break;
      case 2:*cell(&l.f,0x50000E00)=2;break;
      case 3:*cell(&l.f,0x50000038)|=1U<<21;break;
      case 4:*cell(&l.f,0x50000000)=0;break;
      case 5:*cell(&l.f,0x40023834)&=~128U;break;
      case 6:*cell(&l.f,OTG)=1U<<20;break;
      case 7:*cell(&l.f,GINT)=1U<<28;break;
      default:assert(false);
    }
    assert(pump(&r,&l)==-1 && !facts.facts_valid && !r.usb.driver.active);
    quiet(&l,&r,&facts); ++scenarios;
  }
  printf("USB lifecycle: %u composed scenarios including enumeration, suspend/resume, reset cancellation, session end, 40 reconnect cycles and fault cleanup passed\n",scenarios);
}
