#pragma once

#include <memory>
#include <mutex>

#include "selfdrive/pandad/panda_identification.h"

struct libusb_context;
struct libusb_device_handle;

class PandaUsbHandle final : public PandaCommsHandle {
public:
  // Explicit normal-mode selection only. Claims interface 0 exclusively and
  // identifies before returning; never resets, detaches, configures or flashes.
  static std::unique_ptr<PandaUsbHandle> open(const PandaIdentificationPin &pin);
  ~PandaUsbHandle() override;
  const PandaIdentification &identification() const { return identification_.value(); }

  int control_write(uint8_t request, uint16_t param1, uint16_t param2, unsigned int timeout=TIMEOUT) override;
  int control_read(uint8_t request, uint16_t param1, uint16_t param2, unsigned char *data, uint16_t length, unsigned int timeout=TIMEOUT) override;
  int bulk_write(unsigned char endpoint, unsigned char *data, int length, unsigned int timeout=TIMEOUT) override;
  int bulk_read(unsigned char endpoint, unsigned char *data, int length, unsigned int timeout=TIMEOUT) override;
  void cleanup();

private:
  explicit PandaUsbHandle(const std::string &serial) { hw_serial = serial; }
  int record_error(int result);
  int bulk_transfer(unsigned char endpoint, unsigned char *data, int length, unsigned int timeout, bool read);
  libusb_context *context_ = nullptr;
  libusb_device_handle *device_ = nullptr;
  bool claimed_ = false;
  std::optional<PandaIdentification> identification_;
  std::mutex mutex_;
};
