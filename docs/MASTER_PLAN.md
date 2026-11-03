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
| TO-001 / FA-1 | Toxicology room-menu and zoning-floor glyphs | **SOURCE-ONLY FA L2 CANDIDATE — OWNER L4 VISUAL FAIL STILL OPEN (2026-11-03)** | FA reauthored separate editable 64x64 white-only room SVG/PNG (26x35 visible glyph) and separately authored 256x128 isometric floor SVG, exported to a 128x64 TS-private floor atlas slot. Original HEM/MIC/HIST read-only comparisons; no original assets committed, no background baked, no G1 logic modified. Exact source `4ea0c721e396f84a9fea96737f9a1f198ecb3051` icon/floor FA L2 Actions PASS. **TS runtime menu background, floor atlas routing, disabled/hover state and user visual L4 remain pending**. Issue #24 open, Draft PR #14 not mergeable by art L2. |
| ART-001 | Original toxicology analyzer assets and interaction validation | **NEEDS FULL VISUAL REDESIGN — V7 owner REJECTED (2026-11-02)** | The user compared V7 `review_mobile.png` with real vanilla equipment and rejected its flat, generic geometry and insufficient native-style material/detail; passing source/CI checks do NOT constitute art acceptance. Preserve native-reference and addon isolation work, 128px grid, namespaced XML, four-view contracts, preview tooling and PR #15 export verifier (incorporated into PR #14). Follow `docs/ART_001_NATIVE_QUALITY_REDESIGN.md` before any new package. Earlier owner ART-only L4 remains 3 PASS / 2 FAIL / 3 BLOCKED; corrected placement/rotation, staff interaction, DLC/Workshop remain untested. G1 R3 clinical L4 is separate and preserved; no automatic merge/release. |
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
