# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Current evidence baseline (2026-11-01)

| Test | Source and type | Result | Limitation |
| --- | --- | --- | --- |
| G0 disposable CBC in a fourth lab | User's direct in-game report in the predecessor conversation | Reported PASS: fourth room appeared and CBC workflow returned a result | No saved raw output log, game version or reproducible save/load report available here; does not validate G1 |
| G1 independent blood-lead examination | G1 test package/source candidate in predecessor conversation | NOT TESTED / BLOCKED | New test IDs and lead-case flow not demonstrated in actual game |
| G1 patient-spawn panel compilation | Previous Windows installer error screenshot | FAILED / NOT COMPILED | Required legacy C# compiler not found. No genuine game-DLL L3 success recorded |
| G1 GItHub Actions build | Proposed only | NOT RUN | Public repository CI must not assume access to proprietary game references |
| Original-device art acceptance | Not delivered | NOT TESTED | No original interactive equipment approved |
| Four DLC / Workshop / save-load regression | No ABCL L4 matrix | NOT TESTED | Do not claim compatibility or safe uninstall |

## Four evidence levels

- **L1 — unit/logic:** test command, negative cases, results, tested SHA.
- **L2 — data/source/assets:** XML parser, all referenced IDs resolved, room/equipment/medical linkage, atlas/pivots/directions and test failures.
- **L3 — game-compatible build:** real game assembly hashes, compiler/target metadata, exact successful build job and artifact hash. No public upload of game binaries.
- **L4 — gameplay:** human-run test or recorded game run, settings, exact actions, diagnosis/treatment outcome, save/load, baseline regressions, screenshots and output log.

`Verify` initially validates policy files, absence of proprietary compiled artifacts, and any future tracked XML syntax. It **does not** compile a game DLL or run in-game tests.

## L4 case template

```text
Date:
Commit/package SHA256:
Project Hospital build:
DLCs enabled:
Other mods enabled:
Save type (new/existing/disposable):
Scenario and prerequisites:
Steps performed:
Expected:
Actual:
Result (PASS/FAIL/BLOCKED):
Raw log / screenshot references:
Known limitations:
```

## Required G1 gameplay cases

1. New ABCL blood-lead sampling appears for a valid lead-poisoning patient.
2. Sample reaches a staffed ABCL toxicology lab; specialist interacts with an actual required instrument.
3. Lab result returns to the physician and contributes to the diagnostic path.
4. Original CBC still processes at the original hematology lab.
5. Save, close, reopen and reload preserve functioning laboratory tasks and rooms.
6. Test-only spawn controls are off or absent in release configuration.

## G1 genuine L3 build — 2026-11-02 (UTC+8)

- Candidate: `a8e4dadd146ba925ec7b25641eddc43f25171eb1`; protected-main builder: `4eacfef6be50298d5930a6e0b40e6cbfec54528e`.
- [Actions run 41331315755](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41331315755), job `124921843743`: PASS.
- Windows Server 2022; .NET SDK 8.0.427 installed by setup-dotnet; target `net35`, C# 3. Compiler: 0 warnings, 0 errors.
- Owner-authorized AES-256-GCM references decrypted successfully in temporary runner storage; key held only in Actions Secret.
- Produced `ModABCLG1LeadTest.dll`: 7,168 bytes; CLR metadata `v2.0.50727`; SHA256 `9443fa71f3c989aaf865beaba7e240e055e0b2a9c8a4a55dc16b3f7d8015ecaa`.
- Test install package SHA256: `036e7cc1f8c149a562e5cbfbc13b1731da3043bbe5b85c2d02e69fc160c135dc`.
- Actions artifact `ABCL-G1-Compiled-TestOnly`, ID `13092844976`, 9,073 bytes; outer artifact SHA256 `572053f852cef9f5ddf59074110fefe644a58e9334bc5e4ec3e1e18ce9520f0c`; retention ends 2026-11-09 01:25 UTC+8.
- Downloaded artifact inspected: five ABCL XML files, ABCL panel DLL, zero-byte loader marker, installer and test instructions. No original game DLLs or decryption key included. DLL hash matches BUILD_INFO.
- L4 remains NOT RUN: native patient spawning, independent blood-lead workflow, original CBC and save/load require in-game testing. This is not an Alpha release. PR #7 remains draft.

### Genuine reference SHA256 recorded by the build

| Assembly | SHA256 |
| --- | --- |
| Assembly-CSharp.dll | `1120D899FB74D16F31115C5C27325EDBD1154B68E9419E6B7EA03CC3D43B6F24` |
| Assembly-CSharp-firstpass.dll | `63294CC19E24ECBE76F17F0776C9ABF6BF84358C4EF0B55967F141871308360F` |
| UnityEngine.dll | `0613DEFCBE1E30BFBA003D1A18E06000D6606FE14958E89752BA4C74CC7DD673` |
| UnityEngine.CoreModule.dll | `F65BEC39F0D3E75BAC559130775FC7C965BCB3AF03E1B44BC59C004F72F8645F` |
| UnityEngine.IMGUIModule.dll | `3B8E0A9655BAF1EDBA10D68464D03280F9B00D88BDAB0E5CFB1E7B409652C400` |

Game marketing version, DLC/Workshop combinations and gameplay behavior have not been verified by this compile.

## G1 first user L4 attempt — 2026-11-02 (UTC+8), reported

