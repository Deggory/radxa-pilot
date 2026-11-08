#pragma once

#include <array>
#include <memory>
#include <optional>
#include <utility>

#include "selfdrive/pandad/panda_health.h"
#include "selfdrive/pandad/panda_usb_can.h"
#include "selfdrive/pandad/panda_usb.h"
#include "selfdrive/pandad/chimera_usb.h"

struct LegacyF4StatusSample {
  LegacyF4Health health;
  std::array<LegacyF4CanHealth, 3> can;
};

// Passive observation ownership, no raw handle/TX access. F4v17 and original
// Chimera have distinct codecs and health types. Caller serializes access.
// F4 samples are sequential D2+C2(0,1,2); Chimera reads D2 only.
class PandaUsbStatusSession {
public:
  static std::unique_ptr<PandaUsbStatusSession> open(const PandaIdentificationPin &pin);
  std::optional<LegacyF4StatusSample> sample();
  std::optional<ChimeraHealth> sample_chimera();
  std::optional<std::vector<PandaUsbCanFrame>> receive();
  void close() { handle_.reset(); rx_.reset(); chimera_rx_.reset(); }
  bool active() const { return handle_ != nullptr; }
  PandaProtocol protocol() const { return protocol_; }

private:
  explicit PandaUsbStatusSession(std::unique_ptr<PandaUsbHandle> handle)
      : handle_(std::move(handle)), protocol_(handle_->identification().protocol) {}
  std::unique_ptr<PandaUsbHandle> handle_;
  const PandaProtocol protocol_;  // Retained for failure labels after close.
  PandaUsbCanStream rx_;
  ChimeraUsbCanStream chimera_rx_;
};

// Require exactly: program --usb-status SERIAL VERSION. Throws before device IO.
PandaIdentificationPin parse_panda_usb_status_args(int argc, const char *const *argv);
