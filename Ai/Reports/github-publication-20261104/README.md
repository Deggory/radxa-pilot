# Radxa project publication — 2026-11-04

Public repository: https://github.com/Deggory/radxa-pilot

Owner authorized creating the repository from only the Sunnypilot project,
keeping original Sunnypilot master and the Radxa changes as another branch,
with the existing commits. Owner later explicitly selected public visibility.
This is a standalone public copy with full source history. The existing owner
Sunnypilot-network fork `Deggory/sunnypilot-pc` was left untouched.

| Branch | Published source |
| --- | --- |
| master | Original Sunnypilot8cf6ff9a33c94bdf2fcb02e228a9aef1a7e6dc7f;19,005commits |
| radxa/q8b | Actual Q8B project; original camera/Thneed/RetroPilot commits retained |
| opendbc/retropilot | Original child671f8c450fc74f5b8b90b2ee53124394108651ce and its custom RetroPilot history |

Original project0758b123 and all98 pre-task reachable IDs are retained.
Child's8 pre-task reachable IDs are retained too. Both previously shallow
repositories were unshallowed without changing any existing ID, source tree
or branch HEAD. The child now has3,344commits. Its seven local RetroPilot
commits are available in the supporting branch; parent Gitlinks preserve their
exact source pins. No rebase, squash, force push or history rewrite.

The only project configuration changes are `.gitmodules` pointing the
RetroPilot submodule to this owner repository/support branch, and `.lfsconfig`
pointing Radxa assets to its GitHub LFS storage. These are committed as
c7265864864c488ad4cdbdf65ae5cdefdca973c2 with a clone guide. The original
upstream master files and all application/model/DBC/safety source bytes remain
unchanged. The original official origin remote remains; new radxa-pilot remote
and Radxa push/tracking configuration target the owner copy.

## Transfer and actual verification

- Uploaded290LFS objects,1,052,390,826bytes:all current source assets and
  locally introduced historical assets. Sizes match local objects. Older
  upstream-only model bytes are not mirrored wholesale; original historical
  upstream commits retain their original asset-storage configuration.
- A real fresh public clone of radxa/q8b recursively checked out all seven
  nested dependencies at exact pins, including custom opendbc. Selected camera,
  model runtime and RetroPilot source files match this project byte-for-byte.
- A separate fresh master Git clone verifies original SHA and complete19,005
  commit ancestry (blob:none filtering, not a shallow history).
- Fresh LFS download acceptance is recorded in the machine receipt.
- Metadata assertions, preserved commit IDs, notebook links, whitespace and
  final remote refs are checked before task closeout.
- No application/hardware/model/vehicle execution for this publication. Previous
  runtime tests are historical evidence; no claim of new driving validation.

[Receipt](../../Evidence/github-publication-20261104.json),
[asset upload manifest](lfs-upload-manifest.json),
[clone instructions](../../../docs/GITHUB_RADXA.md).

## Resolved transfer issues

The first private copy was created before the owner chose public. A temporary
GitHub Actions Git-object-copy job rejected an old intermediate tag because of
old LFS references. Direct push of complete master succeeded with its original
SHA, so the broad visibility question raised from that failed job was corrected.
The owner then selected public, and this repository was made public. No extra
repository was created and no existing owner fork changed. The temporary
bootstrap branch was deleted; no import tags remain. Actions is disabled again.

The [source-import API was deprecated](https://github.blog/changelog/2024-04-17-updates-to-github-importer-and-the-deprecation-of-the-source-import-rest-api-endpoint/)
and did not perform an import. A Radxa push immediately during visibility
conversion returned transient403; metadata confirmed the repo enabled, and
retry succeeded. One verification helper omitted its json import after a
successful master clone; corrected without recloning or source changes.
Fresh clone required invoking this host's separately installed Git LFS3.8.1,
then installing its local filters; ordinary users must install Git LFS first.

## Preserved boundaries and next step

Only tracked Sunnypilot project content/history/assets were published. Other
Comma workspace repositories, virtualenv, ignored native builds/caches and
backup refs are not copied. Tracked student Ai travels with the project;
central coordinating Ai stays in the workspace. Security signature scan of
tracked regular files<=5MB flagged only the shared stock comma SSH key,
identical to original official upstream blob3f269afe22835721d318ea3c18461daf2d21b79f.
No owner credential or dotenv file was added; this is a narrow scan, not a full
historical secret audit. No personal token was stored in repository files or
Actions secrets; the temporary job used its repository-scoped built-in token.

Camera, Thneed artifact/runtime, RetroPilot code and all seven gitlinks are
unchanged. RetroPilot remains receive-only/noOutput live; existing hardware
holds remain. Automatic upstream update timer stays paused/approval-only.
Next:use the published radxa/q8b branch and documented clone procedure.
Native compilation/environment setup remains a separate installation step.

Skills:Git workflow, documentation, scoped publication/security checks and
CI automation for the discarded temporary transfer job. Source-first REA
routing used Git/source and real transfer/clone evidence; no unrelated binary
analysis or fabricated model/hardware test.
