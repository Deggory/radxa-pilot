# USB-only Radxa status startup

November 6, 2026 — T08a. The Radxa entry path now reaches a native pinned USB
status session. This is status monitoring only: no CAN/pandaStates publication,
sendcan subscription, safety setter, heartbeat, relay operation or ready signal.
The new F413 image still parks/unflashed and is not admitted by this session.

## Entry points and pins

The Python [launcher](../../openpilot/selfdrive/pandad/pandad.py) checks
[pure startup selection](../../openpilot/selfdrive/pandad/usb_startup.py) before
legacy constructors, health probes, internal resets, DFU or firmware/recovery
logic. On Radxa Q8B, both `PANDAD_USB_SERIAL` and `PANDAD_USB_VERSION` are required.
There are no historical serial/version defaults. Serial is1..64ASCII characters
0x21..0x7E; version1..64ASCII bytes0x20..0x7E, matched exactly. No pins are installed
or chosen by this increment; historical evidence is not a current device pin.
Pins must identify reviewed compatible firmware, not an arbitrary version string
copied from a device. Older Panda command numbers can have different effects
even for IN requests ([documented DD collision](OCELOT_PANDA_DOCKER_REVIEW.md)).
Matching descriptors/version is not firmware authentication or proof that an
unreviewed image implements observation-only commands.

The launcher uses an argument list with `os.execv` to replace itself with native
`pandad --usb-status SERIAL VERSION`. Missing/partial/invalid pins or exec failure
raise without falling into the legacy path. No shell expansion, environment
mutation, helper process or broad Panda/DFU discovery is performed by this branch.
Existing Python client modules still import; their device constructors are not
called. On other platforms, specifying either USB variable requests this same
fail-closed path; with neither variable their preexisting launcher is retained.

Native [main.cc](../../openpilot/selfdrive/pandad/main.cc) dispatches the explicit
USB mode before affinity changes or legacy startup. A Q8B-target build rejects
bare/legacy invocation instead of calling `pandad_main_thread` or listing SPI.
The generic Panda SPI constructor/source remains for other entry paths, not a
Radxa fallback. A generic binary built without Q8B identity still requires the
explicit USB flag to use this route; use the correct target build.

## Session ownership and status

[PandaUsbStatusSession](../../openpilot/selfdrive/pandad/panda_usb_status.h)
owns the actual [pinned USB backend](../../openpilot/selfdrive/pandad/panda_usb.cc).
It exposes only sample/close/active; no raw handle or TX operation. Factory
identification requires exclusive interface0, configuration1, exact serial/version,
hardware/protocol qualification and initial health length. This session additionally
requires `LEGACY_F4_V17` and valid typed initial health59 before returning.

Current Panda49 and original Chimera43 remain separate and rejected by this
status session. New Chimera bootstrap remains unsupported by native identification;
phase0 cannot become operational through a host switch. These limitations are
explicit, not a new general support/admission claim.

One sample reads D2 and C2 selectors0/1/2 with the existing exact decoders, each
control-IN timeout1000ms. It returns all four sequential reports or no sample.
This is not an atomic/freshness-qualified MCU snapshot. `active()` means handle
ownership, not healthy hardware or controls readiness. There is no saved-sample
fallback. Any read/validation failure closes the session immediately; exceptions
also close before propagation. Repeated sample after close does no IO. Reopen is
explicit and repeats full identification, never substituting another serial.

Native mode logs completed samples, waits1000ms between cycles and closes on
SIGINT/SIGTERM or error. It issues no OUT/bulk/reset/config writes. A failed
session exits2, without internal retry/recovery/SPI fallback. The existing manager
may relaunch the process; no new restart/backoff policy is claimed. Per-transfer
timeouts do not establish a measured whole-startup or shutdown deadline.
Legacy C2 queries update firmware statistics; [bus-off polling semantics](LEGACY_F4_CAN_HEALTH.md)
still apply. Status-only host behavior does not prove autonomous firmware CAN TX
is silent. Electrical/recovery/MCU policy qualification remains separate.

## Verification and remaining work

Tests exercise the real USB factory/session with fake libusb and no SPI source
linked in the strict sanitizer executable. They cover pins, four-report ordering,
all failure positions, malformed initial/subsequent health, transport exceptions,
immediate cleanup, no stale-state fallback, explicit reopen and rejected profiles.
Python tests prove wrapper routing precedes legacy client/reset/recovery paths,
including partial pins, failed/returning exec and preserved non-Radxa default.
Native invalid-argument checks exit before device IO; the Q8B main object has no
legacy-thread reference. Exact outputs/hashes are in [the receipt](../../Ai/Evidence/chimera-usb-startup-20261106.json).
Source/CLI/GNU evidence; no real USB enumeration, daemon monitoring or hardware run.

T08a startup/status ownership is implemented offline. Next T08b is profile-aware
passive CAN reception and status publication with explicit validity/freshness,
exact-read hardening and reconnect policy. Full Sunnypilot operation, current/
original/new-Chimera profile integration and MCU enforcement remain pending.
