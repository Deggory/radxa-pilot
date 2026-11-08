#include <stdexcept>
#include <optional>

#include "selfdrive/pandad/pandad.h"
#include "common/swaglog.h"
#include "common/util.h"
#include "selfdrive/pandad/panda_usb_publish.h"

int main(int argc, char *argv[]) {
  LOGW("starting pandad");

  if (argc > 1 && std::string(argv[1]) == "--usb-status") {
    std::unique_ptr<PubMaster> publisher;
    PandaIdentificationPin pin;
    std::optional<PandaProtocol> profile;
    const auto publish_end = [&](UsbObservationState state) {
      if (!publisher || !profile) return;
      const uint64_t now = nanos_since_boot();
      MessageBuilder can, status;
      build_usb_can_message(can, {}, now, false);
      if (*profile == PandaProtocol::CHIMERA_MAILBOX) {
        build_chimera_usb_status_message(status, pin, nullptr, now, now, state);
      } else {
        build_usb_status_message(status, pin, nullptr, now, now, state);
      }
      publisher->send("can", can);
      publisher->send("customReservedRawData1", status);
    };
    try {
      pin = parse_panda_usb_status_args(argc, argv);
      ExitHandler usb_exit;
      auto session = PandaUsbStatusSession::open(pin);
      profile = session->protocol();
      publisher = std::make_unique<PubMaster>(std::vector<const char *>{"can", "customReservedRawData1"});
      LOGW("USB passive observation: CAN and isolated diagnostics; no pandaStates or control threads");
      uint64_t last_status = 0;
      while (!usb_exit) {
        auto frames = session->receive();
        if (!frames) throw std::runtime_error("USB CAN receive failed; session closed without fallback");
        MessageBuilder can;
        build_usb_can_message(can, *frames, nanos_since_boot(), true);
        if (publisher->send("can", can) < 0) throw std::runtime_error("CAN publication failed");
        const uint64_t start = nanos_since_boot();
        if (start - last_status >= 1000000000ULL) {
          MessageBuilder status;
          if (*profile == PandaProtocol::CHIMERA_MAILBOX) {
            auto sample = session->sample_chimera();
            if (!sample) throw std::runtime_error("Chimera health43 failed; session closed without fallback");
            build_chimera_usb_status_message(status, pin, &*sample, start, nanos_since_boot(), UsbObservationState::OBSERVING);
          } else {
            auto sample = session->sample();
            if (!sample) throw std::runtime_error("USB status failed; session closed without fallback");
            build_usb_status_message(status, pin, &*sample, start, nanos_since_boot(), UsbObservationState::OBSERVING);
          }
          if (publisher->send("customReservedRawData1", status) < 0) throw std::runtime_error("USB diagnostic publication failed");
          last_status = nanos_since_boot();
        }
        util::sleep_for(10);
      }
      session->close();
      publish_end(UsbObservationState::CLOSED);
      return 0;
    } catch (const std::exception &e) {
      LOGE("USB observation: %s", e.what());
      try { publish_end(UsbObservationState::FAILED); } catch (...) { /* Best effort after publisher failure. */ }
      return 2;
    }
  }

  LOGE("USB startup requires --usb-status SERIAL VERSION");
  return 2;
}
