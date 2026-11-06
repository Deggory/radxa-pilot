#include <algorithm>
#include <cstring>
#include <iostream>
#include <optional>
#include <stdexcept>

#include <libusb-1.0/libusb.h>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_usb.h"

// Complete libusb's opaque types for fake C API implementations. This test does
// not link libusb, enumerate the host or open a real USB device.
struct libusb_context {};
struct libusb_device_handle { libusb_device *device; };
struct libusb_device {
  uint16_t vendor = 0x3801, product_id = 0xddcc;
  std::string serial = "selected", product = "panda", version = "pinned-version";
  std::vector<uint8_t> versions = {17, 4, 5};
  uint8_t hardware = 3;
  size_t health_size = 59;
  int descriptor_error = 0, open_error = 0, string_error = 0;
  libusb_device_handle handle{this};
  int reads = 0;
  bool active = false;
};

namespace {
struct FakeUsb {
  std::vector<libusb_device> devices;
  int init_error = 0, list_error = 0, config_error = 0, claim_error = 0, config = 1;
  int init_calls = 0, contexts = 0, lists = 0, opens = 0, closes = 0, claims = 0, releases = 0;
  int control_in = 0, control_out = 0, bulk_calls = 0;
  std::optional<int> control_result;
  int bulk_result = 0, transferred = 4;
  unsigned int last_timeout = 0;
} usb;
const PandaIdentificationPin PIN{"selected", "pinned-version"};
int scenarios = 0;

void require(bool condition) {
  if (!condition) throw std::logic_error("Unexpected fake libusb operation");
}

void reset(std::vector<libusb_device> devices = {libusb_device{}}) {
  CHECK(usb.contexts == 0 && usb.lists == 0 && usb.opens == usb.closes && usb.claims == usb.releases);
  usb = FakeUsb{};
  usb.devices = std::move(devices);
  ++scenarios;
}

void failed_open(const PandaIdentificationPin &pin = PIN) {
  bool failed = false;
  try {
    PandaUsbHandle::open(pin);
  } catch (const std::runtime_error &) {
    failed = true;
  }
  CHECK(failed);
  CHECK(usb.contexts == 0 && usb.lists == 0 && usb.opens == usb.closes && usb.claims == usb.releases);
  CHECK(usb.control_out == 0 && usb.bulk_calls == 0);
}
}  // namespace

