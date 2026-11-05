# Radxa project on GitHub

Repository: https://github.com/Deggory/radxa-pilot (public).

GitHub opens the Radxa project branch `radxa/q8b` by default. The `master`
branch contains official Sunnypilot source, separate from our Radxa changes.

This is a standalone public copy with preserved Sunnypilot history, rather
than another GitHub fork-network entry. The existing owner fork
`Deggory/sunnypilot-pc` is untouched.

- `master`: official Sunnypilot source, synchronized on November 5, 2026 to
  `932ff06d9316e4351d6b6b9f1dd422d5b639badf` with a normal fast-forward.
  See the [verification receipt](../Ai/Reports/github-master-sync-20261105/receipt.json).
  This does not apply that update to the Radxa branch or enable automatic updates.
- `radxa/q8b`: this actual Radxa project, with camera, Thneed and RetroPilot
  commits and its tracked `Ai/` notebook.
- `opendbc/retropilot`: supporting branch containing the nested opendbc
  repository's original history and custom RetroPilot commits. The main
  branch's `opendbc_repo` submodule points to this same GitHub repository.

Only the `sunnypilot/` Git project is published. Other Comma workspace folders,
virtual environments, generated native builds and ignored machine caches are
not part of the Git upload. Existing project history is preserved; this is
not a file-only copy or a history squash.

## Clone the Radxa branch

Run:

```sh
git clone --branch radxa/q8b --recurse-submodules https://github.com/Deggory/radxa-pilot.git
cd radxa-pilot
git lfs pull
```

Install Git LFS before cloning; see [installation](../install.md) to build
native libraries and set up the Python environment. A clone is source and
tracked assets, not a copy of this machine's generated build or environment.

The Radxa branch uses this repository's GitHub LFS storage for current assets,
including the unchanged CD210 Thneed artifact and fixtures. The untouched
upstream `master` retains its original Hugging Face LFS configuration.
Historical Radxa revisions predate this URL correction; use a local Git LFS
URL override when retrieving custom assets from those revisions. Current and
locally introduced historical asset objects are included in publication;
older upstream-only asset history is not being mirrored wholesale.

The original official `origin` remote remains unchanged locally. The new
`radxa-pilot` remote is for this owner's GitHub repository. Publish explicit
branches; do not push all workspace backups or use mirror/force pushes.
The upstream update timer remains paused and later updates need owner approval.
GitHub Actions is disabled on this new copy until its CI is deliberately set up.
A temporary Git-object transfer workflow failed its old-LFS tag check and
was removed; a direct push subsequently preserved the complete master history.
The temporary branch was deleted and no import tags remain.

This publication does not qualify hardware, models or vehicle control.
RetroPilot remains receive-only/noOutput in its live interface; existing
Chimera and physical actuation holds still apply.
