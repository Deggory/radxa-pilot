# What this notebook knows, and how deeply

Initial knowledge is seeded from existing workspace evidence, checked source
versions and the system review. It is not a claim that every source line or
submodule algorithm has been understood or tested.

| Area | Initial coverage |
| --- | --- |
| Current repository/dependency trees | Complete tracked-path/blob navigation index at recorded pins |
| System folder | Complete 193-path catalog; selected core function bodies reviewed; 139 AST parses |
| Hardware/platform selection and model backend boundary | Selected source paths and established port gaps |
| Camera/model/UI integration | Existing source audit and separate standalone measurements; managed integration unqualified |
| Planning/lateral algorithms and full car support | Topic locations and historical traces; deeper current review still needed |
| Panda/firmware/shared actuator interface | Boundaries and canonical DBC policy; no compatibility or actuation claim |
| Daily update/commit protection | Deployed controller and scoped tests; upstream semantics still require review |
| Entire repository runtime suite | Not established |

New findings must say whether they are source observations, imported historical
measurements or newly executed tests. Preserve provenance and unresolved limits.
If an index/topic pin differs from live HEAD, inspect the relevant diff before
using it as current evidence. A filename or symbol match is a starting point.
