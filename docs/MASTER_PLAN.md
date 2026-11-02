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
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress (original source and refined visual preview PASS; art-only placement test package audited; actual L4 placement/interaction pending) | Draft PR #14 `feature/art-001-two-devices` delivers two originally authored instrument sprites (ICP-MS and sample-digestion station), 4 NW/NE/SE/SW frames each, reproducible 16×8 atlas, original icons, additive ABCL-only GameDBAsset/GameDBObject EN/ZH entries, offline stager, isolated installer and preview/test package workflows. First box-like art prototype was rejected; refined original-art preview from source `c5cefcccc28083ef06ef0ff12b638ce2dfb9b4c8` downloaded, viewed and inspected; atlas SHA256 `fa0b2e0bea72ab71b94d2752599bfc66fb642c0a64b748ca358ba9a2479e9249`. Art-only placement test ZIP (source `1fa723d336f95b27762a202a34aab9c64d003504`, Actions `41408148144`, artifact `13124027790`) compiled/staged via Python and independently audited: inner SHA256 `f39086a685c2ca557cec32e1538d874b4661792a5f68d3f7f8af7ee887b0196a`, 12 allowlisted files only, no original DLL/assets or G1 patient code. This is NOT Alpha, does NOT connect devices to procedures. Next: one disposable-save, single-pass original art placement and 4-direction preview L4 per `docs/ART_001_SINGLE_PASS_L4.md`; subsequent staff interaction/procedure routing remains NOT TESTED. G1 R3 gameplay acceptance on separate artifact `13117942292` is retained; never repeat R3 patient generation for this art-only gate. Keep Issue #3 open and PR #14 Draft. |
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
