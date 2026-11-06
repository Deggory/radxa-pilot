#include <cassert>
#include <stdexcept>

#include "selfdrive/pandad/pandad.h"
#include "common/swaglog.h"
#include "common/util.h"
#include "common/hardware/hw.h"
#include "selfdrive/pandad/panda_usb_publish.h"

int main(int argc, char *argv[]) {
  LOGW("starting pandad");

  if (argc > 1 && std::string(argv[1]) == "--usb-status") {
    std::unique_ptr<PubMaster> publisher;
    PandaIdentificationPin pin;
    const auto publish_end = [&](UsbObservationState state) {
      if (!publisher) return;
      const uint64_t now = nanos_since_boot();
      MessageBuilder can, status;
      build_usb_can_message(can, {}, now, false);
      build_usb_status_message(status, pin, nullptr, now, now, state);
      publisher->send("can", can);
      publisher->send("customReservedRawData1", status);
    };
    try {
      pin = parse_panda_usb_status_args(argc, argv);
      ExitHandler usb_exit;
      auto session = PandaUsbStatusSession::open(pin);
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
          auto sample = session->sample();
          if (!sample) throw std::runtime_error("USB status failed; session closed without fallback");
          MessageBuilder status;
          build_usb_status_message(status, pin, &*sample, start, nanos_since_boot(), UsbObservationState::OBSERVING);
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

#if defined(__RADXA_Q8B__)
  LOGE("Radxa startup requires --usb-status SERIAL VERSION; SPI is disabled for this entry point");
  return 2;
#else

  if (!Hardware::PC()) {
    int err;
    err = util::set_realtime_priority(54);
    assert(err == 0);
    err = util::set_core_affinity({3});
    assert(err == 0);
  }

  std::string serial = (argc > 1) ? argv[1] : "";
  pandad_main_thread(serial);
  return 0;
#endif
}
