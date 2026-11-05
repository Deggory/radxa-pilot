## November 5 — rednose_repo is required, keep it

Owner asked what rednose_repo@28d4a7f is. Source confirms Kalman-filter estimation
used by localization and vehicle-parameter learning; build and Python imports
require it on Radxa. Parent4d6b4c87; child28d4a7f69e80e1c3e0d24ca0733d7daeaeade3d0
matches GitHub. QA-20261105-07 records purpose, consumers and unqualified sensor
integration limits. No source/submodule change, push or runtime test. Next owner
folder question; upstream updates stay paused and Chimera work remains separate.

Dependency evidence: SConstruct loads rednose_filter/REDNOSE_ROOT and builds
rednose's SConscript; pyproject installs rednose editable. locationd generates
PoseKalman/CarKalman filters. Pose observations include gyroscope, accelerometer
and camera odometry; paramsd uses vehicle speed/steering and motion estimates to
learn steering ratio/angle offset and stiffness. These are algorithms and build
infrastructure, not comma-only hardware files. Do not delete the dependency.

## November 5 — msgq_repo is required, keep it

Owner asked what msgq_repo@e7396e7 is. Source confirms core process messaging and
VisionIPC camera transport, used by build/cereal/camera/model paths on Radxa.
Parent3a4e97135; submodule e7396e76dadbb49e374d4b664ff6bbb43a39bcb0 matches GitHub.
QA-20261105-06 records the explanation and exact consumers. No source/submodule
change, push or runtime test. Next: further owner-selected cleanup questions.

Dependency detail: pyproject.toml installs msgq editable from msgq_repo;
SConstruct builds its SConscript and links messaging libraries. Cereal messaging
imports msgq; openpilot/system/camerad/webcam/camerad.py uses VisionIpcServer,
openpilot/selfdrive/modeld/modeld.py uses VisionIpcClient. Package includes native
queue IPC, VisionIPC and deterministic-test helpers. No device-specific removal
is justified by its external-repository name. GitHub's @hash is the saved gitlink.

## November 5 — Every tracked docs entry reviewed for cleanup

Source/public Radxa commitc93bd4197e3b0a45249be12638fb410f7e4474f1. Owner asked
what each docs file does and which to keep.29tracked entries inventoried,390999
logical bytes following the safety symlink. Recommendations only; docs unchanged.
[Complete file/purpose/keep inventory](../Evidence/docs-cleanup-review-20261105.json).

