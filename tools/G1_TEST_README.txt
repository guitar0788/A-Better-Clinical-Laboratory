ABCL G1 R3 NATIVE LEAD-POISONING TEST — DEVELOPMENT ONLY, NOT ALPHA
========================================================================

CURRENT GATE
------------
R3 C# candidate b0a66222f483319baf8750f23c7d064021781a23 passed genuine
Windows/net35 compilation against the owner-authorized original game
assemblies (Actions 41389454623; zero warnings, zero errors). That first
artifact was independently inspected, but its installer message still said
OFFLINE REVIEW ONLY. Use only the refreshed artifact whose BUILD_INFO.txt
matches the latest approved candidate SHA after the installer/documentation
correction has passed Verify and genuine L3 again.

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
1. Download the latest ABCL-G1-Compiled-TestOnly artifact from the exact
   Actions run associated with the approved candidate SHA.
2. Extract the downloaded Actions artifact ZIP. Then extract the inner
   ABCL_G1_Compiled_Install_TestOnly.zip.
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

ONE-SESSION R3 TEST
-------------------
Before clicking:
- Code mods are enabled and the R3 ABCL panel appears in the hospital scene.
- Internal Medicine is open and operational for BOTH outpatient and inpatient
  intake. Its clinic and ward validity must be green; the R3 panel also checks
  the native department gates.
- The original Laboratory is operational, including its mandatory hematology
  lab, waiting room and day laboratory staff.
- The ABCL G1 Toxicology Laboratory is built with every required item and a
  qualified lab specialist on the correct shift.
- There is a contracted insurer with a positive native IMOBILE daily quota.
- At least one actual PARKED, unassigned ambulance is available below its
  native daily-call limit.
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
