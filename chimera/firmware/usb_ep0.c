// SPDX-License-Identifier: MIT
#include "usb_ep0.h"
#include "protocol.h"

static const uint8_t device[] = {18, 1, 0, 2, 0, 0, 0, 64, 0xAA, 0xBB, 0xCC, 0xDD, 0, 1, 1, 2, 3, 1};
static const uint8_t config[] = {9, 2, 18, 0, 1, 1, 0, 0x80, 0, 9, 4, 0, 0, 0, 0xFF, 0, 0, 0};
static const uint8_t language[] = {4, 3, 9, 4};
static const uint8_t manufacturer[] = {22, 3, 'R', 0, 'e', 0, 't', 0, 'r', 0, 'o', 0,
                                      'P', 0, 'i', 0, 'l', 0, 'o', 0, 't', 0};

static bool advance(chimera_usb_ep0 *state) {
  if (state->generation == UINT32_MAX) { state->initialized = 0U; return false; }
  ++state->generation;
  return true;
}

void chimera_usb_ep0_reset(chimera_usb_ep0 *state) {
  if (state != NULL) {
    state->address = 0U;
    state->configuration = 0U;
    state->phase = CHIMERA_EP0_IDLE;
    state->pending_kind = 0U;
    state->pending_value = 0U;
    if (!advance(state)) state->phase = CHIMERA_EP0_STALL;
  }
}
bool chimera_usb_ep0_init(chimera_usb_ep0 *state, const uint8_t *uid,
                          uint8_t self_powered, uint8_t max_power_2ma) {
  if (state == NULL) return false;
  state->generation = 0U;
  chimera_usb_ep0_reset(state);
  state->initialized = 0U;
  state->self_powered = 0U;
  state->max_power_2ma = 0U;
  for (unsigned i = 0U; i < 50U; ++i) state->serial[i] = 0U;
  if (uid == NULL || self_powered > 1U || max_power_2ma > 250U) return false;
  uint8_t any = 0U, all = 255U;
  for (unsigned i = 0U; i < 12U; ++i) { any |= uid[i]; all &= uid[i]; }
  if (any == 0U || all == 255U) return false;
  const char *hex = "0123456789abcdef";
  state->serial[0] = 50U;
  state->serial[1] = 3U;
  for (unsigned i = 0U; i < 12U; ++i) {
    state->serial[2U + i * 4U] = (uint8_t)hex[uid[i] >> 4];
    state->serial[4U + i * 4U] = (uint8_t)hex[uid[i] & 15U];
  }
  state->self_powered = self_powered;
  state->max_power_2ma = max_power_2ma;
  state->initialized = 1U;
  return true;
}

