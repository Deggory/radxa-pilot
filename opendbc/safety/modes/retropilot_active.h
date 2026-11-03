#pragma once

// Parameterized canonical interceptor/iBooster policy. Raw counts are NOT Nm
// or acceleration. A measured endpoint/vehicle contract must supply every
// limit; no production initializer supplies one. See the parent retropilot.h.
typedef struct {
  int steer_center1;
  int steer_center2;
  int steer_max;
  int steer_high_speed_max;
  int steer_up;
  int steer_down;
  int steer_rt_delta;
  int gas_offset1;
  int gas_offset2;
  int gas_range1;
  int gas_range2;
  int gas_step;
  int gas_driver_threshold;
  int brake_max;  // position counts above engineering zero (raw 320)
  int brake_step;
  int speed_divisor;  // raw CAN_SPEED / divisor = km/h, explicitly 1 or 100
  int speed_mode;  // qualified producer's source-selection nibble, not units
  int max_speed_kph;
  int angle_max;  // raw 0.1 degree counts
  int angle_rate_max;  // deg/s
  uint32_t rx_timeout;
  uint32_t steer_interval;
  uint32_t gas_interval;
  uint32_t brake_interval;
} RetroPilotSafetyLimits;

typedef struct {
  int value;
  uint8_t counter;
  bool seen;
  uint32_t timestamp;
  uint8_t release_samples;
} RetroPilotCommand;

static RetroPilotSafetyLimits retropilot_limits;
static bool retropilot_profile_valid = false;
static bool retropilot_engaged = false;
static bool retropilot_available = false;
static bool retropilot_buttons_ready = false;
static uint8_t retropilot_buttons = 0U;
static bool retropilot_ignition = false;
static bool retropilot_engine_brake = false;
static bool retropilot_driver_brake = false;
static bool retropilot_driver_gas = false;
static bool retropilot_override = false;
static int retropilot_speed = 0;
static uint8_t retropilot_rx_samples[7];
static uint8_t retropilot_rx_counters[7];
static uint32_t retropilot_rx_timestamps[7];
static RetroPilotCommand retropilot_commands[3];  // steer, gas, brake
static int retropilot_rt_value = 0;
static uint32_t retropilot_rt_timestamp = 0U;

static bool retropilot_limits_valid(const RetroPilotSafetyLimits *p) {
  return (p != NULL) &&
    (p->steer_max > 0) && (p->steer_max <= 1000) &&
    (p->steer_center1 >= p->steer_max) && (p->steer_center1 <= (32767 - p->steer_max)) &&
    (p->steer_center2 >= p->steer_max) && (p->steer_center2 <= (32767 - p->steer_max)) &&
    (p->steer_high_speed_max > 0) && (p->steer_high_speed_max <= p->steer_max) &&
    (p->steer_up > 0) && (p->steer_up <= p->steer_max) &&
    (p->steer_down > 0) && (p->steer_down <= p->steer_max) &&
    (p->steer_rt_delta >= p->steer_up) && (p->steer_rt_delta <= p->steer_max) &&
    (p->gas_offset1 >= 0) && (p->gas_offset2 >= 0) &&
    (p->gas_range1 > 0) && (p->gas_range1 <= 32767) &&
    (p->gas_range2 > 0) && (p->gas_range2 <= 32767) &&
    (p->gas_offset1 <= (65535 - p->gas_range1)) && (p->gas_offset2 <= (65535 - p->gas_range2)) &&
    (p->gas_step > 0) && (p->gas_step <= p->gas_range1) &&
    (p->gas_driver_threshold >= 0) && (p->gas_driver_threshold < 65535) &&
    (p->brake_max > 0) && (p->brake_max <= 3775) &&
    (p->brake_step > 0) && (p->brake_step <= p->brake_max) &&
    ((p->speed_divisor == 1) || (p->speed_divisor == 100)) &&
    (p->speed_mode >= 0) && (p->speed_mode <= 15) &&
    (p->max_speed_kph > 0) && (p->max_speed_kph <= 300) &&
    (p->angle_max > 0) && (p->angle_max <= 32767) &&
    (p->angle_rate_max > 0) && (p->angle_rate_max <= 65535) &&
    (p->rx_timeout >= 10000U) && (p->rx_timeout <= 1000000U) &&
    (p->steer_interval >= 1000U) && (p->steer_interval <= p->rx_timeout) &&
    (p->gas_interval >= 1000U) && (p->gas_interval <= p->rx_timeout) &&
    (p->brake_interval >= 1000U) && (p->brake_interval <= p->rx_timeout);
}

