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
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress / NEEDS_FIX (original L4: 3 PASS, 2 FAIL, 3 BLOCKED; new source/CI/package PASS, owner visual + corrected L4 pending) | User first tested art package `13124027790` and reported launch/menu/labels PASS, workbench placement and four-direction rotation FAIL, occlusion/staff walking/vanilla equipment regression BLOCKED. Source-confirmed vanilla `AttachmentSlot.AllowedTags` mismatch led to additive private `OBJECT_ABCL_ART001_WORKBENCH` parent; original equipment tags and vanilla XML unchanged. Owner rejected oversized red/boxy aesthetics and branding; project-wide `ABCL-D011` and `docs/LAB_VISUAL_STANDARD.md` require neutral unbranded native-style visual/scale/rotation for every subsequent lab. G1 R3 clinical owner-reported L4 PASS is independent and never repeated for art-only changes. Original source first scaled/desaturated prototype `d0564863` was inspected and rejected internally as too tiny/generic; rewritten eight-frame original instrument source at `af82f65e` has separate upright mass-spectrometer analysis column/capped sample tray and low digestion safety hood/sample wells, distinct front/rear panels and coherent four directions. Current exact source `82182ceb7ad99d1ac59289ec7d5b78305e7a76da` adds a >=100 differing-pixels per-direction regression, no art geometry change. Verify 17 tests (1 existing skip), CodeQL, Analyze Python, preview and placement workflow PASS. Artifact `13130498961` downloaded, audited: outer SHA256 `76e7ed0442988def630e0a7cfc81e82b67498c241fabd60a3e3c4f598d2f72f2`, inner SHA256 `2494c318a0427fb88691e1e2d2369b772419588d003afb4b1a083f3ddced1a83`, exact source and original atlas hashes match, no original DLL/AES/vanilla override. EN/ZH player names unbranded. Owner aesthetic approval and corrected ART-only placement/rotation/tabletop contact/occlusion/staff walking/CBC coexistence all NOT TESTED; preserve historical 3 PASS/2 FAIL/3 BLOCKED and keep Issue #3 open and PR #14 Draft. |
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
