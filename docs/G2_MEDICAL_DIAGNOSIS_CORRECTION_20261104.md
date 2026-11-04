# G2 Medical correction — clinical diagnoses, native test routing and toxicology evidence

**Status:** source-level medical fix / G2 Draft child proposal. No real-game L4, no C2 hard diagnosis lock, no approval of any withdrawn G2 icons or ZIP. Never ship experimental diagnoses in Alpha. **2026-11-04.**

## Why this correction exists

The owner rejected the use of “Cadmium exposure assessment / 镉暴露评估” and “Mercury exposure assessment / 汞暴露评估” as **disease names**. An exposure **assessment** is a clinical activity; elevated blood/urine metal is a **laboratory finding**, not a stand-alone diagnosis. Genuine clinical poisoning requires a compatible syndrome and exposure history in addition to supportive toxicology results.

Read-only vanilla game evidence in the owner-supplied `StreamingAssets.zip`:
- `Database/Diagnoses/DiagnosesINTERN.xml` contains `TRM_LDP` (lead poisoning), `TRM_CMP` (carbon monoxide poisoning) and `TRM_MTP` (methanol poisoning). Their diagnoses and required labs/treatments remain unchanged.
- No original/DLC cadmium- or mercury-specific diagnosis ID was found in the supplied base plus four DLC snapshot; new **namespaced private** G2 records are justified.
- Original `Database/Symptoms.xml` provides all the following adult `MOBILE` symptoms. The combinations below are selected to reflect a particular *form* and *route* of poisoning, not interchangeable heavy-metal symptoms.
- Original `Database/Procedures/Examinations.xml` defines physician `EXM_ABDOMINAL_PALPATION` and `EXM_URINE_SAMPLE_ANALYSIS_SAMPLING`. The latter links to **original** `EXM_URINE_SAMPLE_ANALYSIS_TESTING`, whose route requires `histology_lab` / `deprecated_lab`. This original kidney-support test must remain in the original lab, **never** ABCL.
- Original `Database/Procedures/Treatments.xml` and `TreatmentsHospitalization.xml` contain the native treatments below, including `TRT_CHELATION_THERAPY`. Native existence does not certify medical indication.

## Distinct clinical syndromes and correct mappings

| Private test-only internal ID retained for compatibility | Player-visible DISEASE | ABCL-specific ANALYSIS | Original clinical signs | Proposed original treatments |
| --- | --- | --- | --- | --- |
| `DIA_ABCL_G2_CADMIUM_EXPOSURE` (historical ID retained; **not** a disease label) | **Acute cadmium poisoning / 急性镉中毒** | `EXM_ABCL_G2_BLOOD_CADMIUM_TESTING`: **blood cadmium level / 血镉测定** | `SYM_ABDOMINAL_CRAMPS`, `SYM_NAUSEA`, `SYM_VOMITING`, `SYM_DIARRHEA`, occasionally `SYM_DEHYDRATION`; physician exam `EXM_ABDOMINAL_PALPATION` | `TRT_REHYDRATION`, `TRT_STOMACHICS`, `TRT_HOSPITALIZATION_NORMAL` |
| `DIA_ABCL_G2_MERCURY_EXPOSURE` (historical ID retained; **not** a disease label) | **Chronic elemental mercury poisoning / 慢性元素汞中毒**, with chronic vapor inhalation syndrome | `EXM_ABCL_G2_URINE_MERCURY_TESTING`: **urine mercury level / 尿汞测定** | `SYM_TREMOR`, `SYM_IRRITABILITY`, `SYM_HEADACHE`, `SYM_FATIGUE`, occasionally `SYM_PROTEINURIA`. Existing urinalysis supports renal assessment **in the original histology lab** | `TRT_REST`, `TRT_HOSPITALIZATION_NORMAL`, candidate `TRT_CHELATION_THERAPY` **only if clinically indicated, after specialist assessment** |

**Native admission compatibility:** the original `TRT_HOSPITALIZATION_OBSERVATION` is tied to an Emergency Department observation room (`DetachedDepartmentRef=DPT_EMERGENCY`), while `TRT_HOSPITALIZATION_NORMAL` is the original Internal Medicine normal-ward route. Original internal-medicine diagnoses use the latter, and the native `TRT_CHELATION_THERAPY` itself references `TRT_HOSPITALIZATION_NORMAL`. Both private G2 conditions therefore use the **regular-ward** route; no emergency-only observation bed is required or reassigned.

