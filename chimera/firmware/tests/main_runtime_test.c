// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "main.h"
#include "usb_service_fake.h"

static const chimera_main_usb_config PROFILE = {1, 0, 8, 4};

static void no_poll_io(chimera_main_runtime *r, fake *f) {
  unsigned reads = f->reads, writes = f->writes;
  assert(chimera_main_poll(r) == -1 && f->reads == reads && f->writes == writes);
}

int main(void) {
  unsigned scenarios = 0;
  // This is the production board's explicit NULL-profile path: snapshot only.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(!chimera_main_start(&r, &details, &io, true, NULL));
    assert(r.state == CHIMERA_BOOT_USB_HELD && details.facts_valid && f.reads == 8 && f.writes == 0);
    assert(r.error == CHIMERA_MAIN_USB_NONE && !r.usb.owns_usb);
    no_poll_io(&r, &f);
    unsigned reads = f.reads;
    assert(!chimera_main_start(&r, &details, &io, true, &PROFILE) && f.reads == reads);
    assert(chimera_main_stop(&r) && r.state == CHIMERA_BOOT_USB_STOPPED && !details.facts_valid);
    assert(f.reads == reads && f.writes == 0);
    // Explicit start with no profile cannot reuse a previous profile.
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(chimera_main_stop(&r)); reads = f.reads; unsigned writes = f.writes;
    assert(!chimera_main_start(&r, &details, &io, true, NULL));
    assert(r.state == CHIMERA_BOOT_USB_HELD && f.reads == reads + 8 && f.writes == writes);
    ++scenarios;
  }
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(!chimera_main_start(&r, &details, &io, false, &PROFILE));
    assert(r.state == CHIMERA_BOOT_CLOCK_FAILED && f.reads == 0 && f.writes == 0 && !details.facts_valid);
    no_poll_io(&r, &f); assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Invalid explicit profiles/callbacks fail before any register access.
  for (unsigned bad = 0; bad < 11; ++bad) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_usb_config profile = PROFILE;
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    if (bad == 0) profile.self_powered = 2;
    if (bad == 1) profile.max_power_2ma = 251;
    if (bad == 2) profile.poll_budget = 0;
    if (bad == 3) profile.poll_budget = 1000001U;
    if (bad == 4) profile.event_budget = 0;
    if (bad == 5) profile.event_budget = 33;
    if (bad == 6) io.read32 = NULL;
    if (bad == 7) io.write32 = NULL;
    if (bad == 8) io.delay_us = NULL;
    assert(!chimera_main_start(&r, bad == 9 ? NULL : &details, bad == 10 ? NULL : &io, true, &profile));
    assert(r.state == CHIMERA_BOOT_ARGUMENT_FAILED && r.error == CHIMERA_MAIN_USB_ARGUMENT);
    assert(f.reads == 0 && f.writes == 0 && !details.facts_valid);
    no_poll_io(&r, &f); assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Run the real preparation/service/clock/EP0/driver under the existing fault matrix.
  for (unsigned failure = 0; failure <= 19; ++failure) {
    fake f; base(&f, failure); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    bool ok = chimera_main_start(&r, &details, &io, true, &PROFILE);
    assert(ok == (failure == 0));
    if (ok) {
      assert(r.state == CHIMERA_BOOT_USB_DETACHED && r.usb.driver.active && details.facts_valid);
      assert(r.usb.driver.io == &r.usb.io && r.details == &details);
      assert(chimera_main_poll(&r) == 0);
      unsigned reads = f.reads, writes = f.writes;
      assert(!chimera_main_start(&r, NULL, NULL, false, NULL));
      assert(r.state == CHIMERA_BOOT_USB_DETACHED && details.facts_valid && f.reads == reads && f.writes == writes);
      assert(chimera_main_stop(&r) && !details.facts_valid && !r.usb.owns_usb);
    } else {
      assert(!details.facts_valid);
      assert(r.state == (failure <= 2 ? CHIMERA_BOOT_FACTS_FAILED : CHIMERA_BOOT_USB_FAILED));
      if (failure <= 2) assert(f.writes == 0 && r.error == CHIMERA_MAIN_USB_NONE);
      else assert(r.error == CHIMERA_MAIN_USB_START && r.service_error != CHIMERA_USB_SERVICE_OK);
      assert(r.cleanup_ok == (failure != 9));
      no_poll_io(&r, &f);
      unsigned reads = f.reads;
      assert(!chimera_main_start(&r, &details, &io, true, &PROFILE) && f.reads == reads);
    }
    assert(f.reads < 2000 && f.writes < 150);
    ++scenarios;
  }
  // Clock/controller ownership must be refused without taking it over.
  for (unsigned bad = 0; bad < 4; ++bad) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    if (bad == 0) *cell(&f, 0x40023834) |= 128;
    if (bad == 1) *cell(&f, 0x40023808) = 8;
    if (bad == 2) *cell(&f, 0x40023808) = 128;
    if (bad == 3) *cell(&f, 0x40023800) |= 1U << 18;
    assert(!chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(r.service_error == CHIMERA_USB_SERVICE_OWNERSHIP && f.writes == 0);
    assert(!r.usb.owns_usb && r.cleanup_ok && !details.facts_valid);
    no_poll_io(&r, &f); ++scenarios;
  }
  for (unsigned fault = 0; fault < 10; ++fault) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    switch (fault) {
      case 0: *cell(&f, 0x50000804) = 0; break;
      case 1: *cell(&f, 0x50000008) = 1; break;
      case 2: *cell(&f, 0x50000008) = 32; break;
      case 3: *cell(&f, 0x50000000) = 128; break;
      case 4: *cell(&f, 0x50000038) = 0; break;
      case 5: *cell(&f, 0x40023834) &= ~128U; break;
      case 6: *cell(&f, 0x40023814) |= 128; break;
      case 7: *cell(&f, 0x50000014) = 1U << 11; break;
      case 8: *cell(&f, 0x40023808) = 8; break;
      case 9: f.attach_during_poll = true; break;
      default: assert(false);
    }
    assert(chimera_main_poll(&r) == -1 && r.state == CHIMERA_BOOT_USB_FAILED);
    assert(r.error == CHIMERA_MAIN_USB_POLL && r.service_error != CHIMERA_USB_SERVICE_OK);
    assert(r.cleanup_ok && !r.usb.owns_usb && !details.facts_valid);
    no_poll_io(&r, &f);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Failed cleanup is retained; start/poll cannot silently retry it.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    f.cleanup_stuck = f.clock_gate_stuck = true; *cell(&f, 0x50000008) = 1;
    assert(chimera_main_poll(&r) == -1 && !r.cleanup_ok && r.usb.owns_usb && !details.facts_valid);
    unsigned reads = f.reads, writes = f.writes;
    assert(!chimera_main_start(&r, &details, &io, true, &PROFILE));
    no_poll_io(&r, &f); assert(f.reads == reads && f.writes == writes);
    assert(!chimera_main_stop(&r) && r.state == CHIMERA_BOOT_USB_FAILED && !r.cleanup_ok);
    f.cleanup_stuck = f.clock_gate_stuck = false;
    assert(chimera_main_stop(&r) && r.state == CHIMERA_BOOT_USB_STOPPED && r.cleanup_ok);
    reads = f.reads; assert(chimera_main_stop(&r) && f.reads == reads);
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Two individually stable but different UID snapshots cannot select a new identity.
  {
    fake f; base(&f, 0); f.identity_changed_after_snapshot = true;
    chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(!chimera_main_start(&r, &details, &io, true, &PROFILE));
    assert(r.state == CHIMERA_BOOT_USB_FAILED && r.error == CHIMERA_MAIN_USB_IDENTITY);
    assert(r.cleanup_ok && !r.usb.owns_usb && !details.facts_valid);
    no_poll_io(&r, &f); assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Caller config/IO are copied; progress/budget exhaustion use the real driver.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_usb_config profile = {0, 50, 8, 1};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &profile));
    profile.event_budget = 0; io.read32 = NULL;
    assert(r.config.event_budget == 1 && chimera_main_poll(&r) == 0);
    *cell(&f, 0x50000014) = 1U << 12;
    assert(chimera_main_poll(&r) == 2 && r.state == CHIMERA_BOOT_USB_DETACHED);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  // A successful explicit stop can fail; surface that result and preserve ownership.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details details = {0};
    assert(chimera_main_start(&r, &details, &io, true, &PROFILE));
    f.cleanup_stuck = f.clock_gate_stuck = true;
    assert(!chimera_main_stop(&r) && r.error == CHIMERA_MAIN_USB_STOP && !r.cleanup_ok);
    assert(r.usb.owns_usb && !details.facts_valid);
    f.cleanup_stuck = f.clock_gate_stuck = false;
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  assert(!chimera_main_start(NULL, NULL, NULL, false, NULL));
  assert(chimera_main_poll(NULL) == -1 && !chimera_main_stop(NULL));
  printf("Main USB coordinator: %u real-component gate/start/poll/cleanup/restart scenarios pass; detached only\n", scenarios);
}
