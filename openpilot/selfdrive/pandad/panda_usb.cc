#include "selfdrive/pandad/panda_usb.h"

#include <algorithm>
#include <stdexcept>

#include <libusb-1.0/libusb.h>

namespace {
unsigned int bounded_timeout(unsigned int timeout) {
  // libusb interprets zero as infinite. The shared transport's default must
  // remain finite here, including when a caller requests a longer interval.
  return timeout == 0 ? 1000 : std::min(timeout, 1000U);
}

std::optional<std::string> usb_string(libusb_device_handle *device, uint8_t index) {
  if (index == 0) return std::nullopt;
  unsigned char data[256];
  int length = libusb_get_string_descriptor_ascii(device, index, data, sizeof(data));
  if (length <= 0 || length >= static_cast<int>(sizeof(data)) ||
      !std::all_of(data, data + length, [](unsigned char ch) { return ch >= 0x20 && ch <= 0x7e; })) {
    return std::nullopt;
  }
  return std::string(data, data + length);
}
}  // namespace

std::unique_ptr<PandaUsbHandle> PandaUsbHandle::open(const PandaIdentificationPin &pin) {
  if (pin.serial.empty() || pin.firmware_version.empty() || pin.firmware_version.size() > 64 ||
      !std::all_of(pin.firmware_version.begin(), pin.firmware_version.end(),
                   [](unsigned char ch) { return ch >= 0x20 && ch <= 0x7e; })) {
    throw std::runtime_error("USB connection requires an explicit serial and firmware version pin");
  }
  libusb_context *raw_context = nullptr;
  int error = libusb_init(&raw_context);
  std::unique_ptr<libusb_context, decltype(&libusb_exit)> context(raw_context, libusb_exit);
  if (error < 0 || !context) throw std::runtime_error("Unable to initialize libusb");

  libusb_device **raw_list = nullptr;
  ssize_t count = libusb_get_device_list(context.get(), &raw_list);
  auto free_list = [](libusb_device **list) { libusb_free_device_list(list, 1); };
  std::unique_ptr<libusb_device *, decltype(free_list)> list(raw_list, free_list);
  if (count < 0 || !list) throw std::runtime_error("Unable to enumerate USB devices");

  std::unique_ptr<libusb_device_handle, decltype(&libusb_close)> selected(nullptr, libusb_close);
  PandaUsbIdentity identity{};
  for (ssize_t i = 0; i < count; ++i) {
    libusb_device_descriptor descriptor{};
    if (libusb_get_device_descriptor(list.get()[i], &descriptor) < 0 || descriptor.idProduct != 0xddcc ||
        (descriptor.idVendor != 0x3801 && descriptor.idVendor != 0xbbaa)) continue;
    libusb_device_handle *raw_device = nullptr;
    error = libusb_open(list.get()[i], &raw_device);
    std::unique_ptr<libusb_device_handle, decltype(&libusb_close)> candidate(raw_device, libusb_close);
    if (error < 0 || !candidate) continue;
    const auto serial = usb_string(candidate.get(), descriptor.iSerialNumber);
    if (!serial || *serial != pin.serial) continue;
    if (selected) throw std::runtime_error("Multiple USB devices match the pinned serial");
    const auto product = usb_string(candidate.get(), descriptor.iProduct);
    if (!product) throw std::runtime_error("Selected USB device has no valid product descriptor");
    identity = {descriptor.idVendor, descriptor.idProduct, *serial, *product};
    selected = std::move(candidate);
  }
  if (!selected) throw std::runtime_error("No readable normal-mode USB device matches the pinned serial");
  list.reset();

  // Construct before handing off resources, so allocation/string failures leave
  // the local owners responsible for cleanup.
  auto handle = std::unique_ptr<PandaUsbHandle>(new PandaUsbHandle(identity.serial));
  handle->context_ = context.release();
  handle->device_ = selected.release();
  int configuration = 0;
  if (libusb_get_configuration(handle->device_, &configuration) < 0 || configuration != 1) {
    throw std::runtime_error("Selected USB device must already use configuration 1");
  }
  if (libusb_claim_interface(handle->device_, 0) < 0) {
    throw std::runtime_error("Cannot exclusively claim selected USB interface 0");
  }
  handle->claimed_ = true;
  handle->identification_ = identify_panda(*handle, identity, pin);
  return handle;
}

