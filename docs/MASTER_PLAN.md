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
| ART-001 | Original toxicology analyzer assets and interaction validation | NEEDS_FIX — redesigned smooth original SVG source/CI PASS; owner visual gate and ART-only L4 not passed | Historical first owner ART L4 artifact `13124027790`: 3 PASS (game/menu/labels), 2 FAIL (lab table placement/rotation), 3 BLOCKED (scale/occlusion/staff/original equipment). Native `AttachmentSlot.AllowedTags` mismatch explains original-table placement; source-only private workbench remedy is retained without modifying original labels or medical XML. Owner requested fully vanilla-like, smooth nonpixelated original art (D011/D012) for all future laboratories. Original read-only references: HEM 248–251, RIA 252–255, workbench 472–475 in `objects_small_atlas.png`. Old box/pixel generators and their installer are rejected/held. Draft #14 now includes a 4x supersampled, antialiased, editable SVG source pipeline; latest `5b5f103cb9407edf14bb826d96151455de0b2547` v4 redraws two distinctive integrated devices (ion-source mass spectrometer and enclosed sample digester) with separate front/rear panels rather than tiny box-on-tray. Exact-source Verify `41434695557`, CodeQL, Analyze Python and preview `41434687791` all PASS. Actual preview-only artifact `13136265935` was downloaded and audited: outer ZIP SHA256 `6d458a1f5bad6b09435e2e548a41379068ddda808a2a06791fa15b7720e81ec5`, atlas SHA256 `ae7d6017f62ffe70d0455b06e5f9b47acfea372a3dbbbacbac1e85197028861f`, eight editable SVGs, no game or proprietary binary assets, not installable. Native atlas side-by-side visual comparison remains internal; v4 still less detailed than original, thus final owner visual acceptance and in-game placement/rotation/contact/occlusion/staff/vanilla-equipment compatibility remain NOT TESTED. No clinical G1 R3 retest, no merge/release; Issue #3 OPEN, PR #14 Draft. |
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
