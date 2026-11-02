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
| ART-001 | Original toxicology analyzer assets and interaction validation | NEEDS_FIX — editable SVG v6 source/CI preview PASS; owner visual review, native placement and staff use NOT TESTED | First owner test artifact `13124027790`: 3 PASS (launch/menu/labels), 2 FAIL (workbench placement/four-direction rotation), 3 BLOCKED (contact/occlusion, staff walking, vanilla equipment noninterference). Native private-attachment parent source candidate avoids vanilla tag changes; no corrected in-game evidence. D011/D012 require vanilla-style, smooth, unbranded player-visible laboratory equipment for all future labs; original-game HEM 248–251, RIA 252–255 and table 472–475 are read-only style references, never redistributed. Pixel-block original visuals rejected; installation-package workflow on HOLD. Draft #14 SVG v6 candidate SHA `f98a841484f6e834676b3b5fb3facc5d45ea3b50` adds original shell seams, compact vertical silhouette, small front LCD/rear ventilation, curved digestion safety hood, coherent four views, and mobile review image. Verify `41437792048`, CodeQL `41437792129`, Analyze Python and preview `41437783510` PASS. Preview-only artifact `13136802898` downloaded and audited: outer SHA256 `98cccbb700455e37cae2e060a1a052a85e50a281bfeeab7d513154c7fd9cb57a`, atlas SHA256 `7b17bef0ad4dc768c9008fba280ebe2e0fc0b630ba6a0b0abc7105074a0464a4`, exactly 14 original-art source/preview files, no install scripts or original game DLL/assets. A local reference comparison was checked but not published. Source style improved yet below full original HEM/RIA material richness; owner aesthetic acceptance and all v6 in-game L4 gates remain NOT TESTED. Preserve historical 3 PASS / 2 FAIL / 3 BLOCKED. PR #14 Draft, Issue #3 Open; no repeat G1 R3 clinical L4, no release or merge. |
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