| File | Plain-English purpose | Recommendation |
| --- | --- | --- |
| AI_POLICY.md | Rules for AI-assisted changes, verification and disclosure. | Keep |
| CARS.md | Automatically generated catalogue of supported factory cars; reference only for our custom port. | Optional reference; preserve generator/icon links if removed |
| CONTRIBUTING.md | How developers submit changes and report bugs. | Keep |
| DEBUGGING_SAFETY.md | Use VS Code and replay to inspect C safety rules. | Keep; adapt paths as needed |
| GITHUB_RADXA.md | Our GitHub branches, cloning instructions and asset/submodule setup. | Keep |
| INTEGRATION.md | How supported stock-car assist features interact with openpilot. | Keep as reference |
| LIMITATIONS.md | Known limitations of lane, cruise, warning and driver-monitoring features. | Keep as reference |
| README.md | Starting page linking our Radxa, install, BeamNG and project guides. | Keep |
| RETROPILOT.md | Our custom car port, CAN transport, safety implementation and remaining gaps. | Keep; older sections need current BeamNG status refresh |
| SAFETY.md | Safety design principles, driver takeover and bounded actuation. | Keep |
| index.md | Upstream introduction used as the website home page. | Optional with website |
| serve.py | Builds and serves the documentation website. | Optional with website; tools/op.sh and docs workflow reference it |
| template.html | Page appearance and layout for that website. | Keep with serve.py, otherwise optional |
| concepts/logs.md | Recorded messages, route segments and camera log files. | Keep |
| concepts/safety.md | Symlink to ../SAFETY.md for website navigation; not a second independent text. | Keep while website uses this path |
| contributing/architecture.md | Contains only the Architecture heading. | Removal candidate; fix any references |
| contributing/feedback.md | How upstream comma users report driving/monitoring feedback. | Optional upstream reference |
| contributing/roadmap.md | Upstream openpilot plans; not the Radxa project plan. | Optional; replace only under separate scope |
| how-to/car-port.md | Explains interface, state reader, controller, DBC and safety files for a car port. | Keep |
| how-to/connect-to-comma.md | SSH/serial/ADB instructions for comma hardware. | Removal candidate for Radxa-only docs; navigation/image links must be adapted |
| how-to/replay-a-drive.md | How to replay recorded driving data; its CAN section is unfinished. | Keep; update incomplete/device-specific parts |
| how-to/turn-the-speed-blue.md | Beginner example changing speed-display color and deploying to a comma device. | Optional tutorial; not needed for Q8B setup |
| assets/comma-logo.png | Website logo. | Keep with website, otherwise optional |
| assets/favicon.svg | Website browser-tab icon. | Keep with website, otherwise optional |
| assets/icon-star-empty.svg | Empty rating star in the supported-car catalogue. | Keep with CARS.md |
| assets/icon-star-full.svg | Full rating star in the supported-car catalogue. | Keep with CARS.md |
| assets/icon-star-half.svg | Half rating star in the supported-car catalogue. | Keep with CARS.md |
| assets/icon-youtube.svg | Video-link icon in the supported-car catalogue. | Keep with CARS.md |
| assets/three-back.svg | Picture of comma-device connectors used by the connection tutorial. | Keep with comma connection tutorial, otherwise removal candidate |

Website files and navigation, generated car-list assets and tutorial images have
explicit consumers. A deletion must update those links/workflows together. Keep
safety/developer policies and our Radxa/RetroPilot guides. RETROPILOT.md has older
physical-profile/November3status statements; current RP-SIM-1 receiver/replay and
last0physical CANframes live in the BeamNG guide and student handoff. Retention
is not a claim that every old paragraph is current or that the port is qualified.
No executable/DBC/firmware/website content changed. Source-first Git/documentation
skills reused, no unrelated REA runtime claim or driving acceptance.

## November 5 — JetBrains folders removed and published

Owner explicitly authorized local and GitHub Q8B deletion. Removed six .idea/.run
files (6251bytes) in52afd7a3 and pushed radxa/q8b; independent REST/Git readback
passed. .github/.vscode hashes unchanged; master932ff06d/support150f9371 untouched.
Earlier three local documentation commits are now published too. QA-20261105-04
and dated removal evidence supersede the proposed-only status below. No runtime
source change/test or upstream integration. Next: owner-selected folders or the
separate Chimera receive task, preserving noOutput/relay limits and update hold.

[Removal receipt](../Evidence/editor-folder-removal-20261105.json). The earlier inventory retains pre-deletion sizes/hashes as historical evidence.

## November 5, 2026 — First four development folders inspected

Basee9275765d9eb8bc2670b1f453589213c353fe28e. Owner asked for a smaller project
and folder-by-folder explanation. Current phase explains existing contents before
any deletion. [File/size/hash inventory](../Evidence/editor-folder-audit-20261105.json).

| Folder | Actual contents | Recommendation for this VS Code setup |
| --- | --- | --- |
| .github | Issue templates/labels and test, model-build, release, documentation and maintenance workflows;162408bytes. | Keep for GitHub development; optional for local runtime. |
| .idea | CLion custom SCons targets and external build/clean tools;2639bytes. | Removable candidate if JetBrains editors are unused. |
| .run | JetBrains Debug/Release and BIG/SMALL UI launch shortcuts;3612bytes. | Removable alongside .idea if those editor shortcuts are unused. |
| .vscode | Editor formatting/search exclusions, extension recommendations and debugging shortcuts;2691bytes. | Keep for the owner's VS Code use. |

