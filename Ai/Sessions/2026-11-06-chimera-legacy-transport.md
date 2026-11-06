# Legacy Panda transport foundation — November 6, 2026

Owner: “build in a way our sunnypilot supoort the legency panda”.
Accepted steering: retain modern Chimera goal and add older F4 Panda host
compatibility in reviewed increments. Initial hardware family matches Carrot's
white/grey/black/UNO/DOS; not every historical firmware protocol is assumed.

Implemented T06a: four-method abstract PandaCommsHandle with shared serial and
connection/health state plus virtual destructor. PandaSpiHandle derives from it;
Panda owns unique_ptr<PandaCommsHandle>. Existing SPI constructor/list, packet
implementation, buffer limits and updater/safety behavior remain unchanged.
Added offline native ownership/error/destruction test and SCons target/ignore.
New compatibility doc and roadmap preserve incomplete task identities/status.

Evidence: current project112041136, Panda8a16e089, opendbc150f9371, Carrot69a2d3be
transport/F4 source and earlier self-contained reports. Original Ocelotd87892fa
and workspace Chimera224cfa6 remain reference inputs, unmodified. No new firmware,
restricted linker import or REA artifact/runtime analysis. Used API/interface,
TDD, incremental, planning, source-driven, Git and review skills. No delegation.

TDD: test compile failed on missing PandaCommsHandle before implementation;
strict standalone compile/test then passed. ARM64 project SCons successfully
built native pandad and test_panda_comms/test_pandad_canprotocol; both binaries
ran successfully. Fifteen existing Chimera Python tests pass. Initial unsupported
--extras flag corrected after reading SConstruct; next capnpc-not-found resolved
by activating existing venv. Retain these invocation limits; no installation or
warning suppression introduced. Existing PWD warning did not fail the build.

No USB backend or old health decoder is claimed. Full legacy managed support
needs profile validation, USB I/O/status and protected lifecycle. Next T02
read-only identity/profile contracts then T06b USB; board T01/T03 stays separate.
No hardware/daemon/CAN/relay/config/flash/upstream/push action. Validation receipt
Ai/Evidence/chimera-legacy-transport-20261106.json records actual checks.
