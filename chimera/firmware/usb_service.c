// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "usb_service.h"
#include "usb_time.h"

#define AHB2RSTR 0x40023814U
#define AHB2ENR 0x40023834U
#define USB_RESET 128U
#define DCTL 0x50000804U
#define GAHBCFG 0x50000008U
#define GINTMSK 0x50000018U
#define GCCFG 0x50000038U

static uint32_t rd(const chimera_usb_service *s,uint32_t addr) { return s->io.read32(s->io.context,addr); }
static void wr(const chimera_usb_service *s,uint32_t addr,uint32_t value) { s->io.write32(s->io.context,addr,value); }
static bool clocked(const chimera_usb_service *s) {
  return (rd(s,AHB2ENR)&USB_RESET)!=0U && (rd(s,AHB2RSTR)&USB_RESET)==0U;
}
static void invalidate(chimera_usb_service *s) {
  s->driver.active=0; s->driver.in_armed=0; s->driver.out_armed=0; s->driver.setup_wait=0;
  if(s->driver.ep0.initialized==1U) chimera_usb_ep0_reset(&s->driver.ep0);
}
static bool release(chimera_usb_service *s) {
  if(!s->owns_usb) return true; // Never touch an unowned/inaccessible controller.
  if(clocked(s)) {
    wr(s,DCTL,2U); wr(s,GAHBCFG,0U); wr(s,GINTMSK,0U);
    wr(s,0x50000000U,rd(s,0x50000000U)&~CHIMERA_USB_SESSION_OVERRIDE_MASK);
    wr(s,GCCFG,rd(s,GCCFG)&~(1U<<16));
  }
  wr(s,AHB2RSTR,rd(s,AHB2RSTR)|USB_RESET);
  wr(s,AHB2ENR,rd(s,AHB2ENR)&~USB_RESET);
  bool quiet=(rd(s,AHB2RSTR)&USB_RESET)!=0U && (rd(s,AHB2ENR)&USB_RESET)==0U;
  if(quiet) s->owns_usb=0;
  return quiet;
}
static bool fail(chimera_usb_service *s,enum chimera_usb_service_error error) {
  s->error=error; s->phase=CHIMERA_USB_SERVICE_FAILED;
  invalidate(s); s->cleanup_ok=(uint8_t)release(s);
  return false;
}
static bool detached(const chimera_usb_service *s) {
  return chimera_usb_session_mode_valid(s->session_mode) && clocked(s) &&
    (rd(s,0x40023800U)&(3U|(1U<<18)))==3U &&
    (rd(s,0x40023808U)&255U)==0U && (rd(s,DCTL)&2U)!=0U && (rd(s,GAHBCFG)&33U)==0U &&
    (rd(s,0x50000000U)&CHIMERA_USB_SESSION_OVERRIDE_MASK)==chimera_usb_session_override(s->session_mode) &&
    (rd(s,GCCFG)&((1U<<16)|(1U<<21)))==(1U<<16);
}
bool chimera_usb_service_start(chimera_usb_service *s,const chimera_usb_io *io,
                              uint8_t self_powered,uint8_t max_power_2ma,uint32_t poll_budget) {
  return chimera_usb_service_start_mode(s,io,self_powered,max_power_2ma,poll_budget,CHIMERA_USB_SESSION_UNFORCED);
}
bool chimera_usb_service_start_mode(chimera_usb_service *s,const chimera_usb_io *io,
                                    uint8_t self_powered,uint8_t max_power_2ma,uint32_t poll_budget,
                                    enum chimera_usb_session_mode mode) {
  if(s==NULL || s->phase!=CHIMERA_USB_SERVICE_STOPPED) return false;
  s->phase=CHIMERA_USB_SERVICE_FAILED; s->error=CHIMERA_USB_SERVICE_ARGUMENT;
  s->facts_valid=0; s->owns_usb=0; s->cleanup_ok=1; s->driver.active=0; s->driver.ep0.initialized=0;
  s->session_mode=CHIMERA_USB_SESSION_UNFORCED;
  if(io==NULL || io->read32==NULL || io->write32==NULL || io->delay_us==NULL ||
     self_powered>1U || max_power_2ma>250U || poll_budget==0U || poll_budget>1000000U ||
     !chimera_usb_session_mode_valid(mode)) return false;
  s->session_mode=mode;
  s->io.context=io->context; s->io.read32=io->read32; s->io.write32=io->write32; s->io.delay_us=io->delay_us;
  // Complete ownership/clock preflight before even changing debug timing bits.
  if((rd(s,0x40023800U)&(3U|(1U<<18)))!=3U || (rd(s,0x40023808U)&255U)!=0U ||
     (rd(s,AHB2ENR)&USB_RESET)!=0U) return fail(s,CHIMERA_USB_SERVICE_OWNERSHIP);
  if(!chimera_boot_read_facts(&s->io,&s->facts)) return fail(s,CHIMERA_USB_SERVICE_FACTS);
  s->facts_valid=1;
  if(!chimera_usb_time16_init(&s->io)) return fail(s,CHIMERA_USB_SERVICE_TIMING);
  s->owns_usb=1; // From here clock preparation may change only our USB/PLL state.
  if(!chimera_usb_clock48(&s->io,poll_budget)) return fail(s,CHIMERA_USB_SERVICE_CLOCK);
  if(!chimera_usb_core_detached_mode(&s->io,poll_budget,s->session_mode)) return fail(s,CHIMERA_USB_SERVICE_CORE);
  if(!chimera_usb_driver_init(&s->driver,&s->io,s->facts.uid,self_powered,max_power_2ma,poll_budget))
    return fail(s,CHIMERA_USB_SERVICE_DRIVER);
  if(!detached(s)) return fail(s,CHIMERA_USB_SERVICE_INVARIANT);
  s->error=CHIMERA_USB_SERVICE_OK; s->phase=CHIMERA_USB_SERVICE_DETACHED;
  return true;
}
int chimera_usb_service_poll(chimera_usb_service *s,unsigned event_budget) {
  if(s==NULL || s->phase!=CHIMERA_USB_SERVICE_DETACHED || event_budget==0U || event_budget>32U) return -1;
  if(!detached(s)) { (void)fail(s,CHIMERA_USB_SERVICE_INVARIANT); return -1; }
  int result=chimera_usb_driver_poll(&s->driver,event_budget);
  if(result<0) { (void)fail(s,CHIMERA_USB_SERVICE_POLL); return -1; }
  if(!detached(s)) { (void)fail(s,CHIMERA_USB_SERVICE_INVARIANT); return -1; }
  return result;
}
bool chimera_usb_service_stop(chimera_usb_service *s) {
  if(s==NULL) return false;
  if(s->phase==CHIMERA_USB_SERVICE_STOPPED) return true;
  invalidate(s); s->cleanup_ok=(uint8_t)release(s);
  if(!s->cleanup_ok) { s->phase=CHIMERA_USB_SERVICE_FAILED; s->error=CHIMERA_USB_SERVICE_RELEASE; return false; }
  s->facts_valid=0; s->error=CHIMERA_USB_SERVICE_OK; s->phase=CHIMERA_USB_SERVICE_STOPPED;
  s->session_mode=CHIMERA_USB_SESSION_UNFORCED;
  return true;
}
