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
| ART-001 | Original toxicology analyzer assets and interaction validation | In Progress / NEEDS_FIX (historical L4 3 PASS, 2 FAIL, 3 BLOCKED; isolated parent fix source/static/package PASS; corrected L4 NOT RUN) | Original owner test package `13124027790`, Actions `41408148144`, source `1fa723d336f95b27762a202a34aab9c64d003504`: game launch/menu/labels PASS; bench placement and four-direction rotation FAIL; occlusion, staff walking, original equipment noninterference BLOCKED. No screenshot/log or native error code supplied. Source-proven mismatch: child `AttachedToObject=true` uses private ABCL tags not accepted by original `OBJECT_TABLE_EQUIPMENT`/`OBJECT_TABLE_SQUERE` `AttachmentSlot.AllowedTags`; original table also forces attachment orientation, but separate rotation cause is not yet proven. Draft PR #14 adds isolated namespaced `OBJECT_ABCL_ART001_WORKBENCH` with only two private allowed tags and `ForcesAttachmentOrientation=false`, referencing existing installed original table texture rather than copying it. Fixed source candidate `b4c94125cfbba03c0b473de9678560ddf8356843`: Verify, CodeQL, Analyze Python, art-preview and placement-package workflows PASS. New exact-source audited package Actions `41410173007`, artifact `13125296497`, outer SHA256 `f8e9b8d36de8d2fbb419b1db3dae4dde7f1cb08e788e7787d9a9036b47697797`, inner SHA256 `1ab3b3ceba2ce8fcdbd34778af9d0710d717e95bf1a1c23e062d08f0429d9770`; BUILD_INFO SHA matches; no DLL/key/vanilla overrides. Corrected ART-only L4 placement/rotation is **NOT YET TESTED**, so no past FAIL/BLOCKED field was converted to PASS. All original laboratory/CBC and G1 R3 clinical code are untouched; R3 owner-reported L4 PASS on separate artifact `13117942292` remains accepted, do not retest. Keep Issue #3 open, PR #14 Draft; no merge/release or broad compatibility claim. |
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
