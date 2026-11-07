// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "main.h"
#include "usb_service_fake.h"

#define GOTG 0x50000000U
#define OVERRIDES 0xF0U
#define BSESSION 0xC0U
static const chimera_main_usb_config LEGACY = {1, 0, 8, 1, CHIMERA_USB_SESSION_LEGACY_NO_VBUS};
static unsigned samples;
static enum chimera_vbus_state present(void *ctx) { (void)ctx; ++samples; return CHIMERA_VBUS_PRESENT; }
static const chimera_vbus_io POWER = {NULL, present};

int main(void) {
  unsigned scenarios = 0;
  // The original entry stays unforced; the explicit entry prepares legacy only.
  for (unsigned mode = 0; mode < 2; ++mode) for (unsigned fault = 0; fault < 20; ++fault) {
    fake f; base(&f, fault); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_usb_service s = {0};
    bool ok = mode == 0 ? chimera_usb_service_start(&s, &io, 1, 0, 8) :
      chimera_usb_service_start_mode(&s, &io, 1, 0, 8, CHIMERA_USB_SESSION_LEGACY_NO_VBUS);
    assert(ok == (fault == 0));
    if (ok) {
      assert(s.session_mode == (enum chimera_usb_session_mode)mode);
      assert((*cell(&f, GOTG) & OVERRIDES) == (mode ? BSESSION : 0));
      assert((*cell(&f, 0x50000038) & (1U << 21)) == 0);
      assert(chimera_usb_service_poll(&s, 1) == 0);
      assert(chimera_usb_service_stop(&s));
      assert((*cell(&f, GOTG) & OVERRIDES) == 0 && !s.owns_usb);
      assert(s.session_mode == CHIMERA_USB_SESSION_UNFORCED);
    } else {
      assert(s.phase == CHIMERA_USB_SERVICE_FAILED && !s.driver.active);
      assert((*cell(&f, GOTG) & OVERRIDES) == 0);
      unsigned reads = f.reads, writes = f.writes;
      assert(chimera_usb_service_poll(&s, 1) == -1);
      assert(!chimera_usb_service_start_mode(&s, &io, 1, 0, 8, CHIMERA_USB_SESSION_LEGACY_NO_VBUS));
      assert(f.reads == reads && f.writes == writes);
      if (fault == 9) f.failure = 0; // Explicit retry after the blocking condition clears.
      assert(chimera_usb_service_stop(&s));
    }
    assert(f.reads < 2500 && f.writes < 160); ++scenarios;
  }
  const enum chimera_usb_session_mode bad[] = {(enum chimera_usb_session_mode)-1,
    (enum chimera_usb_session_mode)2, (enum chimera_usb_session_mode)255};
  for (unsigned i = 0; i < 3; ++i) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_usb_service s = {0}; chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    chimera_main_usb_config config = LEGACY; config.session_mode = bad[i];
    assert(!chimera_usb_core_detached_mode(&io, 8, bad[i]));
    assert(!chimera_usb_service_start_mode(&s, &io, 1, 0, 8, bad[i]));
    assert(!chimera_main_start(&r, &d, &io, true, &config));
    assert(r.state == CHIMERA_BOOT_ARGUMENT_FAILED && !d.facts_valid);
    assert(s.error == CHIMERA_USB_SERVICE_ARGUMENT && !s.owns_usb);
    assert(f.reads == 0 && f.writes == 0); assert(chimera_usb_service_stop(&s)); ++scenarios;
  }
  // Main uses the real legacy service, without substituting a VBUS observation.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0}; chimera_main_usb_config config = LEGACY;
    assert(chimera_main_start(&r, &d, &io, true, &config)); config.session_mode = CHIMERA_USB_SESSION_UNFORCED;
    assert(r.config.session_mode == CHIMERA_USB_SESSION_LEGACY_NO_VBUS && r.vbus == CHIMERA_VBUS_UNKNOWN);
    assert(chimera_main_poll(&r, NULL) == 0 && !samples && d.facts_valid);
    unsigned generation = r.usb.driver.ep0.generation;
    r.usb.driver.ep0.address = 17; r.usb.driver.ep0.configuration = 1;
    *cell(&f, 0x50000800) |= 17U << 4; *cell(&f, 0x50000014) = 1U << 12;
    assert(chimera_main_poll(&r, NULL) == 2);
    assert(r.usb.driver.ep0.generation != generation && !r.usb.driver.ep0.address && !r.usb.driver.ep0.configuration);
    assert((*cell(&f, 0x50000800) & (127U << 4)) == 0 && (*cell(&f, GOTG) & OVERRIDES) == BSESSION);
    assert(r.vbus == CHIMERA_VBUS_UNKNOWN && d.facts_valid && !samples);
    assert(chimera_main_stop(&r) && (*cell(&f, GOTG) & OVERRIDES) == 0);
    assert(!chimera_main_start(&r, &d, &io, true, NULL) && r.state == CHIMERA_BOOT_USB_HELD);
    assert(chimera_main_stop(&r));
    assert(chimera_main_start(&r, &d, &io, true, &config));
    assert((*cell(&f, GOTG) & OVERRIDES) == 0);
    assert(chimera_main_poll(&r, NULL) == -1 && r.error == CHIMERA_MAIN_USB_POWER);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Mixing a VBUS reader into explicitly no-sense mode is rejected, not ignored.
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    assert(chimera_main_poll(&r, &POWER) == -1 && !samples);
    assert(r.error == CHIMERA_MAIN_USB_ARGUMENT && !d.facts_valid && !r.usb.owns_usb);
    assert(r.vbus == CHIMERA_VBUS_UNKNOWN && (*cell(&f, GOTG) & OVERRIDES) == 0);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  // Live policy cannot silently change or fall back after controller preparation.
  for (unsigned bad_mode = 0; bad_mode < 2; ++bad_mode) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    r.config.session_mode = bad_mode == 0 ? CHIMERA_USB_SESSION_UNFORCED : (enum chimera_usb_session_mode)2;
    assert(chimera_main_poll(&r, NULL) == -1 && r.error == CHIMERA_MAIN_USB_ARGUMENT);
    assert(!samples && !d.facts_valid && !r.usb.owns_usb && r.cleanup_ok);
    assert((*cell(&f, GOTG) & OVERRIDES) == 0); assert(chimera_main_stop(&r)); ++scenarios;
  }
  for (unsigned fault = 0; fault < 12; ++fault) {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    switch (fault) {
      case 0: *cell(&f, GOTG) &= ~64U; break;
      case 1: *cell(&f, GOTG) &= ~128U; break;
      case 2: *cell(&f, GOTG) = 0; break;
      case 3: *cell(&f, GOTG) |= 16U; break;
      case 4: *cell(&f, GOTG) |= 32U; break;
      case 5: *cell(&f, 0x50000038) |= 1U << 21; break;
      case 6: *cell(&f, 0x50000804) = 0; break;
      case 7: *cell(&f, 0x50000008) = 32; break;
      case 8: *cell(&f, 0x50000014) = 1U << 11; break;
      case 9: *cell(&f, 0x50000014) = 4; break;
      case 10: f.clear_session_during_poll = true; break;
      case 11: *cell(&f, 0x40023834) &= ~128U; break;
      default: assert(false);
    }
    assert(chimera_main_poll(&r, NULL) == -1 && r.state == CHIMERA_BOOT_USB_FAILED);
    assert(r.error == CHIMERA_MAIN_USB_POLL && r.service_error != CHIMERA_USB_SERVICE_OK);
    assert(!d.facts_valid && !r.usb.driver.active && !r.usb.owns_usb && r.cleanup_ok);
    unsigned reads = f.reads, writes = f.writes;
    assert(chimera_main_poll(&r, &POWER) == -1 && !samples);
    assert(!chimera_main_start(&r, &d, &io, true, &LEGACY));
    assert(f.reads == reads && f.writes == writes);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  {
    fake f; base(&f, 0); f.session_write_stuck = true; chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    assert(!chimera_main_start(&r, &d, &io, true, &LEGACY));
    assert(r.error == CHIMERA_MAIN_USB_START && r.service_error == CHIMERA_USB_SERVICE_CORE);
    assert(!r.usb.owns_usb && !d.facts_valid && r.cleanup_ok); assert(chimera_main_stop(&r)); ++scenarios;
  }
  {
    fake f; base(&f, 0); chimera_usb_io io = {&f, rd, wr, delay};
    chimera_main_runtime r = {0}; chimera_boot_details d = {0};
    assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    f.cleanup_stuck = f.clock_gate_stuck = true; *cell(&f, 0x50000014) = 1U << 11;
    assert(chimera_main_poll(&r, NULL) == -1 && !r.cleanup_ok && r.usb.owns_usb);
    assert((*cell(&f, GOTG) & OVERRIDES) == 0 && !d.facts_valid);
    unsigned reads = f.reads, writes = f.writes;
    assert(chimera_main_poll(&r, NULL) == -1 && !chimera_main_start(&r, &d, &io, true, &LEGACY));
    assert(f.reads == reads && f.writes == writes && !samples);
    assert(!chimera_main_stop(&r)); f.cleanup_stuck = f.clock_gate_stuck = false;
    assert(chimera_main_stop(&r)); assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    // Cleanup success does not remove an externally injected fault condition.
    assert(chimera_main_poll(&r, NULL) == -1 && r.error == CHIMERA_MAIN_USB_POLL);
    assert(chimera_main_stop(&r)); *cell(&f, 0x50000014) = 0;
    assert(chimera_main_start(&r, &d, &io, true, &LEGACY));
    assert(chimera_main_poll(&r, NULL) == 0 && r.vbus == CHIMERA_VBUS_UNKNOWN);
    assert(chimera_main_stop(&r)); ++scenarios;
  }
  printf("Legacy session: %u real-component mode/start/reset/fault/cleanup/restart scenarios pass; VBUS unknown, detached only\n", scenarios);
}
