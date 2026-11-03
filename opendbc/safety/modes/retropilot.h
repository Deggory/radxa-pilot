#pragma once

#include "opendbc/safety/declarations.h"

// Canonical ocelot_controls, RetroPilot/opendbc 6b90fafe. Explicit host bus 2
// matches car/retropilot/values.py; it is not a discovery of physical wiring.
// Only disabled commands are qualified here. No active profile, arbitrary
// parameter, incoming message or controls_allowed state may enable actuation.
static safety_config retropilot_init(uint16_t param) {
  static const CanMsg RETROPILOT_TX_MSGS[] = {
    {0x10E, 2, 6, .check_relay = false},  // Brake actuator
    {0x12E, 2, 6, .check_relay = false},  // Steering actuator
    {0x200, 2, 6, .check_relay = false},  // Gas interceptor
    {0x20E, 2, 6, .check_relay = false},  // iBooster
    {0x22E, 2, 5, .check_relay = false},  // SSC steering
    {0x300, 2, 6, .check_relay = false},  // Steering interceptor
    {0x400, 2, 6, .check_relay = false},  // Gas actuator
  };

  // No RX-derived engagement and no forwarding. Unknown parameters allow no TX.
  safety_config ret = {NULL, 0, NULL, 0, true};
  if (param == 0U) {
    ret.tx_msgs = RETROPILOT_TX_MSGS;
    ret.tx_msgs_len = sizeof(RETROPILOT_TX_MSGS) / sizeof(RETROPILOT_TX_MSGS[0]);
  }
  return ret;
}

static bool retropilot_tx_hook(const CANPacket_t *msg) {
  // The dispatcher also enforces address, bus and DLC against the allowlist.
  bool brake = (msg->addr == 0x10EU) || (msg->addr == 0x20EU);
  bool interceptor = (msg->addr == 0x200U) || (msg->addr == 0x300U) || (msg->addr == 0x400U);
  bool steering = (msg->addr == 0x12EU) || (msg->addr == 0x22EU);
  bool valid = (brake || interceptor || steering) &&
               !msg->fd && !msg->extended && !msg->returned && !msg->rejected;
  int counter_byte = interceptor ? 5 : 1;
  uint8_t crc = 0xFFU;

  for (int i = 1; i < GET_LEN(msg); i++) {
    // CRC-8/SAE-J1850: bytes 1..DLC-1, init FF, polynomial 1D, xorout FF.
    crc = crc8_update(crc, msg->data[i], 0x1DU);

    // Engineering zero is offset encoded for brake targets. All modes/ENABLE
    // and reserved bits must be zero; the four counter bits may vary freely.
    uint8_t expected = 0U;
    if (brake) {
      if (i == 3) { expected = 0x7EU; }
      if (i == 4) { expected = 0x40U; }
      if (i == 5) { expected = 0x01U; }
    }
    uint8_t mask = (i == counter_byte) ? 0xF0U : 0xFFU;
    valid = valid && ((msg->data[i] & mask) == expected);
  }

  return valid && (msg->data[0] == (uint8_t)(crc ^ 0xFFU));
}

const safety_hooks retropilot_hooks = {
  .init = retropilot_init,
  .rx = default_rx_hook,
  .tx = retropilot_tx_hook,
};