PandaUsbHandle::~PandaUsbHandle() { cleanup(); }

void PandaUsbHandle::cleanup() {
  std::lock_guard lock(mutex_);
  connected = false;
  comms_healthy = false;
  if (device_) {
    if (claimed_) libusb_release_interface(device_, 0);
    libusb_close(device_);
    device_ = nullptr;
    claimed_ = false;
  }
  if (context_) {
    libusb_exit(context_);
    context_ = nullptr;
  }
}

int PandaUsbHandle::record_error(int result) {
  if (result < 0) comms_healthy = false;
  if (result == LIBUSB_ERROR_NO_DEVICE) connected = false;
  return result;
}

int PandaUsbHandle::control_read(uint8_t request, uint16_t param1, uint16_t param2,
                                 unsigned char *data, uint16_t length, unsigned int timeout) {
  std::lock_guard lock(mutex_);
  if (!connected) return LIBUSB_ERROR_NO_DEVICE;
  if (!comms_healthy) return LIBUSB_ERROR_IO;
  // IN direction alone is not read-only: original firmware dispatches command
  // numbers with side effects regardless of direction. Keep its passive API
  // limited to the two reviewed observation requests.
  if (identification_ && identification_->protocol == PandaProtocol::CHIMERA_MAILBOX &&
      ((request != 0xd2 && request != 0xd6) || param1 != 0 || param2 != 0)) return LIBUSB_ERROR_ACCESS;
  if (length > 0 && !data) return LIBUSB_ERROR_INVALID_PARAM;
  int result = libusb_control_transfer(device_, 0xc0, request, param1, param2, data, length, bounded_timeout(timeout));
  return record_error(result > length ? LIBUSB_ERROR_IO : result);
}

int PandaUsbHandle::control_write(uint8_t request, uint16_t param1, uint16_t param2, unsigned int timeout) {
  std::lock_guard lock(mutex_);
  if (!connected) return LIBUSB_ERROR_NO_DEVICE;
  if (!comms_healthy) return LIBUSB_ERROR_IO;
  if (!identification_ || identification_->protocol == PandaProtocol::CHIMERA_MAILBOX) return LIBUSB_ERROR_ACCESS;
  int result = libusb_control_transfer(device_, 0x40, request, param1, param2, nullptr, 0, bounded_timeout(timeout));
  return record_error(result > 0 ? LIBUSB_ERROR_IO : result);
}

int PandaUsbHandle::bulk_transfer(unsigned char endpoint, unsigned char *data, int length,
                                  unsigned int timeout, bool read) {
  std::lock_guard lock(mutex_);
  if (!connected) return LIBUSB_ERROR_NO_DEVICE;
  if (!comms_healthy) return LIBUSB_ERROR_IO;
  if (!identification_ || (!read && identification_->protocol == PandaProtocol::CHIMERA_MAILBOX)) return LIBUSB_ERROR_ACCESS;
  if (length < 0 || (length > 0 && !data) || endpoint != (read ? 0x81 : 3)) return LIBUSB_ERROR_INVALID_PARAM;
  if (length == 0) return 0;
  int transferred = 0;
  int result = libusb_bulk_transfer(device_, endpoint, data, length, &transferred, bounded_timeout(timeout));
  if (transferred < 0 || transferred > length) return record_error(LIBUSB_ERROR_IO);
  if (read && (result == 0 || result == LIBUSB_ERROR_TIMEOUT)) return transferred;
  if (result < 0) return record_error(result);  // Never retry an uncertain write.
  if (transferred != length) comms_healthy = false;
  return transferred;
}

int PandaUsbHandle::bulk_read(unsigned char endpoint, unsigned char *data, int length, unsigned int timeout) {
  return bulk_transfer(endpoint, data, length, timeout, true);
}

int PandaUsbHandle::bulk_write(unsigned char endpoint, unsigned char *data, int length, unsigned int timeout) {
  return bulk_transfer(endpoint, data, length, timeout, false);
}
