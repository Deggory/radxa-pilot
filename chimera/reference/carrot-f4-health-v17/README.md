# Pinned legacy F4 health fixture

Two unchanged files from `ajouatom/openpilot`, carrot-wip commit
`69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7`:

- [health.h](health.h): original `panda/board/health.h`, health17/59bytes and CAN-health5/64bytes.
- [LICENSE](LICENSE): original `panda/LICENSE`, Comma.ai MIT permission notice.

[Manifest](SOURCES.json) records upstream paths, Git blobs and SHA256 values.
Imported from the previously verified November6 workspace archive; source bytes
and Git blobs rechecked before copying. No new network fetch.

Only `test_panda_health.cc` includes the header, inside a namespace. Runtime
decoding uses original explicit byte reads in `panda_health.cc`. Tests need no
workspace archive/download. This is not a firmware build, current board definition
or evidence of the image installed on any Panda/Chimera.
