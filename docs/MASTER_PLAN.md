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
| G1-001 | Independent blood-lead sample/test and isolated patient-spawn test panel | In Progress (L3/L4 blocked) | G1 XML/source candidate exists from prior chat; original-game DLL compilation and L4 blood-lead examination not verified |
| TO-001 / FA-1 room menu | Toxicology laboratory room-list icon | **VISUAL APPROVED (owner, 2026-11-03); TS L4 PENDING** | Freeze existing original 64x64 transparent foreground and inactive companion; SVG blob `c4a81670a2b0004799513c5b03a61b9239af1f5b`, PNG blob `149bc34ebe68194d13054d91564c28700b5311ab`. These exact resources were already committed on this branch; do not redraw or alter hashes. Owner approval is visual only; TS must still validate LAB backgrounds, disabled state, dedicated room-menu routing and vanilla/DLC/Workshop noninterference. #24 remains open. |
| TO-001 / FA-1 floor zoning | Toxicology laboratory floor glyph | **OWNER VISUAL APPROVED — exact approved-room-icon affine projection (2026-11-03); TS L3/L4 PENDING** | Owner approves the unchanged original flask SVG group coordinates rendered through one parent `matrix(3.3 1.2 -2.3 0.75 96 1.6)` to a 256x128 transparent SVG and reproducible 128x64 TS-private PNG. Approved source hash `76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec`, PNG128 hash `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4`, native PNG256 reproducible hash `a4083e3bef7dab0f9c0d629a42da517a51951729a42884f082eb9d8d5c7e8903`. Previously rejected alternative drawings remain rejected and archived. The approved projection has a reproducible 2048x2048 private tile-376 atlas from FA L2 (SHA256 `00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd`); not registered or installed. TS must independently validate private atlas routing, anchor/UV, zone colors, native and DLC compatibility and L4 before marking Issue #24 Done. |
| ART-001 | Original toxicology analyzer assets and interaction validation | **OWNER APPROVED SOURCE SUBMISSION — TWO FOUR-VIEW SETS STAGED; GAME GATE BLOCKED (2026-11-03)** | User authorized committing existing 1254x1254 mass spectrometer/digestion illustrations without redesign. Exact source images, eight 128x128 direction PNGs, noninstallable diagnostic 2048x1024 atlas and SHA manifest are stored under `assets/art001/review_20261103/`. This does NOT approve the present tabletop XML for the new full-base cabinet art, claim NW native/game visual acceptance, or change historical 3 PASS / 2 FAIL / 3 BLOCKED L4. TS must resolve standalone placement/interaction, 4-view continuity and L3/L4 before a production atlas or XML can be used. Old rejected V7–V10 remain historical. Keep Draft PR #14. |
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
