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
| G1-001 | Independent blood-lead sampling/testing and isolated test-only patient fixture | In Progress (R3 core L4 owner-reported PASS; diagnostic-panel L3 pending) | Genuine Windows net35/CLR2 R3 build: [41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), exact source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, test artifact `13117942292`. Owner reported native TRM_LDP arrival/IM inpatient admission, ABCL sampling/analysis/result, chelation, original CBC and save/reload PASS in a disposable save. Game build, official DLC list and raw logs were not supplied; all-DLC/Workshop compatibility is NOT proven. Separate read-only diagnostic-panel SHA `7faf31c6bba34ab58a9e288217d0359956bd2af2` passed static checks but still needs exact-SHA L3/package audit and then a brief panel-only check. Keep Issue #2 / PR #7 open/draft, no release. |
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress (FA; visual and L4 gates open) | Draft PR #14 is in ongoing FA V7–V10 source-only iterations; exact latest work must be read on its active head. Neither preview/CI PASS nor original-white material studies equal owner visual acceptance. Only earlier art L4 is **3 PASS / 2 FAIL / 3 BLOCKED** (placement and rotation failed). Revised workbench, directions, contact, staff behavior and vanilla/DLC coexistence still need a focused actual game test. PR #15 covers separate source-only art checks; FA owns asset creation, TS owns core integration. |
| TO-001 | Dedicated native-sized toxicology room-list and private on-floor/zoning icons | **NEEDS_FIX / owner photographed L4 FAIL** | [Issue #24](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/24). FA Draft PR #14 delivered transparent white menu glyph/native 60px crop source-only checks (owner visual re-acceptance pending). TS Draft PR #28 addresses a separate hover/status-bar icon. TS Draft [PR #29](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/29) has genuine **owner-branch Windows net35/CLR2 L3 PASS** on exact SHA `49475e91cabb2fa361c85e28d2f29ee0b7510c17` ([Actions 41588842602](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41588842602)); **private floor atlas not yet delivered/registered**, so the floor-icon L4 still FAIL/NOT FIXED. Verify/CodeQL or L3 alone cannot close TO-001. Preserve native room zoning colors and vanilla/DLC/Workshop icons. |
| TO-002 | Toxicology Laboratory in original Dependency tree / 关系图 | **In Progress / actual graph integration blocked** | [Issue #25](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/25). Native `DependencyTreePanelController` exposes no proven node-registration path. Separate test-only [Draft PR #32](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/32) logs a bounded read-only hierarchy when graph is opened; genuine Windows net35/CLR2 L3 **PASS** SHA `109e3f06c94b86e223d06c6126d328e874709e22`, [Actions 41589889327](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41589889327). NO new visual node/edges exist; batch diagnostic with next relevant TO-001 L4, then decide verified additive route or scoped NO-GO. |
| TO-003 | Professional, concise bilingual names and descriptions for new labs, tests and devices | **In Progress / source-only L2** | [Issue #26](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/26). Existing G1 blood-lead and room strings are professionally phrased. [Draft PR #27](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/27) adds bilingual localization/placeholder contract tests, exact SHA `a3ec58ba72a93f6472d7e75b204cf029ed7b909c` Verify/CodeQL PASS. FA ART-001 device terminology still requires feature-accurate medical review, and bilingual UI L4/owner approval is open. Do not claim methods not implemented by G1. |
| ALPHA-001 | Integrated Alpha 0.1 case content and gameplay acceptance | Backlog | Depends on G1 + art; test original labs, save/load and claimed DLC support |

A G0 result is not G1 completion. A pass on XML, source scaffolding, mock tests or the CI `Verify` job is not proof of gameplay.

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