- Source: owner direct in-game test report, with screenshot of an exclamation indicator in the department UI. The screenshot does **not** include the complete G1 spawn-panel status text or a runtime exception log.
- Compiled G1 candidate identified in this PR: `a8e4dadd146ba925ec7b25641eddc43f25171eb1`, Actions `41331315755`; **the owner has not independently supplied the installed package hash**.
- Game started: **reported PASS**.
- New ABCL toxicology laboratory present / inspected: **reported PASS for visibility**, not evidence that the lab is fully operational; the department's warning indicator is unresolved.
- G1 test-panel present: **reported PASS for visibility**.
- Spawn one lead-poisoning patient: **reported PROBLEM / BLOCKED**, exact outcome and exception are unknown. Do not assert a confirmed runtime exception or a confirmed C# defect without the panel status and a log.
- Independent blood-lead sampling, laboratory result, vanilla CBC and save/reload: **NOT RUN**.
- Game version, active DLCs, Workshop mods, game-time state, normal intake/insurance state and screenshot of the spawn-panel status: **not supplied**.

### Focused source diagnosis (not yet a repair)

The ABCL panel calls the same `LopitalEntityFactory.CreateCharacterPatient` overload and schedules `m_fVisitTime` in the same pattern as the original `EventScriptTest.Activate`. Vanilla `BehaviorPatient.UpdateStateSpawned` waits for simulation time and validates insurance before un-hiding the patient. The original blood-lead main symptom `SYM_LEAD_LEVELS_HIGH` is marked `PatientMobility=IMOBILE`, so subsequent patient flow must be checked in actual gameplay. An exclamation icon in the screenshot alone cannot identify a failing room or missing staff.

**Next minimal evidence:** Screenshot immediately after clicking the G1 spawn button, showing its status line; if it reads `Spawn failed. Check output_log.txt.`, supply the error beginning with `[ABCL G1] Spawn failed:` from the game's runtime log. If it instead says `Requested one lead poisoning patient`, record whether simulation time is unpaused and a normal clinic can admit patients. Do not press the spawn button repeatedly or change a real save.

**Gate:** L4 remains **BLOCKED**, Issue #2 open, PR #7 draft. No Alpha claim, no source repair applied before the failure mode is known.

### Focused L4 patient-spawn diagnosis and one bounded repair — 2026-11-02

Owner's second screenshot shows the exact G1 panel message `Requested one lead poisoning patient. Check arrival.` after the click. From the old `SpawnOne()` source, this establishes `TRM_LDP` lookup, non-null native factory result, and `floor.AddCharacter(patient)` returning without exception; **not** visible admission. No `Spawn failed` exception is reported.

Source-backed mechanism (original game XML + ILSpy):
- Original `TRM_LDP` includes `SYM_LEAD_LEVELS_HIGH` with `ProbabilityPercent=100`.
- That symptom has `PatientMobility=IMOBILE`.
- The old test panel forced `PatientMobility.MOBILE`, unlike the disease's mobility. Vanilla `BehaviorPatient.UpdateStateSpawned` subsequently checks whether the insurance company is contracted and whether the immobile patient quota is positive; the patient may transition to `SpawnedFromDisabledInsurance` or `ReservingAmbulance`, instead of being admitted as a normal walk-in.
- Vanilla `LopitalEntityFactory.DebugAddPatients` also requires an inpatient department and at least one ambulance for immobile patients. This is distinct from the ABCL room's own equipment/technologist requirements.

**One D009-bounded correction was committed to PR #7** (new source changes after the successful original L3 build): preflight an inpatient department, an ambulance, a valid contracted insurer with an immobile slot; create `TRM_LDP` with `PatientMobility.IMOBILE` and that insurer; report "queued for native ambulance arrival" rather than suggesting the patient should walk in. Added static source assertions for the expected route.

**Gate reset for corrected source:** the earlier successful L3 build `41331315755` belongs only to old source SHA `a8e4dadd146ba925ec7b25641eddc43f25171eb1`. The corrected C# source is **L3 NOT YET RUN** until it is compiled with original-game DLLs on the trusted runner; corrected L4 **NOT RUN**. The user's previous three UI observations remain true for the original package but do not validate the corrected package.

Next validation in a disposable hospital: ensure operational inpatient care, ambulance, suitable insurance quota, advance game time, verify an actual ambulance arrival, then follow the lab sample/result and vanilla CBC. If the single corrected route still fails, record exact evidence and apply the project stop/re-scope gate rather than making repeated speculative changes.

## R1 corrected build and second owner L4 attempt — 2026-11-02 (UTC+8)

- Owner report explicitly identified source SHA `ea1a9ecb76484b9f86e5cc54dcf659f5548b3160`.
- **L3 PASS — verified independently:** Actions `41369385877`, genuine net35/CLR2 Windows runner job `125036379770`. Logs confirm `Verified SHA ea1a9ecb76484b9f86e5cc54dcf659f5548b3160`, checkout of that exact commit, decrypted original-game references, `Build succeeded`, **0 Warning(s), 0 Error(s)**, packaged and uploaded artifact `ABCL-G1-Compiled-TestOnly` ID `13109130314` (9,502 bytes). Actions' outer artifact SHA256: `6b800f65e56991eb52904294890ae9fe2de7f0db651075144c9eb6db9f9f1bd4`. This proves compilation and artifact creation, **not** which binary hash the owner installed.
- **L4 FAIL/BLOCKED at step 3:** owner reports (1) R1 real compile pass, (2) previous G1 removed/new version installed, (3) combined 'game load and G1 interface' item **failed**. It is **not yet known** whether the game failed to open, game opened but the G1 test button was absent, or another failure. No screenshot, installation transcript, `output_log.txt`, `Player.log`, game version or DLC/Workshop list supplied.
- (4) native department prerequisites, (5) clicking spawn, (6) observed patient admission, (7-8) blood-lead sample/result, (9) original CBC, and (10) save/reload: **NOT TESTED**.
- Source delta from original working G1 GUI to R1: `HospitalIsReady()` and initial GUI button creation are unchanged; changes involve panel window size/text and the `SpawnOne()` immobile-patient method. The installer and original G1 XML have not changed. Therefore a missing GUI before clicking Spawn is **not proof** that immobile insurance preconditions were the cause. Runtime type loading, addon-file placement, hospital readiness or Unity log errors remain unproven hypotheses.

