> **VISUAL GATE HARD STOP — 2026-11-04 (owner rejection before game L4).** The eight G2 `MedicalIcons` PNGs in the earlier test-only ZIP do **not** match original Project Hospital diagnosis/symptom icon style. They were drawn as glossy shaded kidney/flask/test-tube/device illustrations; the actual original `StreamingAssets/Textures/ui/icons.png` uses 2048×6144 native 64px cells, with largely flat white pictograms for diseases. Original `TRM_LDP`/`TRM_CMP`/`TRM_MTP` use icon 1203 (skull and crossed bones), not a glossy laboratory illustration. The generated cadmium/mercury icons are visually rejected; the metals_exam/digestion files are not disease icons at all. **The prior `ABCL_G2_Clinical_Toxicology_Full_TestOnly.zip` is WITHDRAWN from L4 use. Do not install, repackage, mark visual PASS, or test G2 disease UI using these images.** Source L2/Verify remains historical technical evidence only. See [PR #43 owner visual rejection](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/43#issuecomment-6609347652). Correct original-style separate disease/examination/equipment icon families, native 64px/32px readability, original game's custom icon UI and fallback icon behaviour, then obtain explicit owner approval before any replacement package. **No G2 game L4 and no new-disease C2 acceptance has occurred.**

> **G2 RANDOM-POOL ISOLATION / GM DEPENDENCY — 2026-11-04.** The two new exposure assessment records now explicitly contain `Disabled=true` to keep experimental G2 cases out of ordinary patient generation until diagnosis C2 and game L4 are proven. The existing G1 test-only GM panel rejects all disabled cases other than C1: the exact two-case, sampling/main-symptom-validated exception is implemented separately in [TS Draft PR #45](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/45), based on G1 Draft #7. **Do not install or treat this as a working GM test until that matching C# variant has genuinely compiled and the integrated package is audited.** Original R3 lead, C1, CBC and three native labs are separate unaffected paths. The historical visual rejection and withdrawn ZIP warning above still apply.\n\n# G2 clinical toxicology — two instrument pathways, three native assays (test-only)

**Date:** 2026-11-03. **Status:** pre-Alpha medical engineering candidate; no user game L4 and no exclusive diagnosis guarantee.

## Authority and unchanged baselines

- `docs/MASTER_PLAN.md`: one additive toxicology lab, two original devices, three sampling/testing pairs, three clinical case pathways, EN/ZH. User explicitly requested the design and development of both instruments' assays and optional new illnesses with real icons.
- `docs/DECISIONS.md` D003/D004/D005/D006/D011/D012/D014 and draft clinical independence D015 in [Draft PR #37](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/37). D015's **strict exclusive diagnosis** requirement is still a blocker: vanilla `MedicalCondition.IsClear/ForceDiagnosis` can bypass a new blood/urine assay. This **test-only** proposal cannot be marked Alpha-eligible until that clinical requirement is proven or the owner explicitly re-scopes it.
- G1 R3 lead and original CBC, original 3 labs and all four DLC resources remain unmodified on disk. The owner-reported lead core L4 and TO-004 V3 prefab L4 6/6 PASS remain separate historical evidence. Pre-approved TO-004 room PNG/XML SHA `a7d399d429b64ad0f41d16c002a18889ae7b00e8` is frozen.
- FA native device artwork is frozen at source `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`, but **visual art/real personnel operation L4 is still open**. TS integration Draft #42 does not make the devices medically functional.

## Three separately linked native sampling/testing pairs

| Clinical association | Sampling ID | Testing ID | Lab steps in order |
| --- | --- | --- | --- |
| Original `TRM_LDP` lead exposure | `EXM_ABCL_G1_BLOOD_LEAD_SAMPLING` | `EXM_ABCL_G1_BLOOD_LEAD_TESTING` | native `stat_lab_exam` → **private ICP-MS** `abcl_art001_icp_ms` → native waste / hand hygiene |
| New **cadmium exposure assessment** `DIA_ABCL_G2_CADMIUM_EXPOSURE` | `EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING` | `EXM_ABCL_G2_BLOOD_CADMIUM_TESTING` | native `stat_lab_exam` → **private sample digestion station** `abcl_art001_digestion` → **private ICP-MS** → native waste / hand hygiene |
| New **inorganic mercury exposure assessment** `DIA_ABCL_G2_MERCURY_EXPOSURE` | `EXM_ABCL_G2_URINE_MERCURY_SAMPLING` | `EXM_ABCL_G2_URINE_MERCURY_TESTING` | native `stat_lab_exam` → **private ICP-MS** → native waste / hand hygiene |

The cadmium path uses a documented **microwave acid digestion–ICP-MS method for whole-blood multi-element analysis**, but simpler dilution also exists. Digestion must **not** be forced onto lead and urine-mercury testing merely to make the model animate. Cadmium in blood indicates **recent exposure**; urinary mercury is predominantly useful for **elemental/inorganic exposure assessment**. No numeric-result engine, automatic poisoning severity threshold, biomarker speciation or altered clinical treatment is claimed. A test-only in-game high concentration alone does not constitute a definitive medical diagnosis.

**References (medical design only):** CLSI C40 (whole-blood lead ICP-MS, 2024), PubMed 39417861 (validated microwave digestion + ICP-MS), CDC/ATSDR cadmium testing, ATSDR mercury clinical guidance, CDC NHANES urine mercury ICP-MS methodology. The actual game uses simplified equipment-time steps.

## New medical records, names and icons

Two **new G2 assessment conditions** (`DIA_ABCL_G2_CADMIUM_EXPOSURE`, `DIA_ABCL_G2_MERCURY_EXPOSURE`), not unqualified `poisoning` claims, have separate private `IsMainSymptom=true` lab-discovered biomarkers; the disease and main symptom share **their own original big/small custom icon** refs. The generated originals are 64×64/32×32 transparent RGBA assets in `Assets/ABCL/MedicalIcons/` with private `TEXTURE_CUSTOM_SPRITE` declarations. UI includes original vanilla `IconIndex=1203` fallback where certain older panels do not use custom sprites, consistent with the game author's medical-icon guidance.

- English: **Cadmium exposure / Elevated blood cadmium / Blood cadmium level / Blood cadmium sample**.
- 简体中文：**镉暴露评估 / 血镉升高 / 血镉测定 / 血镉采样**。
- English: **Mercury exposure / Elevated urine mercury / Urine mercury level / Urine mercury sample**.
- 简体中文：**汞暴露评估 / 尿汞升高 / 尿汞测定 / 尿汞采样**。

The native game work queue remains owned by `DPT_LAB`, restricted by `RequiredRoomTags=abcl_g1_toxicology_lab`. The pre-existing G1 room still requires original `ui_hematoanalyzer`, `ui_ria` and `thermal_cycler` for the prior L4-ready build; the two new private equipment tags are **recommended** (MinCount=0) so that TO-004 V3 presets and CBC are not silently rendered inoperable. To perform the **new assays**, the private machines must actually exist in the room, even though the room can still be marked operational without them. This is an intentional progression gate, not an undetected missing prerequisite.

## Explicit risks and stop conditions

1. New conditions use a **test-only** low-severity mobile patient route, because the existing development-only G1 GM panel permits controlled spawning of MOBILE medical conditions by exact ID. It does not guarantee arrival or diagnosis, and must **not** ship in Alpha.
2. Game-native registration of the new urine sampling procedure, private atlas icons, room equipment and symptom links must pass actual L4. L2 ID checks alone cannot establish patient AI offering them, procedure dispatch, staff animation, results or native UI icon scaling.
3. **Diagnosis C2 HARD GATE:** manual/forced diagnoses may be applied without test evidence. This has no verified technical fix. In the test report, separately record whether a new case can be diagnosed before the ABCL assay; if so, stop claiming exclusive-confirmation diagnosis and keep G2 diseases out of the Alpha release pending owner re-scope.
4. Never replace original base game `Diagnoses`, `Symptoms`, `Examinations`, CBC objects or original atlas; test-only overrides of *owned G1 addon* `ModExaminations.xml` and `ModRoomTypes.xml` need original SHA verification, backup and rollback. Existing TO-004 PNG/XML and attached ART alternatives are immutable.
5. In-place removal of diagnoses/equipment after saving active patients or their hospital placements is **not save-safe**; all tests run in a disposable save that must not be reopened after uninstall.
6. No universal four-DLC/Workshop support claim without an enumerated matrix and one actual game L4.

## Single focused L4 test plan

Verify addon loads and names/icons; two independent machines placed in a G2 toxicology room, 4 orientations, operator access and actual use; three blood/urine tests available/processed in prescribed device order; each new case's special biomarker discovered, while no premature exclusive-diagnosis claim; vanilla CBC + three labs; TO-004 prefabs and one save/quit/reload; report first failure with screenshot/log, not repeated R3 patient-spawn exercises. **Only user game L4 can promote the runtime result.**
