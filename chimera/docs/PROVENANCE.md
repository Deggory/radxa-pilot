# Starting references — November 6, 2026

The implementation home was created from Sunnypilot
`044772ac169069105763c2547484324a372fbead` on `radxa/q8b`.
The original workspace Chimera archive is pinned at
`224cfa645134db91103c55d8188d87e7976b0ba4`, branch `planning/modern-usb`.
It remains preserved outside this repository; it is not moved or a submodule.

`FIRMWARE_SOURCE_MAP.md` and `firmware-source-map-20261106.json` are exact copies
from that archive's `docs/` and `evidence/` respectively. The receipt retains
Ocelot `d87892fa25ef2a2474110b97bfb5245ee818b534`, pre-existing dirty status and
19 selected source/dependency hashes. Historical checks are labelled as such;
copying this receipt is not a new firmware test.

Current Panda reference: `8a16e089b88593914823743df29e1c30b7dd3e00`.
Current opendbc reference: `150f937198ceab43c43b39f94b9bdea63fcb633c`.
Carrot F413/native USB candidate: ajouatom/openpilot `carrot-wip`,
`69a2d3beb11ff615c7425a4908f4b8e7c8ac98e7`.

The project notebook retains portable comparisons under
`Ai/Reports/panda-chimera-deep-review-20261105/` and
`Ai/Reports/carrot-wip-panda-20261106/`, relative to the Sunnypilot root.
The full source snapshots, nightly recovery bundle and historical Core Config
backups remain in the optional Comma workspace `chimera/` archive. Future
implementation imports must retain source/license/version provenance and bring
required build inputs into this project rather than depending on that archive.

Owner-supplied follow-up: Deggory/Ocelot_Panda_docker
`04b56ba0145588d91ff70e1b35b47b7f2652d4db` and parent
`98de83bb54746d057e6e4bff707eab6cd8c179d9`. A selected31-file source snapshot,
complete current tree/selected history and reproducible offline checks are
retained inside this project under
[reference provenance](../reference/ocelot-panda-docker-20261106/PROVENANCE.md).
The [review](OCELOT_PANDA_DOCKER_REVIEW.md) distinguishes its older Panda target
from the parent Chimera acquisition/relay/OBD-C target. No production source
import, full legacy build, physical compatibility or licensing grant is inferred.