extern "C" {
int LIBUSB_CALL libusb_init(libusb_context **ctx) {
  ++usb.init_calls;
  if (usb.init_error) return usb.init_error;
  *ctx = new libusb_context;
  ++usb.contexts;
  return 0;
}
void LIBUSB_CALL libusb_exit(libusb_context *ctx) { delete ctx; --usb.contexts; }
ssize_t LIBUSB_CALL libusb_get_device_list(libusb_context *, libusb_device ***list) {
  if (usb.list_error) return usb.list_error;
  *list = new libusb_device *[usb.devices.size() + 1]{};
  for (size_t i = 0; i < usb.devices.size(); ++i) (*list)[i] = &usb.devices[i];
  ++usb.lists;
  return usb.devices.size();
}
void LIBUSB_CALL libusb_free_device_list(libusb_device **list, int unref) {
  require(unref == 1);
  delete[] list;
  --usb.lists;
}
int LIBUSB_CALL libusb_get_device_descriptor(libusb_device *device, libusb_device_descriptor *desc) {
  if (device->descriptor_error) return device->descriptor_error;
  *desc = {};
  desc->idVendor = device->vendor;
  desc->idProduct = device->product_id;
  desc->iSerialNumber = 1;
  desc->iProduct = 2;
  return 0;
}
int LIBUSB_CALL libusb_open(libusb_device *device, libusb_device_handle **handle) {
  if (device->open_error) return device->open_error;
  require(!device->active);
  device->active = true;
  device->handle.device = device;
  *handle = &device->handle;
  ++usb.opens;
  return 0;
}
void LIBUSB_CALL libusb_close(libusb_device_handle *handle) { handle->device->active = false; ++usb.closes; }
int LIBUSB_CALL libusb_get_string_descriptor_ascii(libusb_device_handle *handle, uint8_t index,
                                                  unsigned char *data, int length) {
  if (handle->device->string_error) return handle->device->string_error;
  require(index == 1 || index == 2);
  const auto &text = index == 1 ? handle->device->serial : handle->device->product;
  int copied = std::min<int>(text.size(), length);
  std::memcpy(data, text.data(), copied);
  return copied;
}
int LIBUSB_CALL libusb_get_configuration(libusb_device_handle *, int *config) {
  *config = usb.config;
  return usb.config_error;
}
int LIBUSB_CALL libusb_claim_interface(libusb_device_handle *, int interface) {
  require(interface == 0);
  if (usb.claim_error) return usb.claim_error;
  ++usb.claims;
  return 0;
}
int LIBUSB_CALL libusb_release_interface(libusb_device_handle *, int interface) {
  // Destruction must never throw, including after disconnect.
  if (interface != 0) return LIBUSB_ERROR_INVALID_PARAM;
  ++usb.releases;
  return 0;
}
int LIBUSB_CALL libusb_control_transfer(libusb_device_handle *handle, uint8_t type, uint8_t request,
                                        uint16_t, uint16_t, unsigned char *data, uint16_t length,
                                        unsigned int timeout) {
  require(timeout > 0 && timeout <= 1000 && usb.claims > usb.releases);
  usb.last_timeout = timeout;
  if (type == 0x40) {
    require(handle->device->reads >= 4);
    ++usb.control_out;
    return usb.control_result.value_or(0);
  }
  require(type == 0xc0);
  ++usb.control_in;
  ++handle->device->reads;
  if (usb.control_result) return *usb.control_result;
  std::vector<uint8_t> reply;
  switch (request) {
    case 0xd6: reply.assign(handle->device->version.begin(), handle->device->version.end()); break;
    case 0xc1: reply = {handle->device->hardware}; break;
    case 0xdd: reply = handle->device->versions; break;
    case 0xd2: reply.resize(handle->device->health_size); break;
    default: reply = {0xa5}; break;
  }
  std::copy_n(reply.begin(), std::min<size_t>(length, reply.size()), data);
  return reply.size();
}
int LIBUSB_CALL libusb_bulk_transfer(libusb_device_handle *, unsigned char endpoint, unsigned char *data,
                                     int length, int *transferred, unsigned int timeout) {
  require(timeout > 0 && timeout <= 1000 && usb.claims > usb.releases);
  usb.last_timeout = timeout;
  ++usb.bulk_calls;
  *transferred = usb.transferred;
  if ((endpoint & 0x80) && *transferred >= 0 && *transferred <= length) std::fill_n(data, *transferred, 0x5a);
  return usb.bulk_result;
}
}  // extern "C"