All four total171350logical bytes; removing the two JetBrains folders saves6251.
The release file selector already excludes .idea/.run/.github/workflows. None of
these folders changed. Native runtime/build/vehicle behavior was not tested or
changed. This narrow review does not authorize pruning other folders by name.
Source-first Git/documentation workflow used; no unrelated REA binary claim.

# Documentation and Radxa cleanup assessment

Reviewed 2026-11-03 at base d17dc3cd1e71fef7187b5a6267266a51f17a4c81.
Owner wants a simpler Radxa-focused project and asked whether docs/ is needed.

The existing docs tree had27 tracked files,366532 logical bytes (following the
safety symlink),440KiB allocated before the README edit. It is documentation
plus an optional site builder, not the comma-four hardware backend. Changing
these docs does not make the driving pipeline faster; no performance test was
performed. Updated docs/README.md to put actual Q8B install/status/handoff and
BeamNG guides first and label inherited upstream pages as references.

| Group | Current decision and reason |
| --- | --- |
| AI_POLICY.md, CONTRIBUTING.md | Keep development policy and attribution context. |
| SAFETY.md, concepts/safety.md, LIMITATIONS.md, INTEGRATION.md, DEBUGGING_SAFETY.md | Keep conceptual/debugging references; upstream/Panda-specific instructions are not Radxa qualification. concepts/safety.md is a symlink to ../SAFETY.md. |
| how-to/car-port.md, concepts/logs.md, how-to/replay-a-drive.md | Useful car-interface/log/replay guidance; replay page's physical CAN section is device-specific and incomplete. |
| CARS.md and icon assets | Upstream generated catalogue, not loaded car-port code or proof of Radxa/Chimera compatibility. Source generator and maintenance job write this file. |
| how-to/connect-to-comma.md, how-to/turn-the-speed-blue.md | Comma connection/tutorial instructions are not Q8B installation; reference-only during porting. |
| index.md, contributing/{architecture,feedback,roadmap}.md | Upstream public-site/community context; architecture page is currently only a heading. Not our port roadmap. |
| README.md, serve.py, template.html, assets/ | README now Radxa-first; site builder/theme/assets are optional on-board but needed by existing op docs/site workflow. |

Dependencies inspected: tools/op.sh docs function invokes docs/serve.py;
.github/workflows/docs.yaml builds/publishes the optional site;
.github/workflows/repo-maintenance.yaml invokes openpilot/selfdrive/car/docs.py
and stages docs/CARS.md. That generator defaults to docs/CARS.md and emits
relative icon paths. Root pyproject has an assets lint exclusion. A caching
test references remote upstream SAFETY.md, not this local file. git grep also
found a string match in the shipped comma updater binary; string presence is
not proof that the local docs tree is a runtime dependency and was not analysed
as one. No REA runtime/binary question was necessary for this docs decision.

Do not delete hardware directories based on names: actual
openpilot/common/hardware/__init__.py imports HardwareComma unconditionally,
and HardwareRadxa subclasses HardwarePc. Removing either dependency requires
an explicit selector/import/build change and appropriate tests. This inspection
is not a complete hardware/build dependency audit.

Recommendation: keep reference documentation while porting, use the short
Radxa entry page, and omit optional development/site files from a later verified
deployment package. No files were deleted, moved, hidden or executed. No
runtime/backend/build/CI configuration change. The owner's simplification
objective is recorded; a destructive whole-repository pruning was not attempted.
BeamNG optical/CAN requirements and pending implementation remain unchanged.

Skills: code-simplification, deprecation-and-migration, documentation-and-adrs,
Git workflow and source-first review. Validation: README links, notebook checks
and staged whitespace checks; no runtime test needed for the prose-only change.
