## November 6 — Passive USB CAN and isolated diagnostics implemented

QA28/T08b1: pinned legacy F4v17 USB entry now receives classical CAN and publishes
`can` plus complete JSON diagnostics on `customReservedRawData1`. No pandaStates:
hardwared reads ignition without Event.valid gating. RawData0/Thneed untouched.
Fragment age500ms, bounded RX and strict parser errors close ownership; no TX,
reset/retry/cache/SPI fallback. Native build/9native programs,25Python regressions,
ASan/UBSan and checksum mutation check pass offline. No physical USB/IPC session,
pins, firmware or onroad admission.23firmware hashes/7448-byte image, Ocelot39dirty
entries/19hashes, archive and canonical DBC preserved. Updates held; no push.
Next T08b2: profile-aware pandaStates admission, supported-field validity/ignition
and reconnect/backoff policy. New Chimera operational firmware/bench work remain.

Accepted scope: passive RX/isolated status only, unchanged firmware/outputs and
protected camera/model/Thneed. Source modules: panda_usb_can.{h,cc},
panda_usb_publish.{h,cc}, status session, main.cc, SConscript and services.py;
three new/extended native fixtures and test binary ignores. No new runtime pins.

Verification: actual target/9native programs;25Python regressions; strict parser
and fake-libusb real-backend/session sanitizers with no SPI source linked; Capnp/
JSON roundtrips and full-width values; checksum mutation fails; five invalid
native invocations exit2; Q8B main.o has no legacy-thread symbol; services Ruff
and SCons AST pass. Detailed source/version/hash/output pins in receipt. Builds
initially needed correct SCons options, activated toolchain PATH and installed
json11 header path; corrected without weakening checks. No physical USB/publisher
run or fresh firmware build/test suite needed because all23source hashes and
retained raw image are unchanged. CAN6 RTR omission, XOR limits, missing supported-
field/onroad validity, sequential status delays, reconnect/backoff and physical
power/VBUS/recovery/MCU enforcement remain unresolved.

Workflow: source-first selected local source and native/GNU artifacts; relevant
incremental, TDD, API, code-review, Git and docs skills. No unrelated REA/delegated
review claim. Protected Ocelot/archive/DBC verified against saved pins. Updates
held; no fetch/update/push. Commit this verified increment with evidence; normal
pandaStates policy is the exact next step. No project edits predated this slice.

[Receipt](../Evidence/chimera-usb-receive-20261106.json).
[Contract](../../chimera/docs/USB_PASSIVE_RECEIVE.md).