static void retropilot_disengage(bool fault) {
  controls_allowed = false;
  retropilot_engaged = false;
  if (fault) {
    retropilot_available = false;
    retropilot_buttons_ready = false;
  }
  // Retain accepted command values until explicit releases. Clearing them
  // here could conceal outstanding gas when braking (or vice versa) resumes.
}

static safety_config retropilot_profile_init(const RetroPilotSafetyLimits *profile, uint16_t param) {
  static RxCheck checks[] = {
    {.msg = {{0x50, 2, 6, 20, .max_counter = 15U}}},
    {.msg = {{0x75, 2, 8, 20, .max_counter = 15U}}},
    {.msg = {{0x76, 2, 8, 20, .max_counter = 15U}}},
    {.msg = {{0x100, 2, 8, 20, .max_counter = 15U}}},
    {.msg = {{0x301, 2, 8, 20, .max_counter = 15U}}},
    {.msg = {{0x201, 2, 6, 20, .max_counter = 15U}}},
    {.msg = {{0x20F, 2, 5, 20, .max_counter = 15U}}},
  };
  safety_config cfg = retropilot_restricted_init(param);
  retropilot_profile_valid = (param == 0U) && retropilot_limits_valid(profile);
  retropilot_disengage(true);
  retropilot_buttons = 0U;
  retropilot_ignition = false;
  retropilot_engine_brake = false;
  retropilot_driver_brake = false;
  retropilot_driver_gas = false;
  retropilot_override = false;
  retropilot_speed = 0;
  retropilot_rt_value = 0;
  retropilot_rt_timestamp = microsecond_timer_get();
  for (int i = 0; i < 7; i++) {
    checks[i].status = (RxStatus){0};
    retropilot_rx_samples[i] = 0U;
    retropilot_rx_counters[i] = 0U;
    retropilot_rx_timestamps[i] = 0U;
  }
  for (int i = 0; i < 3; i++) {
    retropilot_commands[i] = (RetroPilotCommand){0};
  }
  if (retropilot_profile_valid) {
    retropilot_limits = *profile;
    cfg.rx_checks = checks;
    cfg.rx_checks_len = 7;
  }
  return cfg;
}

static uint32_t retropilot_get_checksum(const CANPacket_t *msg) {
  return msg->data[0];
}

static uint32_t retropilot_compute_checksum(const CANPacket_t *msg) {
  uint8_t crc = 0xFFU;
  for (int i = 1; i < GET_LEN(msg); i++) {
    crc = crc8_update(crc, msg->data[i], 0x1DU);
  }
  return crc ^ 0xFFU;
}

static uint8_t retropilot_get_counter(const CANPacket_t *msg) {
  int index = 7;
  if ((msg->addr == 0x50U) || (msg->addr == 0x201U)) { index = 5; }
  if (msg->addr == 0x20FU) { index = 1; }
  return msg->data[index] & 0xFU;
}

static int retropilot_word(const CANPacket_t *msg, int index) {
  return msg->data[index] | (msg->data[index + 1] << 8);
}

static bool retropilot_quality_valid(const CANPacket_t *msg) {
  bool valid = retropilot_profile_valid && !msg->fd && !msg->extended && !msg->returned && !msg->rejected &&
    (retropilot_get_checksum(msg) == retropilot_compute_checksum(msg));
  if (msg->addr == 0x50U) {
    valid = valid && ((msg->data[5] >> 4) == 1U) &&
      (SAFETY_ABS(to_signed(retropilot_word(msg, 1), 16)) <= retropilot_limits.angle_max) &&
      (retropilot_word(msg, 3) <= retropilot_limits.angle_rate_max);
  }
  if ((msg->addr == 0x301U) || (msg->addr == 0x201U)) {
    valid = valid && ((msg->data[GET_LEN(msg) - 1] >> 4) == 0U);
  }
  if (msg->addr == 0x20FU) {
    valid = valid && ((msg->data[1] >> 4) == 0U) && ((msg->data[2] & 1U) != 0U) && (msg->data[4] == 0U);
  }
  if (msg->addr == 0x76U) {
    valid = valid && ((int)(msg->data[7] >> 4) == retropilot_limits.speed_mode) &&
      (retropilot_word(msg, 5) <= (retropilot_limits.max_speed_kph * retropilot_limits.speed_divisor));
  }
  if ((msg->addr == 0x75U) || (msg->addr == 0x100U)) {
    // Reviewed canonical producer writes NO_FAULT=0 here. SPEED's nibble
    // describes its source instead and is matched explicitly above.
    valid = valid && ((msg->data[7] >> 4) == 0U);
  }
  // The framework skips rx_hook for corrupt/invalid packets. Latch the fault
  // here (called for every matched RX), independently of controls_allowed.
  // Otherwise another user of that shared flag could mask a transient fault
  // before the next valid RX. Requalify this sensor with two clean samples.
  if (!valid) {
    retropilot_disengage(true);
    for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
      if ((unsigned int)current_safety_config.rx_checks[i].msg[0].addr == msg->addr) {
        retropilot_rx_samples[i] = 0U;
      }
    }
  }
  return valid;
}

