# Independent native Chimera passive review — 2026-11-08

Verdict: **Approve the reviewed implementation for the stated offline passive
contract.** No Critical or Required findings remain in the reviewed production
diff. This is a source/offline review, not qualification of installed firmware,
USB hardware, wiring, vehicle operation or managed Sunnypilot admission.

Reviewed against baseline `249726e133e6e83241faae4699cca6eecb6a9c32` on
`radxa/q8b`, including untracked `chimera_usb.h`, `chimera_usb.cc` and
`tests/test_chimera_usb.cc`. Applied the local code-review-and-quality skill;
review was read-only except this requested report and a test executable in
`/tmp`. No source mutations, device accesses, network calls or pandad launch.

## Findings and contract checks

- **Resolved proposal concern:** The native decoder rejects bus3+, DLC9+,
  reserved RDTR bits and malformed standard IDs before filtering RTR/returned
  records. Non-receipt RIR bit0 is rejected; returned records can retain the
  TIR-origin bit and are never published as received CAN
  (`chimera_usb.cc:30–40`). This intentionally tightens the legacy Python
  decoder's bus3 allowance (`chimera_protocol.py:42`). Retained firmware
  distinguishes FIFO RX from TIR receipts (`chimera_old/firmware/chimera/can.h:230–234`,
  `313–320`), and maps three controllers (`142–148`).
- **Correctness/security:** The parser bounds input to4096 bytes and pending
  storage to one16-byte record, rejects zero/backwards timestamps and partials
  older than500ms, latches errors and discards all staged frames in a malformed
  feed (`chimera_usb.cc:21–44`, `chimera_usb.h:24–33`). No unchecked unaligned
  loads, reinterpret casts, variable-sized stack storage or unbounded pending
  accumulation were introduced.
- **Correctness/type boundary:** Health parsing requires exactly43 bytes,
  preserves all18 raw values including signed16-bit safety parameter, and
  accepts raw byte values without pretending they are qualified modern
  booleans/enums (`chimera_usb.cc:10–18`). The separate publisher preserves
  these18 values and labels seven retained-source placeholders, with
  observation-only/nonoperational availability and no per-bus health or
  pandaStates (`panda_usb_publish.cc:116–153`). Placeholder source:
  `chimera_old/firmware/chimera/main.c:110–136`.
- **Lifecycle/profile isolation:** Session opening admits only separately
  decoded F4v17 or old-Chimera reports; CURRENT remains refused. Wrong-profile
  sample calls return without I/O. Chimera sampling performs D2 only. Failure
  closes ownership, and close resets both decoders. The immutable protocol is
  retained after closure (`panda_usb_status.h:23–38`,
  `panda_usb_status.cc:30–98`). Main captures that profile before publication
  and uses it for observing, failure and closed labels (`main.cc:15–65`).
  Exception unwinding releases the session before failure publication.
- **Preserved F4 behavior:** F4 sampling body, F4 stream implementation and F4
  diagnostic builder are unchanged; the new sample guard selects the already
  required F4 protocol. The existing identity and USB transport guards are
  unchanged. Main still creates only CAN and isolated-diagnostic publishers;
  no control/sendcan/heartbeat/reset/flash path was added.
- **FYI — inherent protocol limit:** There is no mailbox record checksum.
  Structurally valid payload corruption or stale ECU content cannot be proved
  absent by this decoder. The contract and codec header explicitly retain this
  limit; no heuristic resynchronization or ECU sample-time claim is made.
- **FYI — verification boundary:** Main profile dispatch was inspected in
  source. Fake session/publisher tests were reviewed, but this reviewer did not
  execute those binaries or a composed main-loop fixture. Full target build,
  Python parity and final preservation checks remain the implementing agent's
  separate verification evidence.

## Exact independent validation

Read the contract, full production diff, added codec/header/test, changed fake
USB/session tests and changed publisher tests. Compared framing/health with
the retained old firmware and Python decoder. Reviewed existing USB ownership,
request and write guards. Tests include literal frames, all bus0..2/DLC0..8
combinations, standard/extended boundaries, all split points, filtering,
malformed-tail atomic rejection, time/size/null bounds, failure latch/reset and
health signed/unaligned boundaries. Session tests cover D6/D2-only traces,
wrong-profile calls, partial data followed by errors, explicit fresh reopen,
profile retention and refused CURRENT/bootstrap paths.

Independently compiled and executed the pure codec test only:

```sh
g++ -std=c++17 -Wall -Wextra -Werror -pedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer -I openpilot \
  openpilot/selfdrive/pandad/chimera_usb.cc \
  openpilot/selfdrive/pandad/tests/test_chimera_usb.cc \
  -o /tmp/chimera-native-independent-review
/tmp/chimera-native-independent-review
```

Result: exit0, no compiler warnings and no ASan/UBSan diagnostics. No mutation
experiment was performed because the assignment requires source to remain
read-only. Later test-only parity additions were not prerequisites for this
production-source verdict and must carry their own validation.

## Reviewed content pins

SHA256 at review (before later test-only additions):

```text
4c8e129536ff2bea023512fce2fd21d3be0143c9fbb131bf62f963d5e668722a  chimera_usb.h
51e6faa4067087b014ae9b8dbf43e4ef749094748d614518b9174f49437dad11  chimera_usb.cc
114311d95823125ac333b7e5eb315d19ed169206abdff5bced18f38cb31d68fc  panda_usb_status.h
8935c9e9b69ba378a0eaab06d4dec3fd885a8d1fc737ea0e6ff0c06237a134b2  panda_usb_status.cc
737d160740e604e48977a318f77f1e985e973d58b572c461abb2ef22cbc66ee8  main.cc
135c09505c0ba5d7de9404ed78c5e3f4086c7ed565d87d545f54bca89aee5d00  panda_usb_publish.cc
3b15410f656362cd662dc6143e4cba0cfd6f3b9b6535c98977728f5630d7eb92  tests/test_chimera_usb.cc
```

Paths in the pin block are relative to `openpilot/selfdrive/pandad/`.
