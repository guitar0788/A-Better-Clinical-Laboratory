# ABCL Independent Toxicology — Medical Content and Native Integration Gate V1

**Status:** Design contract / bounded source review, **NOT** a passing runtime gate.
**Owner directive:** 2026-11-03. **Governs:** existing ALPHA-001 #4 and G1-001 #2.
**Decision:** ABCL-D015. **Historical work:** G1 R2/R3 evidence is preserved, not reinterpreted.

## Product contract

1. The Toxicology Laboratory is a **new test service**, not an alternate processing room for vanilla laboratory examinations. In an installation with ABCL, original hematology, microbiology and histology examinations and their room allocation must remain unchanged.
2. All ABCL testing pairs have private namespaced IDs, dedicated toxicology routing, professionally accurate EN/zh-Hans labels (TO-003 #26) and documented clinical value. New ABCL cases must require original ABCL-specific lab evidence for ordinary confirmation, with the feasibility of an **absolute, non-bypassable diagnosis lock** explicitly tested, not assumed.
3. Any genuinely new disease must have a private disease ID and clinical content; do **not** take over vanilla TRM_LDP or make any vanilla diagnosis require ABCL. The already accepted lead-poisoning R3 fixture is a **technical harness**, not the proof of a new exclusive-diagnosis condition.
4. Preserve native adult patients, medical staff, lab work queues, saves and treatments whenever feasible. Do not introduce a custom numeric lab result engine or a new clinical AI. No proprietary Unity game DLLs / original textures in GitHub.
5. Alpha 0.1 minimum stays at **three independent sampling/testing pairs, three linked clinical cases, two original devices**, one laboratory and EN/zh-Hans; additional assays are a later content backlog, not automatic Alpha scope expansion.
6. No claim of all-DLC/Workshop compatibility, safe removal from mod-affected saves, or vanilla isolation until L4 evidence exists.

## Source-backed native findings (2026-11-03)

Local game reference archive supplied by owner: `dll_ilspy.zip` and `StreamingAssets.zip`, consulted read-only. References below are **method/record evidence, not shipped source code**.

| Evidence | Interpretation | Status |
| --- | --- | --- |
| `Lopital.BehaviorPatient.FindLabSpecialist(GameDBExamination,bool,GameDBEmployeeRole)` and `Lopital.ProcedureComponent.UpdateAllExaminationsForMedicalCondition` | Lab processing and availability consult `Procedure.RequiredRoomTags`, including fallback department. A private lab tag is a viable **candidate** for selecting ABCL work | Source path identified; real negative L4 missing |
| Vanilla `StreamingAssets/Database/Procedures/Examinations.xml`: `EXM_CBC_TESTING` requires `deprecated_lab` / `hematology_lab`; other vanilla procedures reference `microbiology_lab` or `histology_lab` | These original tags are *not* declared on ABCL's G1 toxicology room type. No justification to route vanilla tests to ABCL | Static separation indicated, not guaranteed across all procedures/DLC/mods |
| `Lopital.LabProcedure.FindRoom` | When assigning a lab specialist's home room, the method checks the common `stat_lab` tag. **Do not blindly delete `stat_lab`** to enforce exclusivity: this can break the successful G1 route | Risk demonstrated in original source |
| Current G1 `ModExaminations.xml` | `EXM_ABCL_G1_BLOOD_LEAD_TESTING` requires `abcl_g1_toxicology_lab`, but equipment includes native `hematoanalyzer` / `stat_lab_exam` | Distinct exam ID + room tag, but **not** an original standalone analyzer interaction |
| `Lopital.BehaviorPatient.UncoverSymptomsFromLabExamination` | Finishing a named lab examination uncovers symptoms whose `GameDBSymptom.Examinations` include that exact examination | Candidate medical-content path for ABCL-specific confirmatory findings |
| `Lopital.MedicalCondition.IsClear`, `Diagnose`, `ForceDiagnosis` | A discovered main symptom **or a single possible diagnosis** can permit ordinary native diagnosis; diagnosis approaches and forced/player diagnosis paths may bypass an ABCL assay | **ABSOLUTE ABCL-only confirmation NOT PROVEN**. XML-only proposals must not claim it. |
| `GameDBMedicalCondition.Examinations` and `GameDBSymptom.Examinations` | Native disease/symptom references can express available exams and symptom revealers | Additive record definitions can be tested without modifying vanilla diseases |

**Noninterference rule:** common `stat_lab` / native equipment tags are implementation infrastructure, **not permission to reassign vanilla examinations**. Isolation is determined by exact available exams, required room tags, staff selection and actual processing outcomes; verify each separately.

### C0 offline tag-matrix checkpoint — limited PASS (owner-supplied archived game files)

Read-only parser scan of game data archive SHA256 `e083496f22939712e8af1768836694e59674f50bc5ebecefc02b254b227da4ba`:
- Five relevant examination XML sources were examined: base `Examinations.xml`, `ExaminationsReception.xml`, DLC Hospital Services, DLC Infectious Diseases and DLC Traumatology. DLC Doctor Mode has no standalone examination definition in this supplied snapshot.
- **16 native sampling-to-lab links** point to **14 distinct existing lab testing examination IDs**, all resolvable. Those testing records specify original `hematology_lab`, `microbiology_lab`, `histology_lab` and/or `deprecated_lab` routing tags; none specifies any of the current ABCL room tags `abcl_g1_toxicology_lab`, `stat_lab`, `lab_specialist_workspace`.
- **Observed intersections: 0/14 native linked testing examination IDs**, a *static tag compatibility result*, **not** an observed patient/routing L4 pass, a proof against third-party Workshop additions, or a full DLC interaction guarantee.
- The frozen G1 ABCL testing record's required room tag remains `abcl_g1_toxicology_lab`; the relevant original room tags do not include it. Generic original equipment reuse remains an independent gameplay/art-content concern.
- Audit cannot guarantee that custom code, runtime overrides, other Mod records or nonstandard AI pathways will never dispatch original tests into the new room. C1 negative in-game check remains **BLOCKING**.

## Implementation order — stop/go before adding breadth

### C0 — Freeze accepted evidence; read-only audit (initial source review done, L2 work remains)
- Preserve G1 R3 owner-reported patient/lab/CBC/save L4 and TO-004 V3 prefab approval; no rewriting passed artifacts.
- Record the vanilla test ID -> required tags matrix across the base game and all four supported DLC candidates, and compare with `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB.Tags`. Do not publicly upload game XML.
- Flag unexpected overlap and fallback routes. If overlap is discovered, isolate only with a source-supported, additive adjustment; do not alter vanilla tests.

### C1 — Negative and positive lab routing (blocking)
- Build an additive, exact-SHA fixture containing one ABCL-only exam; keep G1 approved patient harness separate.
- **Negative:** CBC, hematology, microbiology, histology and chosen DLC lab examinations must not execute inside the ABCL toxicology room.
- **Positive:** ABCL assay is offered, physically dispatched and completed in the ABCL room; cannot be executed in each corresponding vanilla lab alone.
- Verify staffing, queue, laboratory fee, result-to-doctor, save/reload and mod disabling behavior only where supported. Collect game build and DLC/Workshop set.
- If the opposite routing happens, stop, preserve matching evidence and make at most one local source-backed correction per D009.

### C2 — ABCL-only diagnosis feasibility (blocking before new-disease implementation)
- Prototype **one** new private medical condition + its private symptom and associated test IDs; do not use old TRM_LDP as the new disease.
- Demonstrate patient state before test; finish all available vanilla lab procedures, use ordinary clinical exam flow and clinician AI, and verify whether the new diagnosis remains unconfirmed.
- Finish ABCL assay and verify discovery of the specific differentiating finding plus normal diagnosis/treatment.
- **Explicitly test exceptions:** singleton possible diagnosis, main symptom alternative uncovering, player-forced/Doctor Mode diagnosis and test-unavailable paths.
- If a *strict* 'only ABCL can ever diagnose this disease' claim cannot be met without unsafe global patches, **NO-GO for the strict lock**, document the precise achievable 'ABCL-only definitive laboratory confirmation' semantics and seek owner's decision; do not fake a hard constraint. Any narrowly scoped patch must demonstrate vanilla patient noninterference, four-DLC compatibility and save safety before approval.

### C3 — Clinical content breadth (after C1 + C2 GO)
- Minimum 3 medically distinct ABCL-owned sample/assay pairs and 3 linked **new** cases; ensure each has justified sample matrix, test interpretation as representable by native symptom/reveal mechanics, treatment and progression.
- Candidate **research only** (not yet selected or proved absent in vanilla/DLC): mercury exposure, arsenic exposure, acetaminophen overdose. Compare all against original/DLC medical IDs and current available symptom/test repertoire; reject duplicates and unsupported diagnoses.
- Provide clinician-reviewable source-to-XML traceability; EN/zh-Hans natural descriptions similar in length to vanilla. Never call an assay merely 'X test' as placeholder.
- Longer-term library expansions beyond Alpha are backlog, prioritized by actual native route and distinguishable clinical value, not target counts alone.

### C4 — Native devices, integrated L3 and L4
- Only use FA devices after separate visual/4-direction/tabletop/clinical interaction gates pass; don't silently inject them into approved TO-004 prefab XMLs.
- Genuine .NET Framework 3.5/CLR2 game-reference compilation where C# is involved; static Verify is L1/L2 only.
- Exact-SHA disposable-save L4: three new cases diagnosed/treatable only via their designated ABCL lab evidence in the promised mode, original lab/CBC unaffected, correct staff workflow and save/reload, and every claimed DLC/Workshop configuration.
- Disable diagnostic patient-spawn panel in Alpha; keep PRs draft until acceptance. No automatic merge or release.

## Acceptance ledger

| Gate | Current state | Completion evidence |
| --- | --- | --- |
| Native tag separation | Source-supported candidate | Full base+four-DLC tag matrix, game negative L4 |
| Noninterference with original labs | Prior CBC regression exists for G1 R3 | New negative vanilla-to-ABCL test |
| Unique new ABCL testing | G1 blood lead technical pair owner-reported R3 L4 pass | Confirm exclusive room/approved equipment and new content |
| New disease requiring ABCL to confirm | NOT PROVEN | One-case C2 test including alternate native diagnosis paths |
| Three new cases / three pairs | Backlog | C3 content acceptance, integrated L4 |
| Original devices | FA needs owner art/interaction approval | ART-001 gate |
| Release-ready Alpha | NOT READY | C4 full L4 + explicitly approved merge/release |

## Governance & scope protection

- **Owner-approved product requirement** is recorded in ABCL-D015; this document provides evidence-backed implementation criteria, *not* final approval of a diagnosis patch.
- Existing Issues: G1 #2, ALPHA #4, ART #3, TO-003 #26 and TO-004 #30. Do not create duplicate feature Issues for these phases.
- This proposal changes **documentation only**, not medical XML, user-created prefabs, art resources, branch protection or Actions secrets.
- Main plan and this gate contract become authoritative **only after the draft planning PR passes review and merges under protected main**. Historical decisions and failure evidence remain intact.
