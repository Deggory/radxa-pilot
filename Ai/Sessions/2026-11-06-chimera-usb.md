# Native USB connection — November 6, 2026

Owner “proceed”, context QA-20261106-10/11. Accepted increment T06b: native USB
factory/backend, explicit pins and T02a identification, fake failure tests;
no live device access or startup enablement. Teacher Carrot/deep review and
Ocelot main/USB sources consulted throughout. Source-first, TDD, incremental,
interface design, Git and review skills used; no REA artifact result invented.

Baseline96ea6bd79; Panda8a16e089/opendbc150f9371; Carrot69a2d3be and Ocelotd87892fa
with original dirty bytes preserved. Existing comma-deps-libusb1.0.29.post103
supplies header/static library; official synchronous/device docs identify1.0.30
and confirm used API semantics. No dependency/system installation or vendor update.

New panda_usb.h/.cc: RAII selection/ownership, unique explicit serial+version,
known normal VID/PID, descriptors/config1/interface0, identification before return.
No set_configuration, kernel detach, reset/recovery or vendor OUT in discovery.
Busy/unconfigured devices refused. Control/bulk mutex, <=1second, no retry;
partial timeout reads retained, uncertain writes/unhealthy/dead states surfaced.
Original Chimera only D6/D2 zero-parameter IN and CAN IN; no OUT. Source dispatch
ignores direction, so IN alone is not enough for passive command protection.

New fake libusb C test never links real libusb;33scenario groups cover success,
failure, exclusive claim, duplicates, cleanup and transfer behavior. Real static
library link test executes only empty-pin guard (fake test proves before init).
Native SCons pandad/all focused targets pass,443identification cases/interface/
CAN codec and15Chimera Python tests pass. Strict ASan/UBSan fake build/run passes.
Initial int/enum list deduction error corrected in test; injected control error
leaked across test iterations, located group6 and reset before next open. gdb
was not installed; no install, suppression, skipped check or product relaxation.
Existing build PWD warning remains non-fatal.

Changed build/ignore, three board docs, source/tests and notebook. Review covers
bounded lengths, no retry, exact resource acquisition/release, pin-before-init,
read-only Chimera request allowlist and no hidden managed activation. API docs:
https://libusb.sourceforge.io/api-1.0/group__libusb__syncio.html
https://libusb.sourceforge.io/api-1.0/group__libusb__dev.html

T06b is offline complete; constructor/list/managed startup unchanged and still
SPI. T05 legacy59-byte status adapter next, then T08 protected managed USB
selection; physical qualification and T01/T03 firmware remain separate gates.
No hardware/daemon/USB enumeration, firmware/DBC/config/CAN/relay, push or update.
Exact checks and hashes: Ai/Evidence/chimera-usb-20261106.json.
