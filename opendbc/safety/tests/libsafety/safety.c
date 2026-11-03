#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

// TODO: time should just be passed into the hooks we expose
uint32_t timer_cnt = 0;
uint32_t microsecond_timer_get(void);
uint32_t microsecond_timer_get(void) {
  return timer_cnt;
}

#include "opendbc/safety/can.h"
#include "opendbc/safety/safety.h"
#include "opendbc/safety/ignition.h"

#ifdef ALLOW_DEBUG
// Artificial raw-unit limits for native tests ONLY. No firmware parameter,
// CarParams, board API or production profile selects these values.
bool set_retropilot_test_profile(int invalid_case) {
  RetroPilotSafetyLimits fixture = {
    .steer_center1 = 1000, .steer_center2 = 1000, .steer_max = 100,
    .steer_high_speed_max = 25, .steer_up = 5, .steer_down = 10, .steer_rt_delta = 20,
    .gas_offset1 = 10, .gas_offset2 = 20, .gas_range1 = 1000, .gas_range2 = 2000,
    .gas_step = 20, .gas_driver_threshold = 100, .brake_max = 128, .brake_step = 16,
    .speed_divisor = 100, .speed_mode = 0, .max_speed_kph = 50, .angle_max = 1000, .angle_rate_max = 500,
    .rx_timeout = 100000U, .steer_interval = 10000U, .gas_interval = 20000U, .brake_interval = 10000U,
  };
  if (invalid_case == 1) { fixture.steer_center1 = -1; }
  if (invalid_case == 2) { fixture.steer_max = 0; }
  if (invalid_case == 3) { fixture.gas_range1 = 0; }
  if (invalid_case == 4) { fixture.brake_max = 4000; }
  if (invalid_case == 5) { fixture.speed_divisor = 10; }
  if (invalid_case == 6) { fixture.rx_timeout = 0U; }
  if (invalid_case == 7) { fixture.steer_interval = 0U; }
  if (invalid_case == 8) { fixture.angle_max = 0; }
  if (invalid_case == 9) { fixture.gas_offset2 = 65535; }
  current_safety_config = retropilot_profile_init(&fixture, 0U);
  return retropilot_profile_valid;
}
#endif

bool safety_config_valid() {
  if (current_safety_config.rx_checks_len <= 0) {
    printf("missing RX checks\n");
    return false;
  }

  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    const RxCheck addr = current_safety_config.rx_checks[i];
    bool valid = addr.status.msg_seen && !addr.status.lagging && addr.status.valid_checksum && (addr.status.wrong_counters < MAX_WRONG_COUNTERS) && addr.status.valid_quality_flag;
    if (!valid) {
      // printf("i %d seen %d lagging %d valid checksum %d wrong counters %d valid quality flag %d\n", i, addr.status.msg_seen, addr.status.lagging, addr.status.valid_checksum, addr.status.wrong_counters, addr.status.valid_quality_flag);
      return false;
    }
  }
  return true;
}

void set_controls_allowed(bool c){
  controls_allowed = c;
}

void set_alternative_experience(int mode){
  alternative_experience = mode;
}

void mads_apply_alternative_experience(int mode){
  mads_set_alternative_experience(&mode);
}

void tick_mads_state(bool vm, bool acc_main, bool op_allowed, bool braking, bool steering_disengage){
  mads_state_update(vm, acc_main, op_allowed, braking, steering_disengage);
}

void set_unseen_rx_checks_valid(void){
  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    RxStatus *status = &current_safety_config.rx_checks[i].status;
    if (!status->msg_seen) {
      status->msg_seen = true;
      status->index = 0;
      status->valid_checksum = true;
      status->wrong_counters = 0;
      status->valid_quality_flag = true;
      status->last_timestamp = microsecond_timer_get();
      status->lagging = false;
    }
  }
}

int get_ignore_frequency_check_count(void){
  int count = 0;
  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    for (uint8_t j = 0U; (j < MAX_ADDR_CHECK_MSGS) && (current_safety_config.rx_checks[i].msg[j].addr != 0); j++) {
      if (current_safety_config.rx_checks[i].msg[j].ignore_frequency_check) {
        count++;
      }
    }
  }
  return count;
}

bool get_rx_check_ignore_frequency(int addr, int bus){
  bool ignore = false;
  for (int i = 0; i < current_safety_config.rx_checks_len; i++) {
    for (uint8_t j = 0U; (j < MAX_ADDR_CHECK_MSGS) && (current_safety_config.rx_checks[i].msg[j].addr != 0); j++) {
      const CanMsgCheck *msg = &current_safety_config.rx_checks[i].msg[j];
      if ((msg->addr == addr) && ((int)msg->bus == bus) && msg->ignore_frequency_check) {
        ignore = true;
      }
    }
  }
  return ignore;
}

void set_relay_malfunction(bool c){
  relay_malfunction = c;
}

bool get_controls_allowed(void){
  return controls_allowed;
}

bool get_ignition_can(void){
  return ignition_can;
}

bool get_relay_malfunction(void){
  return relay_malfunction;
}

bool get_gas_pressed_prev(void){
  return gas_pressed_prev;
}

void set_gas_pressed_prev(bool c){
  gas_pressed_prev = c;
}

bool get_brake_pressed_prev(void){
  return brake_pressed_prev;
}

bool get_regen_braking_prev(void){
  return regen_braking_prev;
}

bool get_steering_disengage_prev(void){
  return steering_disengage_prev;
}

bool get_cruise_engaged_prev(void){
  return cruise_engaged_prev;
}

