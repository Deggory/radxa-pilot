// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "protocol.h"

// Independent wire fixture: CHMR/schema1/length32/F413-family1/bootstrap0,
// no operational capabilities or layout hashes, 3 classical buses, 9 interfaces.
static const uint8_t manifest[32] = {
  0x43, 0x48, 0x4D, 0x52, 1, 32, 1, 0,
  0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 3, 8, 0, 0,
  0xFF, 1, 0, 0, 0, 0, 0, 0,
};
static const char version[] = "chimera-f413-bootstrap-v1";
static unsigned cases;

static void check(const uint8_t *setup, size_t setup_size, size_t capacity, int expected) {
  uint8_t guarded[80];
  memset(guarded, 0xA5, sizeof(guarded));
  int length = chimera_control_read(setup, setup_size, guarded + 8, capacity);
  assert(length == expected);
  for (size_t i = 0; i < sizeof(guarded); ++i) {
    if (expected > 0 && i >= 8 && i < (size_t)expected + 8) {
      const uint8_t *payload = setup[1] == 0xA0 ? manifest : (const uint8_t *)version;
      assert(guarded[i] == payload[i - 8]);
    } else {
      assert(guarded[i] == 0xA5);
    }
  }
  ++cases;
}

int main(void) {
  assert(sizeof(manifest) == CHIMERA_MANIFEST_SIZE);
  assert(memcmp(chimera_manifest, manifest, sizeof(manifest)) == 0);
  assert(strcmp(chimera_firmware_version, version) == 0);
  assert(strcmp(chimera_usb_product, "Chimera F413") == 0);
  uint8_t setup[8] = {0xC0, 0xA0, 0, 0, 0, 0, 64, 0};
  // Exhaustive direction/type/recipient and request-number combinations.
  for (unsigned bm = 0; bm < 256; ++bm) {
    for (unsigned req = 0; req < 256; ++req) {
      setup[0] = bm;
      setup[1] = req;
      int expected = -1;
      if (bm == 0xC0 && req == 0xA0) expected = 32;
      if (bm == 0xC0 && req == 0xD6) expected = sizeof(version) - 1;
      check(setup, 8, 64, expected);
    }
  }
  setup[0] = 0xC0;
  const unsigned requests[] = {0xA0, 0xD6};
  for (unsigned request = 0; request < 2; ++request) {
    setup[1] = requests[request];
    const unsigned payload = request == 0 ? 32U : sizeof(version) - 1U;
    for (unsigned length = 0; length <= UINT16_MAX; ++length) {
      setup[6] = length;
      setup[7] = length >> 8;
      check(setup, 8, 64, length >= payload && length <= 64 ? (int)payload : -1);
    }
    setup[6] = 64;
    setup[7] = 0;
    // wValue and wIndex must be zero, including their high bytes.
    for (unsigned field = 2; field <= 4; field += 2) {
      for (unsigned value = 0; value <= UINT16_MAX; ++value) {
        setup[field] = value;
        setup[field + 1] = value >> 8;
        check(setup, 8, 64, value == 0 ? (int)payload : -1);
      }
      setup[field] = setup[field + 1] = 0;
    }
    for (size_t capacity = 0; capacity <= 64; ++capacity) {
      check(setup, 8, capacity, capacity >= payload ? (int)payload : -1);
    }
    for (size_t size = 0; size <= 16; ++size) {
      check(setup, size, 64, size == 8 ? (int)payload : -1);
    }
  }
  _Alignas(4) uint8_t unaligned[12];
  memcpy(unaligned + 1, setup, 8);
  for (unsigned request = 0; request < 2; ++request) {
    unaligned[2] = requests[request];
    check(unaligned + 1, 8, 64, request == 0 ? 32 : (int)sizeof(version) - 1);
  }
  check(NULL, 8, 64, -1);
  assert(chimera_control_read(setup, 8, NULL, 64) == -1);
  ++cases;
  printf("%u request cases passed; no hardware calls\n", cases);
  return 0;
}