**Important clinical limits:**
1. **Blood cadmium** reflects **recent exposure** and does not reliably predict body burden, clinical outcome or dictate treatment. A long-term cadmium-induced tubulopathy would instead need **urinary cadmium + renal biomarkers**, neither represented by this one blood test. We therefore chose the *acute ingestion* presentation and **did not** label it chronic cadmium nephropathy.
2. **Urinary mercury** is relevant to *elemental vapor or inorganic* exposure, but is not the correct single biomarker for organic methylmercury poisoning. Chronic elemental vapor toxicity fits tremor/irritability and sometimes renal findings. Urinary mercury concentration alone cannot prove a poisoning syndrome or mandate chelation.
3. **Cadmium:** no native chelation treatment in this case. ATSDR does not recommend chelation for cadmium poisoning; stop exposure and supportive care are primary. `TRT_HOSPITALIZATION_NORMAL` is a test-only ordinary Internal Medicine ward representation, not proof every acute poisoning needs admission.
4. **Mercury:** removing exposure is essential, but the current native game treatment set **does not implement occupational exposure removal or toxicologist-directed conditional chelation**. `TRT_CHELATION_THERAPY` is a *candidate available treatment* in a disposable test record, not an automatic order, proven indication, or completed treatment system. No Alpha until actual native clinical behavior can represent this safely.
5. Game percentages for the existing `GameDBSymptomRules` are **scenario weights**, not epidemiologic prevalence. The private "blood cadmium elevated" and "urinary mercury elevated" main symptom IDs remain assay-discovered and separate from disease names, but **do not** establish a diagnosis lock. The original engine may diagnose a singleton condition before lab work.

## Source/equipment/compatibility constraints

- The generator supports two **exact and explicit** G1 baselines. Old G1 requires original `hematoanalyzer` and UI/RIA room items; it remains a historical test-only adapter. **Current G1 standalone** already uses private `abcl_art001_digestion` and `abcl_art001_icp_ms` and requires both as `MinCount=1`. For this current version, the builder preserves the **entire existing lead analysis step order**, existing room prerequisites and art, and appends only distinct Cd/Hg sampling and testing records.
- In both baselines, **never reassign original CBC, urinalysis or another vanilla lab test to ABCL**. Native physician palpation and urine sampling are permitted in their original clinic/laboratory routes; only the new metal assays use the ABCL toxicology room.
- Maintain existing private G2 IDs for compatibility with Draft GM dispatch contract; do not create a duplicate alias disease or rewrite existing G1 lead ID. Keep G2 `Disabled=true` until C1 routing, real game L4 and C2 review are separately accepted.
- **No visual modification**: no alteration to the approved original equipment sprites, TO-004 room previews, medical SVG/PNG files, icon source SHA or original-game icons. This is medical source only. The earlier G2 ZIP with visually rejected icons remains **WITHDRAWN: DO NOT INSTALL**.
- A successful L2 source generator / CI is **not** a real compiled mod nor evidence the patient AI can order, process, or return results for these cases. Game L4, all-DLC/Workshop, diagnosis exclusivity, and release are pending.

## Clinical citations / verification sources

- CDC/ATSDR, *Cadmium Toxicity: Clinical Assessment — Exposure History and Physical Examination*: acute oral gastrointestinal signs, chronic renal syndrome, routes — https://archive.cdc.gov/www_atsdr_cdc_gov/csem/cadmium/Clinical-Assessment.html
- CDC/ATSDR, *Cadmium Toxicity: Clinical Assessment — Laboratory Tests*: blood recent, urine body burden, renal biomarkers — https://archive.cdc.gov/www_atsdr_cdc_gov/csem/cadmium/Laboratory-Evaluation.html
- CDC/ATSDR, *Cadmium Toxicity: Treatment*: no specific antidote / no standard role of chelation — https://archive.cdc.gov/www_atsdr_cdc_gov/csem/cadmium/Treatment.html
- CDC, *Case Definitions for Chemical Poisoning: Elemental Mercury*: tremor, irritability, renal findings; biomarkers do not directly correlate with toxicity — https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5401a1.htm
- CDC/NIOSH, *Elemental Mercury Emergency Response Card*: any chelation decision needs experienced clinical consultation — https://www.cdc.gov/niosh/ershdb/emergencyresponsecard_29750021.html
- NCBI Bookshelf, *Mercury Toxicity*: urine versus blood interpretation; differential and treatment support — https://www.ncbi.nlm.nih.gov/books/NBK499935/

**Acceptance requested before runtime:** source tests for syndrome IDs, vanilla signs/exams/treatments, baseline G1 preservation, bilingual disease names, no false standalone biomarker diagnosis and unchanged art. Later real-game clinical L4 and C2 strict exclusive-confirmation gate must remain open.