static bool retropilot_healthy(void) {
  bool healthy = retropilot_profile_valid && retropilot_ignition &&
    !retropilot_engine_brake && !retropilot_driver_brake && !retropilot_driver_gas && !retropilot_override;
  uint32_t now = microsecond_timer_get();
  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    const RxStatus *s = &current_safety_config.rx_checks[i].status;
    healthy = healthy && (retropilot_rx_samples[i] >= 2U) && s->valid_checksum &&
      s->valid_quality_flag && (s->wrong_counters == 0) &&
      (safety_get_ts_elapsed(now, retropilot_rx_timestamps[i]) <= retropilot_limits.rx_timeout);
  }
  return healthy;
}

static void retropilot_rx_hook(const CANPacket_t *msg) {
  uint32_t now = microsecond_timer_get();
  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    const CanMsgCheck *check = &current_safety_config.rx_checks[i].msg[0];
    if (msg_matches(msg, check->addr, check->bus, check->len)) {
      uint8_t counter = retropilot_get_counter(msg);
      bool sequential = counter == ((retropilot_rx_counters[i] + 1U) & 0xFU);
      bool timely = safety_get_ts_elapsed(now, retropilot_rx_timestamps[i]) <= retropilot_limits.rx_timeout;
      if ((retropilot_rx_samples[i] != 0U) && (!sequential || !timely)) {
        retropilot_disengage(true);
        retropilot_rx_samples[i] = 0U;
      }
      retropilot_rx_samples[i] = SAFETY_MIN(retropilot_rx_samples[i] + 1U, 2U);
      retropilot_rx_counters[i] = counter;
      retropilot_rx_timestamps[i] = now;
    }
  }
  if (msg->addr == 0x75U) {
    retropilot_ignition = (msg->data[4] & 1U) != 0U;
    retropilot_engine_brake = (msg->data[4] & 2U) != 0U;
  }
  if (msg->addr == 0x76U) {
    retropilot_speed = retropilot_word(msg, 5);
    vehicle_moving = retropilot_speed != 0;
    UPDATE_VEHICLE_SPEED(((float)retropilot_speed / (float)retropilot_limits.speed_divisor) * KPH_TO_MS);
  }
  if (msg->addr == 0x301U) { retropilot_override = (msg->data[5] & 1U) != 0U; }
  if (msg->addr == 0x201U) {
    retropilot_driver_gas = (retropilot_word(msg, 1) > retropilot_limits.gas_driver_threshold) ||
                           (retropilot_word(msg, 3) > retropilot_limits.gas_driver_threshold);
  }
  if (msg->addr == 0x20FU) { retropilot_driver_brake = (msg->data[2] & 2U) != 0U; }
  brake_pressed = retropilot_engine_brake || retropilot_driver_brake;
  gas_pressed = retropilot_driver_gas;
  steering_disengage = retropilot_override;

  if (!retropilot_healthy() || (retropilot_engaged && !controls_allowed)) {
    retropilot_disengage(true);
  }
  if (msg->addr == 0x100U) {
    uint8_t buttons = msg->data[2] & 0xFU;
    uint8_t rising = buttons & (uint8_t)~retropilot_buttons;
    if (retropilot_healthy()) {
      if (!retropilot_buttons_ready) {
        retropilot_buttons_ready = buttons == 0U;
      } else if ((buttons & 1U) != 0U) {
        retropilot_disengage(false);
      } else if ((rising & 8U) != 0U) {
        retropilot_available = !retropilot_available;
        retropilot_disengage(false);
      } else if (((rising & 6U) != 0U) && retropilot_available && !retropilot_engaged &&
                 (retropilot_commands[0].release_samples >= 16U) &&
                 (retropilot_commands[1].release_samples >= 16U) &&
                 (retropilot_commands[2].release_samples >= 16U) &&
                 (retropilot_commands[0].value == 0) && (retropilot_commands[1].value == 0) && (retropilot_commands[2].value == 0)) {
        retropilot_engaged = true;
        controls_allowed = true;
        retropilot_rt_value = 0;
        retropilot_rt_timestamp = now;
      }
    }
    retropilot_buttons = buttons;
  }
}

