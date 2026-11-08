# Angle sensor through Chimera CAN2 recheck — November 8, 2026

Accepted scope: test the previously working Waveshare sensor through Radxa's
current receive adapter. Teacher-first read confirms earlier0x25/500kpositive
capture. Fresh Radxa scan shows Chimera but no Waveshare/SocketCAN interface.
Owner clarifies printedChimeraCAN2, separate supply/sharedground, then explicitly
keepsCAN2instead of a suggested physical CAN0comparison.

Initial native startup exit2was USB exclusivity: Core Config/web_app.pyPID23504
held the exact original Chimera node. Preserved failure log; no CAN observation
claimed from it. Owner disconnected app; owner scan empty. Native20.114s/
1892CAN batches/20health and independentPython8s/784polls/15health both0frames.
Readers exit0/stopped; final USB-owner scan empty. App left open/disconnected.

[Report](../Reports/steering-sensor-recheck-20261108/README.md) pins baseline,
raw observation/interpretation, source/native/DBC hashes and actual owner replies.
No OEM angle decoding possible without raw frames; RP-SIM-1counter is not a
sensor decoder. OEM0x25and canonical0x50remain distinct. Current voltage,
CAN2active timing, VCC/STB/termination/waveform/source equivalence still unknown.

All76legacy entries and selected hashes verified unchanged. No host CAN data,
USB OUT/config/heartbeat/relay/reset/flash, app/product/firmware/DBC/model update,
upstream action, CAN0move or push. Used debugging/source-first/direct native and
Python runtime evidence; no unrelated REA binary analysis. Teacher/student
Q&A/topic/state/worklog/handoff/router/session/report updated and verified;
notebook increment committed with blocked physical-acceptance evidence attached.
Actual commit/clean readback retained centrally in FINAL_READBACK.json.

Next remains current CAN2electrical/enable/timing qualification within owner
selected scope; no blind config/firmware writes or repeated port-move request.
