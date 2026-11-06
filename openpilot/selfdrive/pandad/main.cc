#include <cassert>
#include <stdexcept>

#include "selfdrive/pandad/pandad.h"
#include "common/swaglog.h"
#include "common/util.h"
#include "common/hardware/hw.h"
#include "selfdrive/pandad/panda_usb_status.h"

int main(int argc, char *argv[]) {
  LOGW("starting pandad");

  if (argc > 1 && std::string(argv[1]) == "--usb-status") {
    try {
      const auto pin = parse_panda_usb_status_args(argc, argv);
      ExitHandler usb_exit;
      auto session = PandaUsbStatusSession::open(pin);
      LOGW("USB status-only session: no CAN publication or control threads");
      while (!usb_exit) {
        auto sample = session->sample();
        if (!sample) throw std::runtime_error("USB status failed; session closed without fallback");
        LOGD("USB status: uptime=%u, all three controller reports complete", sample->health.uptime);
        util::sleep_for(1000);
      }
      return 0;
    } catch (const std::exception &e) {
      LOGE("USB status startup: %s", e.what());
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
