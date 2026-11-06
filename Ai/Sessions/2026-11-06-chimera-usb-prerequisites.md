# Chimera progress and startup prerequisites — November 6, 2026

Owner requested a plain-language summary and to proceed with power/VBUS, UID and
recovery requirements before USB startup. Accepted T03b3a: source-backed contract,
progress guide and small read-only boot-facts helper. Baseline
f75b1e831e4190e7f62eb21f70bf0f7606976015, radxa/q8b clean. Teacher/student routers,
resume/inbox/handoff/state/tasks/Q&A and previous evidence read. Teacher October4
hardware/recovery notes followed into original code/archive before asking owner.
No unrelated upstream check/advance; November4 hold remains.

[The progress guide](../../chimera/docs/PROGRESS_EXPLAINED.md) explains firmware on MCU versus host software on Radxa, what each tested
piece does, and the lack of flashed/end-to-end operation. Host libraries/identity
are offline; managed startup remains SPI. Firmware startup remains parked. Input
pins/relay/OBD-C preservation is distinct from sampling/configuration/actuation.
[The startup contract](../../chimera/docs/USB_STARTUP_REQUIREMENTS.md) establishes power/VBUS/descriptor/UID/watchdog/recovery and packaging
requirements. Old main/USB force BVALOEN/BVALOVAL; common init uses PA9/PA10 UART,
so no verified VBUS route may be inferred. Wiki supports USB/IGN power sources but
supplies no exact power tree/isolation/draw qualification. Unknown VBUS cannot
permit attachment; bus-only and mixed/external power require different evidence.
No supply profile, current value, detector pin or valid-session override approved.

New original boot_facts.c/.h: trusted read32-only callback reads UID3words at
0x1FFF7A10, raw RCC_CSR0x40023874 and FLASH_OPTCR0x40023C14, then repeatsUID3words.
At most8reads, blank/allFF/inconsistent UID returnsfalse with destination unchanged;
success outputs ascending12bytes and raw flags. No write32 use, flag clearing,
watchdog start/feed, option/flash write or USB operation. Added to ARM build/KEEP
and retained-symbol checks. Existing EP0 formatter supplies24hex serial chars;
synthetic historical serial fixture proves ordering, not a current physical read.
Read callback cannot report bus faults; valid F413 address space is prerequisite.
Raw registers do not prove watchdog stopped or firmware authenticated. No global
context/main call. Driver/startup/board/CAN/protocol/MMIO/USB model hashes unchanged.

Primary evidence: Ocelotd87892fa+originaldirty, ST CMSISV2.6.0 UID/CSR/OPTCR mapping;
ST flash_ex.h at6ef30cf0ef6cc29ad518f37b9e6de89b6b815f90, bloba8217d36ce6f385bafab96b34e8a6df23e131b27,
software/hardware IWDG selector definitions. Retrieved read-only through GitHub
connector into ignored references. Official Chimera wiki rechecked through web.
No full RM0430/USB compliance review. Source-driven, documentation, incremental,
TDD, Git/interface and self-review workflows applied; no unrelated REA provider
analysis. Readable source and simple archive/hash inspection follow fast path.
Existing approved roadmap/scope used; no new permission inferred from skill text.

Recovery source/hash audit only: bundle8158f29132e88bff946cbe23b72d269fa2e6aeb4d6ca5aba7b9539ac04ec043c
contains27976byte signed app SHAe35df778ad0d865d6eab5b7763b9a9081b3923bea11fbb8c2949a40d37796a9b
and11204byte bootstub build SHA2533c53d853826c1fa4e9198d1126446ae5a412adc6ba03c1d5a8171287353ca.
The latter is not an installed dump. All17historical config archive file hashes
match; eight valid/one erased classifications are previous evidence, not new
board reads. October4 failed candidate and restored nightly readbacks/full power
cycle are genuine historical observations; current board state remains unknown.
Legacy bootstub reads word0 length/checks VERS/RSA; new raw word0 is MSP and needs
future compatible packaging. Preserve installed bootstub/config erase sector;
no option unprotect/signature policy change or rollback command executed.

TDD RED absent boot_facts source/header → GREEN. New native fixture exercises
65536snapshot patterns with no writable callback, all three UID-instability
positions, blank/allFF/null checks, destination canaries and existing serial
formatter. Compiler/sanitizers and ARM retention used; no tests skipped/weakened.

Actual checks from Sunnypilot root:

- CHIMERA_TOOLCHAIN_PREFIX=/home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi- python3 -m unittest discover -s chimera/firmware/tests -v
  —21tests pass in15.424s; all prior driver/clock/EP0/control/CAN/GPIO/negative
  artifact/stack/vector/copy-tree checks pass alongside new snapshot cases.
- python3 chimera/firmware/build.py --toolchain-prefix /home/radxa/.local/ocelot-build-tools/usr/bin/arm-none-eabi-
  —pass; raw6608bytes/projected legacy6744/114688budget; SHA256
  409c0940a0ae7f4603c06b408ae3ee305cec3ee0efebcbba3391f116f249fb48.
  Globals8bytes/stack4096 unchanged. GCC13.2.1/binutils2.42/nativeGCC13.3.0.
- .venv/bin/ruff check chimera/firmware —pass. No source dependency on archives,
  ST download or external SDK. No install. Local unsigned ignored artifact only.

[The receipt](../Evidence/chimera-usb-prerequisites-20261106.json) pins exact commands/output/source/test/build and historical hashes.
Ocelot39dirty entries/all19source hashes, clean archive224cfa6, native host/safety
and canonical DBC preserved. Both notebook layers/QA20/roadmap updated. Next
T03b3b can compose a detached startup/service module with fault tests. Actual
attachment still requires exact power/VBUS/current-recovery evidence; status/bulk
endpoints/managed admission/Core Config/acquisition/MCU policy remain later tasks.
No device read/write/flash/reset, config/option/DBC write, actuation, upstream
reference advance or push. No new VCDS finding in this study.

Closeout checks: memory verifier passes140documents/447relative links/246optional
workspace links/8source repositories/4254indexed entries.102active Chimera links
resolve. Final source/test SHA256, Ruff and diff checks pass.
