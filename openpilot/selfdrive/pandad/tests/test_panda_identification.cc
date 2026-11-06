#include <algorithm>
#include <iostream>
#include <stdexcept>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_identification.h"

namespace {
const std::string VERSION = "pinned-application-version";
const PandaUsbIdentity PANDA = {0x3801, 0xddcc, "selected-serial", "panda"};
const PandaUsbIdentity CHIMERA = {0xbbaa, 0xddcc, "selected-serial", "Chimera"};
const PandaIdentificationPin PIN = {"selected-serial", VERSION};
const PandaIdentificationPin CHIMERA_PIN = {"selected-serial", "v1.0.0-DEV-de193215-DEBUG"};

struct Reply {
  uint8_t request;
  std::vector<uint8_t> data;
  int error = 0;
  bool disconnect = false;
};

std::vector<uint8_t> text_bytes(const std::string &text) {
  return {text.begin(), text.end()};
}

// These bytes are independently pinned by the November 5 source-hash receipt.
std::vector<uint8_t> current_versions() {
  return {0xaf, 0x9e, 0x8f, 0xca, 0x76, 0xf2, 0xab, 0x75};
}

class ScriptedHandle : public PandaCommsHandle {
public:
  explicit ScriptedHandle(std::vector<Reply> replies) : replies_(std::move(replies)) {
    hw_serial = "selected-serial";
  }

  int control_read(uint8_t request, uint16_t value, uint16_t index, unsigned char *data,
                   uint16_t length, unsigned int timeout) override {
    if (value != 0 || index != 0 || timeout == 0 || timeout > 1000 || position >= replies_.size()) {
      throw std::logic_error("Unexpected identification read or unbounded timeout");
    }
    const Reply &reply = replies_[position++];
    if (request != reply.request) throw std::logic_error("Unexpected identification request");
    if (reply.disconnect) connected = false;
    if (reply.error < 0) return reply.error;
    std::copy_n(reply.data.begin(), std::min<size_t>(length, reply.data.size()), data);
    return reply.data.size();
  }

  int control_write(uint8_t, uint16_t, uint16_t, unsigned int) override { return forbidden_write(); }
  int bulk_write(unsigned char, unsigned char *, int, unsigned int) override { return forbidden_write(); }
  int bulk_read(unsigned char, unsigned char *, int, unsigned int) override { return forbidden_write(); }

