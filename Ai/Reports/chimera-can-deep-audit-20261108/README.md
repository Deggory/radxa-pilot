# Chimera CAN deep audit — 2026-11-08

## Result and correction

Correct original Chimera detected. Native and independent raw USB observations
still receive no CAN frames. A newly established artifact/source difference is
the strongest software lead: the matching nightly initializes all three speeds
to 250 kbit/s, then applies nonzero saved SYS speeds. Current saved values
500 / 500 / 0 therefore predict **500 / 500 / 250 kbit/s at boot**, not the
preserved source's fixed 500 / 500 / 500. The 500 kbit/s sensor on printed CAN2
would not match that boot configuration. Zero means keep the default in this
nightly's boot routine; the desktop's “Disabled” label is not its behavior.

This corrects the operational interpretation of QA49/50/53/55; the earlier
source observations remain accurate for the preserved source, which differs
from the signed application. The controller's current BTR register and physical
bit timing were not read. Later runtime speed changes and electrical faults
are not excluded. This is a compelling boot mismatch, not a measured repair.

## Fresh observations

- Baseline project radxa/q8b at 1d5b9cc77c0b07518c35586eae6bd0296de11dc4, clean.
- Product Chimera, bbaa:ddcc, serial 3a0044001651333038373636,
  v1.0.0-DEV-de193215-DEBUG; USB 003/021, sysfs3-4.1 behind a hub.
  Interceptor DAC Bench is a separate unit, 003/018; not opened by our guarded probes.
- D3+D4 application signature equals all128signature bytes in saved nightly.
  This fingerprints the signed application; it is not a whole-flash readback.
- Native20.114390901s:1909CAN batches,20health messages,0frames on USB0/1/2;
  chimeraOldMailbox16 profile, clean exit0. Empty batches do not count as frames.
- Independent10.001553321s:43665bulk reads of endpoint0x81; every return code0,
  every actual length0, **zero payload bytes before parsing**,20health reports.
  This rules out the host decoder, DBC or bus selection discarding those bytes.
- Fresh flash read twice: identical776bytes, valid magic/CRC, SHA256
  4b025b9e65b10475013ed39f8d4e66abf780a7cbe6ebf18833d952e46ffe3b22.
  Debug3/output15/watchdogoff; saved rates500/500/0/0kbit/s, other entries empty.
- Read1023bytes from debug UART ring via E0IN/ring0 until empty. Retained text
  includes INIT, WATCHDOG DISABLED, IGN0, angle mappings false. A finite ring
  can truncate/drop logs; no timeout text here does not prove initialization succeeded.
- All application requests were IN-only: D6/D2/D3/D4/FF/E0 and bulk-IN.
  No heartbeat, CAN data TX, bitrate/config write, reset or flash. Reading debug
  consumes that ring's buffered text; its exact returned bytes are preserved.
- Readers stopped/USB released; final target USB owner list empty; REA target closed.
  Existing Core Config GUI remains open/disconnected. Sensor kept on printed CAN2.

Current sensor power/common ground are owner-confirmed from QA52, not newly
measured. The previous direct Waveshare 0x25 sensor success is separate evidence.
Only CAN2 has the sensor attached; monitoring all three does not physically
qualify three connectors or prove the sensor was transmitting in this interval.

## How CAN is read

| Printed connector | MCU controller | USB/cereal bus |
| --- | --- | --- |
| CAN0 | CAN1 | 0 |
| CAN1 | CAN2 | 1 |
| CAN2 (current sensor) | CAN3 | 2 |

Sensor CANH/L -> transceiver -> STM32 receive FIFO0 -> RX interrupt -> raw
receive queue -> USB EP1/bulk-IN0x81 -> libusb -> mailbox decoder -> cereal `can`.

The current native executable is openpilot/selfdrive/pandad/pandad. main.cc
opens PandaUsbStatusSession in panda_usb_status.cc; panda_usb.cc selects the
pinned device/interface0, checks D6version/D2health43, and reads endpoint0x81.
chimera_usb.cc buffers and validates16-byte legacy mailbox records. Each record
contains RIR, RDTR, RDLR and RDHR. Standard ID=RIR>>21, extended ID=RIR>>3,
DLC=RDTR&15, bus=(RDTR>>4)&255; receipt/remote records are excluded.
panda_usb_publish.cc publishes valid received frames to `can`.
This passive startup is separate from managed driving/control admission.

The independent usb_audit.py selects the exact sysfs bus/address/serial/product,
uses libusb directly, and records transfer lengths **before calling either
native or Python decoders**. It retains transferred bytes even with timeout.
All lengths were zero. There is no dependence on RetroPilot message IDs for
this raw observation. OEM0x25 would be visible even without angle mappings;
turning it into canonical RetroPilot0x50 is a separate integration task.

## Signed-image analysis, reproducible evidence

Original27976-byte signed image SHA256
 e35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b.
Header declares27848application bytes plus128signature bytes; VERS2;
repository debug RSA public key verifies the signature. Thumb reset0x08009ab8,
application load0x08004000. Extraction and ARM objdump output are retained here.
Only identified reachable functions and their literal pools were interpreted;
the full linear dump also decodes constants as apparent instructions.

- Reset calls main at0x08009b20; flash snapshot validation/pointer initialization
  reaches startup at0x08009cfa.
