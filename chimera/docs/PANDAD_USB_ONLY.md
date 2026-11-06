# Pandad SPI removal

November6,2026. Owner correction: remove the SPI backend from pandad itself,
including its source/build/classes/default construction/listing. Earlier permission
to retain a generic SPI path is superseded.

Implemented: spi.cc/PandaSpiHandle/SPI buffers and device listing removed. The
native Panda constructor takes an explicit serial/version pin, opens the qualified
USB factory and accepts current-profile status only; opening performs no reset or
configuration write. Legacy F4 uses its separate passive observation session.
The retained managed-control helper also takes a pin, with no automatic listing.
It is not exposed by the executable's startup entry.

All platforms now require `pandad --usb-status SERIAL VERSION`; the Python wrapper
requires PANDAD_USB_SERIAL/PANDAD_USB_VERSION and execs that exact command. There
is no generic wrapper recovery/DFU/automatic flash/internal-reset path, no bare
native fallback, and no implicit firmware version or selected device. No defaults
or runtime pins were installed. Core Config and board firmware are unchanged.

The two hardware-only tests for the removed SPI corruption and implicit internal
Panda recovery/flashing paths were removed with those features. Their complete
source remains in Git at baseline17f933a8. Replacement coverage uses fake libusb,
explicit startup pins, current-profile refusal, no-write construction and cleanup.
These are not removed assertions for still-supported behavior. No hardware test
was run. Panda Python/vendor firmware/reference libraries outside pandad are not
this deployment's backend; their retained wire statistics named spi remain data.

Validation: native build/10native programs,42Python tests and strict fake-USB
ASan/UBSan; five invalid/legacy CLI calls exit2 before IO. nm/ar checks show no
PandaSpiHandle symbol or spi.o in the executable/archive. Deleted ignored stale
spi.o/archive were rebuilt. An interrupted build resumed before verification;
vendored USB linking/include paths were corrected without suppressions.
[Receipt](../../Ai/Evidence/chimera-remove-spi-20261106.json) contains exact pins,
changes and results. No physical USB, flash/reset/config/CAN TX, update or push.

Next in the same accepted task: status field-availability metadata and consumer
checks before enabling ordinary PandaState publication. USB observation remains
passive; new firmware still parked and unflashed.