**Required first discriminator:** does the game reach an in-hospital scene but the `ABCL G1 [Test]` button not appear, or does game/start/save loading itself fail? For the former, inspect the current Addons/ModABCLG1LeadTest location and whether code mods are enabled, then the log for `ModABCLG1LeadTest`, `ModEntryPoint`, `TypeLoadException`, `MissingMethodException` and `[ABCL G1]`. For the latter, stop further gameplay testing, close the game and isolate only the new addon after preserving logs. Do not delete original game XML or modify long-term saves.

**Gate:** R1 L3 PASS; R1 L4 FAIL/BLOCKED, Issue #2 remains open and PR #7 Draft. No second speculative code change; one bounded D009 source correction has already been made and needs an evidence-based failure classification before stop/re-scope.

## Corrected R1 L4 report, superseding the prior step-3 failure — 2026-11-02 (UTC+8)

The owner submitted a new R1 report for source candidate `ea1a9ecb76484b9f86e5cc54dcf659f5548b3160`, correcting the earlier ambiguous "game load/G1 interface FAIL" outcome:
- R1 original-game-DLL compilation: PASS, independently verified GitHub run `41369385877` / artifact `13109130314` (same specific R1 candidate).
- Removed previous version, installed R1: owner-reported PASS (local installed-binary SHA not independently supplied).
- Game loads and G1 panel appears: owner-reported **PASS** (supersedes earlier report).
- Required original departments and equipment: owner-reported PASS, **not independently itemized**.
- Click Spawn once: owner-reported **FAIL**, no R1 status message or game log supplied.
- Ambulance arrival and lead-patient admission: owner-reported **FAIL** after emergency hospitalization was opened, but no detailed admission state, visible vehicle status or log supplied.
- Original CBC: owner-reported **PASS**, no screenshot, trace, or steps attached.
- Blood-lead sample prescription, lab result, save/reload: **NOT TESTED**.
- Game version, DLC/Workshop combination: not supplied.

### Source-grounded differential for an inpatient department without arriving ambulances

The R1 `SpawnOne()` button checks `Hospital.HasAnyInpatientDepartment()`, `Hospital.GetRandomDepartmentWithDiagnoses(PatientMobility.IMOBILE)`, `AmbulanceManager.GetAmbulanceCount()`, and one randomly selected insurer's `m_immobileSpawnedToday` and `m_isContracted` before creating an entity.

Important original-game semantics from inspected decompiled sources:
1. `Hospital.HasAnyInpatientDepartment()` checks `DiagnosisRandomizerImmobile.Count > 0 && department.AcceptsOutpatients()` (despite its misleading method name), while `GetRandomDepartmentWithDiagnoses(IMOBILE)` separately requires `AcceptsInpatients()`. Opening hospitalization alone does not prove both conditions.
2. `AmbulanceManager.GetAmbulanceCount()` counts **owned nonexternal, nonhelicopter** ambulances, not whether one is usable. `GetFreeAmbulance(...)` requires an ambulance `PARKED`, no assigned patient, not `m_stopped`, and `m_callCount < AMBULANCE_MAX_CALLS_PER_DAY` (absent event allowance).
3. `InsuranceManager.GetRandomImmobileCompany()` selects based on `m_immobileSpawnedToday > 0`, or falls back to the first insurer; the R1 preflight can report a missing insurer slot even when inpatient service has just been opened and quotas have not been recalculated. `InsuranceCompany.CalculatePatientCounts` sets immobile count to zero when no eligible inpatient department is open.
4. The native patient factory constructs an immobile patient and sets `PatientState.ReservingAmbulance` before returning. A successful returned object is **not evidence** that `GetFreeAmbulance()` ever finds a vehicle or that a patient arrives.

These are *possible* bottlenecks, not a confirmed single cause. The missing **one discriminating piece of evidence** is the R1 G1 panel **status text immediately after the single button click** (`Need an operational inpatient department`, `Need at least one ambulance`, `No contracted insurer ...`, `Spawn failed`, or `Lead patient queued for native ambulance arrival`). If queued but no vehicle arrives, the next evidence is the native game log and ambulance availability/state.

**Disposition:** G1 R1 L3 PASS, L4 BLOCKED at patient spawn/admission, CBC reportedly passes. D009's single code correction has already been used; no additional speculative source patch or extra research Issue. Keep Issue #2 open, PR #7 Draft, no release, no Alpha claim. Earlier contradictory step-3-failure report is superseded, not erased.

## R1 observed status: preflight aborts before creating a patient — 2026-11-02 (UTC+8)

**New owner evidence:** immediately after pressing the R1 test button, its exact status is `Need an operational inpatient department for immobile patients.` This is a preflight failure, not an ambulance routing or patient-arrival failure. The C# source enters this branch before checking ambulances, insurer quota or invoking `LopitalEntityFactory.CreateCharacterPatient`. No new G1 lead patient was created by this click. The previous report of "ambulance arrival FAIL" is therefore reclassified as **NOT REACHED / NOT TESTED**, not as a proven ambulance fault.