void set_cruise_engaged_prev(bool engaged){
  cruise_engaged_prev = engaged;
}

bool get_vehicle_moving(void){
  return vehicle_moving;
}

bool get_acc_main_on(void){
  return acc_main_on;
}

float get_vehicle_speed_min(void){
  return vehicle_speed.min / VEHICLE_SPEED_FACTOR;
}

float get_vehicle_speed_max(void){
  return vehicle_speed.max / VEHICLE_SPEED_FACTOR;
}

int get_current_safety_mode(void){
  return current_safety_mode;
}

int get_current_safety_param(void){
  return current_safety_param;
}

void set_timer(uint32_t t){
  timer_cnt = t;
}

void set_torque_meas(int min, int max){
  torque_meas.min = min;
  torque_meas.max = max;
}

int get_torque_meas_min(void){
  return torque_meas.min;
}

int get_torque_meas_max(void){
  return torque_meas.max;
}

void set_torque_driver(int min, int max){
  torque_driver.min = min;
  torque_driver.max = max;
}

int get_torque_driver_min(void){
  return torque_driver.min;
}

int get_torque_driver_max(void){
  return torque_driver.max;
}

void set_rt_torque_last(int t){
  rt_torque_last = t;
}

void set_desired_torque_last(int t){
  desired_torque_last = t;
}

void set_desired_angle_last(int t){
  desired_angle_last = t;
}

void set_angle_meas(int min, int max){
  angle_meas.min = min;
  angle_meas.max = max;
}

int get_angle_meas_min(void){
  return angle_meas.min;
}

int get_angle_meas_max(void){
  return angle_meas.max;
}

void set_desired_curvature_last(int t){
  curvature_state.desired_last = t;
}

int get_desired_curvature_last(void){
  return curvature_state.desired_last;
}

void set_curvature_meas(int min, int max){
  curvature_state.meas.min = min;
  curvature_state.meas.max = max;
}

int get_curvature_meas_min(void){
  return curvature_state.meas.min;
}

int get_curvature_meas_max(void){
  return curvature_state.meas.max;
}


// ***** car specific helpers *****

void set_honda_alt_brake_msg(bool c){
  honda_alt_brake_msg = c;
}

void set_honda_fwd_brake(bool c){
  honda_fwd_brake = c;
}

bool get_honda_fwd_brake(void){
  return honda_fwd_brake;
}

static MADSState *get_mads_state(void) {
  return &m_mads_state;
}

bool get_controls_allowed_lateral(void){
  return controls_allowed_lateral;
}

bool get_controls_requested_lateral(void){
  return get_mads_state()->controls_requested_lateral;
}

bool get_enable_mads(void){
  return get_mads_state()->system_enabled;
}

bool get_disengage_lateral_on_brake(void){
  return get_mads_state()->disengage_lateral_on_brake;
}

bool get_pause_lateral_on_brake(void){
  return get_mads_state()->pause_lateral_on_brake;
}

void set_acc_main_on(bool c){
  acc_main_on = c;
}

void set_current_safety_param_sp(uint16_t param){
  current_safety_param_sp = param;
}

uint16_t get_current_safety_param_sp(void){
  return current_safety_param_sp;
}

void set_mads_button_press(int c){
  mads_button_press = c;
}

int get_mads_button_press(void){
  return mads_button_press;
}

void set_controls_allowed_lateral(bool c){
  controls_allowed_lateral = c;
}

bool get_mads_acc_main(void){
  return m_mads_state.acc_main.current;
}

int mads_get_current_disengage_reason(void) {
  return get_mads_state()->current_disengage.active_reason;
}

void mads_set_current_disengage_reason(int reason) {
  m_mads_state.current_disengage.active_reason = reason;
}

void set_controls_requested_lateral(bool c){
  m_mads_state.controls_requested_lateral = c;
}

void set_mads_params(bool enable_mads, bool disengage_lateral_on_brake, bool pause_lateral_on_brake){
  alternative_experience = 0;
  if (enable_mads) {
    alternative_experience |= ALT_EXP_ENABLE_MADS;

    if (disengage_lateral_on_brake) {
      alternative_experience |= ALT_EXP_MADS_DISENGAGE_LATERAL_ON_BRAKE;
    } else if (pause_lateral_on_brake) {
      alternative_experience |= ALT_EXP_MADS_PAUSE_LATERAL_ON_BRAKE;
    } else {
    }
  }

  mads_set_alternative_experience(&alternative_experience);
}

void set_heartbeat_engaged_mads(bool c){
  heartbeat_engaged_mads = c;
}

void set_steering_disengage(bool c){
  steering_disengage = c;
}

int get_gas_interceptor_prev(void){
  return gas_interceptor_prev;
}

void init_tests(void){
  safety_mode_cnt = 2U;  // avoid ignoring relay_malfunction logic
  alternative_experience = 0;
  current_safety_param_sp = 0;
  set_timer(0);
  ts_steer_req_mismatch_last = 0;
  valid_steer_req_count = 0;
  invalid_steer_req_count = 0;

  // assumes autopark on safety mode init to avoid a fault. get rid of that for testing
  tesla_autopark = false;

  ignition_can = false;
  ignition_can_cnt = 0U;

  // reset MADS state to prevent leaking between tests
  mads_set_system_state(false, false, false);
  mads_button_press = MADS_BUTTON_UNAVAILABLE;
  heartbeat_engaged_mads = false;
  heartbeat_engaged_mads_mismatches = 0U;
}
