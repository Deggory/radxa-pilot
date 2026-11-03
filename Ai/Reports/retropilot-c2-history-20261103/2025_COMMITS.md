# RetroPilot C2: every 2025 commit in the reviewed history

A commit is a saved change in Git. This guide explains each change in plain English; click its number to see the original patch.

**53 commits dated 2025:** 28 in the C2 application, 20 in its CAN library, 2 in Panda and 3 in Cereal. They span February 6–August 14, 2025. The application changes span May 15–August 14. This is the 2025 portion of the pinned C2 comparison and its supporting-library comparisons, not a claim that every repository or branch the author used has been reviewed.

The complete comparisons also contain 30 older commits from 2021/2022. Those include inherited upstream and other-author work; they are not counted as new 2025 RetroPilot development. The recorded application author is Kevin Roscom or Comma Device; see the [original application timeline](TIMELINE.md) for attribution.

**What this work built:** a retrofit car port, CAN message definitions, module readings, steering/accelerator/brake/relay commands, cruise-button behavior, tuning support, build/OS changes, shared messages and an initial Panda safety policy.

These rows summarize source changes. The title saying that openpilot drives is the author's report, not an independently verified driving test. WIP means work in progress. The final Panda policy is not evidence of complete actuator safety.

## RetroPilot car/application — 28 commits

