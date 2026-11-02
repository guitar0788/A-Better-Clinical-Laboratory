ABCL G1 R3 NATIVE LEAD-POISONING TEST — DEVELOPMENT ONLY, NOT ALPHA
========================================================================

CURRENT GATE — TWO DISTINCT EVIDENCE LEVELS
-------------------------------------------
The R3 core clinical workflow has an OWNER-REPORTED L4 PASS on historic
test-only artifact 13117942292 (source
1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b, Actions 41391983195).
That user report covers native TRM_LDP creation, ambulance arrival, Internal
Medicine admission, ABCL sampling, toxicology analysis/result, chelation,
original CBC and save/quit/reload. It is not evidence of new read-only
diagnostics or all-DLC/Workshop compatibility.

The current Draft PR #7 read-only diagnostic panel adds Liver TY contract,
ICU readiness/objective, ambulance unlock/count, configured vs live IMOBILE
quota and related native preflight display. It excludes the deprecated base
stub and preserves native insurer eligibility. Changes to the read-only panel
require their own exact-SHA genuine Windows net35/CLR2 L3 and package audit,
then ONLY a focused panel-display L4.

The owner-approved, protected-main "Auto-build verified G1 PR candidate"
workflow now automatically compiles an exact authorized PR #7 head after
Verify. A prior automated build may have passed L3, but that does not prove
any later source revision. For YOUR ZIP, verify its Actions run was SUCCESS,
check BUILD_INFO.txt CANDIDATE_SHA against the PR #7 SHA and DLL_SHA256
against the actual enclosed DLL. Do not reuse old R3 build 13117942292
to validate new panel diagnostics. Do not substitute green Verify/CodeQL
checks for a genuine L3 build.

PANEL-ONLY L4 IS STILL REQUIRED. Do not generate another patient or repeat
the old R3 clinical/CBC/save-load sequence solely for read-only diagnostic
changes. Record Project Hospital version, enabled DLC/Workshop, the exact
panel status/screenshot and a log if there is any failure. Never publish this
test-only spawner as Alpha.

R2 HISTORY — DO NOT REPEAT
--------------------------
R2's benign Emergency DIA_CLD lab-only fixture already passed the owner's
14/14 one-session test, including ABCL sample collection, toxicology-lab
processing, physician result, vanilla CBC and save/reload. Do not repeat the
R2 discovery sequence. R2 does NOT prove authentic TRM_LDP admission or
treatment.

R3 PURPOSE
----------
R3 creates one original TRM_LDP lead-poisoning patient using the game's native
IMOBILE patient factory and ambulance path. The installer adds the ABCL
sampling examination to an addon-local copy of TRM_LDP and adds the optional
ABCL toxicology room to an addon-local copy of DPT_LAB. It does not change
installed original game files, original symptoms/severity, mobility,
hospitalization treatment, chelation treatment, global patient pools or
Harmony patches.

A factory return means CREATED only. It does NOT prove ambulance reservation,
arrival, admission, lab completion or treatment. The in-game panel reports
the preflight separately and has a one-attempt latch. Never click again after
an attempt in the same session.

INSTALL THE R3 MODE
-------------------
1. Open the successful "Auto-build verified G1 PR candidate" Actions
   run for the authorized current PR #7 SHA. Download its test-only artifact
   "ABCL-G1-AutoBuilt-TestOnly" (or the older manually dispatched package
   ONLY when its SHA is explicitly approved for that test).
2. Extract the downloaded Actions artifact ZIP, read BUILD_INFO.txt and
   confirm CANDIDATE_SHA and DLL_SHA256. Extract the inner
   ABCL_G1_AutoBuilt_TestOnly.zip (or the matching legacy installer ZIP).
   Do not use a package compiled from a different or stale G1 source SHA.
3. Close Project Hospital completely.
4. If StreamingAssets/Addons/ModABCLG1LeadTest already exists, remove only
   that ABCL test-addon folder before installing the refreshed package.
   Do not remove or alter any other addon. Do not open an R2-affected save
   after removing/replacing its addon. Keep the old R2 save as historical
   evidence and use a separate disposable R3 save.
5. Run INSTALL_G1_R3.cmd. It prompts for the game root containing
   ProjectHospital_Data. Alternatively, open PowerShell in the extracted
   package directory and run:
       .\Install-ABCL-G1.ps1 -NativeLeadTest
6. Do NOT run INSTALL_G1.cmd for R3: that script intentionally installs the
   historical R2 DIA_CLD fixture by default.
7. Confirm the installer reports that R3 native TRM_LDP test mode was
   installed. If it reports an error, stop; do not manually edit XML.
8. Start a NEW disposable hospital save. Keep the ABCL addon installed for
   every load of that test save. Do not use a long-term or production save.

FOCUSED READ-ONLY PANEL L4 — NO PATIENT GENERATION
------------------------------------------------------
Use ONLY an artifact whose exact SHA has a passing real L3 build and package
audit. Install as described above into a disposable-test environment; leave
all original game XML untouched. Do not migrate the earlier R2/R3 test save
across incompatible addon revisions.

