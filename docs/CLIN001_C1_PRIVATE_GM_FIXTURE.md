# CLIN-001 C1 — Disabled private GM clinical fixture (source-only candidate)

**State:** Developer-only source candidate. **NOT C1 clinical L4, NOT an exclusive-diagnosis C2 acceptance, NOT Alpha medical content.**
**Base:** G1 Draft PR #7 (trusted `net35/CLR2` test DLL). **Scope:** only C1 patient/assay routing.
**Private diagnosis:** `DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE` (`DPT_EMERGENCY`). EN: “Possible mild lead exposure (test only)”; zh-Hans: “疑似轻度铅暴露（仅测试）”.

## Reason for this work

The owner requested that the Chinese Super-GM in every later *development test* package can generate suitable patients without repeatedly unlocking insurer/clinic stages. The prior accepted R3 install overrides original `TRM_LDP` only for the genuine severe lead case. Its Super-GM default was `DIA_CLD`, which in R3 mode **did not** contain ABCL blood-lead sampling. Therefore successfully creating the old default fixture could not validate C1 positive assay routing.

## Native-source rationale (read-only, not shipped)

The provided original `dll_ilspy.zip` establishes:
- `Database.GetEntry<T>(ID)` returns a registered entry **without filtering** `GameDBMedicalCondition.Disabled`.
- `BehaviorPatient.RandomizeMedicalCondition` collects **only non-disabled** entries; `GameDBDepartment` excludes disabled entries from its normal disease randomizers.
- The explicitly specified native factory `LopitalEntityFactory.CreateCharacterPatient(Floor,Vector2i,GameDBMedicalCondition,PatientMobility,GameDBInsuranceCompany,...)` calls `BehaviorPatient.SetMedicalCondition`, and `MedicalCondition.CreateMedicalCondition` does **not** reject the `Disabled` flag outright.
- Therefore a disabled diagnosis with valid **existing MOBILE** symptoms can be a source-supported candidate for explicit GM-only creation without entering normal random disease pools. This is a candidate; object lifetime, actual arrival, lab job dispatch and save handling need real L4.
- `SYM_ABDOMINAL_PAIN`, `SYM_FATIGUE`, `SYM_HEADACHE` and `SYM_WEAKNESS` all have `PatientMobility=MOBILE` in the supplied base `Symptoms.xml`. The referenced original examinations/treatments exist and are ordinary **physician examinations**, not vanilla toxicology lab analyses.

## Candidate details and compatibility

- **No original game XML is written.** The existing `tools/Install-ABCL-G1.ps1` builds `ModDiagnoses.xml` in a temporary ABCL Addon staging directory. Only after its original R2/R3 addon-local copied diagnosis is generated does `Add-PrivateC1Fixture` append a **new** `GameDBMedicalCondition` with a unique private ID.
- `<Disabled>true</Disabled>` keeps it out of natural patient spawning. The same fixture is prepared in **both** R2 and R3 testing modes, preserving the existing default R2/R3 overrides and original adult game data. The addon installation still refuses overwriting an existing G1 addon folder or other installed test plugins.
- A new ID collision guard checks installed other addons before committing the staging directory. It does not claim universal protection against malformed or dynamically created third-party IDs.
- C1 medical content includes common mild symptoms, native rest/analgesic/home treatments, original physician interview/physical/palpation and exactly **one ABCL-owned** sampling ID `EXM_ABCL_G1_BLOOD_LEAD_SAMPLING` linked to testing `EXM_ABCL_G1_BLOOD_LEAD_TESTING`. No original CBC or vanilla lab-analysis examination is added or redirected.
- The in-game test-only GM now defaults to the C1 private diagnosis; it checks that the private record is disabled **and** linked to the real ABCL sampling ID before calling the native factory. For other user-input IDs, it refuses disabled original diseases, and keeps the native severe/immobile guard. It also verifies the returned patient's actual medical condition ID before reporting the creation request.
- Adds localized labels in the existing G1 EN/zh-Hans string tables. They deliberately contain “test only”; not production clinical prose. Original strings and G1 blood-lead labels are retained.
- No changes to `src/ABCL.G1.Panel.csproj` trusted project hash, private game references, GameDB room XML, FA devices, TO-004 V3 prefab art, CBC/other original labs or official DLC.

## Gate evidence / stop conditions

1. **L1/L2**: parse the test-only XML builder; assert unique private ID, Disabled, all mild mobile symptom references and meaningful accepted treatments, private sampling pair, bilingual localization, installer stage placement, noninterference, and GM preflight; check historical R3 contract stays intact.
2. **L3**: only after trusted source authorization of exact new G1 SHA, compile original game-referenced net35/CLR2 DLL and check its source SHA and GM marker. The installer also changed; source/package changes must be audited, since DLL build alone does not execute installer PowerShell.
3. **L4 — focus**: fresh disposable save only, install the complete R3 developer artifact and verify: native C1 fixture registered and localized; one GM forced mild patient **created and actually arrives**; a clinician can prescribe ABCL blood collection; the specimen reaches a staffed ABCL toxicology room, is analyzed and returns a result. Then verify one natural vanilla CBC stays on native hematology and does **not** go to ABCL, and reloading the disposable save preserves flow. Failure of any earlier step blocks dependent test results.
4. **C2 not claimed**: the new record is `Disabled` and has no unique laboratory-only hidden main symptom. It is an *engineering assay-routing fixture*, not medical evidence that a new disease cannot be diagnosed without ABCL. Strict C2 must be separately proven, including singleton diagnosis, Doctor Mode/forced-diagnosis behavior. A successful test here cannot count as any of the three approved Alpha clinical cases.
5. **Production**: Alpha/Stable must exclude this fixture, test diagnosis localizations, GM and debug patient spawner. Keep all PRs Draft until the supported evidence is recorded. Do not publish or merge automatically.

## One-session focused L4 prep

The owner should not be asked to reinstall or retry until exact-source G1 test DLL **and** this installer's staging have both passed the real build/package check. No additional plugin. This fixture is **not** a shortcut to claim true C1 isolation or to avoid authentic clinic/queue observation. Tests stop at the first native discrepancy, with game build, active DLC/Workshop set, screenshot and relevant log line.
