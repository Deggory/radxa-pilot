#include <cstring>
#include <limits>
#include <stdexcept>

#include "common/tests/native_test.h"
#include "selfdrive/pandad/panda_usb_publish.h"
#include "json11/json11.hpp"

void test_messages() {
  PandaUsbCanFrame frame{0x123, 2, 2, false, {0xaa, 0xbb}};
  MessageBuilder can;
  build_usb_can_message(can, {frame}, 123, true);
  auto bytes = can.toBytes();
  AlignedBuffer aligned;
  capnp::FlatArrayMessageReader reader(aligned.align(reinterpret_cast<const char *>(bytes.begin()), bytes.size()));
  auto event = reader.getRoot<cereal::Event>();
  CHECK(event.which() == cereal::Event::CAN && event.getValid() && event.getLogMonoTime() == 123);
  CHECK(event.getCan().size() == 1 && event.getCan()[0].getAddress() == frame.address);
  CHECK(event.getCan()[0].getSrc() == 2 && event.getCan()[0].getDat().size() == 2);
  CHECK(event.getCan()[0].getDat()[0] == 0xaa);

  LegacyF4StatusSample sample{};
  sample.health.voltage_mV = 0xffffffffU;
  sample.health.ignition_line = sample.health.controls_allowed = true;
  sample.health.safety_mode_raw = 0xfd;
  sample.health.interrupt_load = 0.375f;
  sample.health.wake_on_can = true;
  for (unsigned i = 0; i < 3; ++i) sample.can[i].can_number = i;
  sample.can[2].total_rx_cnt = 0xffffffffU;
  const PandaIdentificationPin pin{"selected", "version \"quoted\""};
  const uint64_t end = std::numeric_limits<uint64_t>::max();
  MessageBuilder status;
  build_usb_status_message(status, pin, &sample, end - 1, end, UsbObservationState::OBSERVING);
  auto status_bytes = status.toBytes();
  AlignedBuffer status_aligned;
  capnp::FlatArrayMessageReader status_reader(status_aligned.align(reinterpret_cast<const char *>(status_bytes.begin()), status_bytes.size()));
  auto diagnostic = status_reader.getRoot<cereal::Event>();
  CHECK(diagnostic.which() == cereal::Event::CUSTOM_RESERVED_RAW_DATA1 && diagnostic.getValid());
  auto raw = diagnostic.getCustomReservedRawData1();
  std::string error;
  auto json = json11::Json::parse(std::string(reinterpret_cast<const char *>(raw.begin()), raw.size()), error);
  CHECK(error.empty() && json["schema"].int_value() == 1 && !json["operational"].bool_value());
  CHECK(json["version"].string_value() == pin.firmware_version && json["endNanos"].string_value() == std::to_string(end));
  CHECK(json["health"]["voltage_mV"].number_value() == 4294967295.0);
  CHECK(json["health"]["ignition_line"].bool_value() && json["health"]["controls_allowed"].bool_value());
  CHECK(json["health"]["safety_mode_raw"].int_value() == 0xfd && json["health"]["interrupt_load"].number_value() == 0.375);
  CHECK(json["health"]["sound_output_level"].is_null());
  CHECK(json["availability"]["observationOnly"].bool_value());
  CHECK(json["availability"]["unavailablePandaFields"].array_items().size() == 6);
  CHECK(json["availability"]["unavailablePandaFields"][0].string_value() == "spiErrorCount");
  CHECK(json["health"].object_items().size() == 27 && json["controllers"].array_items().size() == 3);
  CHECK(json["controllers"][0].object_items().size() == 27);
  CHECK(json["controllers"][2]["total_rx_cnt"].number_value() == 4294967295.0);
  for (auto state : {UsbObservationState::FAILED, UsbObservationState::CLOSED}) {
    MessageBuilder failure;
    build_usb_status_message(failure, pin, nullptr, 1, 2, state);
    auto f = failure.getRoot<cereal::Event>().asReader();
    CHECK(f.which() == cereal::Event::CUSTOM_RESERVED_RAW_DATA1 && !f.getValid());
    auto payload = f.getCustomReservedRawData1();
    auto j = json11::Json::parse(std::string(reinterpret_cast<const char *>(payload.begin()), payload.size()), error);
    CHECK(j["health"].is_null() && j["controllers"].array_items().empty());
  }
  for (unsigned scenario = 0; scenario < 4; ++scenario) {
    MessageBuilder bad;
    bool rejected = false;
    try {
      if (scenario == 0) build_usb_status_message(bad, pin, nullptr, 1, 2, UsbObservationState::OBSERVING);
      if (scenario == 1) build_usb_status_message(bad, pin, &sample, 1, 2, UsbObservationState::FAILED);
      if (scenario == 2) build_usb_status_message(bad, pin, &sample, 2, 1, UsbObservationState::OBSERVING);
      if (scenario == 3) build_usb_can_message(bad, {frame}, 1, false);
    } catch (const std::invalid_argument &) { rejected = true; }
    CHECK(rejected);
  }
  MessageBuilder invalid_can;
  build_usb_can_message(invalid_can, {}, 1, false);
  CHECK(!invalid_can.getRoot<cereal::Event>().asReader().getValid());
}

