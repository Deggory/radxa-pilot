// SPDX-License-Identifier: MIT
#pragma once
#include <stddef.h>
#include <stdint.h>

#define CHIMERA_CAN_HEADER_SIZE 6U
#define CHIMERA_CAN_MAX_WIRE_SIZE 14U
#define CHIMERA_CAN_ERROR (-1)
#define CHIMERA_CAN_MORE 0
#define CHIMERA_CAN_FRAME 1

enum chimera_can_status { CHIMERA_CAN_RECEIVED = 0, CHIMERA_CAN_RETURNED = 1, CHIMERA_CAN_REJECTED = 2 };
typedef struct {
  uint32_t address;
  uint8_t bus, length, extended, status;
  uint8_t data[8];
} chimera_can_frame;

// Per-connection state. Initialize before use; an error stays latched until an
// explicit init after transport/session recovery. No sliding resynchronization.
typedef struct {
  uint8_t bytes[CHIMERA_CAN_MAX_WIRE_SIZE];
  uint8_t used, failed;
} chimera_can_stream;

#ifdef __cplusplus
extern "C" {
#endif
// Pure byte codecs, no peripheral/queue/safety-policy calls. They return the
// complete record length, or ERROR without modifying the destination. TX decode
// accepts only host data records, never board return/reject metadata. Input and
// output buffers must not overlap; wire buffers need only byte alignment.
int chimera_can_encode_rx(const chimera_can_frame *frame, uint8_t *wire, size_t capacity);
int chimera_can_decode_tx(const uint8_t *wire, size_t size, chimera_can_frame *frame);
void chimera_can_stream_init(chimera_can_stream *state);
// Returns FRAME for one validated record, MORE for an incomplete record, ERROR
// for a latched failure. consumed counts input bytes through that result; caller
// retains any remaining input and applies backpressure/policy before continuing.
// Frame is untouched except on FRAME. All arguments/storage must be separate;
// data may be NULL only when size==0. Decoding is not permission to transmit.
int chimera_can_stream_feed(chimera_can_stream *state, const uint8_t *data, size_t size,
                            size_t *consumed, chimera_can_frame *frame);
#ifdef __cplusplus
}
#endif
