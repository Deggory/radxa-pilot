# USB-only pinned startup

November6 owner correction: pandad's SPI backend is removed completely, including
its generic constructor/listing/build/source. Read [current migration contract](PANDAD_USB_ONLY.md).

Every platform requires PANDAD_USB_SERIAL and PANDAD_USB_VERSION in the Python
launcher; both are validated without defaults. It execs native
`pandad --usb-status SERIAL VERSION`. The native entry rejects bare/legacy
invocations before device access. There is no Python device-client import,
automatic flash/recovery/DFU/internal reset or transport fallback.

Serial is1..64non-space printable ASCII; version1..64printable ASCII, exact match.
Pins must identify reviewed compatible firmware; old command-number collisions
are recorded in [reference research](OCELOT_PANDA_DOCKER_REVIEW.md). Matching pins
is not authentication of arbitrary firmware. No pins are installed by this work.

The exclusively owned legacy F4v17 USB observation session publishes classical CAN
and complete isolated diagnostics. It accepts no current/original/new-Chimera
profile and exposes no raw handle/TX. Exact typed D2+C2 decoding, bounded RX,
fragment age/error cleanup and publication boundaries are in the
[passive receive contract](USB_PASSIVE_RECEIVE.md). Sequential reports are not an
atomic snapshot, and per-transfer bounds do not prove a whole-loop deadline.

The separate managed Panda class now opens qualified current USB only, with an
explicit pin and no constructor reset/configuration write. It is not selected by
the executable's observation entry. Generic control helpers remain unwired.
No normal PandaState admission/control/heartbeat threads are enabled here.

[Ignition validity](PANDA_IGNITION_VALIDITY.md) and
[offline legacy mapping](LEGACY_F4_PANDA_STATE.md) precede field-availability
metadata/consumer checks. Physical power/VBUS/recovery, new operational firmware
and bench qualification remain separate. Firmware, Core Config and DBC unchanged.
