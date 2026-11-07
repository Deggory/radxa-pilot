// SPDX-License-Identifier: MIT
#include <stddef.h>
#include "usb_driver.h"

#define BASE 0x50000000U
#define EN (1U<<31)
#define NAK (1U<<27)
#define CNAK (1U<<26)
#define STALL (1U<<21)
#define ACTIVE (1U<<15)
#define EVENTS ((1U<<12)|(1U<<13)|(1U<<18)|(1U<<19)|16U)
#define SUSPEND (1U<<11)
#define WAKE (1U<<31)
#define OTG_KNOWN 0x1E0304U
#define OTG_BENIGN ((1U<<18)|(1U<<19))

static uint32_t rd(const chimera_usb_driver *d, uint32_t off) { return d->io->read32(d->io->context,BASE+off); }
static void wr(const chimera_usb_driver *d, uint32_t off,uint32_t value) { d->io->write32(d->io->context,BASE+off,value); }
static bool wait_bits(const chimera_usb_driver *d,uint32_t off,uint32_t mask,uint32_t value) {
  for(uint32_t i=0;i<d->poll_budget;++i) if((rd(d,off)&mask)==value) return true;
  return false;
}
static bool clocked(const chimera_usb_io *io) {
  return (io->read32(io->context,0x40023834U)&128U)!=0U &&
         (io->read32(io->context,0x40023814U)&128U)==0U;
}
static int failure(chimera_usb_driver *d) {
  d->active=0; d->attached=0; d->suspended=0;
  d->in_armed=0; d->out_armed=0; d->setup_wait=0;
  chimera_usb_ep0_reset(&d->ep0);
  wr(d,0x804,2U); wr(d,8,0U); wr(d,0x18,0U);
  wr(d,0x38,rd(d,0x38)&~(1U<<16));
  return -1;
}
static bool flush(const chimera_usb_driver *d,uint32_t bit) {
  if(!wait_bits(d,0x10,1U<<31,1U<<31)) return false;
  wr(d,0x10,bit);
  return wait_bits(d,0x10,bit,0U);
}
static void setup_window(const chimera_usb_driver *d) {
  // ST non-DMA EP0_OutStart: prepare three SETUP slots without EPENA.
  wr(d,0xB10,(3U<<29)|(1U<<19)|24U);
}
static bool stop_in(chimera_usb_driver *d) {
  if((rd(d,0x900)&EN)!=0U) {
    wr(d,0x900,rd(d,0x900)|NAK|(1U<<30));
    if(!wait_bits(d,0x900,EN,0U)) return false;
  }
  if(!flush(d,1U<<5)) return false;
  // Clear old completion/disable/timeout events before a new generation is armed.
  wr(d,0x908,0x1BU); wr(d,0x900,ACTIVE|NAK); d->in_armed=0;
  return true;
}
static bool reset_bus(chimera_usb_driver *d) {
  chimera_usb_ep0_reset(&d->ep0);
  d->setup_wait=0; d->in_armed=0; d->out_armed=0; d->out_seen=0;
  if(!d->ep0.initialized || !wait_bits(d,0xB00,EN,0U) || !stop_in(d) || !flush(d,1U<<4)) return false;
  wr(d,0xB08,0x7BU); wr(d,0xB00,ACTIVE|NAK);
  wr(d,0x800,rd(d,0x800)&~(127U<<4));
  wr(d,0x810,0x109U); wr(d,0x814,9U); wr(d,0x81C,0x10001U); wr(d,0x834,0U);
  setup_window(d);
  return true;
}
bool chimera_usb_driver_init(chimera_usb_driver *d,const chimera_usb_io *io,
                             const uint8_t *uid,uint8_t self_powered,uint8_t max_power_2ma,uint32_t poll_budget) {
  if(d==NULL) return false;
  d->active=0; d->attached=0; d->suspended=0; d->last_otg=0; d->io=NULL;
  if(io==NULL || io->read32==NULL || io->write32==NULL || poll_budget==0 || poll_budget>1000000U ||
     !chimera_usb_ep0_init(&d->ep0,uid,self_powered,max_power_2ma) || !clocked(io)) return false;
  d->io=io; d->poll_budget=poll_budget;
  if((rd(d,0x804)&2U)==0U || (rd(d,8)&32U)!=0U || (rd(d,0x800)&3U)!=3U ||
     (rd(d,0xC)&((1U<<30)|(1U<<6)))!=((1U<<30)|(1U<<6)) || (rd(d,0x38)&(1U<<16))==0U) return false;
  wr(d,8,0U); // Polling only; never enable the global interrupt line.
  if(!reset_bus(d)) { (void)failure(d); return false; }
  wr(d,0x14,(1U<<12)|(1U<<13)); wr(d,0x18,EVENTS); d->active=1;
  return true;
}
bool chimera_usb_driver_attach(chimera_usb_driver *d) {
  if(d==NULL || !d->active || d->attached) return false;
  // Owning service has drained events and checked invariants while detached.
  if(!d->ep0.initialized || d->ep0.address || d->ep0.configuration ||
     d->ep0.phase!=CHIMERA_EP0_IDLE || d->setup_wait || d->in_armed || d->out_armed) return false;
  if(!clocked(d->io) || (rd(d,0x804)&2U)==0U || (rd(d,8)&33U)!=0U) return false;
  wr(d,0x18,EVENTS|4U|SUSPEND|WAKE);
  wr(d,0x804,rd(d,0x804)&~2U);
  if((rd(d,0x804)&2U)!=0U) { (void)failure(d); return false; }
  d->attached=1;
  return true;
}
static bool stall(chimera_usb_driver *d) {
  d->setup_wait=0; d->out_armed=0; d->out_seen=0;
  d->ep0.phase=CHIMERA_EP0_STALL; d->ep0.pending_kind=0;
  if(!stop_in(d)) return false;
  wr(d,0x900,ACTIVE|NAK|STALL); wr(d,0xB00,ACTIVE|NAK|STALL); setup_window(d);
  return true;
}
static bool start_in(chimera_usb_driver *d) {
  if(d->reply_size<0) return stall(d);
  unsigned size=(unsigned)d->reply_size, words=(size+3U)/4U;
  if(size>64U || (rd(d,0x900)&EN)!=0U) return false;
  bool space=words==0U;
  for(uint32_t i=0;!space && i<d->poll_budget;++i) space=(rd(d,0x918)&65535U)>=words;
  if(!space) return false;
  wr(d,0x908,0x1BU);
  wr(d,0x910,(1U<<19)|size);
  d->in_generation=d->ep0.generation; d->in_armed=1;
  wr(d,0x900,ACTIVE|CNAK|EN);
  for(unsigned word=0;word<words;++word) {
    uint32_t value=0;
    for(unsigned byte=0;byte<4U;++byte) {
      unsigned at=word*4U+byte;
      if(at<size) value|=(uint32_t)d->reply[at]<<(byte*8U);
    }
    wr(d,0x1000,value);
  }
  return true;
}
static bool in_complete(chimera_usb_driver *d) {
  uint32_t events=rd(d,0x908);
  if((events&0x108U)!=0U) return false;
  wr(d,0x908,events&0x1BU);
  if((events&1U)==0U || !d->in_armed) return true;
  if((rd(d,0x900)&EN)!=0U || (rd(d,0x910)&0x7FFFFU)!=0U) return false;
  d->in_armed=0;
  if(!chimera_usb_ep0_in_complete(&d->ep0,d->in_generation)) return false;
  if(d->ep0.phase==CHIMERA_EP0_STATUS_OUT) {
    d->out_generation=d->ep0.generation; d->out_armed=1; d->out_seen=0;
    wr(d,0xB08,1U); wr(d,0xB10,(3U<<29)|(1U<<19)|64U);
    wr(d,0xB00,ACTIVE|CNAK|EN);
  } else {
    wr(d,0x800,(rd(d,0x800)&~(127U<<4))|((uint32_t)d->ep0.address<<4));
    setup_window(d);
  }
  return true;
}
static bool rx_packet(chimera_usb_driver *d) {
  uint32_t status=rd(d,0x20);
  unsigned ep=status&15U, size=(status>>4)&2047U, kind=(status>>17)&15U;
  if(ep!=0U || size>64U || (kind!=1U && kind!=2U && kind!=3U && kind!=4U && kind!=6U) ||
     (kind!=2U && kind!=6U && size!=0U) || (kind==6U && size!=8U)) return false;
  uint8_t setup[8];
  for(unsigned word=0;word<(size+3U)/4U;++word) {
    uint32_t value=rd(d,0x1000);
    if(kind==6U) for(unsigned i=0;i<4U;++i) setup[word*4U+i]=(uint8_t)(value>>(i*8U));
  }
  if(kind==6U) {
    d->out_armed=0; d->out_seen=0;
    // New SETUP invalidates pending software work before any later completion.
    d->reply_size=chimera_usb_ep0_setup(&d->ep0,setup,8U,d->reply,sizeof(d->reply));
    if(!d->ep0.initialized || !stop_in(d)) return false;
    wr(d,0xB08,1U); wr(d,0xB00,ACTIVE|NAK); d->setup_wait=1;
  } else if(kind==2U) {
    if(!d->out_armed || d->out_seen || size!=0U) return stall(d);
    d->out_seen=1;
  }
  return true;
}
static bool out_complete(chimera_usb_driver *d) {
  uint32_t events=rd(d,0xB08);
  wr(d,0xB08,events&0x7BU);
  if((events&8U)!=0U) {
    if(!d->setup_wait) return false;
    d->setup_wait=0;
    return start_in(d); // SETUP dominates a coalesced old OUT completion.
  }
  if((events&1U)!=0U && d->out_armed) {
    if(!d->out_seen || (rd(d,0xB00)&EN)!=0U ||
       !chimera_usb_ep0_out_complete(&d->ep0,d->out_generation,0U)) return false;
    d->out_armed=0; d->out_seen=0; setup_window(d);
  }
  return true;
}
int chimera_usb_driver_poll(chimera_usb_driver *d,unsigned event_budget) {
  if(d==NULL || !d->active || event_budget==0U || event_budget>32U) return -1;
  if(!clocked(d->io)) {
    d->active=0; d->attached=0; d->suspended=0;
    d->in_armed=0; d->out_armed=0; d->setup_wait=0;
    chimera_usb_ep0_reset(&d->ep0);
    return -1; // Do not access a gated/reset core.
  }
  bool progress=false;
  for(unsigned i=0;i<event_budget;++i) {
    uint32_t events=rd(d,0x14);
    // Wrong role/mode, connector-role change or unsupported LPM are fatal.
    if((events&(3U|(1U<<27)|(1U<<28)|(1U<<29)))!=0U) return failure(d);
    if((events&4U)!=0U) {
      uint32_t causes=rd(d,4U); d->last_otg=causes;
      if(causes==0U || (causes&~OTG_KNOWN)!=0U) return failure(d);
      wr(d,4U,causes); // W1C only the observed causes, not a second read/RMW.
      if((causes&~(OTG_BENIGN|4U))!=0U) return failure(d);
      if((causes&4U)!=0U) {
        if(!d->attached) return failure(d);
        (void)failure(d); // Session end dominates reset and old completions.
        return 3;
      }
    } else if((events&(1U<<12))!=0U) {
      if(!reset_bus(d)) return failure(d);
      d->suspended=0;
      wr(d,0x14,events&((1U<<12)|SUSPEND|WAKE));
    } else if((events&(SUSPEND|WAKE))!=0U) {
      if(!d->attached) return failure(d);
      // Both may be coalesced: current hardware status decides, never ordering.
      d->suspended=(uint8_t)(rd(d,0x808)&1U);
      wr(d,0x14,events&(SUSPEND|WAKE));
    } else if(d->suspended) {
      return progress ? 1:0; // Retain pending control transfer through suspend.
    } else if((events&(1U<<13))!=0U) {
      if((rd(d,0x808)&6U)!=6U || !reset_bus(d)) return failure(d); // Internal FS PHY only.
      wr(d,0x804,rd(d,0x804)|(1U<<8)); // Clear inherited global IN NAK after enumeration.
      wr(d,0x14,1U<<13);
    } else if((events&(1U<<18))!=0U) {
      if((rd(d,0x818)&~0x10001U)!=0U || !in_complete(d)) return failure(d);
    } else if((events&16U)!=0U) {
      if(!rx_packet(d)) return failure(d);
    } else if((events&(1U<<19))!=0U) {
      if((rd(d,0x818)&~0x10001U)!=0U || !out_complete(d)) return failure(d);
    } else return progress ? 1:0;
    progress=true;
  }
  return 2;
}