- 0x08009d02 loads2500, 0x08009d06/0a stores it into speed array RAM
  0x200000cc/d0/d4 (units100bit/s). r6=0x20000000 is loaded from0x08009e90.
- r7=10 is established at0x08009c74 and preserved over calls. With SYS type1,
  0x08009f44..6a loops i=0..2, reads uint16 at SYS+15+2*i, skips zero,
  stores value*10 into speed[i]. Saved500thus becomes5000; zero leaves2500.
- 0x08009d14..1a clears can_silent mask atRAM0x200000c8, then calls the
  all-controller initializer0x0800798c. It loops0..2 through0x08007960.
  Speed helper0x0800755c selects the array value and calls0x08005fa6.
  The latter computes prescaler=30000/speed-1 and writes BTRoffset0x1c.
  With24MHz peripheral timing and8quanta,2500means250kbit/s;5000means500kbit/s.
- The RX0 wrappers0x080074fc/7500/7504 select buses0/1/2 and branch into
  common receive0x08006ef0. This reads RF0Roffset0x0c and FIFO0offset0x1b0.
  0x0800743e..6e tags RDTR, unconditionally queues raw frames and releases FIFO.
  No populated sensor mapping is required to reach that raw enqueue.
- Filter helper0x08006090..615c writes bank0and14 and activation0x4001,
  retaining the source's questionable generic handling. ST's official HAL
  treats CAN3as14independent banks and accesses CAN1/2shared filters through
  CAN1. This is a firmware quality issue to investigate, but valid bank0is
  also enabled; bank14alone is not established as the CAN2 zero-RX cause.
- The actual nightly USB DE handler is jump-table entry0x080081f8 ->0x08008412:
  accepts wValuebus0..2, stores wIndex at speed[bus], calls can_init(bus).
  Unlike preserved main.c's bus0-only branch, it supports temporary CAN2rate.
  This is a static contract observation; no OUT request was sent to test it.

REA open_binary accepted the raw artifact and supplied its digest. Its overview
failed provider_unavailable: no configured Ghidra/IDA and missing Hopper.
No REA pseudocode or complete function graph was obtained. Used the existing
ARM objdump explicitly instead; no engine installation/configuration change.
Exact upstream source remains unrecovered; fresh GitHub commit lookup returned
HTTP422 “No commit found for SHA”, not a fresh404. Official HAL fetched200,
SHA256306376efc392862121c3f656948c308b3e98cf0ec6df8f5b8194fcdd487c0a2c;
RM0430 web fetch exceeded size limit and local download timed out.

## Ranked diagnosis and next test

1. **Bitrate mismatch at boot — strong artifact evidence.** Current SYS CAN2zero
   retains250k in matching nightly versus sensor's previously working500k.
   Current register timing remains unmeasured. A temporary bus2=5000runtime
   request is the narrowest controlled follow-up; then capture raw0x25 again.
2. **Electrical supply/standby/termination — still unresolved.** Earlier labelled
   5Vrail4.5V and CANH/Labout1..1.15V each are historical. Actual transceiver
   VCC/STB/RXD and waveform are unmeasured. NXP's TJA1042reference allows VCC
   4.5..5.5V and has undervoltage standby; board markings/version still need
   physical qualification. USB version/health do not prove CAN supply health.
3. **Filter/controller/interrupt initialization — residual firmware leads.**
   Generic filter setup and ignored llcan_init return values warrant review;
   matching timing alone would not prove these states. Health error fields are
   not comprehensive ESR/TEC/REC readbacks, and voltage/current are placeholders.
4. **Wrong USB device, wrong observed bus or host parser — tested against.**
   Exact identity/signature match; all raw USB buses observed; no bytes arrive;
   nonempty host vectors work. These results do not electrically qualify the board.

Prepared follow-up, **not executed**: after an explicit change to the existing
write hold, select only this original Chimera, vendor controlOUT0x40/requestDE,
wValue2/wIndex5000/no payload; require completion, release USB, then repeat native
and raw capture. This changes RAM/controller timing, not flash; the saved CAN2
zero remains and reboot would restore250k. Do not reset or use CLI SYS Save,
Format or flashing to perform that test. Existing bridge blocks OUT and is kept
so. If approved, first qualify/guard the actual handler and setup again, and
record actual controller acceptance. Do not silently route around the hold.

## Verification and preserved scope

23Python unittest cases pass; native/Python parity covers432mailbox and5health
vectors. Five existing native executables pass: test_chimera_usb, test_panda_usb,
test_panda_usb_can, test_panda_usb_publish, test_panda_usb_link. Nonempty frames,
all3buses, standard/extended IDs, allDLCs, split records, malformed input and
session/publication boundaries are covered; fake transports do not prove wire RX.
Initial pytest attempts failed (first relative path, then pytest absent in venv);
used the existing unittest framework, with no dependency installation.
All76legacy manifest entries, native executable SHA and canonical DBC SHA remain
unchanged. No firmware/host product/DBC/hardware changes, push or upstream update.
Skills used: debugging, Unlazy, REA, source/graph explanation, git/documentation.
Graph metadata was insufficient/stale for this behavior; direct source/artifact
pins take precedence. Teacher/student memory is documentation, not model training.

Primary references: [ST official CAN driver](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/master/Src/stm32f4xx_hal_can.c),
[NXP TJA1042](https://www.nxp.com/docs/en/data-sheet/TJA1042.pdf).
