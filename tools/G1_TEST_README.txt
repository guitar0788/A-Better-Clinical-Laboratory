ABCL G1 R2 LAB-ONLY FIXTURE — DEVELOPMENT TEST ONLY, NOT ALPHA

IMPORTANT: Do NOT use or install this source candidate until:
- The exact R2 SHA passes genuine net35/CLR2 L3 compilation against original
  game assemblies and its fresh Actions artifact is audited.
- The native lab availability and fallback review gate is explicitly GO.
- A complete, fixed one-session L4 setup checklist is issued.
Old R1 artifacts do not include the R2 source.

Purpose
-------
R2 replaces the severe lead-poisoning spawn exercise with a MOBILE, ordinary
vanilla Emergency outpatient case DIA_CLD, only to check whether the NEW
ABCL blood-lead sampling/testing pair actually reaches the separate ABCL
toxicology laboratory and returns a laboratory result.

A disposable-save-only local override attaches the ABCL sampling exam to
DIA_CLD. The real lead-poisoning disease TRM_LDP, its symptoms and severity
are not overridden in R2. A lab result from this benign fixture does NOT
prove a positive blood-lead clinical diagnosis or treatment of poisoning.

Test readiness (when approved for L4)
-------------------------------------
1. Close Project Hospital and use ONLY a disposable test save.
2. Confirm the test package's BUILD_INFO.txt records the exact approved R2 SHA.
3. Remove any old ModABCLG1LeadTest addon before installing the fresh build.
4. Use INSTALL_G1.cmd; provide the game root with ProjectHospital_Data.
5. The installer creates only StreamingAssets/Addons/ModABCLG1LeadTest, with
   local copies of necessary original records (DPT_LAB and DIA_CLD) plus
   ABCL-owned XML. Original game files unchanged.
6. Ensure code mods are enabled; use an operating Emergency OUTPATIENT clinic
   with valid doctor office, waiting room and day doctor. No Internal Medicine
   hospitalization, ambulance, ICU or heavy lead-poisoning setup is required
   by this R2 fixture.
7. Ensure the original Laboratory department is operating, with the mandatory
   hematology lab and day laboratory staff; add the optional ABCL G1
   Toxicology Laboratory with its required equipment and a lab specialist.
8. With the game running, click the R2 G1 button ONCE, record its exact status
   and observe outpatient arrival. The button does NOT guarantee admission.
9. In the doctor/patient UI, locate the new ABCL sampling, observe sample
   collection, lab delivery to the ABCL room, staff use and returned result.
10. If any step fails, STOP and preserve a screenshot + output_log.txt/Player.log.
11. Preserve the original CBC pass as historical evidence; one final optional
    CBC regression checks that R2 did not interfere with it.
12. Save/quit/reload ONLY while the addon remains installed. Never open an
    affected save after uninstall; R2 is not a release.

Do not mistake source-only Verify or L3 compilation for gameplay L4.
Never distribute game assemblies, encryption keys, or R2 test-spawn controls.


R3 NATIVE LEAD-POISONING CANDIDATE — NOT YET APPROVED FOR INSTALL/L4
------------------------------------------------------------------------
R2 mobile outpatient lab-fixture L3/L4 completed (owner-reported 14/14)
on source 7f3c5f29cebd39338df854a1475ceb604dca164f,
Actions 41377881918. No repeat of the established R2/CBC path is required.

R3 source adds a distinct native-IMOBILE test panel that appears only if
TRM_LDP, in the loaded addon-local database, links to ABCL blood-lead sampling.
The R3 installer has the explicit -NativeLeadReviewOnly switch and retains
the normal R2 installation as its default. It does not modify original game
files or native hospitalization/insurance/ambulance code.

R3 panel checks ALL conditions before allowing a single patient request:
- TRM_LDP + ABCL exam linkage
- Internal Medicine outpatient/day doctor + clinic readiness
- Internal Medicine complete inpatient rooms + day/night staff + stretcher
- Native immobile diagnosis pool and hospital intake condition
- Contracted insurer with a positive current IMOBILE quota
- Actually available PARKED ambulance below its native call limit

A native factory return means only CREATED, never ARRIVED or hospitalized.
R3 does not bypass native quota, collision, hospitalization or DLC rules.
No repeated spawns after a partial failed factory call. Do not use on a
long-term save, and do not interpret R2 test results as positive blood-lead
diagnosis/treatment evidence.

HOLD: Do NOT install or test R3 until the exact current Git commit passes the
owner-authorized real-game net35/CLR2 L3 workflow, the artifact is independently
audited, and a consolidated checkbox L4 protocol is explicitly issued.
