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
| ART-001 | Original toxicology analyzer assets and interaction validation | NEEDS_FIX — v7 native-bounds SVG source and cloud checks PASS; owner visual acceptance and corrected game L4 pending | Historical owner artifact `13124027790`: 3 PASS / 2 FAIL / 3 BLOCKED (placement/rotation failed; contact/occlusion, staff walking and vanilla coexistence blocked). Current source SHA `45d84ac7f6dcb10a18327810089acb752af42e53` on Draft PR #14 uses the active smooth SVG generator for preview AND offline staging; legacy pixel generator is deprecated and no longer called. v7 measures against owner-supplied native HEM NW bbox `(7,20,126,128)` and RIA NW `(8,43,108,127)`: ICP-MS frames occupy 107×106px and touch y=128; digestion frames occupy 99×85px and touch y=128. Three custom 64×64 RGBA icons are padded into the 60×60 safe area. Private workbench palette in `ModColorSets.xml` has five slots; no vanilla color set is modified. Workbench no longer relies on IconIndex. Exact preview Actions `41444867554` PASS, Verify `41444867580` PASS, CodeQL `41444867525` PASS; artifact `13140934442` (16 files, non-installable) outer SHA256 `cfbfcff2854817fe5a4dd4c2238f2060780011553a4816505c72bac8b63f1b28`, atlas SHA256 `a5bad4aae0c41b5775586bba358f1c3a5c42cc099a8e28b41c1e174e485559c3`. 2px per-cell transparent RGB edge bleed is source-tested, alpha preserved. PR #14 stays Draft, Issue #3 open. No install package generated; do not repeat accepted G1 R3 clinical L4. |
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