1. Launch Project Hospital with code mods enabled; load or create a disposable
   test hospital suitable for checking the native insured/ICU/ambulance gates.
2. Open the ABCL G1 [Test] panel. Do NOT click REQUEST ONE NATIVE LEAD PATIENT.
3. Read and capture the Liver TY contract and ICU objective status, ambulance
   unlock and currently parked count, configured IMOBILE quota and actual live
   daily allowance. Clearly distinguish target quota from live availability.
4. Confirm the displayed status is internally consistent with the vanilla
   insurance/department/ambulance state. It is acceptable for fields to show
   NOT READY when the matching native prerequisites are not met.
5. Confirm opening/closing the panel does not modify vanilla insurer state,
   generate a patient, start an ambulance dispatch or interrupt original labs.
6. Record package CANDIDATE_SHA / DLL_SHA256, game version, enabled DLCs,
   panel screenshot and exact PASS/FAIL. If a field is wrong or an exception
   occurs, stop and preserve the matching game log.

This focused check is NOT a full R3 clinical acceptance or a claim of complete
DLC/Workshop compatibility. The historical R3 workflow below is retained as
reproduction guidance only and MUST NOT be repeated for panel-only changes.

HISTORICAL ONE-SESSION R3 CLINICAL TEST — DO NOT REPEAT FOR PANEL-ONLY WORK
---------------------------------------------------------------------------
Before clicking:
- Code mods are enabled and the R3 ABCL panel appears in the hospital scene.
- Internal Medicine is open and operational for BOTH outpatient and inpatient
  intake. Its clinic and ward validity must be green; the R3 panel also checks
  the native department gates.
- The original Laboratory is operational, including its mandatory hematology
  lab, waiting room and day laboratory staff.
- The ABCL G1 Toxicology Laboratory is built with every required item and a
  qualified lab specialist on the correct shift.
- Normal vanilla route: contract Liver TY (`IN_COM_CCC`, Chinese
  localization `肝泰保险`) and complete its ICU hospitalization objective
  (#4) to unlock ambulances. Its next objective (#5) requires at least one
  ambulance and rewards a configured IMOBILE quota of 2.
- The R3 panel shows Liver TY contract state, ICU readiness, objective #4/#5
  completion, ambulance unlock/count, configured quota and live daily quota.
  A configured target is not the same as a positive live daily allowance.
- The test harness still follows vanilla semantics: any visible contracted
  insurer with a positive live IMOBILE allowance can qualify; it does not
  force Liver TY or edit insurance/objective state.
- There must be a visible contracted insurer with a positive **live**
  IMOBILE daily quota and at least one actual PARKED, unassigned ambulance
  below its native daily-call limit.
- No conflicting old ABCL test addon or third-party Workshop mods are active.
  Record the official DLCs enabled; do not claim untested DLC compatibility.

1. Open ABCL G1 [Test] and read every R3 preflight line.
2. Proceed only when every line says OK. If any line says NOT READY, EMPTY,
   ZERO or NONE, do not click. Capture the panel and stop for source-backed
   diagnosis; do not build rooms or change insurance one item at a time.
3. Click REQUEST ONE NATIVE LEAD PATIENT exactly once.
4. Record the exact panel status. CREATED is not ARRIVED. Observe the native
   ambulance reservation, dispatch, patient arrival and Internal Medicine
   intake. Do not retry if the ambulance does not arrive.
5. Confirm the patient is the original TRM_LDP case and reaches appropriate
   Internal Medicine care.
6. Check that the physician can order EXM_ABCL_G1_BLOOD_LEAD_SAMPLING.
   Observe collection, delivery to the ABCL toxicology lab, specialist/device
   work, completed linked testing and the returned physician result.
7. Confirm the original high-priority hospitalization and chelation-therapy
   pathway can be carried out. The original high-lead symptom has a 6–12
   in-game-hour collapse window; do not spend the test window on unrelated
   setup after creating the patient.
8. Run one final vanilla CBC regression only; do not repeat the already
   accepted R2 CBC discovery.
9. Save, quit and reload once while the same R3 addon remains installed.
10. If any step fails, stop immediately. Preserve a screenshot of the exact
    status/UI and the matching output_log.txt or Player.log. Do not spawn
    another patient or make an unapproved source patch.

EVIDENCE TO RECORD
------------------
- BUILD_INFO.txt candidate SHA and DLL SHA256.
- Project Hospital build/version and official DLCs enabled.
- Confirmation that no Workshop mods were active.
- Save type (new disposable save).
- Every R3 preflight line and the exact one-click status.
- Whether an ambulance was assigned, dispatched and arrived.
- Patient department/admission, ABCL order, collection, lab queue, specialist
  work, result, high-priority hospitalization and chelation outcome.
- One CBC regression and save/reload result.
- Screenshot and game log on the first failure.

SAFETY / COMPATIBILITY
----------------------
This is a test-only debug panel and addon-local override. It is not Alpha,
not a release, and not a promise of all-DLC/Workshop compatibility. Do not
publish or distribute the test package. Do not open affected saves after
removing the addon; uninstall safety has not been established. No original
game DLLs, decrypted references or AES key belong in the package.
