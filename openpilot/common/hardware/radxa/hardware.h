#pragma once

#include "common/hardware/pc/hardware.h"

// Identity only. Retain generic Linux paths and no-op hardware operations.
class HardwareRadxa : public HardwarePC {
public:
  static std::string get_name() { return "Radxa Dragon Q8B"; }
  static cereal::InitData::DeviceType get_device_type() { return cereal::InitData::DeviceType::RADXA_Q8B; }
};
