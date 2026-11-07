// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "main.h"
#include "usb_service_fake.h"

static const chimera_main_usb_config PROFILE = {1, 0, 8, 1}; // Synthetic only.
typedef struct { enum chimera_vbus_state before, after; unsigned samples; } power;
static enum chimera_vbus_state sample(void *ctx) {
  power *p = ctx;
  return p->samples++ == 0 ? p->before : p->after;
}
static void latched(chimera_main_runtime *r, fake *f, power *p, const chimera_vbus_io *vbus) {
  unsigned reads = f->reads, writes = f->writes, samples = p->samples;
  assert(chimera_main_poll(r, vbus) == -1);
  assert(!chimera_main_start(r, NULL, NULL, true, &PROFILE));
  assert(f->reads == reads && f->writes == writes && p->samples == samples);
}
int main(void) {
  unsigned scenarios = 0;
  // Missing callback or any non-PRESENT/invalid sample is refused before poll.
  const enum chimera_vbus_state bad[] = {CHIMERA_VBUS_UNKNOWN, CHIMERA_VBUS_ABSENT,
    (enum chimera_vbus_state)-1, (enum chimera_vbus_state)3, (enum chimera_vbus_state)255};
  for (unsigned i = 0; i < 7; ++i) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {i < 5 ? bad[i] : CHIMERA_VBUS_PRESENT, CHIMERA_VBUS_PRESENT, 0};
    chimera_vbus_io vbus = {&p, i == 6 ? NULL : sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(r.vbus == CHIMERA_VBUS_UNKNOWN && p.samples == 0);
    // Polling the service would detect this invariant fault; power must win first.
    *cell(&f, 0x50000008) = 1;
    assert(chimera_main_poll(&r, i == 5 ? NULL : &vbus) == -1);
    assert(r.state == CHIMERA_BOOT_USB_FAILED && r.error == CHIMERA_MAIN_USB_POWER);
    assert(r.service_error == CHIMERA_USB_SERVICE_OK);
    assert(r.vbus == (i == 1 ? CHIMERA_VBUS_ABSENT : CHIMERA_VBUS_UNKNOWN));
    assert(p.samples == (i < 5 ? 1U : 0U));
    assert(r.cleanup_ok && !r.usb.owns_usb && !r.usb.driver.active && !details.facts_valid);
    latched(&r, &f, &p, &vbus);
    assert(chimera_main_stop(&r) && r.vbus == CHIMERA_VBUS_UNKNOWN);
    ++scenarios;
  }
  // Presence can be lost during a bounded service poll; never return success.
  for (unsigned i = 0; i < 5; ++i) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {CHIMERA_VBUS_PRESENT, bad[i], 0}; chimera_vbus_io vbus = {&p, sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    *cell(&f, 0x50000014) = 1U << 12; // Real driver handles reset/budget exhaustion.
    assert(chimera_main_poll(&r, &vbus) == -1 && p.samples == 2);
    assert(r.error == CHIMERA_MAIN_USB_POWER && r.service_error == CHIMERA_USB_SERVICE_OK);
    assert(r.vbus == (i == 1 ? CHIMERA_VBUS_ABSENT : CHIMERA_VBUS_UNKNOWN));
    assert(r.cleanup_ok && !r.usb.owns_usb && !details.facts_valid);
    latched(&r, &f, &p, &vbus); assert(chimera_main_stop(&r)); ++scenarios;
  }
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {CHIMERA_VBUS_PRESENT, CHIMERA_VBUS_PRESENT, 0}; chimera_vbus_io vbus = {&p, sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(chimera_main_poll(&r, &vbus) == 0 && p.samples == 2);
    assert(r.vbus == CHIMERA_VBUS_PRESENT && r.state == CHIMERA_BOOT_USB_DETACHED && details.facts_valid);
    *cell(&f, 0x50000014) = 1U << 12;
    assert(chimera_main_poll(&r, &vbus) == 2 && p.samples == 4);
    assert(chimera_main_stop(&r) && r.vbus == CHIMERA_VBUS_UNKNOWN);
    unsigned samples = p.samples, reads = f.reads, writes = f.writes;
    assert(chimera_main_poll(&r, &vbus) == -1 && p.samples == samples);
    assert(f.reads == reads && f.writes == writes);
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(r.vbus == CHIMERA_VBUS_UNKNOWN);
    // Earlier present readings cannot replace a missing reader on a new poll.
    assert(chimera_main_poll(&r, NULL) == -1 && p.samples == samples);
    assert(r.error == CHIMERA_MAIN_USB_POWER && !details.facts_valid);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {CHIMERA_VBUS_ABSENT, CHIMERA_VBUS_PRESENT, 0}; chimera_vbus_io vbus = {&p, sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    f.cleanup_stuck = f.clock_gate_stuck = true;
    assert(chimera_main_poll(&r, &vbus) == -1 && !r.cleanup_ok && r.usb.owns_usb);
    assert(r.error == CHIMERA_MAIN_USB_POWER && r.service_error == CHIMERA_USB_SERVICE_OK);
    assert(r.usb.error == CHIMERA_USB_SERVICE_RELEASE && !details.facts_valid);
    latched(&r, &f, &p, &vbus);
    assert(!chimera_main_stop(&r) && r.error == CHIMERA_MAIN_USB_STOP);
    assert(r.usb.owns_usb && r.vbus == CHIMERA_VBUS_UNKNOWN);
    f.cleanup_stuck = f.clock_gate_stuck = false;
    assert(chimera_main_stop(&r));
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    p.before = p.after = CHIMERA_VBUS_PRESENT; p.samples = 0;
    assert(chimera_main_poll(&r, &vbus) == 0 && p.samples == 2);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {CHIMERA_VBUS_PRESENT, CHIMERA_VBUS_UNKNOWN, 0}; chimera_vbus_io vbus = {&p, sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    *cell(&f, 0x50000008) = 1;
    assert(chimera_main_poll(&r, &vbus) == -1 && p.samples == 1);
    assert(r.error == CHIMERA_MAIN_USB_POLL && r.service_error == CHIMERA_USB_SERVICE_INVARIANT);
    assert(r.vbus == CHIMERA_VBUS_PRESENT && !details.facts_valid);
    latched(&r, &f, &p, &vbus); assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Production no-profile path does not call a power reader or USB service.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    power p = {CHIMERA_VBUS_PRESENT, CHIMERA_VBUS_PRESENT, 0}; chimera_vbus_io vbus = {&p, sample};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(!chimera_main_start(&r, &details, &io, true, NULL));
    assert(r.state == CHIMERA_BOOT_USB_HELD && r.vbus == CHIMERA_VBUS_UNKNOWN);
    assert(chimera_main_poll(&r, &vbus) == -1 && !p.samples && f.reads == 8 && !f.writes);
    assert(chimera_main_stop(&r));
    assert(chimera_main_poll(NULL, &vbus) == -1 && !p.samples); ++scenarios;
  }
  printf("Main VBUS supervision: %u real-component scenarios pass; pre/post observations, fail-closed cleanup, explicit restart; no attachment\n", scenarios);
}