**Precise conditional:** the branch triggers if either `Hospital.HasAnyInpatientDepartment()` returns false OR `Hospital.GetRandomDepartmentWithDiagnoses(PatientMobility.IMOBILE)` returns null. Those two outcomes are indistinguishable with the current single combined UI message.

**Original-game source check (private ILSpy decompilation, not committed):**
- `Hospital.HasAnyInpatientDepartment()` tests whether some department's `DiagnosisRandomizerImmobile.Count > 0` **and** `AcceptsOutpatients()` succeeds. Despite its name, it does not by itself require operational hospitalization.
- `Hospital.GetRandomDepartmentWithDiagnoses(IMOBILE)` filters out closed departments and requires `AcceptsInpatients()` **and** a nonempty immobile diagnosis pool.
- `Department.AcceptsOutpatients()` for clinical departments requires valid required outpatient rooms and at least one available **day-shift** outpatient doctor assigned to an outpatient-compatible home room. `AcceptsInpatients()` requires all applicable departmental minimum inpatient staffing, valid inpatient rooms and stretcher counts.
- Offline cross-check of owner-supplied original `StreamingAssets/Database/Diagnoses/DiagnosesER.xml`, other vanilla diagnosis XML, vanilla symptom metadata and `GameDBDepartment.UpdateDiagnoses()`: the **30** vanilla `DPT_EMERGENCY` diagnoses contain **zero** symptoms whose mobility is `IMOBILE` or `INTUBATED`. Hence the original Emergency department alone cannot satisfy the R1 nonempty immobile diagnosis pool requirement, even when its clinic and hospitalization both work. This conclusion is specific to the supplied vanilla dataset; DLC/Workshop overrides may alter diagnosis lists.
- The original Internal Medicine department `DPT_INTERNAL_MEDICINE_DEPARTMENT` has **15** diagnoses with immobile symptoms; `TRM_LDP` itself is assigned to Internal Medicine. Both an operational **Internal Medicine outpatient clinic** and **Internal Medicine hospitalization** are the relevant base-game capability to test.
- Vanilla Internal Medicine minimum rooms: outpatient office + waiting room; hospitalization inpatient office, on-call room, nurses' station, inpatient ward, high-priority inpatient ward. Min day clinic doctor = 1; inpatient day/night doctor = 1 each, day/night nurse = 1 each, stretcher = 1. Room and staff operational validity still need the game UI to confirm; do not bypass this with a Harmony patch.

**No-code next test in a disposable hospital:** make Internal Medicine available, satisfy both outpatient and hospitalization requirements and check there are no corresponding validity warnings. Then click R1 spawn exactly once, recording the new panel status. If it advances to `Need at least one ambulance`, `No contracted insurer ...`, or `Lead patient queued ...`, the precise preflight gate has been cleared. If the *same* inpatient status persists after documented valid Internal Medicine outpatient+inpatient readiness, capture the department panels or runtime log; the two disjuncts cannot yet be identified independently.

**State:** R1 L3 PASS, L4 stopped at department preflight; ambulance and subsequent G1 tests NOT REACHED. No additional source correction, no release, Issue #2 remains open and PR #7 remains Draft. D009's one-code-repair budget is preserved as already consumed, with a no-code environment diagnosis now supported by concrete original game source.

## G1 cross-department laboratory routing control — 2026-11-02, offline only

The owner previously reported full vanilla CBC functionality (including an R1 CBC regression PASS). **No additional CBC gameplay test has been requested.**

