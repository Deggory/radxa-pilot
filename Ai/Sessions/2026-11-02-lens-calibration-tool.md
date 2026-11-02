# Printable lens target and collection/solve tool — 2026-11-02

Owner said proceed after road capturef4f4d01; teacher search found only70°FOV
visual estimate/zero mountangles/1.22mheight, not measuredK/distortion. Asked
owner only for missing physical target availability; owner explicitly selected
prepare printable target/tool. Current model-layout fix6fea7ecf committed and
validation journaled separately;23tests/140actualframe pairs/current CPU-warp
synthetic parity pass. Its model input is uint8[2,6,128,256], not direct720pRGB.
Model execution/Adreno and real geometry remain unqualified.

Added webcam/calibrate.py target/capture/solve commands, exact-scale vector
A4landscape PDF/SVG under webcam/calibration and CALIBRATION.md. 10×7squares,
9×6internalcorners,25mmsquares and100mmruler. PDF MediaBox841.89×595.276points;
rendered preview inspected and real detector reads54corners from it. Regeneration
is deterministic and existing targets/outputs/capture directories are preserved.

Live collection uses only native AK720pMJPG60/latest capture, Tk/Pillow preview
(OpenCV build is headless). Space saves complete, distinct full-resolution grids;
Escape/Finish closes source and preserves partial images/manifest. Records
timestamps/sequence/hash/profile/rotation and reads optical controls, without
setting focus. Current continuousAF1is displayed as provisional; exact optical
state and future fixed-focus policy need review before installation.

Offline solver rechecks manifest720pMJPG60profile, hashes, all corner detections
and resolution. Requires12views,15%center spread on both axes; globalRMS≤1px,
per-viewRMS≤1.5px, finiteK/distortion/uncertainty, positivefocal/plausibleprincipal
point. No failed views silently removed. JSON has fullK/five distortionterms,
per-viewerrors/uncertainties/provenance, candidate_not_installed and explicit
optical/mountreview flags. Q8B calibration guard remains active; no old70°guess,
no profile registration, no model/runtime/driver-monitoring/vehicle changes.

6calibration tests cover target size, detector on grid/blank, known-camera
recovery from16synthetic projected views, bad/repeated/high-error rejection and
no overwrite/hash-change handling. Combined with23camera/identity checks gives
29focused tests. Hidden real Tk/Pillow GUI exercised synthetic JPEGs:1saved,
duplicate rejected, source closed; no camera hardware accessed by that test.
It is not a real measured calibration. Physical printed-target images remain
uncollected. Need printer100%actualsize, checked25mmsquare/100mmruler, flat mount,
then varied views and focus review; mounted-camera extrinsics are separate.

Used source-first/TDD/incremental/debugging/code-review/documentation/Git skills.
Primary OpenCV calibration workflow/API consulted, linked in guide. No unrelated
REA result claimed; source/actualcamera IPC/CPUwarp/syntheticcalibration evidence
distinguished. Build/test environment stays existingmsm-venv plus previously
hash-checked temporary dependencywheels; no system or venv package installation.
Source/model pins unchanged since6fea7ecf; stock model SHA65a08adc. Evidence in
optional workspace Ai/Reports/sunnypilot-camera-contract-20261102 includes model
contract, live padded-camera records, target preview, GUI and final checks.

Final lifecycle review: collector handles SIGINT/SIGTERM through normal Tk
close, restores prior handlers, closes the capture owner, and records save/read
errors. Solver rejects a capture manifest with an error rather than silently
using its partial data. Synthetic real-Tk SIGTERM/save/duplicate checks pass.

Generated PDF is marked binary in project .gitattributes to preserve PDF byte
offsets and avoid text normalization. PDF/A4/raster/print-geometry checks stay
explicit; this does not suppress source lint or change test thresholds.
