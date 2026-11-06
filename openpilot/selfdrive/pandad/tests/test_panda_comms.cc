#include <memory>
#include <type_traits>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_comms.h"

static_assert(std::is_abstract_v<PandaCommsHandle>);
static_assert(std::is_base_of_v<PandaCommsHandle, PandaSpiHandle>);
static_assert(std::has_virtual_destructor_v<PandaCommsHandle>);

// No device is opened. Verify transport ownership and error propagation through
// the interface that both SPI and the future USB backend will implement.
class DisconnectedHandle : public PandaCommsHandle {
public:
  explicit DisconnectedHandle(bool &destroyed) : destroyed_(destroyed) {
    hw_serial = "offline-device";
    connected = false;
    comms_healthy = false;
  }

  ~DisconnectedHandle() override { destroyed_ = true; }

  int control_write(uint8_t, uint16_t, uint16_t, unsigned int) override { return -1; }
  int control_read(uint8_t, uint16_t, uint16_t, unsigned char *, uint16_t, unsigned int) override { return -1; }
  int bulk_write(unsigned char, unsigned char *, int, unsigned int) override { return -1; }
  int bulk_read(unsigned char, unsigned char *, int, unsigned int) override { return -1; }

private:
  bool &destroyed_;
};

void test_transport_interface() {
  bool destroyed = false;
  {
    std::unique_ptr<PandaCommsHandle> handle = std::make_unique<DisconnectedHandle>(destroyed);
    CHECK(handle->hw_serial == "offline-device");
    CHECK(!handle->connected);
    CHECK(!handle->comms_healthy);

    unsigned char buffer[1] = {0x5a};
    CHECK(handle->control_read(0xc1, 0, 0, buffer, sizeof(buffer)) == -1);
    CHECK(handle->control_write(0, 0, 0) == -1);
    CHECK(handle->bulk_read(0x81, buffer, sizeof(buffer)) == -1);
    CHECK(handle->bulk_write(3, buffer, sizeof(buffer)) == -1);
    CHECK(buffer[0] == 0x5a);
  }
  CHECK(destroyed);
}

int main() {
  return run_native_test(test_transport_interface);
}
