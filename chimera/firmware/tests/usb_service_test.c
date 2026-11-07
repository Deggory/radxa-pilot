// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "usb_service.h"
#include "usb_time.h"

#include "usb_service_fake.h"

int main(void) {
  unsigned scenarios=0;
  for(unsigned failure=0;failure<=19;++failure) {
    fake f;base(&f,failure);chimera_usb_io io={&f,rd,wr,delay};
    chimera_usb_service s={0};
    bool ok=chimera_usb_service_start(&s,&io,1,0,8);
    assert(ok==(failure==0));
    if(ok) {
      assert(s.phase==CHIMERA_USB_SERVICE_DETACHED && s.driver.active && s.facts_valid);
      assert(s.driver.io==&s.io && s.facts.reset_csr==0x28000003);
      assert(s.driver.ep0.serial[2]=='3' && s.driver.ep0.serial[4]=='a');
      assert(chimera_usb_service_poll(&s,4)==0);
      unsigned before=f.reads;assert(!chimera_usb_service_start(&s,&io,1,0,8) && f.reads==before);
      assert(chimera_usb_service_poll(&s,0)==-1 && f.reads==before);
      assert(chimera_usb_service_stop(&s) && s.phase==CHIMERA_USB_SERVICE_STOPPED);
      assert((*cell(&f,0x40023814)&128) && !(*cell(&f,0x40023834)&128));
    } else {
      assert(s.phase==CHIMERA_USB_SERVICE_FAILED && s.error!=CHIMERA_USB_SERVICE_OK);
      assert(!s.driver.active);
      enum chimera_usb_service_error expected=failure<=2 ? CHIMERA_USB_SERVICE_FACTS:
        failure<=5 ? CHIMERA_USB_SERVICE_TIMING:failure<=10 ? CHIMERA_USB_SERVICE_CLOCK:
        failure<=17 ? CHIMERA_USB_SERVICE_CORE:failure==18 ? CHIMERA_USB_SERVICE_DRIVER:CHIMERA_USB_SERVICE_INVARIANT;
      assert(s.error==expected && s.cleanup_ok==(failure!=9));
      if(failure<=2) assert(f.writes==0);
      unsigned before=f.reads;assert(chimera_usb_service_poll(&s,1)==-1 && f.reads==before);
      assert(!chimera_usb_service_start(&s,&io,1,0,8) && f.reads==before);
    }
    assert((*cell(&f,0x40023814)&0x200) && (*cell(&f,0x40023834)&0x100));
    assert(f.reads<1500 && f.writes<140);++scenarios;
  }
  // Refuse to touch another USB owner or an incompatible CPU profile.
  for(unsigned bad=0;bad<4;++bad) {
    fake f;base(&f,0);chimera_usb_io io={&f,rd,wr,delay};chimera_usb_service s={0};
    if(bad==0) *cell(&f,0x40023834)|=128;
    if(bad==1) *cell(&f,0x40023808)=8;
    if(bad==2) *cell(&f,0x40023808)=128;
    if(bad==3) *cell(&f,0x40023800)|=1U<<18;
    assert(!chimera_usb_service_start(&s,&io,1,0,8) && f.writes==0 &&
           s.error==CHIMERA_USB_SERVICE_OWNERSHIP && !s.owns_usb);
    unsigned reads=f.reads;assert(chimera_usb_service_stop(&s) && f.reads==reads);++scenarios;
  }
  // Runtime invariant failures and driver errors must latch and quiesce USB.
  for(unsigned fault=0;fault<10;++fault) {
    fake f;base(&f,0);chimera_usb_io io={&f,rd,wr,delay};chimera_usb_service s={0};
    assert(chimera_usb_service_start(&s,&io,1,0,8));
    switch(fault) {
      case 0: *cell(&f,0x50000804)=0;break; // Unexpected attach.
      case 1: *cell(&f,0x50000008)=1;break; // IRQ unexpectedly enabled.
      case 2: *cell(&f,0x50000008)=32;break; // DMA unexpectedly enabled.
      case 3: *cell(&f,0x50000000)=128;break; // Forced session-valid.
      case 4: *cell(&f,0x50000038)=0;break; // PHY unexpectedly off.
      case 5: *cell(&f,0x40023834)&=~128U;break; // Core gated: no USB register access allowed.
      case 6: *cell(&f,0x40023814)|=128;break; // Core held reset.
      case 7: *cell(&f,0x50000014)=1U<<11;break; // Driver suspend failure.
      case 8: *cell(&f,0x40023808)=8;break; // CPU clock profile changed.
      case 9: f.attach_during_poll=true;break; // Post-poll invariant check.
      default:assert(false);
    }
    assert(chimera_usb_service_poll(&s,4)==-1 && s.phase==CHIMERA_USB_SERVICE_FAILED &&
           !s.driver.active && s.cleanup_ok && !s.owns_usb);
    unsigned reads=f.reads;assert(chimera_usb_service_poll(&s,4)==-1 && f.reads==reads);
    assert(chimera_usb_service_stop(&s));++scenarios;
  }
  // Failed cleanup readbacks must not pretend recovery succeeded.
  fake f;base(&f,0);chimera_usb_io io={&f,rd,wr,delay};chimera_usb_service s={0};
  assert(chimera_usb_service_start(&s,&io,1,0,8));
  f.cleanup_stuck=true;f.clock_gate_stuck=true;*cell(&f,0x50000008)=1;
  assert(chimera_usb_service_poll(&s,4)==-1 && !s.cleanup_ok && s.owns_usb);
  assert(!chimera_usb_service_stop(&s) && s.error==CHIMERA_USB_SERVICE_RELEASE);
  f.cleanup_stuck=false;f.clock_gate_stuck=false;
  assert(chimera_usb_service_stop(&s) && s.cleanup_ok && !s.owns_usb);++scenarios;
  // Explicit stop/restart is required, and driver IO points at the owned copy.
  base(&f,0);assert(chimera_usb_service_start(&s,&io,0,50,8));
  io.read32=NULL;assert(chimera_usb_service_poll(&s,4)==0);
  assert(chimera_usb_service_stop(&s));unsigned reads=f.reads;
  assert(chimera_usb_service_stop(&s) && f.reads==reads);io.read32=rd;
  assert(chimera_usb_service_start(&s,&io,0,50,8) && s.driver.io==&s.io);
  *cell(&f,0x50000014)=1U<<12;assert(chimera_usb_service_poll(&s,1)==2);
  assert(chimera_usb_service_stop(&s));++scenarios;
  for(unsigned bad=0;bad<8;++bad) {
    base(&f,0);chimera_usb_service fresh={0};chimera_usb_io invalid=io;
    if(bad==0) invalid.read32=NULL;
    if(bad==1) invalid.write32=NULL;
    if(bad==2) invalid.delay_us=NULL;
    assert(!chimera_usb_service_start(&fresh,bad==3 ? NULL:&invalid,bad==4 ? 2:1,bad==5 ? 251:0,
                                     bad==6 ? 0:bad==7 ? 1000001U:8));
    assert(f.reads==0 && f.writes==0 && fresh.error==CHIMERA_USB_SERVICE_ARGUMENT);++scenarios;
  }
  assert(!chimera_usb_service_start(NULL,&io,1,0,8) && !chimera_usb_service_stop(NULL));
  assert(chimera_usb_service_poll(NULL,1)==-1);
  printf("USB service: %u real-component startup scenarios passed; attachment disabled\n",scenarios);
}
