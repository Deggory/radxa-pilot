# Chimera modern USB roadmap — November 5, 2026 UTC

Owner requested research/explanation before code, dedicated chimera/folder,
modern Panda-compatible USB for Radxa Sunnypilot, Core Config, direct input/bus
and onboard relay preservation, OBD-C explanation. Read teacher/student startup,
routers,Q&A,current state,inbox and relevant source reports. Reconciled Git:
parente888f939/Panda8a16e089/child150f9371clean; Ocelotd87892faalreadydirty.
No updates/check/fetch/merge; existing upstream hold retained.

Created new independent board evidence/docs folder,capabilitymap,draftSPEC,
20taskroadmap,USB/config/CoreConfig designs,hardware map,immutable references,
originalnightlybundle,official OBD-Creference drawing.94manifestentries/93copied;
all75priorreview sourcehashesmatch. Restrictedlinkerhashonly; no blanket Ocelot
license asserted. Prior report/test and matchingREAartifact evidence reused,
not new runtime coverage. Official wiki/STdatasheet webtext and comma GitHub
harness/drawing read; STlocaldownloads timedout,RM0430notreviewed; receipts saved.

Key conclusions:nativehostSPIonlyrequiresUSBbackend; modernCANframingclassical
limits; distinctidentity/earlyfiltering avoids startupwrites/H7flash; Core Config
needsmoderntransportandversionedtransactionalsettings; bus0reports/parser2need
sourcecontract; allTXroutesneedMCUpolicy; PB0relayonlyknown3CAN0powerpaths,PA2/PB1
OBD-Ccodeexistsbutroutingunknown. Latestownerincludesonboardrelaypreservationin
plan,supersedingearliergenericexclusionforthiscircuitonly; no hardwareoperation.

Skills applied: spec-driven-development,api-and-interface-design,
planning-and-task-breakdown,source-driven-development,documentation-and-adrs,
git-workflow-and-versioning,code-review-and-quality. User explicitly requested
roadmap before change,so capability/spec/plan delivered together as proposed,
without pretending design approval. Source-firstREAroute used; no unnecessary
binarytoolrun. No application/firmware source changes,flash/config/CAN/relay/
actuatoraction,pushorupdate. Implementation remains pending ownerroadmapreview.

Both Q&A logs QA-20261105-13 synchronized; central/project current/state/topic/
session/worklog/handoff and decision scope updated. NextT01/T02boardmemory,
recovery,identity/RPCandbussourcecontracts; isolated passivebench later. Checks
recorded in chimera/evidence/validation.json; no historical tests called fresh.

Fresh closeout checks passed:94manifest entries/93copied files and75prior hashes;
ZIP/image27976bytes andofficialOBD-Csha256;14board/reportMarkdown28links;
student121docs/365relative links/8source repos4254entries;QA13equal;protected
Panda/opendbc/Ocelotstateunchanged andSunnypilotAi-onlydiff. Historical21runtime
tests/189mailbox/336modernvectors were not rerun. Evidence in
`/home/radxa/comma/chimera/evidence/validation.json`; no productbehaviorclaim.

Board evidence committed locally: `306c0c8e1fc073d12af9f6d4f6c2d93c90a0a2a7` on `planning/modern-usb`; no remote/push. Initial new-repository commit lacked Git identity; reused the existing Sunnypilot identity locally and retried successfully,without changing global configuration.
