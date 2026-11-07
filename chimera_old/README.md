# Original Chimera / C2-era baseline

Created November7,2026 at the owner's request. This is a separate copy of the
preserved legacy Chimera implementation. The newer `../chimera/` work is halted.

- `firmware/chimera/main.c`: original application, inputs, reports and relay loop.
- `firmware/chimera/{can,usb,chimera}.h`: old CAN/USB and persistent configuration.
- `firmware/{boards,drivers,inc,crypto}/`: shared dependencies and original headers.
- Firmware startup/root headers, public certificates and build references retained.
- `recovery/chimera.bin.signed`: saved historical `de193215` Chimera image.
- `recovery/bootstub.bin` and `manifest.json`: historical bundle companions.
- `SOURCES.json`: per-file source, SHA256, version and explicit exclusions.

Copied source is Ocelot `d87892fa25ef2a2474110b97bfb5245ee818b534` plus its saved
local changes, including `main.c`/`chimera.h`. It is byte-for-byte preserved.
The historical image's exact source `de193215490b4906aa74aae6aa426b8f4740f3fa`
has not been recovered. "C2-era" identifies the requested legacy route, not a
verified match to the image installed on your C2 or board. Original Chimera's
mailbox16/health43 protocol differs from stock C2 Panda CAN5/health50.

This step copies files only. Existing Sunnypilot host integration is unchanged.
Future work can adapt Sunnypilot to the pinned original Chimera protocol here.
No compilation, signing, flashing or hardware operation was performed.

The inherited build files are references, not a ready build command: the old
Atollic linker script is excluded because its header prohibits redistribution;
private signing keys and generated objects are also excluded. This is not a
complete reproducible build or proof the historical bootstub accepts a new image.
Original copyright/license notices are retained. Do not add flashing to this copy
or replace it with stock Panda firmware as part of a source-preservation step.
