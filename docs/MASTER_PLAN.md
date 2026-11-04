# Canonical Development Plan

**Project:** A Better Clinical Laboratory (ABCL)  
**State:** pre-alpha technical integration; Alpha 0.1 not yet released  
**Target:** first playable Alpha within two calendar months *after an explicit kickoff is recorded*. The clock has not started. This is a planning ceiling, not a guarantee.  
**Authority:** this file records the current task state. `docs/DECISIONS.md` records binding decisions; `docs/TEST_EVIDENCE.md` records verified evidence. Do not remove historical decisions or overstate completion.

## Frozen Alpha 0.1 product boundary

- One optional clinical toxicology laboratory integrated into the existing laboratory department.
- Two original, interactable lab devices.
- Three independent sampling/testing pairs and three linked clinical cases.
- English and Simplified Chinese localization.
- Reuse original adult characters, laboratory staff and work queues; no new patient/rendering/clinical AI, standalone stock ledger, or numeric laboratory-result engine.
- Vanilla laboratory basics must remain usable. Unsupported Workshop combinations may be documented (including HAO).
- No proprietary game DLLs/assets in the public repository or release.

## Active task register

| ID | Work item | Status | Completion / blocker |
| --- | --- | --- | --- |
| GOV-002 | Conditional TS-approved low-risk PR auto-merge (ABCL-D014) | Done (protected-main integration) | PR #20 squash-merged as `f412cc1b2c9d2ccf08bd6a29943a254aff3ecc3a`; exact-SHA TS approval + Verify/CodeRabbit/(Python CI when relevant) and safe file allowlist active on main. PR #21 first demonstrated safe refusal while CodeRabbit was pending, then was **successfully auto-merged** after Verify and CodeRabbit passed at the approved SHA `843eb0412ad4af9d72c1fbb2520c65ad4a0a782f` (merge `03b31556f58e692a32fff345a9bfdb5ee43338ec`). The low-risk pipeline is operational; no broader PR class is automatically accepted. All core/ART/CI/decision/release changes remain manual-owner-authorized. |
| GOV-001 | Establish governance, `Verify`, branch protection | Done | Governance PR #5 merged; GitHub Actions Verify passed; active main ruleset #26316259 requires PR and Verify, blocks deletion and force pushes; extra CodeQL gate removed |
| G0-001 | Fourth-room disposable-save CBC preflight | Evidence recorded (user report) | User reported room placement and successful lab processing; no preserved game logs/version or complete save/load evidence; not a production test |
| G1-001 | G1 native blood-lead sampling/testing, R3 diagnostic preflight and isolated test package | **In Progress — current G1 genuine net35/CLR2 L3 PASS; owner combined L4 unresolved** | Historical R3 clinical workflow L4 owner-reported PASS is preserved in `docs/TEST_EVIDENCE.md`, without assuming it applies to newer builds. The 2026-11-04 integrated user report (ZIP SHA256 `e4c2fbc77af26aeee71736062ced7fc4e5198b7e1184c79fe2e3b6b53ad2e7ca`) was **8 PASS / 1 FAIL / 0 BLOCKED / 4 NOT TESTED**; separate GM patient diagnosis/treatment failure and wider patient effects were reported. C1 fixture used four original non-main symptoms (`IsMainSymptom=false`) and its Super-GM called the insurer-registering native factory; Super-GM, C1 and generic `DIA_CLD` R2 override were retired, not concealed. Current [Draft PR #7](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/7) SHA `32fd883c99a62a207cf6b4be0dbfd6bd5b6be809` is genuine Windows net35/CLR2 L3 PASS [Actions #41752846916](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41752846916), artifact `13286912693`, ABCL DLL SHA256 `c02cbb8cbfaa6a32a1887d52378537e5c9a78168f3d2078e31ac0e84f18fbe0a`; Verify, CodeQL and synthetic R3 installer isolation PASS. Refreshed integrated test archive `ABCL_TEST_R3_20261104_RestoreFix.zip` SHA256 `01400d176d180c6ad71da96b398a8ffd170223441a3e2975c6571478d87381c0` includes no GM/C1/G2, and fixes restore receipt mismatch with synthetic Windows rollback tests PASS. **Current candidate's actual game L4 NOT RUN**; staff operation, CBC, save/reload, rollback, DLC/Workshop remain open. No Alpha. |
| G2-001 | Two-machine native heavy-metal toxicology exam content (test-only) | **G2 V1 art FAIL; V2 letters touched pictogram; owner requested V3 separation integrated into TS source; true 32px/64px PNG L2 PASSED on exact-head CI / real G2 L4 not run; V1 ZIP WITHDRAWN; C2 BLOCKED** | [TS Draft PR #43](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/43) source `d92b7a057fba99c4df8520eaaf78d507233698dc`, [Actions #41670728220](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41670728220): Verify + **9/9** native XML regressions and exact pinned-G1 source L2 PASS, CodeQL pending/verified separately. Three native pairs: blood lead → private ICP-MS; whole-blood cadmium → private digestion station → private ICP-MS; urine mercury → private ICP-MS, each retains original stat-lab waste/hygiene and G1 owner-only XML. Two **experimental** mobile exposure-assessment conditions `DIA_ABCL_G2_CADMIUM_EXPOSURE` and `DIA_ABCL_G2_MERCURY_EXPOSURE` have namespaced main symptoms, EN/zh-Hans medical labels and separate original small/big generated clinical icon PNGs; elevated concentrations represent **exposure**, not definitive toxic clinical disease. Historical **WITHDRAWN, DO NOT INSTALL** test-only ZIP SHA256 `d631f8755e65d51613922d3d568e68e3cc43c0218c0c9d291725acceeb895366` (41 files, 35 addon SHA match), includes genuine earlier compiled ABCL G1 DLL (not original game DLL), owner-approved V3 prefab resources, frozen FA ART source. **Owner explicitly rejected all eight medical-icon PNGs before testing: illustration-style organ/flask/device images do not match vanilla 64px white pictogram disease/symptom set. Corrective [Draft PR #44](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/44) adds two original white flat SVG pictograms (Cd ingots and Hg droplet) with 64px+32px transparent PNG generation, 4 private disease+main-symptom assets only, no equipment or examination art in MedicalIcons. Examination entries use original blood/urine atlas indexes 1641/1691; new assessment condition+main symptom fallback uses neutral index 1169 instead of skull 1203. Exact generated four PNG SHA256, native readability bounds, 9 clinical+3 visual regression tests passed [Actions #41675838032](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41675838032). **V2 failed owner fine-detail review (Cd/Hg letters too close to the symbol). User directed implementation of the separated V3 image layout in TS.** [Draft PR #44](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/44) now has revised **editable** Cd/Hg SVG groups, pinned 4 new 64/32px RGBA PNG SHA256 values in both the renderer and G2 clinical XML builder, and an independent alpha-row source-only audit requiring >=8 fully transparent rows in 64px and >=4 in 32px with an intentional connecting-line negative test. Updated owner-review preview at true native size, and no unapproved equipment or exam art in MedicalIcons. V3 is source-integrated; exact-head [Actions #41681804327](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41681804327) Verify/CodeQL/G2 native-icon pixel L2 **PASS**; audited artifact #13251869955, SHA256 `8108f5726b2a38d85464184c49ecb39ff7ec9cea2f802513335f450468a0d48b`. Native 32px Cd separator y16–19 and Hg y15–18 (four fully transparent rows), 64px Cd y32–39 / Hg y30–37 (eight rows), deliberate bridging-line negative check rejects all four. Owner in-game icon validation and clinical C2 still separate gates. **No corrected installable G2 ZIP exists; do not install withdrawn V1.** Visual approval required before any new L4 ZIP. Windows installer not executed; G2 native games/diagnosis/exclusive C2 and DLC/Workshop L4 not proven**, no release or auto-merge. PR #37 strict exclusive diagnosis decision remains blocked; cannot claim Alpha case 2/3 ready. |
| ART-001 | Two original free-standing toxicology machines, four views and work interaction | **In Progress — owner game L4 placement/rendering PASS; staff use NOT TESTED** | Owner 2026-11-04 integrated L4 items 04–07 PASS: mass spectrometer and digestion workstation both appeared, placed, rendered NW/NE/SE/SW, and had acceptable dimensions/perspective/floor contact. Exact FA original art SHA `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`, equipment atlas SHA256 `b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651`; [Draft #14](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/14) and TS standalone [Draft #42](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/42). The new integrated R3 archive keeps all 8 directional frames and two independent one-tile objects byte-identical. Lab specialist pathing/interaction, actual analysis handoff, vanilla CBC and save/reload were NOT TESTED by the latest user report. Historical failed workbench-based L4 remains in the evidence archive; no game L4 or production-ready claim for the untested gates. |
| TO-001 | Vanilla-style toxicology room-list icon and scoped private floor glyph | **In Review — owner approved visual source; current G1 compiled L3; integrated owner UI L4 NOT RUN** | [Issue #24](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/24), original FA [Draft #14](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/14), scoped TS source [Draft #29](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/29), integration [Draft #36](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/36). The owner 2026-11-04 integrated test found **both menu and floor icons absent** despite other lab features passing. Exact approved menu PNG SHA256 `acb0042bb006f1f6a85c5b099f1c311ac5268b19944206cb1003b96a7930cb8a`, original floor projection SHA256 `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4`, isolated 2048² atlas tile 376 SHA256 `00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd`. Assets and exact-room scoped renderer now reside in the genuine L3 G1 build and integrated R3 ZIP, not the original game atlas; renderer ownership is private. Combined in-game menu/floor display, vanilla zone colors and Workshop coexistence **NOT TESTED**. Approved source and green CI do not close the issue. |
| TO-002 | Toxicology Laboratory in native relationship / Dependency tree | **TS bounded original-source/ABI gate complete; actual graph node/edge BLOCKED pending one future L4 anchor** | [#25](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/25), [Draft #32](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/32), `docs/TO002_NATIVE_GRAPH_GO_NO_GO.md`. Original `dep_tree` 1400×620 RGBA32 has fixed boxes/3 original lab arrows; localized icons/text are independent UI. No add-on room registry for graph. Latest read-only exact `Image.sprite` **or** `RawImage.texture` anchor probe, only unique/active objects, Canvas-relative coordinates for existing labels, SHA `2455d8b09f5d9b2937d8f98c042a8096a0d4d48f`: [Verify + true Windows net35/CLR2 L3 **PASS** #41632567170](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41632567170), CodeQL PASS. **No additional Toxicology node or clinical arrow has been implemented**. Do not infer coordinates/edges or modify original `dep_tree`; collect one log in the next owner-approved joint L4, then GO on exact anchor + medical route or explicit scoped NO-GO. No separate game test or user reinstall. |
| TO-003 | Professional, concise bilingual names and descriptions for new labs, tests and devices | **In Progress / source-only L2** | [Issue #26](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/26). Existing G1 blood-lead and room strings are professionally phrased. [Draft PR #27](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/27) adds bilingual localization/placeholder contract tests, exact SHA `a3ec58ba72a93f6472d7e75b204cf029ed7b909c` Verify/CodeQL PASS. FA ART-001 device terminology still requires feature-accurate medical review, and bilingual UI L4/owner approval is open. Do not claim methods not implemented by G1. |
| TO-004 | Two original 8×6 / 12×6 Toxicology Laboratory prefab designs | **DONE for original V3 6/6 standalone owner L4; integrated label correction awaits owner L4** | [Issue #30](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/30) closed after owner-reported V3 6/6 standalone L4. The later 2026-11-04 integrated L4 passed placement/rotation/access but **FAILED menu item 08**: the localized names embedded sizes which original `MapEditorUIController.CreatePrefabButton` appended a second time. Exact V3 geometry and previews stayed unchanged at historical source SHA `a7d399d429b64ad0f41d16c002a18889ae7b00e8`. Corrected EN/zh-Hans labels are dimension-free in [Draft #31](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/31), source SHA `9130c7a3241315d1b73e8bcfdf4cc2f560cd9804`, and current-base TS [Draft #47](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/47) has source, CodeQL and Windows mock prefab overlay PASS. **Corrected integrated game L4 NOT RUN**. Historical failure and owner PASS remain separate; no release or universal compatibility. |
| ALPHA-001 | Integrated Alpha 0.1 case content and gameplay acceptance | Backlog | Depends on G1 + art; test original labs, save/load and claimed DLC support |

A G0 result is not G1 completion. A pass on XML, source scaffolding, mock tests or the CI `Verify` job is not proof of gameplay.

**Visual-L4 hold — 2026-11-03:** The joint ABCL TO+FA test-only package in Draft [PR #34](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/34) compiled successfully (Windows net35/CLR2, 0 errors/0 warnings, Actions [#41595009929](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41595009929)), but the owner rejected five visual surfaces and confirmed the relationship graph node was unimplemented. **DO NOT RETEST THIS PACKAGE OR PROMOTE TO ALPHA.** The joint source was later corrected to remove an accidentally packaged 0-byte `0Harmony.dll` compatibility placeholder. This source-only corrective change has Verify/CodeQL PASS, but cannot retroactively fix the owner's installed ZIP or replace visual L4 acceptance. Keep all original historical R3 clinical results and preserve adult/DLC/Workshop compatibility.

## PR / Issue / branch lifecycle checkpoint (2026-11-04; review pending)

The [repository lifecycle audit](PR_ISSUE_BRANCH_REGISTER_20261104.md)
records the initial **37 branches / 23 open PRs / 6 open Issues** and the
current **38 branches / 17 open PRs / 6 open Issues**. Seven stale, withdrawn
or superseded PRs (#34, #35, #38, #39, #41, #45, #46) were closed **without
merging**; all original branches, commits and failure evidence remain.

**Current implementation and evidence:**
- G1 #7: exact source `0283e789bbf125b709490bda4c1164c30883fdcd` has Verify,
  CodeQL and synthetic R3 installer smoke PASS. Genuine Windows net35/CLR2
  build PASS: Actions #41754602137, artifact 13287840694, DLL SHA256
  `c5e8ddeee5dcad5adedfbbf9b42e04af02716f87d1485c3c4a2c976f2a38f373`.
- The previous owner L4 result found the C1/Super-GM patient route unusable
  and reported broad patient-state impact. Source audit found the C1 fixture
  used four original symptoms, all `IsMainSymptom=false`; the native factory
  also registers created patients with insurers. Super-GM, C1 and the R2
  generic `DIA_CLD` override have been removed. Only the original TRM_LDP
  R3 native test path remains.
- TO-001 approved active room sprite, TS-derived neutral-gray inactive sprite,
  and private floor tile 376 atlas are registered with exact-room adapters in G1.
  The native custom-icon path ignores its inactive sprite index, so the disabled
  glyph is a distinct transparent derivative; no background/zone color is baked.
  New combined game L4 is still pending.
- ART-001 devices passed owner L4 appearance, placement, four views, scale,
  perspective and ground contact; staff operation/assay workflow is pending.
- TO-004 bilingual prefab labels are dimension-free at source head
  `9130c7a3241315d1b73e8bcfdf4cc2f560cd9804`; vanilla UI appends dimensions.
  Current-base overlay successor is Draft PR #47. Combined game L4 after the
  label correction remains pending.
- G2 clinical/icon source remains PR #43/#44 only. G2 C2 exclusivity and
  genuine playable DLL/L4 are not proven; no G2 payload is in the current
  integrated package. The old GM dispatcher PR #45 and privileged workflow
  PR #46 are retired.
- TO-004 V3 separate 6/6 L4 remains recorded under closed Issue #30.
  TO-002 graph is not implemented; complete TO-003 UI L4 remains pending.
- Current ChatGPT test-only ZIP:
  `ABCL_TEST_R3_20261104.zip`, SHA256
  `38f132fe6f814607c2a8f698030282645fe309f644fd0499e3ded71b161d65b9`.
  It contains 45 files / 26 addon files. G1 L3 is proven, but refreshed
  combined game L4, staff operation, CBC, save/reload and rollback remain
  NOT TESTED. It is not Alpha.

**Lifecycle rule:** update an existing Issue/PR before creating another;
close superseded/withdrawn Drafts with rationale and preserved evidence;
keep unmerged original source branches as long as they contain unique work;
delete merged branch refs only after verifying no active dependent PR.
None of the historical branches were deleted by this checkpoint. Follow
frozen D014 manual-owner approval for privileged CI, core, medical, art,
plan, release and compatibility changes. This checkpoint is a Draft plan
update and has not changed main.

## Stage gates and stop rules

1. **G1 core clinical gate:** an ABCL-namespaced sampling/testing pair is offered to an eligible patient, dispatched to the new laboratory, processed by a staffed interactable instrument, exposes a diagnostic result and permits treatment. Existing CBC must still work. If no reliable native path exists after one scoped, evidence-backed correction, stop this implementation.
2. **Art gate:** original 4-direction equipment displays correctly and a lab specialist can actually operate it.
3. **Regression gate:** base game, baseline laboratories, saves/loads, and every DLC configuration explicitly declared supported are exercised. Unsupported mods and save migration modes are documented.
4. **Release gate:** an actual packaged Alpha was installed and tested. No automatic release based on green CI.

**Workstream coordination:** TS owns G1/core integration and governance; FA owns ART-001 art/previews. See [TS / FA workflow](TEAM_WORKFLOW.md). D011/D012 are binding art decisions, and the R2 G1 test-only re-scope is D013. A source-only art review can proceed while the separate read-only diagnostic-panel L3 is pending; none of these statuses authorize Alpha or a production debug spawner.

## Dependency order

GOV-001 → G1-001 → ART-001 → ALPHA-001. **User-approved TO-001/TO-002/TO-003 are additional UI/medical-copy gates, not substitutes for G1 clinical/art validation.** TO-001 must pass real native UI + floor-icon owner L4; TO-003 requires bilingual medical terminology + UI acceptance. TO-002 must prove a collision-safe original graph route or be explicitly re-scoped as a documented NO-GO before Alpha scope is frozen. Research results do not silently unlock a dependent task. Maintain one active engineering bottleneck, not many parallel Issues waiting for each other.

## Update rules

Update status only when a dated evidence record supports the change; preserve why an item became Blocked, Done, or Cancelled. Any new feature must cite a recorded decision and account for the frozen Alpha scope.
