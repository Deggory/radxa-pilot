// Build against generated, real cereal schemas for the Python/C++ wire check.
#include <cassert>
#include <iostream>

#include <capnp/message.h>
#include <capnp/serialize.h>

#include "common/hardware/hw.h"

int main(int argc, char **) {
  assert(Hardware::PC());
#if defined(__RADXA_Q8B__)
  assert(Hardware::get_name() == "Radxa Dragon Q8B");
  assert(Hardware::get_device_type() == cereal::InitData::DeviceType::RADXA_Q8B);
#else
  assert(Hardware::get_name() == "pc");
  assert(Hardware::get_device_type() == cereal::InitData::DeviceType::PC);
#endif
  capnp::MallocMessageBuilder message;
  auto event = message.initRoot<cereal::Event>();
  if (argc > 1) {
    event.initInitData().setDeviceType(Hardware::get_device_type());
  } else {
    event.initDeviceState().setDeviceType(Hardware::get_device_type());
  }
  std::cerr << Hardware::get_name() << '\n';
  capnp::writeMessageToFd(1, message);
  return 0;
}
