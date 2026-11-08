#include "selfdrive/pandad/panda_usb_status.h"

#include <algorithm>
#include <chrono>
#include <stdexcept>

namespace {
void validate_pin(const PandaIdentificationPin &pin) {
  const auto printable = [](const std::string &s, unsigned char minimum) {
    return !s.empty() && s.size() <= 64 && std::all_of(s.begin(), s.end(), [minimum](unsigned char c) {
      return c >= minimum && c <= 0x7e;
    });
  };
  if (!printable(pin.serial, 0x21) || !printable(pin.firmware_version, 0x20)) {
    throw std::invalid_argument("USB startup requires bounded printable serial and exact firmware version pins");
  }
}
}  // namespace

PandaIdentificationPin parse_panda_usb_status_args(int argc, const char *const *argv) {
  if (argc != 4 || argv == nullptr || argv[1] == nullptr || argv[2] == nullptr || argv[3] == nullptr ||
      std::string(argv[1]) != "--usb-status") {
    throw std::invalid_argument("USB startup requires --usb-status SERIAL VERSION");
  }
  PandaIdentificationPin pin{argv[2], argv[3]};
  validate_pin(pin);
  return pin;
}

std::unique_ptr<PandaUsbStatusSession> PandaUsbStatusSession::open(const PandaIdentificationPin &pin) {
  validate_pin(pin);
  auto handle = PandaUsbHandle::open(pin);
  const auto &id = handle->identification();
  const bool f4 = id.protocol == PandaProtocol::LEGACY_F4_V17 &&
                  decode_legacy_f4_health(id.protocol, id.initial_health.data(), id.initial_health.size()).has_value();
  const bool chimera = id.protocol == PandaProtocol::CHIMERA_MAILBOX &&
                       decode_chimera_health(id.initial_health.data(), id.initial_health.size()).has_value();
  if (!f4 && !chimera) {
    throw std::runtime_error("USB observation requires qualified F4v17 or original Chimera health43");
  }
  return std::unique_ptr<PandaUsbStatusSession>(new PandaUsbStatusSession(std::move(handle)));
}

std::optional<LegacyF4StatusSample> PandaUsbStatusSession::sample() {
  if (!handle_ || protocol_ != PandaProtocol::LEGACY_F4_V17) return std::nullopt;
  try {
    const auto profile = handle_->identification().protocol;
    auto health = read_legacy_f4_health(*handle_, profile);
    if (!health) { close(); return std::nullopt; }
    std::array<LegacyF4CanHealth, 3> can;
    for (uint16_t i = 0; i < can.size(); ++i) {
      auto state = read_legacy_f4_can_health(*handle_, profile, i);
      if (!state) { close(); return std::nullopt; }
      can[i] = *state;
    }
    return LegacyF4StatusSample{*health, can};
  } catch (...) {
    close();
    throw;
  }
}

std::optional<ChimeraHealth> PandaUsbStatusSession::sample_chimera() {
  if (!handle_ || protocol_ != PandaProtocol::CHIMERA_MAILBOX) return std::nullopt;
  try {
    std::array<uint8_t, 64> raw;
    const int size = handle_->control_read(0xd2, 0, 0, raw.data(), raw.size(), 1000);
    auto health = size < 0 ? std::nullopt : decode_chimera_health(raw.data(), size);
    if (!health || !handle_->connected.load() || !handle_->comms_healthy.load()) {
      close();
      return std::nullopt;
    }
    return health;
  } catch (...) {
    close();
    throw;
  }
}

std::optional<std::vector<PandaUsbCanFrame>> PandaUsbStatusSession::receive() {
  if (!handle_) return std::nullopt;
  try {
    std::array<uint8_t, 4096> buffer;
    const int size = handle_->bulk_read(0x81, buffer.data(), buffer.size(), 10);
    if (size < 0 || static_cast<size_t>(size) > buffer.size() || !handle_->comms_healthy.load()) {
      close();
      return std::nullopt;
    }
    const auto now = std::chrono::steady_clock::now().time_since_epoch();
    const auto stamp = std::chrono::duration_cast<std::chrono::nanoseconds>(now).count();
    auto frames = protocol_ == PandaProtocol::CHIMERA_MAILBOX ? chimera_rx_.feed(buffer.data(), size, stamp)
                                                            : rx_.feed(buffer.data(), size, stamp);
    if (!frames) close();
    return frames;
  } catch (...) {
    close();
    throw;
  }
}
