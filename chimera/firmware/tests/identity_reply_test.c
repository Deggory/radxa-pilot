// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "protocol.h"

int main(void) {
  uint8_t setup[8] = {0xC0U, CHIMERA_REQUEST_MANIFEST, 0U, 0U, 0U, 0U, 64U, 0U};
  uint8_t reply[64];
  int count = chimera_control_read(setup, sizeof(setup), reply, sizeof(reply));
  assert(count == 32);
  assert(fwrite(reply, 1U, (size_t)count, stdout) == (size_t)count);
  setup[1] = CHIMERA_REQUEST_VERSION;
  count = chimera_control_read(setup, sizeof(setup), reply, sizeof(reply));
  assert(count == 25);
  assert(fwrite(reply, 1U, (size_t)count, stdout) == (size_t)count);
  const uint8_t unavailable[] = {0xC1U, 0xDDU, 0xD2U, 0xC2U, 0xDCU};
  for (size_t i = 0U; i < sizeof(unavailable); ++i) {
    setup[1] = unavailable[i];
    for (size_t j = 0U; j < sizeof(reply); ++j) reply[j] = 0xA5U;
    assert(chimera_control_read(setup, sizeof(setup), reply, sizeof(reply)) == CHIMERA_CONTROL_STALL);
    for (size_t j = 0U; j < sizeof(reply); ++j) assert(reply[j] == 0xA5U);
  }
  return 0;
}
