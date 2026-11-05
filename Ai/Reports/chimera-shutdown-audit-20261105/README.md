# Chimera/Sunnypilot shutdown audit — 2026-11-05

Owner requested audit,GitHub update,then PC and Radxa shutdown. Scope is the
saved work and normal ordered shutdown; no upstream integration or firmware work.
Baseline Sunnypilotf63e84685/Chimera306c0c8/Panda8a16e089/opendbc150f9371;
Ocelotd87892fa pre-existingdirty source preserved. The nine unpublished parent
commits sincec93bd4197 affect Ai only; modern firmware is still proposed.

## Fresh verification

- Existing verifier rerun in the project's `.venv`:21tests pass,0errors/failures/
  skips;189mailbox and336modern vectors,all split/corruption checks; freshly
  compiled native communications library with fake controllers.
- 94manifest entries/93copies still match sourceSHA256; original nightly image
 27976bytes matches; protected Panda/opendbc/Ocelot state unchanged.
- 157selected files scanned for narrow private-key/GitHub/AWS credential patterns,
  no matches. This is a limited signature scan,not proof of every secret absence.
- Student notebook and synchronized Q&A/whitespace are checked at final closeout.
  No device enumeration/USB/CAN/config/relay/actuation action or upstream update.

[Fresh tests](tests.txt),[contract output](contracts.log),[layouts/native build](validation.json),
[source/artifact audit](audit.json),[Chimera GitHub readback](chimera-publication.json).

Two invocation-context failures are retained: [missing import root](initial-import-context.txt)
and [system Python missing dependencies](system-python-missing-dependencies.txt).
Using `PYTHONPATH` and the existing project `.venv` resolved both; no product code,
test assertion or dependency installation changed. Actual passing run used the
original verifier via importlib,with its OUT redirected to this report directory.
The original earlier evidence and frozen references are unchanged.

## Publication and shutdown

Chimera backed up privately at `Deggory/chimera`,planning/modern-usb,306c0c8;
Git/REST README blob verified,Actions disabled. The connected GitHub app returned
404for the new private repo; authenticated gh REST/Git were used instead. Initial
default-branch change raced the first push and returned422; after branch creation,
defaultplanning/modern-usb was set and read back. No force push or public exposure.

Sunnypilot target remains `Deggory/radxa-pilot:radxa/q8b`; preserve public master
932ff06d/defaultmaster and childsupport150f9371. Final receipt is saved in teacher
`Ai/Reports/chimera-shutdown-audit-20261105/` after the last push.

PC reached atpc@10.43.0.216using saved trustedHostKeyAlias10.42.0.216; first strict
connection without that known alias refused,not bypassed. No game/gateway/editor/
apt/dpkg process found in the selected process-name check; desktop user manager
running. Local VSCode autosaveafterDelay/backups0; explicitSaveAllnot independently
verified. Use normal GNOME shutdown respecting editor prompts/inhibitors,PC first,
Radxa last. No force kill/discard; physical poweroff is not asserted in advance.

Next restart: review `chimera/tasks/plan.md`,thenT01/T02board partitions/recovery,
identity/RPC/bus-source contracts. Inputs,3buses,onboard relay retained by scope;
firmware/managed bridge/active profiles remain unimplemented/unqualified.

## Actual requests

[Shutdown receipt](shutdown-request.json): PC normal shutdown initiated andSSH
unreachable; Radxa120snormal GNOME timer confirmedwaiting. No physical poweroff
claim. Final handoff/request publication follows the earlier source/audit backup.