A new privacy-preserving, source-level diagnostic implementation was committed:
- `tools/audit_g1_native_route.py` (requires only the developer's local original `StreamingAssets/Database` to inspect real room and exam tags; outputs aggregate JSON and does not copy original records).
- `tests/test_g1_native_route_audit.py` (public `Verify` synthetic XML tests, no proprietary fixtures).
- The original-game `GameDBDepartment.CanHaveAnyRoom` and `ProcedureComponent.UpdateAllExaminationsForMedicalCondition` source predicates were compared to `ProcedureSceneFactory.CreateProcedureScene`, `BehaviorPatient.FindLabSpecialist`, and vanilla lab reference XML.

On the inspected owner-supplied game dataset, both **Emergency** and **Internal Medicine** patient departments allow the G1 sampling tag (`examinations_basic_equipment`) but not its linked lab-testing tag (`abcl_g1_toxicology_lab`). **The same static check fails for original CBC's linked test tags** (`deprecated_lab` / `hematology_lab`) from these two departments, despite the owner's observed successful CBC. The ABCL target room is correctly `stat_lab`, and the lab-test's `FallbackLabDepartmentRef=DPT_LAB` can find the ABCL room after local optional room registration. Native lab-specialist lookup has explicit DPT_LAB fallback paths.

**Interpretation:** A `NOT_AVAILABLE_DEPARTMENT` return from this one examination-list predicate is a **possible source-path warning**, not evidence that a custom test cannot reach the laboratory at runtime; vanilla CBC is a negative control showing why the overall flow must be investigated. No vanilla department or CBC data was modified to silence this warning.

**Current deliverables:** Offline auditor + synthetic-data tests + updated `docs/G1_SINGLE_PASS_L4_PROTOCOL.md`. No new executable or test-patient fixture was built. R1 genuine L3 PASS only for the original corrected candidate `ea1a9ec`, L4 still BLOCKED at clinical department preflight. ABCL blood-lead ordering, sample processing, result return and save/load remain untested. A benign mobile test-only fixture remains an engineering **proposal**, not a validated feature or owner test authorization.

## G1 R2 outpatient lab-fixture source — 2026-11-02 (no gameplay evidence)

**Test-only engineering re-scope ABCL-D013.** This is a new *candidate*, not a repair claimed to have passed L3/L4 and not an Alpha clinical design change.

The draft PR #7 branch now contains:
- R2 `src/ABCLG1Panel.cs`: a one-click **mobile** patient based on original Emergency `DIA_CLD` clinic condition, with valid outpatient office checks, a contracted visible insurer with a positive walk-in quota, and a strict check that the test diagnosis contains the ABCL sampling exam before creating a patient.
- `tools/Install-ABCL-G1.ps1`: addon-local override of `DIA_CLD` derived from the user's original `DiagnosesER.xml`, retaining the optional original `DPT_LAB` room override. No R2 modifications to real `TRM_LDP` or `SYM_LEAD_LEVELS_HIGH`; no writes to installed original game XML.
- The original independent ABCL sampling/testing pair and DPT_LAB toxicology room remain unchanged for this test, with the native `FallbackLabDepartmentRef` intact.
- R2 tests now check `DIA_CLD`, `PatientMobility.MOBILE`, outpatient readiness, original lead case non-interference and CLR2 native `GameDBPointer<T>.IsValid` usage. An earlier candidate C# nullable comparison was corrected after inspecting the original `GameDBPointer<T>` **value type**; this avoids an obvious compiler ABI mismatch but is NOT a substitute for L3.
- An offline native route auditor and synthetic control tests were added. Their static route report shows that both G1 and original CBC have the same patient-department linked-lab-tag mismatch, so neither a static warning nor a green `Verify` establishes end-to-end G1 routing.

**Gates currently pending:** R2 exact source SHA genuine Windows net35 game-DLL build and artifact SHA; verify the complete built package has only ABCL files; native doctor UI orderability, sample transport, ABCL room specialist/equipment work, result returned, and save/load are all **NOT TESTED**. The benign fixture does not provide a medically positive lead result; true original `TRM_LDP` remains a separate future L4 acceptance scenario. Owner must **not** install the staged source or run another game test until an independently reviewed, genuine R2 L3 artifact and consolidated one-pass L4 checklist are ready.

**Previously verified:** R1's exact genuine L3 build PASS (`41369385877`); the owner previously reported original CBC working, so CBC workflow discovery need not be repeated.

## G1 R2 complete laboratory workflow — owner-reported L4 PASS, 2026-11-02

**Provenance:** Owner submitted a completed, clickable 14/14 test checklist in ChatGPT; no raw screenshots, game log, game build number, or enabled DLC/Workshop inventory supplied. All 14 results are **owner-reported**, not independent telemetry. No failure was reported.

**Exact build:** source SHA `7f3c5f29cebd39338df854a1475ceb604dca164f`, GitHub Actions genuine game-reference Windows/net35 L3 `41377881918` (0 warnings, 0 errors), artifact `13112246582`. R2's disposable-save `DIA_CLD` Emergency mobile-patient fixture and addon-local examination override, not a real lead-poisoning `TRM_LDP` patient.

**Owner checklist — all PASS:** (1) old G1 removed/new R2 installed; (2) disposable save and conflicting old tests excluded; (3) Emergency outpatient clinic operational; (4) vanilla hematology staffed/operational; (5) ABCL toxicology room/equipment/staff ready; (6) game and G1 R2 panel load; (7) one patient spawned and actually arrived; (8) physician could order ABCL blood-lead sampling; (9) sample taken by staff; (10) sample entered ABCL lab queue; (11) lab specialist operated equipment and completed analysis; (12) result returned to physician; (13) vanilla CBC completed; (14) save/quit/reload preserved lab operation. Failure description: none.

**Gate interpretation:** R2 independent ABCL lab *technical test-fixture path* L3+L4 **PASS (owner report)**. The prior `NOT_AVAILABLE_DEPARTMENT` static-predicate concern is now resolved by actual observed result for this tested configuration, not by expanding vanilla Emergency metadata or Harmony patching. R1 severe inpatient/ambulance harness remains retired under D013. Genuine positive blood-lead poisoning case (`TRM_LDP`), medical diagnosis/treatment/discharge, non-test release without debug fixture, game build/DLC/Workshop combinations, and uninstall/legacy-save behavior remain **NOT TESTED**. G1-001 remains open for its original clinical-case acceptance. Do not falsely classify Alpha or all compatibility as passed. Keep PR #7 Draft and retain history.


## G1 R3 genuine L3 and first artifact audit — 2026-11-02

- Exact C# candidate: `b0a66222f483319baf8750f23c7d064021781a23`.
- Owner-dispatched [Actions run 41389454623](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41389454623), job `125097403764`: immutable Verify gate PASS; exact candidate checkout; owner-authorized encrypted references decrypted in runner temporary storage; genuine Windows 2022 build against the five original game assemblies.
- Target `net35`, C# 3 / CLR2 metadata; compiler **0 warnings / 0 errors**. Output DLL `ModABCLG1LeadTest.dll`, 13,312 bytes; SHA256 `BDC8F9DF8EA8FA945D0277C11CB012E893ACB2A7157A75412152DABC334BA310`.
- Actions artifact `ABCL-G1-Compiled-TestOnly`, ID `13116563798`, 13,776 bytes; outer SHA256 `563edcf7b2e2d9bb1217a8282ab18b32e044f950914a059c0fe01f883d22451b`. Inner install ZIP SHA256 `64c67f4008fc43e23db2ff23492399d8434a1b517f8cf04fbb9bdf2c82710494`.
- Independent archive audit: package contains the ABCL DLL, five ABCL-owned XML/localization files, installer, README and an intentional zero-byte `0Harmony.dll` loader marker. No original game DLL, decrypted reference archive or AES key is present. `BUILD_INFO.txt` candidate SHA and DLL hash match the run.
- **Important packaging correction:** this first artifact's R3 installer message still said OFFLINE REVIEW ONLY and its generic CMD launches the R2 default. It is evidence of R3 L3 and package contents, but **not the artifact to install for L4**. A refreshed R3-specific installer command and protocol must pass Verify and a fresh exact-SHA build before gameplay.
- R3 L4 remains **NOT RUN**. R2's owner-reported 14/14 L4 result remains historical and is not repeated.



## G1 R3 second genuine L3 build and artifact audit — 2026-11-02

- Exact candidate source: `ba68b17723587c07baf791127bd751dcdde05546`.
- Owner-dispatched [Actions run 41391190322](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391190322), job `125102727949`: Verify gate passed for the candidate; log confirms exact candidate checkout; owner-authorized encrypted references decrypted in runner temporary storage; genuine Windows Server 2022 build against the five original game assemblies.
- Target `net35`, CLR 2 metadata; compiler **0 warnings / 0 errors**. Output DLL `ModABCLG1LeadTest.dll`, 13,312 bytes; SHA256 `1E3B244FEE4B48F185F3DD716BD4ED0CE0A7F905BD06F32E0F25FBA0293990AC`.
- Artifact `ABCL-G1-Compiled-TestOnly`, ID `13116939196`; outer archive SHA256 `4c7bde7fda7df5eeb5d7ea839adc9d36c5bbd732158f9f7cc97660505c1b0b42`; inner install ZIP SHA256 `8d6d6da77c48f4ad2fb2cab23dce47eab104eec973ea397813271cbffb7e6c02`.
- Independent downloaded-archive inspection: BUILD_INFO candidate SHA and DLL SHA match. Inner ZIP contains ABCL DLL, ABCL-owned XML/localization, zero-byte native-loader marker, README, `Install-ABCL-G1.ps1` and generic `INSTALL_G1.cmd`; it **does not contain `INSTALL_G1_R3.cmd`**. No original game DLL, decrypted references or AES key is present.
- **Root cause established from the workflow run and source:** the manual dispatch was made on `main` at workflow revision `6fd635e2bbe2e36bc9724b8b2cada96a8b6ca253`. GitHub executed that main-branch workflow, whose package command still copied only the R2 launcher. The workflow then checked out candidate source `ba68...` for compilation; a candidate's corrected workflow file does not replace the workflow definition already selected for the run.
- **Disposition:** genuine L3 PASS for this exact candidate; package audit FAIL; artifact `13116939196` is **NOT FOR INSTALLATION**. R3 L4 remains NOT RUN. The next build must execute the corrected feature-branch workflow (owner-only exact branch gate) and confirm the R3 launcher is present while the generic R2 launcher is absent.


## G1 R3 corrected-branch genuine L3 build and independent package audit — 2026-11-02

- Exact candidate source: `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`; workflow dispatch branch: `feature/g1-secure-build`.
- Owner-dispatched [Actions run 41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), job `125105163406`: run conclusion **success**. The log confirms the candidate Verify check was queried and accepted, exact candidate checkout, owner-authorized encrypted references decrypted only in runner temporary storage, and real Windows Server 2022 compilation against the five original game assemblies. Candidate checks: Verify PASS (26/26), CodeQL PASS, Analyze Python PASS.
- Target `net35`, C# 3 / CLR 2 metadata; compiler **0 warnings / 0 errors**. Output `ModABCLG1LeadTest.dll`, 13,312 bytes; SHA256 `80538D30D6BE164466F21151199B752FE07F076564D6B1A1DD69D4698CA02466` (matches downloaded artifact BUILD_INFO).
- Artifact `ABCL-G1-Compiled-TestOnly`, ID `13117942292`, 14,946 bytes; outer artifact SHA256 `3d961a05cae82d7cdf319a3c7e9df2a9ff37fe267705a2e31648a76a9bbe671f`.
- Inner install archive `ABCL_G1_Compiled_Install_TestOnly.zip`, 15,384 bytes; SHA256 `f95932142a813afab7070e9aa160b9f71e454d2b515b8b5e50ad46628cdca7c3`.
- Independent archive audit: exact candidate SHA and DLL SHA match BUILD_INFO. Inner ZIP contains the ABCL DLL, five ABCL-owned XML/localization files, the intentional zero-byte `0Harmony.dll` loader marker (workflow comment says it is never loaded), `G1_TEST_README.txt`, `Install-ABCL-G1.ps1`, and **`INSTALL_G1_R3.cmd`**. It does **not** contain the R2 generic `INSTALL_G1.cmd`. No original game DLL, decrypted reference archive, or AES key is present.
- The downloaded user-supplied original `StreamingAssets.zip` was checked read-only: exactly one original `DPT_LAB` and one `TRM_LDP` entry exist in the expected source XML files. `DPT_LAB` retains mandatory `ROOM_TYPE_HEMATOLOGY_LAB` MinCount 1; `TRM_LDP` points to `DPT_INTERNAL_MEDICINE_DEPARTMENT`, retains 100% `SYM_LEAD_LEVELS_HIGH`, and contains original `TRT_HOSPITALIZATION_HIGH_PRIORITY` and `TRT_CHELATION_THERAPY`. The installer creates addon-local copies and refuses to overwrite an existing ABCL test addon; no installed original XML is modified by the script.
- **Disposition:** genuine L3 PASS and independent package audit PASS. Artifact `13117942292` is eligible for **one controlled R3 test-only L4 attempt**, not Alpha or release. R3 actual patient creation, ambulance reservation/arrival, admission, ABCL sample collection/lab result, hospitalization, chelation, CBC regression, and save/reload remain **NOT YET L4-TESTED**. No DLC/Workshop compatibility claim is made. Keep Issue #2 open and PR #7 Draft.


## G1 R3 owner screenshot — preflight blocked by native insurer quota, 2026-11-02

**Owner evidence:** screenshot of the installed R3 test panel in a disposable hospital. The following read-only preflight results are visible:

- Native `TRM_LDP` + ABCL exam: OK.
- Internal Medicine outpatient: OK.
- Internal Medicine inpatient: OK.
- Native immobile diagnosis pool: OK.
- Native hospital intake gate: OK.
- Contracted immobile insurer quota: **ZERO**.
- Parked free ambulance: OK.

The request button is disabled by the R3 preflight. Owner did **not** click it. No patient was created; no ambulance reservation, dispatch, arrival, admission, sampling, lab work, treatment, CBC regression or save/reload was attempted. This is a preflight blocker, not a patient-spawn failure and not an L4 clinical-path failure.

**Source-based diagnosis, using the owner-supplied original game data and ILSpy source:**

- `src/ABCLG1Panel.cs::ChooseEligibleImmobileInsurer` selects only an insurer that is contracted, not hidden, has `m_immobileSpawnedToday > 0`, and has a valid original database pointer/entry.
- Original `BehaviorPatient.UpdateStateReservingAmbulance` checks the same native contract/quota boundary. If the patient is not from a level and its insurer is not contracted or `m_immobileSpawnedToday == 0`, vanilla switches it to `SpawnedFromDisabledInsurance`. Removing the preflight gate would create a false-positive patient that vanilla rejects.
- All regular non-campaign insurance entries in the supplied `StreamingAssets/Database/InsuranceCompanies.xml` start with `ImmobilePerDay=0`. Their positive IMOBILE quotas are granted through sequential insurance objectives (for example, Cheap O'Care's `SET_IMMOBILE_PATIENT_COUNT=3` after its three-ambulance objective; Federal Med's `SET_IMMOBILE_PATIENT_COUNT=2` after its prerequisite objectives including a working ICU hospitalization and one ambulance). Campaign-only hidden insurers with positive base quotas are not a general sandbox workaround.
- The native quota is calculated from the contracted company's current quota/reward state and the presence of an IMOBILE diagnosis department. The panel already reports the IMOBILE diagnosis pool and hospital intake gate as OK, so the remaining observed gate is the insurer state/quota.

**Next discriminator:** inspect the user's Hospital Management → Insurance Companies screen once, including contracted companies, their incoming patient/trauma (immobile) counts, and current objective/reward progress. Do not buy ambulances, change contracts, advance objectives, click patient generation, or patch the quota until the currently contracted insurer and its active objective are known. Keep R3 L4 blocked at preflight; Issue #2 open; PR #7 Draft.


## G1 R3 native Liver TY / ICU preflight diagnostic repair — 2026-11-02

**Why the repair was made:** the owner identified the normal vanilla route after the first R3 panel screenshot showed `Contracted immobile insurer quota: ZERO`. The screenshot itself did not show an attempted patient creation; the request button remained disabled and no click occurred.

**Original data confirmation (owner-supplied StreamingAssets, read-only):**
- `IN_COM_CCC` localizes to **肝泰保险** in `StringTableZhHansNames.xml`; English localization is **Liver TY**. The active patched record is `IN_COM_CCC_PATCH_1_1`, with stable `NameLocID=IN_COM_CCC`.
- Liver TY objective #4 (zero-based index 3) requires `WORKING_HOSPITALIZATION_AT_DEPARTMENT` for `DPT_ICU` and rewards `UNLOCK_AMBULANCES`.
- Objective #5 (zero-based index 4) requires `NUMBER_OF_AMBULANCES >= 1` and rewards `SET_IMMOBILE_PATIENT_COUNT=2`.
- Vanilla `InsuranceCompany.IsRequirementPassed` evaluates `WORKING_HOSPITALIZATION_AT_DEPARTMENT` by checking `Department.AcceptsInpatients()`; the panel's ICU readiness line mirrors that predicate.
- `ProcessReward(SET_IMMOBILE_PATIENT_COUNT)` writes `m_currentImmobilePatients`; vanilla `CalculatePatientCounts` separately derives the live `m_immobileSpawnedToday` quota and zeroes it if no eligible IMOBILE diagnosis department exists. The new panel shows configured target and live daily value separately.

**Source change on the existing Draft PR #7 branch:**
- Added read-only identification of the visible Liver TY company by stable `NameLocID`.
- Added ICU hospitalization readiness, Liver TY objective #4/#5 completion, native ambulance-unlock state, actual ambulance count, configured IMOBILE target, and live daily quota to the R3 panel.
- Kept the actual patient factory and one-attempt latch unchanged.
- Kept vanilla insurer eligibility: any visible contracted insurer with a positive live IMOBILE quota remains eligible. Liver TY is displayed as the standard unlock route, not hard-coded as the only possible valid insurer.
- No call to `CalculatePatientCounts`, `ProcessReward`, contract APIs, or quota mutation is added. No vanilla XML, insurance objective, ambulance, diagnosis pool or treatment is changed.
- Expanded the R3 panel window to fit the extra diagnostic lines.
- Added static tests for the Liver TY chain, non-hardcoded insurer selection, and read-only preflight.

**Static verification:** exact candidate `66c95d61a63619e3377b59feac9b5241d3ffb924` passed GitHub Verify **29/29 tests** (Actions run `41402697471`), CodeQL and Analyze Python (run `41402697480`). The selection regression test confirms the harness still accepts any native eligible insurer rather than hardcoding Liver TY. The helper explicitly ignores the deprecated base `IN_COM_CCC` stub and inspects the active patched record by stable `NameLocID`.

**Disposition:** source/logic repair and static gates PASS. Genuine Windows/net35/CLR2 L3 for exact candidate `66c95d61a63619e3377b59feac9b5241d3ffb924` is **PENDING**; no refreshed artifact exists. Historical artifact `13117942292` corresponds to the pre-diagnostic source and does not include this repair. Do not use it as the updated panel build. No new gameplay attempt has occurred; R3 L4 remains blocked until the native live IMOBILE quota is positive and a free parked ambulance is available. Keep Issue #2 open and PR #7 Draft.


## G1 R3 end-to-end native lead-case L4 — owner-reported PASS (2026-11-02)

**Provenance and exact tested package**
- Evidence source: the project owner supplied the completed real-game test report in this conversation. No screenshot, raw game log, or independent telemetry was attached; results below are therefore recorded as **owner-reported**, not independently corroborated.
- Tested package: `ABCL-G1-Compiled-TestOnly`, Actions artifact **`13117942292`**, from [Actions run 41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195).
- Exact compiled source SHA: `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`.
- The artifact had already passed genuine Windows Server 2022 / net35 / CLR2 compilation (0 warnings, 0 errors) and independent package audit. Outer artifact SHA256: `3d961a05cae82d7cdf319a3c7e9df2a9ff37fe267705a2e31648a76a9bbe671f`; inner install ZIP SHA256: `f95932142a813afab7070e9aa160b9f71e454d2b515b8b5e50ad46628cdca7c3`.
- Important source distinction: artifact `13117942292` predates the later read-only Liver TY / ICU diagnostic-panel enhancement. It validates the R3 gameplay implementation at SHA `1a13e8d9...`, not the newer diagnostic-panel source candidate `7faf31c6...`.

**Reported environment and preflight**
- Correct R3 install package: PASS.
- Fresh temporary hospital save: PASS.
- No third-party Workshop mods and no old ABCL test plugins: PASS.
- Internal Medicine outpatient and inpatient services operational: PASS.
- Original laboratory, hematology laboratory and day-shift staff ready: PASS.
- ABCL toxicology laboratory, equipment and specialist ready: PASS.
- Contracted insurer had a positive live IMOBILE daily quota: PASS.
- An available parked, unassigned ambulance existed: PASS.
- All preflight items shown by the installed R3 panel: PASS.
- Game version: **NOT PROVIDED**.
- Official DLC enabled: **NOT PROVIDED**.
- The insurer's name and its exact objective/reward state were not separately recorded.

**Owner-reported gameplay results — all listed items PASS**
1. Game launched and G1 panel displayed.
2. One click created an original native `TRM_LDP` patient.
3. A native ambulance was assigned and dispatched.
4. The ambulance arrived at the hospital.
5. The patient entered Internal Medicine.
6. The physician could order ABCL blood-lead sampling.
7. Staff collected the sample and sent it onward.
8. The specimen entered the ABCL toxicology laboratory queue.
9. A laboratory specialist operated the equipment and completed analysis.
10. The result returned to the physician.
11. Original high-priority hospitalization worked.
12. Original chelation treatment worked.
13. Original CBC regression passed.
14. After save, exit and reload, the laboratory remained functional.

**Evidence fields not supplied**
- Exact panel status immediately after the one click: **NOT RECORDED**.
- Game version and official DLC list: **NOT PROVIDED**.
- Screenshots and game logs: **NOT ATTACHED**.
- No failure or exception was reported.

**Gate assessment**
- R3 authentic `TRM_LDP` patient creation → native ambulance dispatch/arrival → Internal Medicine admission → ABCL sample collection → ABCL toxicology analysis → physician result → native hospitalization/chelation, plus CBC and save/reload, is **L4 PASS (owner-reported) for the tested package and configuration**.
- This is not evidence for every DLC configuration, Workshop combination, uninstall behavior, old-save migration, or release safety. Do not claim those as passed.
- The previously recorded zero-quota preflight was an earlier blocked attempt; this later report supersedes that state for the tested disposable save. Do not continue describing R3 L4 as blocked by zero quota.
- The newer diagnostic-panel candidate `7faf31c6bba34ab58a9e288217d0359956bd2af2` has Verify 29/29, CodeQL and Analyze Python PASS, but still needs its own genuine Windows/net35/CLR2 L3 build and package audit. The successful gameplay test on artifact `13117942292` does **not** validate those newer diagnostic lines.
- Because the newer C# delta is limited to read-only insurance/ICU/quota diagnostics and panel layout, while leaving the patient factory and one-attempt spawn path unchanged, do **not** repeat the full patient/laboratory/treatment sequence solely for that diagnostic change. After exact-SHA L3 and package audit, perform a focused panel display/preflight check only.
- Keep Issue #2 open and PR #7 Draft until the refreshed diagnostic candidate has its exact-SHA L3/package gate reviewed. Do not mark Alpha or broad compatibility complete.
