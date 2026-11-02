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
| ART-001 | Original toxicology analyzer assets and interaction validation | NEEDS_FIX / Art redesign in progress (smooth SVG source-only preview gate; placement package HOLD; owner visual + L4 pending) | First owner ART L4 on artifact `13124027790`: launch/menu/labels 3 PASS; equipment bench placement and four-direction display 2 FAIL; occlusion, nearby staff walking and original equipment 3 BLOCKED. No new L4 performed. Original source review: `objects_small_atlas.png` is 2048×8192 with 128×128 cells; original `OBJECT_HEMATOLOGY_ANALYZER` slots 248–251, `OBJECT_RIA` 252–255 and original equipment bench 472–475. Earlier arbitrary 65×51 silhouette gate rejected as unproven; actual original alpha footprints vary by view and include shadows. Owner requested original-equipment visual fidelity and smooth, non-blocky/non-pixelated artwork for every future lab. D011/D012 and `docs/LAB_VISUAL_STANDARD.md` freeze unbranded player labels, internal ABCL namespaces, genuine tabletop proportions and anti-aliased original art. A new original edit-ready SVG pipeline (`tools/generate_art_001_svg.py`) produces 4x supersampled and Lanczos-downsampled 128×128 isometric sprites; `tests/test_art_001_svg.py` and a review-only GitHub preview workflow check source and antialias. Old installable procedural-pixel package workflow is intentionally on HOLD and no new user L4 requested. A nonpixel concept image is only a design proposal, not actual native asset evidence. Keep PR #14 Draft and Issue #3 open; do not copy game graphics or repeat separately accepted G1 R3 clinical L4. |
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
