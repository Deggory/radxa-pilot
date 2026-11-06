#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_usb.h"

// Pull the real backend and vendored libusb into the executable, then exercise
// only the pin guard. The fake-USB suite also proves this guard precedes init.
int main() {
  return run_native_test([] {
    bool rejected = false;
    try {
      PandaUsbHandle::open({"", ""});
    } catch (const std::runtime_error &) {
      rejected = true;
    }
    CHECK(rejected);
  });
}
