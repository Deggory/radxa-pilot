# Project location correction — 2026-11-01

The owner clarified: sunnypilot is the project being worked on; other Comma
folders are knowledge/reference, and only sunnypilot will be used when ready.
The previous split protected changes but put implementation in the wrong
user-facing location. This direct clarification authorizes correcting it.

Moved the complete protected repository12e44feeff241334e184c86dc9daccdc7f9e4fa1
from q8b/sunnypilot-radxa into sunnypilot. Moved clean master
 a86979d2b2b176413a7f3e5cccf8c807596a7def into q8b/sunnypilot-upstream.
Git history/assets/submodules and identical IDE files were retained. The old
project path is a compatibility symlink, not a second implementation copy.

Copied specialist notebooked8afadef6d8d47722f7d66a16e25bbe7a56c813 into a
regular tracked Ai directory, excluding nested Git. Original notebook history
is retained unchanged as a reference. Updated README, project/workspace agent
rules and daily updater configuration/hooks. No upstream merge or application
behavior change was part of this relocation.

The report under the optional workspace Ai records exact before/after commits,
source hashes and tests. Project-local `verify_memory.py` checks notebook
layout; `--workspace /home/radxa/comma` additionally validates reference paths
and pinned vendor index. Existing identity tests and native checks verify the
new location. The actual daily update service passed while project HEAD/content stayed
unchanged; the persistent daily15:30UTC timer was restored.

Identity is implemented; full camera/model/UI/health and deployment remain
unqualified. Test environments/tools are development dependencies, not required
outside reference source imports. No firmware/CAN/vehicle service is started.

## Relocation verification completed

From the canonical sunnypilot path:11 Python identity tests,4 native C++→Python
message checks and the actual SCons platform probe passed. Application/build
source is unchanged from12e44fee and both IDE files are byte-identical. The
31-test updater suite passed. Project-local notebook verification passed24docs,
51 relative links and the eight-repository/4252-entry vendor index. A temporary
standalone copy of Ai plus project documentation passed without the workspace.
Verifier Ruff/AST and Git diff checks passed.

The actual retargeted daily service succeeded2026-11-01 20:39:22UTC with exit0,
observing upstreama86979d2. Project HEAD/status and selected source/notebook
hashes stayed identical through the service. Persistent daily timer is enabled,
active/waiting, next run2026-11-02 15:30UTC. No new pending related upstream
commit was discovered. Historical02bf09e8 notebook failure remains retained in
the ledger; it is not a current relocation or application failure.
