#pragma once

#include <array>
#include <memory>
#include <optional>
#include <utility>

#include "selfdrive/pandad/panda_health.h"
#include "selfdrive/pandad/panda_usb_can.h"
#include "selfdrive/pandad/panda_usb.h"

struct LegacyF4StatusSample {
  LegacyF4Health health;
  std::array<LegacyF4CanHealth, 3> can;
};

// Passive observation ownership, no raw handle/TX access. Legacy F4v17 only in this slice;
// other profiles need their own publisher/validity qualification. Caller serializes
// access. Each sample is sequential D2 + C2(0,1,2), not an atomic MCU snapshot.
class PandaUsbStatusSession {
public:
  static std::unique_ptr<PandaUsbStatusSession> open(const PandaIdentificationPin &pin);
  std::optional<LegacyF4StatusSample> sample();
  std::optional<std::vector<PandaUsbCanFrame>> receive();
  void close() { handle_.reset(); rx_.reset(); }
  bool active() const { return handle_ != nullptr; }

private:
  explicit PandaUsbStatusSession(std::unique_ptr<PandaUsbHandle> handle) : handle_(std::move(handle)) {}
  std::unique_ptr<PandaUsbHandle> handle_;
  PandaUsbCanStream rx_;
};

// Require exactly: program --usb-status SERIAL VERSION. Throws before device IO.
PandaIdentificationPin parse_panda_usb_status_args(int argc, const char *const *argv);