static bool retropilot_tx_hook(const CANPacket_t *msg) {
  // The shared dispatcher applies this fault after the mode hook. Do not
  // credit a release that the dispatcher will prevent from reaching CAN.
  if (relay_malfunction) {
    retropilot_disengage(true);
    return false;
  }
  int index = -1;
  if (msg->addr == 0x300U) { index = 0; }
  if (msg->addr == 0x200U) { index = 1; }
  if (msg->addr == 0x20EU) { index = 2; }
  bool disabled = retropilot_disabled_command(msg);
  uint32_t now = microsecond_timer_get();
  if (disabled) {
    if (retropilot_profile_valid && (index >= 0)) {
      uint8_t counter = msg->data[(index == 2) ? 1 : 5] & 0xFU;
      const RetroPilotCommand *prev = &retropilot_commands[index];
      // A strict-counter endpoint can ignore the target yet advance its
      // counter on an invalid sequence. Do not transmit that sequence and
      // diverge from the endpoint's history. Production restricted mode (no
      // profile) still permits all sixteen disabled counter values.
      if (!prev->seen || (counter == ((prev->counter + 1U) & 0xFU))) {
        uint8_t samples = SAFETY_MIN(prev->release_samples + 1U, 16U);
        retropilot_commands[index] = (RetroPilotCommand){.value = 0, .counter = counter, .seen = true,
                                                      .timestamp = now, .release_samples = samples};
        if (index == 0) { retropilot_rt_value = 0; retropilot_rt_timestamp = now; }
      } else {
        retropilot_disengage(true);
        return false;
      }
    }
    return true;
  }

  bool valid = retropilot_profile_valid && (index >= 0) && controls_allowed &&
    retropilot_engaged && retropilot_available && retropilot_healthy() &&
    !msg->fd && !msg->extended && !msg->returned && !msg->rejected &&
    (retropilot_get_checksum(msg) == retropilot_compute_checksum(msg));
  int value = 0;
  if (valid) {
    const RetroPilotSafetyLimits *p = &retropilot_limits;
    const RetroPilotCommand *prev = &retropilot_commands[index];
    uint8_t counter = msg->data[(index == 2) ? 1 : 5] & 0xFU;
    uint32_t interval = (index == 0) ? p->steer_interval : ((index == 1) ? p->gas_interval : p->brake_interval);
    valid = !prev->seen || ((counter == ((prev->counter + 1U) & 0xFU)) &&
                           (safety_get_ts_elapsed(now, prev->timestamp) >= interval));
    if (index == 0) {
      value = retropilot_word(msg, 1) - p->steer_center1;
      int other = p->steer_center2 - retropilot_word(msg, 3);
      int max_speed = p->max_speed_kph * p->speed_divisor;
      int max_steer = p->steer_max - ((p->steer_max - p->steer_high_speed_max) * retropilot_speed / max_speed);
      int step = (SAFETY_ABS(value) > SAFETY_ABS(prev->value)) ? p->steer_up : p->steer_down;
      if (safety_get_ts_elapsed(now, retropilot_rt_timestamp) > 250000U) {
        retropilot_rt_value = prev->value;
        retropilot_rt_timestamp = now;
      }
      valid = valid && ((msg->data[5] & 0xF0U) == 0x80U) && (value == other) &&
        (SAFETY_ABS(value) <= max_steer) && (SAFETY_ABS(value - prev->value) <= step) &&
        (((value * prev->value) >= 0) || (SAFETY_ABS(value) <= p->steer_up)) &&
        (SAFETY_ABS(value - retropilot_rt_value) <= p->steer_rt_delta);
    } else if (index == 1) {
      value = retropilot_word(msg, 1) - p->gas_offset1;
      int other = retropilot_word(msg, 3) - p->gas_offset2;
      valid = valid && ((msg->data[5] & 0xF0U) == 0x80U) && (value >= 0) && (value <= p->gas_range1) &&
        (other >= 0) && (other <= p->gas_range2) && (value * p->gas_range2 == other * p->gas_range1) &&
        (SAFETY_ABS(value - prev->value) <= p->gas_step) && ((value == 0) || (retropilot_commands[2].value == 0));
    } else {
      value = retropilot_word(msg, 4) - 320;
      valid = valid && ((msg->data[1] & 0xF0U) == 0x20U) && (retropilot_word(msg, 2) == 0x7E00) &&
        (value >= 0) && (value <= p->brake_max) && (SAFETY_ABS(value - prev->value) <= p->brake_step) &&
        ((value == 0) || (retropilot_commands[1].value == 0));
    }
    if (valid) {
      retropilot_commands[index] = (RetroPilotCommand){.value = value, .counter = counter, .seen = true,
                                                    .timestamp = now, .release_samples = prev->release_samples};
    }
  }
  if (!valid) { retropilot_disengage(true); }
  return valid;
}
