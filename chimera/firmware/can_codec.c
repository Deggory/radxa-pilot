// SPDX-License-Identifier: MIT
#include "can_codec.h"

static uint32_t word_le(const uint8_t *data) {
  return (uint32_t)data[0] | ((uint32_t)data[1] << 8) |
         ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
}

static uint8_t checksum(const uint8_t *data, size_t size) {
  uint8_t result = 0U;
  for (size_t i = 0U; i < size; ++i) result ^= data[i];
  return result;
}

static int valid_tx_header(const uint8_t *wire) {
  return (wire[0] & 1U) == 0U && ((wire[0] >> 1) & 7U) < 3U &&
         (wire[0] >> 4) <= 8U && (wire[1] & 3U) == 0U &&
         ((wire[1] & 4U) != 0U || (word_le(wire + 1) >> 3) <= 0x7FFU);
}

int chimera_can_encode_rx(const chimera_can_frame *frame, uint8_t *wire, size_t capacity) {
  if (frame == NULL || wire == NULL || frame->bus >= 3U || frame->length > 8U ||
      frame->extended > 1U || frame->status > CHIMERA_CAN_REJECTED || frame->address > 0x1FFFFFFFU ||
      (frame->extended == 0U && frame->address > 0x7FFU) ||
      capacity < CHIMERA_CAN_HEADER_SIZE + frame->length) return CHIMERA_CAN_ERROR;

  const uint32_t flags = frame->status == CHIMERA_CAN_RETURNED ? 2U :
                         frame->status == CHIMERA_CAN_REJECTED ? 1U : 0U;
  const uint32_t word = (frame->address << 3) | ((uint32_t)frame->extended << 2) | flags;
  wire[0] = (uint8_t)((frame->length << 4) | (frame->bus << 1));
  for (unsigned i = 0U; i < 4U; ++i) wire[1U + i] = (uint8_t)(word >> (i * 8U));
  for (unsigned i = 0U; i < frame->length; ++i) wire[6U + i] = frame->data[i];
  wire[5] = checksum(wire, 5U) ^ checksum(frame->data, frame->length);
  return (int)(CHIMERA_CAN_HEADER_SIZE + frame->length);
}

int chimera_can_decode_tx(const uint8_t *wire, size_t size, chimera_can_frame *frame) {
  if (wire == NULL || frame == NULL || size < CHIMERA_CAN_HEADER_SIZE || size > CHIMERA_CAN_MAX_WIRE_SIZE ||
      !valid_tx_header(wire) || size != CHIMERA_CAN_HEADER_SIZE + (wire[0] >> 4) ||
      checksum(wire, size) != 0U) return CHIMERA_CAN_ERROR;

  // All validation precedes destination writes. Explicit member/data stores
  // avoid a compiler-emitted libc memset for aggregate initialization on ARM.
  frame->address = word_le(wire + 1) >> 3;
  frame->bus = (wire[0] >> 1) & 7U;
  frame->length = wire[0] >> 4;
  frame->extended = (wire[1] >> 2) & 1U;
  frame->status = CHIMERA_CAN_RECEIVED;
  for (unsigned i = 0U; i < 8U; ++i) frame->data[i] = i < frame->length ? wire[6U + i] : 0U;
  return (int)size;
}

void chimera_can_stream_init(chimera_can_stream *state) {
  if (state != NULL) {
    for (unsigned i = 0U; i < CHIMERA_CAN_MAX_WIRE_SIZE; ++i) state->bytes[i] = 0U;
    state->used = 0U;
    state->failed = 0U;
  }
}

static int stream_error(chimera_can_stream *state) {
  if (state != NULL) {
    state->used = 0U;
    state->failed = 1U;
  }
  return CHIMERA_CAN_ERROR;
}

int chimera_can_stream_feed(chimera_can_stream *state, const uint8_t *data, size_t size,
                            size_t *consumed, chimera_can_frame *frame) {
  if (consumed != NULL) *consumed = 0U;
  if (state == NULL || consumed == NULL || frame == NULL || (data == NULL && size != 0U)) return stream_error(state);
  if (state->failed != 0U) return CHIMERA_CAN_ERROR;
  if (state->used >= CHIMERA_CAN_MAX_WIRE_SIZE) return stream_error(state);
  if (state->used >= CHIMERA_CAN_HEADER_SIZE &&
      (!valid_tx_header(state->bytes) || state->used >= CHIMERA_CAN_HEADER_SIZE + (state->bytes[0] >> 4))) {
    return stream_error(state);
  }
  while (*consumed < size) {
    state->bytes[state->used++] = data[(*consumed)++];
    if (state->used < CHIMERA_CAN_HEADER_SIZE) continue;
    if (!valid_tx_header(state->bytes)) return stream_error(state);
    if (state->used == CHIMERA_CAN_HEADER_SIZE + (state->bytes[0] >> 4)) {
      if (chimera_can_decode_tx(state->bytes, state->used, frame) < 0) return stream_error(state);
      state->used = 0U;
      return CHIMERA_CAN_FRAME;
    }
  }
  return CHIMERA_CAN_MORE;
}
