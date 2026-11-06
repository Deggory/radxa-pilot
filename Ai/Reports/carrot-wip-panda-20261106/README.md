# CarrotPilot carrot-wip: F4 Panda and USB reference

Fetched 2026-11-06 from `ajouatom/openpilot`, branch `carrot-wip`, at
`69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7` (commit time10:27:29UTC).
The owner's “carriotpilot-wp” was interpreted as this branch, consistent with
the teacher's earlier CarrotPilot reference. Exact-name repository searches did
not find `carriotpilot-wp` or `carrotpilot-wp`.

**It retains older F4 Panda support and a native USB host, while using six-byte
checksum CAN records. It does not use Chimera's old16-byte mailbox USB format.**

These31selected source files are frozen references, not a full build tree or an
installed port. [Manifest](SOURCES.json) pins every Git blob/SHA-256; both project
and Panda MIT license files are retained. No upstream code was copied into our
firmware or managed Sunnypilot runtime. Read the
[verification result](validation.json) and
[verification script](/home/radxa/comma/chimera/evidence/carrot-wip-20261106/verify_reference.py).

## What “legacy Panda” means here

The checked tree has7,319entries and is not truncated. Panda is an ordinary
vendored directory, not a gitlink; no root `.gitmodules` or `legacy_panda` path
was found at this commit. Older-board support lives in normal `panda/` source.
The previous November1 lateral comparison at4a555c75 remains historical evidence;
this new pin is a focused Panda/host study, not a refreshed lateral evaluation.

| Layer | CarrotPilot source evidence |
| --- | --- |
| F4 target | `panda/SConscript` uses Cortex-M4,STM32F413xx,app0x08004000 |
| Firmware builds | `panda/board/SConscript` builds both `panda`(F4) and `panda_h7`, plus variant images |
| Older board definitions | `stm32f4/board.h` includes white/grey/black/uno/dos and board detection |
| Python device types | F4 white/grey/black/uno/dos; separate H7 list; internal UNO/DOS/TRES/CUATRO |
| Native transport | `PandaCommsHandle` interface, `PandaUsbHandle`, `PandaSpiHandle` |
| Native selection | `Panda` constructor tries USB then SPI; listing unions/deduplicates serials |
| Native build | SConscript links usb-1.0 and compiles panda_comms.cc plus SPI |
| Multiple boards | Internal board sorted first; each board receives4host-bus positions via bus_offset |

Supporting an older F4 board is separate from retaining its earliest wire format.
The native header is6bytes, has XOR integrity, preserves partial records and
returned/rejected metadata. The Python encoder also exposes FD metadata; the
F4 bxCAN hardware path stays classical and constructs RX packets withfd=0.

## Compared with our two existing paths

| Contract | Existing Chimera/Ocelot | Fetched CarrotPilot | Current Sunnypilot/Panda |
| --- | --- | --- | --- |
| CAN USB record |16-byte STM32 mailbox |6-byte header+payload,XOR |6-byte header+payload,XOR |
| Health bytes |43 |59 |49 |
| Per-bus health |No current compatible endpoint |64 |64 |
| Version RPC DD |No active matching handler in inspected local source |3bytes: health17,CAN4,CANhealth5 |8bytes: two32-bit layout hashes |
| Managed native transport |Dedicated receiver exists separately; not a managed replacement |USB+SPI |SPI-only |
| Default app addresses |F4130x08004000 |F4 0x08004000;H7 0x08020000 |H7target0x08020000 |

The current native firmware/header pins remain Panda8a16e089 and
opendbc150f9371; protected Sunnypilot baselinec1811280. Same CAN frame bytes do
not make status RPCs, firmware identity, SPI transport or startup compatible.
Current health has a packed flag field and16-bit voltage/current; Carrot retains
separate byte flags and32-bit voltage/current. Never cast59bytes as49or43.

## Actual USB/lifecycle path and limitations

`PandaUsbHandle` uses libusb, configuration1/interface0, bulkOUT3/bulkIN81.
Its native enumeration and connection filter is **3801:ddcc only**. Python's
USB list accepts bbaa and3801, but that does not extend the native filter.
Our historically observed Chimera isbbaa:ddcc, so even its identity would require
an explicit protected adapter; sharing PID alone is insufficient.

