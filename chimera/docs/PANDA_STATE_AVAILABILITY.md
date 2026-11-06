# PandaState availability and consumer checks

November 6, 2026 — T08b2c, after USB-only commit `0fedef7b0`.

`PandaState.statusAvailability` is appended at ordinal42; existing ordinals and
the type ID are preserved. It declares a current or legacyF4v17 profile, an
observationOnly flag and typed unavailable fields. This describes field support;
it does not authenticate firmware or authorize controls.

The legacy preview declares all six missing current fields: spiErrorCount,
soundOutputLevel, controlsAllowedLateral, controlsAllowedLongitudinal, nmiReset
and hardfaultReset. Its Event remains invalid and observationOnly remains true.
The isolated schema1 JSON diagnostics add the same list under
`availability.unavailablePandaFields`, with observationOnly=true. Raw legacy
measurements remain available there. Generic current-format conversion declares
the current profile; its ordinary startup is still unwired.

The shared [consumer guard](../../openpilot/selfdrive/pandad/panda_state.py)
rejects invalid events, explicit unknown profiles, unknown unavailable-field
ordinals, incomplete legacy declarations and observation-only data. It rejects
the entire batch when one board fails, preserving board/configuration indices.
Each consumer also declares the fields it needs. Merely changing Event.valid to
true cannot promote an observation. Retained-sample consumers require liveness.

| Consumer | Required fields and behavior |
| --- | --- |
| hardwared | Type, both ignition flags and harness status; unusable update revokes ignition, preserves last valid shutdown harness context and existing no-update grace |
| manager | Same ignition fields; invalid/stale/observation data cannot trigger ignition-on parameter clearing |
| UI | Same ignition fields; unusable/stale status clears type/ignition |
| selfdrived | controlsAllowed, safetyModel/Param, alternativeExperience, safetyRxChecksInvalid and faults; unusable batch causes controlsMismatch and counts an enabled mismatch |
| MADS | controlsAllowedLateral and safetyModel; missing lateral support counts a lateral mismatch while MADS is active |

For compatibility, historical producers without this appended metadata retain
their existing current-format contract. Absence is not evidence of authenticity;
the guard cannot identify a dishonest producer. A legacy profile with a complete
missing list may be usable only for consumers whose required fields are present,
and only after a future policy removes observationOnly. No such promotion is
implemented. Card subscribes to Panda status but has no direct value reader in
the reviewed source. Diagnostic/reference readers are not operational consumers.

Current Panda D2 health reads now require exactly49bytes and C2 CAN-health reads
exactly64bytes, connected/healthy handles before and after, and bounded timeouts.
Invalid controller selectors fail before IO. Short or oversized health replies
cannot become zero-filled valid status. Legacy exact-size readers remain distinct.

The existing current generic fault-list code has a separate source-level risk:
it allocates for all set bits but fills only fault0..26; fault27 is absent from
the schema. That ordinary path remains unexposed. The legacy converter rejects
unrepresentable fault bits rather than inventing entries.

Verification: native pandad builds; ten native programs and124Python tests
(56focused plus68control/MADS/power/fan regressions) pass. Actual selected manager,
UI, selfdrived and MADS source branches execute with fake dependencies; these are
not full daemon/GUI integration tests. Native preview serialization interoperates
with Python, including metadata and rejection after forged Event.valid=true.
ASan/UBSan passes for USB/current reads and the preview; linked existing support
libraries are unsanitized. Removing the observation-only check in a temporary
copy causes seven failures in fourteen availability/consumer tests. Ruff and
whitespace checks pass. The evidence receipt retains initial test/fixture failures
and exact commands. No warnings or assertions were suppressed to pass checks.

SPI removal is complete in pandad source/build/discovery/entry paths. Wire fields
whose historical names contain spi remain diagnostic facts. The parked7448-byte
firmware image is unchanged and unflashed. Canonical DBC, Ocelot references and
camera/model/Thneed code are preserved. No physical USB, live IPC/daemon, reset,
configuration, flash, CAN TX, update or push was performed.

Next: specify passive normal-status publication and disconnect/reconnect lifecycle
without granting operational ignition/control admission to legacy observations.
Other profiles, new Chimera operational firmware and physical power/VBUS/recovery/
bench qualification remain pending. Hardware remains untested.

[Receipt](../../Ai/Evidence/chimera-availability-20261106.json).
