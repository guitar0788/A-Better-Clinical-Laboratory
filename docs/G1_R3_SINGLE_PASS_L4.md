# G1 R3 single-pass L4 protocol

**Status:** Ready for one controlled gameplay attempt only after the refreshed
R3-specific artifact has a successful exact-SHA Verify/L3 build. The earlier
artifact 13116563798 is audited evidence but must not be installed because its
installer still labels R3 offline-review-only and its generic CMD selects R2.

## Fixed scope

R3 validates the authentic original lead-poisoning case `TRM_LDP`, not a
generic mobile fixture. The installer adds the ABCL sampling examination only
to an addon-local copy of `TRM_LDP`; the original lead symptom, IMOBILE
mobility, high-priority hospitalization and chelation treatment remain native.
It also adds the optional ABCL room to an addon-local copy of `DPT_LAB`.
No installed original XML is edited, no Harmony patch/global pool change is
made, and no other mod is required.

R2 already passed its 14/14 owner-reported lab-fixture test. Do not repeat
R2's Emergency `DIA_CLD` test or its CBC discovery sequence.

## Before starting

- [ ] Use the latest refreshed Actions artifact and verify that its
      `BUILD_INFO.txt` candidate SHA is the exact approved candidate.
- [ ] Close Project Hospital.
- [ ] Remove only an existing `StreamingAssets/Addons/ModABCLG1LeadTest`
      folder if replacing the old test package. Do not touch other Addons.
- [ ] Keep the old R2 test save as historical evidence. Do not open an
      R2-affected save after removing/replacing its addon; use a separate
      disposable R3 save.
- [ ] Run `INSTALL_G1_R3.cmd` or
      `Install-ABCL-G1.ps1 -NativeLeadTest`. Do not run generic
      `INSTALL_G1.cmd`, which intentionally installs R2 by default.
- [ ] Confirm installer success and start a new disposable hospital. Keep
      the R3 addon installed for the entire save/reload test.

## Read-only preflight — no patient is created here

Open the R3 panel and check all seven lines:

- [ ] Native `TRM_LDP` + ABCL sampling examination: OK.
- [ ] Internal Medicine outpatient intake: OK.
- [ ] Internal Medicine inpatient intake: OK.
- [ ] Native immobile diagnosis pool: OK.
- [ ] Native hospital intake gate: OK.
- [ ] Contracted insurer with positive immobile quota: OK.
- [ ] Actually free parked ambulance: OK.

If any line is not OK, **do not click**. Capture the whole panel and stop.
Do not build rooms one at a time, change insurers blindly or repeat a test.
The panel is read-only until the single request button is pressed.

## One patient attempt

- [ ] Click `REQUEST ONE NATIVE LEAD PATIENT` exactly once.
- [ ] Record the exact status. `CREATED` is not `ARRIVED`.
- [ ] Observe the native ambulance being reserved, dispatched and returning
      the patient to the hospital.
- [ ] Confirm the patient is admitted/assigned to Internal Medicine.
- [ ] If the factory returns null, throws, no ambulance is assigned, or no
      arrival occurs, stop. Do not retry in that save. Capture screenshot
      and the matching game log.

The original `SYM_LEAD_LEVELS_HIGH` is High hazard and has a 6–12 in-game-hour
collapse window. After creation, do not spend the window on unrelated setup.

## Clinical acceptance in the same session

- [ ] Confirm the physician can order
      `EXM_ABCL_G1_BLOOD_LEAD_SAMPLING` for this `TRM_LDP` patient.
- [ ] Observe the sample collection.
- [ ] Observe the specimen entering the ABCL toxicology laboratory workflow.
- [ ] Observe a qualified lab specialist use the required equipment and finish
      the linked ABCL testing examination.
- [ ] Confirm the result returns to the physician.
- [ ] Confirm native high-priority hospitalization and chelation therapy can
      be prescribed/performed as appropriate to the case.
- [ ] Run one final vanilla CBC regression only. Do not repeat the accepted
      R2 CBC discovery.
- [ ] Save, quit, and reload once while the R3 addon remains installed.

Stop at the first failure. Do not press Spawn again or make a speculative
code change under the same evidence. Capture screenshot, exact status, game
build, enabled official DLC, confirmation that no Workshop mods were active,
and the matching `output_log.txt` / `Player.log`.

## Limits

This is a test-only debug panel and addon-local clinical override, not Alpha
and not a release. It does not prove natural patient generation, every DLC or
Workshop combination, or safe uninstall from an affected save. The factory
return alone never proves arrival/admission. PR #7 remains Draft until the
clinical gate is independently reviewed.