| Date (2025, UTC) | Commit | Original title | Plain-English change |
| --- | --- | --- | --- |
| 05-15 | [c3c6ad17](https://github.com/RetroPilot/retropilot/commit/c3c6ad1700a99b7388df1fb95d0e25e73bdd3d2e) | update submodules | Pointed the project at RetroPilot versions of Panda, Cereal and the CAN library. |
| 05-15 | [b79e2fc7](https://github.com/RetroPilot/retropilot/commit/b79e2fc7eef3c94b74bb12cb9665f7adf6ecf50f) | compile on ubuntu 24.04 | Updated build, compiler and video-library compatibility so the old software could compile on Ubuntu 24.04. |
| 06-05 | [b243c4a5](https://github.com/RetroPilot/retropilot/commit/b243c4a5a828cfd396fbd5a986f9d405c89aed11) | update opendbc | Selected the CAN-library version that integrates the Ocelot message definitions. |
| 06-10 | [64a819b4](https://github.com/RetroPilot/retropilot/commit/64a819b42eae4a481a0912bf44ef28f938e7d276) | WIP RP Retrofit car port | Added the first RetroPilot car port: vehicle selection, state reading, command generation, settings and joystick changes. Marked work in progress. |
| 06-14 | [72b5328b](https://github.com/RetroPilot/retropilot/commit/72b5328ba19b3c1a41931ba2143cb8b9bb73a3c1) | update to latest commit | Updated supporting libraries, added module-selection defaults and revised steering/brake/relay/joystick handling. Also included OS and inherited base updates. |
| 06-26 | [be4e6f5a](https://github.com/RetroPilot/retropilot/commit/be4e6f5a1c9633a89dd4b5bf1b6957b213ada78f) | WIP ECU detection | Expanded readings for different accelerator, brake and steering modules; connected steering-angle readings. Module detection remained work in progress. |
| 06-30 | [2a174790](https://github.com/RetroPilot/retropilot/commit/2a174790561fe621277df12993a583b9fa5e5092) | update with new signals | Added CAN readers and expected message rates for speed, cruise buttons and optional modules; temporarily set steering rate to zero. |
| 06-30 | [ae77cb88](https://github.com/RetroPilot/retropilot/commit/ae77cb887b4ff150043f9f6f9014e3aa47138ec9) | update | Selected an updated CAN library with a speed-pulse scaling correction. |
| 06-30 | [72ea730f](https://github.com/RetroPilot/retropilot/commit/72ea730f88a6b1c0a8a02333d4c5c06391110cfe) | ugh | Selected an intermediate CAN library correction for the speed-message counter. |
| 06-30 | [395e1f24](https://github.com/RetroPilot/retropilot/commit/395e1f24ab59ee6b975e1abe830466d8185b191e) | ... | Selected the corrected four-bit speed-message counter definition. |
| 07-01 | [07ef4f91](https://github.com/RetroPilot/retropilot/commit/07ef4f91f504064ba29a09a5bf46f67e81601e39) | attach signals | Calculated vehicle speed from speed-sensor pulses, connected steering-rate readings and fixed steering-signal names. |
| 07-13 | [047c72b8](https://github.com/RetroPilot/retropilot/commit/047c72b8ad1e6ecbe05117af9153be6d9793b123) | NEOS 20 from GitHub | Changed NEOS 20 operating-system download addresses to GitHub. |
| 07-13 | [64c7e67f](https://github.com/RetroPilot/retropilot/commit/64c7e67f921f93d5ef42a34061d4d284600a0bef) | Merge branch 'c2' of github.com:RetroPilot/retropilot into c2 | Merged the two C2 development histories and their vehicle-state changes. |
| 07-13 | [05965c06](https://github.com/RetroPilot/retropilot/commit/05965c068ae2a891d120bee0039280bc810ef02b) | fix typo | Attempted to fix relay message names and selected the signed steering-angle CAN definition; another relay naming fix followed. |
| 07-13 | [15c3b366](https://github.com/RetroPilot/retropilot/commit/15c3b3665ea9cc33b4516e2c473e4d0289aced18) | fix more typos | Fixed iBooster brake message names and the relay signal/message ordering. |
| 07-13 | [6edcb2a1](https://github.com/RetroPilot/retropilot/commit/6edcb2a15527a26c64088cf3686338f248969bdf) | cast to int | Converted relay status to a whole number before reading its indicator bits. |
| 07-13 | [14be5858](https://github.com/RetroPilot/retropilot/commit/14be5858eac4d2ddbadee36aee27fb31cbf6e2b3) | cast to bool | Converted left/right indicator readings to true/false values. |
| 07-13 | [8e4c76b5](https://github.com/RetroPilot/retropilot/commit/8e4c76b5ff5e336dda81ab70ff4196a353d0c843) | get rid of debug print | Removed repeated module-detection debug printing. |
| 07-15 | [2aa9e5ef](https://github.com/RetroPilot/retropilot/commit/2aa9e5ef7d94ed3ff82fc602cbc17292157acbfe) | bon voyage? | Selected the author's accelerator/steering/iBooster setup, increased throttle scaling and revised joystick relay mapping. |
| 07-15 | [57f06590](https://github.com/RetroPilot/retropilot/commit/57f06590a0328cbc0c35859b41af7a8aa4caa880) | vibe coding the cruise state machine bc i just wanna goooo | Implemented cruise-button behavior: on/off, set, resume, cancel and remembered set speed. |
| 07-15 | [6e292258](https://github.com/RetroPilot/retropilot/commit/6e292258d823e28b14c525d6c4633340336d650d) | engaging now | Hard-coded the reported gear to Drive and corrected the driver-brake signal to allow engagement with that setup. |
| 07-15 | [17116c0a](https://github.com/RetroPilot/retropilot/commit/17116c0aa0c89ebab388ace0fc244d8c7f3d76bd) | fix typo on filename | Corrected the tuning module filename. |
| 07-15 | [12f283e0](https://github.com/RetroPilot/retropilot/commit/12f283e0616a45500438351559f0c79ec092f9c3) | fix bad import | Corrected an import from the tuning module. |
| 07-16 | [4ed61e6f](https://github.com/RetroPilot/retropilot/commit/4ed61e6f32114dfbf789027c0edc8b15bb2c16c2) | WIP: op drives, need to do more QOL | Author reported that openpilot drives. Changed accelerator/brake interaction, speed-button steps and steering tuning; added tuning reload while inactive and changed event/UI handling. |
| 07-24 | [159d3b32](https://github.com/RetroPilot/retropilot/commit/159d3b3225ef8209d0f473e22ab3080122117b29) | live tuning WIP | Added speed-dependent steering limits and revised throttle, brake and live-tuning settings. Still marked work in progress. |
| 07-24 | [228d647c](https://github.com/RetroPilot/retropilot/commit/228d647c831bc426843a16ab2623d226d492386f) | add override bit from interceptor | Connected the steering interceptor's driver-override flag to vehicle state. |
| 07-24 | [f5838b5c](https://github.com/RetroPilot/retropilot/commit/f5838b5c5a9fcbe5eec862e839eecef6e5352103) | update opendbc | Selected the corrected steering-override/status CAN definitions. |
| 08-14 | [b9a942ef](https://github.com/RetroPilot/retropilot/commit/b9a942efd3cb210127bb5efb5cf9ccf6a811c728) | remove Pipfile from lfs | Stored Python dependency files as ordinary Git files instead of Git LFS pointers. |

## CAN library and DBC — 20 commits

| Date (2025, UTC) | Commit | Original title | Plain-English change |
| --- | --- | --- | --- |
| 02-06 | [a4d54fb0](https://github.com/RetroPilot/opendbc/commit/a4d54fb0f9c6204b963c29418280f25ba3929994) | yeah. | Added steering-interceptor command and feedback messages. |
| 02-06 | [97f1449b](https://github.com/RetroPilot/opendbc/commit/97f1449b5fd6b3c3dbf0670d7b9eadeea28ef7b3) | fix ocelot steering status msg addr | Corrected the steering-interceptor feedback message address. |
| 02-14 | [27b146d2](https://github.com/RetroPilot/opendbc/commit/27b146d20ea035ce828d90962f459708b6c4be03) | add new signals | Added cruise buttons, wheel speeds, steering angle/rate and revised pedal definitions. |
| 02-22 | [8d5b4d57](https://github.com/RetroPilot/opendbc/commit/8d5b4d57c2088b0e66dd3ec37bba3e270cb9586a) | add throttle actuator | Added accelerator-actuator command and feedback definitions. |
| 02-25 | [6d8b114a](https://github.com/RetroPilot/opendbc/commit/6d8b114acd9fd9df8d215ba0f00ff29927a70c9b) | remove deprecated dbcs | Removed obsolete Ocelot/Smart Roadster definition files. |
| 06-05 | [f71a6fc5](https://github.com/RetroPilot/opendbc/commit/f71a6fc525998ae48620be480a48291904715827) | merge ocelot | Integrated Ocelot definitions and checksum/counter handling into the active CAN library. |
| 06-10 | [0fe13b3a](https://github.com/RetroPilot/opendbc/commit/0fe13b3a11ff525607da05ac24bd44c931cc90e9) | add Relay Core to DBC | Added RelayCore command and feedback messages. |
| 06-14 | [e41610f4](https://github.com/RetroPilot/opendbc/commit/e41610f4ea449406d6766ea8f2e01cc555136913) | update dbc | Reorganized message layouts and updated brake/steering names, including iBooster. |
| 06-26 | [a03f2557](https://github.com/RetroPilot/opendbc/commit/a03f2557fefa47adcd5b2709611319975e734995) | add new signals | Reworked steering-angle, engine and cruise-button message definitions. |
| 06-27 | [0b1ab361](https://github.com/RetroPilot/opendbc/commit/0b1ab361a115baea30e2de69c50940bcdf76ffa2) | define speed and engine signals better | Added a separate vehicle-speed message with CAN-speed and pulse measurements; revised engine data. |
| 06-27 | [63e15913](https://github.com/RetroPilot/opendbc/commit/63e159131765a38d057507bd958d08be51f3d624) | update cruise control msg with ADC | Expanded the cruise-button message with two raw sensor readings and status fields. |
| 06-27 | [233a1af6](https://github.com/RetroPilot/opendbc/commit/233a1af6920d48e497680c881eca1b9e734a6b42) | endianness fixes | Corrected the byte order of cruise-button sensor readings. |
| 06-30 | [0a6e66d7](https://github.com/RetroPilot/opendbc/commit/0a6e66d779ea278c0128bcb559deb90bdd34c099) | more signals - wrapping it up | Added steering rate, ignition status and driver-brake status. |
| 06-30 | [dff50616](https://github.com/RetroPilot/opendbc/commit/dff506167c2c4d8edd8dc65b6b0e6b37fee8ce1d) | fix typo | Corrected speed-pulse measurement scaling. |
| 06-30 | [d04567a3](https://github.com/RetroPilot/opendbc/commit/d04567a3f9a5470644a0a6dd1738a4660d466efd) | dammit | Made an intermediate adjustment to the speed-message counter width. |
| 06-30 | [6f38c538](https://github.com/RetroPilot/opendbc/commit/6f38c538359200c8514a0eba1aa0fa5c448a774b) | ... | Corrected the speed-message counter to four bits. |
| 07-13 | [7cbd799d](https://github.com/RetroPilot/opendbc/commit/7cbd799d71671e1603ef0ebcc0f9039986ace9fd) | signed angle | Allowed negative steering angles by making the angle field signed. |
| 07-14 | [775de849](https://github.com/RetroPilot/opendbc/commit/775de84978e622b29a09054d1361c5c58d6797b8) | DBC fixes | Corrected accelerator-actuator and RelayCore status-bit positions. |
| 07-24 | [ecdc3407](https://github.com/RetroPilot/opendbc/commit/ecdc340733bb040cbdabf8f395ce03daa320f0d3) | add override bit to icore | Added the driver-override flag and expanded steering-interceptor feedback. |
| 07-24 | [6b90fafe](https://github.com/RetroPilot/opendbc/commit/6b90fafe59e81822bfae58e4ecb080248e9de40d) | fix typos | Corrected the override/status/counter layout; this is the final shared DBC version selected by C2. |

## Panda firmware — 2 commits

| Date (2025, UTC) | Commit | Original title | Plain-English change |
| --- | --- | --- | --- |
| 06-10 | [89ac4452](https://github.com/RetroPilot/panda/commit/89ac4452543fe6915ee7e49aecfed27e7441083c) | WIP Retropilot Panda safety | Added an initial RetroPilot Panda safety policy and message rules, explicitly work in progress. |
| 06-14 | [9e6d47f6](https://github.com/RetroPilot/panda/commit/9e6d47f63675d5a45170ae7972c24412034dc136) | continue modifying safety | Revised that unfinished safety policy. The resulting policy still has integrity-check, message-length and actuator-limit gaps. |

## Cereal shared messages — 3 commits

| Date (2025, UTC) | Commit | Original title | Plain-English change |
| --- | --- | --- | --- |
| 05-15 | [7406e44f](https://github.com/RetroPilot/cereal/commit/7406e44f7024d7f2457acd89494bb211b373c1d2) | make compile on Ubuntu 24.04 | Updated C++ messaging compatibility for Ubuntu 24.04 builds. |
| 06-10 | [58bc67b1](https://github.com/RetroPilot/cereal/commit/58bc67b1d4fdf40a196eaff9cf5c442cb6580520) | add new safety model in enum | Added the RetroPilot safety-model identifier to the shared message schema. |
| 06-14 | [a7193d0f](https://github.com/RetroPilot/cereal/commit/a7193d0f0e472f90709e6671ce6ff01d1534c2a5) | relay control msg | Added a shared message field for relay-control requests. |

## Sources, scope and current Radxa limits

Source snapshots: [application patches](commit-history.json), [application comparison](parent-compare.json), [CAN-library comparison](opendbc-compare.json), [20 CAN-library commit patches](opendbc-2025-commits.json), [Panda comparison](panda-compare.json), and [Cereal comparison](cereal-compare.json).

Pinned tips: application b9a942efd3cb210127bb5efb5cf9ccf6a811c728; opendbc 6b90fafe59e81822bfae58e4ecb080248e9de40d; Panda 9e6d47f63675d5a45170ae7972c24412034dc136; Cereal a7193d0f0e472f90709e6671ce6ff01d1534c2a5. GitHub C2 branch was rechecked on 2026-11-03 and still matched the application pin. Commit dates use the saved author dates in UTC.

The [adaptation report](README.md) explains which ideas were carried into modern Sunnypilot on Radxa Q8B and which remain pending. This historical list does not mean all 53 changes were copied or that our BeamNG/Chimera control loop has been tested. Current vehicle command output remains disabled.