void test_usb() {
  reset();
  {
    auto handle = PandaUsbHandle::open(PIN);
    CHECK(handle->identification().protocol == PandaProtocol::LEGACY_F4_V17);
    CHECK(handle->hw_serial == "selected" && usb.control_in == 4);
    CHECK(usb.control_out == 0 && usb.bulk_calls == 0 && usb.lists == 0);
    unsigned char data[64] = {};
    CHECK(handle->control_read(0xee, 0, 0, data, sizeof(data)) == 1 && data[0] == 0xa5);
    CHECK(usb.last_timeout == 1000);
    CHECK(handle->control_write(0xc0, 0, 0) == 0);
    CHECK(handle->bulk_read(0x81, data, sizeof(data)) == 4 && data[0] == 0x5a);
    CHECK(handle->bulk_write(3, data, sizeof(data), 5) == 4);
    CHECK(!handle->comms_healthy);  // A short write is not full success.
  }
  reset();
  for (int result : std::initializer_list<int>{0, LIBUSB_ERROR_TIMEOUT}) {
    for (int count : {0, 1, 64}) {
      auto handle = PandaUsbHandle::open(PIN);
      unsigned char data[64] = {};
      usb.bulk_result = result;
      usb.transferred = count;
      CHECK(handle->bulk_read(0x81, data, sizeof(data), 10) == count);
      CHECK(handle->connected && handle->comms_healthy);
    }
  }
  reset();
  for (int error : {LIBUSB_ERROR_IO, LIBUSB_ERROR_NO_DEVICE, LIBUSB_ERROR_OVERFLOW, LIBUSB_ERROR_PIPE}) {
    auto handle = PandaUsbHandle::open(PIN);
    unsigned char data[64] = {};
    usb.bulk_result = error;
    CHECK(handle->bulk_read(0x81, data, sizeof(data)) == error);
    CHECK(!handle->comms_healthy);
    if (error == LIBUSB_ERROR_NO_DEVICE) {
      CHECK(!handle->connected);
      int calls = usb.bulk_calls;
      CHECK(handle->bulk_read(0x81, data, sizeof(data)) == LIBUSB_ERROR_NO_DEVICE);
      CHECK(usb.bulk_calls == calls);
    }
  }
  reset();
  for (int count : {-1, 65}) {
    auto handle = PandaUsbHandle::open(PIN);
    unsigned char data[64] = {};
    usb.transferred = count;
    CHECK(handle->bulk_read(0x81, data, sizeof(data)) == LIBUSB_ERROR_IO);
    CHECK(!handle->comms_healthy);
  }
  reset();
  {
    auto handle = PandaUsbHandle::open(PIN);
    unsigned char data[64] = {};
    usb.bulk_result = LIBUSB_ERROR_TIMEOUT;
    usb.transferred = 4;
    int calls = usb.bulk_calls;
    CHECK(handle->bulk_write(3, data, sizeof(data)) == LIBUSB_ERROR_TIMEOUT);
    CHECK(usb.bulk_calls == calls + 1 && !handle->comms_healthy);
  }
  reset();
  for (int error : {LIBUSB_ERROR_TIMEOUT, LIBUSB_ERROR_PIPE, LIBUSB_ERROR_NO_DEVICE}) {
    usb.control_result.reset();
    auto handle = PandaUsbHandle::open(PIN);
    usb.control_result = error;
    unsigned char data[1] = {};
    CHECK(handle->control_read(0xee, 0, 0, data, 1) == error);
    CHECK(!handle->comms_healthy);
  }
  reset();
  {
    auto handle = PandaUsbHandle::open(PIN);
    unsigned char data[1] = {};
    int calls = usb.bulk_calls;
    CHECK(handle->bulk_read(0x81, nullptr, 1) == LIBUSB_ERROR_INVALID_PARAM);
    CHECK(handle->bulk_read(0x81, data, -1) == LIBUSB_ERROR_INVALID_PARAM);
    CHECK(handle->bulk_write(0x83, data, 1) == LIBUSB_ERROR_INVALID_PARAM);
    CHECK(handle->bulk_read(1, data, 1) == LIBUSB_ERROR_INVALID_PARAM);
    CHECK(usb.bulk_calls == calls);
    CHECK(handle->bulk_read(0x81, nullptr, 0) == 0);
    CHECK(handle->bulk_write(3, nullptr, 0) == 0);
    CHECK(handle->bulk_read(0x81, data, 1, 5000) == LIBUSB_ERROR_IO);
    CHECK(usb.last_timeout == 1000);
    handle->cleanup();
    handle->cleanup();
    CHECK(!handle->connected);
    CHECK(handle->control_write(0xc0, 0, 0) == LIBUSB_ERROR_NO_DEVICE);
  }
  reset();
  {
    auto handle = PandaUsbHandle::open(PIN);
    unsigned char data[1] = {};
    usb.control_result = 2;
    CHECK(handle->control_read(0xee, 0, 0, data, sizeof(data)) == LIBUSB_ERROR_IO);
    CHECK(!handle->comms_healthy);
  }
  reset();
  {
    auto handle = PandaUsbHandle::open(PIN);
    usb.control_result = LIBUSB_ERROR_TIMEOUT;
    int calls = usb.control_out;
    CHECK(handle->control_write(0xc0, 0, 0) == LIBUSB_ERROR_TIMEOUT);
    CHECK(!handle->comms_healthy && usb.control_out == calls + 1);
  }
  reset();
  auto chimera = libusb_device{};
  chimera.vendor = 0xbbaa;
  chimera.product = "Chimera";
  chimera.version = "v1.0.0-DEV-de193215-DEBUG";
  chimera.health_size = 43;
  usb.devices = {chimera};
  {
    auto handle = PandaUsbHandle::open({"selected", chimera.version});
    CHECK(handle->identification().protocol == PandaProtocol::CHIMERA_MAILBOX && usb.control_in == 2);
    unsigned char data[64] = {};
    CHECK(handle->control_write(0xdc, 0, 0) == LIBUSB_ERROR_ACCESS);
    CHECK(handle->bulk_write(3, data, sizeof(data)) == LIBUSB_ERROR_ACCESS);
    int reads = usb.control_in;
    CHECK(handle->control_read(0xd8, 0, 0, data, sizeof(data)) == LIBUSB_ERROR_ACCESS);
    CHECK(handle->control_read(0xdc, 0, 0, data, sizeof(data)) == LIBUSB_ERROR_ACCESS);
    CHECK(handle->control_read(0xd2, 1, 0, data, sizeof(data)) == LIBUSB_ERROR_ACCESS);
    CHECK(usb.control_in == reads);
    CHECK(handle->control_read(0xd2, 0, 0, data, sizeof(data)) == 43);
    CHECK(usb.control_out == 0 && usb.bulk_calls == 0);
    CHECK(handle->bulk_read(0x81, data, sizeof(data)) == 4);
  }
  reset();
  usb.devices[0].hardware = 7;
  usb.devices[0].versions = {0xaf, 0x9e, 0x8f, 0xca, 0x76, 0xf2, 0xab, 0x75};
  usb.devices[0].health_size = 49;
  { auto handle = PandaUsbHandle::open(PIN); CHECK(handle->identification().protocol == PandaProtocol::CURRENT); }
  reset();
  usb.devices[0].vendor = 0xbbaa;
  { auto handle = PandaUsbHandle::open(PIN); CHECK(handle->identification().protocol == PandaProtocol::LEGACY_F4_V17); }
  reset();
  auto other = libusb_device{};
  other.serial = "other";
  auto bootstub = libusb_device{};
  bootstub.product_id = 0xddee;
  auto dfu = libusb_device{};
  dfu.vendor = 0x0483; dfu.product_id = 0xdf11;
  usb.devices = {bootstub, dfu, other, libusb_device{}};
  { auto handle = PandaUsbHandle::open(PIN); CHECK(usb.opens == 2 && usb.closes == 1); }
  reset({libusb_device{}, libusb_device{}});
  failed_open();  // Duplicate serial is ambiguous, not first-match selection.
  reset({}); failed_open();
  reset(); failed_open({"", "pinned-version"}); CHECK(usb.init_calls == 0);
  reset(); failed_open({"selected", ""}); CHECK(usb.init_calls == 0);
  reset(); usb.init_error = LIBUSB_ERROR_NO_MEM; failed_open();
  reset(); usb.list_error = LIBUSB_ERROR_IO; failed_open();
  reset(); usb.devices[0].descriptor_error = LIBUSB_ERROR_IO; failed_open();
  reset(); usb.devices[0].open_error = LIBUSB_ERROR_ACCESS; failed_open();
  reset(); usb.devices[0].string_error = LIBUSB_ERROR_PIPE; failed_open();
  reset(); usb.devices[0].serial = "other"; failed_open();
  reset(); usb.devices[0].product = ""; failed_open();
  reset(); usb.devices[0].serial = std::string(256, 'x'); failed_open();
  reset(); usb.devices[0].version = "unknown"; failed_open();
  reset(); usb.devices[0].versions = {0, 0}; failed_open();
  reset(); usb.devices[0].health_size = 49; failed_open();
  reset(); usb.config_error = LIBUSB_ERROR_NO_DEVICE; failed_open();
  reset(); usb.config = 0; failed_open();
  reset(); usb.claim_error = LIBUSB_ERROR_BUSY; failed_open(); CHECK(usb.control_in == 0);
  reset(); usb.control_result = LIBUSB_ERROR_NO_DEVICE; failed_open();
  reset();
  std::cout << scenarios << " USB scenario groups passed; no real USB calls\n";
}

int main() {
  return run_native_test([] {
    try {
      test_usb();
    } catch (...) {
      std::cerr << "USB scenario group " << scenarios << '\n';
      throw;
    }
  });
}