int chimera_usb_ep0_setup(chimera_usb_ep0 *state, const uint8_t *setup, size_t setup_size,
                          uint8_t *reply, size_t capacity) {
  if (state == NULL || state->initialized != 1U) return -1;
  state->phase = CHIMERA_EP0_STALL;
  state->pending_kind = 0U;
  state->pending_value = 0U;
  if (!advance(state)) return -1;
  if (setup == NULL || setup_size != 8U) return -1;
  const uint16_t value = (uint16_t)setup[2] | ((uint16_t)setup[3] << 8);
  const uint16_t index = (uint16_t)setup[4] | ((uint16_t)setup[5] << 8);
  const uint16_t length = (uint16_t)setup[6] | ((uint16_t)setup[7] << 8);
  if (setup[0] == 0xC0U) {
    if (state->configuration != 1U) return -1;
    int result = chimera_control_read(setup, setup_size, reply, capacity);
    if (result >= 0) state->phase = CHIMERA_EP0_DATA_IN;
    return result;
  }
  const uint8_t *data = NULL;
  size_t size = 0U;
  uint8_t small[2];
  small[0] = 0U;
  small[1] = 0U;
  bool ascii = false, configuration_descriptor = false;
  switch (((unsigned)setup[0] << 8) | setup[1]) {
    case 0x8006: // GET_DESCRIPTOR: full-speed only, one control-only interface.
      switch (value) {
        case 0x0100: if (index != 0U) return -1; data = device; size = sizeof(device); break;
        case 0x0200:
          if (index != 0U) return -1;
          data = config; size = sizeof(config); configuration_descriptor = true; break;
        case 0x0300: if (index != 0U) return -1; data = language; size = sizeof(language); break;
        case 0x0301: if (index != 0x0409U) return -1; data = manufacturer; size = sizeof(manufacturer); break;
        case 0x0302:
          if (index != 0x0409U) return -1;
          data = (const uint8_t *)chimera_usb_product;
          while (size < 31U && data[size] != 0U) ++size;
          if (size == 31U) return -1;
          size = size * 2U + 2U; ascii = true; break;
        case 0x0303: if (index != 0x0409U) return -1; data = state->serial; size = 50U; break;
        default: return -1;
      }
      break;
    case 0x0005: // SET_ADDRESS: do not commit before the status packet succeeds.
      if (value > 127U || index != 0U || length != 0U || state->configuration != 0U) return -1;
      state->pending_kind = 1U; state->pending_value = (uint8_t)value; break;
    case 0x0009: // SET_CONFIGURATION.
      if (state->address == 0U || value > 1U || index != 0U || length != 0U) return -1;
      state->pending_kind = 2U; state->pending_value = (uint8_t)value; break;
    case 0x8008: // GET_CONFIGURATION.
      if (state->address == 0U || value != 0U || index != 0U || length != 1U) return -1;
      small[0] = state->configuration; data = small; size = 1U; break;
    case 0x8000: // GET_STATUS, device. No remote-wake capability.
      if (state->address == 0U || value != 0U || index != 0U || length != 2U) return -1;
      small[0] = state->self_powered; data = small; size = 2U; break;
    case 0x8100: // GET_STATUS, sole interface.
      if (state->configuration != 1U || value != 0U || index != 0U || length != 2U) return -1;
      data = small; size = 2U; break;
    case 0x8200: // GET_STATUS, control endpoint only; SETUP clears its STALL.
      if (state->address == 0U || value != 0U || (index != 0U && index != 0x80U) || length != 2U) return -1;
      data = small; size = 2U; break;
    case 0x810A: // GET_INTERFACE.
      if (state->configuration != 1U || value != 0U || index != 0U || length != 1U) return -1;
      data = small; size = 1U; break;
    case 0x010B: // SET_INTERFACE, alt0 only, no non-control endpoints to reset.
      if (state->configuration != 1U || value != 0U || index != 0U || length != 0U) return -1;
      break;
    default: return -1;
  }
  const size_t full_size = size;
  if (size > length) size = length;
  if (size > capacity || (size != 0U && reply == NULL)) {
    state->pending_kind = 0U;
    return -1;
  }
  for (size_t i = 0U; i < size; ++i) {
    if (!ascii) reply[i] = data[i];
    else if (i == 0U) reply[i] = (uint8_t)full_size;
    else if (i == 1U) reply[i] = 3U;
    else reply[i] = (i & 1U) ? 0U : data[(i - 2U) / 2U];
  }
  if (configuration_descriptor && size > 7U) reply[7] = (uint8_t)(0x80U | (state->self_powered << 6));
  if (configuration_descriptor && size > 8U) reply[8] = state->max_power_2ma;
  state->phase = length == 0U ? CHIMERA_EP0_STATUS_IN : CHIMERA_EP0_DATA_IN;
  return (int)size;
}

bool chimera_usb_ep0_in_complete(chimera_usb_ep0 *state, uint32_t generation) {
  if (state == NULL || state->initialized != 1U || generation != state->generation) return false;
  if (state->phase == CHIMERA_EP0_DATA_IN) { state->phase = CHIMERA_EP0_STATUS_OUT; return true; }
  if (state->phase != CHIMERA_EP0_STATUS_IN) return false;
  if (state->pending_kind == 1U) { state->address = state->pending_value; state->configuration = 0U; }
  if (state->pending_kind == 2U) state->configuration = state->pending_value;
  state->pending_kind = 0U;
  state->phase = CHIMERA_EP0_IDLE;
  return true;
}
bool chimera_usb_ep0_out_complete(chimera_usb_ep0 *state, uint32_t generation, size_t size) {
  if (state == NULL || state->initialized != 1U || generation != state->generation) return false;
  if (state->phase == CHIMERA_EP0_STATUS_OUT && size == 0U) { state->phase = CHIMERA_EP0_IDLE; return true; }
  state->pending_kind = 0U;
  state->phase = CHIMERA_EP0_STALL;
  return false;
}
