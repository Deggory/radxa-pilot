// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "can_codec.h"
// Reference is the project's actual packed wire header, used only by tests.
#include "can.h"

static unsigned vectors, splits, corruptions, headers, fuzz_cases, collisions;
static uint8_t stream_bytes[4096];
static chimera_can_frame stream_frames[256];
static size_t stream_size, stream_count;

static uint8_t xor_bytes(const uint8_t *data, size_t size) {
  uint8_t value = 0;
  for (size_t i = 0; i < size; ++i) value ^= data[i];
  return value;
}

static void repair(uint8_t *wire, size_t size) {
  wire[5] = 0;
  wire[5] = xor_bytes(wire, size);
}

static void unchanged(const chimera_can_frame *frame) {
  const uint8_t *bytes = (const uint8_t *)frame;
  for (size_t i = 0; i < sizeof(*frame); ++i) assert(bytes[i] == 0xA5);
}

static void check_rejected(const uint8_t *wire, size_t size) {
  chimera_can_frame out;
  memset(&out, 0xA5, sizeof(out));
  assert(chimera_can_decode_tx(wire, size, &out) == -1);
  unchanged(&out);
}

static void check_splits(const uint8_t *wire, size_t size, const chimera_can_frame *frame) {
  for (size_t split = 0; split <= size; ++split) {
    chimera_can_stream state;
    chimera_can_stream_init(&state);
    chimera_can_frame out;
    memset(&out, 0xA5, sizeof(out));
    size_t consumed = 99;
    int result = chimera_can_stream_feed(&state, wire, split, &consumed, &out);
    assert(consumed == split);
    if (split < size) {
      assert(result == CHIMERA_CAN_MORE);
      unchanged(&out);
      result = chimera_can_stream_feed(&state, wire + split, size - split, &consumed, &out);
      assert(consumed == size - split);
    }
    assert(result == CHIMERA_CAN_FRAME);
    assert(memcmp(&out, frame, sizeof(out)) == 0);
    assert(!state.failed && state.used == 0);
    ++splits;
  }
}

static void vector(chimera_can_frame frame) {
  CANPacket_t expected = {0};
  expected.bus = frame.bus;
  expected.data_len_code = frame.length;
  expected.extended = frame.extended;
  expected.addr = frame.address;
  expected.returned = frame.status == CHIMERA_CAN_RETURNED;
  expected.rejected = frame.status == CHIMERA_CAN_REJECTED;
  for (unsigned i = 0; i < frame.length; ++i) {
    frame.data[i] = (uint8_t)(0x31 + i * 17 + frame.length * 3 + frame.bus);
    expected.data[i] = frame.data[i];
  }
  const size_t size = 6 + frame.length;
  expected.checksum = xor_bytes((const uint8_t *)&expected, size);
  uint8_t guarded[30];
  memset(guarded, 0xA5, sizeof(guarded));
  assert(chimera_can_encode_rx(&frame, guarded + 8, 14) == (int)size);
  assert(memcmp(guarded + 8, &expected, size) == 0);
  for (size_t i = 0; i < sizeof(guarded); ++i) {
    if (i < 8 || i >= 8 + size) assert(guarded[i] == 0xA5);
  }
  const uint8_t *wire = guarded + 8;
  printf("V %x %u %u %u %u ", frame.address, frame.bus, frame.length, frame.extended, frame.status);
  for (size_t i = 0; i < size; ++i) printf("%02x", wire[i]);
  putchar('\n');
  ++vectors;
  if (frame.status != CHIMERA_CAN_RECEIVED) {
    check_rejected(wire, size); // Host TX cannot supply board echo metadata.
    return;
  }
  chimera_can_frame out;
  assert(chimera_can_decode_tx(wire, size, &out) == (int)size);
  assert(memcmp(&out, &frame, sizeof(out)) == 0);
  check_splits(wire, size, &frame);
  for (size_t bit = 0; bit < size * 8; ++bit) {
    uint8_t damaged[14];
    memcpy(damaged, wire, size);
    damaged[bit / 8] ^= 1U << (bit % 8);
    check_rejected(damaged, size);
    ++corruptions;
  }
  assert(stream_size + size <= sizeof(stream_bytes));
  assert(stream_count < sizeof(stream_frames) / sizeof(stream_frames[0]));
  memcpy(stream_bytes + stream_size, wire, size);
  stream_size += size;
  stream_frames[stream_count++] = frame;
}