  size_t position = 0;
  int forbidden_calls = 0;

private:
  int forbidden_write() {
    ++forbidden_calls;
    throw std::logic_error("Identification attempted a non-control-read operation");
  }
  std::vector<Reply> replies_;
};

std::vector<Reply> panda_replies(uint8_t hardware, const std::vector<uint8_t> &versions, size_t health_size) {
  return {{0xd6, text_bytes(VERSION)}, {0xc1, {hardware}}, {0xdd, versions}, {0xd2, std::vector<uint8_t>(health_size)}};
}

int rejected = 0;
void reject(const PandaUsbIdentity &identity, const PandaIdentificationPin &pin, std::vector<Reply> replies) {
  ScriptedHandle handle(std::move(replies));
  bool failed = false;
  try {
    identify_panda(handle, identity, pin);
  } catch (const std::runtime_error &) {
    failed = true;
  }
  CHECK(failed);
  CHECK(handle.forbidden_calls == 0);
  ++rejected;
}

void test_identification() {
  for (uint16_t vendor : {0x3801, 0xbbaa}) {
    auto identity = PANDA;
    identity.vendor_id = vendor;
    for (uint8_t hardware : {1, 2, 3, 5, 6}) {
      ScriptedHandle handle(panda_replies(hardware, {17, 4, 5}, 59));
      auto result = identify_panda(handle, identity, PIN);
      CHECK(result.protocol == PandaProtocol::LEGACY_F4_V17);
      CHECK(result.hardware_type == hardware);
      CHECK(result.firmware_version == VERSION);
      CHECK(result.initial_health.size() == 59);
      CHECK(handle.position == 4 && handle.forbidden_calls == 0);
    }
    for (uint8_t hardware : {7, 9, 10, 0xb1}) {
      ScriptedHandle handle(panda_replies(hardware, current_versions(), 49));
      auto result = identify_panda(handle, identity, PIN);
      CHECK(result.protocol == PandaProtocol::CURRENT);
      CHECK(result.hardware_type == hardware);
      CHECK(result.initial_health.size() == 49);
      CHECK(handle.position == 4 && handle.forbidden_calls == 0);
    }
  }
  ScriptedHandle chimera({{0xd6, text_bytes(CHIMERA_PIN.firmware_version)}, {0xd2, std::vector<uint8_t>(43)}});
  auto result = identify_panda(chimera, CHIMERA, CHIMERA_PIN);
  CHECK(result.protocol == PandaProtocol::CHIMERA_MAILBOX);
  CHECK(!result.hardware_type.has_value());
  CHECK(result.initial_health.size() == 43);
  CHECK(chimera.position == 2 && chimera.forbidden_calls == 0);

  // Descriptor/pin rejection must happen before any vendor request.
  for (auto identity : {PandaUsbIdentity{0x3801, 0xddee, "selected-serial", "panda"},
                        PandaUsbIdentity{0x0483, 0xdf11, "selected-serial", "DFU"},
                        PandaUsbIdentity{0x1234, 0xddcc, "selected-serial", "panda"},
                        PandaUsbIdentity{0x3801, 0xddcc, "other-serial", "panda"},
                        PandaUsbIdentity{0x3801, 0xddcc, "selected-serial", "Chimera"}}) {
    reject(identity, PIN, {});
  }
  reject(PANDA, {"", VERSION}, {});
  reject(PANDA, {"selected-serial", ""}, {});
  reject(PANDA, {"selected-serial", std::string(65, 'x')}, {});
  reject(PANDA, {"selected-serial", std::string("bad\0version", 11)}, {});
  reject(PANDA, {"selected-serial", "bad\nversion"}, {});
  reject(CHIMERA, PIN, {});  // An arbitrary version pin is not a reviewed Chimera protocol.
  reject(PANDA, PIN, {{0xd6, text_bytes("different-version")}});
  reject(PANDA, PIN, {{0xd6, {}, -7}});
  reject(PANDA, PIN, {{0xd6, text_bytes(VERSION), 0, true}});
  reject(PANDA, PIN, {{0xd6, text_bytes(VERSION)}, {0xc1, {}, -4}});
  reject(PANDA, PIN, {{0xd6, text_bytes(VERSION)}, {0xc1, {1}}, {0xdd, {}, -4}});
  auto error_health = panda_replies(1, {17, 4, 5}, 59);
  error_health.back().error = -4;
  reject(PANDA, PIN, error_health);

  // Missing/short/overlong identification replies never choose a default profile.
  for (size_t length = 0; length <= 65; ++length) {
    if (length != VERSION.size()) reject(PANDA, PIN, {{0xd6, std::vector<uint8_t>(length, 'x')}});
    if (length != 1) reject(PANDA, PIN, {{0xd6, text_bytes(VERSION)}, {0xc1, std::vector<uint8_t>(length, 1)}});
    if (length != 3) reject(PANDA, PIN, {{0xd6, text_bytes(VERSION)}, {0xc1, {1}}, {0xdd, std::vector<uint8_t>(length)}});
    if (length != 59) reject(PANDA, PIN, panda_replies(1, {17, 4, 5}, length));
    if (length != 49) reject(PANDA, PIN, panda_replies(7, current_versions(), length));
    if (length != 43) reject(CHIMERA, CHIMERA_PIN, {{0xd6, text_bytes(CHIMERA_PIN.firmware_version)},
                                               {0xd2, std::vector<uint8_t>(length)}});
  }
  for (auto versions : {std::vector<uint8_t>{16, 4, 5}, {17, 3, 5}, {17, 4, 4}, current_versions()}) {
    reject(PANDA, PIN, panda_replies(1, versions, 59));
  }
  auto wrong_hash = current_versions();
  wrong_hash[0] ^= 1;
  reject(PANDA, PIN, panda_replies(7, wrong_hash, 49));
  reject(PANDA, PIN, panda_replies(7, {17, 4, 5}, 59));
  for (uint8_t hardware : {0, 4, 8, 255}) {
    reject(PANDA, PIN, panda_replies(hardware, {17, 4, 5}, 59));
    reject(PANDA, PIN, panda_replies(hardware, current_versions(), 49));
  }
  ScriptedHandle disconnected({});
  disconnected.connected = false;
  bool failed = false;
  try {
    identify_panda(disconnected, PANDA, PIN);
  } catch (const std::runtime_error &) {
    failed = true;
  }
  CHECK(failed && disconnected.position == 0);
  ScriptedHandle unhealthy({});
  unhealthy.comms_healthy = false;
  failed = false;
  try {
    identify_panda(unhealthy, PANDA, PIN);
  } catch (const std::runtime_error &) {
    failed = true;
  }
  CHECK(failed && unhealthy.position == 0);
  ScriptedHandle wrong_handle({});
  wrong_handle.hw_serial = "another-device";
  failed = false;
  try {
    identify_panda(wrong_handle, PANDA, PIN);
  } catch (const std::runtime_error &) {
    failed = true;
  }
  CHECK(failed && wrong_handle.position == 0);
  std::cout << "19 supported fixtures; " << rejected << " rejected fixtures; 3 invalid transports; zero writes\n";
}
}  // namespace

int main() {
  return run_native_test(test_identification);
}
