ABCL G1 R3 NATIVE LEAD-POISONING TEST — DISPOSABLE SAVE ONLY
================================================================

CURRENT PACKAGE SAFETY
----------------------
This candidate uses only the original TRM_LDP native IMOBILE route.
The old R2 DIA_CLD outpatient override and C1 disabled Super-GM fixture
were retired after the owner's 2026-11-04 L4 report.

There is NO Chinese Super-GM panel and NO arbitrary diagnosis spawn.
Do not install an older package that contains 中文超级GM or the C1 fixture.
Do not use an R2-affected save for this build.

The C1 fixture was not clinically valid: its four selected original symptoms
all have IsMainSymptom=false. It therefore had no native main symptom for
the diagnosis/treatment UI. The old GM button also used the original patient
factory, which registers the created entity with the insurer. It was not a
side-effect-free preview. The fixture and panel are removed, not hidden.

The generic R2 installer mode is removed. Both INSTALL_G1.cmd and
INSTALL_G1_R3.cmd explicitly request the R3 native TRM_LDP route.
Install-ABCL-G1.ps1 refuses to run without -NativeLeadTest.

R3 adds the ABCL blood-lead sampling examination only to an addon-local
copy of the original TRM_LDP record. It does not override DIA_CLD, any
generic outpatient diagnosis, the native severe symptom, or chelation/
hospitalization treatments. The original game XML and other addons are
not modified. The optional Toxicology Laboratory remains additive to DPT_LAB.

TO-001 assets in the refreshed package are:
- approved 64x64 active and inactive Toxicology Laboratory room-list sprites;
- a private 2048x2048 floor atlas containing only approved isometric tile 376.
The private atlas is separate from the vanilla floor texture. It does not
replace the original floor atlas or change zone/room overlay colors.
Visual source approval does not establish native UI/game L4.

TO-004 V3 prefab labels are dimension-free. Vanilla MapEditorUIController
appends the displayed width and height once; the localized string must not
repeat the dimensions.

INSTALLATION
------------
1. Close Project Hospital completely.
2. Use only a package whose BUILD_INFO.txt exact CANDIDATE_SHA and DLL_SHA256
   match a successful genuine Windows net35/CLR2 build.
3. Extract outside the game directory.
4. Run INSTALL_G1_R3.cmd (or INSTALL_G1.cmd). Enter the game root containing
   ProjectHospital_Data when prompted.
5. Use a NEW disposable hospital save. Do not use a long-term save.
6. Keep this addon installed for every load of that disposable save.
7. If the installer reports a failure, stop. Do not edit game XML manually.

PATIENT TESTING
---------------
The ABCL G1 panel is a one-attempt native TRM_LDP preflight/test control.
It is not a general-purpose patient generator. Do not click it unless the
hospital has the native Internal Medicine outpatient and inpatient route,
Liver TY ICU progression, ambulance unlock/count, a positive live IMOBILE
quota, and the required native lab staffing/rooms.

A factory return is only CREATED, not ARRIVED, ADMITTED, DIAGNOSED, TESTED
or TREATED. Do not retry after one attempt in the same session. Do not use
the former Super-GM panel; it has been removed.

The owner's historical R3 clinical L4 report remains valid for the exact
historical build it tested. It does not certify this refreshed integration,
the TO-001 room/floor UI, TO-004 names, or all DLC/Workshop combinations.

CURRENT OWNER L4 OBSERVATIONS — 2026-11-04
-----------------------------------------
G1 panel and Toxicology Laboratory: PASS.
Both standalone instruments: PASS for menu, placement and four views.
TO-004 prefabs: placement/rotation/access PASS; labels FAIL (fixed in source).
TO-001 room icon/floor icon: absent in prior package (now integrated in source).
Super-GM patient: FAIL (retired; no more tests).
Staff operation, vanilla CBC, save/reload and rollback: NOT TESTED.
The refreshed combined candidate requires its own focused L4 before acceptance.

NO ALPHA / NO RELEASE
---------------------
Do not publish this test candidate as Alpha. No all-DLC or Workshop
compatibility claim is made. Preserve the failed test save and logs for
historical evidence; use a new disposable save for the refreshed build.