static void multiple_chunks(void) {
  for (size_t chunk = 1; chunk <= stream_size; ++chunk) {
    chimera_can_stream state;
    chimera_can_stream_init(&state);
    size_t position = 0, frames = 0;
    while (position < stream_size) {
      const size_t end = position + chunk < stream_size ? position + chunk : stream_size;
      while (position < end) {
        size_t consumed;
        chimera_can_frame out;
        int result = chimera_can_stream_feed(&state, stream_bytes + position, end - position, &consumed, &out);
        assert(result != CHIMERA_CAN_ERROR && consumed > 0 && consumed <= end - position);
        position += consumed;
        if (result == CHIMERA_CAN_FRAME) {
          assert(frames < stream_count && memcmp(&out, &stream_frames[frames++], sizeof(out)) == 0);
        }
      }
    }
    assert(frames == stream_count && state.used == 0 && !state.failed);
    ++splits;
  }
}

static void errors(void) {
  const uint8_t golden[] = {0x34, 0x18, 0x09, 0, 0, 0x25, 0x11, 0x22, 0x33};
  chimera_can_frame frame;
  assert(chimera_can_decode_tx(golden, sizeof(golden), &frame) == 9);
  assert(frame.address == 0x123 && frame.bus == 2 && frame.length == 3 && !frame.extended);
  for (size_t capacity = 0; capacity < sizeof(golden); ++capacity) {
    uint8_t wire[14];
    memset(wire, 0xA5, sizeof(wire));
    assert(chimera_can_encode_rx(&frame, wire, capacity) == -1);
    for (unsigned i = 0; i < sizeof(wire); ++i) assert(wire[i] == 0xA5);
  }
  for (unsigned bad = 0; bad < 6; ++bad) {
    chimera_can_frame invalid = frame;
    if (bad == 0) invalid.address = 0x20000000U;
    if (bad == 1) invalid.address = 0x800U;
    if (bad == 2) invalid.bus = 3;
    if (bad == 3) invalid.length = 9;
    if (bad == 4) invalid.extended = 2;
    if (bad == 5) invalid.status = 3;
    uint8_t wire[14];
    memset(wire, 0xA5, sizeof(wire));
    assert(chimera_can_encode_rx(&invalid, wire, sizeof(wire)) == -1);
    for (unsigned i = 0; i < sizeof(wire); ++i) assert(wire[i] == 0xA5);
  }
  uint8_t wire[20] = {0};
  memcpy(wire, golden, sizeof(golden));
  for (size_t size = 0; size <= sizeof(wire); ++size) if (size != sizeof(golden)) check_rejected(wire, size);
  check_rejected(NULL, sizeof(golden));
  assert(chimera_can_decode_tx(golden, sizeof(golden), NULL) == -1);
  assert(chimera_can_encode_rx(NULL, wire, sizeof(wire)) == -1);
  assert(chimera_can_encode_rx(&frame, NULL, sizeof(wire)) == -1);

  // A valid checksum cannot turn a non-extended 12-bit ID into a standard ID.
  uint8_t bad_standard[6] = {0, 0, 0x40, 0, 0, 0}; // addr0x800, extended0.
  repair(bad_standard, sizeof(bad_standard));
  check_rejected(bad_standard, sizeof(bad_standard));
  chimera_can_stream invalid_header;
  chimera_can_stream_init(&invalid_header);
  size_t read_header;
  assert(chimera_can_stream_feed(&invalid_header, bad_standard, sizeof(bad_standard), &read_header, &frame) == CHIMERA_CAN_ERROR);
  assert(invalid_header.failed && read_header == 6);

  // Cross-check all first-two-header-byte combinations against actual bitfields.
  for (unsigned bits = 0; bits < 65536; ++bits) {
    uint8_t packet[14] = {bits & 255U, bits >> 8};
    CANPacket_t reference = {0};
    memcpy(&reference, packet, 6);
    const size_t size = reference.data_len_code <= 8 ? 6 + reference.data_len_code : 14;
    repair(packet, size);
    const int valid = !reference.fd && reference.bus < 3 && reference.data_len_code <= 8 &&
                      !reference.returned && !reference.rejected && (reference.extended || reference.addr <= 0x7FF);
    assert((chimera_can_decode_tx(packet, size, &frame) > 0) == valid);
    ++headers;
  }

  // Checksum corruption latches an error; a following good record cannot recover.
  memcpy(wire, golden, sizeof(golden));
  wire[8] ^= 1;
  chimera_can_stream state;
  chimera_can_stream_init(&state);
  size_t consumed;
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_FRAME);
  memset(&frame, 0xA5, sizeof(frame));
  assert(chimera_can_stream_feed(&state, wire, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_ERROR);
  assert(state.failed && consumed == sizeof(golden));
  unchanged(&frame);
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_ERROR);
  assert(consumed == 0);
  unchanged(&frame);
  chimera_can_stream_init(&state);
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_FRAME);
  chimera_can_stream_init(&state);
  assert(chimera_can_stream_feed(&state, golden, 4, &consumed, &frame) == CHIMERA_CAN_MORE);
  chimera_can_stream_init(&state); // New session discards a partial old header.
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_FRAME);
  assert(chimera_can_stream_feed(&state, NULL, 0, &consumed, &frame) == CHIMERA_CAN_MORE && consumed == 0);
  assert(chimera_can_stream_feed(&state, NULL, 1, &consumed, &frame) == CHIMERA_CAN_ERROR && consumed == 0);
  assert(chimera_can_stream_feed(NULL, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_ERROR);
  chimera_can_stream_init(&state);
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), NULL, &frame) == CHIMERA_CAN_ERROR && state.failed);
  chimera_can_stream_init(&state);
  assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, NULL) == CHIMERA_CAN_ERROR && state.failed);
  for (unsigned used = 14; used <= 255; ++used) {
    chimera_can_stream_init(&state);
    state.used = used;
    assert(chimera_can_stream_feed(&state, golden, sizeof(golden), &consumed, &frame) == CHIMERA_CAN_ERROR);
    assert(state.failed && consumed == 0);
  }
}