The constructor immediately gets hardware type and resets CAN communications.
Python connect performs initialization writes: default heartbeat-disable/power
save, communications reset and all3bitrates. Its FD-auto initialization loop is
commented out. Thus this client also is not a harmless read-only Chimera probe.

The wrapper lists DFU devices and recovers them, constructs/flashes every listed
Panda, chooses an image from the MCU type, verifies signatures, resets on first
run and launches native pandad. It also has a Tesla-specific firmware selection
path. These are supported-Panda lifecycle policies, not Chimera permissions.
Do not run this daemon/client/flasher against our board as an experiment.

Native `get_state/get_can_state` accept nonnegative lengths without an exact-size
check. Some control reads/writes retry until disconnect without a retry budget;
the error handler clears connected only for NO_DEVICE. Bulk timeout returns the
transferred byte count. These source limitations need explicit bounded handling
if this implementation is used as a starting point. They are not measured faults
on a live device or reasons to copy old behavior into the new host backend.

## Firmware enforcement and board differences

F4 bxCAN RX builds CANPacket metadata/checksum, calls safety_fwd_hook, routes a
permitted forwarded copy through can_send with skip_tx_hook, then calls
safety_rx_hook/ignition handling and publishes RX. Normal can_send invokes
safety_tx_hook and produces rejected receipts for blocked requests. Forwarding
therefore has its own policy path; hook presence does not qualify every safety
mode. Heartbeat loss selects silent/power save; startup selects silent.

This is materially more complete than inspected Chimera's unguarded host send
and direct generated-message mailbox writes, but it is not a measured RetroPilot
production policy. Current disabled-only mode39 and all earlier actuation holds
remain unchanged. No vehicle/control safety profile was adopted here.

The F4 common bus map defaults0→CAN1,1→CAN2,2→CAN3, but Panda harness orientation
can swap0and2. Chimera's fixed physical Cores/ADAS/vehicle roles must remain
explicit. Panda board detection also probes PA4/5/6, used by Chimera inputs.
Black-Panda PB1 is a USB load-switch output; Chimera uses PB1 for OBD-C ignition.
Panda's harness relay is not Chimera's PB0 power relay. A real Chimera board
definition must retain its input frontends, ADCs, transceiver enables and power
state machine instead of impersonating black Panda or reusing its GPIO init.

## Implication for the roadmap

This provides a concrete candidate for T03's F413 support and T06's native USB
transport boundary. It reduces the need to invent low-level USB/bxCAN plumbing.
Keep our chosen current Sunnypilot protocol/status/identity contract and adapt
reviewed components deliberately. Do not replace the host base or flash an
unmodified Carrot Panda image. App-address coincidence is not proof of image
size, bootstub/signature/config preservation or Chimera GPIO compatibility.

T01/T02partition/identity/bus-source decisions and the existing isolated passive
bench gates are still pending. This source study does not complete those tasks.

## Fresh checks and coverage limits

31source files match GitHub tree/blob SHA-1 and SHA-256.189classical frames across
3buses/7addresses/lengths0–8 match our current Python encoder exactly;4,158split
checks across both pure decoders and378checksum corruptions pass. A native C++
fixture using the unchanged actual health headers reports59/64/6/49/64bytes;
Python health formats agree. The check never imports a Panda class or opens a
device. It is not a full host or ARM firmware build, FD test, runtime USB or
hardware qualification. Tooling failures/corrections are retained in
[the tooling note](tooling-limits.txt).

Primary source paths at the pinned commit:
[F4 build](https://github.com/ajouatom/openpilot/blob/69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7/panda/SConscript),
[native USB](https://github.com/ajouatom/openpilot/blob/69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7/openpilot/selfdrive/pandad/panda_comms.cc),
[native codec](https://github.com/ajouatom/openpilot/blob/69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7/openpilot/selfdrive/pandad/panda.cc),
[health](https://github.com/ajouatom/openpilot/blob/69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7/panda/board/health.h),
[wrapper](https://github.com/ajouatom/openpilot/blob/69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7/openpilot/selfdrive/pandad/pandad.py).
