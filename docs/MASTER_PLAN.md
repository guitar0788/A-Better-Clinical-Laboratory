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
| GOV-001 | Establish governance, `Verify`, branch protection | Done | Governance PR #5 merged; GitHub Actions Verify passed; active main ruleset #26316259 requires PR and Verify, blocks deletion and force pushes; extra CodeQL gate removed |
| G0-001 | Fourth-room disposable-save CBC preflight | Evidence recorded (user report) | User reported room placement and successful lab processing; no preserved game logs/version or complete save/load evidence; not a production test |
| G1-001 | Independent blood-lead sampling/testing + test-only patient fixture | In Progress (R2 lab fixture owner-reported L4 PASS; historical R3 L3/package PASS; updated R3 diagnostic source Verify 29/29 + CodeQL + Analyze Python PASS; exact-SHA L3 pending; L4 pending live quota) | R2 owner-reported 14/14 L4 PASS on `7f3c5f29cebd39338df854a1475ceb604dca164f`, Actions `41377881918`, artifact `13112246582`; do not repeat. Historical R3 source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, Actions `41391983195`, artifact `13117942292`: genuine net35/CLR2 L3 and package audit PASS. Owner screenshot: native TRM_LDP/ABCL, Internal Medicine clinic/ward, IMOBILE pool, hospital gate and free ambulance all OK; quota ZERO, request disabled, no click/no patient created. Original XML/source identifies Liver TY (`IN_COM_CCC`, Chinese `肝泰保险`) objective #4: working DPT_ICU hospitalization -> UNLOCK_AMBULANCES; objective #5: at least one ambulance -> SET_IMMOBILE_PATIENT_COUNT=2. Updated panel reports Liver TY contract, ICU readiness, objective #4/#5 progress, ambulance unlock/count, configured vs live quota, and selected eligible insurer; it ignores the deprecated base stub, does not mutate game state, and preserves eligibility for any contracted insurer with positive live quota. Exact updated candidate `66c95d61a63619e3377b59feac9b5241d3ffb924` passed Verify 29/29 (Actions `41402697471`), CodeQL and Analyze Python (`41402697480`). Genuine L3 for this exact SHA is pending; historical artifact `13117942292` does not include the new diagnostics. No L4 patient attempt; require positive live IMOBILE quota and free parked ambulance. Keep Issue #2 open and PR #7 Draft. |
| ART-001 | Original toxicology analyzer assets and interaction validation | Backlog | Begins only after G1 independent-test L4 works |
| ALPHA-001 | Integrated Alpha 0.1 case content and gameplay acceptance | Backlog | Depends on G1 + art; test original labs, save/load and claimed DLC support |

A G0 result is not G1 completion. A pass on XML, source scaffolding, mock tests or the CI `Verify` job is not proof of gameplay.

## Stage gates and stop rules

1. **G1 core clinical gate:** an ABCL-namespaced sampling/testing pair is offered to an eligible patient, dispatched to the new laboratory, processed by a staffed interactable instrument, exposes a diagnostic result and permits treatment. Existing CBC must still work. If no reliable native path exists after one scoped, evidence-backed correction, stop this implementation.
2. **Art gate:** original 4-direction equipment displays correctly and a lab specialist can actually operate it.
3. **Regression gate:** base game, baseline laboratories, saves/loads, and every DLC configuration explicitly declared supported are exercised. Unsupported mods and save migration modes are documented.
4. **Release gate:** an actual packaged Alpha was installed and tested. No automatic release based on green CI.

## Dependency order

GOV-001 → G1-001 → ART-001 → ALPHA-001. Research results do not silently unlock a dependent task. Maintain one active engineering bottleneck, not many parallel Issues waiting for each other.

## Update rules

Update status only when a dated evidence record supports the change; preserve why an item became Blocked, Done, or Cancelled. Any new feature must cite a recorded decision and account for the frozen Alpha scope.