static void xor_limits(void) {
  // Matching the current format means XOR is not authentication. Balanced data
  // changes can pass; a changed DLC can also create a valid shorter prefix.
  uint8_t balanced[] = {0x34, 0x18, 0x09, 0, 0, 0x25, 0x10, 0x23, 0x33};
  chimera_can_frame frame;
  assert(chimera_can_decode_tx(balanced, sizeof(balanced), &frame) == 9);
  assert(frame.data[0] == 0x10 && frame.data[1] == 0x23);
  ++collisions;
  uint8_t changed_dlc[] = {0x10, 0, 0, 0, 0, 0, 0x10};
  assert(chimera_can_decode_tx(changed_dlc, sizeof(changed_dlc), &frame) == 7);
  changed_dlc[0] ^= 0x10;
  check_rejected(changed_dlc, sizeof(changed_dlc)); // Exact record size rejects.
  chimera_can_stream state;
  chimera_can_stream_init(&state);
  size_t consumed;
  assert(chimera_can_stream_feed(&state, changed_dlc, sizeof(changed_dlc), &consumed, &frame) == CHIMERA_CAN_FRAME);
  assert(consumed == 6 && frame.length == 0 && frame.address == 0);
  assert(chimera_can_stream_feed(&state, changed_dlc + consumed, 1, &consumed, &frame) == CHIMERA_CAN_MORE);
  assert(state.used == 1);
  ++collisions;
}

static void fuzz(void) {
  uint32_t random = 0x12345678U;
  for (unsigned i = 0; i < 10000; ++i) {
    uint8_t bytes[80];
    for (unsigned j = 0; j < sizeof(bytes); ++j) {
      random = random * 1664525U + 1013904223U;
      bytes[j] = random >> 24;
    }
    chimera_can_stream state;
    chimera_can_stream_init(&state);
    chimera_can_frame out;
    memset(&out, 0xA5, sizeof(out));
    size_t consumed;
    int result = chimera_can_stream_feed(&state, bytes, i % sizeof(bytes), &consumed, &out);
    assert(consumed <= i % sizeof(bytes) && consumed <= 14);
    if (result == CHIMERA_CAN_FRAME) {
      chimera_can_frame reference;
      assert(chimera_can_decode_tx(bytes, consumed, &reference) > 0);
      assert(memcmp(&out, &reference, sizeof(out)) == 0);
    } else {
      unchanged(&out);
      assert(result == CHIMERA_CAN_MORE || state.failed);
    }
    ++fuzz_cases;
  }
}

int main(void) {
  _Static_assert(sizeof(chimera_can_frame) == 16, "frame ABI");
  const uint32_t addresses[] = {0, 1, 0x123, 0x7FF, 0x800, 0x1234567, 0x1FFFFFFF, 0x123};
  for (unsigned a = 0; a < 8; ++a) {
    for (unsigned bus = 0; bus < 3; ++bus) {
      for (unsigned len = 0; len <= 8; ++len) {
        for (unsigned status = 0; status <= 2; ++status) {
          chimera_can_frame frame = {.address = addresses[a], .bus = bus, .length = len,
            .extended = a == 7 || addresses[a] >= 0x800, .status = status};
          vector(frame);
        }
      }
    }
  }
  multiple_chunks();
  errors();
  xor_limits();
  fuzz();
  printf("SUMMARY vectors=%u splits=%u corruptions=%u headers=%u fuzz=%u known_xor_collisions=%u\n",
         vectors, splits, corruptions, headers, fuzz_cases, collisions);
  return 0;
}
