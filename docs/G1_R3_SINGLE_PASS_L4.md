# G1 R3 single-pass L4 protocol

**Status:** R3 core gameplay L4 is **owner-reported PASS** on artifact
`13117942292`, exact compiled source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`
(Actions `41391983195`). The report covers native `TRM_LDP` creation, ambulance
arrival, Internal Medicine admission, ABCL sampling/lab/result, native
hospitalization/chelation, CBC and save/reload. Game version, official DLC list,
post-click panel status, screenshots and logs were not supplied.

The newer read-only diagnostic-panel candidate is
`7faf31c6bba34ab58a9e288217d0359956bd2af2`; Verify 29/29, CodeQL and Analyze
Python pass. Its genuine Windows/net35/CLR2 L3 and package audit are still
pending. Artifact `13117942292` validates the R3 gameplay implementation but
does not contain the newer diagnostic lines. After the exact-SHA build/audit,
perform a focused panel display/preflight check; do not repeat the full clinical
flow solely for this read-only diagnostic change.

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

## Vanilla insurer / ambulance unlock chain — read-only

The supplied original data identifies Liver TY as `IN_COM_CCC` (Simplified
Chinese localization: `肝泰保险`; the active patch database entry is
`IN_COM_CCC_PATCH_1_1`). Its native objective order is:

1. Objective #4 (zero-based index 3): a working ICU hospitalization department
   (`WORKING_HOSPITALIZATION_AT_DEPARTMENT`, `DPT_ICU`, evaluated by vanilla
   `Department.AcceptsInpatients()`) grants `UNLOCK_AMBULANCES`.
2. Objective #5 (zero-based index 4): at least one ambulance
   (`NUMBER_OF_AMBULANCES >= 1`) grants
   `SET_IMMOBILE_PATIENT_COUNT=2`.

The reward writes the configured target `m_currentImmobilePatients`; the
live daily allowance `m_immobileSpawnedToday` is calculated separately by
vanilla `CalculatePatientCounts`. The panel displays both values and does
not force a reward, recalculate a quota, contract an insurer or modify the
hospital. A target of 2 with a live daily allowance of 0 is **not** permission
to spawn.

For compatibility, the test harness preserves vanilla selection semantics:
any visible contracted insurer with a positive live IMOBILE allowance is
eligible. Liver TY is shown as the normal progression route, not hard-coded
as the only insurer that can ever qualify.

## Read-only preflight — no patient is created here

The R3 panel now reports:
- [ ] Native `TRM_LDP` + ABCL sampling examination.
- [ ] Internal Medicine outpatient and inpatient intake.
- [ ] Native IMOBILE diagnosis pool and hospital intake gate.
- [ ] Liver TY contract state.
- [ ] ICU hospitalization readiness and Liver TY objective #4 completion.
- [ ] Ambulances unlocked and actual ambulance count.
- [ ] Liver TY objective #5 completion and configured/live IMOBILE quota.
- [ ] The actually selected eligible insurer and its live quota.
- [ ] An actually free parked ambulance.

Proceed only when the clinical gates, selected insurer's live quota, and free
parked ambulance are all valid. The Liver TY progression lines are diagnostic;
if another vanilla insurer already has a positive live quota, the original
game's admission rule remains valid. If no eligible insurer has a positive
live quota, **do not click**. Capture the whole panel and stop. The panel is
read-only until the single request button is pressed.

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

## Recorded L4 result — owner-reported PASS (2026-11-02)

Tested package: artifact `13117942292`, source SHA
`1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, Actions run `41391983195`.
The owner confirms the correct R3 package, fresh temporary hospital save,
no third-party Workshop mods/old ABCL test plugins, operational Internal
Medicine clinic and ward, original laboratory/hematology/day staff, ABCL
toxicology room/equipment/specialist, positive live IMOBILE quota, free parked
ambulance, and all displayed R3 preflight items OK.

Owner reports PASS for: game and G1 panel load; one-click original `TRM_LDP`
creation; ambulance assignment, dispatch and arrival; Internal Medicine
admission; physician ABCL blood-lead order; sample collection and delivery;
ABCL toxicology queue; specialist/device analysis; physician result return;
native high-priority hospitalization; native chelation; original CBC; and
save/exit/reload with the laboratory still functional.

Not recorded/provided: exact post-click panel status, game version, official
DLC list, screenshots and game logs. No failure was reported. The insurer's
name/objective progress was not separately stated. This is owner-reported L4
evidence for the tested artifact/configuration, not independent telemetry or
proof of all-DLC/Workshop/uninstall compatibility.

The earlier zero-quota screenshot was an earlier blocked preflight and is
superseded for this later disposable-save run. Do not repeat the complete R3
clinical sequence solely for the newer read-only diagnostic-panel source.
After that source receives exact-SHA L3 and package audit, check only the
updated panel's displayed diagnostics/preflight.

## Limits

This is a test-only debug panel and addon-local clinical override, not Alpha
and not a release. It does not prove natural patient generation, every DLC or
Workshop combination, or safe uninstall from an affected save. The factory
return alone never proves arrival/admission. PR #7 remains Draft until the
clinical gate is independently reviewed.