void test_chimera_messages() {
  const PandaIdentificationPin pin{"selected", "v1.0.0-DEV-de193215-DEBUG"};
  ChimeraHealth sample{};
  sample.uptime = 0xffffffffU;
  sample.ignition_line_raw = 255;
  sample.safety_model_raw = 17;
  sample.safety_param_raw = -32768;
  for (auto state : {UsbObservationState::OBSERVING, UsbObservationState::FAILED, UsbObservationState::CLOSED}) {
    MessageBuilder message;
    build_chimera_usb_status_message(message, pin, state == UsbObservationState::OBSERVING ? &sample : nullptr,
                                    1, 2, state);
    const auto event = message.getRoot<cereal::Event>().asReader();
    CHECK(event.which() == cereal::Event::CUSTOM_RESERVED_RAW_DATA1);
    CHECK(event.getValid() == (state == UsbObservationState::OBSERVING));
    auto raw = event.getCustomReservedRawData1();
    std::string error;
    auto json = json11::Json::parse(std::string(reinterpret_cast<const char *>(raw.begin()), raw.size()), error);
    CHECK(error.empty() && json["profile"].string_value() == "chimeraOldMailbox16");
    CHECK(!json["operational"].bool_value() && json["availability"]["observationOnly"].bool_value());
    CHECK(!json["availability"]["pandaStates"].bool_value());
    CHECK(json["availability"]["preservedSourcePlaceholders"].array_items().size() == 7);
    CHECK(json["controllers"].array_items().empty() && json["health"].is_null());
    if (state == UsbObservationState::OBSERVING) {
      CHECK(json["rawHealth"].object_items().size() == 18);
      CHECK(json["rawHealth"]["uptime"].number_value() == 4294967295.0);
      CHECK(json["rawHealth"]["ignition_line_raw"].int_value() == 255);
      CHECK(json["rawHealth"]["safety_model_raw"].int_value() == 17);
      CHECK(json["rawHealth"]["safety_param_raw"].int_value() == -32768);
      CHECK(json["rawHealth"]["voltage_mV"].is_null());
    } else {
      CHECK(json["rawHealth"].is_null());
      CHECK(json["state"].string_value() == (state == UsbObservationState::FAILED ? "failed" : "closed"));
    }
  }
  for (unsigned scenario = 0; scenario < 3; ++scenario) {
    bool rejected = false;
    try {
      MessageBuilder invalid;
      if (scenario == 0) build_chimera_usb_status_message(invalid, pin, nullptr, 1, 2, UsbObservationState::OBSERVING);
      if (scenario == 1) build_chimera_usb_status_message(invalid, pin, &sample, 1, 2, UsbObservationState::FAILED);
      if (scenario == 2) build_chimera_usb_status_message(invalid, pin, &sample, 2, 1, UsbObservationState::OBSERVING);
    } catch (const std::invalid_argument &) { rejected = true; }
    CHECK(rejected);
  }
}

int main() { return run_native_test([] { test_messages(); test_chimera_messages(); }); }
