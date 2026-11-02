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
| GOV-002 | Conditional TS-approved low-risk PR auto-merge (ABCL-D014) | Done (protected-main integration) | PR #20 squash-merged as `f412cc1b2c9d2ccf08bd6a29943a254aff3ecc3a`; exact-SHA TS approval + Verify/CodeRabbit/(Python CI when relevant) and safe file allowlist active on main. Smoke test PR #21 demonstrated fail-closed skip while CodeRabbit pending; the first successful automatic merge must be separately verified. All core/ART/CI/decision/release changes remain manual-owner-authorized. |
| GOV-001 | Establish governance, `Verify`, branch protection | Done | Governance PR #5 merged; GitHub Actions Verify passed; active main ruleset #26316259 requires PR and Verify, blocks deletion and force pushes; extra CodeQL gate removed |
| G0-001 | Fourth-room disposable-save CBC preflight | Evidence recorded (user report) | User reported room placement and successful lab processing; no preserved game logs/version or complete save/load evidence; not a production test |
| G1-001 | Independent blood-lead sampling/testing and isolated test-only patient fixture | In Progress (R3 core L4 owner-reported PASS; diagnostic-panel L3 pending) | Genuine Windows net35/CLR2 R3 build: [41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), exact source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, test artifact `13117942292`. Owner reported native TRM_LDP arrival/IM inpatient admission, ABCL sampling/analysis/result, chelation, original CBC and save/reload PASS in a disposable save. Game build, official DLC list and raw logs were not supplied; all-DLC/Workshop compatibility is NOT proven. Separate read-only diagnostic-panel SHA `7faf31c6bba34ab58a9e288217d0359956bd2af2` passed static checks but still needs exact-SHA L3/package audit and then a brief panel-only check. Keep Issue #2 / PR #7 open/draft, no release. |
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress (FA; visual and L4 gates open) | Draft PR #14 is in ongoing FA V7–V10 source-only iterations; exact latest work must be read on its active head. Neither preview/CI PASS nor original-white material studies equal owner visual acceptance. Only earlier art L4 is **3 PASS / 2 FAIL / 3 BLOCKED** (placement and rotation failed). Revised workbench, directions, contact, staff behavior and vanilla/DLC coexistence still need a focused actual game test. PR #15 covers separate source-only art checks; FA owns asset creation, TS owns core integration. |
| ALPHA-001 | Integrated Alpha 0.1 case content and gameplay acceptance | Backlog | Depends on G1 + art; test original labs, save/load and claimed DLC support |

A G0 result is not G1 completion. A pass on XML, source scaffolding, mock tests or the CI `Verify` job is not proof of gameplay.

## Stage gates and stop rules

1. **G1 core clinical gate:** an ABCL-namespaced sampling/testing pair is offered to an eligible patient, dispatched to the new laboratory, processed by a staffed interactable instrument, exposes a diagnostic result and permits treatment. Existing CBC must still work. If no reliable native path exists after one scoped, evidence-backed correction, stop this implementation.
2. **Art gate:** original 4-direction equipment displays correctly and a lab specialist can actually operate it.
3. **Regression gate:** base game, baseline laboratories, saves/loads, and every DLC configuration explicitly declared supported are exercised. Unsupported mods and save migration modes are documented.
4. **Release gate:** an actual packaged Alpha was installed and tested. No automatic release based on green CI.

**Workstream coordination:** TS owns G1/core integration and governance; FA owns ART-001 art/previews. See [TS / FA workflow](TEAM_WORKFLOW.md). D011/D012 are binding art decisions, and the R2 G1 test-only re-scope is D013. A source-only art review can proceed while the separate read-only diagnostic-panel L3 is pending; none of these statuses authorize Alpha or a production debug spawner.

## Dependency order

GOV-001 → G1-001 → ART-001 → ALPHA-001. Research results do not silently unlock a dependent task. Maintain one active engineering bottleneck, not many parallel Issues waiting for each other.

## Update rules

Update status only when a dated evidence record supports the change; preserve why an item became Blocked, Done, or Cancelled. Any new feature must cite a recorded decision and account for the frozen Alpha scope.
