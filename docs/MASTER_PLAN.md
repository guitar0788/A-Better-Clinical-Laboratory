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
| G1-001 | Independent blood-lead sampling/testing + test-only patient fixture | In Progress (R2 lab fixture owner-reported L4 PASS; R3 genuine L3 PASS, L4 pending) | R2 owner-reported 14/14 one-session L4 PASS on exact source `7f3c5f29cebd39338df854a1475ceb604dca164f`, Actions `41377881918`, artifact `13112246582`: mobile Emergency `DIA_CLD` fixture, ABCL sample/collection/lab/result, vanilla CBC and save/reload passed. Do not repeat R2. R3 native `TRM_LDP` addon-local exam overlay + guarded IMOBILE factory passed genuine Windows/net35/CLR2 L3 on exact source `ba68b17723587c07baf791127bd751dcdde05546`, Actions `41391190322`, artifact `13116939196` (0 warnings/errors). Independent archive audit: BUILD_INFO candidate SHA and DLL hash match; no original game DLL/AES key; but the inner ZIP omitted `INSTALL_G1_R3.cmd` and included only the generic R2 launcher. Root cause: run dispatched on `main` used the old workflow revision from main, not the candidate branch's corrected workflow. Artifact `13116939196` is NOT FOR INSTALLATION. Feature-branch workflow is being corrected to require/include the R3 launcher and exclude the R2 launcher; pre-merge build must dispatch from `feature/g1-secure-build`. R3 actual ambulance arrival, TRM_LDP sample/result, high-priority hospitalization, chelation, CBC regression and save/load are NOT YET L4-tested. DLC/Workshop compatibility and Alpha/release remain unproven. Keep Issue #2 open and PR #7 Draft. |
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
